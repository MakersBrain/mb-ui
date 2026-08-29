<script>
	/**
	 * A titled region of a page: a hairline above, a title, the content.
	 *
	 * The unit of a page is a panel rather than a card. A page carrying nine
	 * bordered cards reads as nine objects the reader has to sort; the same nine
	 * as ruled panels read as one page with nine parts, which is what they are.
	 * Cards are kept for the things that genuinely are objects -- one worker,
	 * one run -- where the border is saying "this is a thing", not "this is a
	 * section".
	 */
	let {
		title = undefined,
		subtitle = undefined,
		note = undefined,
		level = 'h2',
		class: className = '',
		actions,
		children,
		...rest
	} = $props();
</script>

<section class="mb-panel {className}" {...rest}>
	{#if title || actions}
		<div class="mb-panel-head">
			<div>
				<svelte:element this={level} class="mb-panel-title">{title}</svelte:element>
				{#if subtitle}<p class="mb-panel-subtitle">{subtitle}</p>{/if}
			</div>
			{#if actions}<div class="mb-actions">{@render actions()}</div>{/if}
		</div>
	{/if}
	{@render children?.()}
	{#if note}<p class="mb-panel-note">{note}</p>{/if}
</section>
