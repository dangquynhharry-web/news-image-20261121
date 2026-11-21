#!/usr/bin/env python3
"""The World — Saturday 21 November 2026, drawn as a newspaper front page.

Writes /output/entry.png (1024x1024 PNG). The stories are data in the
STORIES table; the renderer lays them out in three bands: one lead, a
row of three, a row of two. Deterministic: no network, no clock, no
randomness — two runs write byte-identical output. Python 3.13, Pillow,
DejaVu fonts bundled in fonts/.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "fonts")
OUT_PATH = "/output/entry.png"

PAGE_W, PAGE_H = 1024, 1024
SIDE = 46
BLACK = (0, 0, 0)
MID = (96, 96, 96)
WHITE = (255, 255, 255)

# (section, headline, standfirst) — six stories, all first reported on
# Saturday 21 November 2026. Sources: Reuters, AP, AFP, SCMP, Al Jazeera.
STORIES = [
    {
        "section": "MEXICO",
        "headline": "Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'",
        "standfirst": (
            "Fausto Isidro Meza-Flores seized in a Friday-night raid in "
            "Guasave, Sinaloa; 11 killed as gunmen fought back and torched "
            "trucks across the city."
        ),
    },
    {
        "section": "POLAND",
        "headline": "Russian missiles land in Poland",
        "standfirst": (
            "Missiles and a jet drone breach Polish airspace as Europe holds "
            "drills nearby; NATO calls it a violation, Warsaw an intentional "
            "provocation."
        ),
    },
    {
        "section": "CLIMATE  ·  ANTALYA",
        "headline": "COP31 talks run into overtime",
        "standfirst": (
            "Nearly 200 nations deadlocked after the draft drops all "
            "fossil-fuel language; a third draft is expected on Saturday."
        ),
    },
    {
        "section": "WASHINGTON",
        "headline": "Trump threatens 'tremendous tax' on AI data centres built abroad",
        "standfirst": (
            "US firms warned they risk losing America's AI lead to China if "
            "they build overseas."
        ),
    },
    {
        "section": "RIYADH  ·  YEMEN",
        "headline": "Houthis strike Riyadh as Saudi jets hit Yemen",
        "standfirst": (
            "Houthis claim strikes on a Saudi power plant and port; 41 "
            "killed in Yemen airstrikes, Houthi media say."
        ),
    },
    {
        "section": "FRANCE",
        "headline": "French protests shrink as cost-of-living marches go on",
        "standfirst": (
            "82,500 march nationwide, down from 106,000 a week earlier; "
            "70,000 police deployed."
        ),
    },
]

# One-line briefs, all first reported on Saturday 21 November 2026.
BRIEFS = [
    "EU budget chief proposes a 3% digital tax and €40 billion in cuts "
    "to the 2028–2034 budget.",
    "France's Senate approves a police shootings law critics call a "
    "'licence to kill'.",
    "SpaceX Dragon cargo craft leaves the ISS and is due to splash down "
    "off California on Saturday.",
]


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_lines(text, typeface, max_w):
    """Greedy word wrap, measured with the real font."""
    out, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if typeface.getlength(trial) <= max_w:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), WHITE)
        self.pen = ImageDraw.Draw(self.img)
        self.y = 34

    def bar(self, weight, left=None, right=None):
        left = SIDE if left is None else left
        right = PAGE_W - SIDE if right is None else right
        self.pen.line([(left, self.y), (right, self.y)], fill=BLACK, width=weight)
        self.y += weight

    def gap(self, n):
        self.y += n

    def centred(self, text, typeface, colour=BLACK):
        self.pen.text((PAGE_W // 2, self.y), text, font=typeface,
                      fill=colour, anchor="mt")
        self.y += typeface.size

    def story(self, item, width, head_size, deck_size, x=None):
        """Draw one story at the current y, or at x when given. Returns
        the y just below it."""
        x = SIDE if x is None else x
        top = self.y
        head = load("DejaVuSerif-Bold.ttf", head_size)
        deck = load("DejaVuSans.ttf", deck_size)
        tag = load("DejaVuSans-Bold.ttf", 16)
        self.pen.text((x, top), item["section"], font=tag, fill=BLACK)
        cursor = top + 25
        for line in fit_lines(item["headline"], head, width):
            self.pen.text((x, cursor), line, font=head, fill=BLACK)
            cursor += int(head_size * 1.14)
        cursor += 3
        for line in fit_lines(item["standfirst"], deck, width):
            self.pen.text((x, cursor), line, font=deck, fill=MID)
            cursor += int(deck_size * 1.38)
        return cursor


def render():
    page = Page()
    draw = page.pen

    # Masthead.
    page.bar(2)
    page.gap(5)
    page.bar(1)
    page.gap(12)
    page.centred("THE WORLD", load("DejaVuSerif-Bold.ttf", 92))
    page.gap(10)
    page.centred("SATURDAY, 21 NOVEMBER 2026", load("DejaVuSans.ttf", 21))
    page.gap(30)
    page.bar(4)
    page.gap(24)

    full = PAGE_W - 2 * SIDE

    # Band 1: the lead, full width.
    page.y = page.story(STORIES[0], full, 42, 21)
    page.gap(16)
    page.bar(2)
    page.gap(20)

    # Band 2: three across.
    gutter = 28
    third = (full - 2 * gutter) // 3
    starts = [SIDE, SIDE + third + gutter, SIDE + 2 * (third + gutter)]
    bottoms = []
    for item, x in zip(STORIES[1:4], starts):
        keep = page.y
        bottoms.append(page.story(item, third, 23, 16, x=x))
        page.y = keep
    page.y = max(bottoms) + 8
    for x in starts:
        page.bar(1, left=x, right=x + third)
    page.gap(16)

    # Band 3: two across.
    half = (full - gutter) // 2
    starts = [SIDE, SIDE + half + gutter]
    bottoms = []
    for item, x in zip(STORIES[4:6], starts):
        keep = page.y
        bottoms.append(page.story(item, half, 27, 18, x=x))
        page.y = keep
    page.y = max(bottoms) + 14
    page.bar(2)
    page.gap(14)

    # "Also on Saturday" briefs, full width.
    brief_font = load("DejaVuSans.ttf", 16)
    page.pen.text((SIDE, page.y), "ALSO ON SATURDAY",
                  font=load("DejaVuSans-Bold.ttf", 16), fill=BLACK)
    page.y += 25
    for brief in BRIEFS:
        for line in fit_lines("•  " + brief, brief_font, full):
            page.pen.text((SIDE, page.y), line, font=brief_font, fill=BLACK)
            page.y += 23
        page.y += 2
    page.gap(8)
    page.bar(1)
    page.gap(12)

    # Credit line.
    draw.text(
        (PAGE_W // 2, page.y),
        "Sources: Reuters  ·  AP  ·  AFP  ·  SCMP  ·  Al Jazeera",
        font=load("DejaVuSans.ttf", 15), fill=MID, anchor="mt",
    )

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    page.img.save(OUT_PATH, format="PNG")


if __name__ == "__main__":
    render()
