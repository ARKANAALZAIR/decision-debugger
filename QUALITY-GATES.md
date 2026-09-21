# Quality Gates

## Gate A — Structure

Must include:
- `SKILL.md`
- `.claude-plugin/plugin.json`
- plugin skill path
- references
- templates
- examples
- tests / evals
- validation scripts

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
- isolate untrusted content
- inspect second-order effects when material
- keep values / preferences separate from factual premises
- preserve user-supplied probabilities as estimates unless verified
- handle materially equivalent alternatives without forced ranking
- enforce ledger minimization and retention boundaries
- preserve citation support integrity

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
