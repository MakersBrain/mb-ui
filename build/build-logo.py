#!/usr/bin/env python3
"""Generate the weave logo asset set, and the path constants that ship with it.

The wordmark is Bitter SemiBold outlined to paths, so no surface has to ship a
font to render the logo correctly. Bitter is SIL OFL 1.1; outlining glyphs into
a logo is permitted, and the licence notice lives in fonts/README.md.

    python3 build/build-logo.py

Requires inkscape and Bitter SemiBold installed for the wordmark step only.
Pass --skip-wordmark to regenerate everything else from the cached path data in
src/logo/wordmark.svg, and --no-raster to skip the PNG step.

Everything this writes is committed. The package has no build step -- a
consumer installs it and imports CSS, SVG, `.js` and `.svelte` directly -- so
the generated files have to be in the tree, and CI runs this with `--check` to
fail a commit where they are not.
"""

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "src"
LOGO = SRC / "logo"

INK = "#1E1915"        # sand-900
PAPER = "#F4EFEB"      # sand-100, the ink equivalent on dark grounds
CLAY = "#C05F3D"       # clay-500, the brand tone
CLAY_DARK = "#D27C5C"  # clay-400, stepped up so it survives on a dark ground
PAPER_GROUND = "#F7F3EE"  # --mb-bg, the ground raster assets are painted on

# The mark, in its 32-unit grid. Two strands crossing over and under: strand A
# is the top bar plus the left stem, strand B is the bottom bar plus the right
# stem. The third path puts A back on top at the top-right crossing, which is
# what makes it a weave rather than two overlapping brackets.
STRAND_A = "M3 3h26v6H9v20H3Z"
STRAND_B = "M29 29H3v-6h20V3h6Z"
CROSSING = "M23 3h6v6h-6Z"

# One-bit cut for the thermal label path, which has no greys at all: a solid
# ring with two slots knocked out along the edge of whichever strand passes in
# front at each crossing. Without the slots the mark prints as a plain square.
ONE_BIT = "M3 3h26v26H3Z M9 9h14v14H9Z M23 9h6v1.2h-6Z M9 23h1.2v6H9Z"

# The chop: the mark on a filled clay tile, for surfaces that need to be told
# apart from each other in a strip of browser tabs rather than told apart from
# other companies. It is a cut, not a second mark -- no path here is new.
#
# It has to use ONE_BIT rather than the two-strand cut. On a filled tile both
# strands would be the same paper colour, and the over-under -- the thing the
# CROSSING path exists to produce -- would simply disappear. The one-bit cut
# already solves exactly this problem for the label printer, so the chop
# borrows it and lets the tile colour show through the slots.
CHOP_RADIUS = 6

# The mark draws in a 32-unit box but only occupies units 3..29 of it, so the
# inset is computed on the 26 units actually inked. 0.62 of the tile leaves the
# corner radius clear of the strands at every size we rasterise.
CHOP_RATIO = 0.62
CHOP_SCALE = CHOP_RATIO * 32 / 26
CHOP_OFFSET = (32 - CHOP_RATIO * 32) / 2 - 3 * CHOP_SCALE

SVG_OPEN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{extra}>'


# Populated by every write(); --check compares this against the tree instead of
# touching it, which is what lets CI prove the committed output matches the
# generator without needing a clean-tree diff.
PENDING: dict[pathlib.Path, str] = {}


def emit(path: pathlib.Path, body: str) -> pathlib.Path:
    PENDING[path] = body
    return path


def write(name: str, body: str) -> pathlib.Path:
    return emit(LOGO / name, body.rstrip() + "\n")


def flush(check: bool) -> int:
    """Write everything queued, or report what does not match."""
    drifted = []
    for path, body in sorted(PENDING.items()):
        current = path.read_text() if path.exists() else None
        if current == body:
            continue
        if check:
            drifted.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)

    if drifted:
        print("generated files do not match the generator:", file=sys.stderr)
        for path in drifted:
            print(f"  {path.relative_to(ROOT)}", file=sys.stderr)
        print("\nRun `npm run build` and commit the result.", file=sys.stderr)
        return 1
    return 0


