# MakersBrain design-system consolidation plan

Status: in progress
Last updated: 2026-08-29

## Execution record

Completed on 2026-08-29:

- renamed the repository to public `MakersBrain/mb-ui` and the package to
  public `@makersbrain/ui`;
- replaced `@makersbrain/ui@0.1.0` under `AGPL-3.0-only`, verified its package
  checks and tarball, and granted workflow read access to every current
  consumer;
- created public `MakersBrain/mb-site`, built the SvelteKit static homepage,
  Privacy Policy, and Terms, and deployed them through Cloudflare Pages at
  `https://makersbrain.app/`;
- migrated the control plane, catalogue, and Odoo repositories to
  `@makersbrain/ui`;
- generated and drift-checked the Odoo SCSS projection from the shared tokens;
- removed the old Odoo-owned landing build after the canonical site became
  live; and
- adopted `AGPL-3.0-only` for current MakersBrain-authored work across the
  organization, while retaining mandatory upstream licenses for third-party
  dependencies and bundled fonts.

Still open:

- confirm the public contact mailbox, legal-controller identity, retention
  language, and legal review before submitting Google OAuth verification;
- finish classifying product-specific selectors and promoting only primitives
  proven in two consumers;
- add the compatibility fixture and complete the documented visual,
  accessibility, and rollback rehearsals; and
- deprecate `@makersbrain/brand` if registry permissions are later granted.

## Decision

Rename the GitHub repository from `MakersBrain/brand` to
`MakersBrain/mb-ui` and rename the published package from
`@makersbrain/brand` to `@makersbrain/ui`.

Create the public website in a separate `MakersBrain/mb-site` repository. The
site consumes `@makersbrain/ui`; it does not own or copy the design system.

The names describe different boundaries:

- `mb-ui` owns the implemented visual identity and cross-product UI system;
- `mb-site` owns public content, legal pages, static-site routing, and
  Cloudflare Pages deployment;
- product repositories own product workflows, domain components, and
  product-specific layout.

`mb-ui` is preferred to `mb-design`: this repository ships implemented tokens,
styles, assets, and components, while “design” would suggest design source
material or documentation without defining a runtime package boundary. Brand
assets remain part of the UI package because every product surface consumes
them with the same tokens and components.

This is intentionally a breaking package rename while the consumer set is
small. Publish `@makersbrain/ui` as a new package and migrate every known
consumer deliberately; do not silently republish different contents under the
old name.

## Why now

The package is already consumed by the control plane, catalogue explorer, Odoo
brand checks, and landing-page builder. It has the correct shared foundations:
tokens, fonts, marks, flat assets, reference pages, and Svelte brand components.
The next consumers should not introduce a second system while the dependency
surface is still small enough to regularize deliberately.

The current boundary is not yet clean. `src/ui.css` contains both reusable UI
rules and product nouns such as workshops, services, members, invitations,
recovery, provisioning, and operations. Conversely, consumers still define
repeated presentation locally, including status badges, progress bars, page
headers, font declarations, lockups, and theme adapters. Consolidation means
moving each rule to its correct owner, not moving every rule into one package.

## Target package contract

`@makersbrain/ui` will expose four stable layers:

1. **Identity** — logo geometry, wordmark, lockups, favicons, OAuth artwork, and
   documented usage constraints.
2. **Foundations** — semantic colour, typography, spacing, radius, elevation,
   motion, breakpoints, and theme behavior.
3. **Primitives** — accessible, domain-neutral CSS and Svelte components whose
   semantics recur across at least two MakersBrain surfaces.
4. **Adapters** — narrowly scoped mappings for frameworks used by a consumer,
   such as shadcn/Tailwind or Odoo SCSS, generated from the same foundations.

The package will not contain workshop, catalogue, ceramics, tenant, recovery,
operator, invoice, or other product-domain behavior. It will not become a
general application framework, own routing, fetch data, or require a specific
deployment platform.

Proposed public exports, preserving equivalent paths under the new package:

```text
@makersbrain/ui/tokens.css
@makersbrain/ui/fonts.css
@makersbrain/ui/base.css
@makersbrain/ui/ui.css                 compatibility composition
@makersbrain/ui/svelte
@makersbrain/ui/adapters/shadcn.css
@makersbrain/ui/logo/*
@makersbrain/ui/fonts/*
```

The exact adapter name is confirmed only after comparing the control-plane and
catalogue implementations. Adapters remain optional; foundational tokens must
not depend on Tailwind or shadcn.

