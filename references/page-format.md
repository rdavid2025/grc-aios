# Knowledge page format

Knowledge pages are prose pages in `context/`, `program/`, and `references/`. Use this format for every one so a reviewer, auditor, or new session can trace each statement back to its evidence.

```markdown
---
title: Access management
sources: ["sources/access-control-policy-2026.md"]
updated: 2026-11-13
status: draft
---
# Access management

Fact: Production access requires MFA.

> "All production access requires multi-factor authentication." - sources/access-control-policy-2026.md

Interpretation: The policy covers production only, so staging access may not need MFA.

Open question: Does the MFA requirement cover break-glass accounts? Owner: IT lead. See action A-012.
```

## Rules

| Kind of statement | How to write it |
|---|---|
| **Fact** | Cite the source: a frontmatter `sources:` entry, a link, or an exact quote. Include the source's date where it matters. |
| **Interpretation** | Start with `Interpretation:` and give the reasoning. |
| **Open question** | Start with `Open question:` and name an owner. Add a discovery action to `program/actions.md`. |
| **Conflict** | Keep both claims, each with its date and source. Don't resolve it silently. |

- **Quotes** use exactly `> "text" - sources/file.md` (a hyphen or em dash before the path). `python scripts/grc_os.py lint` fails if the text does not appear in that source. Whitespace and curly quotes are normalized, but nothing else is.
- **`status`** is `draft` or `approved`. It is a label, not an approval workflow. Only a human sets `approved`.
- **`updated`** is the date someone last checked the content, not just the date it was last edited.
- Registers (tables in `program/`) use the columns already in each file. Dates are always `YYYY-MM-DD`. Leave a cell blank, or write `TBD`, rather than guessing.

## Accepting a source

When you add or revise a document in `sources/`:

```bash
python scripts/grc_os.py status          # lists new and changed sources and the pages that cite them
python scripts/grc_os.py lint            # must report no errors
python scripts/grc_os.py accept sources/<file>.md
```

If an accepted source changes, `accept` refuses until you name every page that cites it with `--reviewed <page>`. A changed policy can't quietly leave stale summaries behind. Commit the reviewed batch with Git afterwards.
