<script>
	/** A short statement about the page's state, banded by a rule down its side. */
	let { tone = 'info', class: className = '', children, ...rest } = $props();
</script>

<div class="mb-notice {tone} {className}" role={tone === 'bad' ? 'alert' : undefined} {...rest}>
	{@render children?.()}
</div>
