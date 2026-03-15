#!/usr/bin/env python3

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path.home() / ".codex/skills/canvas-design/canvas-fonts"


PROJECTS = {
    "skillforge": {
        "subtitle": "OpenClaw skill scaffolding for agent teams",
        "command": "brew install itamaker/tap/skillforge",
        "labels": ["openclaw", "scaffold", "go cli"],
        "show_command": True,
        "subtitle_max_width": 620,
        "palette": {
            "bg0": "#101515",
            "bg1": "#183231",
            "base": "#E9E1D3",
            "muted": "#A6B5AF",
            "accent": "#F26A3D",
            "accent2": "#6FD1C8",
            "line": "#284846",
            "shadow": "#09100F",
        },
        "motif": "forge",
    },
    "runlens": {
        "subtitle": "Trace latency, failures, and token-heavy runs",
        "command": "brew install itamaker/tap/runlens",
        "labels": ["observability", "jsonl", "go cli"],
        "show_command": True,
        "subtitle_max_width": 620,
        "palette": {
            "bg0": "#0E1420",
            "bg1": "#1B2741",
            "base": "#E8EDF6",
            "muted": "#9FB0CC",
            "accent": "#68C0FF",
            "accent2": "#CFF264",
            "line": "#263451",
            "shadow": "#060B14",
        },
        "motif": "lens",
    },
    "ragcheck": {
        "subtitle": "Fast retrieval evaluation for engineering and research",
        "command": "brew install itamaker/tap/ragcheck",
        "labels": ["retrieval", "metrics", "go cli"],
        "show_command": True,
        "subtitle_max_width": 620,
        "palette": {
            "bg0": "#16100E",
            "bg1": "#3B221A",
            "base": "#F4E9D8",
            "muted": "#C6B39C",
            "accent": "#FF8C5A",
            "accent2": "#FFCF70",
            "line": "#5A342A",
            "shadow": "#0C0807",
        },
        "motif": "rank",
    },
    "promptdeck": {
        "subtitle": "Prompt templating and experiment matrix generation",
        "command": "brew install itamaker/tap/promptdeck",
        "labels": ["templates", "experiments", "go cli"],
        "show_command": True,
        "subtitle_max_width": 620,
        "palette": {
            "bg0": "#141119",
            "bg1": "#2F1E39",
            "base": "#F6EFE8",
            "muted": "#C5B1CC",
            "accent": "#FF7A59",
            "accent2": "#5CE0D2",
            "line": "#4B3157",
            "shadow": "#0C0910",
        },
        "motif": "cards",
    },
    "datasetlint": {
        "subtitle": "Catch duplicates, empty fields, and split leakage",
        "command": "brew install itamaker/tap/datasetlint",
        "labels": ["datasets", "quality", "go cli"],
        "show_command": True,
        "subtitle_max_width": 620,
        "palette": {
            "bg0": "#0F1411",
            "bg1": "#1F3526",
            "base": "#EFF0E7",
            "muted": "#AFC0B0",
            "accent": "#9BD449",
            "accent2": "#F2B94B",
            "line": "#35503C",
            "shadow": "#070B08",
        },
        "motif": "grid",
    },
    "go-chrome-ai": {
        "subtitle": "Patch Chrome Local State for Ask Gemini with CLI or GUI",
        "command": "brew install --cask itamaker/tap/go-chrome-ai",
        "labels": ["chrome ai", "desktop", "go tool"],
        "title_size": 84,
        "subtitle_size": 28,
        "subtitle_max_width": 620,
        "show_command": True,
        "command_font_size": 18,
        "command_max_width": 520,
        "motif_box": (820, 150, 1150, 460),
        "palette": {
            "bg0": "#121316",
            "bg1": "#1D2E38",
            "base": "#F2EFE5",
            "muted": "#B9C7CF",
            "accent": "#F59D3D",
            "accent2": "#4DD2C4",
            "line": "#314753",
            "shadow": "#0A0D10",
        },
        "motif": "browser",
    },
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size=size)


