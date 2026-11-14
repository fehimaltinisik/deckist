# AGENTS.md

DeckIst map UI. Callers are anonymous. There is no login. Shared repo rules are in the root `AGENTS.md`.

## Readability

Backend review of this UI has to be possible without parsing JSX. Write control flow as statements.

- Prefer `if` and early `return`. Unnest. One condition per branch.
- Do not nest ternary operators. Do not use a ternary chain in place of `if` / `else`.
- Extract a named function when a branch is hard to read, especially around auth, refresh, tokens, report HTML, and iframes.
- Keep styling out of the branch. Put layout in `sx`, a `styled()` component, or a colocated styles module. The conditional decides what renders. It does not decide spacing, color, and markup in the same expression.
- Security-sensitive code (session restore, `refreshSession`, route guards, report iframes, CSP-related markup) stays flat enough to review top to bottom.

## HTTP

- Calls go through axios in `src/actions/actions.jsx` against `VITE_BACKEND_SERVICE_URL`.
- Do not add a token, a refresh cookie, or RTK Query unless the task asks.
- Route and time state stays in Redux memory. Do not write it to `localStorage`.
- Keep the compact-geometry mapping in `src/actions/actions.jsx` aligned with the backend response. Do not change field names on one side only.
