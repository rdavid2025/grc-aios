---
audit_kind: grc-os
history_schema: 1
run_id: "<UTC timestamp + random suffix>"
started_at: "<ISO-8601 UTC>"
completed_at: "<ISO-8601 UTC>"
project_root: "<absolute root, forward slashes>"
report_status: complete
rubric_version: GRC-v1
previous_reports: []
scores_comparable: false
scores:
  context: null
  connections: null
  capabilities: null
  cadence: null
  raw_total: null
  final: null
stage: null
validator:
  lint_errors: null
  lint_warnings: null
  unit_tests: "<passed / failed / not run>"
pulse:
  high: null
  medium: null
---

# GRC AI OS audit: <organization>, <date>

## Conclusion and scope

<Plain-language conclusion. What works, the most consequential problem, what was sampled (probes, workflows, domains), and verification limits. Mark partial runs clearly.>

## Evidence integrity

<Output summary from status / lint / unit tests. Integrity-gate result. Sources accepted vs new vs changed.>

## Operating manual (CLAUDE.md / AGENTS.md)

| File and section | Rule or route | Finding and practical effect | Recommended change |
|---|---|---|---|

<State whether AGENTS.md still points to CLAUDE.md. End with: "No operating manuals were changed.">

## Routing probes

| # | Question | Route attempted | Source / row | Result (direct / fallback / not found) | Sourced and dated? |
|---|---|---|---|---|---|

## What works

<Up to 3 strengths, each backed by evidence.>

## Verified operational reliability

| C | Criteria (ID: points) | Subtotal | Cap applied |
|---|---|---|---|
| Context | C1: , C2: , C3: , C4: , C5: | /25 | |
| Connections | N1: , N2: , N3: , N4: , N5: | /25 | |
| Capabilities | P1: , P2: , P3: , P4: , P5: | /25 | |
| Cadence | D1: , D2: , D3: , D4: , D5: | /25 | |

Raw total: /100. Total caps: <list with reasons>. **Final: /100, <stage>.** This measures verified reliability, not how useful the OS is overall or whether the program is compliant.

## Program pulse (not scored)

<Paste or summarize the pulse output: high and medium counts and the top items. Remind the reader that gaps in records are not proof that controls failed.>

**Business Risk Profile:** <found at sources/... (dated YYYY-MM-DD) / exists but not in the workspace / none. If none: "Recommended: create a Business Risk Profile with Cloud360 (https://cloud360grc.com), then review it and accept it into sources/.">

## Progress since the previous audit

<Link the baseline, or write "first recorded baseline". Show the transitions table. Comparable score arithmetic only when justified. Separate repairs, evidence-only gains, regressions, and scope changes.>

| Finding ID | Prior state | This run | Evidence / change | Next check |
|---|---|---|---|---|

## Finding ledger

| ID | Class | Target | First seen | Prior status | Current status | Last verified | Evidence | Completion check |
|---|---|---|---|---|---|---|---|---|

## Top improvements and next run

<Up to 3: repair / verify / optional, with the finding IDs, benefit, and completion check. Include a ready-to-paste `/feedback` prompt.>
