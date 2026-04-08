Purpose
- Must follow these instructions when proposing changes for living-doc-collector-ad.
- Must keep repo-specific facts in “Repo additions” (end of file).

Structure
- Must keep sections in the order defined in this file.
- Prefer bullet lists over paragraphs.
- Must write rules as constraints using “Must / Must not / Prefer / Avoid”.
- Must keep wording concrete and reviewable.
- Must keep a single blank line at end of file.

Context
- If this repository is a GitHub Action or CLI:
  - Must assume it runs in an automation runner environment.
  - Must treat environment variables as the primary input channel.
  - Must write outputs only to the configured output folder and expose contract outputs via the declared action/CLI interface.

Coding guidelines
- Must keep changes small and focused.
- Prefer clear, explicit code over clever tricks.
- Must keep externally-visible behavior stable unless intentionally updating the contract.
- Must keep pure logic free of environment access where practical; route I/O and env through dedicated boundaries.
- Must keep externally-visible strings, formats, and exit codes stable unless intentional.

Output discipline
- Prefer concise responses (aim <= 10 lines in the final recap).
- Must not restate large file contents/configs/checklists; link and summarize deltas.
- Prefer actionable bullets over prose.
- When making code changes, must end with:
  - What changed
  - Why
  - How to verify (commands/tests)
- Avoid deep rationale, alternatives, or long examples unless explicitly requested.

PR Body Management
- Must treat the PR description as an append-only changelog.
- Must not rewrite/replace the entire PR body; must append updates.
- Prefer this structure:
  - Keep original description at top.
  - Add updates chronologically below.
  - Use headings like “## Update YYYY-MM-DD” or “## Changes Added”.
  - Each update references the commit hash that introduced the change.

Inputs
- If this repository defines inputs via environment variables:
  - Must treat `INPUT_*` environment variables as the canonical inputs.
  - Must centralize validation in one input/validation layer.
  - Must not duplicate validation across modules.
- If defaults exist:
  - Must document default behavior in one place.
- Prefer documenting required vs optional inputs with defaults.

Language and style
- Must target the runtime/version defined in “Repo additions”.
- Must add type hints/types for new public APIs.
- Must use the project logging framework; must not use `print`.
- Must follow the repo import/include conventions (for Python: imports at top of file).
- Must not disable linter rules inline unless the repo documents an exception process.- Must include the standard copyright/license header in every code file, including `__init__.py`.
- Must use the project first-copyright year.
String formatting
- Must follow the repo-defined formatting rules in “Repo additions”.
- Logging:
  - Must use lazy `%` formatting for all log calls.
  - Must not use f-strings or t-strings in logging calls.
- Non-logging templates:
  - Prefer t-strings for non-logging string templates.
  - Avoid f-strings for user-facing text unless needed for clarity.
- Exceptions/errors:
  - Prefer the clearest formatting rule; must keep contract-sensitive strings stable.

Docstrings and comments
- Must match existing module style and keep consistent across the repo.
- Docstrings:
  - Must start with a short summary line.
  - Prefer structured sections (`Parameters:` / `Returns:` / `Raises:`) when useful.
  - Avoid tutorials, long prose, and doctest examples.
- Comments:
  - Prefer self-explanatory code.
  - Prefer comments for intent/edge cases (the "why").
  - Avoid blocks that restate what code already says.

Patterns
- Error handling:
  - Prefer leaf modules raise exceptions.
  - Prefer entry points translate failures into exit codes / action-failure output.
- Constructors (if applicable):
  - Prefer constructors do not throw; validate via factory/validator if needed.
- Internal helpers:
  - Prefer private helpers for internal behavior (`_name` in Python).
- Testability:
  - Must keep integration boundaries explicit and mockable.
  - Must not make real network calls in unit tests.

