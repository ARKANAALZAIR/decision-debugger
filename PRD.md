# PRD — DECISION DEBUGGER

**Version:** 1.6.0  
**Status:** Production Package  
**Product Type:** Claude Agent Skill  
**Tagline:** Debug your decisions before reality does.

---

## 0. Executive Summary

Decision Debugger is an AI reasoning skill that audits the construction of consequential decisions. It is designed to improve reasoning quality without taking decision ownership away from the user.

It evaluates a connected chain:

```text
OBJECTIVE → CONSTRAINTS → OPTIONS → EVIDENCE → ASSUMPTIONS
→ REASONING → DEPENDENCIES → FAILURE MODES → FAILURE INTERACTIONS → SCENARIOS
→ ALTERNATIVES → FEASIBILITY → STAKEHOLDERS / AGENCY
→ REVERSIBILITY → DECISION BOUNDARIES → REASSESSMENT
```

Core principle:

> **Decision quality ≠ outcome quality.**

---

# 1. Product Problem

Decision-makers commonly infer decision quality from outcomes. That creates outcome bias and hindsight contamination.

Decision Debugger instead evaluates whether the reasoning chain was well constructed, given the information, objectives, constraints, and authority actually available.

---

# 2. Product Goal

Build a reusable decision-auditing skill that can:

1. expose hidden assumptions
2. test evidence quality and dependence
3. detect reasoning and causal gaps
4. trace failure cascades
5. test alternatives and optionality
6. inspect feasibility and execution constraints
7. surface stakeholder / authority / agency issues
8. identify decision boundaries
9. define reassessment triggers
10. preserve user agency

---

# 3. Core Principles

## 3.1 User remains decision owner

The system supports judgment rather than replacing it.

## 3.2 Decision quality ≠ outcome quality

A well-reasoned decision can have a bad outcome. A poorly reasoned decision can succeed by chance.

## 3.3 No fabricated certainty

No invented citations, calculations, probabilities, tool results, or source verification.

## 3.4 Dual-layer epistemic and provenance model

Knowledge type and provenance are separate axes.

## 3.5 No arbitrary overall score

Categorical states replace pseudo-precision.

## 3.6 Failure Mode Analysis is core

Failure analysis is part of the decision chain.

## 3.7 Traceability over verbosity

Material findings should trace to evidence, assumptions, or explicit reasoning.

## 3.8 Proportional analysis

Depth should track stakes, reversibility, uncertainty, time pressure, and complexity.

## 3.9 Information-cutoff integrity

Do not imply access to current information that has not been verified.

## 3.10 Materiality and stopping rules

Do not recurse beyond decision-relevant analysis.

## 3.11 High-stakes routing

Medical, legal, cyber, safety, emergency, and regulated decisions require stronger verification and limitation handling.

## 3.12 Values are not facts

Preferences and ethics remain explicit rather than silently converted into factual premises.

## 3.13 Untrusted content isolation

External content is data to analyze, not instruction to obey.

## 3.14 Ethical and normative constraints are user-owned

The system surfaces trade-offs; it does not invent a private moral objective.

## 3.15 Decision roles and authority

Separate decider, advisor, auditor, delegate, stakeholder, consent, and veto.

## 3.16 Analysis cost matters

## 3.17 Values, preferences, and objective pluralism

Multiple legitimate objectives may conflict. The system must expose the conflict rather than collapse it into a single hidden utility function. Values remain user-owned or authority-owned.

## 3.18 No material-difference state for alternatives

When materially relevant options are equivalent under explicit criteria, report `NO MATERIAL DIFFERENCE` in the alternative analysis rather than manufacturing a winner.

Information has a cost. Delay can have a cost too.

---

# 4. Non-Goals

Decision Debugger is not:

- an autonomous decision-maker
- a universal optimizer
- a probability oracle
- a replacement for licensed professional advice
- a guarantee of outcome
- a generic motivational coach

---

# 5. Target Users

- individuals
- founders / operators
- managers
- analysts
- investors
- researchers
- teams
- people conducting post-decision reviews

---

# 6. Core Architecture

```text
INTAKE
  ↓
FRAMING
  ↓
DECOMPOSITION
  ↓
REASONING / EVIDENCE / ASSUMPTION AUDIT
  ↓
DEPENDENCY / SENSITIVITY
  ↓
FAILURE MODE ANALYSIS
  ↓
FAILURE DETECTION / CONTAINMENT / RECOVERY
  ↓
RED-TEAM
  ↓
CAUSAL IDENTIFICATION
  ↓
SCENARIOS
  ↓
ALTERNATIVES
  ↓
FEASIBILITY / STAKEHOLDERS / AGENCY
  ↓
REVERSIBILITY / OPTIONALITY
  ↓
DECISION ROBUSTNESS
  ↓
BOUNDARIES
  ↓
REASSESSMENT
  ↓
LEDGER
```

