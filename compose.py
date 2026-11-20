#!/usr/bin/env python3
"""
compose.py -- builds the front page of "The World in One Day"
(Friday 20 November 2026) as a deterministic 1024x1024 PNG.

The photograph (hero.webp, kept next to this script) carries no text;
every word on the page is typeset here with Pillow and the DejaVu
fonts, so the page can be re-typeset without touching the picture.

Run:  python3 compose.py     -> writes entry.png next to this script
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(HERE, "hero.webp")
OUT_PATH = os.path.join(HERE, "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PAGE = 1024
MARGIN = 40
WIDTH = PAGE - 2 * MARGIN  # 944 px of live matter

PAPER = (250, 247, 238)
INK = (22, 20, 18)
FADED = (96, 90, 82)
ACCENT = (122, 28, 28)
HAIRLINE = (60, 56, 50)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start_size, max_width):
    """Largest size <= start_size at which text fits max_width."""
    size = start_size
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured with the real font metrics."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((PAGE - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, y, thickness=1, fill=INK):
    draw.rectangle([MARGIN, y, PAGE - MARGIN, y + thickness - 1], fill=fill)
    return y + thickness


def paste_hero(canvas, box):
    """Centre-crop the photograph into box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    img = Image.open(HERO_PATH).convert("RGB")
    scale = max(tw / img.width, th / img.height)
    resized = img.resize(
        (round(img.width * scale), round(img.height * scale)),
        Image.LANCZOS,
    )
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    canvas.paste(resized.crop((left, top, left + tw, top + th)), (x0, y0))


def story(draw, x, y, col_width, dateline, headline, body):
    """One secondary story; returns the y just below it."""
    head_f = font(SANS_BOLD, 18)
    body_f = font(SANS, 13)
    head_lines = wrap(draw, dateline + " — " + headline, head_f, col_width)
    for line in head_lines:
        draw.text((x, y), line, font=head_f, fill=INK)
        y += 21
    y += 3
    for line in wrap(draw, body, body_f, col_width):
        draw.text((x, y), line, font=body_f, fill=INK)
        y += 16
    return y


