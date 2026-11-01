#!/usr/bin/env python3
"""Build with Java 25 and dependencies from an installed Minecraft 26.3 client."""
import argparse
import json
import os
import re
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minecraft-dir", required=True, type=Path,
                        help="Minecraft directory containing versions/ and libraries/")
    parser.add_argument("--java-home", type=Path, help="Optional JDK 25+ directory")
    args = parser.parse_args()
    java_home = args.java_home or (Path(os.environ["JAVA_HOME"]) if os.environ.get("JAVA_HOME") else None)
    java_home = java_home.expanduser() if java_home else None
    javac = str(java_home / "bin/javac") if java_home else "javac"
    java = str(java_home / "bin/java") if java_home else "java"
    version_output = subprocess.check_output([javac, "-version"], stderr=subprocess.STDOUT, text=True)
    match = re.search(r"javac (\d+)", version_output)
    if not match or int(match.group(1)) < 25:
        parser.error("JDK 25+ is required; select it via --java-home or JAVA_HOME")
    base = Path(__file__).resolve().parent
    root = args.minecraft_dir.expanduser().resolve()
    clients = []
    for candidate in sorted((root / "versions").rglob("*.jar")):
        with ZipFile(candidate) as jar:
            if "version.json" not in jar.namelist():
                continue
            version = json.loads(jar.read("version.json"))
            if version.get("id") == "26.3" and "com/mojang/blaze3d/font/GlyphInfo.class" in jar.namelist():
                clients.append(candidate)
    if not clients:
        parser.error("Minecraft 26.3 client JAR not found; launch the installed 26.3 Fabric profile first")
    libraries = sorted((root / "libraries").rglob("*.jar"))
    if not libraries:
        parser.error("Minecraft libraries not found")
    classpath = os.pathsep.join(str(p) for p in [clients[0], *libraries])
    resources = base / "src/main/resources"
    metadata = json.loads((resources / "fabric.mod.json").read_text())
    mixins = json.loads((resources / "galmuri-bold-fix.mixins.json").read_text())
    output = base / "dist" / ("galmuri-bold-fix-" + metadata["version"] + ".jar")
    output.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="galmuri-build-") as temp:
        temp = Path(temp)
        classes = temp / "classes"
        classes.mkdir()
        sources = sorted((base / "src/main/java").rglob("*.java"))
        subprocess.run([javac, "--release", "25", "-proc:none", "-cp", classpath,
                        "-d", str(classes), *map(str, sources)], check=True)
        prefix = mixins["package"].replace(".", "/") + "/"
        actual = {p.relative_to(classes).as_posix() for p in classes.rglob("*.class")
                  if p.relative_to(classes).as_posix().startswith(prefix)}
        expected = {prefix + name + ".class" for name in mixins["client"]}
        if actual != expected:
            raise RuntimeError("Mixin package must contain only declared Mixin classes")
        verify = temp / "Verify.java"
        verify.write_text("""import local.galmuri.font.GalmuriGlyphInfo;
import com.mojang.blaze3d.font.GlyphInfo;
public class Verify {
 public static void main(String[] args) {
  for (float advance : new float[]{3, 5, 8, 11}) {
   GlyphInfo original = GlyphInfo.simple(advance);
   GlyphInfo fixed = new GalmuriGlyphInfo(advance);
   if (fixed.getAdvance() != original.getAdvance()
       || fixed.getShadowOffset() != original.getShadowOffset()
       || fixed.getBoldOffset() != 0.5f
       || fixed.getAdvance(true) != advance + 0.5f) throw new AssertionError();
  }
  System.out.println("PASS: regular metrics and shadows preserved; bold offset 0.5");
 }
}
""")
        verify_classes = temp / "verify"
        verify_classes.mkdir()
        test_classpath = os.pathsep.join([str(classes), classpath])
        subprocess.run([javac, "--release", "25", "-proc:none", "-cp", test_classpath,
                        "-d", str(verify_classes), str(verify)], check=True)
        subprocess.run([java, "-cp", str(verify_classes) + os.pathsep + test_classpath,
                        "Verify"], check=True)
        with ZipFile(output, "w", ZIP_DEFLATED) as jar:
            for path in sorted(classes.rglob("*.class")):
                jar.write(path, path.relative_to(classes).as_posix())
            for path in sorted(resources.rglob("*")):
                if path.is_file():
                    jar.write(path, path.relative_to(resources).as_posix())
            jar.write(base.parents[1] / "LICENSE", "LICENSE")
        with ZipFile(output) as jar:
            if jar.testzip() is not None:
                raise RuntimeError("Invalid output archive")
    print(output)


if __name__ == "__main__":
    main()
