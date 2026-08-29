<script>
	/**
	 * A state, as a dot and a word.
	 *
	 * The dot is not decoration: colour never carries meaning alone here, and a
	 * reader who cannot separate the green from the red still has the word. It
	 * is hidden from assistive technology for the same reason -- the word is
	 * already the accessible content.
	 */
	let { tone = 'neutral', dot = true, class: className = '', children, ...rest } = $props();
</script>

<span class="mb-badge {tone} {className}" {...rest}>
	{#if dot}<span class="mb-dot" aria-hidden="true"></span>{/if}{@render children?.()}
</span>