TITLE_FONT = "BricolageGrotesque-Bold.ttf"
BODY_FONT = "InstrumentSans-Regular.ttf"
META_FONT = "GeistMono-Regular.ttf"
META_BOLD_FONT = "GeistMono-Bold.ttf"


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def with_alpha(color: str, alpha: int) -> tuple[int, int, int, int]:
    return (*hex_rgb(color), alpha)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c0: str, c1: str, t: float) -> tuple[int, int, int]:
    a = hex_rgb(c0)
    b = hex_rgb(c1)
    return tuple(int(lerp(a[i], b[i], t)) for i in range(3))


def draw_gradient(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    width, height = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        row = mix(top, bottom, t)
        for x in range(width):
            px[x, y] = row
    return img


def add_blur_glow(base: Image.Image, center: tuple[int, int], radius: int, color: str, alpha: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=with_alpha(color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=42))
    base.alpha_composite(layer)


def draw_frame(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], color: str, width: int = 2) -> None:
    draw.rounded_rectangle(bounds, radius=28, outline=hex_rgb(color), width=width)


def draw_grid(base: Image.Image, color: str, step: int, alpha: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    width, height = base.size
    rgba = with_alpha(color, alpha)
    for x in range(step, width, step):
        draw.line((x, 0, x, height), fill=rgba, width=1)
    for y in range(step, height, step):
        draw.line((0, y, width, y), fill=rgba, width=1)
    base.alpha_composite(layer)


def draw_dots(base: Image.Image, color: str, spacing: int, alpha: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    width, height = base.size
    rgba = with_alpha(color, alpha)
    for y in range(spacing // 2, height, spacing):
        for x in range(spacing // 2, width, spacing):
            draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=rgba)
    base.alpha_composite(layer)


def draw_label_pill(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    palette: dict[str, str],
) -> int:
    tag_font = font(META_FONT, 20)
    x, y = xy
    left, top, right, bottom = draw.textbbox((x, y), text.upper(), font=tag_font)
    pad_x = 16
    pad_y = 10
    draw.rounded_rectangle(
        (left - pad_x, top - pad_y, right + pad_x, bottom + pad_y),
        radius=18,
        fill=with_alpha(palette["line"], 130),
        outline=with_alpha(palette["accent2"], 110),
        width=1,
    )
    draw.text((x, y), text.upper(), font=tag_font, fill=hex_rgb(palette["base"]))
    return (right - left) + pad_x * 2


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    text_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    if not words:
        return [text]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        left, _, right, _ = draw.textbbox((0, 0), candidate, font=text_font)
        if right - left <= max_width:
            current = candidate
            continue
        lines.append(current)
        current = word
    lines.append(current)
    return lines


def draw_command_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    command: str,
    palette: dict[str, str],
    command_font: ImageFont.FreeTypeFont,
    label_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(
        box,
        radius=24,
        fill=with_alpha(palette["line"], 110),
        outline=with_alpha(palette["accent2"], 120),
        width=2,
    )

    label = "INSTALL"
    draw.text((x0 + 20, y0 + 14), label, font=label_font, fill=hex_rgb(palette["accent2"]))

    command_lines = wrap_text(draw, command, command_font, max_width)
    line_height = command_font.size + 8
    text_y = y0 + 42
    for idx, line in enumerate(command_lines):
        draw.text((x0 + 20, text_y + idx * line_height), line, font=command_font, fill=hex_rgb(palette["base"]))


def draw_forge(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, str]) -> None:
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    size = min(x1 - x0, y1 - y0) * 0.78
    for idx, scale in enumerate((1.0, 0.78, 0.56)):
        s = size * scale
        points = [
            (cx, cy - s / 2),
            (cx + s / 2, cy),
            (cx, cy + s / 2),
            (cx - s / 2, cy),
        ]
        color = palette["accent"] if idx == 0 else palette["accent2"] if idx == 1 else palette["base"]
        draw.line(points + [points[0]], fill=hex_rgb(color), width=8 if idx == 0 else 6)
    draw.line((cx - size * 0.12, cy + size * 0.24, cx + size * 0.18, cy - size * 0.18), fill=hex_rgb(palette["accent"]), width=10)
    for offset in (-0.22, -0.08, 0.06):
        draw.line(
            (cx + size * offset, cy + size * 0.34, cx + size * (offset + 0.12), cy + size * 0.20),
            fill=hex_rgb(palette["accent2"]),
            width=4,
        )


def draw_lens(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, str]) -> None:
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    radius = min(x1 - x0, y1 - y0) * 0.34
    for idx, width in enumerate((18, 10, 4)):
        r = radius - idx * 38
        color = palette["accent"] if idx == 0 else palette["base"] if idx == 1 else palette["accent2"]
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=hex_rgb(color), width=width)
    for idx in range(5):
        y = cy - radius + idx * radius * 0.52
        draw.arc((cx - radius * 1.25, y - 38, cx + radius * 1.25, y + 38), start=190, end=350, fill=hex_rgb(palette["accent2"]), width=4)
    draw.line((cx + radius * 0.72, cy + radius * 0.72, cx + radius * 1.26, cy + radius * 1.26), fill=hex_rgb(palette["accent"]), width=18)
    draw.ellipse((cx + radius * 1.16 - 18, cy + radius * 1.16 - 18, cx + radius * 1.16 + 18, cy + radius * 1.16 + 18), fill=hex_rgb(palette["accent"]))


