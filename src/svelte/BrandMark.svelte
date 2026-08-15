<script>
	/**
	 * The weave, inline.
	 *
	 * Inline rather than an `<img>` because the mark is two-tone and only one of
	 * the tones is fixed: the strands take `currentColor` so the mark inherits
	 * whatever text colour surrounds it, and only the clay strand is stated. That
	 * is what lets one component sit in a light topbar, on a dark ground, and in
	 * a single-colour context without three separate assets -- an `<img>` would
	 * need one file per context.
	 *
	 * `--mb-brand` comes from `@makersbrain/brand/tokens.css`, which re-points it
	 * to clay-400 on a dark ground. Import that stylesheet, or set the property
	 * yourself, or pass `mono` to opt out of the second colour entirely.
	 */
	import { WEAVE } from '../marks.js';

	let {
		size = '1.35em',
		mono = false,
		title = undefined,
		...rest
	} = $props();

	const strand = $derived(mono ? 'currentColor' : 'var(--mb-brand, #C05F3D)');
</script>

<svg
	style:width={size}
	style:height={size}
	viewBox="0 0 32 32"
	role={title ? 'img' : 'presentation'}
	aria-label={title}
	aria-hidden={title ? undefined : 'true'}
	focusable="false"
	{...rest}
>
	{#if title}<title>{title}</title>{/if}
	<path d={WEAVE.strandA} fill="currentColor" />
	<path d={WEAVE.strandB} fill={strand} />
	<path d={WEAVE.crossing} fill="currentColor" />
</svg>

<style>
	svg {
		display: block;
		flex: none;
	}
</style>
