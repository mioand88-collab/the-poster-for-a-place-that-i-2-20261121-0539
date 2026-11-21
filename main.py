#!/usr/bin/env python3
"""VELMARA — a travel poster for a place that does not exist.

Draws a 1024x1024 travel poster: a lantern-lit cliff city floating above a
sea of clouds at dusk, with the place's name set in large type. Deterministic:
no network, no randomness, no time dependence. Writes /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png).
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
NAME = "VELMARA"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

# Palette: dusk indigo -> violet -> gold horizon -> pale cloud sea.
SKY_TOP = (24, 28, 66)
SKY_MID = (74, 62, 118)
SKY_LOW = (214, 128, 84)
HORIZON = (250, 196, 120)
CLOUD_LIGHT = (246, 226, 205)
CLOUD_SHADOW = (196, 170, 196)
CITY_DARK = (22, 20, 48)
LANTERN = (255, 196, 96)
LANTERN_HOT = (255, 232, 170)
GOLD = (242, 180, 90)
INK = (26, 22, 54)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient():
    """Vertical dusk gradient with a warm band at the horizon."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        if t < 0.45:
            c = lerp(SKY_TOP, SKY_MID, t / 0.45)
        elif t < 0.72:
            c = lerp(SKY_MID, SKY_LOW, (t - 0.45) / 0.27)
        else:
            c = lerp(SKY_LOW, HORIZON, (t - 0.72) / 0.28)
        for x in range(W):
            px[x, y] = c
    return img


def draw_stars(img):
    """A sparse field of early-evening stars in the upper sky."""
    d = ImageDraw.Draw(img)
    state = 777
    for _ in range(90):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        sx = 20 + state % (W - 40)
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        sy = 20 + state % 300
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        r = 1 + state % 2
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        bright = 150 + state % 105
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(bright, bright, min(255, bright + 20)))
    return img


def draw_birds(img):
    """Three small distant birds crossing the sunset sky."""
    d = ImageDraw.Draw(img)
    for (bx, by, s) in [(640, 420, 14), (690, 395, 11), (610, 380, 9)]:
        d.arc([bx - s, by - s // 2, bx, by + s // 2], start=200, end=340,
              fill=(40, 32, 70), width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], start=200, end=340,
              fill=(40, 32, 70), width=3)
    return img


def add_sun(img):
    """Paint the low sun with a halo using layered blurred ellipses."""
    halo = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(halo)
    hd.ellipse([660 - 170, 540 - 170, 660 + 170, 540 + 170], fill=140)
    halo = halo.filter(ImageFilter.GaussianBlur(90))
    img = Image.composite(Image.new("RGB", (W, H), (255, 176, 92)), img, halo)
    d = ImageDraw.Draw(img)
    d.ellipse([660 - 66, 540 - 66, 660 + 66, 540 + 66], fill=(255, 204, 110))
    d.ellipse([660 - 50, 540 - 50, 660 + 50, 540 + 50], fill=(255, 226, 150))
    return img


