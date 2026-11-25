#!/usr/bin/env python3
"""Sum up 24 November 2026's world news in one image.

Draws a newspaper-style infographic (1024x1024 PNG) in pure Python:
a hand-built 5x7 bitmap font, canvas drawing primitives, six verified
stories, and a small PNG encoder. Standard library only, no network.
Run: python3 main.py  ->  writes output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png). Two runs are byte-identical.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (250, 246, 236)
INK = (24, 24, 24)
GREY = (110, 108, 100)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
NAVY = (32, 54, 96)
PURPLE = (104, 52, 140)
TEAL = (14, 110, 110)
BLUE = (36, 84, 180)
GREEN = (34, 110, 58)
GOLD = (176, 132, 32)

# 5x7 bitmap font: each glyph is 7 row ints, 5 bits wide, bit 4 = left pixel.
FONT = {
    'A': (14, 17, 17, 31, 17, 17, 17),
    'B': (30, 17, 17, 30, 17, 17, 30),
    'C': (14, 17, 16, 16, 16, 17, 14),
    'D': (30, 17, 17, 17, 17, 17, 30),
    'E': (31, 16, 16, 30, 16, 16, 31),
    'F': (31, 16, 16, 30, 16, 16, 16),
    'G': (14, 17, 16, 23, 17, 17, 15),
    'H': (17, 17, 17, 31, 17, 17, 17),
    'I': (14, 4, 4, 4, 4, 4, 14),
    'J': (7, 2, 2, 2, 2, 18, 12),
    'K': (17, 18, 20, 24, 20, 18, 17),
    'L': (16, 16, 16, 16, 16, 16, 31),
    'M': (17, 27, 21, 21, 17, 17, 17),
    'N': (17, 25, 21, 19, 17, 17, 17),
    'O': (14, 17, 17, 17, 17, 17, 14),
    'P': (30, 17, 17, 30, 16, 16, 16),
    'Q': (14, 17, 17, 17, 21, 18, 13),
    'R': (30, 17, 17, 30, 20, 18, 17),
    'S': (15, 16, 16, 14, 1, 1, 30),
    'T': (31, 4, 4, 4, 4, 4, 4),
    'U': (17, 17, 17, 17, 17, 17, 14),
    'V': (17, 17, 17, 17, 17, 10, 4),
    'W': (17, 17, 17, 21, 21, 27, 17),
    'X': (17, 17, 10, 4, 10, 17, 17),
    'Y': (17, 17, 10, 4, 4, 4, 4),
    'Z': (31, 1, 2, 4, 8, 16, 31),
    'a': (0, 0, 14, 1, 15, 17, 15),
    'b': (16, 16, 30, 17, 17, 17, 30),
    'c': (0, 0, 14, 16, 16, 17, 14),
    'd': (1, 1, 15, 17, 17, 17, 15),
    'e': (0, 0, 14, 17, 31, 16, 14),
    'f': (6, 8, 8, 30, 8, 8, 8),
    'g': (0, 15, 17, 17, 15, 1, 14),
    'h': (16, 16, 30, 17, 17, 17, 17),
    'i': (4, 0, 12, 4, 4, 4, 14),
    'j': (2, 0, 6, 2, 2, 18, 12),
    'k': (16, 16, 20, 24, 20, 18, 17),
    'l': (12, 4, 4, 4, 4, 4, 14),
    'm': (0, 0, 26, 21, 21, 21, 21),
    'n': (0, 0, 30, 17, 17, 17, 17),
    'o': (0, 0, 14, 17, 17, 17, 14),
    'p': (0, 0, 30, 17, 30, 16, 16),
    'q': (0, 0, 15, 17, 15, 1, 1),
    'r': (0, 0, 22, 25, 16, 16, 16),
    's': (0, 0, 15, 16, 14, 1, 30),
    't': (8, 8, 28, 8, 8, 8, 6),
    'u': (0, 0, 17, 17, 17, 19, 13),
    'v': (0, 0, 17, 17, 17, 10, 4),
    'w': (0, 0, 17, 21, 21, 27, 17),
    'x': (0, 0, 17, 10, 4, 10, 17),
    'y': (0, 0, 17, 17, 15, 1, 14),
    'z': (0, 0, 31, 2, 4, 8, 31),
    '0': (14, 17, 19, 21, 25, 17, 14),
    '1': (4, 12, 4, 4, 4, 4, 14),
    '2': (14, 17, 1, 6, 8, 16, 31),
    '3': (31, 2, 4, 2, 1, 17, 14),
    '4': (2, 6, 10, 18, 31, 2, 2),
    '5': (31, 16, 30, 1, 1, 17, 14),
    '6': (6, 8, 16, 30, 17, 17, 14),
    '7': (31, 1, 2, 4, 8, 8, 8),
    '8': (14, 17, 17, 14, 17, 17, 14),
    '9': (14, 17, 17, 15, 1, 2, 12),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 12, 12),
    ',': (0, 0, 0, 0, 12, 4, 8),
    "'": (0, 4, 4, 8, 0, 0, 0),
    '-': (0, 0, 0, 14, 0, 0, 0),
    ':': (0, 12, 12, 0, 12, 12, 0),
    ';': (0, 12, 12, 0, 12, 4, 8),
    '!': (4, 4, 4, 4, 4, 0, 4),
    '?': (14, 17, 1, 2, 4, 0, 4),
    '/': (1, 1, 2, 4, 8, 16, 16),
    '(': (2, 4, 8, 8, 8, 4, 2),
    ')': (8, 4, 2, 2, 2, 4, 8),
    '%': (25, 25, 2, 4, 8, 19, 19),
    '+': (0, 4, 4, 31, 4, 4, 0),
    '=': (0, 0, 31, 0, 31, 0, 0),
    '|': (4, 4, 4, 4, 4, 4, 4),
}

# --- canvas: one RGB bytearray, row-major. ---
_px = bytearray(W * H * 3)


def _put(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        _px[i], _px[i + 1], _px[i + 2] = color


def fill(color):
    _px[:] = bytes(color) * (W * H)


def fill_rect(x, y, w, h, color):
    for yy in range(max(0, y), min(H, y + h)):
        base = (yy * W + max(0, x)) * 3
        for xx in range(max(0, x), min(W, x + w)):
            _px[base], _px[base + 1], _px[base + 2] = color
            base += 3


def rect(x, y, w, h, color, t=1):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def hline(x, y, w, color, t=1):
    fill_rect(x, y, w, t, color)


def vline(x, y, h, color, t=1):
    fill_rect(x, y, t, h, color)


def line(x0, y0, x1, y1, color, t=1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        fill_rect(x0 - t // 2, y0 - t // 2, t, t, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def fill_circle(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        half = int(math.sqrt(max(0, r * r - (yy - cy) ** 2)))
        hline(cx - half, yy, 2 * half + 1, color)


def circle(cx, cy, r, color, t=1):
    steps = max(24, int(2 * math.pi * r))
    for i in range(steps):
        a = 2 * math.pi * i / steps
        fill_rect(int(cx + r * math.cos(a)) - t // 2,
                  int(cy + r * math.sin(a)) - t // 2, t, t, color)


def ellipse(cx, cy, rx, ry, color, t=1):
    steps = max(32, int(2 * math.pi * max(rx, ry)))
    for i in range(steps):
        a = 2 * math.pi * i / steps
        fill_rect(int(cx + rx * math.cos(a)) - t // 2,
                  int(cy + ry * math.sin(a)) - t // 2, t, t, color)


def fill_triangle(x0, y0, x1, y1, x2, y2, color):
    pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts

    def edge(xa, ya, xb, yb, yy):
        if yb == ya:
            return xa
        return xa + (xb - xa) * (yy - ya) / (yb - ya)

    for yy in range(ay, cy + 1):
        if yy < by:
            xa = edge(ax, ay, bx, by, yy)
            xb = edge(ax, ay, cx, cy, yy)
        else:
            xa = edge(bx, by, cx, cy, yy)
            xb = edge(ax, ay, cx, cy, yy)
        lo, hi = sorted((int(xa), int(xb)))
        hline(lo, yy, hi - lo + 1, color)


# --- text. ---
def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, color):
    cx = x
    for ch in s:
        rows = FONT.get(ch, FONT[' '])
        for r, bits in enumerate(rows):
            for c in range(5):
                if bits & (1 << (4 - c)):
                    fill_rect(cx + c * scale, y + r * scale,
                              scale, scale, color)
        cx += 6 * scale


def draw_text_centered(cx, y, s, scale, color):
    draw_text(cx - text_w(s, scale) // 2, y, s, scale, color)


def wrap_lines(s, scale, max_w):
    lines, cur = [], ''
    for word in s.split(' '):
        trial = word if not cur else cur + ' ' + word
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            while text_w(word, scale) > max_w:
                cut = max_w // (6 * scale)
                lines.append(word[:cut])
                word = word[cut:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, s, scale, color, max_w, line_h=None, max_lines=None):
    if line_h is None:
        line_h = 9 * scale
    out = wrap_lines(s, scale, max_w)
    if max_lines is not None:
        out = out[:max_lines]
    for i, ln in enumerate(out):
        draw_text(x, y + i * line_h, ln, scale, color)
    return len(out)


def tag_chip(x, y, text, color):
    w = text_w(text, 2) + 16
    fill_rect(x, y, w, 22, color)
    draw_text(x + 8, y + 4, text, 2, WHITE)


# --- small pictures for the story blocks. Each gets its own box. ---
def art_quake(x, y, w, h, color):
    rel = [(0.0, 0.5), (0.15, 0.5), (0.25, 0.15), (0.35, 0.85),
           (0.5, 0.25), (0.6, 0.75), (0.7, 0.5), (0.85, 0.5), (1.0, 0.5)]
    pts = [(x + int(fx * w), y + int(fy * h)) for fx, fy in rel]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        line(x0, y0, x1, y1, color, 2)
    hline(x, y + h - 2, w, color, 1)


def art_chess(x, y, w, h, color):
    cell_w, cell_h = w // 4, h // 4
    for row in range(4):
        for col in range(4):
            if (row + col) % 2 == 0:
                fill_rect(x + col * cell_w, y + row * cell_h,
                          cell_w, cell_h, color)
    rect(x, y, w, h, color, 2)
    fill_rect(x + 3 * cell_w + 4, y + 4, cell_w - 8, cell_h - 8, RED)


def art_tower(x, y, w, h, color):
    bw = w // 5
    fill_rect(x, y + h // 2, bw, h // 2, color)
    fill_rect(x + 2 * bw, y + h // 5, bw, 4 * h // 5, color)
    fill_rect(x + 4 * bw, y + h // 3, bw, 2 * h // 3, color)
    hline(x, y + h - 2, w, color, 1)


def art_boat(x, y, w, h, color):
    fill_triangle(x + 6, y + h // 2, x + w - 6, y + h // 2,
                  x + w // 2, y + 3 * h // 4, color)
    vline(x + w // 2, y + 2, h // 2, color, 2)
    line(x + w // 2, y + 4, x + w // 2 + 20, y + h // 5, color, 2)
    line(x + 4, y + h - 6, x + w // 3, y + h - 6, color, 2)
    line(x + w // 2, y + h - 3, x + w - 4, y + h - 3, color, 2)


def art_scales(x, y, w, h, color):
    cx, cy = x + w // 2, y + h // 2
    vline(cx, cy - 26, 52, color, 2)
    hline(cx - 28, cy - 24, 56, color, 2)
    fill_rect(cx - 5, cy - 30, 10, 5, color)
    for side in (-1, 1):
        px = cx + side * 28
        line(px, cy - 24, px - 10, cy - 4, color, 2)
        line(px, cy - 24, px + 10, cy - 4, color, 2)
        fill_triangle(px - 11, cy - 4, px + 11, cy - 4, px, cy + 12, color)
    fill_rect(cx - 22, cy + 26, 44, 4, color)


def art_shield(x, y, w, h, color):
    cx, cy = x + w // 2, y + h // 2
    line(cx - 24, cy - 22, cx + 24, cy - 22, color, 2)
    line(cx - 24, cy - 22, cx - 24, cy + 4, color, 2)
    line(cx + 24, cy - 22, cx + 24, cy + 4, color, 2)
    line(cx - 24, cy + 4, cx, cy + 24, color, 2)
    line(cx + 24, cy + 4, cx, cy + 24, color, 2)
    corners = []
    for i in range(10):
        r = 10 if i % 2 == 0 else 4
        a = -math.pi / 2 + i * math.pi / 5
        corners.append((int(cx + r * math.cos(a)),
                        int(cy - 4 + r * math.sin(a))))
    for i in range(10):
        line(corners[i][0], corners[i][1],
             corners[(i + 1) % 10][0], corners[(i + 1) % 10][1], color, 2)


# --- the six stories, in the order they appear on the page. ---
STORIES = [
    dict(tag="DISASTER - NEPAL", color=NAVY,
         headline="M5.6 quake shakes Nepal near Tibet border",
         summary="The 07:17 quake hit Taplejung, Koshi Province. Felt in "
                 "India, Bhutan and Bangladesh. No casualties.",
         stat="M5.6 - 07:17 LOCAL", art=art_quake),
    dict(tag="CHINA - BEIJING", color=PURPLE,
         headline="China probes Politburo member Chen Jining",
         summary="Shanghai's party chief is probed for graft, Xinhua said. "
                 "Fourth Politburo member investigated since 2025.",
         stat="4TH SINCE 2025", art=art_scales),
    dict(tag="MIDDLE EAST - RIYADH", color=TEAL,
         headline="Riyadh tower hit in 'terrorist attack'",
         summary="The Saudi-led coalition said a Riyadh finance-district "
                 "tower was targeted. The PIF tower was hit this month.",
         stat="TALLEST TOWER HIT", art=art_tower),
    dict(tag="DIPLOMACY - FLORIDA", color=BLUE,
         headline="Trump to meet NATO chief Rutte on Wednesday",
         summary="The White House said Trump will meet Mark Rutte in Palm "
                 "Beach, Florida, on Wednesday.",
         stat="WEDNESDAY - PALM BEACH", art=art_shield),
]


def story_block(x, y, w, h, st):
    fill_rect(x, y, 6, h, st['color'])
    tx = x + 18
    tag_chip(tx, y, st['tag'], st['color'])
    draw_wrapped(tx, y + 34, st['headline'], 3, INK, w - 18,
                 line_h=25, max_lines=2)
    draw_wrapped(tx, y + 88, st['summary'], 2, INK, w - 18,
                 line_h=18, max_lines=3)
    draw_text(tx, y + h - 32, st['stat'], 2, st['color'])
    st['art'](x + w - 150, y + h - 58, 132, 46, st['color'])


# --- the page. ---
MX = 32
CW = W - 2 * MX


def build():
    fill(PAPER)
    rect(8, 8, W - 16, H - 16, INK, 2)
    fill_rect(8, 8, W - 16, 8, RED)

    draw_text_centered(W // 2, 30, "TUESDAY  -  24 NOVEMBER 2026", 2, RED)
    draw_text_centered(W // 2, 56, "WORLD NEWS IN ONE IMAGE", 6, INK)
    draw_text_centered(
        W // 2, 112,
        "Six stories that defined the day, from Geneva to Riyadh",
        2, GREY)
    hline(MX, 140, CW, INK, 4)
    hline(MX, 148, CW, INK, 1)

    fill_rect(MX, 158, CW, 34, INK)
    draw_text_centered(
        W // 2, 168,
        "M5.6 QUAKE  |  CHESS 0.5-0.5  |  175 MIGRANTS  |  4TH POLITBURO PROBE",
        2, WHITE)

    # lead story: the chess title match
    ly, lh = 206, 158
    fill_rect(MX, ly, 6, lh, RED)
    tx = MX + 18
    tag_chip(tx, ly, "SPORT - GENEVA", RED)
    draw_wrapped(tx, ly + 34,
                 "World chess title match opens with a Berlin draw",
                 3, INK, 690, line_h=25, max_lines=2)
    draw_wrapped(tx, ly + 88,
                 "Sindarov, White, and champion Gukesh drew Game 1 in Geneva "
                 "in 38 moves. Gukesh spent about 37 minutes on 17...Bb4, "
                 "then held with 32...Kg8.",
                 2, INK, 690, line_h=18, max_lines=3)
    bx, bw = 742, 250
    rect(bx, ly, bw, lh, RED, 2)
    art_chess(bx + 2, ly + 8, 56, 62, RED)
    draw_text(bx + 80, ly + 22, "0.5-0.5", 4, RED)
    draw_text(bx + 80, ly + 58, "38 moves,", 2, INK)
    draw_text(bx + 80, ly + 76, "threefold", 2, INK)
    draw_text(bx + 80, ly + 94, "repetition", 2, INK)
    draw_text(bx + 16, ly + 118, "BERLIN DEFENCE", 2, RED)
    hline(MX, ly + lh + 12, CW, INK, 1)

    # two rows of two stories
    ry, rh = 388, 196
    col_w = (CW - 32) // 2
    story_block(MX, ry, col_w, rh, STORIES[0])
    story_block(MX + col_w + 32, ry, col_w, rh, STORIES[1])
    hline(MX, ry + rh + 12, CW, INK, 1)

    ry2, rh2 = 608, 196
    story_block(MX, ry2, col_w, rh2, STORIES[2])
    story_block(MX + col_w + 32, ry2, col_w, rh2, STORIES[3])
    hline(MX, ry2 + rh2 + 12, CW, INK, 1)

    # sixth story, full width
    sy, sh = 828, 96
    fill_rect(MX, sy, 6, sh, GREEN)
    tx = MX + 18
    tag_chip(tx, sy, "MIGRATION - SENEGAL", GREEN)
    draw_wrapped(tx, sy + 34, "175 unaccounted for off Senegal",
                 3, INK, 700, line_h=25, max_lines=1)
    draw_wrapped(tx, sy + 62,
                 "A Europe-bound pirogue left Dakar about two weeks ago and "
                 "contact was lost. Navy rescued 974 on Monday.",
                 2, INK, 700, line_h=18, max_lines=2)
    art_boat(830, sy + 6, 150, 84, GREEN)
    hline(MX, sy + sh + 10, CW, INK, 4)

    fy = 950
    draw_text_centered(W // 2, fy, "SOURCES: CHESSBASE - REUTERS - XINHUA",
                       2, GREY)
    draw_text_centered(W // 2, fy + 22,
                       "VERIFIED 24 NOV 2026  -  DRAWN IN CODE, NO PHOTOS",
                       2, GREY)


# --- PNG output: truecolour, one filter byte of 0 per scanline. ---
def _chunk(kind, data):
    body = kind + data
    return (struct.pack('>I', len(data)) + body +
            struct.pack('>I', zlib.crc32(body) & 0xffffffff))


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += _px[y * W * 3:(y + 1) * W * 3]
    png = b'\x89PNG\r\n\x1a\n'
    png += _chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
    png += _chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += _chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


def main():
    build()
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', 'output')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'entry.png')
    size = write_png(path)
    print('wrote %s (%d bytes, %dx%d)' % (path, size, W, H))


if __name__ == '__main__':
    main()
