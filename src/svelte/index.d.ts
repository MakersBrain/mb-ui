import type { Component, Snippet } from 'svelte';
import type { HTMLAttributes, SVGAttributes } from 'svelte/elements';

export interface BrandMarkProps extends Omit<SVGAttributes<SVGSVGElement>, 'title'> {
	/** Any CSS length. Defaults to `1.35em`, so the mark scales with its label. */
	size?: string;
	/** Drop the clay strand and take `currentColor` for the whole mark. */
	mono?: boolean;
	/** Accessible name. Omitted, the mark is decorative and hidden from readers. */
	title?: string;
}

export interface BrandWordmarkProps extends Omit<SVGAttributes<SVGSVGElement>, 'title'> {
	/** Any CSS length; width follows the aspect ratio. */
	height?: string;
	title?: string;
}

export interface BrandLockupProps extends HTMLAttributes<HTMLElement> {
	/** The surface's name, e.g. `Catalogue`. Hidden on narrow viewports. */
	product?: string;
	size?: string;
	wordmarkHeight?: string;
	mono?: boolean;
	/** Renders an anchor instead of a span. */
	href?: string;
}

export declare const BrandMark: Component<BrandMarkProps>;
export declare const BrandWordmark: Component<BrandWordmarkProps>;
export declare const BrandLockup: Component<BrandLockupProps>;

/** A status colour. Never the only carrier of the meaning; pair it with a word. */
export type Tone = 'good' | 'warn' | 'bad' | 'info' | 'busy' | 'neutral';

export interface MetricProps extends HTMLAttributes<HTMLDivElement> {
	label: string;
	value?: string | number;
	/** What would make someone act on the number. */
	detail?: string;
	/** Applied to the value only, so the label and detail stay readable. */
	tone?: 'good' | 'warn' | 'bad' | 'quiet';
	/** Turns the detail into a link to wherever the number is explained. */
	href?: string;
	/** Replaces the value, for a figure that needs its own markup. */
	children?: Snippet;
}

export interface StatusBadgeProps extends HTMLAttributes<HTMLSpanElement> {
	tone?: Tone;
	/** The dot is on by default: colour must not carry the meaning alone. */
	dot?: boolean;
	children?: Snippet;
}

export interface PanelProps extends HTMLAttributes<HTMLElement> {
	title?: string;
	subtitle?: string;
	/** The caveat a reader needs before believing the panel. */
	note?: string;
	/** The heading level the title takes in the document outline. */
	level?: 'h2' | 'h3' | 'h4';
	actions?: Snippet;
	children?: Snippet;
}

export interface PageHeaderProps extends HTMLAttributes<HTMLElement> {
	title: string;
	eyebrow?: string;
	description?: string;
	/** Where the page above this one is. Rendered as a quiet link over the title. */
	backHref?: string;
	backLabel?: string;
	actions?: Snippet;
	children?: Snippet;
}

export interface SectionHeaderProps extends HTMLAttributes<HTMLDivElement> {
	title: string;
	description?: string;
	level?: 'h2' | 'h3' | 'h4';
	actions?: Snippet;
}

export interface DataListItem {
	term: string;
	value: string | number;
	/** A tooltip for the value, e.g. how exact a measured figure is. */
	title?: string;
}

export interface DataListProps extends HTMLAttributes<HTMLDListElement> {
	items?: DataListItem[];
	children?: Snippet;
}

export interface TableWrapProps extends HTMLAttributes<HTMLDivElement> {
	children?: Snippet;
}

export interface EmptyStateProps extends HTMLAttributes<HTMLDivElement> {
	title?: string;
	children?: Snippet;
}

export interface NoticeProps extends HTMLAttributes<HTMLDivElement> {
	tone?: 'good' | 'warn' | 'bad' | 'info';
	children?: Snippet;
}

export interface TabItem {
	href: string;
	label: string;
	/** What a narrow viewport gets instead of the label. */
	short?: string;
	/** Match the href exactly rather than as a path prefix. */
	exact?: boolean;
}

export interface TabsProps extends Omit<HTMLAttributes<HTMLElement>, 'children'> {
	items?: TabItem[];
	/** The current pathname. */
	current?: string;
	/** The nav's accessible name, e.g. "Operations sections". */
	label?: string;
	/** Rendered inside each tab, for a count beside its label. */
	badge?: Snippet<[TabItem]>;
}

export declare const Metric: Component<MetricProps>;
export declare const StatusBadge: Component<StatusBadgeProps>;
export declare const Panel: Component<PanelProps>;
export declare const PageHeader: Component<PageHeaderProps>;
export declare const SectionHeader: Component<SectionHeaderProps>;
export declare const DataList: Component<DataListProps>;
export declare const TableWrap: Component<TableWrapProps>;
export declare const EmptyState: Component<EmptyStateProps>;
export declare const Notice: Component<NoticeProps>;
export declare const Tabs: Component<TabsProps>;
