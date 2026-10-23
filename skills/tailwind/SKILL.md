---
name: tailwind
description: How we style with Tailwind CSS v4, including CSS-first configuration with @theme, content detection, dark mode, design tokens, class merging and the v3 to v4 renames that silently change how UIs look. Use whenever writing or reviewing Tailwind classes, setting up Tailwind in Next.js, Vite, Django templates or Shopify themes, migrating from Tailwind v3, adding design tokens or custom utilities, or when you see @import "tailwindcss", tailwind.config or @theme.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, css, tailwind, frontend]
---

# Tailwind CSS

Tailwind v4 moved configuration into CSS. Most broken Tailwind code from
models is v3 syntax (`tailwind.config.js` themes, `@tailwind base`, old
utility names) dropped into a v4 project.

## Before you start

1. Check the version (`npm ls tailwindcss`). v4 projects have
   `@import "tailwindcss";` in a CSS file; v3 projects have `@tailwind base;`
   plus a `tailwind.config.js` theme.
2. Find the design tokens: the `@theme { ... }` block (v4) or `theme.extend`
   (v3). Use existing tokens before inventing values.
3. Check for a class-merge helper (`cn()` built on `clsx` + `tailwind-merge`)
   and `prettier-plugin-tailwindcss`.

## Defaults for new projects

- Tailwind 4.3+, via `@tailwindcss/vite` (Vite), `@tailwindcss/postcss`
  (Next.js/PostCSS) or `@tailwindcss/cli` (Django templates, Shopify themes,
  anything without a JS build).
- Tokens (colours, fonts, spacing, radii, breakpoints) in `@theme` as CSS
  variables; components use the tokens, not raw hex values.
- `cn()` helper for conditional classes; Prettier plugin for class order.

```css
@import "tailwindcss";
@source "../templates";                        /* add paths auto-detection misses */
@custom-variant dark (&:where(.dark, .dark *)); /* class-based dark mode */

@theme {
  --color-brand-500: oklch(0.62 0.19 260);
  --font-sans: "Inter", sans-serif;
}
```

## Verify loop

- Run the dev server and look at the changed screens at mobile and desktop
  widths, in light and dark mode.
- `npm run build` and confirm the classes exist in the output CSS. A class
  that "does nothing" usually wasn't detected (see Pitfalls).

## Rules that matter

- **No dynamic class construction.** `bg-${color}-500` is invisible to the
  scanner. Map to complete class strings: `{ red: "bg-red-500", ... }[color]`.
- Prefer tokens and the default scale over arbitrary values (`p-[13px]`);
  repeated arbitrary values mean a token is missing.
- Extract repetition into components (React/Liquid/Django includes), not
  into `@apply`-heavy CSS. Define custom utilities with `@utility`, not
  `@layer utilities`.
- Mobile-first: unprefixed = all sizes, `md:` and up add overrides.
- Accessibility still applies: visible focus styles (`focus-visible:`),
  sufficient contrast, `sr-only` labels for icon buttons.

## Changed recently (checked 2026-10-23, latest 4.3.3)

- **v4 config is CSS-first:** `@theme`, `@source`, `@utility`,
  `@custom-variant`, `@plugin`. A JS config still loads via
  `@config "./tailwind.config.js";` for migrations.
- **Content detection is automatic** (`.gitignore`d paths are skipped); add
  extra paths with `@source`.
- **v3 → v4 renames that change visuals:** `shadow-sm`→`shadow-xs`,
  `shadow`→`shadow-sm`, `rounded`→`rounded-sm`, `blur`→`blur-sm`,
  `outline-none`→`outline-hidden`; `ring` default width 3px → 1px; default
  border colour is now `currentColor`. Important modifier goes at the end:
  `bg-red-500!`. Run `npx @tailwindcss/upgrade` rather than renaming by hand.
- **v4 browser floor:** Safari 16.4+, Chrome 111+, Firefox 128+. Projects
  that need older browsers must stay on v3.4.
- **4.3** added scrollbar, scrollbar-gutter, zoom and tab utilities plus
  `@container-size`; **4.2** added the mauve/olive/mist/taupe palettes and a
  webpack plugin.

## Pitfalls

- Mixing v3 docs/snippets into a v4 project (`@tailwind` directives,
  `theme.extend` edits that are never loaded).
- Conflicting classes (`p-2 p-4`) where order in the CSS, not the attribute,
  decides the winner; use `tailwind-merge`.

## Sources

- `research/2026-10-23-stack-baseline.md` → Tailwind section.