def draw_rank(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, str]) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    height = y1 - y0
    bar_width = width * 0.12
    gap = width * 0.05
    start_x = x0 + width * 0.12
    base_y = y0 + height * 0.82
    heights = [0.22, 0.38, 0.58, 0.76]
    colors = [palette["line"], palette["muted"], palette["accent2"], palette["accent"]]
    centers = []
    for idx, h in enumerate(heights):
        left = start_x + idx * (bar_width + gap)
        top = base_y - height * h
        right = left + bar_width
        draw.rounded_rectangle((left, top, right, base_y), radius=18, fill=hex_rgb(colors[idx]))
        centers.append((left + bar_width / 2, top + 10))
    path = []
    for idx, (cx, top) in enumerate(centers):
        path.append((cx, top + 18))
        if idx < len(centers) - 1:
            next_cx, next_top = centers[idx + 1]
            path.append(((cx + next_cx) / 2, min(top, next_top) - 24))
    draw.line(path, fill=hex_rgb(palette["base"]), width=8, joint="curve")
    draw.line((centers[-2][0] - 28, centers[-1][1] + 44, centers[-1][0], centers[-1][1] + 70, centers[-1][0] + 54, centers[-1][1] + 10), fill=hex_rgb(palette["accent"]), width=10, joint="curve")


def draw_cards(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, str]) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    height = y1 - y0
    cards = [
        (x0 + width * 0.18, y0 + height * 0.22, x0 + width * 0.72, y0 + height * 0.72, palette["line"], -16),
        (x0 + width * 0.28, y0 + height * 0.16, x0 + width * 0.82, y0 + height * 0.66, palette["accent2"], 0),
        (x0 + width * 0.38, y0 + height * 0.10, x0 + width * 0.92, y0 + height * 0.60, palette["accent"], 16),
    ]
    for left, top, right, bottom, color, shift in cards:
        draw.rounded_rectangle((left, top + shift, right, bottom + shift), radius=28, fill=hex_rgb(color))
        inset = 24
        draw.rounded_rectangle(
            (left + inset, top + shift + inset, right - inset, bottom + shift - inset),
            radius=18,
            outline=with_alpha(palette["base"], 190),
            width=3,
        )
        draw.line((left + inset * 1.2, top + shift + 70, right - inset * 1.2, top + shift + 70), fill=with_alpha(palette["base"], 160), width=3)
        draw.line((left + inset * 1.2, top + shift + 110, right - inset * 2.2, top + shift + 110), fill=with_alpha(palette["base"], 120), width=3)


