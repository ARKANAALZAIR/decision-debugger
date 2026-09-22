# Decision Debugger

> **Debug your decisions before reality does.**

Decision Debugger is a Claude Agent Skill that audits decision-making as a connected reasoning system rather than simply telling you what to choose. It traces the chain from objectives, constraints, options, evidence, and assumptions through reasoning, dependencies, failure modes, alternatives, feasibility, reversibility, and the conditions that should trigger reassessment.

## What it detects

- Unclear or conflicting objectives
- Inconsistent or hidden constraints
- Incomplete option sets
- Weak or unsupported evidence
- Dependent or duplicated evidence
- Stale or unverified claims
- Hidden and interacting assumptions
- Causal-identification gaps
- Reasoning leaps and false precision
- Dependency and sensitivity vulnerabilities
- Material second-order effects and feedback loops
- Failure Mode Analysis with trigger → mechanism → cascade → detection → prevention → containment → recovery
- Missing alternatives, including inaction, delay, pilots, and reversible paths
- Execution and feasibility problems
- Stakeholder and decision-rights conflicts
- Agency, coercion, consent, and dependency issues
- Portfolio concentration and common dependencies
- Uncertainty treated as certainty
- User-supplied probability estimates treated as verified probabilities
- Missing decision boundaries
- Missing reassessment triggers
- Value or preference criteria silently treated as objective facts
- Hindsight contamination

## Why it exists

A decision is not just a conclusion. It is a connected chain:

`OBJECTIVE → CONSTRAINTS → OPTIONS → EVIDENCE → ASSUMPTIONS → REASONING → FAILURE MODES → ALTERNATIVES → EXECUTION → DECISION`

A weak link can make an apparently reasonable decision fragile. Decision Debugger makes those dependencies explicit before the decision is executed, while keeping the final decision with the user.

A good outcome does not automatically prove that the reasoning was good, and a bad outcome does not automatically prove that the reasoning was bad. For post-mortems, the skill separates information available at decision time from information learned later.

## Signature feature: Decision-Chain Stress Testing

Example request:

> I am considering leaving my job to build a startup full-time. My runway is 12 months and I expect to validate revenue within six months. Debug the decision.

The skill decomposes the decision into objectives, constraints, options, assumptions, evidence, and dependencies; tests the reasoning; traces failure paths; compares alternatives; checks feasibility and reversibility; and identifies the conditions that should change the decision later.

It does not make the decision for the user.

## Modes

| Mode | Purpose |
|---|---|
| RAPID | Time-constrained audit of material vulnerabilities |
| STANDARD | Full default audit |
| DEEP | Comprehensive stress test for high-stakes or complex decisions |
| POST-MORTEM | Review using the decision-time information set |

## Decision States

```text
INSUFFICIENT EVIDENCE
→ CONTESTED
→ FRAGILE
→ CONDITIONAL
→ ROBUST
```

`ROBUST` is gated. It is not a guarantee, an optimality claim, or a success probability.

There is intentionally no arbitrary overall 0–100 score.

## Example output

The following is illustrative only and uses hypothetical inputs. It demonstrates categorical diagnosis rather than an arbitrary overall score.

```text
DECISION DEBUGGER REPORT

Decision State: CONDITIONAL
Assessment Confidence: MODERATE

Primary Vulnerability:
The decision depends heavily on an unverified assumption about
how quickly the new business can reach sufficient revenue.

Decision-Changing Finding:
If the revenue validation timeline extends materially beyond
the available runway, the current decision structure changes.

DECISION PROFILE
Decision:
Should I leave my current job to build a startup full-time?
Objective:
Build the startup while maintaining sufficient financial security.
Key Constraints:
- 12 months personal runway
- No external funding yet
- Full-time commitment required for the current growth plan
Options:
A. Leave job and build full-time
B. Keep job and build part-time
C. Delay the transition
D. Run a defined pilot before leaving

MATERIAL FINDINGS
[DECISION-CHANGING] #001
Severity: HIGH
Type: ASSUMPTION
Location: Revenue validation
Problem:
The six-month revenue target is treated as a planning assumption,
but the evidence supporting that timeline is weak.
Impact:
A materially longer validation period could compress the available
runway and force a different decision before the business reaches
the intended milestone.
Recommended Action:
Validate the revenue timeline against comparable evidence and
construct a downside runway scenario.

FAILURE MODE ANALYSIS
Family: RESOURCE / CONSTRAINT FAILURE
Trigger:
Revenue validation takes substantially longer than planned.
↓
Vulnerable Dependency:
Runway planning depends on the six-month validation assumption.
↓
Failure Mechanism:
Revenue stays below the level needed to maintain the original runway.
↓
Failure State:
The available financial buffer becomes materially shorter than planned.
↓
Cascade:
Cash pressure → short-term optimization → scope changes
→ execution focus decreases → validation slows further.
↓
Detection Signal:
Burn rate or validation progress diverges from the operating plan.
↓
Prevention:
Validate the timeline and model explicit downside runway conditions.
Containment:
Use predefined evidence-based conditions to reduce spend or alter scope.
Recovery / Exit:
Preserve the option to return to income, reduce burn, or stage the transition.
Residual Vulnerability:
The true validation timeline remains uncertain.

ALTERNATIVE ANALYSIS
Option A — Full-time transition
Higher commitment, lower available income.
Option B — Part-time build
Lower execution capacity, longer validation window.
Option C — Delay
Preserves optionality but delays full-time execution.
Option D — Pilot
Creates additional information before an irreversible transition.

DECISION BOUNDARIES
The current reasoning should be reassessed if:
- actual monthly burn materially exceeds the estimate
- validation takes substantially longer than planned
- runway falls below the minimum required buffer
- new evidence materially changes the revenue assumption

FINAL DECISION DEBUG
What is sound:
The objective and major constraints are identifiable.
What is fragile:
The decision relies heavily on the revenue validation timeline.
What is unresolved:
The evidence supporting that timeline is insufficient.
What would change the decision:
Verified evidence showing materially different validation
requirements or runway.
What should be monitored:
Cash burn, validation progress, runway, and evidence supporting
the revenue assumptions.
```

