# Copilot Instructions — Living Documentation Collector for Azure DevOps

This file tells a coding agent how to work in this repository. It describes this repo's
own layout, contract, and workflow; it is not shared with or copied from other repos.

**Section order** — keep the sections below in exactly this order:
Overview → Repo specifics → Coding guidelines → Inputs → Language and style →
Logging and string formatting → Docstrings and comments → Patterns → Testing →
Tooling and quality gates → Common pitfalls → Learned rules.

**House rules for this file**

- Must write every guidance bullet as a constraint led by one of `Must`, `Must not`, `Prefer`, `Avoid`.
- Must not put a colon after the leading keyword, and Must not use any other keyword style such as `Do`, `Should`, or a two-keyword `Do` / `Avoid` variant.
- Prefer bullet lists over paragraphs.
- Must end the file with a single trailing newline.

## Overview

`Living Documentation Collector for Azure DevOps` is a composite GitHub Action that
data-mines Azure DevOps organizations and projects for living-documentation content and
writes machine-readable JSON for the downstream `living-doc-*` generators.

- Must treat execution as a GitHub Action on a GitHub-hosted runner as the supported path; the `run_script.sh` / `python3 main.py` flow is a development and debugging affordance only.
- Must read action inputs from `INPUT_*` environment variables and nowhere else.
- Must keep the whole collect pipeline AI-free — deterministic Python only, no LLM call anywhere in that path.
- Prefer keeping environment access at the module boundary — `action_inputs.py` and `main.run()` — and Must keep the collectors and models free of environment reads.

## Repo specifics

Module map — a flat package per mode plus shared `utils/`:

| Path | Responsibility |
|---|---|
| `main.py` | Entry point — `run()`; orchestrates user-config validation and the `work-items` mode collector, then sets the `output-path` Action output and maps any failure to exit code `1` |
| `action_inputs.py` | Input layer — `ActionInputs(BaseActionInputs)`, reads every `INPUT_*` via `living_doc_utilities.github.utils.get_action_input`; `_validate()` verifies the ADO PAT and each configured organization against the Azure DevOps REST API (`requests`); `get_organizations()` parses `work-items-organizations` JSON into `ConfigOrganization`, raising `FetchOrganizationsException` |
| `work_items/` | `work-items` mode — `collector.py` (`ADWorkItemsCollector`, `collect()` → `bool`), `model/config_organization.py` (`ConfigOrganization` — `load_from_json`, `organization_name`, `projects_name_filter`) |
| `utils/` | Shared — `constants.py` (`Mode` enum, `INPUT_*` key names `WORK_ITEMS_ORGANIZATIONS` / `VERBOSE_LOGGING`), `exceptions.py` (`FetchOrganizationsException`), `utils.py` (`make_absolute_path`) |

- Must treat `main.py` function `run()` as the entry point — its step order is setup logging → `ActionInputs().validate_user_configuration()` → when `work-items` is enabled `ADWorkItemsCollector(output_path).collect()` → `set_action_output("output-path", output_path)` → `sys.exit(1)` when any enabled mode failed.
- Must keep the step order and the `"Liv-Doc collector for Azure DevOps - ..."` step logs in `run()` stable, since `tests/unit/test_main.py` asserts on them.

Inputs — `INPUT_*` environment variables, parsed only in `ActionInputs` (key names in `utils/constants.py`):

| Input | Env var | Required | Notes |
|---|---|---|---|
| `ADO-TOKEN` | `INPUT_ADO_TOKEN` | yes | Azure DevOps PAT; read via `get_action_input("ADO_TOKEN", "")` |
| `work-items` | `INPUT_WORK_ITEMS` | no | mode switch; `"false"` when unset |
| `verbose-logging` | `INPUT_VERBOSE_LOGGING` | no | default `false` |
| `work-items-organizations` | `INPUT_WORK_ITEMS_ORGANIZATIONS` | no | JSON array string, default `[]`; required when `work-items` is `true`; `jq`-compacted in `action.yml` before it reaches the runner |

Contract-sensitive outputs:

