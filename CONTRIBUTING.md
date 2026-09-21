# Contributing to Decision Debugger

## Contribution standard

Every meaningful behavioral change should have a concrete reason and, where practical, a regression case.

## Preferred workflow

1. Identify a concrete failure mode.
2. Create a deterministic test case.
3. Update the skill rule or reference that should prevent the failure.
4. Update examples if the change affects user-facing behavior.
5. Run `python scripts/validate.py`.
6. Run `python scripts/run_spec_eval.py`.

## Good contributions

- stronger evidence dependence detection
- better causal identification
- clearer state precedence
- safer high-stakes routing
- stronger hindsight protection
- better agency / authority handling
- better failure-cascade tracing
- improved machine-readable output
- adversarial test cases

## Avoid

- arbitrary 0–100 scores
- hidden recommendations
- fabricated certainty
- unverified benchmark claims
- model-specific hacks that break the conceptual contract
