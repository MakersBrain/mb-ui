import type { Component } from 'svelte';
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
