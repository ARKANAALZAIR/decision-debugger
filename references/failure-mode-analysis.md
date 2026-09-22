# Failure Mode Analysis

Failure Mode Analysis is the decision's failure-engine. It explains how a branch can break, what dependency breaks, how failure propagates, how early it can be detected, which control barrier applies, how recovery works, and whether the failure changes the decision.

## Canonical architecture

```text
OPTION / BRANCH
↓
FAMILY + FAILURE CRITICALITY
↓
TRIGGER / PRECONDITION
↓
UPSTREAM LINK
↓
VULNERABLE DEPENDENCY
↓
FAILURE MECHANISM
↓
FAILURE STATE
↓
DIRECT EFFECT
↓
CASCADE
↓
INTERACTION / COMMON-MODE DRIVER / FEEDBACK LOOP (if material)
↓
TERMINAL CONSEQUENCE
↓
DETECTION SIGNAL + SIGNAL TYPE + WINDOW
↓
PREVENTION
↓
CONTAINMENT
↓
RECOVERY / EXIT
↓
RESIDUAL VULNERABILITY
↓
DECISION BOUNDARY / REASSESSMENT TRIGGER (if supportable)
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

## Failure criticality

Use qualitative labels when supportable:

- `DECISION-CRITICAL`
- `DECISION-RELEVANT`
- `MONITOR-ONLY`
- `NON-MATERIAL`

These are descriptive materiality labels, not risk scores.

## Required fields

Every material failure mode should identify:

```text
ID
OPTION / BRANCH
FAMILY
FAILURE CRITICALITY
TRIGGER / PRECONDITION
UPSTREAM LINK(S)
VULNERABLE DEPENDENCY
FAILURE MECHANISM
FAILURE STATE
DIRECT EFFECT
CASCADE
COMMON-MODE DRIVER (if any)
INTERACTIONS (if any)
FEEDBACK LOOP (if any)
TERMINAL CONSEQUENCE
DETECTION SIGNAL
SIGNAL TYPE: LEADING / LAGGING / UNKNOWN
DETECTION WINDOW (if supportable)
PREVENTION
CONTAINMENT
RECOVERY / EXIT
RESIDUAL VULNERABILITY
DECISION RELEVANCE
DECISION-CHANGING
DETECTABILITY
RECOVERABILITY
OPTIONALITY IMPACT
DECISION BOUNDARY / REASSESSMENT TRIGGER (if supportable)
EVIDENCE / PROVENANCE
```

Use `UNKNOWN` instead of inventing missing mechanisms, thresholds, timing, probabilities, or recovery paths.

## Symmetry rule

Analyze materially relevant failure modes for each live option, plus inaction / delay where material. Ask:

- how can this branch fail?
- how can the alternative fail?
- how can waiting fail?
- which failure is hardest to detect?
- which is hardest to contain?
- which is hardest to recover from?
- which destroys the most optionality?
- are any failure drivers shared across branches?

Do not treat inaction as a risk-free baseline.

## Common-mode analysis

After branch-specific FMA, map shared upstream drivers:

```text
BRANCH A ──┐
BRANCH B ──┼──> COMMON FAILURE DRIVER
INACTION ──┘
```

A common-mode driver is one assumption, dependency, constraint, or external response that can impair multiple branches. This prevents false diversification across superficially different options.

## Failure interactions

Use only materially supported interactions:

- `CASCADING`: A directly triggers B;
- `AMPLIFICATION`: A increases the magnitude or speed of B;
- `MASKING`: A hides B and delays detection;
- `COMPENSATING`: A offsets B;
- `COMMON-MODE`: multiple branches are impaired by the same driver;
- `FEEDBACK`: an effect changes an upstream cause.

For feedback loops, identify the participating failure modes, direction, reinforcing vs balancing character, activation signal, and practical intervention point. Do not assert a loop merely because two events are correlated.

## Deduplication rule

Merge failure modes when they share the same trigger, mechanism, and material consequence. Keep them separate when intervention point, detection path, or decision implication differs materially. Use interaction links rather than copying the same common-mode driver into every branch.

## Assumption-to-failure linkage

Every material failure mode should trace to one or more of:

```text
ASSUMPTION
DEPENDENCY
CONSTRAINT
EVIDENCE GAP
STAKEHOLDER / EXTERNAL RESPONSE
```

If the parent is inferred rather than established, label it `INFERRED` or `UNKNOWN`.

Every high-sensitivity assumption should be checked for a concrete failure path unless explicitly `NOT MATERIAL`.

## Early warning → decision trigger

When a detectable warning exists, express it as:

```text
WARNING SIGNAL
→ CONDITION
→ INTERPRETATION
→ IMPLICATION / REASSESSMENT
```

Also state whether the signal is `LEADING`, `LAGGING`, or `UNKNOWN`. Monitoring is not mitigation unless the signal has a defined decision consequence.

## Barrier model

Keep controls distinct:

- `PREVENT`: reduce exposure before trigger;
- `CONTAIN`: limit damage after failure begins;
- `RECOVER / EXIT`: repair, reverse, stage, abandon, or preserve optionality.

Ask which barrier is missing, weak, or unsupported. Do not invent a recovery path the branch cannot actually perform.

## Qualitative stress dimensions

Avoid numeric risk scores and fabricated probabilities. Use:

- `DECISION-CHANGING`: YES / NO / UNKNOWN
- `DETECTABILITY`: EARLY / MID-COURSE / LATE / UNKNOWN
- `RECOVERABILITY`: HIGH / MODERATE / LOW / UNKNOWN
- `OPTIONALITY IMPACT`: PRESERVED / REDUCED / LOST / UNKNOWN

A failure with low detectability, low recoverability, and high optionality loss deserves explicit attention without needing a probability.

## Decision-boundary linkage

Material failure signals should become decision boundaries or reassessment triggers when supportable:

```text
FAILURE SIGNAL
→ CONDITION
→ INTERPRETATION
→ IMPLICATION
```

Do not fabricate thresholds.

## Stopping rule

Stop when additional decomposition no longer changes the decision, a decision condition, detection/control point, or optionality. Do not recurse into every imaginable downstream event.
