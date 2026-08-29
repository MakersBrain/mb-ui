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
 *
 * The mark carries its own colours and needs only `tokens.css`. Everything
 * below the mark is styled by `@makersbrain/ui/patterns.css`, which a surface
 * on `ui.css` already has -- and which a surface on Tailwind or shadcn can
 * import on its own, because nothing in it selects an element.
 */
export { default as BrandMark } from './BrandMark.svelte';
export { default as BrandWordmark } from './BrandWordmark.svelte';
export { default as BrandLockup } from './BrandLockup.svelte';
export { default as Metric } from './Metric.svelte';
export { default as StatusBadge } from './StatusBadge.svelte';
export { default as Panel } from './Panel.svelte';
export { default as PageHeader } from './PageHeader.svelte';
export { default as SectionHeader } from './SectionHeader.svelte';
export { default as DataList } from './DataList.svelte';
export { default as TableWrap } from './TableWrap.svelte';
export { default as EmptyState } from './EmptyState.svelte';
export { default as Notice } from './Notice.svelte';
export { default as Tabs } from './Tabs.svelte';
