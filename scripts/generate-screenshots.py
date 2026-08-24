# -*- coding: utf-8 -*-
"""Generate VS Code interface preview screenshot for Soft Sky Theme.
Outputs:
  screenshots/en/screenshot-1-browser.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_EN = os.path.join(BASE, "screenshots", "en", "screenshot-1-browser.png")
OUT_EN_STORE = os.path.join(BASE, "store-assets", "screenshots", "en", "screenshot-1-browser.png")
OUT_ZH_STORE = os.path.join(BASE, "store-assets", "screenshots", "zh", "screenshot-1-browser.png")
W, H = 1440, 900

P = {
    "titleBar": "#0F1722",
    "titleText": "#AFC4DC",
    "activityBar": "#111A26",
    "activityIcon": "#4E6480",
    "activityIconActive": "#7CC4F8",
    "sideBar": "#111A26",
    "sideBarText": "#C6D2E0",
    "sideBarSub": "#6B7C93",
    "tabActive": "#141D2A",
    "tabInactive": "#0D1520",
    "tabBorder": "#26374E",
    "editorBg": "#141D2A",
    "editorText": "#C6D2E0",
    "lineNumber": "#3A4D66",
    "lineNumberActive": "#7CC4F8",
    "statusBar": "#0D1520",
    "statusText": "#8FA2B8",
    "accent": "#7CC4F8",
    "border": "#26374E",
    "keyword": "#9FB3DF",
    "function": "#7CC4F8",
    "string": "#F5DFA8",
    "number": "#F0B7A4",
    "comment": "#5E7388",
    "type": "#BDDDE4",
    "tag": "#9FB3DF",
    "property": "#8FB7E8",
}


def hex_to_rgba(h, alpha=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def load_fonts(lang="en"):
    mono_candidates = [
        "C:\\Windows\\Fonts\\JetBrainsMono-Regular.ttf",
        "C:\\Windows\\Fonts\\FiraCode-Regular.ttf",
        "C:\\Windows\\Fonts\\Consolas.ttf",
        "C:\\Windows\\Fonts\\Courier New.ttf",
    ]
    mono = next((p for p in mono_candidates if os.path.exists(p)), None)
    if lang == "zh":
        ui = next((p for p in ("C:\\Windows\\Fonts\\msyh.ttc", "C:\\Windows\\Fonts\\simhei.ttf")
                   if os.path.exists(p)), mono)
    else:
        ui = mono

    def _load(path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()

    return {
        "ui": _load(ui, 16),
        "ui_small": _load(ui, 13),
        "code": _load(mono, 18),
        "code_small": _load(mono, 14),
        "title": _load(ui, 13),
    }


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_code_line(draw, x, y, tokens, font, line_h):
    cx = x
    for text, color in tokens:
        draw.text((cx, y), text, fill=color, font=font)
        w, _ = text_size(draw, text, font)
        cx += w
    return y + line_h


def build_code_tokens():
    k = P["keyword"]
    f = P["function"]
    s = P["string"]
    n = P["number"]
    c = P["comment"]
    t = P["type"]
    tag = P["tag"]
    prop = P["property"]
    txt = P["editorText"]
    punc = txt

    lines = [
        [("// Soft Sky - a calm morning React hook", c)],
        [("import ", k), ("{ useState, useEffect }", txt), (" from ", k), ("'react'", s), (";", punc)],
        [("",)],
        [("export ", k), ("const ", k), ("useSunrise", f), (" = ", punc), ("(", punc), ("altitude", txt), (": ", punc), ("number", t), (")", punc), (" => ", punc), ("{", punc)],
        [("  const ", k), ("[clouds, setClouds]", txt), (" = ", punc), ("useState", f), ("(", punc), ("[]", punc), (");", punc)],
        [("",)],
        [("  useEffect", f), ("(()", punc), (" => ", punc), ("{", punc)],
        [("    const ", k), ("timer", txt), (" = ", punc), ("setInterval", f), ("(()", punc), (" => ", punc), ("{", punc)],
        [("      setClouds", f), ("(", punc), ("c", txt), (" => ", punc), ("[...c.slice(", txt), ("-5", n), ("), ", txt), ("{", punc), ("drift", txt), (": ", punc), ("Math.random", f), ("()", punc), ("}]", punc), (");", punc)],
        [("    }, ", punc), ("15000", n), (");", punc)],
        [("    return ", k), ("()", punc), (" => ", punc), ("clearInterval", f), ("(timer);", punc)],
        [("  }, []);", punc)],
        [("",)],
        [("  return ", k), ("{ clouds, altitude };", txt)],
        [("};", punc)],
        [("",)],
        [("const ", k), ("SkyCard", f), (" = ", punc), ("(", punc), ("{ title }", txt), (": ", punc), ("{ title: string }", t), (")", punc), (" => ", punc), ("{", punc)],
        [("  return ", k), ("(", punc)],
        [("    <", punc), ("div", tag), (" className", prop), ("=", punc), ("\"sky-card\"", s), (">", punc)],
        [("      <", punc), ("h2", tag), (">{title}</", punc), ("h2", tag), (">", punc)],
        [("      <", punc), ("p", tag), (">{", punc), ("\"Breathe in the blue.\"", s), ("}</", punc), ("p", tag), (">", punc)],
        [("    </", punc), ("div", tag), (">", punc)],
        [("  );", punc)],
        [("};", punc)],
    ]
    return lines


def draw_activity_icon(d, idx, cx, cy, color, bar_color):
    if idx == 0:  # files
        d.rounded_rectangle((cx - 7, cy - 10, cx + 7, cy + 10), radius=2, outline=color, width=2)
        d.polygon([(cx - 1, cy - 10), (cx + 7, cy - 10), (cx + 7, cy - 2)], fill=color)
        d.line((cx - 1, cy - 10, cx + 7, cy - 2), fill=bar_color, width=2)
    elif idx == 1:  # search
        d.ellipse((cx - 6, cy - 7, cx + 4, cy + 3), outline=color, width=2)
        d.line((cx + 2, cy + 2, cx + 8, cy + 8), fill=color, width=2)
    elif idx == 2:  # source control branch
        d.ellipse((cx - 7, cy - 9, cx - 1, cy - 3), outline=color, width=2)
        d.ellipse((cx - 7, cy + 3, cx - 1, cy + 9), outline=color, width=2)
        d.ellipse((cx + 1, cy - 3, cx + 7, cy + 3), outline=color, width=2)
        d.line((cx - 4, cy - 3, cx - 4, cy + 3), fill=color, width=2)
        d.line((cx - 4, cy, cx + 1, cy), fill=color, width=2)
    elif idx == 3:  # extensions
        d.rounded_rectangle((cx - 8, cy - 8, cx - 1, cy - 1), radius=1, outline=color, width=2)
        d.rounded_rectangle((cx + 1, cy - 8, cx + 8, cy - 1), radius=1, outline=color, width=2)
        d.rounded_rectangle((cx - 8, cy + 1, cx - 1, cy + 8), radius=1, outline=color, width=2)
        d.rounded_rectangle((cx + 1, cy + 1, cx + 8, cy + 8), radius=1, outline=color, width=2)
        d.polygon([(cx + 7, cy + 4), (cx + 10, cy + 7), (cx + 7, cy + 10), (cx + 4, cy + 7)], fill=hex_to_rgba(P["accent"]))
    elif idx == 4:  # run and debug
        d.polygon([(cx - 7, cy - 9), (cx + 9, cy), (cx - 7, cy + 9)], fill=color)
    else:  # settings gear
        import math
        d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=color)
        for angle in (0, 45, 90, 135, 180, 225, 270, 315):
            rad = math.radians(angle)
            d.line((cx + 9 * math.cos(rad), cy + 9 * math.sin(rad),
                    cx + 13 * math.cos(rad), cy + 13 * math.sin(rad)), fill=color, width=5)
        d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=hex_to_rgba(P["activityBar"]))


def draw_screenshot(lang="en"):
    img = Image.new("RGBA", (W, H), hex_to_rgba(P["editorBg"]))
    d = ImageDraw.Draw(img)
    fonts = load_fonts(lang)

    # Title bar
    d.rectangle((0, 0, W, 32), fill=hex_to_rgba(P["titleBar"]))
    d.text((96, 9), "Soft Sky Theme - Visual Studio Code", fill=hex_to_rgba(P["titleText"]), font=fonts["title"])
    for i, color in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        d.ellipse((16 + i * 18, 10, 28 + i * 18, 22), fill=hex_to_rgba(color))

    # Activity bar
    d.rectangle((0, 32, 52, H - 24), fill=hex_to_rgba(P["activityBar"]))
    for i in range(5):
        y = 56 + i * 46
        color = P["activityIconActive"] if i == 3 else P["activityIcon"]
        if i == 3:
            d.rectangle((0, y - 9, 3, y + 25), fill=hex_to_rgba(P["accent"]))
        draw_activity_icon(d, i, 26, y + 10, hex_to_rgba(color), P["activityBar"])

    # Sidebar
    sb_x, sb_w = 52, 220
    d.rectangle((sb_x, 32, sb_x + sb_w, H - 24), fill=hex_to_rgba(P["sideBar"]))
    explorer_label = "\u8d44\u6e90\u7ba1\u7406\u5668" if lang == "zh" else "EXPLORER"
    d.text((sb_x + 16, 48), explorer_label, fill=hex_to_rgba(P["sideBarSub"]), font=fonts["ui_small"])
    d.text((sb_x + 16, 74), "v SOFT-SKY", fill=hex_to_rgba(P["sideBarText"]), font=fonts["ui"])
    files = [
        ("  package.json", P["sideBarText"]),
        ("  themes", P["sideBarText"]),
        ("    soft-sky-color-theme.json", P["accent"]),
        ("  README.md", P["sideBarText"]),
        ("  CHANGELOG.md", P["sideBarText"]),
        ("  LICENSE", P["sideBarText"]),
    ]
    y = 102
    for name, color in files:
        d.text((sb_x + 16, y), name, fill=hex_to_rgba(color), font=fonts["ui_small"])
        y += 26

    # Tabs
    tabs = [("soft-sky-color-theme.json", False), ("package.json", False), ("preview.tsx", True)]
    tab_x = sb_x + sb_w
    tab_y = 32
    tab_h = 38
    for name, active in tabs:
        color = P["tabActive"] if active else P["tabInactive"]
        w, _ = text_size(d, name, fonts["ui"])
        tab_w = w + 56
        d.rectangle((tab_x, tab_y, tab_x + tab_w, tab_y + tab_h), fill=hex_to_rgba(color))
        if active:
            d.rectangle((tab_x, tab_y + tab_h - 2, tab_x + tab_w, tab_y + tab_h), fill=hex_to_rgba(P["accent"]))
        d.text((tab_x + 18, tab_y + 10), name, fill=hex_to_rgba(P["editorText"]), font=fonts["ui"])
        cx = tab_x + tab_w - 15
        cy = tab_y + 19
        cross_color = hex_to_rgba(P["sideBarSub"])
        d.line((cx - 3, cy - 3, cx + 3, cy + 3), fill=cross_color, width=1)
        d.line((cx + 3, cy - 3, cx - 3, cy + 3), fill=cross_color, width=1)
        tab_x += tab_w

    # Editor
    editor_x = sb_x + sb_w
    editor_y = tab_y + tab_h
    editor_w = W - editor_x
    editor_h = H - 24 - editor_y
    d.rectangle((editor_x, editor_y, editor_x + editor_w, editor_y + editor_h), fill=hex_to_rgba(P["editorBg"]))

    code_x = editor_x + 72
    code_y = editor_y + 30
    line_h = 26
    lines = build_code_tokens()
    for i, tokens in enumerate(lines):
        ln = i + 1
        ln_x = editor_x + 44
        ln_color = P["lineNumberActive"] if ln == 16 else P["lineNumber"]
        d.text((ln_x, code_y), str(ln), fill=hex_to_rgba(ln_color), font=fonts["code_small"], anchor="ra")
        if tokens and (len(tokens) > 1 or tokens[0][0]):
            draw_code_line(d, code_x, code_y, tokens, fonts["code"], line_h)
        code_y += line_h

    # Status bar
    d.rectangle((0, H - 24, W, H), fill=hex_to_rgba(P["statusBar"]))
    d.text((16, H - 21), "main*", fill=hex_to_rgba(P["statusText"]), font=fonts["ui_small"])
    d.text((180, H - 21), "TypeScript JSX", fill=hex_to_rgba(P["statusText"]), font=fonts["ui_small"])
    d.text((W - 220, H - 21), "Ln 16, Col 18", fill=hex_to_rgba(P["statusText"]), font=fonts["ui_small"])
    d.text((W - 90, H - 21), "UTF-8", fill=hex_to_rgba(P["statusText"]), font=fonts["ui_small"])

    return img


def main():
    outputs = [
        (OUT_EN, "en"),
        (OUT_EN_STORE, "en"),
        (OUT_ZH_STORE, "zh"),
    ]
    for out, lang in outputs:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        img = draw_screenshot(lang)
        img.convert("RGB").save(out)
        print("saved:", os.path.abspath(out), "size:", img.size, "mode: RGB")


if __name__ == "__main__":
    main()
