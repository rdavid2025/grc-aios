# Design notes

How this template was put together from two AI OS designs and a set of GRC discovery questions, and why each choice was made.

## Inputs

| Input | Role | Strengths | Gaps for GRC |
|---|---|---|---|
| **[AIS-OS](https://github.com/nateherkai/AIS-OS)** (Nate Herk) | **Primary design** | A lean, opinionated structure. An onboarding wizard that writes to a resumable intake file. An evidence-based audit (Four Cs, rubric v2 with caps so a big skill library can't hide missing connections or cadence). Audit history with stable finding IDs. The operator framework (Three Ms: EAD, autonomy levels, Bike Method, Intern Rule, Kill Switch). An append-only decisions log. Clear "what not to add" rules | Built for sales and marketing operators. No concept of evidence provenance, obligations, risk, controls, exceptions, or decision authority. Voice and revenue-centric questions. Six skills (more than needed to start). Duplicate Claude and Codex trees that need a sync script |
| **AI OS Implementation Playbook** (supplementary) | **Evidence and integrity layer** | Source documents with provenance (`raw/`). Knowledge pages that separate fact, interpretation, and open question. A validator that checks quotes against sources and catches broken links. Source fingerprints with an "accept" step that forces re-review of pages citing a changed source. A deterministic daily review script. Five evaluation questions answered from a fresh session. A 7-day pilot. Git revert recovery. Explicit GRC cautions (missing evidence ≠ failed control; a vendor statement ≠ your implementation) | Written around a weekly intelligence brief, not GRC operations. A hot cache (`hot.md`) that duplicates canonical facts. Heavier folder set |
| **20 GRC discovery questions** | **Onboarding content** | Comprehensive coverage based on NIST small-business guidance and ISO 31000. A per-answer triad of owner, evidence, and decision, with unknowns turned into tasks | 20 questions is too many for one sitting. Several overlap. Some are process-design questions better answered with a proposed default than in an interview |

## What was taken from where

| Element | From | Adaptation |
|---|---|---|
| Single root operating manual with a routing table | AIS-OS | Added GRC evidence rules and hard decision boundaries. `AGENTS.md` became a 3-line bridge instead of a duplicate, so there's nothing to keep in sync |
| `/onboard` becomes **`/start`** | AIS-OS | Intake file as source of truth, checkpoint after each answer, one-shot scaffold, idempotent re-runs with backups, voice paste rule, closing "wow" prompt. Now driven by the refined GRC questions, with three rounds and pause points, the owner/evidence/decision triad, unknowns turned into discovery actions, "read the document instead of asking", and deep-dive follow-ups (from AIS-OS `/grill-me`) |
| **`/audit`** | AIS-OS (rubric v2, history, report template) | GRC anchors for all 20 criteria. A new **evidence-integrity gate** (any fabricated quote caps Context at 10). The deterministic validator runs as part of the audit. Autonomy ceilings checked under Capabilities. A **program pulse** that is reported but never scored, keeping OS reliability separate from program health. Cross-runtime compatibility checks reduced to a bridge check |
| `/level-up` + correction capture become **`/feedback`** | AIS-OS `/level-up` + the playbook's "preserve approved decisions" | Two modes. Capture mode routes each correction to the file a future session will read (fact → register/source, preference → manual, defect → skill + test). The weekly loop keeps the Three Ms flow (Mindset candidates → EAD/map/autonomy/measure → Machine build options, Bike Method headers) with GRC KPI buckets (reduce risk / accelerate trust / cut effort) and GRC autonomy ceilings |
| `sources/` with provenance | Playbook (`raw/`) | Renamed for GRC clarity. `sources/private/` is gitignored for confidential copies |
| Fact / Interpretation / Open question page format | Playbook | `references/page-format.md`. The lint enforces quote fidelity and that frontmatter sources exist |
| Validator and fingerprint acceptance | Playbook (`brain.py`) | Rewritten as `scripts/grc_os.py` (standard library only) with GRC register checks: date formats, duplicate IDs, required columns |
| Daily review script | Playbook | `grc_os.py review`, which adds the program pulse and saves to `audits/`. A non-zero exit code makes failures visible in schedulers |
| Five evaluation questions | Playbook | `references/eval-questions.md`, tailored by `/start` and used as `/audit` routing probes. Expected answers stay outside the repo |
| Decisions log, archives, "what not to add" | AIS-OS | The decisions log also records the reasoning behind risk acceptances. Tracking happens in `program/exceptions.md` |
| `connections.md` registry | AIS-OS | GRC evidence domains (identity, cloud, MDM, HR, ticketing, code, vuln/SIEM, GRC platform, docs, comms), read-only and least-privilege rules, `references/<tool>-guide.md` |
| Three Ms framework | AIS-OS | Condensed GRC version in `references/operating-principles.md`, with attribution |

## Deliberately left out

- **Hot cache (`hot.md`).** AIS-OS rubric v2 gives it no credit and warns about duplication and staleness. `grc_os.py status` and `pulse` produce the same "where am I" view straight from canonical data.
- **`/grill-me`, `/link`, `/3d-brain`.** Not core for v1. Deep-dive interviews are part of `/start`, and routing fixes go through `/feedback` (class: routing gap). See EXPANSIONS for when to add them back.
- **Duplicate Codex skill tree and sync script.** Replaced by the `AGENTS.md` bridge.
- **Enabled hooks.** A committed hook would run Python for everyone who clones the template. The session-start check is a line in `CLAUDE.md` instead. Hook setup is described in EXPANSIONS.

## Changes to the 20 discovery questions

The 20 questions became **12 core questions** (G1 to G12), **2 personalization questions** (S1, S2), and **6 deep-dive topics**. Nothing of substance was dropped. Each original question is either merged, moved to a deep-dive, or replaced by a proposed default.

| Original | Now | Why |
|---|---|---|
| 1 Business outcomes | **G1** (merged with 19) | Outcomes and how leadership measures them are one conversation |
| 2 Frameworks / certifications | **G2** | Kept as is. It drives the roadmap and deadlines |
| 3 Legal / regulatory | **G3** (merged with 4) | Both feed one obligations register. Legal validation is flagged explicitly |
| 4 Commitments already made | **G3** | See above |
| 5 Initial scope | **G4** | Kept. AI added as a risk domain |
| 6 Critical processes / assets | **G5** | Kept. Adds recovery expectations |
| 7 Sensitive data | **G6** | Kept |
| 8 Significant risks / what incidents showed | **G7** | Kept. Pen tests added as an evidence source |
| 9 Risk appetite / who accepts risk | **G8** (merged with 10, 12) | Sponsor, ownership, appetite, and acceptance authority are all decision rights |
| 10 Sponsor / owners | **G8** | See above |
| 11 Controls operating + evidence | **G9** (merged with 17) | "What works" and "where's the proof" can't be separated. Also seeds `connections.md` |
| 12 Remediation process | **G8 default** | A process-design question. `/start` proposes a default escalation rule (30/90/180 days) for the user to confirm instead of designing one in the interview |
| 13 Vendors | **G10** | Kept |
| 14 Workforce lifecycle | **Deep-dive: workforce** | Control-level detail. Better after the core program exists |
| 15 Product / change / AI review | **Deep-dive: change-and-ai** | Same. AI adoption now gets its own focus |
| 16 Incident response | **G11** | Kept in the core set because it's often untested and high impact |
| 17 Evidence retention / automation | **G9** + **deep-dive: evidence-automation** | Location in core, automation detail later |
| 18 Budget / people / tools | **G12** (merged with 20) | Capacity only matters against the plan |
| 19 Leadership measures | **G1** + **deep-dive: metrics** | Headline measures in core, KPI/KRI design later |
| 20 90-day and one-year plan | **G12** | Kept with capacity and dependencies |

**New questions:** S1 (who you are: in-house vs consultant vs auditor, and who approves your work, which drives decision boundaries and the one-workspace-per-client rule) and S2 (pasted voice samples, the AIS-OS rule against voice contamination). There are also two more deep-dives: `continuity` and `questionnaires`.

**Starting-point questions (added later):** S3 (existing program, partial, or from scratch, which changes whether answers are documented from evidence or designed), S4 (existing tools such as Vanta, Drata, OneTrust, AWS, or Google Sheets, which seeds `connections.md` and can pre-fill registers from exports), and S5 (system description, existing or partial programs only, which pre-fills scope and data flows).

**Kept from the source document:** for each answer, capture an accountable owner, supporting evidence, and a resulting decision or action. When an answer is unknown, assign a discovery task with a due date.
