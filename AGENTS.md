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

- Schedules are İETT GTFS (`iett-gtfs-verisi`). Do not load the `public-transport-gtfs-data` feed or its shapes.
- Do not add another backend, accounts, or a deploy-target change unless the task asks.
- Update `master` from `origin`, branch off that commit, and do not commit on `master`.
