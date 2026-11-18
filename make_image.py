#!/usr/bin/env python3
"""Render entry.png: the world news of Tuesday 17 November 2026 in one image.

A newspaper front page drawn with Pillow and real fonts, so every word is
crisp. The make.fun entry itself is main.ts, which copies the PNG this
script produces to /output/entry.png. Every headline below was reported on
17 November 2026; SOURCES.md lists the reporting behind each one.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 24, 29)
FAINT = (90, 88, 80)
RULE = (20, 24, 29)
WHITE = (250, 248, 242)
SUB = (45, 48, 52)
HAIR = (196, 188, 168)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_w):
    """Largest size <= size at which text fits max_w on one line."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.18):
    x, y = xy
    lh = int(fnt.size * leading)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 44  # page margin

# ---------------------------------------------------------------- masthead
d.text((M, 24), "THE WORLD IN ONE IMAGE", font=font(SANS_B, 25), fill=(163, 22, 33))
kick = "A FRONT PAGE FOR PEOPLE WHO MISSED THE DAY"
kw = d.textlength(kick, font=font(SANS, 19))
d.text((W - M - kw, 28), kick, font=font(SANS, 19), fill=FAINT)

date = "17 NOVEMBER 2026"
df = fit_font(d, date, SERIF_B, 88, W - 2 * M)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 52), date, font=df, fill=INK)

sub = "TUESDAY  ·  THE DAY'S BIGGEST STORIES, AT A GLANCE"
sf = font(SANS_B, 22)
sw = d.textlength(sub, font=sf)
d.text(((W - sw) / 2, 152), sub, font=sf, fill=FAINT)
d.line([(M, 188), (W - M, 188)], fill=RULE, width=5)
d.line([(M, 196), (W - M, 196)], fill=RULE, width=2)

# ---------------------------------------------------------------- lead story
LEAD_C = (163, 22, 33)
ly = 216
d.rectangle([M, ly, 218, ly + 34], fill=LEAD_C)
d.text((M + 12, ly + 5), "LEAD · WAR", font=font(SANS_B, 21), fill=WHITE)

lead_head = "U.S. strikes Iran's Qeshm Island; tankers burn in Hormuz"
y = text_block(d, (M, ly + 46), lead_head, font(SERIF_B, 44), INK, 660, 1.12)
lead_sub = ("Warplanes hit a missile site on Qeshm. In the Strait of Hormuz, "
            "mine-struck ships caught fire and Oman rescued 24 crew from a "
            "blazing gas carrier.")
text_block(d, (M, y + 8), lead_sub, font(SANS, 22), SUB, 660, 1.22)

# lead icon: tanker on waves, sun above (right of the lead text)
ix, iy = 748, ly + 16
d.ellipse([ix + 150, iy, ix + 196, iy + 46], fill=(217, 164, 65))          # sun
d.polygon([(ix, iy + 128), (ix + 196, iy + 128), (ix + 172, iy + 158),
           (ix + 24, iy + 158)], fill=INK)                                  # hull
d.rectangle([ix + 30, iy + 106, ix + 118, iy + 128], fill=INK)              # deck cargo
d.rectangle([ix + 138, iy + 92, ix + 162, iy + 128], fill=INK)              # bridge tower
d.rectangle([ix + 144, iy + 78, ix + 156, iy + 92], fill=LEAD_C)            # funnel
for r in range(3):                                                          # waves
    wy = iy + 172 + r * 13
    for x0 in range(ix - 6, ix + 196, 34):
        d.arc([x0, wy, x0 + 26, wy + 12], 180, 360, fill=(37, 84, 124), width=3)

d.line([(M, 500), (W - M, 500)], fill=RULE, width=3)

# ---------------------------------------------------------------- story grid
PANELS = [
    ("EUROPE", (29, 53, 87), "bridge",
     "Ukraine hits the Kerch Bridge again",
     "Russia answers with missiles on Kyiv, hitting Dnipro bridges "
     "and cutting heat and water."),
    ("DIPLOMACY", (15, 118, 110), "circles",
     "Trump, Xi and Putin converge on Shenzhen",
     "Leaders gather for APEC; a first U.S.-China-Russia trilateral "
     "is set for Thursday."),
    ("GAZA", (148, 107, 0), "aid",
     "West urges Israel to open Gaza crossings",
     "Four Western allies call the aid crisis catastrophic; the UN "
     "warns rains flood shelters."),
    ("CLIMATE", (46, 125, 50), "globe",
     "COP31 draft urges fossil-fuel phase-out",
     "Antalya text triples adaptation finance to $120bn a year by "
     "2035; ministers take over."),
    ("TECH", (91, 75, 138), "chip",
     "U.S. tightens AI chip rules on China",
     "Licences now cover advanced chips in overseas data centres. "
     "Beijing protests."),
    ("HEALTH", (150, 40, 70), "cross",
     "U.S. loses its measles elimination status",
     "A year of unbroken transmission; worst case counts in over "
     "three decades."),
]