## Component admission rule

A component moves into `mb-ui` only when all of the following are true:

- it is used, or immediately needed, by at least two surfaces;
- its API can be expressed without product-domain types;
- accessibility behavior is part of its contract;
- visual variants are semantic rather than consumer-specific;
- consumers can extend it without selector-specificity workarounds; and
- the package can test it without importing application code.

One-off product components stay local even when they use shared tokens. A local
component can be promoted later after a second real use proves the abstraction.

Initial evaluation candidates are:

- `BrandMark`, `BrandWordmark`, and `BrandLockup` — already shared;
- `StatusBadge` with neutral semantic tones and caller-provided labels, if a
  second surface needs the same semantics;
- `ProgressBar` with bounded values and complete ARIA state, retained in the
  control plane unless a genuine second use appears;
- notice/callout presentation;
- page header, section header, tabs, stack, row, and action layout primitives;
- buttons and form controls where native-element behavior is sufficient; and
- a shared font declaration and three-state theme contract.

Initial non-candidates are `OperationCard`, workshop and platform navigation,
member/recovery rows, catalogue charts, data-series colours, and Odoo-specific
views.

## Work plan

### Phase 0 — Record the baseline

- Finish or deliberately shelve the existing uncommitted changes in
  the current repository; do not mix them into mechanical rename work.
- Run the package checks and each consumer's existing frontend checks.
- Capture desktop, narrow, light, and dark renders of the style guide, design
  chart, control-plane shell, and catalogue shell.
- Record the currently installed `@makersbrain/brand` version in every
  consumer. This is the rollback baseline.

Exit criteria: all existing checks pass and the visual baseline is retained as
review evidence.

### Phase 1 — Rename the repository only

- Rename `MakersBrain/brand` to `MakersBrain/mb-ui` in GitHub.
- Update the local `origin` URL to
  `https://github.com/MakersBrain/mb-ui.git`, then rename the local checkout
  directory from `mb-brand` to `mb-ui` when no process depends on its path.
- Update `repository`, `homepage`, and `bugs` in `package.json`.
- Update repository references and workflow comments, but leave package names,
  consumer manifests, imports, and lockfiles unchanged in this phase.
- Confirm existing `@makersbrain/brand` installs and package-release history
  remain reachable after the GitHub rename.

Exit criteria: the new repository URL is canonical, the old GitHub redirect
works, existing consumers still install unchanged, and CI passes.

### Phase 2 — Publish the new package identity

- License MakersBrain-authored package contents under `AGPL-3.0-only`, retain
  upstream font licenses, and state separately that the copyright license does
  not grant trademark rights or permission to imply endorsement.
- Change the package name to `@makersbrain/ui` and start its independent release
  line at `0.1.0`; the old and new names are distinct registry subjects.
- Update package metadata, documentation, workflow configuration, provenance,
  registry configuration, and examples to use the new name.
- Preserve equivalent exports and behavior in the first `@makersbrain/ui`
  release. Do not combine the identity cutover with CSS or component redesign.
- Publish `@makersbrain/ui@0.1.0` and verify a clean installation and packed
  tarball from a temporary consumer.
- Leave existing applications pinned to `@makersbrain/brand` until their own
  migration phase. Do not require an atomic multi-repository change.
- Document `@makersbrain/ui` as the successor, but do not deprecate the old
  package while known applications still depend on it.

Exit criteria: `@makersbrain/ui@0.1.0` installs independently, contains every
documented export, has explicit code and brand-asset terms, and no existing
consumer was forced to change to complete the release.

### Phase 3 — Launch `mb-site` and satisfy OAuth prerequisites

- Create `MakersBrain/mb-site` as a Svelte 5/SvelteKit repository using
  `@sveltejs/adapter-static`.
- Pin `@makersbrain/ui` and consume its current tokens, fonts, lockup, and UI
  layer directly. The website must not wait for later consolidation phases.
- Use prerendered routes with trailing slashes:
  `/`, `/privacy/`, and `/terms/`.
- Set `prerender = true`, `csr = false`, and `trailingSlash = 'always'` at the
  root layout so the public site emits complete HTML without a hydration
  runtime. If client behavior is introduced later, revisit this deliberately.
- Migrate the homepage and legal content from `mb-odoo-addons/landing` without
  moving the UI system or copying its CSS.
- Add metadata, canonical URLs, sitemap, robots policy, favicons, accessible
  landmarks, and Cloudflare Pages `_headers`.
