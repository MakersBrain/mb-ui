<script>
	/**
	 * The label above a group of panels or a table.
	 *
	 * An eyebrow rather than a heading size: the page has one title, and a
	 * second thing set at heading size argues with it. Marked up as a real
	 * heading all the same, so the document outline is honest.
	 */
	let { title, description = undefined, level = 'h2', class: className = '', actions, ...rest } =
		$props();
</script>

<div class="mb-panel-head {className}" {...rest}>
	<div>
		<svelte:element this={level} class="mb-eyebrow">{title}</svelte:element>
		{#if description}<p class="mb-panel-subtitle">{description}</p>{/if}
	</div>
	{#if actions}<div class="mb-actions">{@render actions()}</div>{/if}
</div>
