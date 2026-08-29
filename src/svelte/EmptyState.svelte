<script>
	/**
	 * Nothing here, and what would put something here.
	 *
	 * An empty table is ambiguous -- broken, or genuinely empty? -- so the state
	 * says which, and says what action fills it.
	 */
	let { title = undefined, class: className = '', children, ...rest } = $props();
</script>

<div class="mb-empty {className}" {...rest}>
	{#if title}<strong class="mb-empty-title">{title}</strong>{/if}
	{@render children?.()}
</div>
