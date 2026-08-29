<script>
	/**
	 * A table that scrolls sideways inside its own box.
	 *
	 * Wide content must never make the page scroll horizontally: on a phone that
	 * moves the whole interface, including the header, off to the left.
	 */
	let { class: className = '', children, ...rest } = $props();
</script>

<div class="mb-table-wrap {className}" {...rest}>{@render children?.()}</div>
