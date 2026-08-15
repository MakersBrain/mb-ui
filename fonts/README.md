# Fonts

woff2 subsets embedded into `../style-guide.html` by `../build-style-guide.py`.

Both families are SIL Open Font License 1.1, so redistributing them inside a
built page is fine. Keep this notice with them.

| File | Family | Axes / weights | Subset |
| --- | --- | --- | --- |
| `bitter-latin.woff2` | Bitter | variable, 400–700 | latin |
| `bitter-latinext.woff2` | Bitter | variable, 400–700 | latin-ext |
| `plex-latin.woff2` | IBM Plex Sans | variable | latin |
| `plex-latinext.woff2` | IBM Plex Sans | variable | latin-ext |

The latin-ext subsets are not optional. French copy needs `œ Œ` and the
combining marks that live outside the latin range; on a latin-only subset the
browser falls back mid-word and the line changes face partway through.

## Refreshing them

Google Fonts serves the subsets above from the `css2` endpoint. Fetch the
stylesheet with a browser user-agent (otherwise it returns TTF), then pull the
`latin` and `latin-ext` URLs out of it:

```sh
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Bitter:wght@400..700"
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600"
```

If the `unicode-range` values in the returned CSS have changed, update the
`LATIN` and `LATIN_EXT` constants in `../build-style-guide.py` to match.

JetBrains Mono is referenced by `--mb-font-mono` but is not embedded: the mono
role is a handful of identifiers, not running text, and a system mono stack is
an acceptable fallback there. Self-host it when the real product surfaces ship.
