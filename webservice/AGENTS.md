# AGENTS.md

FastAPI service for DeckIst. Shared repo rules are in the root `AGENTS.md`.

## Read before deciding

| Question | Doc |
| --- | --- |
| How does the repo fit together? | `../AGENTS.md` |
| How do I run this package? | `README.md` |

## Boundaries

- No accounts. Do not add a login wall unless the task asks.
- Leave `/route` and `/routes` in place unless the task says to remove them.

## Layering

HTTP, services, persistence, and domain stay in separate packages. New deck behavior copies `src/routers/deck.py` and its service and mapper. Do not add SQL, FastAPI types, or HTTP models into whichever module is already open.

## Refactoring Rules

1. Do not rename variables during move-only refactors.
	Keep variable names unchanged when reorganizing code (for example: extracting methods, moving blocks, splitting files, or reordering logic) unless a rename is explicitly requested.

2. Do not edit out-of-scope files or unrelated imports.
	Limit changes to files and code paths required by the task. Avoid touching random files, unrelated import sections, or opportunistic cleanups unless explicitly requested.

## Import Rules

1. Use absolute imports, not relative imports.

2. Use one import per line.

3. For first-party application modules (routers, services, repositories, clients, and similar), import the module with a clear alias and access symbols through the module namespace. Use this when helper names such as get_user could collide across modules.

	Do not:
	from src.services.user import get_user

	Do:
	from src.services import user as user_service
	user_service.get_user(...)

4. Direct symbol imports are fine for third-party and standard-library modules (for example: from loguru import logger, from typing import Optional).

## Module Layout

1. Put public functions first. Put private helpers, names that start with `_`, at the bottom of the module.
	Callers above them are fine: the helper runs after the module has finished loading. Leave private helpers in older modules where they are unless that file is already in scope for another change.

## Comment Rules

1. Do not add comments to new code under src unless requested or truly necessary.
	Default to self-explanatory code. Add a brief comment only when logic is non-obvious and readability would otherwise suffer.

## Language Rules

1. Do not use Turkish in source code except content.
	Keep identifiers, comments, docstrings, API/schema descriptions, log messages, and test names in English. Turkish is allowed only in content data (for example route labels and UI copy).

## Security Rules

This API is a public App Runner service. The frontend is Amplify. There is no API Gateway in this design, and there is no auth on these routes. Do not treat a route as safe because the caller is the frontend.

Review security-sensitive changes carefully, by reading the branch. Do not assume the surrounding code is already safe. Slow down when a change touches who can call the process, what an anonymous caller can learn, or where secrets are read or logged:

- Routes and CORS
- Logging and secrets

1. No secret defaults in code. Read secrets from the environment and list them in `.env.example`.

2. Do not log credentials, connection strings, or query strings that carry them.

3. CORS allow-list comes from the `ORIGINS` environment variable.

## Test Rules

1. Prefer BDD-style test names for structure, not strict enforcement.
	Aim for clear Given/When/Then-style intent when practical, but prioritize readability over rigid formatting.

2. Always separate setup, act, and assert blocks with a blank line.
	Keep tests visually structured so each phase is easy to scan.

3. Group test cases per function under a class.
	Each public function under test gets its own class Test<FunctionName>: block. Module-level fixtures remain at module scope.

### Test Naming Template

Use patterns like:
- test_given_valid_request_when_search_called_then_returns_results
- test_given_missing_user_id_when_create_called_then_raises_validation_error
- test_when_cache_is_warm_then_returns_cached_response
