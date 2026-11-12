# .github

Parent: [../CONTEXT.md](../CONTEXT.md)

## Purpose

CI workflows, pull request checks, issue and pull request templates, Dependabot configuration.

## Conventions

- Pin every action to a full commit SHA, with its version in a trailing comment.
- Quality jobs run `make install`, then a `Makefile` target, never the raw tool: `test.yml` runs `format-check`,
  `lint`, `types` and `coverage` on Python 3.10–3.14.
- A CI change must not change the action's outputs or exit codes.
- Never print a secret or token in a workflow step.
- The release-notes configuration is the same in every `living-doc*` repository (AbsaOSS/living-doc#97):
  `release_draft.yml`'s `release-notes-title` and `chapters` through `row-format-link-pr`,
  `check_pr_release_notes.yml`'s `skip-labels`, and both workflows' `permissions:`. Change it in all of them together
  → [what it covers and how the generator sorts](https://github.com/AbsaOSS/living-doc/blob/master/.github/CONTEXT.md)

## Pull request checks

- `check-pr-requirements.yml`: issue number in the title and the branch name, the `## Overview`, `## Release Notes`
  and `## Related` sections, a closing issue reference, target `master`, `support/*` or `release/*`. The rules for
  people are in `CONTRIBUTING.md`. Skipped on pull requests Dependabot opened (by the pull request's author, not
  `github.actor`).
- `check_pr_release_notes.yml`: a `## Release Notes` section; the labels `no RN` and `pr:no-release-notes` skip it.
- `link-check.yml`: lychee over the Markdown files.
- A pull request opened with `GITHUB_TOKEN` (for example by `agd-update.yml`) starts no workflows: edit it, or close
  and reopen it, to run the checks.

## Other workflows

- `test.yml`: the quality gate above, skipped when no Python-related file changed.
- `agd-update.yml`: every Monday, `agd update`; when an update is due, it opens a `chore/<n>-agd-update` pull request.
- `release_draft.yml`: manual release draft (`DEVELOPER.md` § Releasing).
- `aquasec-night-scan.yml`: nightly security scan.
