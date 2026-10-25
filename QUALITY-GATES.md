# Quality Gates

## Gate A — Structure

Must include:
- exactly one root `SKILL.md` for the universal package
- README / PRD / release metadata
- references
- templates
- examples
- tests / evals
- validation scripts
- Claude Code install helper

A legacy plugin wrapper may exist in a separate distribution package, but it is not required for the universal standalone package.

## Gate B — Core behavior

Must:
- separate knowledge type from provenance
- enforce deterministic state precedence
- gate ROBUST
- detect decision-changing findings
- inspect evidence dependence
- inspect causal claims
- trace material failure cascades
- inspect authority / agency when relevant
- preserve user decision ownership
- protect against hindsight contamination
- preserve a locked decision-time calibration record and keep later outcome information in a separate review
- compare forecasts only with supplied outcomes and mark missing comparisons `NOT ASSESSABLE`
- distinguish decision-process quality from outcome quality
- limit cross-decision patterns and quantitative calibration metrics to the evidence and sample supplied, with limitations stated
- keep calibration records user-controlled and make no unsupported persistence, reminder, or monitoring claims
- isolate untrusted content
- inspect second-order effects when material
- keep values / preferences separate from factual premises
- preserve user-supplied probabilities as estimates unless verified
- handle materially equivalent alternatives without forced ranking
- enforce ledger minimization and retention boundaries
- preserve citation support integrity
- make dependency / sensitivity explicit
- make red-team output explicit
- make Value of Information explicit
- make reversibility / optionality explicit
- make robustness conditions explicit
- make decision boundaries explicit
- make reassessment triggers explicit
- require a final execution-integrity check

## Gate C — Evaluation integrity

Never present deterministic spec evaluation as runtime Claude evaluation.

Runtime claims require:
- actual target model execution
- retained prompts
- retained outputs
- recorded model/version/date
- explicit scoring criteria
- failure log
- regression updates

## Gate D — Release

Do not claim:
- hallucination-free
- guaranteed decision quality
- guaranteed outcomes
- runtime validated

without evidence sufficient to support the claim.
