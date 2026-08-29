# @makersbrain/ui

The MakersBrain visual identity, as one installable package: the colour and type
tokens, the component layer built on them, the weave mark in every cut a surface
needs, and the Svelte components that render it.

Direction: **warm craft-modern**, aimed at artisans broadly rather than ceramics
alone, in the plainspoken register of Basecamp rather than the precision-tooling
register of Linear.

This replaces the copy-and-check arrangement the brand used to live under, where
`brand/` sat inside one product's repository and every other surface received a
generated copy of it. That worked while there was one consumer. It stops working
at three, because "the source of truth" and "the thing your app imports" were
different files, and only a `make` target kept them the same.

## Install

The package is published to **GitHub Packages**, not npmjs.com, so npm has to be
told where the scope lives. Copy [`.npmrc.example`](.npmrc.example) into the
consuming repository:

```ini
@makersbrain:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

A token with `read:packages` is enough. Then:

```sh
npm install @makersbrain/ui
```

## Use

There is **no build step**. Everything in `src/` is committed and consumed
directly -- CSS as CSS, SVG as SVG, components as Svelte source that the
consumer's own compiler handles. Nothing here has to be built before it can be
imported, and nothing here has an opinion about your bundler.

### Foundations and components

```css
@import '@makersbrain/ui/tokens.css';
@import '@makersbrain/ui/fonts.css'; /* optional self-hosted faces */
@import '@makersbrain/ui/base.css';  /* reset, type, focus, motion */
@import '@makersbrain/ui/ui.css';    /* optional primitives; composes base.css */
```

`tokens.css` is the whole system -- colour, type, spacing, radius, elevation --
and `ui.css` is the domain-neutral component layer built on it. Take the first
without the second if the surface has its own components; never take the second
without the first, which is a stylesheet of `var()` calls resolving to nothing.
Product workflows and layouts stay in their product repository.

Framework bridges are explicit and optional:

```css
@import '@makersbrain/ui/adapters/shadcn.css';
```

The generated `@makersbrain/ui/adapters/odoo.scss` is the exact SCSS projection
used to keep Odoo's compile-time variables aligned with the CSS tokens.

### The mark

```svelte
<script>
  import { BrandLockup } from '@makersbrain/ui/svelte';
</script>

<BrandLockup product="Catalogue" href="/" />
```

`BrandMark`, `BrandWordmark` and `BrandLockup` are the three. The mark inherits
`currentColor` for its ink strand and reads `--mb-brand` for its clay one, which
is why it needs no dark-mode variant: import `tokens.css` and it adapts.

For anything that is not Svelte, the paths themselves are exported:

```js
import { WEAVE, ONE_BIT, WORDMARK } from '@makersbrain/ui';
```

And the flat assets are addressable:

```js
import favicon from '@makersbrain/ui/logo/chop.svg';
```

## The mark

**The weave**: two strands crossing over and under. It is a half-lap joint to a
woodworker, a warp and weft to a weaver, and a coil to a basket maker -- one
geometry that does not pick a craft, and the only candidate that also says
something about the software: two things fitting together.

| File | Use |
| --- | --- |
| `weave.svg` | Default. `currentColor` plus clay-500, for light grounds. |
| `weave-dark.svg` | Dark grounds. The accent steps up to clay-400 to survive there. |
| `weave-mono.svg` | Single colour, inherits `currentColor` entirely. |
| `weave-1bit.svg` | Thermal labels. Pure black with slots knocked out at the crossings. |
| `chop.svg` / `-dark` | The mark on a filled tile. Tabs and app icons only -- see below. |
| `wordmark.svg` | Bitter SemiBold outlined to paths -- needs no font. |
| `lockup-horizontal.svg` / `-dark` | Navigation, email, documents. |
| `lockup-stacked.svg` / `-dark` | Square placements, print, packaging. |
| `favicon.svg`, `favicon-{16,32,48,180,512}.png` | Browser and home screen. |
| `chop-{16,32,48,180,512}.png` | The catalogue tools' favicon. |
| `avatar-1024.png` | GitHub org avatar, and any other square profile slot. |
| `oauth-120.png` | Google OAuth consent screen. 120x120, opaque. |

All of it regenerates from three path constants in
[`build/build-logo.py`](build/build-logo.py):

```python
STRAND_A = "M3 3h26v6H9v20H3Z"    # top bar + left stem
STRAND_B = "M29 29H3v-6h20V3h6Z"  # bottom bar + right stem
CROSSING = "M23 3h6v6h-6Z"        # A back on top, top-right
```

`CROSSING` is load-bearing. It puts strand A back on top at the top-right, which
is what makes this a weave rather than two overlapping brackets. A derivation
that loses the over-under has stopped being the mark.

The one-bit cut matters more than it looks. The Phomemo label path has no greys
at all, so both strands print solid black and the mark collapses into a plain
square ring. `weave-1bit.svg` knocks a slot out along the edge of whichever
strand passes in front at each crossing, which is what keeps the over-under
readable with one ink.

The chop is a **cut, not a second mark** -- no path in it is new. It exists for
one problem the ordinary weave cannot solve: a browser tab is the only place the
wordmark beside the mark is illegible, so with several MakersBrain surfaces open
every tab carries the identical favicon. A filled tile is picked out of a strip
of tabs at a glance where an open mark is not. A surface carries the ordinary
weave in its header and the chop in its tab. It reuses `ONE_BIT` and has to: on
a filled tile both strands would be the same paper colour and the over-under
would vanish, which is the same failure the label printer produces and the same
fix. Below about 24 px the slots close and it reads as a plain ring; that is
accepted, because at tab size the tile is doing the identifying.

`avatar-1024.png` is inset to 56% of its canvas and painted on the cream ground
rather than left transparent. GitHub masks org avatars to a rounded square and
shows them as small as 40 px: the inset keeps the corner radius off the strands,
and the painted ground stops the mark inheriting whatever sits behind it. It has
to be uploaded by hand -- GitHub has no API for organization avatars, so this is
upload-only at `https://github.com/organizations/MakersBrain/settings/profile`.