def draw_grid_scan(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, str]) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    height = y1 - y0
    cols = 5
    rows = 5
    cell_w = width * 0.12
    cell_h = height * 0.12
    gap = width * 0.03
    start_x = x0 + width * 0.12
    start_y = y0 + height * 0.18
    highlights = {(1, 2), (3, 1), (2, 3)}
    for row in range(rows):
        for col in range(cols):
            left = start_x + col * (cell_w + gap)
            top = start_y + row * (cell_h + gap)
            right = left + cell_w
            bottom = top + cell_h
            fill = palette["accent2"] if (col, row) in highlights else palette["line"]
            draw.rounded_rectangle((left, top, right, bottom), radius=12, fill=hex_rgb(fill))
            if (col, row) in highlights:
                draw.line((left + 14, bottom - 24, left + 34, bottom - 8, right - 14, top + 16), fill=hex_rgb(palette["bg0"]), width=5)
    ring_x = x0 + width * 0.72
    ring_y = y0 + height * 0.68
    radius = width * 0.15
    draw.ellipse((ring_x - radius, ring_y - radius, ring_x + radius, ring_y + radius), outline=hex_rgb(palette["accent"]), width=16)
    draw.line((ring_x + radius * 0.72, ring_y + radius * 0.72, ring_x + radius * 1.28, ring_y + radius * 1.28), fill=hex_rgb(palette["accent"]), width=16)
    draw.line((ring_x - radius, ring_y, ring_x + radius, ring_y), fill=hex_rgb(palette["base"]), width=4)
    draw.line((ring_x, ring_y - radius, ring_x, ring_y + radius), fill=hex_rgb(palette["base"]), width=4)


def draw_browser(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], palette: dict[str, str]) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    height = y1 - y0
    outer = (x0 + width * 0.10, y0 + height * 0.12, x1 - width * 0.06, y1 - height * 0.16)
    draw.rounded_rectangle(outer, radius=36, fill=hex_rgb(palette["line"]), outline=hex_rgb(palette["accent2"]), width=4)

    header_y = outer[1] + height * 0.14
    draw.line((outer[0] + 18, header_y, outer[2] - 18, header_y), fill=with_alpha(palette["base"], 180), width=3)

    bubble_y = outer[1] + 26
    bubble_x = outer[0] + 28
    for idx, color in enumerate((palette["accent"], palette["accent2"], palette["base"])):
        draw.ellipse((bubble_x + idx * 28, bubble_y, bubble_x + idx * 28 + 14, bubble_y + 14), fill=hex_rgb(color))

    panel = (outer[0] + width * 0.10, outer[1] + height * 0.22, outer[2] - width * 0.12, outer[3] - height * 0.20)
    draw.rounded_rectangle(panel, radius=24, outline=with_alpha(palette["base"], 150), width=3)
    draw.line((panel[0] + 24, panel[1] + 42, panel[2] - 24, panel[1] + 42), fill=with_alpha(palette["base"], 120), width=3)
    draw.line((panel[0] + 24, panel[1] + 84, panel[2] - 80, panel[1] + 84), fill=with_alpha(palette["base"], 80), width=3)

    toggle = (panel[0] + width * 0.08, panel[3] - height * 0.14, panel[0] + width * 0.36, panel[3] - height * 0.03)
    draw.rounded_rectangle(toggle, radius=32, fill=hex_rgb(palette["accent"]))
    knob_r = (toggle[3] - toggle[1]) * 0.44
    knob_cx = toggle[2] - knob_r - 10
    knob_cy = (toggle[1] + toggle[3]) / 2
    draw.ellipse((knob_cx - knob_r, knob_cy - knob_r, knob_cx + knob_r, knob_cy + knob_r), fill=hex_rgb(palette["bg0"]))

    spark_cx = outer[2] - width * 0.10
    spark_cy = outer[1] + height * 0.18
    draw.line((spark_cx, spark_cy - 42, spark_cx, spark_cy + 42), fill=hex_rgb(palette["accent2"]), width=6)
    draw.line((spark_cx - 42, spark_cy, spark_cx + 42, spark_cy), fill=hex_rgb(palette["accent2"]), width=6)
    draw.line((spark_cx - 28, spark_cy - 28, spark_cx + 28, spark_cy + 28), fill=hex_rgb(palette["base"]), width=4)
    draw.line((spark_cx - 28, spark_cy + 28, spark_cx + 28, spark_cy - 28), fill=hex_rgb(palette["base"]), width=4)


MOTIFS = {
    "forge": draw_forge,
    "lens": draw_lens,
    "rank": draw_rank,
    "cards": draw_cards,
    "grid": draw_grid_scan,
    "browser": draw_browser,
}


