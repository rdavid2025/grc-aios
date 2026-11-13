---
name: audit
description: Audit the GRC AI OS itself. Scores verified operational reliability across Context, Connections, Capabilities, and Cadence (rubric GRC-v1), runs the evidence-integrity validator, takes a program health snapshot from the registers, and saves a dated report to audits/ that tracks findings across runs. Use when someone asks to audit their GRC OS, check whether it can be trusted, find stale evidence or broken routes, or measure progress. Read-only apart from the saved report.
argument-hint: "[focus area, optional]"
---

# /audit: is this GRC AI OS trustworthy?

Answer two separate questions and never blur them:

1. **Can this AI OS be relied on?** That means verified operational reliability, scored out of 100 using [rubric.md](rubric.md).
2. **What does the program look like right now?** That is a health snapshot taken from the registers. **It is not scored.** A program full of overdue actions can still have a reliable OS that reports them accurately.

A folder, an installed skill, an API key, or a confident claim is not proof. Score only evidence you observed in this run or in dated records. Optional focus from the user: `$ARGUMENTS`.

## Boundaries

- **Read-only.** No repairs, no file moves, no register or manual edits, no scheduler changes, no messages, no external writes. The only thing you write is the new report in `audits/`.
- Don't run paid or side-effecting workflows to earn points. Don't trigger scheduled jobs. Use existing evidence, or label the item **unverified**.
- Redact secrets and avoid copying bulk confidential register content into the report. Reference IDs and paths instead.
- Never inflate or depress a score to encourage another run. Unverified evidence is a verification gap, not proof of failure.
- Don't use subagents unless the user asks.

## Step 1: Scope and history

1. Get the current UTC time and the project root. Read `CLAUDE.md` (and `AGENTS.md` to confirm it still only bridges to `CLAUDE.md`).
2. **Load history:** list `audits/audit-*.md` and read the frontmatter only. Take the latest `audit_kind: grc-os` report, plus the latest *complete* one if that's a different report. Carry its finding ledger forward. No prior report means **first recorded baseline**. Ignore `review-*.md` files when choosing a baseline, but you may use them as cadence evidence.
3. Identify the user's role, main outcome, and up to three priority workflows from actual context. Unfilled `{{placeholders}}` count as missing context, not as context.

## Step 2: Mechanical checks (deterministic)

Run each of these and keep the output for the report:

```bash
python scripts/grc_os.py status
python scripts/grc_os.py lint
python scripts/grc_os.py pulse
python -m unittest discover -s tests
```

Try `python3` or `py -3` if `python` is missing. If none works, record **validator unavailable**. That is a Context verification gap, and the integrity gate can't be passed. Never guess at lint results.

**Evidence-integrity gate:** any lint **error** about a fabricated quotation, a missing quoted source, or a missing frontmatter source caps Context at 10 (see the rubric). A broken internal link is a routing defect, not an integrity failure.

## Step 3: Routing probes

Use the five questions in `references/eval-questions.md`. If they're still template text, use the defaults in that file adapted to whatever context exists, and record that the eval set hasn't been personalized. For each question:

- route: manual, then the register or page, then the specific row or source
- result: **direct** (found through the declared route), **fallback** (only found by searching), or **not found**
- whether the answer would carry a source and date, and whether the source is past its review date

Don't grade against expected answers. The user keeps those outside the workspace. Offer the answers you found so the user can grade them.

Also check:
- **Authority:** current status comes from registers or live systems. Exact wording comes from `sources/`. There are no duplicate sources of truth (for example a second risk list outside `program/risks.md`). Archived material is not presented as current.
- **Freshness:** `status` shows no changed-but-unreviewed sources. Prose pages have plausible `updated:` dates. The CLAUDE.md snapshot doesn't copy figures that have since changed.
- **Manual health:** every routing-table target exists, the evidence rules and decision boundaries are intact, and `AGENTS.md` still points to `CLAUDE.md`.

## Step 4: Verify Connections, Capabilities, Cadence

- **Connections:** for each domain in `connections.md`, record whether it's relevant (or `n/a` with a reason), the mechanism, its access scope (read-only?), evidence of a successful read and its date, and whether a guide exists in `references/`. A configured MCP or `.env` key doesn't prove authentication. Use only narrow, safe, read-only checks, and only when a guide documents them. Never print secrets or bulk records.
- **Capabilities:** choose up to three GRC workflows tied to the priorities *before* looking at their outputs. Examples: questionnaire drafting, evidence collection for a control, risk review prep, the onboarding itself. For each, check the trigger, inputs, an actual output (in the workspace or referenced), acceptance criteria, failure handling, autonomy level against the ceilings in `references/operating-principles.md`, and repeated real use. A workflow that sends external content above L2 is a confirmed defect.
- **Cadence:** look for actual enabled schedules (Task Scheduler, cron, Claude scheduled tasks, CI), dated `audits/review-*.md` outputs, and documented human rituals (`program/governance.md` review cadence) that have dated completion evidence. A cadence table on its own is a plan, not a run. Manual-only cadence is capped at 10.

## Step 5: Score

Read the whole of [rubric.md](rubric.md). Award all 20 criteria (0, 1, 3, or 5 each), apply the gates and caps, and show the arithmetic. Then group findings as **confirmed defects**, **verification gaps**, and **improvement opportunities**. Give each underlying issue one stable ID (`GRC-<run-id>-NN`) and reuse it everywhere. Rank by impact on the user's work: wrong or stale answers and integrity failures first, cosmetic issues last. Recommend at most three fixes. Don't invent three if the system is healthy.

## Step 6: Report and save

Fill in [templates/report.md](templates/report.md) completely and save it to `audits/audit-YYYY-MM-DD-HHMMSS-<4 hex>.md` (UTC). Use exclusive creation: never overwrite, and retry with a new suffix if the name exists. Then read the saved file back and check the metadata, arithmetic, and finding IDs.

**Finding history.** Carry forward every prior finding. Keep its original ID and first-seen date, and update the status:

| Status | Requires |
|---|---|
| New | First observed in this history |
| Still open | Rechecked and still present |
| Resolved | The original completion check passes with current evidence (a proposed edit or a changed timestamp is not enough) |
| Reopened | Previously resolved, and the same failure is back |
| Not rechecked | Not covered this run. Keep the last verified state. Never treat it as resolved |
| No longer applicable | Scope or requirements changed, with the reason given. This is not a repair |

Compare scores with a previous report only when it's complete and covers the same rubric version and materially the same scope. Otherwise write **scores not directly comparable** and say why. Separate actual repairs from gains that come only from better evidence.

**Chat reply (concise):**
1. Score: final `/100`, stage, the four subtotals, and any caps with the reason for each
2. What works (up to 3 items)
3. Program pulse headline (counts of high and medium items, plus the single most urgent item)
4. Top fixes (up to 3), each labeled repair, verify, or optional, with a completion check
5. Progress since the last audit, or "first baseline"
6. Next step: a ready-to-paste `/feedback` prompt for the highest-value fix
7. A clickable link to the saved report

If saving fails, say **report not saved**, explain why, and return the full report in chat. If the user asked you not to save, say **not saved at your request**. Never claim a report was saved without reading it back.

Recommend running `/audit` again after the chosen fix, weekly during setup, and monthly after that. Scores can go down when evidence goes stale, and that's the system working.