`oauth-120.png` is the chop flattened onto the cream ground. Google fixes the
consent-screen logo at 120x120 and masks it to a circle, so it is the filled
tile rather than the open mark, and it carries no alpha channel -- some Google
surfaces render a transparent corner as black. It is uploaded by hand under
APIs & Services -> OAuth consent screen -> Branding in the Google Cloud console.

## Two rules that are easy to get wrong

- **Never declare a colour whose only definition sits inside a media query or a
  `[data-theme]` block.** Define it on the bare `:root` first. Otherwise the
  default "system" setting -- which stamps no attribute at all -- renders one
  theme's text on the other theme's ground.
- **`--mb-brand` and `--mb-accent` are not the same colour and not
  interchangeable.** Brand (clay-500) is for marks and decoration; white text on
  it lands at 4.25:1 and fails AA. Accent (clay-600) is for anything
  interactive, and clears AA at 5.88:1.

Every pairing in `tokens.css` is measured, and the numbers are in the style
guide's colour table. Two values were moved off the natural ramp to clear 4.5:1
as text: warning is kiln-700 darkened to `#96600D`, and subtle text is `#7A6A5D`
rather than sand-500.

## Typefaces

- **Bitter** (SIL OFL) -- display and headings. A screen-native slab: workshop
  signage rather than boutique editorial.
- **IBM Plex Sans** (SIL OFL) -- interface and body. Chosen over Inter for its
  numerals and its Latin-ext coverage, which French micro-entreprise paperwork
  actually exercises.
- **JetBrains Mono** (SIL OFL) -- lot codes, SKUs, SIRET numbers, QR payloads.
  Anything a person reads back aloud or types into a label printer.

All three are OFL, so self-hosting is fine. Serve the `latin` and `latin-ext`
subsets both; a French interface on a latin-only subset falls back mid-word.

The `latin` and `latin-ext` woff2 subsets of Bitter and IBM Plex Sans ship with
the package, at `@makersbrain/ui/fonts/*.woff2`. An app is free to deliver
them through fontsource or its own pipeline instead -- but a page that inlines
its fonts to stay self-contained (the landing page, the two reference pages
below) needs the bytes from somewhere, and sourcing them per-consumer is how two
surfaces end up on different cuts of the same family.

The wordmark needs no font at any point, because it is outlined.

## Working on it

```sh
npm install
npm run build          # regenerate the logo set and the reference pages
npm run check          # what CI runs
```

`build/build-logo.py` writes every asset and `src/marks.js`. It takes
`--skip-wordmark` to reuse the cached outlined wordmark instead of re-running
inkscape, `--no-raster` to skip the PNGs, and `--check` to compare against the
tree instead of writing -- which is the form CI uses to prove the committed
output still matches the generator.

The two reference pages are built artefacts, self-contained in one file each:

- `pages/style-guide.html` -- the decision record: the five candidate marks, the
  palette, the type pairing.
- `pages/design-chart.html` -- how the product is built: layout, navigation,
  density, components, states, motion, accessibility, writing.

They are not pictures of the components. `build/build-pages.py` inlines the real
`src/tokens.css` and `src/ui.css`, so a drift between the chart and the package
is not possible without the chart visibly breaking. Edit the `.src.html` files,
never the built ones.

## Releasing

Publishing is triggered by a tag, so a release is a deliberate act with a name
rather than a side effect of merging:

```sh
npm version minor --tag-version-prefix=ui-v
git push --follow-tags
```

`.github/workflows/publish.yml` re-runs every CI gate, refuses to publish if the
`ui-v*` tag does not match the version in `package.json`, and publishes with the
workflow's own `GITHUB_TOKEN` -- no long-lived npm credential exists anywhere.
The same workflow can be dispatched manually with `dry_run` to pack and validate
without publishing.

To move to npmjs.com instead, change `registry-url` in the workflow and
`publishConfig.registry` in `package.json`, and supply an `NPM_TOKEN` secret.

## License and brand use

MakersBrain-authored code, styles, components, scripts, documentation, and
visual assets are AGPL-3.0-only. Trademark rights are not granted, and bundled
fonts retain their upstream OFL terms. See [LICENSE.md](LICENSE.md) for the exact
boundary.
