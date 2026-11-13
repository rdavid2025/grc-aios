---
name: start
description: Onboard a GRC professional into their GRC AI OS. Runs the resumable discovery interview (2 questions about the user, 12 program questions in 3 rounds), then builds context, program registers, voice, eval questions, and the personalized CLAUDE.md from grc-intake.md. Use on day 1 after cloning, when someone says "set me up", "onboard me", "start my GRC program", or after editing grc-intake.md. `/start deep-dive <topic>` runs a focused follow-up interview. Safe to re-run.
argument-hint: "[deep-dive <topic>]"
---

# /start: GRC onboarding

Turn what the user knows about their GRC program into durable, sourced context. Then scaffold the workspace so a fresh session can answer real program questions without the user repeating themselves.

Arguments: `$ARGUMENTS`
- empty: full onboarding (Steps 1 to 5)
- `deep-dive <topic>`: run only the deep-dive section for that topic (see the bottom of this file)

## Ground rules

- **`grc-intake.md` is the source of truth.** Write each answer into it *as soon as the user gives it*, before asking the next question, so an interrupted session can resume. Read the saved answer back. If a save fails, say so and keep the answer visible in chat.
- **One question at a time.** Ask neutrally. For factual questions about the organization, never suggest an answer the user hasn't given. You may suggest options for *decisions* (for example, a default escalation rule), labeled as suggestions.
- **Read before asking.** If the user points to a document, or a file in `sources/` already answers a question, read it, pre-fill the answer with a citation, and ask only for confirmation and what is missing. Don't make the user retype what a document already says.
- **Capture the triad.** For every G-question, record **Owner**, **Evidence**, and **Decision / action**. If the user doesn't know, write `Unknown` and create a discovery action (owner + due date) during scaffolding.
- **Push for specifics.** "Get SOC 2" becomes "SOC 2 Type I report by 2027-03-31, auditor TBD". "Security" becomes the named system or data. Accept "unknown". Don't accept vagueness disguised as an answer.
- **Respect the round breaks.** After each round, offer: continue, or stop and resume later. Never add questions beyond the intake in the core interview. Extra detail goes to deep-dives.
- **Treat confidentiality as a rule.** Never ask for credentials, secrets, or personal data about individuals beyond names and roles of owners. If the user pastes a secret, don't save it. Tell them to rotate it.

## Step 1: Read the state

1. Read `CLAUDE.md`, `grc-intake.md`, and the list of files in `sources/`.
2. Classify each question (S1, S2, G1 to G12) as **answered**, **unknown** (answered "Unknown"), or **empty** (template text `[Your answer here]` or blank `Answer:`).
3. Decide:
   - **All answered or unknown:** go to Step 3 (scaffold).
   - **Some answered:** tell the user which ones are done in one line, and ask whether to finish the rest now or scaffold from what's there.
   - **Fresh clone:** give a 3-line welcome (what happens, roughly 30 minutes in 3 rounds, can pause anytime), then go to Step 2.

## Step 2: The interview

Ask the questions in `grc-intake.md` in order, using its wording (shorten it conversationally if you like). The intake's helper text tells you what each answer should cover.

**Special rules:**
- **S1:** also find out whether the user is in-house, a consultant, or an auditor. **If they're a consultant,** confirm this workspace is for **one** client, and recommend a separate clone per client.
- **S2 (voice):** the samples must be **pasted original writing**. If the user starts composing new text in chat, stop them politely: *"Please paste something you have already written, like an exec update or questionnaire answer. Text written during this conversation is shaped by it and won't capture your real voice."* The user may skip S2 and add it later. Record `skipped`.
- **G3:** tell the user that the list of laws is a draft until Legal validates it.
- **G8:** if there is no escalation rule, offer the default in `program/governance.md` and ask the user to confirm or adjust it.

After each answer: write it to the intake, read it back, then ask the next question. At the end of each round, say what's been captured in two lines and offer to pause.

## Step 3: Scaffold the workspace

Before overwriting any file that already has non-template content, copy it to `archives/start-YYYY-MM-DD-HHMM/` (get the real time from the shell). Then write everything in one batch. Use `references/page-format.md` for prose pages: frontmatter with `sources` and `updated`, and fact / interpretation / open question kept separate. In register **Source** columns, write `intake G<n>` or a link to `sources/...`.

