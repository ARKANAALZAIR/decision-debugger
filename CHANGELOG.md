## 1.9.0 — Canonical Trigger & UX Contract Hardening

### Added
- canonical one-line trigger: `Jalankan Decision Debugger.`
- explicit contract that a supplied decision can be fully audited without a complex prompt or module names
- canonical trigger support for attached decision artifacts
- regression cases for the canonical trigger and artifact workflow

### Fixed / strengthened
- removes ambiguity around whether users must know the internal module names
- keeps natural-language aliases (`Debug this.`, `Debug this decision.`, `Audit this.`, `Stress-test this decision.`) mapped to STANDARD
- aligns README, command wrapper, core SKILL, PRD, tests, and release metadata

## 1.7.0 — Decision Audit Contract Hardening

### Added
- automatic STANDARD execution for natural prompts such as “Debug this decision.”
- explicit diagnostic vs synthesis / control module classes
- canonical module status taxonomy: ERROR FOUND, ERROR NOT FOUND, NOT ASSESSABLE, NOT APPLICABLE, COMPLETED
- Module Execution Matrix for every STANDARD, DEEP, and POST-MORTEM report
- one-primary-owner finding model with Related Modules to prevent duplicate findings
- final Audit Integrity Check for module coverage, status / finding reconciliation, applicability, and human / machine parity
- proportionality rules for simple everyday low-stakes decisions
- FMA barrier coverage and weakest-barrier reporting
- ten new specification cases and expanded behavioral regression coverage

### Fixed / strengthened
- prevents synthesis modules from being labelled FOUND merely because they reference related findings
- prevents detectors with only related findings from claiming ERROR FOUND
- makes missing material inputs visible as findings or assessability blockers rather than ERROR NOT FOUND
- makes NOT APPLICABLE distinct from ERROR NOT FOUND
- makes FMA controls auditable as prevention → containment → recovery rather than a single mitigation bucket

## 1.6.0 — Full Failure Mode Analysis Upgrade

### Added
- common-mode failure analysis across action, alternative, and inaction branches
- material failure interactions: cascading, amplification, masking, compensating, common-mode, and feedback
- supportable feedback-loop mapping with activation signal and intervention point
- qualitative failure criticality classes without numeric risk scoring
- leading vs lagging detection signal typing
- barrier analysis across prevention, containment, and recovery / exit
- failure-path deduplication rules to prevent combinatorial explosion
- canonical decision-boundary linkage for decision-critical failures
- synchronized human-readable examples and machine-readable failure-mode schema
- regression/specification cases for common-mode drivers, interactions, loops, criticality, barriers, and signal typing

### Fixed / strengthened
- aligned examples with the canonical FMA engine rather than the legacy short cascade format
- prevents superficial branch diversity from being mistaken for independent protection against a shared failure driver
- prevents correlation from being mislabeled as a feedback loop
- prevents duplicate failure paths from bloating the analysis
- separates monitoring signals from actual prevention / containment / recovery controls

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
