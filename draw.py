#!/usr/bin/env python3
"""Render entry.png (1024x1024): the world news of Tuesday 17 Nov 2026 in one image.

Original drawing code using only Pillow shapes and system Noto Sans fonts.
No external images, no network. Deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto/"

BG = (247, 243, 232)        # newspaper cream
INK = (17, 17, 17)
WHITE = (255, 255, 255)
SUB = (55, 55, 55)

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

BOLD = "NotoSans-Bold.ttf"
BLACK = "NotoSans-Black.ttf"
COND_BOLD = "NotoSans-CondensedBold.ttf"
REG = "NotoSans-Regular.ttf"

def fit(draw, text, name, max_size, min_size, max_width):
    """Largest font (<= max_size) whose text fits max_width."""
    size = max_size
    while size > min_size:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(name, min_size)

def center(draw, cx, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return y + f.size

# ---------------------------------------------------------------- icons

def icon_bridge(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(219, 234, 254))
    # sea
    sea_y = y0 + (y1 - y0) * 0.68
    d.rectangle([x0, sea_y, x1, y1], fill=(37, 99, 235))
    for i in range(3):  # wave dashes
        wy = sea_y + 14 + i * 18
        for wx in range(int(x0 + 12), int(x1 - 30), 52):
            d.line([wx, wy, wx + 24, wy], fill=(147, 197, 253), width=4)
    deck_y = y0 + (y1 - y0) * 0.52
    mid = (x0 + x1) / 2
    # towers
    for tx in (x0 + (x1 - x0) * 0.22, x0 + (x1 - x0) * 0.78):
        d.rectangle([tx - 7, deck_y - 78, tx + 7, sea_y], fill=(75, 85, 99))
    # cables: from each tower top down to the deck ends and to the gap
    for tx in (x0 + (x1 - x0) * 0.22, x0 + (x1 - x0) * 0.78):
        pass
    lt = (x0 + (x1 - x0) * 0.22, deck_y - 78)
    rt = (x0 + (x1 - x0) * 0.78, deck_y - 78)
    d.line([lt[0], lt[1], x0 + 4, deck_y - 4], fill=(75, 85, 99), width=4)
    d.line([lt[0], lt[1], mid - 58, deck_y - 4], fill=(75, 85, 99), width=4)
    d.line([rt[0], rt[1], mid + 58, deck_y - 4], fill=(75, 85, 99), width=4)
    d.line([rt[0], rt[1], x1 - 4, deck_y - 4], fill=(75, 85, 99), width=4)
    # intact deck, left and right of the gap
    d.rectangle([x0, deck_y, mid - 58, deck_y + 14], fill=(31, 41, 55))
    d.rectangle([mid + 58, deck_y, x1, deck_y + 14], fill=(31, 41, 55))
    # broken span, tilted down into the gap
    d.polygon([(mid - 58, deck_y + 2), (mid + 46, deck_y + 12),
               (mid + 40, deck_y + 30), (mid - 52, deck_y + 18)], fill=(185, 28, 28))
    # explosion star at the break
    cx, cy, r = mid, deck_y - 26, 30
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=(245, 158, 11), outline=(185, 28, 28))

def icon_quad(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(224, 242, 241))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = min(x1 - x0, y1 - y0) * 0.21
    off = r * 1.08
    cells = [("US", (30, 58, 138), WHITE, cx - off, cy - off),
             ("JP", (255, 255, 255), (185, 28, 28), cx + off, cy - off),
             ("IN", (249, 115, 22), WHITE, cx - off, cy + off),
             ("AU", (2, 132, 199), WHITE, cx + off, cy + off)]
    f = font(BOLD, int(r * 0.78))
    for label, fillc, textc, ccx, ccy in cells:
        d.ellipse([ccx - r, ccy - r, ccx + r, ccy + r], fill=fillc, outline=INK, width=4)
        tw = d.textlength(label, font=f)
        d.text((ccx - tw / 2, ccy - f.size * 0.62), label, font=f, fill=textc)

def icon_drone(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(254, 226, 226))
    # --- drone, clean front view, upper right
    cx, cy = x0 + w * 0.60, y0 + h * 0.20
    for sx in (-1, 1):  # arms + rotor discs
        rx = cx + sx * w * 0.26
        d.line([cx, cy, rx, cy - 6], fill=INK, width=7)
        d.ellipse([rx - 27, cy - 15, rx + 27, cy + 3], outline=INK, width=6)
    d.rounded_rectangle([cx - 30, cy - 12, cx + 30, cy + 14], radius=10, fill=INK)
    d.line([cx - 18, cy + 14, cx - 24, cy + 30], fill=INK, width=5)
    d.line([cx + 18, cy + 14, cx + 24, cy + 30], fill=INK, width=5)
    d.ellipse([cx - 8, cy + 16, cx + 8, cy + 32], fill=(185, 28, 28), outline=INK, width=3)
    # --- radar dish, lower left: bowl + mast + base
    fx, fy = x0 + w * 0.30, y1 - h * 0.30   # dish focal point
    d.arc([fx - 52, fy - 10, fx + 30, fy + 62], start=250, end=70, fill=INK, width=11)
    d.line([fx - 34, fy + 44, fx - 6, fy + 16], fill=INK, width=8)
    base_y = y1 - h * 0.07
    d.line([fx - 20, base_y, fx - 14, fy + 40], fill=INK, width=8)
    d.line([fx - 44, base_y, fx + 4, base_y], fill=INK, width=8)
    d.ellipse([fx - 7, fy - 7, fx + 7, fy + 7], fill=(185, 28, 28))
    # --- red signal arcs from the dish up toward the drone
    for rr in (30, 52, 74):
        d.arc([fx - rr, fy - rr, fx + rr, fy + rr], start=255, end=345,
              fill=(220, 38, 38), width=6)

def icon_chip(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(236, 252, 203))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = min(x1 - x0, y1 - y0) * 0.30
    green = (101, 163, 13)
    # pins
    for i in range(-1, 2):
        o = i * s * 0.55
        d.line([cx + o, y0 + 8, cx + o, cy - s], fill=INK, width=7)
        d.line([cx + o, cy + s, cx + o, y1 - 8], fill=INK, width=7)
        d.line([x0 + 8, cy + o, cx - s, cy + o], fill=INK, width=7)
        d.line([cx + s, cy + o, x1 - 8, cy + o], fill=INK, width=7)
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=16, fill=green, outline=INK, width=5)
    inner = s * 0.58
    d.rounded_rectangle([cx - inner, cy - inner, cx + inner, cy + inner], radius=10,
                        outline=WHITE, width=5)
    f = font(BLACK, int(s * 0.85))
    tw = d.textlength("AI", font=f)
    d.text((cx - tw / 2, cy - f.size * 0.60), "AI", font=f, fill=WHITE)

def draw_crab(d, cx, cy, s, body=(220, 38, 38), dark=(153, 27, 27)):
    # legs: 3 simple bent lines per side
    lw = max(3, int(s * 0.11))
    for side in (-1, 1):
        for dy in (-0.14, 0.06, 0.26):
            lx, ly = cx + side * s * 0.44, cy + s * dy
            kx, ky = lx + side * s * 0.30, ly + s * 0.16
            d.line([lx, ly, kx, ky], fill=dark, width=lw)
            d.line([kx, ky, kx - side * s * 0.10, ky + s * 0.24], fill=dark, width=lw)
    # claws
    for side in (-1, 1):
        ccx, ccy = cx + side * s * 0.52, cy - s * 0.38
        d.ellipse([ccx - s * 0.20, ccy - s * 0.16, ccx + s * 0.20, ccy + s * 0.16], fill=body, outline=dark, width=3)
    # body
    d.ellipse([cx - s * 0.55, cy - s * 0.34, cx + s * 0.55, cy + s * 0.34], fill=body, outline=dark, width=3)
    # eyes
    for side in (-1, 1):
        ex = cx + side * s * 0.18
        d.line([ex, cy - s * 0.30, ex, cy - s * 0.52], fill=dark, width=max(3, int(s * 0.09)))
        d.ellipse([ex - s * 0.08, cy - s * 0.64, ex + s * 0.08, cy - s * 0.48], fill=INK)

def icon_crabs(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(254, 243, 199))  # sand
    # road strip across the middle
    road_y0 = y0 + (y1 - y0) * 0.34
    road_y1 = y0 + (y1 - y0) * 0.72
    d.rectangle([x0, road_y0, x1, road_y1], fill=(107, 114, 128))
    for wx in range(int(x0 + 16), int(x1 - 40), 74):  # dashes
        d.rectangle([wx, (road_y0 + road_y1) / 2 - 4, wx + 38, (road_y0 + road_y1) / 2 + 4], fill=WHITE)
    # sea on the right
    d.rectangle([x1 - (x1 - x0) * 0.20, y0, x1, y1], fill=(37, 99, 235))
    for i in range(4):
        wy = y0 + 24 + i * ((y1 - y0) / 4)
        d.line([x1 - (x1 - x0) * 0.16, wy, x1 - 18, wy], fill=(147, 197, 253), width=5)
    # crabs marching right, toward the sea (all fully inside the box)
    draw_crab(d, x0 + (x1 - x0) * 0.18, road_y0 + (road_y1 - road_y0) * 0.40, 44)
    draw_crab(d, x0 + (x1 - x0) * 0.42, road_y0 + (road_y1 - road_y0) * 0.58, 56)
    draw_crab(d, x0 + (x1 - x0) * 0.64, road_y0 + (road_y1 - road_y0) * 0.36, 38)
    draw_crab(d, x0 + (x1 - x0) * 0.28, y0 + (y1 - y0) * 0.86, 30)
    draw_crab(d, x0 + (x1 - x0) * 0.55, y0 + (y1 - y0) * 0.87, 26)

# ---------------------------------------------------------------- panels

STORIES = [
    {"tag": "WAR", "accent": (0, 91, 187), "icon": icon_bridge,
     "headline": ["BRIDGES HIT IN", "UKRAINE WAR"],
     "sub": ["Ukraine damages Crimea bridge;", "Kyiv bridges struck"]},
    {"tag": "DIPLOMACY", "accent": (15, 118, 110), "icon": icon_quad,
     "headline": ["QUAD LEADERS", "MEET IN MANILA"],
     "sub": ["First summit since 2024;", "mineral deals agreed"]},
    {"tag": "MIDDLE EAST", "accent": (185, 28, 28), "icon": icon_drone,
     "headline": ["IRAN DRONES TARGET", "BAHRAIN BASE"],
     "sub": ["Bahrain says drones intercepted;", "no casualties reported"]},
    {"tag": "BUSINESS", "accent": (101, 163, 13), "icon": icon_chip,
     "headline": ["NVIDIA SALES", "DOUBLE AGAIN"],
     "sub": ["Revenue hits $115.8 billion", "on AI demand"]},
    {"tag": "NATURE", "accent": (220, 38, 38), "icon": icon_crabs,
     "headline": ["RED CRABS MARCH TO SEA"],
     "sub": ["Tens of millions cross Christmas Island roads"]},
]

def panel(d, box, story, icon_w):
    x0, y0, x1, y1 = box
    accent = story["accent"]
    d.rounded_rectangle(box, radius=14, fill=WHITE, outline=accent, width=4)
    # icon area
    pad = 12
    ibox = [x0 + pad, y0 + pad, x0 + pad + icon_w, y1 - pad]
    d.rounded_rectangle(ibox, radius=10, outline=accent, width=2)
    # clip icon drawing to its box by drawing on a temp image
    tmp = Image.new("RGB", (int(ibox[2] - ibox[0]), int(ibox[3] - ibox[1])), WHITE)
    td = ImageDraw.Draw(tmp)
    story["icon"](td, [0, 0, tmp.width, tmp.height])
    return tmp, ibox
    # (paste handled by caller)

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- top banner
    d.rectangle([0, 0, W, 148], fill=INK)
    d.rectangle([0, 148, W, 156], fill=(245, 158, 11))
    f_title = fit(d, "TUESDAY 17 NOVEMBER 2026", BLACK, 58, 30, W - 40)
    center(d, W / 2, 16, "TUESDAY 17 NOVEMBER 2026", f_title, WHITE)
    f_sub = font(COND_BOLD, 30)
    center(d, W / 2, 92, "T H E   W O R L D   I N   O N E   I M A G E", f_sub, (245, 158, 11))

    margin, gap = 20, 14
    top = 172
    footer_h = 30
    area_bottom = H - margin - footer_h
    row_h = [(area_bottom - top - gap * 2) // 3] * 3
    row_h[2] += (area_bottom - top - gap * 2) - sum(row_h)
    col_w = (W - margin * 2 - gap) // 2

    positions = []
    y = top
    for r in range(3):
        if r < 2:
            positions.append([margin, y, margin + col_w, y + row_h[r]])
            positions.append([margin + col_w + gap, y, W - margin, y + row_h[r]])
        else:
            positions.append([margin, y, W - margin, y + row_h[r]])
        y += row_h[r] + gap

    for story, box in zip(STORIES, positions):
        x0, y0, x1, y1 = box
        accent = story["accent"]
        wide = (x1 - x0) > col_w + 10
        icon_w = 300 if wide else 168
        tmp, ibox = panel(d, box, story, icon_w)
        img.paste(tmp, (int(ibox[0]), int(ibox[1])))
        d.rounded_rectangle(ibox, radius=10, outline=accent, width=2)

        tx = ibox[2] + 18
        tw = x1 - tx - 14
        # tag pill
        f_tag = font(COND_BOLD, 21)
        tag_w = d.textlength(story["tag"], font=f_tag) + 22
        d.rounded_rectangle([tx, y0 + 14, tx + tag_w, y0 + 46], radius=8, fill=accent)
        d.text((tx + 11, y0 + 18), story["tag"], font=f_tag, fill=WHITE)
        # headline
        hy = y0 + 56
        max_head = 46 if not wide else 54
        for line in story["headline"]:
            f_h = fit(d, line, BLACK, max_head, 24, tw)
            d.text((tx, hy), line, font=f_h, fill=INK)
            hy += f_h.size + 6
        # sublabel
        f_s = font(REG, 24 if not wide else 27)
        sy = hy + 6
        for line in story["sub"]:
            f_line = fit(d, line, REG, f_s.size, 16, tw)
            d.text((tx, sy), line, font=f_line, fill=SUB)
            sy += f_line.size + 5

    # ---- footer
    f_f = font(COND_BOLD, 20)
    center(d, W / 2, H - margin - footer_h + 4,
           "SOURCES: ZARK NEWS - WHITE HOUSE - JUST SECURITY - MOTLEY FOOL - FOX WEATHER",
           f_f, (100, 100, 100))

    img.save("entry.png", format="PNG")
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
