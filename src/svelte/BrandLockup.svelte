<script>
	/**
	 * The mark, the wordmark, and optionally the name of one surface.
	 *
	 * The company is identified by the mark and the wordmark; a surface is
	 * identified by the word beside them. That division is the reason no
	 * MakersBrain surface needs a mark of its own -- the catalogue tools, the
	 * workshop app and the console are one company seen from three places, and a
	 * second mark would say they were three companies.
	 *
	 * `product` is dropped below `compact`, where the words would cost more than
	 * they earn; the mark and wordmark carry it alone.
	 */
	import BrandMark from './BrandMark.svelte';
	import BrandWordmark from './BrandWordmark.svelte';

	let {
		product = undefined,
		size = '1.25rem',
		wordmarkHeight = '0.72rem',
		mono = false,
		href = undefined,
		...rest
	} = $props();

	const label = $derived(product ? `MakersBrain ${product}` : 'MakersBrain');
</script>

<svelte:element
	this={href ? 'a' : 'span'}
	class="mb-lockup"
	{href}
	title={label}
	{...rest}
>
	<BrandMark {size} {mono} />
	<BrandWordmark height={wordmarkHeight} />
	{#if product}
		<span class="mb-lockup-product">{product}</span>
	{/if}
</svelte:element>

<style>
	.mb-lockup {
		display: flex;
		flex: none;
		align-items: center;
		gap: 0.5rem;
		color: inherit;
		text-decoration: none;
	}

	/* The product word is the one part set in live text rather than outlines:
	   it is not a brand asset, it is the name of a surface, and it should look
	   like the interface it sits in. */
	.mb-lockup-product {
		font-family: var(--mb-font-ui, inherit);
		font-size: var(--mb-text-body, 0.9375rem);
		color: var(--mb-text-muted, inherit);
		white-space: nowrap;
	}

	@media (max-width: 40rem) {
		.mb-lockup-product {
			display: none;
		}
	}
</style>
