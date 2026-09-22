# Example — Business Decision

This is an illustrative output, not a recommendation.

## Input

> Should we migrate our production database to a new provider this quarter?

## Example Output

```text
DECISION DEBUGGER REPORT

Decision State: CONDITIONAL
Assessment Confidence: MODERATE

Primary Vulnerability:
The rollback path and production-specific compatibility assumptions are not yet demonstrated.

Decision-Changing Finding:
If rollback cannot reliably preserve data integrity or production compatibility, the timing and execution conditions change.

DECISION PROFILE
Objective: Improve the target infrastructure without unacceptable operational disruption
Constraints: Downtime tolerance, data integrity, staffing, dependencies, rollback capability
Options: Migrate now, delay, pilot, staged migration

MATERIAL FINDINGS

[DECISION-CHANGING] #001
Severity: HIGH
Type: REVERSIBILITY
Problem: Rollback is assumed to be available but its operational and data-integrity limits are not established.
Impact: A failed migration could create a longer outage or data divergence.
Recommended Action: Test rollback and restoration under production-like conditions.

FAILURE MODE ANALYSIS
FM-001 — Decision-Critical Execution Failure
Trigger: Production differs materially from staging.
Upstream Link: ASSUMPTION — staging coverage represents production behavior.
Vulnerable Dependency: Compatibility with production-only dependencies.
Failure Mechanism: A dependency or data path behaves differently under real production conditions.
Failure State: The migrated workload cannot operate at the required reliability.
Direct Effect: Application errors or partial service disruption.
Cascade: Partial migration → rollback complications → extended disruption.
Common-Mode Driver: The same dependency can impair the staged alternative if testing uses the same incomplete fixture.
Failure Interaction: FM-001 may AMPLIFY a resource/operational failure through incident load.
Detection: LEADING — production-like test failure, dependency mismatch, or failed rollback rehearsal.
Detection Window: Before broad rollout, if the pilot is representative.
Prevention: Pilot on a bounded workload; test production-like dependencies; verify rollback.
Containment: Stop rollout, isolate the affected workload, preserve the known-good path.
Recovery / Exit: Roll back if data integrity remains intact; otherwise use the tested restoration path.
Residual Vulnerability: Production behavior outside the tested envelope remains uncertain.
Decision Boundary: Condition: pilot or rollback rehearsal exposes unresolved integrity/compatibility failure → Interpretation: control barrier is insufficient → Implication: pause, redesign, or stage.
SECOND-ORDER EFFECTS
Migration may change operational workload, vendor dependencies, monitoring requirements, and incident-response procedures.

ALTERNATIVES
- pilot on a bounded workload
- staged migration
- delay until rollback evidence is stronger
- migrate now with explicit stop conditions

FINAL DECISION DEBUG
What is sound: The decision has a concrete objective and testable operational constraints.
What is fragile: Production compatibility and rollback assumptions.
What is unresolved: Whether rollback preserves data integrity under realistic failure conditions.
What would change the decision: Verified migration or rollback evidence that materially changes the risk boundary.
What should be monitored: Error rates, data integrity, dependency failures, rollback readiness, and downtime.
```
