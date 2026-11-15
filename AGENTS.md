# AGENTS.md

DeckIst is one repo with two packages: `webservice/` (FastAPI) and `frontend/` (Vite, React, deck.gl). It shows a day of Istanbul bus traffic.

Cursor loads this file together with the `AGENTS.md` next to the code you are editing. Shared rules stay here. Package rules stay in the package file.

## Where to read

| Working in | Rules |
| --- | --- |
| `webservice/` | `webservice/AGENTS.md` |
| `frontend/` | `frontend/AGENTS.md` |
| How to run a package | That package's `README.md` |

## Boundaries

- Schedules come from İETT GTFS (`iett-gtfs-verisi`). Bus paths come from the İETT route lines dataset (`iett-hat-guzergahlari`).
- Do not add another backend, accounts, or a deploy-target change unless the task asks.
- Update `master` from `origin`, branch off that commit, and do not commit on `master`.

## Code style

Follow Robert C. Martin's Clean Code for functions. A reader should follow a function line by line without decoding any single line.

- Keep functions small and doing one thing. Extract a well-named helper instead of a comment or a long block.
- One level of abstraction per function. The public function reads like a summary; details live in helpers below it.
- Name intermediate values and conditions. Prefer named tuples or small classes over indexing into tuples.
- Few arguments. Group related tuning values into one object instead of passing them one by one.
- Prefer early returns over nested branches.

Package files add language-specific rules.
