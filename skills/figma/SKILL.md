---
name: figma
description: How we move between Figma and code, covering implementing Figma frames in Next.js with Tailwind or in Flutter through the official Figma MCP server, mapping Figma variables to design tokens, Code Connect for component mapping, pushing coded screens back into Figma, design-system sync, and design handoff checks for states, responsiveness and accessibility. Use whenever someone shares a figma.com link, asks to build or update UI from a design, wants design tokens or a component library synced between Figma and code, sets up Code Connect, or wants a coded page turned into a Figma design.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [design, figma, frontend, ui]
---

# Figma

The design is the visual target; the codebase's components and tokens are
the building material. Never paste generated absolute-positioned markup into
the app. Translate it into our components, layout and tokens.

## Before you start

1. Check the **Figma MCP server** is connected and the Figma plugin skills
   are available. They're authoritative for tool usage:
   `figma-design-to-code` (**required before `get_design_context`**),
   `figma-code-connect`, `figma-generate-design` (code → Figma),
   `figma-generate-library` (design systems), `figma-use`.
2. Parse the URL: `figma.com/design/<fileKey>/...?node-id=1-2` → fileKey,
   nodeId `1:2` (dash becomes colon). Branch URLs use the branch key.
3. Load the project's UI stack skills: `nextjs` + `tailwind`, or `flutter`.
   Find the existing component library and token source (`@theme` in
   Tailwind v4, `ThemeData` in Flutter).

## Design → code

1. Get the design context **with a screenshot** (the visual target).
   Sparse responses mean fetching child nodes, not guessing.
2. **Reuse before you build:** match design components to existing code
   components (Code Connect mappings first), and design variables to
   existing tokens. Add tokens to `@theme` / `ThemeData` rather than
   hardcoding hex values or pixel sizes.
3. Implement with responsive layout (flex/grid, Flutter `Row`/`Column`/
   `LayoutBuilder`), not fixed positions, and wire real interactivity and
   data.
4. Download every static asset into the repo; no temporary Figma asset URLs
   in code.
5. **Verify visually:** render the screen (dev server / Flutter run),
   screenshot it at the design's frame size, and compare with the design
   screenshot; fix in-scope mismatches.

## Handoff checklist (ask design if missing)

- States: default, hover, focus-visible, active, disabled, loading, empty,
  error, success.
- Breakpoints: mobile and desktop at minimum; what collapses or reflows.
- Content extremes: long names, missing images, 0 and 1000 items, Indian
  number/currency formats (₹1,00,000).
- Accessibility: contrast, focus order, labels for icon buttons, touch
  targets ≥ 44 px.
- Motion: durations and easing, and reduced-motion behaviour.

## Design system sync

- **Figma variables ↔ code tokens** are the contract. Choose one source of
  truth per token set (usually Figma for colour/type, code for spacing
  scale) and sync with a script or Style Dictionary (`style-dictionary` 5),
  not by hand.
- **Code Connect** (`@figma/code-connect` 2.x, `*.figma.ts` files next to
  components) makes Dev Mode and the MCP server return *our* component
  usage. Add mappings for the most-used components first.
- Code → Figma (`figma-generate-design`) for documenting built screens or
  starting a redesign from production.

## Pitfalls

- Implementing from the screenshot alone (wrong spacing, tokens, assets).
- A new one-off component for every design variant instead of extending the
  existing component's props/variants.
- Ignoring states and breakpoints the design didn't show; ask rather than
  invent.

## Sources

- Installed Figma plugin skills and registry versions;
  `research/2026-10-23-product-platform-baseline.md` → Figma.
