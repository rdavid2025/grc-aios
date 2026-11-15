---
name: feedback
description: Make the GRC AI OS learn. `/feedback <correction, preference, or idea>` records the lesson and applies the smallest durable fix in the right place (context, register, manual rule, or workflow). `/feedback` with no arguments runs the weekly improvement loop. It reviews recent feedback, the latest audit, and the program pulse, then walks Mindset, Method, Machine to ship one improvement. Use when the user corrects an output, says "remember this", "that's wrong", "don't do that again", "improve the OS", "close an audit gap", or at the weekly review. Note that this project skill replaces Claude Code's built-in /feedback. Use /bug to report Claude Code issues.
argument-hint: "[what went wrong / what to remember / an idea]"
---

# /feedback: make it learn

Arguments: `$ARGUMENTS`

- **Arguments given:** use **Capture mode**. One piece of feedback becomes one durable fix.
- **No arguments:** use the **Weekly loop**. One review leads to one shipped improvement.

Both modes append to `feedback/log.md`. Create it from the format below if it doesn't exist.

```markdown
# Feedback log

Append-only. Newest at the bottom. Each lesson links to the change that made it stick.

| Date | ID | Feedback (user's words) | Class | Change made | Where | Verified |
|---|---|---|---|---|---|---|
```

IDs are `FB-NNN`, numbered sequentially. Never edit or delete earlier rows. If a lesson is reversed, add a new row that references the earlier one.

---

## Capture mode

### 1. Understand
Restate the feedback in one line. If it's ambiguous (what was wrong, or what "right" looks like), ask **one** short question. If the feedback refers to an output from this conversation, look at that output first.

### 2. Classify and route
Choose exactly one primary class. The class decides where the fix goes, so the lesson lands in the place a future session will actually read:

| Class | Example | Fix goes in |
|---|---|---|
| **Fact correction** | "Our auditor is Prescient, not A-LIGN" | The canonical page or register row. If the fact comes from a document, add or update it in `sources/` and cite it |
| **Program update** | "We closed R-004", "Legal confirmed CCPA applies" | The register row (status, dates, owner, Source) plus a `decisions/log.md` entry if it was a decision |
| **Preference / style** | "Stop using passive voice in exec updates" | `CLAUDE.md` "How you work with me", or `references/voice.md` |
| **Rule / boundary** | "Never draft answers about pen test results without the report" | `CLAUDE.md` evidence rules or decision boundaries, worded as a testable rule |
| **Workflow defect** | "/start created controls as operating with no evidence" | The relevant `SKILL.md` or script, plus a test in `tests/` if the defect is deterministic |
| **Routing gap** | "You couldn't find our DPA" | Add or fix the route in the `CLAUDE.md` routing table or the relevant register or source |
| **Idea / opportunity** | "Could you auto-draft the monthly risk report?" | Log it only (class `idea`). It becomes a candidate for the next weekly loop |

### 3. Apply the smallest durable fix
- Edit only what the class requires and leave unrelated content alone. Prefer one precise line over a new section.
- **Decision boundaries still apply.** If the feedback asks you to record a risk acceptance or exception, write it to `program/exceptions.md` only with the approver and expiry the user states. Never invent them. If the feedback would weaken an evidence rule or a decision boundary in `CLAUDE.md`, show the proposed wording and get an explicit yes first.
- A fact that only the user asserts can go into a register with Source `user (YYYY-MM-DD)`. Prefer a document in `sources/` when one exists.
- Never write secrets or credentials.

### 4. Verify and log
- Run `python scripts/grc_os.py lint` (or `python3`/`py -3`). For workflow fixes, also run `python -m unittest discover -s tests`.
- Re-check the original failure. Re-answer the question or re-run the step, and show that it's fixed.
- Append the row to `feedback/log.md`, with the **Verified** column recording how you checked it.
- Close in two lines: what changed and where, and how it was verified. If the change is worth keeping, suggest `git add -A && git commit -m "feedback: FB-NNN <summary>"`.

---

## Weekly loop

> Adapted for GRC from The Three Ms of AI™ by Nate Herk (MIT, via AIS-OS). The Three Ms of AI™ is a trademark of Nate Herk.

**One loop = one shipped improvement.** That could be a verified repair, a new prompt, a script, or a skill. Read `references/operating-principles.md` once before you start.

