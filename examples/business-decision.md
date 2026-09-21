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

FAILURE MODE
Trigger: Production differs materially from staging.
→ Weak Point: Compatibility assumptions are based on incomplete testing.
→ Failure: Migration encounters an untested dependency.
→ Immediate Impact: Application errors.
→ Secondary Impact: Customer-facing outage.
→ Cascade: Partial migration → rollback complications → extended disruption.
→ Early Warning: Production-like test failures, dependency mismatches, or rollback test failure.

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
