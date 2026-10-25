# Production Readiness — Decision Debugger v1.10.0

Classification: CODE/CONTRACT HARDENED — RUNTIME RELEASE BLOCKED

## Local evidence

- Repository, frontmatter, output-schema, and package checks: see `scripts/validate.py`.
- Legacy structural markers: 62/62 pass; these are supplementary specification checks, not runtime behavior evidence.
- Calibration evaluator unit suite: 14 tests pass against controlled evaluator fixtures.
- Captured-output evaluation: not run because no target-runtime captures are available.
- Target runtime: not invoked. The Claude CLI is unavailable in the current environment.

The package contains `scripts/calibration_eval.py` for actual captured responses. A release-runtime claim requires all ten target-runtime scenarios, their exact prompts, runtime metadata, raw responses, parsed outputs, and passing scenario checks. The locally generated evaluator fixtures do not satisfy that gate.
