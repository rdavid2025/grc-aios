# GRC AI OS rubric (GRC-v1)

> Structure adapted from the AIS-OS audit rubric v2 and The Four Cs of an AI OS™ (Context, Connections, Capabilities, Cadence) by Nate Herk, MIT-licensed via [AIS-OS](https://github.com/nateherkai/AIS-OS). The Four Cs of an AI OS™ is a trademark of Nate Herk. GRC anchors, the integrity gate, and the autonomy ceilings were added for this template.

## Scoring rules

There are 5 criteria per C, each worth 5 points. Award **0, 1, 3, or 5 only**: the highest anchor fully supported by evidence. A higher anchor includes the checks below it. Never interpolate, never start at full marks and deduct, and never substitute optimism for evidence. Documentation can earn 1 point where an anchor says so. It is not a working result. A bounded sample proves the sample, not the whole system, so name what you sampled.

## Context: can a fresh session understand the program and trace its claims? (25)

| ID | Criterion | 1 | 3 | 5 |
|---|---|---|---|---|
| C1 | Personalized program context | CLAUDE.md has non-placeholder identity, organization, and purpose | Outcomes, obligations, scope, and priorities each have specific, usable pages or rows | All of those agree across sampled sources, and priorities have measures and dates |
| C2 | Routing and findability | The manual gives at least one specific usable route | At least 3 of 5 probes succeed through declared routes, and every routing-table target exists | All 5 probes are direct; there are no broken internal links and no important unrouted material |
| C3 | Freshness | Changing facts have `updated:`, source dates, or register dates | `status` shows no changed-but-unreviewed sources, and sampled facts are within their review interval | Every sampled current fact is verified within its interval, and the CLAUDE.md snapshot links to registers instead of copying stale figures |
| C4 | Evidence integrity and authority | Sources exist in `sources/` with provenance, or a canonical system of record is identified | Lint has no integrity errors; sampled facts cite sources; fact, interpretation, and open question are separated in sampled pages | At least 3 sources are accepted with fingerprints; sampled authority chains resolve end to end; conflicts are preserved with dates |
| C5 | Continuity | A real decision, exception, or action record exists | The sampled priority has a current status, an owner, a next step, and decision rationale reachable from its entry point | A second program thread (for example a vendor review or audit prep) can also be resumed from durable records |

## Connections: can it reach the evidence it needs? (25)

Inventory the domains in `connections.md` first. Mark domains `n/a` only for a reason grounded in the program (for example "no endpoints, fully browser-based contractors"), never because they're disconnected.

| ID | Criterion | 1 | 3 | 5 |
|---|---|---|---|---|
| N1 | Relevant domain access | At least one relevant domain has evidence of a successful read | At least half of the relevant domains have successful-read evidence | Every relevant domain has successful-read evidence within its expected interval |
| N2 | Useful evidence retrieval | A specific evidence query and expected result are documented | One real control-evidence query returns the right records, date range, and source | Two distinct evidence queries succeed, with completeness or pagination checked |
| N3 | Reproducible access routes | One connection has a documented route and purpose | Every relevant domain has a route or an explicit missing status; connected ones have guides in `references/` with auth steps (no secrets) and query examples | A sampled route is reproduced from its guide alone, with no hidden chat context |
| N4 | Least privilege | Read/write scope and approval boundaries are documented | Connections use dedicated service identities with read-only scope, or any write scope is justified and recorded | Sampled operations respect scope, and safeguards against duplicate or unintended writes are verified (never do a live write to prove it) |
| N5 | Freshness and failure visibility | Expected refresh intervals are documented | Sampled reads or exports are within interval, and failures surface instead of being replaced by old data | All relevant domains have recent success evidence, and an expired-auth or stale-data case was handled visibly at least once |

## Capabilities: do GRC workflows produce usable, defensible output? (25)

Choose up to three priority workflows *before* inspecting their outputs. Onboarding counts as a workflow. If a priority needs a workflow that doesn't exist, keep that gap in the sample.

| ID | Criterion | 1 | 3 | 5 |
|---|---|---|---|---|
| P1 | Fit and invocation | A workflow has a clear trigger tied to a stated priority | One sampled workflow has a successful real invocation | All sampled workflows have successful invocations, and their triggers don't overlap confusingly |
| P2 | Output quality | An example output and acceptance criteria exist | One real output was checked against acceptance criteria, with claims sourced and gaps labeled | All sampled outputs were verified against their criteria by a human reviewer, not just self-reported |
| P3 | Failure handling and boundaries | Missing-input and error cases are documented | One missing-input or stale-source case was handled correctly | Every sampled workflow has a tested boundary case and respects the autonomy ceilings (external content stays at L2 or below; never accepts risk or attests) |
| P4 | Portability | Required files and the invocation route are documented | Entry points and references resolve, and `python -m unittest` passes | A clean-session run reproduces a sampled workflow with no hidden state |
| P5 | Repeated real use | One dated real use is evidenced | One workflow has two distinct real uses with output references | All sampled workflows show repeated use, and `/feedback` corrections show up in the current version and were validated afterwards |

## Cadence: does GRC work happen reliably over time? (25)

| ID | Criterion | 1 | 3 | 5 |
|---|---|---|---|---|
| D1 | Real trigger | A documented human ritual or scheduler configuration exists | At least one enabled trigger (for example a scheduled `grc_os.py review`) has a verified host and expected output | That trigger has demonstrably run unattended in its intended environment |
| D2 | Due executions | One dated manual completion or failed automatic attempt is recorded | One due automatic run completed (for example a `review-*.md` exists for its due date) | Two or more due runs completed, with no unexplained missed runs in the period |
| D3 | Observability | Run status and failure-notification behavior are documented | Runs leave timestamped outcomes, and the failure path is verified | A real or safely simulated failure reached the reporting path and recovery was evidenced |
| D4 | Control and recovery | Stop/disable, owner, and recovery steps are documented | Configuration shows those controls and prevents overlapping runs | A stop or recovery was demonstrated without side effects (for example a `git revert` of a bad update) |
| D5 | Program rhythm | Review frequencies are defined in `program/governance.md` | One completed review (risk, exception, or vendor) is evidenced with a date and its outcome is recorded | Two distinct review cycles are evidenced, and their follow-up actions were tracked to closure |

## Gates and stages

1. **Evidence-integrity gate:** any lint error for a fabricated quote, a missing quoted source, or a missing frontmatter source caps **Context at 10**. A validator that can't be run also caps Context at 10, because integrity is unverifiable.
2. **Purpose gate:** if no probe can recover the program's main outcome or any authoritative status source, **Context is capped at 10**.
3. **Manual-only cadence:** with no verified enabled automatic trigger, **Cadence is capped at 10**.
4. **Raw total** = the sum of the four capped subtotals.
5. **Total caps** (the lowest applicable one wins):
   - Any C below 10: total capped at **49**
   - Any C below 15, or fewer than two verified due automatic runs: total capped at **69**
   - Any C below 20, or an unresolved source-authority conflict: total capped at **84**
6. **Final** = min(raw total, the caps). Report every cap applied and the reason for it.

| Final | Stage |
|---|---|
| 0-24 | Unproven |
| 25-49 | Foundation |
| 50-69 | Working, with gaps |
| 70-84 | Dependable in the verified scope |
| 85-100 | Maintained and evidenced |

## Calibration

- A fresh clone with placeholders: Unproven. Shipped files earn no credit.
- After `/start` with good registers but no sources, connections, or runs: Context around 9 to 15, everything else low. Foundation at best.
- One fabricated quote in an otherwise excellent workspace: Context 10, total capped at 49. Integrity comes first in GRC.
- Perfect Context, Connections, and Capabilities with manual-only cadence: raw 85, final 69.
- A scheduled `grc_os.py review` with two dated due reports and no misses: earns D2 = 5. Two back-to-back manual runs do not.
- A pulse showing 20 overdue actions does **not** lower the score. It shows the OS is surfacing reality. The score falls only if the registers themselves are unreliable (stale, unowned, or contradicting sources).