def mark(fill_a: str, fill_b: str, label: str) -> str:
    return (
        SVG_OPEN.format(vb="0 0 32 32", extra=f' role="img" aria-label="{label}"')
        + f'\n  <path d="{STRAND_A}" fill="{fill_a}"/>'
        + f'\n  <path d="{STRAND_B}" fill="{fill_b}"/>'
        + f'\n  <path d="{CROSSING}" fill="{fill_a}"/>'
        + "\n</svg>"
    )


def chop(tile: str, ink: str, label: str) -> str:
    t = (f'transform="translate({CHOP_OFFSET:.3f} {CHOP_OFFSET:.3f})'
         f' scale({CHOP_SCALE:.4f})"')
    return (
        SVG_OPEN.format(vb="0 0 32 32", extra=f' role="img" aria-label="{label}"')
        + f'\n  <rect width="32" height="32" rx="{CHOP_RADIUS}" fill="{tile}"/>'
        + f'\n  <path {t} fill-rule="evenodd" d="{ONE_BIT}" fill="{ink}"/>'
        + "\n</svg>"
    )


def outline_wordmark() -> str:
    """Return the wordmark path data, outlining it with inkscape."""
    if not shutil.which("inkscape"):
        sys.exit("inkscape not found; rerun with --skip-wordmark")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "in.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" '
            'viewBox="0 0 1200 300">'
            '<text x="0" y="200" font-family="Bitter SemiBold" font-weight="600" '
            'font-size="200" letter-spacing="-4" fill="#000">MakersBrain</text>'
            "</svg>"
        )
        subprocess.run(
            ["inkscape", "--export-text-to-path", "--export-plain-svg",
             "--export-area-drawing", "--export-type=svg",
             f"--export-filename={tmp / 'out.svg'}", str(tmp / "in.svg")],
            check=True, capture_output=True,
        )
        out = (tmp / "out.svg").read_text()

    d = re.search(r'<path\s[^>]*?d="([^"]+)"', out, re.S)
    box = re.search(r'viewBox="([^"]+)"', out)
    if not d or not box:
        sys.exit("could not find the outlined path in inkscape's output")
    return d.group(1), box.group(1)


def cached_wordmark() -> tuple[str, str]:
    src = (LOGO / "wordmark.svg").read_text()
    d = re.search(r'<path d="([^"]+)"', src)
    box = re.search(r'viewBox="([^"]+)"', src)
    if not d or not box:
        sys.exit("src/logo/wordmark.svg is missing or malformed")
    return d.group(1), box.group(1)


BANNER = (
    "// Generated by build/build-logo.py. Do not edit.\n"
    "//\n"
    "// The mark is defined once, as three path constants, and every cut in\n"
    "// src/logo/ is generated from them. Importing the paths rather than an SVG\n"
    "// file is what lets a component inherit `currentColor` and re-colour a\n"
    "// single strand, which no <img> can do.\n"
)

MARKS_DOC = """
/**
 * The weave: two strands crossing over and under.
 *
 * `crossing` is load-bearing rather than decorative. It puts strand A back on
 * top at the top-right, which is what makes this a weave and not two
 * overlapping brackets. Draw the three in the order they are declared.
 */"""

ONE_BIT_DOC = """
/**
 * The single-ink cut. A solid ring with a slot knocked out along the edge of
 * whichever strand passes in front at each crossing, `fill-rule: evenodd`.
 *
 * For any surface with no second colour to spend: a thermal label, or the chop,
 * where both strands would otherwise be the same paper tone and the over-under
 * would vanish.
 */"""

WORDMARK_DOC = """
/** Bitter SemiBold outlined to paths, so no surface has to ship the font. */"""


def marks_js(wd: str, wbox: str) -> str:
    return (
        BANNER
        + MARKS_DOC
        + "\nexport const WEAVE = Object.freeze({\n"
        f"\tstrandA: '{STRAND_A}',\n"
        f"\tstrandB: '{STRAND_B}',\n"
        f"\tcrossing: '{CROSSING}'\n"
        "});\n"
        + ONE_BIT_DOC
        + f"\nexport const ONE_BIT = '{ONE_BIT}';\n"
        + WORDMARK_DOC
        + "\nexport const WORDMARK = Object.freeze({\n"
        f"\tviewBox: '{wbox}',\n"
        f"\tpath: '{wd}'\n"
        "});\n"
        "\n/** The chop's tile geometry, so a consumer can reproduce it inline. */\n"
        "export const CHOP = Object.freeze({\n"
        f"\tradius: {CHOP_RADIUS},\n"
        f"\tscale: {CHOP_SCALE:.4f},\n"
        f"\toffset: {CHOP_OFFSET:.3f}\n"
        "});\n"
    )