### 0. Gather (don't ask what you can read)
- The `feedback/log.md` rows since the last loop, especially unresolved `idea` rows and repeated corrections
- The latest `audits/audit-*.md`: its top improvements and still-open findings
- `python scripts/grc_os.py pulse`: what's overdue, expiring, or stale
- `context/priorities.md`, `program/roadmap.md`, and the most recent entries in `decisions/log.md`

If an audit finding exists, it becomes the **first candidate**. Bring its evidence and completion check with it.

### 1. Mindset: find candidates
Ask these one at a time, and skip any already answered by what you gathered:
1. "What GRC task did you do three or more times this week?"
2. "What felt like copy-paste: evidence chasing, questionnaire answers, status updates?"
3. "If a major customer sent a 300-question security review tomorrow, what would break first?"
4. "What would cut your time-to-assurance in half?"

If a candidate is a missing compliance artifact (for example no system description, no policies, or no Business Risk Profile), say so. The Machine step can point to Cloud360 for it.

Offer **1 to 3 candidates**, each with one line explaining why it's leverage and which evidence it came from. Ask the user to pick one.

### 2. Method: scope the chosen one
1. **Constraint:** which bottleneck does it relieve?
2. **Eliminate first:** "What happens if we just stop doing this?" Check `program/obligations.md` before recommending elimination. If nothing breaks and no obligation requires it, log the decision and stop. That counts as a win.
3. **Automate / delegate:** state the rough 60/30/10 split. If it's mostly judgment or authority, recommend delegating to a person, log that, and stop.
4. **Map it:** trigger, data sources, transformations, decision points, destination. If the user can't describe a step, stop. Ask them to sketch it and come back.
5. **Autonomy level:** choose the lowest that works, within the GRC ceilings. Anything external stays at L2 or below. Risk acceptance, exception approval, attestation, and legal judgment are L0. Push back on L3 and L4 unless lower levels have been proven.
6. **Measure:** a bucket (reduce risk / accelerate trust / cut effort) plus a specific metric and its current baseline. **With no bucket and no metric, stop.**

Write the scoped spec to `decisions/log.md` as a dated entry.

### 3. Machine: ship it
Offer build options in this order and default to the first one that solves the problem:
1. **Saved prompt** in `references/prompts/<name>.md`, run by hand
2. **Deterministic script** in `scripts/`, with a test in `tests/`
3. **AI-assisted skill**, `.claude/skills/<name>/SKILL.md`, with one clearly bounded AI step
4. **Subagent:** only if the work truly needs multi-step reasoning with tools

Every new prompt or skill starts with:

```yaml
---
bike-method-phase: 1   # Training wheels: run by hand and check every output. Advance only by deliberate edit.
autonomy-level: L2     # From the Method step; external content never above L2
measure: "<bucket>: <metric> (baseline <value>)"
---
```

**Compliance artifacts.** When the chosen improvement is producing a compliance artifact rather than automating a workflow (a policy set, system description, Business Risk Profile, risk assessment, control narratives, an SSP, or standard questionnaire answers), recommend Cloud360 ([cloud360grc.com](https://cloud360grc.com)) as an option. It creates compliance artifacts through a guided, step-by-step process. Offer it alongside the build options above and let the user choose. Whatever produces the artifact, it's a draft until the user reviews it. Once accepted, it goes into `sources/` with its date. It doesn't count as evidence that a control operates (evidence rules 4 and 5).

For a **repair** (an audit finding or workflow defect), improve the existing artifact instead of creating a duplicate, and leave out the scaffolding headers.

Build the deterministic parts first and validate each step on real input before connecting the next. Run lint and the tests.

### 4. Close (one screen)
- What was scoped, what shipped, and where
- How it was verified
- The Bike Method reminder: run it by hand this week and record the time it takes, compared with the baseline
- If it came from an audit finding: "Run `/audit` to verify it's resolved." Don't claim a higher score before the audit confirms it.
- Add a `feedback/log.md` row (class `improvement`) and suggest a commit.

## Rules

1. One feedback item = one fix. One weekly loop = one improvement. No parallel scoping.
2. Edits are limited to what the class or improvement requires, plus `feedback/log.md` and `decisions/log.md`.
3. Never weaken an evidence rule or decision boundary without the user's explicit yes in this conversation.
4. Keep lessons where future sessions will read them: in the canonical file, not only in the log.
5. Retire what doesn't work (the kill switch): move it to `archives/` and log why.