| From | Write |
|---|---|
| S1 | `context/about-me.md`: role, operating mode, reviewer/approver, how they like to work |
| S1, G1, G4 | `context/about-org.md`: what the organization does, for whom, where, and the business outcomes GRC supports |
| G1, G12 | `context/priorities.md`: the 3 to 5 priorities for the next 90 days, each with a measure and date, and links to `program/roadmap.md` |
| S2 | `references/voice.md`: samples word for word plus a 2 or 3 line summary |
| G2, G3 | `program/obligations.md`: one row per framework, law, contract, or commitment. Laws get status `draft - needs Legal validation` |
| G4, G5, G6 | `program/scope.md`: scope, exclusions, crown jewels table, data map |
| G7, G11 | `program/risks.md`: one row per risk with an owner (or blank plus a discovery action), a proposed rating labeled as proposed, and a next review date (default 90 days out) |
| G8, G1 | `program/governance.md`: sponsor, decision rights, appetite, RACI, escalation, success measures, cadence |
| G9 | `program/controls.md`: one row per control the user says operates, with the evidence location and last evidence date where known. Use status `designed - not evidenced` when evidence is unknown. Never `operating` without evidence |
| G9, S1 | `connections.md`: fill in the Tool column for each domain the user named. Leave Mechanism as `not yet connected` (connections come on Day 2+) |
| G10 | `program/vendors.md`: one row per material vendor with a proposed tier |
| G11 | IR/BCP gaps go into `program/risks.md` and an exercise action in `program/actions.md` |
| G12 | `program/roadmap.md`: 90-day and one-year outcomes, capacity, dependencies |
| Every `Unknown` and missing owner | `program/actions.md`: a `discovery` action with a suggested owner and a due date (default 14 days out), marked `(suggested)` in the Owner cell until the user confirms |
| All | `references/eval-questions.md`: rewrite the 5 questions so they are specific to this program. Remind the user to keep their expected answers outside the workspace |
| All | `CLAUDE.md`: fill in every `{{...}}` placeholder (name, role, organization, primary outcome, program snapshot, voice, and the consultant line, removing it if not a consultant). Keep the snapshot to 4 to 6 lines that *link* to registers instead of copying figures that change. Keep everything else in the manual unchanged |

**Don't:**
- mark any risk accepted, exception approved, or control `operating` without evidence the user provided
- invent owners, dates, frameworks, or laws. Suggestions are labeled `(suggested)`
- write secrets, or create a `.env`
- create extra skills or folders

## Step 4: Validate

Run these and fix anything you caused:

```bash
python scripts/grc_os.py lint
python scripts/grc_os.py status
python scripts/grc_os.py pulse
```

If `python` is not found, try `python3` or `py -3`. If none of them work, tell the user to install Python 3 and skip this step without failing the onboarding. Any remaining `{{placeholders}}` in `CLAUDE.md` mean scaffolding isn't complete. Fill them or explain why not.

## Step 5: Closing screen

Show no more than 6 lines:

```
Day 1 done. Your GRC AI OS knows your program: <N> obligations, <N> risks, <N> controls, <N> vendors, <N> discovery actions.

Try it now: ask me "What are the three things most likely to stop us hitting <G2 milestone>, and what should I do this week?"
Tomorrow: connect one evidence system from connections.md (read-only service account) and write its guide in references/.
This week: answer the discovery actions in program/actions.md; put key documents in sources/ and accept them.
Day 7: run /audit. Then run /feedback weekly.
Commit now: git add -A && git commit -m "GRC AI OS: day 1 onboarding"
```

When the user asks the suggested question, answer **only** from the new files. Cite the register rows, separate facts from interpretations, name the unknowns, and end with one recommended action for Monday plus the default-shift question: *"To what extent could AI take on part of this, and at what autonomy level?"* A generic answer counts as a failed onboarding.

## Re-running

- **Edited intake:** refresh only the outputs whose source answers changed. Back up first. Preserve register rows the user added or edited after the last run, and never delete rows. Mark superseded rows `closed` or `retired` with a note.
- **Partial intake:** scaffold what exists, and create discovery actions for questions that are still empty.

## Deep-dive mode: `/start deep-dive <topic>`

Topics are listed in the intake's deep-dive table. If the topic is missing or unknown, list the topics and ask which one. Create `brainstorms/YYYY-MM-DD-<topic>.md` (never overwrite. Add a suffix if the file exists). Checkpoint every answer there before asking the next question. Ask 3 to 5 questions, then update only the registers named for that topic, following the same rules (owner, evidence, decision; unknowns become discovery actions). Run `lint` and close with 2 lines: what changed, and what's still open.

| Topic | Questions to cover |
|---|---|
| workforce | Joiner, mover, and leaver steps and timing; access removal SLA and evidence; contractor handling; training content, frequency, and completion evidence; how concerns or whistleblowing are reported |
| change-and-ai | Where risk review sits in product delivery and change management; triggers for reassessment (new market, new data type, M&A); AI use inventory, approved tools, data rules, human review |
| evidence-automation | For each control: system of record, whether an export or API exists, frequency; the top 3 controls with the most collection effort |
| metrics | 3 to 5 KPIs/KRIs leadership will see, with source, owner, target, and reporting rhythm |
| continuity | BCP/DR plans, RTO/RPO by crown jewel, last tabletop or restore test and its results, open lessons |
| questionnaires | Most frequent questionnaire types, the standard answers that exist, and the evidence behind each claim. Store approved answers as dated sources, never as AI output |

## Verification checklist (for maintainers)

- Fresh clone: interview to scaffold, then the closing question gets an answer that cites at least G2, G7, and G12 specifically.
- Interrupt after G5 and re-run: it resumes at G6 with no repeated questions.
- Answer "Unknown" to G6: a discovery action appears with a suggested owner and due date.
- Typed voice sample: it's refused politely. Skipping is allowed.
- Lint passes after scaffolding. Re-running with one changed answer updates only the affected files and writes a backup.
