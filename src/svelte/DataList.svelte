<script>
	/**
	 * Terms on the left, figures right-aligned on the right.
	 *
	 * Right-aligned and tabular because the point of a column of numbers is that
	 * a reader can compare them without reading them, which a ragged left edge
	 * takes away. Pass `items`, or the `dt`/`dd` pairs as children when a value
	 * needs its own markup.
	 */
	let { items = [], class: className = '', children, ...rest } = $props();
</script>

<dl class="mb-datalist {className}" {...rest}>
	{#each items as item (item.term)}
		<dt>{item.term}</dt>
		<dd title={item.title}>{item.value}</dd>
	{/each}
	{@render children?.()}
</dl>