def cloud_band(img, y_base, height, light, shadow, seed):
    """One band of soft cloud puffs, drawn as overlapping blurred ellipses."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Deterministic pseudo-random positions from a fixed seed.
    state = seed
    x = -60
    while x < W + 80:
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        rw = 120 + state % 160
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        rh = int(height * (0.45 + (state % 100) / 200.0))
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        dy = (state % 40) - 20
        d.ellipse([x, y_base + dy - rh, x + rw, y_base + dy + rh],
                  fill=light + (235,))
        x += rw // 2
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"),
              (0, 0))
    return img


def draw_city(img):
    """The cliff city of Velmara: terraced rock, towers, glowing windows."""
    d = ImageDraw.Draw(img)
    # Main cliff mass, left-centre, rising out of the clouds.
    cliff = [(150, 1024), (150, 640), (210, 560), (300, 520), (380, 470),
             (470, 470), (520, 520), (560, 640), (560, 1024)]
    d.polygon(cliff, fill=CITY_DARK)
    # Second, smaller cliff on the right.
    cliff2 = [(760, 1024), (760, 700), (810, 640), (880, 620), (930, 660),
              (950, 760), (950, 1024)]
    d.polygon(cliff2, fill=(30, 26, 58))
    # Terraced ledges on the main cliff.
    for (x0, y0, x1) in [(170, 620, 520), (210, 560, 470), (300, 500, 430)]:
        d.rectangle([x0, y0, x1, y0 + 10], fill=(34, 30, 66))
    # Towers with pointed roofs.
    towers = [(225, 560, 46, 150), (330, 500, 40, 190), (420, 500, 36, 150),
              (790, 640, 34, 120), (880, 620, 40, 150)]
    for (tx, ty, tw, th) in towers:
        d.rectangle([tx, ty - th, tx + tw, ty], fill=CITY_DARK)
        d.polygon([(tx - 6, ty - th), (tx + tw // 2, ty - th - 52),
                   (tx + tw + 6, ty - th)], fill=(30, 26, 60))
    # The great lantern tower: tallest, crowned with a glowing beacon.
    d.rectangle([300, 300, 356, 500], fill=(26, 22, 52))
    d.polygon([(294, 300), (328, 226), (362, 300)], fill=(32, 28, 64))
    d.ellipse([316, 196, 340, 220], fill=LANTERN_HOT)
    # Arched bridge between the cliffs.
    d.arc([520, 640, 780, 860], start=200, end=340, fill=(38, 32, 72), width=14)
    # Windows: small warm rectangles, deterministic grid with fixed pattern.
    windows = []
    for gx in range(0, 14):
        for gy in range(0, 9):
            if (gx * 7 + gy * 11) % 5 in (0, 1):
                windows.append((gx, gy))
    for (gx, gy) in windows:
        wx = 185 + gx * 24
        wy = 520 + gy * 26
        if 170 < wx < 540 and 420 < wy < 980:
            d.rectangle([wx, wy, wx + 9, wy + 13], fill=LANTERN)
    for gx in range(0, 6):
        for gy in range(0, 5):
            if (gx * 5 + gy * 3) % 3 == 0:
                wx = 775 + gx * 26
                wy = 660 + gy * 30
                d.rectangle([wx, wy, wx + 8, wy + 11], fill=LANTERN)
    # Lantern glow dots along the bridge.
    for i in range(6):
        bx = 545 + i * 38
        by = 700 - int(38 * (1 - ((bx - 545) / 230.0) ** 2)) + 8
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=LANTERN_HOT)
    return img


def add_beacon_glow(img):
    """Warm halo around the great lantern tower's beacon."""
    halo = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(halo)
    hd.ellipse([328 - 60, 208 - 60, 328 + 60, 208 + 60], fill=160)
    halo = halo.filter(ImageFilter.GaussianBlur(40))
    return Image.composite(Image.new("RGB", (W, H), (255, 200, 110)), img, halo)


def draw_frame(img):
    """Thin double gold frame, classic travel-poster finish."""
    d = ImageDraw.Draw(img)
    d.rectangle([18, 18, W - 19, H - 19], outline=(242, 180, 90), width=3)
    d.rectangle([30, 30, W - 31, H - 31], outline=(255, 240, 214), width=1)
    return img


def draw_name(img):
    """VELMARA in large serif capitals, centred in the upper sky."""
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, 118)
    text = NAME
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2 - bbox[0]
    y = 96
    # Soft shadow for legibility against the sky.
    d.text((x + 4, y + 5), text, font=font, fill=(18, 16, 44))
    d.text((x, y), text, font=font, fill=(255, 240, 214))
    # Thin gold rules flanking a small diamond under the name.
    d.line([(x, y + 148), (x + tw, y + 148)], fill=GOLD, width=3)
    d.polygon([(512, y + 138), (522, y + 148), (512, y + 158), (502, y + 148)],
              fill=GOLD)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = sky_gradient()
    img = draw_stars(img)
    img = add_sun(img)
    img = draw_birds(img)
    # Distant cloud sea first (behind the city), then city, then foreground clouds.
    img = cloud_band(img, 700, 90, CLOUD_SHADOW, CLOUD_SHADOW, seed=12345)
    img = draw_city(img)
    img = add_beacon_glow(img)
    img = cloud_band(img, 880, 130, CLOUD_LIGHT, CLOUD_SHADOW, seed=98765)
    img = cloud_band(img, 960, 90, (255, 244, 224), CLOUD_SHADOW, seed=4242)
    img = draw_name(img)
    img = draw_frame(img)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
