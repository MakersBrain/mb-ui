<script>
	/**
	 * "MakersBrain", as outlines rather than text.
	 *
	 * Bitter SemiBold, outlined by `build/build-logo.py`, so a surface renders the
	 * wordmark correctly without shipping the font. A wordmark set in live text
	 * silently falls back to whatever face is present, and a wordmark in the
	 * wrong face is a wordmark that says the wrong thing -- which is the one
	 * failure mode a brand asset must not have.
	 *
	 * Height rather than width is the prop, because a lockup aligns on the
	 * wordmark's cap height against the mark beside it.
	 */
	import { WORDMARK } from '../marks.js';

	let { height = '0.72rem', title = 'MakersBrain', ...rest } = $props();
</script>

<svg
	style:height
	viewBox={WORDMARK.viewBox}
	role="img"
	aria-label={title}
	focusable="false"
	{...rest}
>
	<title>{title}</title>
	<path d={WORDMARK.path} fill="currentColor" />
</svg>

<style>
	svg {
		display: block;
		width: auto;
		flex: none;
	}
</style>
