# AGENTS.md

A day of Istanbul bus traffic. This package is the Vite, React, and deck.gl map. Applicants, a panel, and grants do not exist here. Shared repo rules are in the root `AGENTS.md`.

## Readability

Backend review of this UI has to be possible without parsing JSX. Write control flow as statements.

- Prefer `if` and early `return`. Unnest. One condition per branch.
- Do not nest ternary operators. Do not use a ternary chain in place of `if` / `else`.
- Extract a named function when a branch is hard to read, especially around auth, refresh, tokens, report HTML, and iframes.
- Keep styling out of the branch. Put layout in `sx`, a `styled()` component, or a colocated styles module. The conditional decides what renders. It does not decide spacing, color, and markup in the same expression.
- Security-sensitive code (session restore, `refreshSession`, route guards, report iframes, CSP-related markup) stays flat enough to review top to bottom.

## HTTP

- Calls go through axios in `src/actions/actions.jsx` against `VITE_BACKEND_SERVICE_URL`. There is no RTK Query, refresh cookie, or access token. Do not add them for the public demo.
- The compact mapper is the deck.gl contract. Do not change `{ path, timestamps }` or rename `routeShortName` on one side only. Helper lines live in `INITIAL_STATE_HELPER_ROUTE_SEGMENTS`.