def marks_dts() -> str:
    return (
        BANNER
        + "\nexport declare const WEAVE: Readonly<{\n"
        "\tstrandA: string;\n\tstrandB: string;\n\tcrossing: string;\n}>;\n"
        "\nexport declare const ONE_BIT: string;\n"
        "\nexport declare const WORDMARK: Readonly<{\n"
        "\tviewBox: string;\n\tpath: string;\n}>;\n"
        "\nexport declare const CHOP: Readonly<{\n"
        "\tradius: number;\n\tscale: number;\n\toffset: number;\n}>;\n"
    )


def main() -> int:
    check = "--check" in sys.argv
    LOGO.mkdir(parents=True, exist_ok=True)

    # ---- the mark, in every cut a surface actually needs ----
    write("weave.svg", mark("currentColor", CLAY, "MakersBrain"))
    write("weave-dark.svg", mark(PAPER, CLAY_DARK, "MakersBrain"))
    write("weave-mono.svg", mark("currentColor", "currentColor", "MakersBrain"))
    write(
        "weave-1bit.svg",
        SVG_OPEN.format(vb="0 0 32 32", extra=' role="img" aria-label="MakersBrain"')
        + f'\n  <path fill-rule="evenodd" d="{ONE_BIT}" fill="#000"/>\n</svg>',
    )
    write("favicon.svg", mark(INK, CLAY, "MakersBrain"))

    # The chop, and the catalogue tools' favicon cut from it. The catalogue
    # carries the ordinary weave in its header and this in its tab, which is
    # the one place the wordmark beside the mark is not legible enough to say
    # which MakersBrain surface a tab belongs to.
    write("chop.svg", chop(CLAY, PAPER, "MakersBrain"))
    write("chop-dark.svg", chop(CLAY_DARK, INK, "MakersBrain"))

    # ---- wordmark ----
    if "--skip-wordmark" in sys.argv:
        wd, wbox = cached_wordmark()
    else:
        wd, wbox = outline_wordmark()
    ww, wh = (float(v) for v in wbox.split()[2:4])
    write(
        "wordmark.svg",
        SVG_OPEN.format(vb=wbox, extra=' role="img" aria-label="MakersBrain"')
        + f'\n  <path d="{wd}" fill="currentColor"/>\n</svg>',
    )

    # ---- lockups ----
    # The mark sits at 1.46x the wordmark's ascender height and one 0.6em gap
    # away, which is the same optical relationship the HTML lockup produces.
    size = wh * 1.46
    gap = wh * 0.762
    scale = size / 32

    def placed_mark(x: float, y: float, fill_b: str) -> str:
        t = f'transform="translate({x:.1f} {y:.1f}) scale({scale:.4f})"'
        return (
            f'\n  <g {t}>'
            f'\n    <path d="{STRAND_A}" fill="currentColor"/>'
            f'\n    <path d="{STRAND_B}" fill="{fill_b}"/>'
            f'\n    <path d="{CROSSING}" fill="currentColor"/>'
            f'\n  </g>'
        )

    for suffix, clay in (("", CLAY), ("-dark", CLAY_DARK)):
        w = size + gap + ww
        write(
            f"lockup-horizontal{suffix}.svg",
            SVG_OPEN.format(
                vb=f"0 0 {w:.1f} {size:.1f}",
                extra=' role="img" aria-label="MakersBrain"',
            )
            + placed_mark(0, 0, clay)
            + f'\n  <path d="{wd}" fill="currentColor"'
            f' transform="translate({size + gap:.1f} {(size - wh) / 2:.1f})"/>'
            + "\n</svg>",
        )

        # Stacked, the mark carries the composition rather than sitting beside
        # the word, so it takes a larger share than in the horizontal lockup.
        stack_size = wh * 2.45
        stack_scale = stack_size / 32
        stack_gap = wh * 0.6
        h = stack_size + stack_gap + wh
        t = (f'transform="translate({(ww - stack_size) / 2:.1f} 0)'
             f' scale({stack_scale:.4f})"')
        write(
            f"lockup-stacked{suffix}.svg",
            SVG_OPEN.format(
                vb=f"0 0 {ww:.1f} {h:.1f}",
                extra=' role="img" aria-label="MakersBrain"',
            )
            + f'\n  <g {t}>'
            f'\n    <path d="{STRAND_A}" fill="currentColor"/>'
            f'\n    <path d="{STRAND_B}" fill="{clay}"/>'
            f'\n    <path d="{CROSSING}" fill="currentColor"/>'
            f'\n  </g>'
            + f'\n  <path d="{wd}" fill="currentColor"'
            f' transform="translate(0 {stack_size + stack_gap:.1f})"/>'
            + "\n</svg>",
        )

    # ---- the same definition, for anything that imports rather than links ----
    emit(SRC / "marks.js", marks_js(wd, wbox))
    emit(SRC / "marks.d.ts", marks_dts())

    status = flush(check)
    if status:
        return status
    if check:
        print("generated assets match the generator")
    else:
        print(f"wrote {len(PENDING)} files to src/")

    # The PNGs are compared by hand rather than by content: inkscape's output is
    # not byte-reproducible across versions, so a --check that diffed them would
    # fail on a machine whose inkscape differs by a patch release. The SVGs they
    # derive from are checked, which is where a real change would show up.
    if check or "--no-raster" in sys.argv:
        return 0
    rasterise()
    return 0