## Installation

### Claude.ai

This package is a standalone Agent Skill with exactly one `SKILL.md` at the skill directory root. Zip the `decision-debugger/` folder so it is the single top-level entry in the ZIP, then upload it through the applicable **Customize → Skills → Create/Upload** flow in Claude.

### Claude Code

For a project skill, place the repository's `SKILL.md` in:

```text
.claude/skills/decision-debugger/SKILL.md
```

For a personal skill, use:

```text
~/.claude/skills/decision-debugger/SKILL.md
```

You can copy the same `SKILL.md` from this repository into that path; the repository contains a helper installer at `scripts/install_claude_code.sh`.

### API / other Agent Skills-compatible runtimes

Preserve the standalone skill directory with `SKILL.md` at its root and follow the host runtime's current registration or upload mechanism.

## Usage

Make the decision context available, then ask naturally:

- `Debug this decision.`
- `Find only decision-changing issues.`
- `Stress-test my assumptions.`
- `Run a deep decision audit.`
- `Analyze how this decision could fail.`
- `Compare my alternatives, including doing nothing.`
- `What would change this decision later?`
- `Run a post-mortem using only information available at the time.`

For deeper analysis, provide:

- decision
- objective
- constraints
- options
- evidence
- assumptions
- relevant stakeholders
- timing or deadlines
- reversibility or switching costs

The skill can work with incomplete information, but it reports which checks are blocked by missing, ambiguous, stale, or unverified inputs rather than silently filling the gaps.

## Supported decision contexts

Designed to work with, when the environment can read them:

- Career and education decisions
- Business and operational decisions
- Investment and financial decisions
- Product and project decisions
- Hiring and team decisions
- Vendor and partnership decisions
- Personal planning and major life decisions
- Strategic and recurring policy decisions
- Decision logs and post-mortems
- Documents, spreadsheets, notes, screenshots, and supplied text relevant to the decision

The skill is domain-agnostic. Domain-specific evidence and professional advice may still be required for high-stakes decisions.

## Reliability philosophy

Decision Debugger is optimized for **high-signal decision auditing**, not maximum comment volume. A finding should be grounded in evidence and tied to a potentially material consequence.

The system is designed to:

- distinguish evidence from assertion
- distinguish decision quality from outcome quality
- search for disconfirming evidence and alternative explanations
- expose interacting assumptions and dependencies
- stress-test failure paths and second-order effects
- compare meaningful alternatives, including inaction and delay
- surface uncertainty instead of manufacturing precision
- preserve user agency and decision ownership
- stop when additional work is unlikely to materially change the diagnosis

Static repository validation is a packaging/specification check, not proof of runtime model accuracy. Real-world evaluation should include adversarial cases and human review.

## Decision integrity

The skill will not fabricate citations, tool results, probabilities, evidence, or facts. It should not turn incomplete information into false certainty.

For past decisions, it uses **Information-Set Lock**: evaluate the original reasoning using information reasonably available at the decision time, then analyze the outcome separately.

The skill also keeps values and preferences distinct from empirical claims. A value-based trade-off is not silently converted into an objective fact.

## Limitations

- It cannot guarantee that a decision will succeed.
- It is not an automatic decision-maker or prediction engine.
- Decision analysis depends on the quality and completeness of the supplied evidence.
- High-stakes legal, medical, financial, safety, or other specialist decisions may require qualified professional advice.
- Stakeholder consent, authority, and organizational context may require information unavailable to the skill.
- Future conditions can change even when the original reasoning was sound.
- The default system does not use an arbitrary overall health score; it uses explicit states, materiality, evidence sufficiency, and uncertainty.

## Repository structure

```text
decision-debugger/
├── SKILL.md
├── README.md
├── PRD.md
├── references/
├── templates/
├── examples/
├── tests/
├── evals/
├── scripts/
├── commands/
├── manifest.json
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── QUALITY-GATES.md
```

## Roadmap

### v1.4.2

- Production-hardened decision reasoning workflow
- Decision framing and decomposition
- Evidence, assumption, reasoning, dependency, and sensitivity audits
- Failure Mode Analysis and cascading-failure tracing
- Red-team challenge and causal-identification checks
- Scenario and alternative analysis
- Feasibility, stakeholder, agency, and reversibility checks
- Value of Information and second-order-effect analysis
- Decision boundaries and reassessment triggers
- Rapid, Standard, Deep, and Post-Mortem modes
- Untrusted-content isolation and verification-freshness controls
- Canonical machine-readable output contract
- Regression cases, specification evaluation, templates, references, and a Claude Code install helper

### Future

- Expanded domain-specific benchmark suites
- More automated dependency and sensitivity reporting
- Broader high-stakes decision edge cases
- Additional runtime evaluation tooling for false positives and decision-changing findings

## License

Released under the MIT License. See `LICENSE`.

## Validation

Run:

```bash
python scripts/validate.py
python scripts/run_spec_eval.py
```

Static/specification validation checks repository integrity and required behavioral controls; it does not prove that a Claude runtime will make every decision judgment correctly. Do not publish runtime pass rates unless the target runtime was actually executed and the transcripts/results were retained.
