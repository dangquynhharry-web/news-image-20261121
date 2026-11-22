#!/usr/bin/env python3
"""The World — Saturday 21 November 2026, drawn as a newspaper front page.

Standard library only: no Pillow, no network, no clock, no randomness.
The text is set from glyph bitmaps baked at build time from DejaVu
(serif-bold for the masthead and headlines, sans for everything else)
and carried below as base64; the PNG itself is encoded by hand with
zlib (filter 0 scanlines). Two runs write byte-identical output.

Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import base64
import binascii
import os
import struct
import zlib

PAGE_W, PAGE_H = 1024, 1024
SIDE = 46
BLACK = (0, 0, 0)
MID = (96, 96, 96)
WHITE = (255, 255, 255)

# Characters covered by the baked fonts, in blob order.
CHARS = [chr(c) for c in range(32, 127)] + ["·", "–", "—", "•", "€"]

# Baked glyphs: two fonts (serif-bold, sans) at 16 px. Per font: ascent,
# descent, then per character: advance, xoff, yoff (signed, from the
# baseline), width, height, then height rows of bit-packed pixels.
FONT_B64 = "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"


def _load_fonts():
    """Decode FONT_B64 into {name: (ascent, descent, {char: glyph})}.

    A glyph is (advance, xoff, yoff, width, height, bitmap rows).
    xoff/yoff are in baked pixels, yoff measured from the baseline.
    """
    raw = base64.b64decode(FONT_B64)
    fonts = {}
    pos = 0
    for name in ("serif", "sans"):
        ascent, descent = raw[pos], raw[pos + 1]
        pos += 2
        glyphs = {}
        for ch in CHARS:
            adv, xoff, yoff, w, h = struct.unpack_from("bbbBB", raw, pos)
            pos += 5
            n = h * ((w + 7) // 8)
            glyphs[ch] = (adv, xoff, yoff, w, h, raw[pos:pos + n])
            pos += n
        fonts[name] = (ascent, descent, glyphs)
    return fonts


FONTS = _load_fonts()


def _line_height(font_name, scale):
    ascent, descent, _ = FONTS[font_name]
    return (ascent + descent) * scale


def _text_width(text, font_name, scale):
    _, _, glyphs = FONTS[font_name]
    return sum(glyphs[ch][0] for ch in text) * scale


def _wrap(text, font_name, scale, max_w):
    """Greedy word wrap, measured with the real glyph advances."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if _text_width(trial, font_name, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---- pixel buffer ----

