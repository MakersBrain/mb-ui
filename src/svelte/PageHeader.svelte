<script>
	/**
	 * What this page is, and the one or two things you can do to it.
	 *
	 * The heading carries `data-page-identity` and a negative tabindex: a route
	 * has exactly one answer to what it is, and something has to be focusable
	 * after a client-side navigation or a screen reader is left where the last
	 * page put it.
	 */
	let {
		title,
		eyebrow = undefined,
		description = undefined,
		backHref = undefined,
		backLabel = undefined,
		class: className = '',
		actions,
		children,
		...rest
	} = $props();
</script>

<header class="mb-page-header {className}" {...rest}>
	<div class="mb-page-identity">
		{#if backHref}
			<a class="mb-page-back" href={backHref}>{backLabel ?? 'Back'}</a>
		{/if}
		{#if eyebrow}<span class="mb-eyebrow">{eyebrow}</span>{/if}
		<h1 class="mb-page-title" tabindex="-1" data-page-identity>{title}</h1>
		{#if description}<p class="mb-page-description">{description}</p>{/if}
		{@render children?.()}
	</div>
	{#if actions}<div class="mb-actions">{@render actions()}</div>{/if}
</header>