- Must keep the Action output key `output-path` stable — set via `set_action_output("output-path", ...)` and exposed by `action.yml` as `output-path`.
- Must keep exit-code behaviour stable — `0` on success, `1` on any failure (user-config validation, or an enabled mode's `collect()` returning `False`). There is no `2`–`5` taxonomy in this repo.
- Must keep the `"Liv-Doc collector for Azure DevOps - ..."` log strings stable — tests assert exact text.

## Coding guidelines

- Must keep changes small and scoped to the task.
- Prefer explicit code over clever constructs.
- Must keep externally visible behaviour stable unless the task is an intentional contract change.
- Must not change existing log texts or error messages without a stated reason.
- Prefer pure functions for parsing and collection logic, and Avoid reading the environment outside `action_inputs.py` and `main.run()`.

## Inputs

- Must read every input through `ActionInputs`, and Must not call `get_action_input` or `os.getenv("INPUT_...")` from any other module.
- Must centralise parsing, defaulting, and validation in `ActionInputs` (`_validate()` / `validate_user_configuration()`).
- Avoid duplicating input validation across modules.
- Must raise `FetchOrganizationsException` for unparseable `work-items-organizations` JSON so `_validate()` counts it as a configuration error and `run()` exits `1`.

## Language and style

- Must target Python 3.10+ (the ecosystem floor; the published action image may run a newer interpreter).
- Must add type hints for new public functions and classes.
- Must keep imports at module top — no imports inside functions or methods.
- Must not introduce a 3.11+-only standard-library import or syntax without a `sys.version_info` fallback — `X | Y` unions and `match` / `case` are 3.10-native and stay.
- Must not disable a linter rule inline unless this file records the exception under Learned rules.

## Logging and string formatting

- Must use `logging`, never `print`.
- Must use lazy `%` formatting in logging calls — `logger.info("msg %s", value)`.
- Must not use f-strings inside logging calls.
- Prefer the clearest formatting when constructing exception and failure messages, and Must keep contract-sensitive strings stable.

## Docstrings and comments

- Must match the existing module docstring style — a short summary of what the module contains.
- Prefer a one-line docstring summary for functions, with `@param` / `@return` / `@raise` lines where they add information, matching the surrounding code.
- Avoid tutorial-style prose or long examples in docstrings.

## Patterns

- Prefer leaf modules raising the typed exceptions in `utils/exceptions.py`.
- Must let `main.run()` be the only place that translates a failure into an Action-failure exit code.
- Prefer private helpers (`_name`) for internal behaviour (`_call_profile_api`, `_call_org_api`, `_validate`).
- Must keep integration boundaries — the Azure DevOps REST API (`requests`), and the filesystem — explicit and mockable.

## Testing

- Must use `pytest` with `pytest-mock` (`mocker`), and Must not use `unittest`.
- Must keep tests under `tests/`, mirroring the package layout — `tests/unit/` today, adding `tests/unit/work_items/`, `tests/unit/utils/` as the mode grows.
- Must test behaviour — return values, raised exceptions, log messages, exit codes.
- Must mock `INPUT_*` environment variables and the Azure DevOps REST API in unit tests.
- Must not call external services or the real Azure DevOps API in unit tests.
- Prefer shared fixtures in `tests/conftest.py`.

## Tooling and quality gates

- Must run `make qa` before finishing a code change — it runs `format-check` → `lint` → `types` → `coverage` and fails on the first failing gate.
- Must use the individual targets while iterating — `make format`, `make format-check`, `make lint`, `make types`, `make test`, `make coverage`.
- Must keep `make lint` clean — it runs ruff (`E` / `F` / `I` / `B` over tracked `*.py`, config in `pyproject.toml`) then Pylint, and Pylint must score 9.5 or higher.
- Must keep `make format-check` (Black, line length 120, config in `pyproject.toml`) clean, and Prefer `make format` (ruff autofix + Black) to fix import order and formatting in one step.
- Must keep `make types` (mypy, config in `pyproject.toml`) clean, and Prefer fixing types over adding ignores.
- Must keep `make coverage` (pytest, `--cov-fail-under=80`) passing.
- Must expect the lint/test workflow to call the same `make` targets, so local and CI never drift.

## Common pitfalls

- Must verify a new dependency supports Python 3.10 before adding it, and Must keep `requirements.txt` and `action.yml` in step when inputs or dependencies change.
- Must remove unused imports and variables in the same change, and Avoid leaving dead code.
- Avoid changing externally visible strings, the `output-path` key, or exit codes unless the task calls for it.
- Must keep `pyproject.toml`, `.pylintrc`, and the CI Python version in step when the floor moves.

## Learned rules

- Must keep the `"Liv-Doc collector for Azure DevOps - ..."` log strings and exit code `1` stable — `tests/unit/test_main.py` asserts exact strings and `sys.exit(1)`.
- Must not introduce a `2`–`5` exit-code taxonomy; this action reports success as `0` and every failure as `1`.
- Must keep `ADWorkItemsCollector.collect()` returning `bool` — `main.run()` maps `False` to exit code `1`.