def icon(kind, x, y, s, color):
    """Tiny flat glyphs, one per beat, drawn in the panel's accent colour."""
    if kind == "bridge":  # arc deck with two pylons
        d.arc([x, y + 6, x + s, y + s], 180, 360, fill=color, width=5)
        d.line([(x - 4, y + s // 2 + 3), (x + s + 4, y + s // 2 + 3)], fill=color, width=5)
        d.line([(x + s * 0.28, y + s * 0.28), (x + s * 0.28, y + s // 2 + 3)], fill=color, width=4)
        d.line([(x + s * 0.72, y + s * 0.28), (x + s * 0.72, y + s // 2 + 3)], fill=color, width=4)
    elif kind == "circles":  # three leaders, three rings
        r = s * 0.30
        for cx, cy in [(x + s * 0.32, y + s * 0.38), (x + s * 0.68, y + s * 0.38), (x + s * 0.5, y + s * 0.68)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    elif kind == "aid":  # aid crate with a cross
        d.rectangle([x + 4, y + 10, x + s - 4, y + s - 6], outline=color, width=5)
        d.rectangle([x + s / 2 - 6, y + s * 0.32, x + s / 2 + 6, y + s * 0.68], fill=color)
        d.rectangle([x + s * 0.32, y + s / 2 - 6, x + s * 0.68, y + s / 2 + 6], fill=color)
    elif kind == "globe":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=color, width=5)
        d.ellipse([x + s * 0.32, y + 4, x + s * 0.68, y + s - 4], outline=color, width=3)
        d.line([(x + 4, y + s / 2), (x + s - 4, y + s / 2)], fill=color, width=3)
    elif kind == "chip":
        d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78], outline=color, width=5)
        d.rectangle([x + s * 0.40, y + s * 0.40, x + s * 0.60, y + s * 0.60], fill=color)
        for t in (0.32, 0.5, 0.68):
            d.line([(x + s * t, y + 2), (x + s * t, y + s * 0.22)], fill=color, width=4)
            d.line([(x + s * t, y + s * 0.78), (x + s * t, y + s - 2)], fill=color, width=4)
            d.line([(x + 2, y + s * t), (x + s * 0.22, y + s * t)], fill=color, width=4)
            d.line([(x + s * 0.78, y + s * t), (x + s - 2, y + s * t)], fill=color, width=4)
    elif kind == "cross":
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=color, width=5)
        d.rectangle([x + s / 2 - 7, y + s * 0.28, x + s / 2 + 7, y + s * 0.72], fill=color)
        d.rectangle([x + s * 0.28, y + s / 2 - 7, x + s * 0.72, y + s / 2 + 7], fill=color)


GY = 502            # grid top
RH = 140            # row height
COLW = (W - 2 * M - 28) // 2
for i, (tag, color, glyph, head, sub) in enumerate(PANELS):
    cx = M + (i % 2) * (COLW + 28)
    cy = GY + (i // 2) * RH
    if i % 2 == 1:
        d.line([(cx - 14, cy + 2), (cx - 14, cy + RH - 12)], fill=HAIR, width=2)
    if i >= 2:
        d.line([(cx, cy - 8), (cx + COLW, cy - 8)], fill=HAIR, width=2)
    d.rectangle([cx, cy, cx + 128, cy + 28], fill=color)
    tw = d.textlength(tag, font=font(SANS_B, 17))
    d.text((cx + (128 - tw) / 2, cy + 5), tag, font=font(SANS_B, 17), fill=WHITE)
    icon(glyph, cx + COLW - 60, cy, 54, color)
    y = text_block(d, (cx, cy + 34), head, font(SANS_B, 24), INK, COLW - 70, 1.1)
    text_block(d, (cx, y + 2), sub, font(SANS, 17), SUB, COLW, 1.15)

# ---------------------------------------------------------------- markets ticker
TY = 928
d.rectangle([0, TY, W, H], fill=INK)
tick = ("MARKETS:  S&P 500 -1.0%  ·  DOW -1.6%  ·  NASDAQ -0.7%  -  Nvidia "
        "beats forecasts after the bell")
tf = fit_font(d, tick, SANS_B, 21, W - 2 * M)
tw = d.textlength(tick, font=tf)
d.text(((W - tw) / 2, TY + 16), tick, font=tf, fill=(240, 234, 220))
foot = "Every story above was reported on Tuesday 17 November 2026"
ff = font(SANS, 17)
fw = d.textlength(foot, font=ff)
d.text(((W - fw) / 2, TY + 54), foot, font=ff, fill=(168, 162, 148))

img.save("/home/hatch/workspace/makefun/entry-news-image/entry.png", optimize=True)
print("saved entry.png")
