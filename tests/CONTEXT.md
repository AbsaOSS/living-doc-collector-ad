# tests

Parent: [../CONTEXT.md](../CONTEXT.md)

## Purpose

Unit tests for the action. `tests/unit/` mirrors the package tree (`tests/unit/utils/`, `tests/unit/work_items/`).
`make test` and `make coverage` ignore `tests/integration/`.

## Conventions

- `pytest` with `pytest-mock` (`mocker`); never `unittest`.
- Test behavior: return values, raised exceptions, log calls, exit codes. Cover the success and the failure path.
- Never call the real Azure DevOps API or any other external service. Stub HTTP with `responses` only, so the suite
  keeps one HTTP-mocking convention.
- Never put a real PAT in a test, fixture or log assertion.
- Shared fixtures go in `tests/conftest.py`. Its autouse `_clear_action_inputs` deletes the four `INPUT_*` variables
  before every test, so set the ones a test needs with `monkeypatch.setenv`.
- Assert contract-sensitive strings and exit codes exactly (the parent's Contracts section).
- Coverage gate: 80 % over non-test code (`tests/*` is omitted in `pyproject.toml`).

## Mock targets

| To fake | Use | Applies to |
|---|---|---|
| `INPUT_*` action inputs | `monkeypatch.setenv("INPUT_ADO_TOKEN", ...)`, or `mocker.patch("action_inputs.ActionInputs.get_*", return_value=...)` | `action_inputs.py`, which reads through `get_action_input` |
| User-config validation | `mocker.patch("main.ActionInputs.validate_user_configuration", return_value=True/False)` | `main.run()` |
| ADO REST API | `@responses.activate` and `responses.add(responses.GET, <url>, status=..., json=...)` with `https://app.vssps.visualstudio.com/_apis/profile/me` and `https://dev.azure.com/<org>/_apis/projects`, registered without the `api-version` query | `_call_profile_api`, `_call_org_api` |
| Per-organization outcome | the org endpoint returning `200`, `401`, `404` or another status; assert the error count `_validate()` returns and the logged error | `ActionInputs._validate()` |
| Organization JSON | plain `dict`s passed to `ConfigOrganization.load_from_json`, no mocks | `work_items/model/config_organization.py` |
| `FetchOrganizationsException` | a malformed JSON string in `INPUT_WORK_ITEMS_ORGANIZATIONS` | `ActionInputs.get_organizations()` |
| Mode collector | `mocker.patch("main.ADWorkItemsCollector")`, then set `.return_value.collect.return_value` | `main.run()` dispatch |
| Exit code | `pytest.raises(SystemExit)`, then assert `.value.code == 1` | `main.run()` |
| Action output | `mocker.patch("main.set_action_output")`, assert the call `("output-path", <absolute path>)` | `main.run()` |
| Path resolution | `mocker.patch("main.make_absolute_path")`, or patch `utils.utils.os.path.isabs` / `os.path.abspath` | `main.run()`, `utils.utils.make_absolute_path` |
| Logging setup and log lines | `mocker.patch("main.setup_logging")`; `mocker.patch("<module>.logger")` and assert `.info` / `.warning` / `.error` calls | `main.run()`, any module |