class Page:
    def __init__(self):
        self.buf = bytearray(bytes(WHITE) * (PAGE_W * PAGE_H))
        self.y = 24
        self._runs_cache = {}

    def rect(self, x, y, w, h, color):
        row = bytes(color) * w
        for yy in range(y, y + h):
            off = (yy * PAGE_W + x) * 3
            self.buf[off:off + w * 3] = row

    def bar(self, weight, left=None, right=None):
        left = SIDE if left is None else left
        right = PAGE_W - SIDE if right is None else right
        self.rect(left, self.y, right - left, weight, BLACK)
        self.y += weight

    def gap(self, n):
        self.y += n

    def _glyph_runs(self, font_name, ch, scale, color):
        """Ink runs of a glyph scaled by `scale`: [(dy, [(dx, bytes)])].

        Only ink is painted, never the white inside a glyph box, so a
        glyph whose bitmap is wider than its advance cannot erase the
        next glyph. Cached per (font, char, scale, colour).
        """
        key = (font_name, ch, scale, color)
        cached = self._runs_cache.get(key)
        if cached is not None:
            return cached
        _, _, glyphs = FONTS[font_name]
        adv, xoff, yoff, w, h, data = glyphs[ch]
        ink = bytes(color)
        stride = (w + 7) // 8
        out = []
        for yy in range(h):
            row = data[yy * stride:(yy + 1) * stride]
            runs = []
            xx = 0
            while xx < w:
                if (row[xx // 8] >> (7 - (xx % 8))) & 1:
                    x0 = xx
                    while xx < w and ((row[xx // 8] >> (7 - (xx % 8))) & 1):
                        xx += 1
                    runs.append((x0 * scale, ink * ((xx - x0) * scale)))
                else:
                    xx += 1
            for k in range(scale):
                out.append((yy * scale + k, runs))
        self._runs_cache[key] = out
        return out

    def _blit(self, font_name, ch, x, baseline_y, scale, color, bold=False):
        _, _, glyphs = FONTS[font_name]
        adv, xoff, yoff, w, h, _ = glyphs[ch]
        if w == 0:
            return
        passes = (0,) if not bold else (0, scale)
        for extra in passes:
            ox = x + xoff * scale + extra
            oy = baseline_y + yoff * scale
            for dy, runs in self._glyph_runs(font_name, ch, scale, color):
                yy = oy + dy
                if yy < 0 or yy >= PAGE_H:
                    continue
                base = (yy * PAGE_W + ox) * 3
                for dx, b in runs:
                    self.buf[base + dx * 3:base + dx * 3 + len(b)] = b

    def text_line(self, text, font_name, scale, x=None, color=BLACK, bold=False):
        """Draw one line, baseline at y + ascent*scale; advance y."""
        x = SIDE if x is None else x
        ascent, _, glyphs = FONTS[font_name]
        baseline = self.y + ascent * scale
        cx = x
        for ch in text:
            self._blit(font_name, ch, cx, baseline, scale, color, bold)
            cx += glyphs[ch][0] * scale
        self.y += _line_height(font_name, scale)

    def centred(self, text, font_name, scale, color=BLACK, bold=False):
        w = _text_width(text, font_name, scale)
        self.text_line(text, font_name, scale, x=(PAGE_W - w) // 2,
                       color=color, bold=bold)

    def story(self, item, width, head_scale, deck_scale, x=None):
        """Draw one story at the current y, or at x when given. Returns
        the y just below it."""
        x = SIDE if x is None else x
        top = self.y
        self.text_line(item["section"], "sans", 1, x=x, bold=True)
        for line in _wrap(item["headline"], "serif", head_scale, width):
            self.text_line(line, "serif", head_scale, x=x)
        self.gap(2)
        for line in _wrap(item["standfirst"], "sans", deck_scale, width):
            self.text_line(line, "sans", deck_scale, x=x, color=MID)
        return self.y


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


def _png(buf, w, h):
    """Encode an RGB buffer as PNG: filter 0 scanlines, zlib, stdlib only."""
    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", binascii.crc32(typ + data) & 0xFFFFFFFF)
        return out

    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += buf[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
            + chunk(b"IEND", b""))


def render():
    page = Page()

    # Masthead.
    page.bar(2)
    page.gap(4)
    page.bar(1)
    page.gap(8)
    page.centred("THE WORLD", "serif", 5)
    page.gap(2)
    page.centred("SATURDAY, 21 NOVEMBER 2026", "sans", 1)
    page.gap(8)
    page.bar(3)
    page.gap(8)

    full = PAGE_W - 2 * SIDE

    # Band 1: the lead, full width.
    page.y = page.story(STORIES[0], full, 3, 1)
    page.gap(6)
    page.bar(2)
    page.gap(8)

    # Band 2: three across.
    gutter = 28
    third = (full - 2 * gutter) // 3
    starts = [SIDE, SIDE + third + gutter, SIDE + 2 * (third + gutter)]
    bottoms = []
    for item, x in zip(STORIES[1:4], starts):
        keep = page.y
        bottoms.append(page.story(item, third, 2, 1, x=x))
        page.y = keep
    page.y = max(bottoms) + 6
    for x in starts:
        page.bar(1, left=x, right=x + third)
    page.gap(8)

    # Band 3: two across.
    half = (full - gutter) // 2
    starts = [SIDE, SIDE + half + gutter]
    bottoms = []
    for item, x in zip(STORIES[4:6], starts):
        keep = page.y
        bottoms.append(page.story(item, half, 2, 1, x=x))
        page.y = keep
    page.y = max(bottoms) + 6
    page.bar(2)
    page.gap(6)

    # "Also on Saturday" briefs, full width.
    page.text_line("ALSO ON SATURDAY", "sans", 1, bold=True)
    for brief in BRIEFS:
        for line in _wrap("•  " + brief, "sans", 1, full):
            page.text_line(line, "sans", 1)
        page.gap(2)
    page.gap(2)
    page.bar(1)
    page.gap(4)

    # Credit line.
    page.centred("Sources: Reuters  ·  AP  ·  AFP  ·  SCMP  ·  Al Jazeera",
                "sans", 1, color=MID)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(_png(page.buf, PAGE_W, PAGE_H))
    print("wrote", out_path, "final y:", page.y)


if __name__ == "__main__":
    render()
