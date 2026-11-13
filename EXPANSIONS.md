# Expansions: what to add as you grow

The template ships lean on purpose. Add structure only when real work needs it. A GRC OS should look like a well-run program, not an evidence dump.

## Ships with the template (don't remove)

| Item | Purpose |
|---|---|
| `CLAUDE.md` / `AGENTS.md` | One operating manual, plus a bridge for other assistants |
| `grc-intake.md` | Source of truth for `/start` |
| `program/` (9 registers) | Program state. Keep the column headers, because `grc_os.py` relies on them |
| `sources/` | Original documents with provenance |
| `references/` | Page format, operating principles, voice, eval questions |
| `connections.md` | Evidence systems registry |
| `decisions/log.md` | Append-only decisions |
| `archives/` | Retired material |
| `scripts/grc_os.py`, `tests/` | Deterministic checks |
| `.claude/skills/` | `/start`, `/audit`, `/feedback` |

## Add when you need it

| Add | When | Why |
|---|---|---|
| `references/<tool>-guide.md` | You connect an evidence system | Research once, keep it. `/audit` gives credit for reproducible access routes |
| `references/prompts/` | `/feedback` ships a saved prompt (for example a questionnaire drafting prompt) | The lowest-autonomy, most auditable form of automation |
| `references/sops/` | A GRC process is run by someone new (access review, vendor intake) | The OS follows the same steps every time |
| `references/questionnaire-answers.md` | You answer the same customer questions repeatedly | Approved, sourced standard answers. Keep the approval date and evidence for every answer |
| `program/policies.md` | You manage more than a handful of policies | Policy register: owner, version, approval date, next review |
| `program/audits.md` | You run external audits or assessments | Audit calendar, auditor, scope, findings, linked to `actions.md` |
| `scripts/<tool>_export.py` | A connection is easier as a script than an MCP server | Most second connections are scripts. Read-only, with a test |
| `.claude/agents/` | Repeated multi-step research (regulatory scanning, vendor due diligence) | Keeps the main session lean. Only after a prompt version is proven |
| `/grill-me`-style skill | You often need long-form discovery beyond `/start deep-dive` | Adapt it from AIS-OS. Checkpoint every answer |
| `/link`-style skill | You add sources and projects often | Adapt it from AIS-OS. Smallest useful routing edit |
| Hooks (`.claude/settings.json`) | The manual routine works and you want automatic checks | Example: a `SessionStart` hook running `python scripts/grc_os.py status`, or a `PostToolUse` hook on Edit/Write running `lint`. A post-edit hook reports problems *after* an edit and can't undo it, so keep the final review step |
| A separate clone per client or entity | Different confidentiality boundaries | Never mix client material. Share only general methods |

## Don't add

- **Raw exports or email dumps in `sources/`.** Keep interpreted, attributable documents only. Record where bulk evidence lives instead.
- **A second risk list, action list, or decisions file.** One canonical register per concept.
- **`notes/`, `misc/`, `tmp/`, `inbox/`.** These become graveyards. Use `archives/` for old material, or write a real page in the right place.
- **Empty folders "for later".** Wait until the work needs them.
- **AI summaries as sources.** They are not corroboration.
- **A hot cache that copies register figures.** It will go stale. Run `grc_os.py pulse` instead.

## Is it time to add something?

1. Is it conceptually new, or does it fit an existing register?
2. Will you touch it three or more times in the next month?
3. Will a future `/feedback` improvement or `/audit` probe actually use it?

Two yeses: add it. One yes: wait.
