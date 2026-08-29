<script>
	/**
	 * A number, what it is, and what would make someone act on it.
	 *
	 * Summary before detail, and never the number alone: a tile that says "3"
	 * and nothing else makes the reader open another page to find out whether 3
	 * is bad. The value is the display face with tabular figures -- display
	 * because it is the thing being read, tabular because a row of these should
	 * have its digits in columns and must not reflow as a live counter ticks.
	 *
	 * `tone` is applied to the value only, so the label and the detail stay
	 * readable when a figure turns red.
	 */
	let {
		label,
		value = undefined,
		detail = undefined,
		tone = undefined,
		href = undefined,
		class: className = '',
		children,
		...rest
	} = $props();
</script>

<div class="mb-metric {className}" {...rest}>
	<span class="mb-metric-label">{label}</span>
	{#if children}
		{@render children()}
	{:else}
		<span class="mb-metric-value {tone ?? ''}">{value}</span>
	{/if}
	{#if detail}
		{#if href}
			<a class="mb-metric-detail" {href}>{detail}</a>
		{:else}
			<span class="mb-metric-detail">{detail}</span>
		{/if}
	{/if}
</div>