def main():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- masthead ------------------------------------------------------
    y = rule(draw, 16, 1, HAIRLINE)
    y += 8
    masthead_f = fit_font(draw, "THE WORLD IN ONE DAY", SERIF_BOLD, 54, WIDTH)
    y = centered(draw, y, "THE WORLD IN ONE DAY", masthead_f)
    y += 6
    centered(draw, y, "FRIDAY · 20 NOVEMBER 2026", font(SANS_BOLD, 16), FADED)
    y += 26
    y = rule(draw, y, 4)
    y += 3
    y = rule(draw, y, 1)
    y += 10

    # ---- hero photograph ------------------------------------------------
    hero_h = 330
    paste_hero(page, (MARGIN, y, PAGE - MARGIN, y + hero_h))
    draw = ImageDraw.Draw(page)  # paste invalidates nothing, but be safe
    y += hero_h + 6
    centered(
        draw,
        y,
        "The Peace Palace in The Hague at dawn, as crowds gathered for the World Court's judgment.",
        font(SANS, 13),
        FADED,
    )
    y += 18

    # ---- lead story ------------------------------------------------------
    centered(draw, y, "THE HAGUE · INTERNATIONAL COURT OF JUSTICE",
             font(SANS_BOLD, 13), ACCENT)
    y += 18
    lead_head_f = font(SERIF_BOLD, 34)
    for line in wrap(
        draw,
        "World Court Rules Myanmar's Military Committed Genocide Against the Rohingya",
        lead_head_f,
        WIDTH,
    ):
        centered(draw, y, line, lead_head_f)
        y += 40
    y += 4
    lead_body_f = font(SERIF, 16)
    for line in wrap(
        draw,
        "The International Court of Justice ruled 9–6 that Myanmar's military "
        "committed genocide against the Rohingya minority in northern Rakhine "
        "State — the first time the court has held a state responsible for genocide.",
        lead_body_f,
        WIDTH,
    ):
        draw.text((MARGIN, y), line, font=lead_body_f, fill=INK)
        y += 20
    y += 6
    y = rule(draw, y, 1, HAIRLINE)
    y += 10

    # ---- secondary stories, two columns ----------------------------------
    gutter = 30
    col_w = (WIDTH - gutter) // 2
    col_x = (MARGIN, MARGIN + col_w + gutter)

    left_bottom = story(
        draw, col_x[0], y, col_w, "KYIV",
        "Russian Strikes Hit Dnipro Bridges",
        "Overnight missile and drone strikes on bridges across the Dnipro "
        "River killed eight people and wounded 28 across nine regions. "
        "Poland said Russian missiles and a drone violated its airspace, "
        "and Estonia said it would close its border with Russia for six months.",
    )
    left_bottom = story(
        draw, col_x[0], left_bottom + 8, col_w, "SHENZHEN",
        "Trump, Xi and Putin Issue Joint Declaration",
        "The three leaders issued a four-point joint declaration after "
        "their first trilateral meeting, but 70 minutes of talks brought "
        "no breakthrough on Ukraine, Iran or nuclear weapons. In Berlin, "
        "envoy Jared Kushner said Russia was “comfortable” with NATO "
        "Article 5-style security guarantees for Ukraine.",
    )

    right_bottom = story(
        draw, col_x[1], y, col_w, "RIYADH",
        "Houthi Missile Hits Financial District",
        "A Houthi missile struck Riyadh's financial district and damaged "
        "the Public Investment Fund tower. Saudi Arabia intercepted "
        "another missile and five drones on Friday.",
    )
    right_bottom = story(
        draw, col_x[1], right_bottom + 8, col_w, "MARKETS",
        "Anthropic Soars on Debut as Stocks Slide",
        "Anthropic closed 17% above its offer price on its Nasdaq debut, "
        "but the S&P 500 fell for a fifth straight day, Japan's Nikkei "
        "dropped 4.8%, SoftBank plunged 16% and gold fell 4.2%. The IMF "
        "warned global public debt is nearing 100% of world GDP.",
    )

    y = max(left_bottom, right_bottom) + 12

    # ---- ALSO TODAY band ---------------------------------------------------
    y = rule(draw, y, 1, HAIRLINE)
    y += 8
    draw.text((MARGIN, y), "ALSO TODAY", font=font(SANS_BOLD, 14), fill=ACCENT)
    y += 21
    also_f = font(SANS, 12)
    also_items = [
        "GTA VI is the biggest entertainment launch in history: $2.36 billion and 24.6 million copies on day one (Sensor Tower estimates)",
        "Kenya discharges its last Ebola patient, 37 days after the first case",
        "Ukraine hits the Kerch Bridge for the third time this week, halting rail traffic",
        "US Senate blocks bid to end the Iran war 51–48; Trump will not decide next steps until the new year",
        "Youth protests over living costs and militarisation in more than 25 countries",
        "IAEA says North Korea is expanding uranium enrichment",
    ]
    for item in also_items:
        lines = wrap(draw, "•  " + item, also_f, WIDTH)
        for line in lines:
            draw.text((MARGIN, y), line, font=also_f, fill=INK)
            y += 14
    y += 6
    y = rule(draw, y, 1, HAIRLINE)

    # ---- footer -------------------------------------------------------------
    y += 10
    centered(
        draw,
        y,
        "Compiled from news reporting of Friday 20 November 2026 — wire services and international outlets.",
        font(SANS, 11),
        FADED,
    )

    assert y + 16 <= PAGE, f"page overflow: content ends at {y}"
    page.save(OUT_PATH, format="PNG")
    print(f"wrote {OUT_PATH} (content ends at y={y})")


if __name__ == "__main__":
    main()