def rasterise() -> None:
    """Emit the PNGs that no SVG-only pipeline can supply.

    Favicons because some clients still refuse SVG, and the org avatar and OAuth
    logo because neither GitHub nor the Google Cloud console has an API for
    them: both are upload-only through a web UI, so this produces the file a
    human then drags into the form.
    """
    if not shutil.which("inkscape"):
        print("inkscape not found; skipping the PNG step", file=sys.stderr)
        return

    for stem, src in (("favicon", "favicon.svg"), ("chop", "chop.svg")):
        for size in (16, 32, 48, 180, 512):
            subprocess.run(
                ["inkscape", "--export-type=png",
                 f"--export-width={size}", f"--export-height={size}",
                 f"--export-filename={LOGO / f'{stem}-{size}.png'}",
                 str(LOGO / src)],
                check=True, capture_output=True,
            )

    # GitHub renders an org avatar as a rounded square and shows it as small as
    # 40px, so the mark is inset to about 56% of the canvas: enough that the
    # corner radius never clips a strand, and enough that the weave still reads
    # at list size. The ground is painted rather than left transparent, because
    # a transparent avatar inherits whatever GitHub sits it on.
    canvas, ratio = 1024, 0.56
    # weave.svg draws in a 32-unit box but only occupies units 3..29 of it.
    render = round(canvas * ratio * 32 / 26)
    with tempfile.TemporaryDirectory() as tmp:
        mark = pathlib.Path(tmp) / "mark.png"
        subprocess.run(
            ["inkscape", "--export-type=png",
             f"--export-width={render}", f"--export-height={render}",
             f"--export-filename={mark}", str(LOGO / "favicon.svg")],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["magick", "-size", f"{canvas}x{canvas}", f"xc:{PAPER_GROUND}",
             str(mark), "-gravity", "center", "-composite",
             str(LOGO / "avatar-1024.png")],
            check=True, capture_output=True,
        )

    # The OAuth consent screen. Google fixes the logo at 120x120 and masks it to
    # a circle, so this is the chop -- a filled tile survives a circle mask where
    # an open mark floats -- flattened onto the cream ground so the rounded
    # corners carry a colour rather than transparency, which some Google
    # surfaces render as black. The chop insets the mark to 62% of the tile,
    # which clears the inscribed circle at every point.
    with tempfile.TemporaryDirectory() as tmp:
        tile = pathlib.Path(tmp) / "tile.png"
        subprocess.run(
            ["inkscape", "--export-type=png",
             "--export-width=120", "--export-height=120",
             f"--export-filename={tile}", str(LOGO / "chop.svg")],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["magick", "-size", "120x120", f"xc:{PAPER_GROUND}",
             str(tile), "-gravity", "center", "-composite",
             "-alpha", "off", str(LOGO / "oauth-120.png")],
            check=True, capture_output=True,
        )

    print(f"wrote {len(list(LOGO.glob('*.png')))} png files to src/logo/")


if __name__ == "__main__":
    raise SystemExit(main())
