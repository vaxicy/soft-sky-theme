# Generate Soft Sky Theme extension icon (128x128 PNG)
# Code-first: layered deep-blue sky gradient + warm cream sun + soft morning clouds.
from PIL import Image, ImageDraw

SIZE = 128
OUT = "icon.png"

TOP = (20, 32, 48)        # deep blue sky
BOT = (58, 84, 120)       # lighter morning blue
SUN = (255, 227, 176)     # warm cream sunrise (FFE3B0)
SUN_HI = (255, 241, 213)  # warm cream highlight (FFF1D5)
CLOUD = (158, 198, 243)   # sky blue (9EC6F3)
CLOUD_SOFT = (189, 221, 228)  # mist blue (BDDDE4)

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Vertical gradient background
for y in range(SIZE):
    t = y / (SIZE - 1)
    r = int(TOP[0] + (BOT[0] - TOP[0]) * t)
    g = int(TOP[1] + (BOT[1] - TOP[1]) * t)
    b = int(TOP[2] + (BOT[2] - TOP[2]) * t)
    d.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

# Sun glow (soft halo)
for radius, alpha in [(42, 36), (34, 52), (27, 74)]:
    x0 = 92 - radius
    y0 = 30 - radius
    x1 = 92 + radius
    y1 = 30 + radius
    d.ellipse([x0, y0, x1, y1], fill=(SUN[0], SUN[1], SUN[2], alpha))

# Sun core
d.ellipse([80, 18, 104, 42], fill=SUN_HI)

# Clouds (sky blue, low on the horizon)
def cloud(cx, cy, w, h, color, alpha):
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    dl.ellipse([cx - w * 0.35, cy - h * 0.45, cx + w * 0.35, cy + h * 0.55], fill=(*color, alpha))
    dl.ellipse([cx - w * 0.55, cy - h * 0.05, cx + w * 0.55, cy + h * 0.75], fill=(*color, alpha))
    dl.ellipse([cx - w * 0.15, cy - h * 0.55, cx + w * 0.25, cy + h * 0.25], fill=(*color, alpha))
    img.alpha_composite(layer, (0, 0))

cloud(38, 102, 58, 26, CLOUD, 200)
cloud(88, 116, 64, 28, CLOUD_SOFT, 185)

# Code braces accent in sky blue (minimal, geometric — no letters)
d.arc([22, 52, 52, 82], start=40, end=320, fill=(159, 179, 223, 235), width=5)
d.arc([76, 52, 106, 82], start=220, end=140, fill=(159, 179, 223, 235), width=5)

img.save(OUT, "PNG")
print("saved", OUT, img.size, img.mode)
