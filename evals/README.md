# Evaluation Pack

## 1. Specification evaluation

`python scripts/run_spec_eval.py` checks that the standalone production skill contains the behavioral controls required by the fixed regression cases. The suite is a specification / contract check; it does not execute Claude and therefore cannot establish runtime behavioral accuracy.

This is a deterministic repository-level check.

## 2. Runtime evaluation

A runtime evaluation must actually execute the fixed cases against the target Claude runtime and retain:

- exact prompt
- model identifier
- model/version date when available
- full output
- evaluator decision
- failure category
- regression disposition

A spec pass is never evidence of a runtime pass.

## Current regression coverage

The release contains 31 fixed specification cases plus hardened execution markers for mandatory module coverage, dependency / sensitivity reporting, red-team output, Value of Information, robustness, decision boundaries, and uncertainty structure.
