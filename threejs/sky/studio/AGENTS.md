# Living Field Studio v01 — Codex instructions

This file applies to work under `threejs/sky/studio/` and to any new shared files created specifically for Living Field Studio.

## Read first

1. `threejs/sky/studio/HANDOFF.md`
2. `threejs/sky/studio/studio-config.example.json`
3. `threejs/sky/v12/index.html`
4. `threejs/sky/index.html`

## Non-negotiable rules

- Work only on branch `feature/living-field-studio-v01` unless the user explicitly instructs otherwise.
- Do not modify, delete, rename, or overwrite `threejs/sky/v03` through `threejs/sky/v12`.
- Do not change the production router in `threejs/sky/index.html` until the Studio has been reviewed and the user explicitly approves publication.
- The default Studio preset must reproduce the visual character of Living Field v12 as closely as practical.
- Preserve the core design principle: meadow, responsive sky, ordinary flyers, and rainbow flyer flocks react to one shared wind field with different sensitivities.
- Do not draw wind as obvious lines. Wind should remain legible through motion, density, light, and the behavior of grass and flyers.
- Avoid changing the visual language beyond what is needed to expose parameters. The tool is for studying the existing design, not redesigning it without instruction.
- Keep the project deployable as static GitHub Pages content. Prefer plain HTML, CSS, and ES modules. Do not introduce a framework or mandatory build step unless there is a clear technical need and it is documented.
- Do not put GitHub write credentials or secrets in browser code.

## Implementation priorities

1. Make the current v12 design parameter-driven without breaking its default appearance.
2. Implement deterministic seeded randomness.
3. Implement a usable parameter panel grouped by Scene, Wind, Meadow, Sky, Ordinary Flyers, Rainbow Flocks, and Quality.
4. Distinguish live-updatable parameters from parameters that require scene reconstruction.
5. Implement preset save/load, A/B slots, undo/redo, and JSON import/export.
6. Keep desktop and mobile usable. The mobile UI may be a collapsible bottom sheet or drawer.
7. Preserve `prefers-reduced-motion` behavior.

## Engineering guidance

- Keep renderer logic separate from control-panel logic.
- Use one canonical configuration object. UI values, presets, JSON export, and runtime settings must all use that object.
- Validate imported configuration values against safe ranges before applying them.
- Use a seeded PRNG for all design-relevant randomness. Do not mix uncontrolled `Math.random()` into reproducible scene generation.
- For expensive parameters such as blade count and instance count, provide an explicit `Apply / Rebuild` operation rather than rebuilding on every slider event.
- Avoid allocation-heavy work inside the animation loop.
- Keep the current fixed-color material approach for rainbow flyers unless testing proves a simpler solution works reliably across current browsers.
- Initialize every instance matrix explicitly so no stray foreground triangles appear.
- Retain stratified spawning or an equivalent method that prevents repeated spatial bias.

## Verification before reporting completion

- Run from a local HTTP server, not by opening `file://` directly.
- Confirm no JavaScript errors in the browser console.
- Confirm the v12 baseline preset loads and animates.
- Confirm changing each primary control has the intended effect.
- Confirm the same seed and configuration reproduce the same initial scene after reload.
- Confirm JSON export and re-import reproduce the same settings.
- Confirm A/B switching does not corrupt state.
- Confirm undo and redo work for representative controls.
- Confirm desktop layout around 1920×1080 and mobile layout around 390×844.
- Confirm reduced-motion mode remains usable.
- Confirm published versions v03–v12 are unchanged by comparing Git status/diff.

## Git workflow

- Commit logical units with clear messages.
- Do not merge to `master` automatically.
- At the end, report changed files, tests performed, known limitations, and the exact local URL used for verification.