def render_social(name: str, config: dict[str, object], out_path: Path) -> None:
    palette = config["palette"]
    img = draw_gradient((1280, 640), palette["bg0"], palette["bg1"]).convert("RGBA")
    add_blur_glow(img, (985, 210), 180, palette["accent"], 58)
    add_blur_glow(img, (1080, 470), 150, palette["accent2"], 48)
    draw_grid(img, palette["line"], 64, 28)
    draw_dots(img, palette["base"], 80, 30)
    draw = ImageDraw.Draw(img)

    draw_frame(draw, (28, 28, 1252, 612), palette["line"], width=3)
    draw.line((100, 126, 520, 126), fill=with_alpha(palette["line"], 180), width=2)

    label_font = font(META_BOLD_FONT, 22)
    title_font = font(TITLE_FONT, int(config.get("title_size", 108)))
    subtitle_font = font(BODY_FONT, int(config.get("subtitle_size", 34)))
    command_font = font(META_FONT, int(config.get("command_font_size", 20)))
    command_label_font = font(META_BOLD_FONT, 18)

    draw.text((100, 84), "ITAMAKER / AI CLI", font=label_font, fill=hex_rgb(palette["accent2"]))
    title_y = 150
    draw.text((100, title_y), name, font=title_font, fill=hex_rgb(palette["base"]))
    _, _, _, title_bottom = draw.textbbox((100, title_y), name, font=title_font)

    subtitle = config["subtitle"]
    subtitle_y = title_bottom + 18
    subtitle_max_width = config.get("subtitle_max_width")
    if subtitle_max_width:
        subtitle_lines = wrap_text(draw, subtitle, subtitle_font, int(subtitle_max_width))
    else:
        subtitle_lines = [subtitle]

    line_height = subtitle_font.size + 10
    for idx, line in enumerate(subtitle_lines):
        draw.text((104, subtitle_y + idx * line_height), line, font=subtitle_font, fill=hex_rgb(palette["muted"]))
    subtitle_bottom = subtitle_y + (len(subtitle_lines) - 1) * line_height + subtitle_font.size

    pill_x = 104
    pill_y = subtitle_bottom + 34
    for label in config["labels"]:
        pill_x += draw_label_pill(draw, (pill_x + 18, pill_y), label, palette) + 18

    if config.get("show_command", True):
        panel_top = max(pill_y + 54, 456)
        panel_box = (100, panel_top, 690, panel_top + 98)
        draw_command_panel(
            draw,
            panel_box,
            config["command"],
            palette,
            command_font,
            command_label_font,
            int(config.get("command_max_width", 530)),
        )
    motif_box = config.get("motif_box", (720, 120, 1180, 520))
    MOTIFS[config["motif"]](draw, motif_box, palette)

    corner = [(1144, 552), (1178, 552), (1178, 586)]
    draw.line(corner, fill=hex_rgb(palette["accent"]), width=5)
    img.convert("RGB").save(out_path)


def render_logo(name: str, config: dict[str, object], out_path: Path) -> None:
    palette = config["palette"]
    img = draw_gradient((512, 512), palette["bg0"], palette["bg1"]).convert("RGBA")
    add_blur_glow(img, (372, 148), 110, palette["accent"], 72)
    add_blur_glow(img, (396, 356), 96, palette["accent2"], 58)
    draw_grid(img, palette["line"], 48, 26)
    draw = ImageDraw.Draw(img)
    draw_frame(draw, (22, 22, 490, 490), palette["line"], width=3)
    motif_box = (74, 82, 438, 410)
    MOTIFS[config["motif"]](draw, motif_box, palette)
    word_font = font(META_BOLD_FONT, 24)
    draw.text((42, 446), name.upper(), font=word_font, fill=hex_rgb(palette["base"]))
    img.convert("RGB").save(out_path)


def main() -> None:
    for name, config in PROJECTS.items():
        out_dir = ROOT / name / "docs" / "images"
        out_dir.mkdir(parents=True, exist_ok=True)
        render_social(name, config, out_dir / "social-preview.png")
        render_logo(name, config, out_dir / "logo-mark.png")


if __name__ == "__main__":
    main()
