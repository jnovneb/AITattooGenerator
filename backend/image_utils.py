from PIL import Image, ImageEnhance
import os

def overlay_tattoo(base_path, tattoo_path, x, y, scale, rotation, opacity):
    base = Image.open(base_path).convert("RGBA")
    tattoo = Image.open(tattoo_path).convert("RGBA")

    w, h = tattoo.size
    tattoo = tattoo.resize((int(w*scale), int(h*scale)))
    tattoo = tattoo.rotate(rotation, expand=True)
    alpha = tattoo.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    tattoo.putalpha(alpha)

    base.paste(tattoo, (x, y), tattoo)
    out_path = f"static/overlays/overlay_{os.path.basename(base_path)}"
    base.save(out_path)
    return out_path
