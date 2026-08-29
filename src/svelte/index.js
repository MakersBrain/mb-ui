/**
 * `@makersbrain/ui/svelte` -- the mark, rendered.
 *
 *     import { BrandLockup } from '@makersbrain/ui/svelte';
 *
 * Deep imports work too, and are what to reach for when a bundler should see
 * only the one component:
 *
 *     import BrandMark from '@makersbrain/ui/svelte/BrandMark.svelte';
 *
 * These ship as Svelte source, not compiled output. The consumer's own Svelte
 * compiles them, which is what keeps the package free of a build step and free
 * of an opinion about the consumer's Svelte version beyond the peer range.
 */
export { default as BrandMark } from './BrandMark.svelte';
export { default as BrandWordmark } from './BrandWordmark.svelte';
export { default as BrandLockup } from './BrandLockup.svelte';
