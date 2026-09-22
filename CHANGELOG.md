# Changelog

## 1.5.0 — Failure Mode Engine Hardening

### Added
- upgraded Failure Mode Analysis from a short cascade list into a structured failure-engine
- added trigger / precondition → vulnerable dependency → mechanism → failure state → cascade → detection → prevention → containment → recovery / exit → residual vulnerability
- added failure-mode families covering premise, execution, resource, timing, interaction, measurement, reversibility, and coordination failures
- added symmetry testing across action, alternative, and inaction / delay when material
- added explicit early-warning → decision-boundary / reassessment linkage
- added qualitative detectability, recoverability, and optionality-impact fields without numeric risk scoring
- added regression cases for FMA depth, symmetry, uncertainty, detection, and upstream linkage

### Fixed / strengthened
- prevents generic labels such as “execution risk” from qualifying as complete failure analysis
- separates prevent, contain, and recover / exit actions
- requires material failure modes to trace upstream to assumptions, dependencies, constraints, evidence gaps, or external responses
- makes unsupported detection windows, probabilities, recovery paths, and thresholds explicit as UNKNOWN rather than inferred


## 1.4.2 — Runtime Execution Hardening

### Fixed / strengthened
- added a mandatory execution gate so core modules are executed or explicitly marked not material / not applicable
- strengthened dependency and sensitivity reporting with qualitative sensitivity ranking
- made red-team output explicit with attack / target / defeat condition / status
- strengthened Value of Information into a ranked qualitative priority with acquisition and delay costs
- made reversibility / optionality output explicit
- added deterministic robustness stress-testing and robustness / fragility conditions
- added structured decision-boundary format: condition → interpretation → implication
- added an explicit uncertainty structure in the output contract
- added a final integrity check preventing silent omission of core modules
- aligned the evaluation harness with the standalone universal skill package


## 1.4.1 — Production Hardened

### Fixed / strengthened
- replaced minimal examples with full Decision Debugger example outputs
- removed remaining Financial Debugger-style example ambiguity
- added explicit second-order-effect analysis and output field
- added value-dominant decision handling and objective pluralism
- added `NO MATERIAL DIFFERENCE` alternative relationship
- added user-supplied probability handling and calibration boundary
- added firsthand / lived-experience evidence scope rules
- added base-rate / reference-class reasoning guidance
- strengthened decision-ledger minimization and retention boundaries
- strengthened citation support integrity requirements
- expanded deterministic specification regression cases from 16 to 25
- expanded canonical output reference and schema

## 1.4.0 — Production Package

### Added
- canonical root `SKILL.md`
- Claude Code plugin wrapper
- skill copy under `skills/decision-debugger/`
- slash-command wrapper
- decision framework references
- evidence audit reference
- failure-mode reference
- causal-analysis reference
- stakeholder / agency reference
- output schema reference
- rapid / deep / postmortem templates
- career / business / investment examples
- behavioral regression suite
- deterministic specification evaluator
- structural validator
- release quality gates

### Hardened
- epistemic status vs provenance
- decision-state precedence
- ROBUST admission gates
- decision-changing test
- evidence lineage and dependence
- causal identification
- stakeholder authority / consent
- agency / coercion
- portfolio linkage
- reversibility / optionality
- value of information
- hindsight protection
- untrusted-content isolation
- high-stakes routing
- recurring policy mode
- machine-readable output

### Validation policy
This release deliberately does not claim a runtime Claude benchmark. Any future runtime result must include reproducible execution evidence.