- Configure Cloudflare Pages with production branch `main`, build command
  `npm run build`, and output directory `build`.
- Add visible links to the canonical public Privacy Policy and Terms from the
  authenticated control-plane shell and any Google-authenticated product
  surface before verification is submitted.
- Connect `makersbrain.app`, verify it in Google Search Console, and use the
  exact public homepage, privacy, and terms URLs in the OAuth consent screen.
- Confirm the contact mailbox, legal controller identity, approved retention
  language, and legal review before OAuth verification or production personal
  data.

Exit criteria: Cloudflare production and preview deployments pass link,
accessibility, security-header, and no-JavaScript smoke checks; all public URLs
are reachable without sign-in; in-product policy links resolve to the canonical
pages; and the OAuth consent-screen links exactly match those URLs.

### Phase 4 — Separate foundations from product CSS

- Inventory every selector in `src/ui.css` and classify it as base, primitive,
  composition, or product-specific.
- Add `fonts.css` so consumers stop recreating identical `@font-face` rules.
- Add `base.css` for reset, typography, focus, reduced motion, and accessibility
  utilities.
- Keep reusable primitives in a domain-neutral layer.
- Move control-plane-specific selectors such as `.workshops`, `.member`,
  `.recovery-row`, `.operation-card`, and `.invitation-shell` into the control
  plane.
- Retain `ui.css` as a compatibility composition during the migration; remove
  no existing export in a `0.x` patch release.
- Ensure selectors in shared CSS use an `mb-` prefix or an explicitly
  documented low-specificity public class. Avoid styling generic application
  class names accidentally.
- Release these additions under `@makersbrain/ui`, then migrate the control
  plane's package manifest, imports, Docker build, and lockfile. Move its
  product-specific rules locally in the same consumer change.

Exit criteria: shared CSS contains no product-domain nouns, the control plane
uses only `@makersbrain/ui`, and its baseline renders and checks pass.

### Phase 5 — Establish one token source and Odoo projection

- Introduce a machine-readable token source for values that must reach CSS and
  Odoo SCSS.
- Generate committed CSS tokens and an Odoo-compatible SCSS artifact inside
  the `@makersbrain/ui` package. The package build must never write into a
  sibling consumer repository.
- Export the generated Odoo artifact through the package manifest. The Odoo
  repository either consumes it during its asset build or checks its pinned
  local projection byte-for-byte against that package artifact.
- Keep semantic tokens separate from raw palette values.
- Preserve the three-state theme rule: system preference by default, explicit
  `data-theme` choice overriding it in either direction.
- Add automated contrast checks for documented text/background pairs.
- Retain the catalogue data-visualization palette as a consumer-owned,
  independently validated system; only its neutral interface mappings use
  brand tokens.

Exit criteria: the Odoo repository uses `@makersbrain/ui`, no longer relies on
a hand-maintained value copy, generated outputs stay inside their owning
repository, and drift fails CI.

### Phase 6 — Promote proven shared Svelte primitives

- Re-evaluate `StatusBadge`, `ProgressBar`, callouts, and layout primitives
  against the component admission rule after `mb-site` and the control plane
  are using the new package.
- Promote only components with two genuine consumers. Mapping backend states
  to labels and tones stays in the consuming product; components that remain
  single-use remain local.
- Add component types beside implementations and expose them through the
  `@makersbrain/ui/svelte` entry point.
- Add focused tests for accessible names, ARIA state, value bounds, forwarded
  attributes, keyboard focus, and semantic variants.
- Demonstrate each component and state in the generated design chart.
- Migrate one consumer at a time and remove the superseded local component only
  after its checks pass.

Exit criteria: every promoted primitive has at least two real consumers, no
superseded local copy remains, and package plus consumer tests pass. It is valid
for this phase to leave an evaluation candidate local.

### Phase 7 — Normalize framework adapters and migrate the catalogue

- Compare the catalogue's shadcn/Tailwind palette bridge with the plain-CSS
  control-plane mapping.
- Move only stable token-to-framework mappings into an optional adapter.
- Keep Tailwind scanning instructions and theme-selection behavior documented
  beside that adapter.
- Do not make Tailwind, shadcn, or SvelteKit a runtime dependency of the token
  and asset layers.
- Keep chart-specific colours and application layout in the catalogue.
- Release the stable adapter, then migrate the catalogue package manifest,
  imports, Docker build, and lockfile to `@makersbrain/ui`.

