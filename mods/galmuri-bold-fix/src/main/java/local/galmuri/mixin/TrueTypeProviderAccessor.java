package local.galmuri.mixin;
import com.mojang.blaze3d.font.TrueTypeGlyphProvider;
import org.lwjgl.util.freetype.FT_Face;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
@Mixin(value=TrueTypeGlyphProvider.class, remap=false)
public interface TrueTypeProviderAccessor {
 @Accessor("face") FT_Face galmuri$getFace();
}
