# GRC AI OS

A free, MIT-licensed template that turns Claude Code into your personal **GRC AI Operating System**: a workspace where your AI already knows your program, retrieves evidence with sources, follows repeatable GRC procedures, and keeps decisions for every future session.

Clone it, run `/start`, and within an hour you have a sourced obligations register, risk register, control baseline, vendor list, governance model, and 90-day roadmap built from your own answers. From then on, your AI answers program questions without you explaining the business again.

> **The test:** open a fresh session and ask *"What could stop us passing our SOC 2 audit in March, and what should I do this week?"* You should get a specific answer that cites your own registers and sources, separates facts from interpretation, and says what is still unknown.

Built for in-house GRC leads, security and compliance managers, vCISOs and consultants (one clone per client), and internal auditors at startups and mid-market companies.

---

## Three commands

| Command | What it does | When |
|---|---|---|
| `/start` | Onboarding interview: up to 5 questions about you and your starting point (existing program or from scratch, current tools such as Vanta, Drata, AWS, or Google Sheets, and your system description) plus 12 program discovery questions in three resumable rounds. Builds context, registers, voice, eval questions, and your personalized `CLAUDE.md`. `/start deep-dive <topic>` goes deeper later (workforce, change-and-ai, evidence-automation, metrics, continuity, questionnaires). | Day 1, then after editing `grc-intake.md` |
| `/audit` | Evidence-based reliability score (0 to 100) across Context, Connections, Capabilities, and Cadence, plus an evidence-integrity gate (no fabricated quotes) and an unscored program health snapshot (overdue actions, expired exceptions, stale evidence). Saves a dated report and tracks findings across runs. Read-only. | Day 7, after each fix, then monthly |
| `/feedback` | `/feedback <correction>` records the lesson in the right file so it sticks. `/feedback` alone runs the weekly improvement loop (Mindset, Method, Machine) to ship **one** improvement. | Whenever you correct it, and weekly |

> `/feedback` here replaces Claude Code's built-in `/feedback` inside this project. To report a Claude Code issue, use `/bug`.

Plus one deterministic utility with no AI and no network, standard library only:

```bash
python scripts/grc_os.py status   # new/changed sources and the pages that cite them, placeholders left, register counts
python scripts/grc_os.py lint     # broken links, quotes not found in their source, missing sources, bad dates, duplicate IDs
python scripts/grc_os.py pulse    # overdue actions, unowned risks, expired exceptions, stale evidence, upcoming deadlines
python scripts/grc_os.py accept sources/<file>.md [--reviewed <page>]   # fingerprint a reviewed source
python scripts/grc_os.py review   # status + lint + pulse saved to audits/ (schedule this)
```

---

## Quick start

