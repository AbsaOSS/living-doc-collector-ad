# Rule: docs lifecycle — specs shrink as code ships

A prospective spec (a `SPEC.md`, a mode design doc, a "planned" section) describes what does
**not** exist yet. Once a section is implemented, that section stops being a spec and
becomes a fact about the codebase — so it belongs in the live docs, not in the spec.

## The rule

When a PR implements a prospective-spec section, that same PR must:

1. **Delete** the implemented content from the spec (the whole section, or the specific
   subsections that are now shipped).
2. **Add** the equivalent, "what actually exists" description to the live docs:
   - `README.md` for user-facing usage and examples;
   - the mode doc for mode-specific behavior — e.g. a future `work_items/README.md` (and
     `boards/README.md`, `pipelines/README.md`, `test_plans/README.md`,
     `release_notes/README.md` as those modes are built);
   - `DEVELOPER.md` for local-dev workflow.

This is a **move**, not a copy. After the PR, the information exists in exactly one place —
the live docs — and the spec is smaller. The spec trends toward empty as the modes ship.

## What "move" means

- Do not leave the section in the spec with a "✅ implemented" marker. Remove it.
- Do not duplicate the schema/flow/table in both the spec and the mode doc. One home.
- If only part of a section shipped, split it: the shipped part moves to live docs, the
  unshipped part stays in the spec.
- Cross-references that pointed at the moved spec section must be repointed to its new
  home in the same PR (keep `link-check` green).

## When the spec is empty

When a spec document has no remaining unimplemented content, delete the file (or reduce it
to a one-line pointer to the live docs). A spec with nothing prospective in it is drift
waiting to happen.