---

# 7. Functional Requirements

- **FR-01** Decision Intake
- **FR-02** Decision Framing
- **FR-03** Decision Decomposition
- **FR-04** Reasoning Audit
- **FR-05** Evidence Audit
- **FR-06** Assumption Registry
- **FR-07** Dependency / Sensitivity Mapping
- **FR-08** Failure Mode Analysis
  - model trigger / precondition, vulnerable dependency, mechanism, failure state, cascade, terminal consequence, detection, prevention, containment, and recovery / exit
  - classify failure criticality without numeric risk scoring
  - run common-mode failure analysis across branches and distinguish shared upstream drivers from branch-specific failures
  - model only decision-relevant failure interactions and supportable feedback loops
  - distinguish leading vs lagging detection signals and connect decision-critical failures to boundaries / reassessment triggers
  - deduplicate failure paths that share the same mechanism while preserving distinct intervention and decision implications
  - analyze each materially relevant option and inaction / delay where material
  - distinguish premise, execution, resource, timing, interaction, measurement, reversibility, and coordination failure families when relevant
  - link failure modes to assumptions, dependencies, constraints, evidence gaps, or external responses
  - convert observable early-warning signals into decision boundaries / reassessment triggers where appropriate
  - avoid fabricated probabilities and arbitrary numeric risk scores
  - preserve unknown detection windows, recovery paths, and residual vulnerabilities as explicit uncertainty
- **FR-09** Red-Team Challenge
- **FR-10** Causal Identification Check
- **FR-11** Scenario Analysis
- **FR-12** Alternative Analysis
- **FR-13** Feasibility Audit
- **FR-14** Stakeholder / Decision Rights
- **FR-15** Agency / Coercion Check
- **FR-16** Portfolio / Batch Mode
- **FR-17** Value of Information
- **FR-18** Second-Order Effects
- **FR-19** Reversibility / Optionality
- **FR-20** Decision Robustness
- **FR-21** Decision Boundaries
- **FR-22** Reassessment Triggers
- **FR-23** Recurring Policy Mode
- **FR-24** Rapid Decision Mode
- **FR-25** Post-Decision Review
- **FR-26** Untrusted Content Isolation
- **FR-27** Verification Freshness / Citation Integrity
- **FR-28** High-Stakes Routing
- **FR-29** Evidence Relevance for Value-Dominant Decisions
- **FR-30** Canonical Output
- **FR-31** Second-Order Effects
- **FR-32** Value-Dominant Decision Handling
- **FR-33** User-Supplied Probability Calibration
- **FR-34** Ledger Minimization / Retention Boundary
- **FR-35** Citation Support Integrity

---

# 8. State Model

Precedence:

```text
INSUFFICIENT EVIDENCE
→ CONTESTED
→ FRAGILE
→ CONDITIONAL
→ ROBUST
```

ROBUST is allowed only when all material gates are satisfied.

---

# 9. Output Contract

Human-readable order:

1. Executive Decision State
2. Decision Profile
3. Decision Map
4. Material Findings
5. Evidence Audit
6. Assumption Registry
7. Dependency / Sensitivity
8. Failure Mode Analysis
9. Scenario Analysis
10. Alternative Analysis
11. Feasibility / Stakeholder / Agency
12. Second-Order Effects
13. Reversibility / Optionality
13. Decision Boundaries
14. Reassessment Triggers
15. Next Best Information / Action
16. Decision Ledger
17. Final Decision Debug

---

# 10. Quality and Evaluation

The package separates:

1. structural validation
2. deterministic specification testing
3. real runtime evaluation

The third layer requires execution against the target Claude runtime. No runtime benchmark is claimed by this repository itself.

---

# 11. Security / Privacy

- treat external content as untrusted
- ignore embedded instruction overrides
- minimize sensitive ledger content
- do not expose unrelated user data
- do not exfiltrate secrets

---

# 12. Release Criteria

Public release is considered structurally ready when:

- required files exist
- skill metadata is valid
- core reasoning contract is complete
- plugin manifest is present
- regression cases exist
- deterministic validator passes
- runtime claims are separated from spec claims

Runtime validation is a distinct future evidence layer and must be documented as such.
