# Failure Mode Analysis

Failure Mode Analysis is the decision's failure-engine. It explains how an option can break, how the break propagates, how early it can be detected, and whether it can still be contained or reversed.

## Canonical path

```text
OPTION / ACTION
↓
TRIGGER / PRECONDITION
↓
VULNERABLE DEPENDENCY
↓
FAILURE MECHANISM
↓
FAILURE STATE
↓
DIRECT EFFECT
↓
CASCADE / FEEDBACK
↓
TERMINAL CONSEQUENCE
↓
DETECTION SIGNAL + WINDOW
↓
PREVENT
↓
CONTAIN
↓
RECOVER / EXIT
↓
RESIDUAL VULNERABILITY
```

## Failure-mode families

Use only the families that matter:

- `PREMISE FAILURE`
- `EXECUTION FAILURE`
- `RESOURCE / CONSTRAINT FAILURE`
- `TIMING / SEQUENCING FAILURE`
- `RESPONSE / INTERACTION FAILURE`
- `MEASUREMENT / FEEDBACK FAILURE`
- `REVERSIBILITY / RECOVERY FAILURE`
- `COORDINATION / AUTHORITY FAILURE`

## Required fields

Every material failure mode should identify:

```text
ID
OPTION / BRANCH
FAMILY
TRIGGER / PRECONDITION
VULNERABLE DEPENDENCY
FAILURE MECHANISM
FAILURE STATE
DIRECT EFFECT
CASCADE
TERMINAL CONSEQUENCE
DETECTION SIGNAL
DETECTION WINDOW (if supportable)
PREVENTION
CONTAINMENT
RECOVERY / EXIT
RESIDUAL VULNERABILITY
DECISION RELEVANCE
EVIDENCE / PROVENANCE
```

Use `UNKNOWN` instead of inventing missing mechanics, timing, probabilities, recovery paths, or thresholds.

## Symmetry rule

Analyze materially relevant failure modes for each live option, plus inaction / delay where material. Ask:

- how can this option fail?
- how can the alternative fail?
- how can waiting fail?
- which failure is hardest to detect?
- which is hardest to contain or recover from?
- which destroys the most optionality?

Do not treat inaction as a risk-free baseline.

## Upstream linkage

Every material failure mode should trace to one or more of:

```text
ASSUMPTION
DEPENDENCY
CONSTRAINT
EVIDENCE GAP
STAKEHOLDER / EXTERNAL RESPONSE
```

Every high-sensitivity assumption should be checked for a concrete failure path unless it is explicitly marked not material.

## Early warning → decision trigger

When a detectable warning exists, express it as:

```text
WARNING SIGNAL
→ CONDITION
→ INTERPRETATION
→ IMPLICATION / REASSESSMENT
```

Monitoring is not mitigation unless the observed signal has a defined decision consequence.

## Mitigation types

Keep these distinct:

- `PREVENT`: reduce exposure before the trigger;
- `CONTAIN`: limit damage once the failure begins;
- `RECOVER / EXIT`: repair, reverse, stage, abandon, or preserve optionality.

A failure mode may have one, several, or none of these. Do not invent a recovery path that the option does not actually permit.

## Qualitative stress dimensions

Avoid numeric risk scores and fabricated probabilities. Use:

- `DECISION-CHANGING`: YES / NO / UNKNOWN
- `DETECTABILITY`: EARLY / MID-COURSE / LATE / UNKNOWN
- `RECOVERABILITY`: HIGH / MODERATE / LOW / UNKNOWN
- `OPTIONALITY IMPACT`: PRESERVED / REDUCED / LOST / UNKNOWN

A material failure is especially important when it is hard to detect, hard to recover from, or destroys optionality.

## Quality bar

A useful failure mode explains the mechanism, not merely the label. Avoid statements like `execution risk`, `market risk`, or `things may go wrong` unless they are decomposed into an actual trigger → mechanism → consequence chain.

Stop when additional cascade steps no longer change the decision, the evidence ceiling is reached, or the extra decomposition only repeats an existing mechanism.
