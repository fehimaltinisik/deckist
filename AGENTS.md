# AGENTS.md

DeckIst is one repo with two packages: `webservice/` (FastAPI) and `frontend/` (Vite, React, deck.gl).

Cursor loads this file together with the `AGENTS.md` next to the code you are editing. Shared rules stay here. Package rules stay in the package file.

## Where to read

| Working in | Rules |
| --- | --- |
| `webservice/` | `webservice/AGENTS.md` |
| `frontend/` | `frontend/AGENTS.md` |
| How to run a package | That package's `README.md` |

## Boundaries

- This repo is the transit visualization. Do not add another backend, accounts, or a deploy-target change unless the task asks.
- Update `master` from `origin`, branch off that commit, and do not commit on `master`.

## Instructions

- Keep a change inside the package it belongs to. A frontend task does not edit the webservice, and the reverse, unless the task says both.
- Do not rename variables, edit unrelated imports, or clean up files outside the task.
- Prefer the existing module layout over a new pattern.
