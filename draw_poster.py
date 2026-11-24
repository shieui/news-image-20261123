#!/usr/bin/env python3
"""Build-time poster renderer for the 23 November 2026 news poster.

Draws a one-page newspaper-style poster with Pillow and writes
entry.png next to this script. Runs only on this machine at build
time; the graded entrypoint (main.py) merely copies entry.png.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34

PAPER = (247, 243, 234)
INK = (24, 24, 26)
RED = (178, 34, 34)
DARKRED = (128, 20, 20)
GREY = (92, 88, 80)
LIGHT = (233, 227, 214)
NAVY = (26, 48, 84)
TEAL = (18, 96, 92)
GOLD = (176, 128, 24)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, spacing=6):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_BOLD, 19)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 26


def headline(draw, x, y, text, width, size=34):
    f = font(SERIF, size)
    return draw_wrapped(draw, x, y, text, f, width, spacing=4)


def body(draw, x, y, text, width, size=21):
    f = font(SANS, size)
    return draw_wrapped(draw, x, y, text, f, width, fill=(52, 50, 46), spacing=5)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# double border frame
d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([18, 18, W - 19, H - 19], outline=RED, width=1)

# ---------------------------------------------------------------- masthead
y = 34
f_title = font(SANS_BOLD, 26)
t = "THE WORLD IN ONE DAY"
d.text(((W - d.textlength(t, font=f_title)) / 2, y), t, font=f_title, fill=GREY)
y += 38
f_date = font(SERIF, 47)
t = "MONDAY 23 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f_date)) / 2, y), t, font=f_date, fill=INK)
y += 66
d.line([(MARGIN, y), (W - MARGIN, y)], fill=RED, width=4)
y += 12
d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
y += 14
f_sub = font(SANS, 22)
t = "Six stories that defined the day  •  From every region, every field"
d.text(((W - d.textlength(t, font=f_sub)) / 2, y), t, font=f_sub, fill=GREY)
y += 44

# ---------------------------------------------------------------- lead story
lead_x = MARGIN
lead_w = 560
art_x = MARGIN + lead_w + 26
art_w = W - MARGIN - art_x
art_h = 200

lead_top = y
y = kicker(d, lead_x, y, "Lead story  •  War at sea")
y = headline(d, lead_x, y, "Ukraine sinks Russian\nwarship off Libya", lead_w, size=44)
y = body(d, lead_x, y,
         "President Zelenskyy confirmed on Monday that Ukrainian "
         "naval drones sank the Russian corvette Merkury and hit a "
         "sanctioned cargo ship at Benghazi port — taking the war "
         "hundreds of miles into the Mediterranean.",
         lead_w, size=22)

# illustration: sea, ship, drones
ax0, ay0 = art_x, lead_top
d.rectangle([ax0, ay0, ax0 + art_w, ay0 + art_h], fill=(198, 222, 235),
            outline=NAVY, width=2)
# sky
d.rectangle([ax0, ay0, ax0 + art_w, ay0 + 96], fill=(214, 232, 242))
# sun
d.ellipse([ax0 + art_w - 74, ay0 + 18, ax0 + art_w - 26, ay0 + 66], fill=GOLD)
# sea waves
for i, wy in enumerate((128, 152, 176)):
    for wx in range(0, art_w, 44):
        d.arc([ax0 + wx, ay0 + wy, ax0 + wx + 40, ay0 + wy + 18],
              start=0, end=180, fill=NAVY, width=3)
# ship hull and tower
d.polygon([(ax0 + 40, ay0 + 150), (ax0 + 260, ay0 + 150),
           (ax0 + 236, ay0 + 186), (ax0 + 64, ay0 + 186)], fill=(58, 62, 70))
d.rectangle([ax0 + 120, ay0 + 112, ax0 + 150, ay0 + 150], fill=(58, 62, 70))
d.rectangle([ax0 + 128, ay0 + 96, ax0 + 134, ay0 + 112], fill=(58, 62, 70))
d.line([(ax0 + 131, ay0 + 96), (ax0 + 131, ay0 + 78)], fill=DARKRED, width=3)
# tilted, listing ship: red flag
d.polygon([(ax0 + 131, ay0 + 78), (ax0 + 158, ay0 + 86), (ax0 + 131, ay0 + 94)],
          fill=RED)
# two drones above
for dx, dy in ((ax0 + 210, ay0 + 52), (ax0 + 268, ay0 + 34)):
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
    d.line([(dx - 14, dy), (dx + 14, dy)], fill=INK, width=2)
    d.line([(dx, dy - 12), (dx, dy + 12)], fill=INK, width=2)
# caption
f_cap = font(SANS, 18)
d.text((ax0, ay0 + art_h + 8), "Ukrainian sea drones struck at Benghazi.",
       font=f_cap, fill=GREY)

lead_bottom = max(y, ay0 + art_h + 34)
d.line([(MARGIN, lead_bottom), (W - MARGIN, lead_bottom)], fill=INK, width=2)

# ---------------------------------------------------------------- grid of stories
stories = [
    ("Markets  •  Technology", RED,
     "Nvidia brings back\nJensen Huang",
     "Eleven days after resigning, Huang is CEO again. "
     "Shares jumped about 33% and the S&P 500 rose 4.8%."),
    ("War  •  Iran", DARKRED,
     "US hits Iran's shadow\nbanking network",
     "The Treasury sanctioned over two dozen Iranian exchange "
     "houses and front firms; an Iranian court claimed "
     "$290bn from the US."),
    ("Security  •  Europe", NAVY,
     "NATO sends AWACS\nto Poland",
     "After Russian missiles fell in Poland on Friday, "
     "NATO met in emergency session and agreed to send an "
     "early-warning aircraft."),
    ("War  •  Ukraine", DARKRED,
     "Russian strike kills\n11 in Dymer",
     "A missile hit an apartment block north of Kyiv. "
     "Rescuers pulled survivors from the rubble as the "
     "death toll rose through the day."),
    ("Disaster  •  South America", TEAL,
     "Magnitude 6.7 quake\nshakes Peru's Andes",
     "A strong earthquake struck the Andean highlands on "
     "Monday, rattling towns and sending residents into "
     "the streets."),
    ("Markets  •  In numbers", GOLD,
     "The day in figures",
     "S&P 500  +4.8%  •  Nvidia  +33%  •  Kospi  -3.3%  •  "
     "Nikkei  -5% in Asian trading  •  Samsung  -3.1%  •  "
     "SK Hynix  -2.5%"),
]

cell_w = (W - 2 * MARGIN - 2 * 20) // 3
cell_h = 178
grid_y = lead_bottom + 18
for i, (kick, color, head, text) in enumerate(stories):
    col = i % 3
    row = i // 3
    cx = MARGIN + col * (cell_w + 20)
    cy = grid_y + row * (cell_h + 16)
    # thin top rule for each cell
    d.line([(cx, cy), (cx + cell_w, cy)], fill=color, width=3)
    yy = cy + 12
    yy = kicker(d, cx, yy, kick, color=color)
    yy = headline(d, cx, yy, head, cell_w, size=25)
    body(d, cx, yy, text, cell_w, size=17)

grid_bottom = grid_y + 2 * (cell_h + 16)

# ---------------------------------------------------------------- footer ticker
fy = grid_bottom + 6
d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=RED, width=3)
fy += 14
f_tick = font(SANS_BOLD, 19)
tick = ("ALSO TODAY:  UK and EU sign a reconciliation deal a decade after Brexit  •  "
        "Deadly strike on buses in Yemen's Lahj province  •  "
        "India pledges €1.4bn to rebuild Nepal after a glacier flood")
draw_wrapped(d, MARGIN, fy, tick, f_tick, W - 2 * MARGIN, fill=INK, spacing=4)
fy += 62
f_foot = font(SANS, 17)
t = "All stories as reported on Monday 23 November 2026  •  One day, one page."
d.text(((W - d.textlength(t, font=f_foot)) / 2, fy), t, font=f_foot, fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
