package local.galmuri.mixin;
import com.mojang.blaze3d.font.GlyphInfo;
import local.galmuri.font.GalmuriGlyphInfo;
import com.mojang.blaze3d.font.TrueTypeGlyphProvider;
import org.lwjgl.util.freetype.FT_Face;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;
@Mixin(targets="com.mojang.blaze3d.font.TrueTypeGlyphProvider$Glyph", remap=false)
public abstract class GalmuriBoldMixin {
 @Redirect(method="<init>", at=@At(value="INVOKE", target="Lcom/mojang/blaze3d/font/GlyphInfo;simple(F)Lcom/mojang/blaze3d/font/GlyphInfo;"), require=1)
 private GlyphInfo galmuri$adjustBold(float advance, TrueTypeGlyphProvider owner, float bearingX, float bearingY, int width, int height, float rawAdvance, int index) {
  FT_Face face=((TrueTypeProviderAccessor)(Object)owner).galmuri$getFace();
  String family=face.family_nameString();
  return family != null && family.startsWith("Galmuri") ? new GalmuriGlyphInfo(advance) : GlyphInfo.simple(advance);
 }
}
