<script>
	/** What this page is, and the one or two things you can do to it. */
	let {
		title,
		eyebrow = undefined,
		description = undefined,
		class: className = '',
		actions,
		children,
		...rest
	} = $props();
</script>

<header class="mb-page-header {className}" {...rest}>
	<div>
		{#if eyebrow}<span class="mb-eyebrow">{eyebrow}</span>{/if}
		<h1 class="mb-page-title">{title}</h1>
		{#if description}<p class="mb-page-description">{description}</p>{/if}
		{@render children?.()}
	</div>
	{#if actions}<div class="mb-actions">{@render actions()}</div>{/if}
</header>
