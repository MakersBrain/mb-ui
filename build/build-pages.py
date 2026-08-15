#!/usr/bin/env python3
"""Inline the webfonts into the style guide.

The Artifact CSP blocks every external host, so a linked font URL would fail
silently and the specimen would render in a fallback face -- which is exactly
the thing a type specimen must not do. This embeds the woff2 files as data
URIs instead.

    python3 brand/build-style-guide.py

Reads  brand/style-guide.src.html and brand/fonts/*.woff2
Writes brand/style-guide.html
"""

import base64
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "src"
FONTS = ROOT / "fonts"
PAGES_DIR = ROOT / "pages"

LATIN = (
    "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, "
    "U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, "
    "U+2212, U+2215, U+FEFF, U+FFFD"
)
LATIN_EXT = (
    "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, "
    "U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, "
    "U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF"
)

# family, weight range, file stem, unicode-range
FACES = [
    ("Bitter", "400 700", "bitter-latin", LATIN),
    ("Bitter", "400 700", "bitter-latinext", LATIN_EXT),
    ("IBM Plex Sans", "100 700", "plex-latin", LATIN),
    ("IBM Plex Sans", "100 700", "plex-latinext", LATIN_EXT),
]


def face_css(family: str, weight: str, stem: str, urange: str) -> str:
    path = FONTS / f"{stem}.woff2"
    if not path.exists():
        sys.exit(f"missing font: {path}\nSee fonts/README.md for the source URLs.")
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        "@font-face{"
        f"font-family:'{family}';font-style:normal;font-weight:{weight};"
        "font-display:block;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');"
        f"unicode-range:{urange};"
        "}"
    )



# Every page is self-contained: one file, no external requests. That is a hard
# requirement for the Artifact runtime and a convenience everywhere else --
# deploying the landing page is copying one file. The cost is ~190 KB of
# base64 font in each, which is the right trade for pages of this size.
PAGES = [
    PAGES_DIR / "style-guide.src.html",
    PAGES_DIR / "design-chart.src.html",
]


def main() -> None:
    fonts = "\n".join(face_css(*f) for f in FACES)

    for src_path in PAGES:
        if not src_path.exists():
            continue
        src = src_path.read_text()
        if "__FONT_CSS__" not in src:
            sys.exit(f"{src_path.name} has no __FONT_CSS__ placeholder")

        out = src.replace("__FONT_CSS__", fonts)

        # Pages render with the real shipped stylesheets rather than a copy of
        # them, so a component on a page cannot drift from the component the
        # product actually gets.
        for token, name in (("__TOKENS_CSS__", "tokens.css"), ("__UI_CSS__", "ui.css")):
            if token in out:
                out = out.replace(token, (SRC / name).read_text())

        dest = src_path.with_name(src_path.name.replace(".src.html", ".html"))
        dest.write_text(out)
        print(f"wrote {dest.relative_to(ROOT)} ({len(out) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
