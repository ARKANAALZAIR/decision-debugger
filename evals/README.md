# Evaluation Pack

## 1. Specification evaluation

`python3 -B scripts/run_spec_eval.py --offline-only` runs the standalone skill's structural checks and the captured-output evaluator's own unit tests. The 62 legacy cases remain marker-based specification checks; they are supplementary and do not establish runtime behavior.

The local suite validates deterministic output contracts and evaluator behavior. It does not invoke Claude or establish that a model followed the skill.

## 2. Captured-output evaluation

Run `python3 -B scripts/run_spec_eval.py --captures PATH` after executing all ten calibration scenarios against the target runtime. Each `<case-id>.json` file must preserve:

- `case_id`
- exact prompt, including the evaluator's JSON-output suffix
- runtime, model identifier, and capture timestamp in `metadata`
- full unedited response in `raw_output`
- parsed structured response in `output`, byte-for-byte semantically equal to the JSON block in `raw_output`

The capture evaluator checks the canonical output schema and scenario-specific invariants. Missing captures return `BLOCKED`; malformed or behaviorally incorrect captures fail. Local metadata is not independently authenticated, so retain the runtime's original capture artifacts alongside these files.

`python3 -B scripts/run_spec_eval.py` without arguments runs offline checks, then exits `2` with an explicit target-runtime block. Use `--offline-only` when only local checks are intended.

## 3. Runtime evaluation

A runtime evaluation must execute the fixed cases against the target Claude runtime. A structural or evaluator-unit-test pass is never evidence of a runtime pass.

## Current regression coverage

The release contains 62 fixed specification cases plus hardened execution markers for mandatory module coverage, dependency / sensitivity reporting, red-team output, Value of Information, robustness, decision boundaries, and uncertainty structure.


The FMA suite additionally checks common-mode drivers, material failure interactions, supportable feedback loops, qualitative criticality, leading/lagging detection signals, barrier analysis, and deduplication.


The 1.9.1 hardening suite additionally checks automatic execution, proportionality for everyday decisions, module status semantics, primary/related finding ownership, status/finding reconciliation, NOT APPLICABLE semantics, synthesis completion status, audit-integrity reconciliation, material-input gaps, and FMA barrier coverage.

The 1.10.0 suite covers complete pre-decision records, locked-record preservation, both outcome-bias directions, numeric forecast comparisons, cross-decision patterns, insufficient metric data, missing original forecasts, invalidated assumptions, and protection against later-information leakage. Its captured-output checks are runtime-gated; evaluator unit fixtures do not count as model behavior.