Exit criteria: consumers no longer duplicate the same semantic theme mapping,
the catalogue uses only `@makersbrain/ui`, and data visualization and
product-specific styling remain independent.

### Phase 8 — Retire compatibility paths and the old landing build

- Keep the old page available until the custom domain and legal links have been
  verified in production.
- Remove `mb-odoo-addons/landing`, its Python builder, and the `make landing`
  target. Retain the `@makersbrain/ui` development dependency while the Odoo
  token projection or brand checks consume it.
- Preserve only a short documentation link to `mb-site`.
- Verify that Odoo release artifacts never include the public website.
- After every consumer uses `@makersbrain/ui`, remove compatibility CSS only in
  a documented breaking release. At that point, mark `@makersbrain/brand`
  deprecated with a pointer to `@makersbrain/ui` if registry permissions allow
  it. The initial `@makersbrain/ui@0.1.0` was deliberately replaced before
  adoption to correct its license; all subsequent published versions are
  treated as immutable rollback artifacts.

Exit criteria: the public site has one source repository and one deployment
path, and `mb-odoo-addons` retains no website build responsibility.

### Phase 9 — Release and governance

- Use semantic versions and document whether a change is visual-only,
  additive, deprecated, or breaking.
- Require a package release before consumer lockfiles change; do not consume a
  mutable branch in production builds.
- Add a compatibility fixture that installs the packed tarball into a minimal
  Svelte application and compiles every public component export.
- Require before/after visual evidence for token or component appearance
  changes and keyboard/accessibility evidence for behavioral changes.
- Deprecate for at least one minor release before removing a public export.
- Keep release notes actionable for each consumer.
- Document two rollback paths:
  - before a consumer migrates, it remains pinned to `@makersbrain/brand@0.1.0`;
  - after migration, it rolls back by pinning its previous known-good
    `@makersbrain/ui` version;
  - reverting across the package-name boundary additionally restores that
    consumer's manifest, imports, Docker configuration, and lockfile together.

Exit criteria: package releases are reproducible, consumer upgrades are
deliberate, and both same-package and cross-package rollback procedures have
been rehearsed.

## Verification matrix

| Layer | Required verification |
| --- | --- |
| Package | generated assets, `svelte-check`, export/tarball check, component tests |
| CSS/tokens | light/dark/system render, contrast checks, no undefined variables |
| Control plane | existing Svelte check/build plus authenticated-shell smoke render |
| Catalogue | existing Svelte check/build plus chart palette regression checks |
| Odoo | SCSS projection drift check, asset build, login/backend render |
| Public site | static build, link crawl, HTML without JS, responsive/a11y smoke tests |
| Deployment | Cloudflare preview, custom-domain TLS, headers, canonical URLs, public access |

## Rollout order

Use one-way, releasable steps:

1. record the current test and visual baseline;
2. rename the repository and update repository metadata only;
3. publish behavior-equivalent `@makersbrain/ui@0.1.0` with explicit licensing;
4. build and deploy `mb-site`, add in-product legal links, and complete the
   public OAuth prerequisites;
5. split shared and product CSS, release it, and migrate the control plane;
6. publish the token source and Odoo projection, then migrate Odoo tooling;
7. promote only proven shared components;
8. publish the optional framework adapter and migrate the catalogue; and
9. deprecate the old package and remove compatibility CSS and the old landing
   build only after every consumer is pinned to the replacement.

At every step, the previous published package remains available. A rollback
within `@makersbrain/ui` restores one pinned version; a rollback across the
package-name boundary restores the consumer manifest, imports, build
configuration, and lockfile as one reviewed change. Do not coordinate an
unreleased package change and simultaneous edits across all repositories as one
atomic deployment.

## Completion criteria

The consolidation is complete when:

- the canonical repository is `MakersBrain/mb-ui`;
- `@makersbrain/ui` is the single active published design-system package and
  `@makersbrain/brand` is retained only as deprecated release history;
- no consumer copies brand fonts, marks, semantic token values, or shared
  primitives by hand;
- shared styles and components contain no product-domain behavior;
- Odoo's required SCSS values are generated and drift-checked;
- the control plane, catalogue, Odoo, and public site visibly share the same
  identity, foundations, and interaction states;
- `mb-site` alone owns the public homepage and legal pages; and
- each migrated consumer can upgrade or roll back within `@makersbrain/ui`
  through one pinned version, and the cross-package rollback procedure is
  documented and rehearsed.
