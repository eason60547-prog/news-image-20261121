#!/usr/bin/env python3
"""Draw the 21 Nov 2026 world-news front page, 1024x1024, PIL only.

Layout is my own: masthead, one lead panel with a night-skyline
illustration, three stories in a row, an ALSO strip and a source line.
All text is drawn with DejaVu fonts so nothing is garbled.
News verified from AP / Reuters / Kyiv Independent on 21 Nov 2026
(see the README for the source notes):
- Russian ballistic missiles hit Kryvyi Rih, Zelenskyy's hometown:
  a boy of 7 and a 20-year-old paramedic killed, 60 wounded.
- Mexico captures FBI most-wanted cartel boss "El Chapo Isidro"
  in Sinaloa with US help; 11 killed in the violence that followed.
- COP31 climate talks in Antalya run into overtime with no deal;
  fossil fuels still missing from the draft.
- Markets plunge on the AI sell-off: S&P 500 -3.7%, Nasdaq wipes
  out its 2026 gains, Nikkei -5.06%.
- Also: Russian missiles land in Poland, NATO calls it a violation;
  rights groups urge sanctions after the World Court's Myanmar
  genocide ruling; Iran strikes three tankers.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (250, 246, 238)
INK = (18, 24, 38)
NAVY = (16, 34, 64)
NIGHT = (14, 22, 44)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (90, 96, 108)
BLUE = (36, 84, 158)
GREEN = (46, 120, 70)
AMBER = (255, 176, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, x, y, w, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y), text, font=fnt, fill=fill)


def burst(draw, cx, cy, r, fill):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)
    draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 230, 150))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- masthead ---
d.rectangle([0, 0, W, 116], fill=NAVY)
center(d, 0, 14, W, "THE WORLD IN ONE DAY", font(SERIF, 52), (255, 255, 255))
center(d, 0, 74, W, "SATURDAY  •  21 NOVEMBER 2026", font(SANS_B, 26), GOLD)
d.rectangle([0, 116, W, 122], fill=RED)

# --- lead panel: night sky over Kryvyi Rih ---
d.rectangle([28, 138, 996, 480], fill=NIGHT)
# horizon glow
for i in range(26):
    d.rectangle([28, 440 - i, 996, 441 - i],
                fill=(14 + i * 3, 22 + i * 2, 44 + i))
# missile trails
d.line([640, 150, 830, 250], fill=(255, 220, 160), width=4)
d.line([700, 150, 900, 300], fill=(255, 220, 160), width=3)
d.ellipse([636, 146, 648, 158], fill=(255, 240, 200))
d.ellipse([696, 146, 708, 158], fill=(255, 240, 200))
# blast bursts
burst(d, 830, 250, 42, AMBER)
burst(d, 900, 300, 30, AMBER)
# skyline with one broken tower
d.rectangle([28, 410, 996, 480], fill=(8, 12, 26))
towers = [(640, 46, 110), (700, 34, 70), (760, 52, 60), (830, 40, 95),
          (890, 30, 65), (940, 44, 55)]
for x, w, h in towers:
    d.rectangle([x, 480 - h, x + w, 480], fill=(8, 12, 26),
                outline=(120, 140, 180), width=2)
# jagged broken top on the middle tower
d.polygon([(760, 428), (778, 404), (792, 424), (806, 406), (812, 428)],
          fill=(8, 12, 26), outline=(120, 140, 180))
# lit windows
for x in range(650, 980, 26):
    for y in range(420, 475, 17):
        if (x * 5 + y * 11) % 4 == 0:
            d.rectangle([x, y, x + 6, y + 8], fill=(255, 210, 90))
# smoke puffs
for cx, cy, r in [(830, 210, 30), (900, 262, 22), (770, 230, 18)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 116, 128))
# lead text
d.text((48, 152), "LEAD  •  UKRAINE", font=font(SANS_B, 22), fill=GOLD)
lines = wrap(d, "RUSSIAN MISSILES HIT ZELENSKYY'S HOMETOWN",
             font(SERIF, 40), 580)
y = 186
for ln in lines:
    d.text((48, y), ln, font=font(SERIF, 40), fill=(255, 255, 255))
    y += 48
sub = wrap(d, "A ballistic strike on Kryvyi Rih kills a boy of 7 and a "
              "young paramedic; 60 wounded, six of them children.",
           font(SANS, 22), 580)
y += 8
for ln in sub:
    d.text((48, y), ln, font=font(SANS, 22), fill=(225, 230, 240))
    y += 30

# --- three stories in a row ---
boxes = [
    ("MEXICO  •  JUSTICE", RED, "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
     "FBI most-wanted cartel boss seized in Sinaloa with US help; "
     "11 killed in the violence that followed."),
    ("CLIMATE  •  COP31", GREEN, "CLIMATE TALKS RUN INTO OVERTIME",
     "Antalya summit passes its deadline with no deal; fossil fuels "
     "still missing from the draft."),
    ("MARKETS", BLUE, "AI SELL-OFF DRAGS MARKETS DOWN",
     "S&P 500 falls 3.7%; Nasdaq wipes out its 2026 gains as chip "
     "shares plunge."),
]
bx, by = 28, 500
bw, bh = 312, 268
gap = 16
for i, (kicker, col, head, sub2) in enumerate(boxes):
    x = bx + i * (bw + gap)
    y = by
    d.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255),
                outline=(200, 194, 182), width=2)
    d.rectangle([x, y, x + bw, y + 8], fill=col)
    d.rectangle([x + 18, y + 26, x + 30, y + 38], fill=col)
    d.text((x + 40, y + 20), kicker, font=font(SANS_B, 18), fill=col)
    hl = wrap(d, head, font(SERIF, 27), bw - 36)
    yy = y + 56
    for ln in hl:
        d.text((x + 18, yy), ln, font=font(SERIF, 27), fill=INK)
        yy += 34
    sl = wrap(d, sub2, font(SANS, 19), bw - 36)
    yy += 4
    for ln in sl:
        d.text((x + 18, yy), ln, font=font(SANS, 19), fill=GREY)
        yy += 26

# --- ALSO strip ---
fy = 788
d.rectangle([28, fy, 996, fy + 96], fill=NAVY)
d.text((48, fy + 10), "ALSO:", font=font(SANS_B, 20), fill=GOLD)
also = wrap(d, "Russian missiles land in Poland — NATO calls it a violation  •  "
               "Myanmar genocide ruling: rights groups urge sanctions  •  "
               "Iran strikes three tankers as talks stall",
            font(SANS, 19), 928)
yy = fy + 38
for ln in also:
    d.text((48, yy), ln, font=font(SANS, 19), fill=(255, 255, 255))
    yy += 26

# --- source line ---
d.text((28, 992), "Sources: AP, Reuters, Kyiv Independent — 21 Nov 2026",
       font=font(SANS, 16), fill=GREY)

img.save("/home/hatch/workspace/makefun/news-image-20261121/entry.png",
         optimize=True)
print("saved", img.size)