**Prerequisites:** [Claude Code](https://code.claude.com/docs/en/setup), Git, and Python 3.9+ (`python`, `python3`, or `py -3`). Obsidian is optional, for browsing.

1. **Clone the template into a private repository.** Your workspace will describe your risks and control gaps. Never make it public.
   ```bash
   git clone https://github.com/<you>/grc-aios.git my-grc-os
   ```
2. **Check it works:**
   ```bash
   cd my-grc-os
   python -m unittest discover -s tests
   python scripts/grc_os.py lint
   ```
3. **Open Claude Code in the folder and run `/start`.** Answer honestly. "Unknown" is a good answer, because it becomes a discovery task with an owner and a due date. If you already have a SOC 2 report, policies, or past questionnaires, convert them to Markdown, put them in `sources/` first, and `/start` will read them instead of asking.
4. **Commit:** `git add -A && git commit -m "Day 1 onboarding"`.

### Your first two weeks

| Day | Do | Evidence it worked |
|---|---|---|
| 1 | `/start`, ask the closing question | Specific, sourced answer; first commit |
| 2 | Add 3 to 5 key sources to `sources/` with provenance, review the pages that cite them, `accept` them | `status` shows them accepted, `lint` is clean |
| 3 | Connect one evidence system read-only (see `connections.md`), write `references/<tool>-guide.md` | A dated successful read |
| 4 | Fresh session: ask the five questions in `references/eval-questions.md` and grade them against answers you keep outside the repo | Score recorded |
| 5 | Produce one real deliverable (questionnaire draft, risk review pack, evidence request list) | Time spent and corrections noted; corrections sent through `/feedback` |
| 6 | Change a source and see `status` flag the pages that cite it; practise `git revert` | Stale content caught, recovery works |
| 7 | `/audit` | Baseline report in `audits/` |
| 8 to 14 | Schedule `grc_os.py review` weekly; run `/feedback` (weekly loop) on the top audit gap | Two due runs; one improvement shipped |

A sensible bar for expanding scope: your chosen workflow succeeds twice with less effort than before and no unsupported critical claims. That bar is a proposed pilot standard, not a benchmark.

---

## How it is designed

Three layers you can tell apart, and an honest score.

**1. Evidence discipline.** Every statement is a *fact* (with a source), an *interpretation* (labeled), or an *open question* (with an owner). Quotes must match their source word for word, and the validator fails otherwise. Sources carry provenance and are fingerprinted, so when a policy changes you're told which pages to re-review. Missing evidence is reported as a gap in proof, never as a failed control. A vendor's SOC 2 is never treated as proof of *your* controls.

**2. Decision boundaries.** The AI drafts, analyzes, tracks, and reminds. It **never** accepts risk, approves exceptions, signs or attests, sends anything external, or declares compliance. External content is capped at autonomy level L2 (AI drafts, human reviews).

**3. The Four Cs, adapted for GRC**

| Layer | In this template | "In place" test |
|---|---|---|
| **Context** | `context/`, `program/` registers, `sources/`, `CLAUDE.md` routing | A fresh session answers your five eval questions with sources |
| **Connections** | `connections.md`: identity, cloud, MDM, HR, ticketing, code, scanners, GRC platform, docs | Live evidence reads through read-only service identities |
| **Capabilities** | `/start`, `/audit`, `/feedback`, plus workflows you add through `/feedback` | A short request produces a defensible deliverable |
| **Cadence** | Scheduled `grc_os.py review`, risk, exception, and vendor review rhythm in `governance.md` | Reports appear on schedule with no one asking |

---

## Layout

```
grc-aios/
├── CLAUDE.md                 Operating manual: routing, evidence rules, decision boundaries (personalized by /start)
├── AGENTS.md                 Points other assistants (Codex, etc.) to CLAUDE.md
├── grc-intake.md             Source of truth for /start: the discovery questions and your answers
├── connections.md            Evidence systems the OS can reach, with scope and last successful read
├── context/                  About you, the organization, priorities (created by /start)
├── program/                  The GRC program state
│   ├── obligations.md        Frameworks, laws, contracts, commitments
│   ├── scope.md              Scope, crown jewels, sensitive data map
│   ├── risks.md              Risk register
│   ├── controls.md           Control baseline and where evidence lives
│   ├── vendors.md            Third parties by tier
│   ├── actions.md            Remediation, discovery, audit-prep actions
│   ├── exceptions.md         Exceptions and risk acceptances (approver + expiry)
│   ├── governance.md         Sponsor, decision rights, appetite, RACI, metrics, cadence
│   └── roadmap.md            90-day and one-year plan, capacity, dependencies
├── sources/                  Original documents with provenance (sources/private/ is gitignored)
├── references/               Page format, operating principles, voice, eval questions, tool guides
├── decisions/log.md          Append-only decisions and why
├── feedback/log.md           Lessons learned (created by /feedback)
├── audits/                   Dated /audit and review reports (gitignored)
├── archives/                 Retired material. Move things here, don't delete
├── scripts/grc_os.py         Deterministic status / lint / pulse / accept / review
├── tests/                    Unit tests for the utility and template
├── docs/DESIGN.md            How this template was derived and why
└── .claude/skills/           start, audit, feedback
```

See [EXPANSIONS.md](EXPANSIONS.md) for what to add as you grow, and [docs/DESIGN.md](docs/DESIGN.md) for the design rationale.

---

## Scheduling the weekly review

**Windows Task Scheduler:** create a task named `GRC OS Weekly Review`. Set Program to the full path of `python.exe`, Arguments to the full path of `scripts\grc_os.py review`, and Start in to your workspace folder. Run it once by hand and check that `audits/review-*.md` appears.

**macOS / Linux (cron):** `0 8 * * 1 cd /path/to/my-grc-os && python3 scripts/grc_os.py review`

The review exits with a non-zero code when lint finds errors, so a failed run is visible in the scheduler's history. It makes no AI calls. Once it's reliable, you can also schedule a Claude Code task that reads the latest review and drafts the week's priorities.

## Recovery and backups

- Every accepted batch of changes gets a Git commit. To undo a bad commit, run `git log --oneline` and then `git revert <commit>`.
- `audits/` and `brainstorms/` are gitignored because they may contain sensitive detail. Include them in your normal backup.
- Test a restore once a month.

## Privacy

Keep the repository private. Never store credentials or personal data in Markdown. Record *where* confidential evidence lives rather than copying it. Consultants should use one workspace per client.

---

## Credits and license

MIT License. See [LICENSE](LICENSE).

The architecture, command patterns, audit rubric structure, and operator framework are adapted from **[AIS-OS](https://github.com/nateherkai/AIS-OS)** by Nate Herk (MIT). *The Three Ms of AI™* and *The Four Cs of an AI OS™* are trademarks of Nate Herk, used here with attribution. Source provenance, quote validation, source acceptance, and the review routine are adapted from an AI OS implementation playbook used as a supplementary source. The discovery questions draw on NIST's small-business cybersecurity guidance and ISO 31000's approach of tying risk management to business objectives.
