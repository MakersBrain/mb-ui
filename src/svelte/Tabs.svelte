<script>
	/**
	 * One level of navigation: which view of this thing.
	 *
	 * The active tab is named by an underline and a weight rather than a filled
	 * pill. A row of pills reads as a row of buttons, and then the one control
	 * on the page that really is a button has nothing left to distinguish it.
	 *
	 * Each item is `{ href, label, short?, badge? }`. `short` is what a narrow
	 * viewport gets, so the strip shortens before it scrolls and scrolls before
	 * it wraps -- a wrap costs three lines of a phone viewport that has twelve,
	 * and what it pushes off the screen is the thing the reader came for.
	 */
	let { items = [], current = '', label = undefined, class: className = '', badge, ...rest } =
		$props();

	/** @param {{ href: string, exact?: boolean }} item */
	const active = (item) =>
		item.exact ? current === item.href : current === item.href || current.startsWith(`${item.href}/`);
</script>

<nav class="mb-tabs {className}" aria-label={label} {...rest}>
	{#each items as item (item.href)}
		<a class="mb-tab" href={item.href} aria-current={active(item) ? 'page' : undefined}>
			{#if item.short}
				<span class="mb-tab-long">{item.label}</span>
				<span class="mb-tab-short">{item.short}</span>
			{:else}
				{item.label}
			{/if}
			{#if badge}{@render badge(item)}{/if}
		</a>
	{/each}
</nav>