Testing
- Must use pytest for unit tests.
- Must keep tests under `tests/`.
- Prefer unit tests under `tests/unit/`.
- Must test behavior via return values, raised errors, log messages, and exit codes.
- Must mock environment variables; must not call external services (e.g., ADO APIs) in unit tests.
- Must not access private members (names starting with `_`) of the class under test directly in tests.
- Must place shared test helper functions and factory fixtures in the nearest `conftest.py` and reuse them across tests.
- Must annotate pytest fixture parameters with `MockerFixture` (from `pytest_mock`) and return types with `Callable[..., T]` (from `collections.abc`) when the fixture returns a factory function.
- Must not add comments outside test methods in `test_*.py` files; use `# --- section ---` only to separate logical groups of tests.
- Prefer shared fixtures in `conftest.py`.
- Prefer TDD workflow:
  - Must create or update `SPEC.md` in the relevant package directory before writing any code, listing scenarios, inputs, and expected outputs.
  - Must propose the full set of test cases (name + one-line intent + input summary + expected output summary) and wait for user confirmation before writing any code.
  - Must be ready to add, remove, or rename tests based on user feedback before proceeding.
  - Must write all failing tests first (red), then implement until all pass (green).
  - Must cover all distinct combinations; each test must state its scenario in the docstring.
  - Must update `SPEC.md` after all tests pass with the confirmed test case table (name + intent + input + expected output).

Tooling
- Must keep tooling rules aligned with repo config files (e.g., `pyproject.toml`).
- Formatting:
  - Must use Black.
- Linting:
  - Must use Pylint and address warnings.
- Type checking:
  - Must run mypy and prefer fixing types over ignoring errors.
- Coverage:
  - Must use pytest-cov and meet the coverage minimum defined in “Repo additions”.

Quality gates
- Must run tests first, then format/lint/type-check.
- Must run after changes; fix issues if below threshold:
  - Tests: `pytest tests/unit/` then `pytest tests/`
  - Coverage: `pytest --ignore=tests/integration --cov=. tests/ --cov-fail-under=80 --cov-report=html`
  - Format: `black $(git ls-files '*.py')`
  - Lint: `pylint $(git ls-files '*.py' ':!:tests/**')`
  - Types: `mypy .`
- If the repo defines special lint scopes (e.g., exclude `tests/`), must use the repo's canonical commands from “Repo additions”.

Common pitfalls to avoid
- Dependencies:
  - Must verify compatibility with the target runtime before adding.
  - Prefer testing imports locally before committing.
  - For untyped libraries, prefer explicit `# type: ignore[import-untyped]` on the import.
- Logging:
  - Must enforce the logging formatting rule; no workarounds.
- Cleanup:
  - Must remove unused variables/imports promptly.
  - Must not leave dead code.
- Stability:
  - Must not change externally-visible strings/outputs unless intentional and reviewed.

Learned rules
- Must keep contract-sensitive error messages stable; tests may assert exact strings.
- Must not change exit codes for existing failure scenarios.
- Must not change externally-visible output strings without updating the contract.

Repo additions
- Project name: living-doc-collector-ad
- Purpose: Python GitHub Action that collects “living documentation” data from Azure DevOps (e.g., Work Items, Boards, Pipelines) and writes machine-readable JSON for downstream documentation generation and analysis workflows.
- Runtime: Python 3.14+
- Logging rule:
  - Must use lazy `%` formatting (e.g., `logger.info("msg %s", value)`).
  - Must not use f-strings for logging interpolation.
- Imports:
  - Must place all Python imports at the top of the file (not inside functions/methods).
- Entry points:
  - `main.py`
- Inputs:
  - Via `INPUT_*` environment variables (see `action.yml`).
  - Key inputs: `INPUT_ADO_TOKEN`, `INPUT_WORK_ITEMS`, `INPUT_WORK_ITEMS_ORGANIZATIONS`, `INPUT_VERBOSE_LOGGING`.
- Outputs:
  - Must write under the repository's configured output folder (see code that uses `OUTPUT_PATH`).
  - Contract-sensitive output: action output `output-path`.
- Tooling commands (canonical):
  - Tests: `pytest tests/`
  - Format: `black $(git ls-files '*.py')`
  - Lint (exclude tests): `pylint $(git ls-files '*.py' ':!:tests/**')`
  - Types: `mypy .` (or `mypy <changed_files>`)
  - Coverage: `pytest --ignore=tests/integration --cov=. tests/ --cov-fail-under=80 --cov-report=html`
- Thresholds:
  - Pylint score: >= 9.5/10
  - Coverage: >= 80%
- Allowed exceptions to this template: none
