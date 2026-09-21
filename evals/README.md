# Evaluation Pack

The evaluation pack has two intentionally separate layers.

## 1. Specification evaluation

`python scripts/run_spec_eval.py` checks that the production skill contains the behavioral controls required by the fixed regression cases. The suite is a specification/contract check; it does not execute the language model and therefore cannot establish runtime behavioral accuracy.

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

The release contains 25 fixed specification cases covering framing, evidence, causal reasoning, hindsight, authority, agency, portfolio linkage, alternatives, high-stakes routing, probability handling, equivalence, conflicts, reversibility, recurring policy, prompt-injection isolation, second-order effects, value-dominant decisions, firsthand evidence, privacy, reference classes, and citation integrity.
