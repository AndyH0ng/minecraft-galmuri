package local.galmuri.font;
import com.mojang.blaze3d.font.GlyphInfo;
public record GalmuriGlyphInfo(float advance) implements GlyphInfo {
 public float getAdvance() { return advance; }
 public float getBoldOffset() { return 0.5f; }
}
