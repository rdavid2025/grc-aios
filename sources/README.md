# Sources

Original documents that support the knowledge pages and registers: policies, audit reports, SOC 2 reports, contracts, DPAs, questionnaires, pen test summaries, regulator guidance, and meeting decisions.

## Rules

1. **Markdown only.** Convert PDFs, Word files, and spreadsheets to readable Markdown first, and check the conversion. The validator does not run OCR or parse binary formats.
2. **Every source starts with provenance frontmatter.** `python scripts/grc_os.py lint` warns when any of these fields is missing:

   ```markdown
   ---
   title: Information Security Policy
   owner: CISO
   origin: Policy portal POL-001 (or a URL)
   version_date: 2026-03-01
   captured: 2026-11-13
   confidentiality: internal
   ---
   ```

3. **Sources are evidence, not opinions.** Don't save AI-generated summaries here. If you approve a decision that came out of an AI draft, save it as a dated decision note in your own words, for example `sources/2026-11-13-decision-mfa-scope.md`.
4. **Revise deliberately.** After you change an accepted source, run `python scripts/grc_os.py status` to see which pages need review, then `accept` again with `--reviewed`.
5. **Confidential material.** Prefer recording *where* a confidential document lives (in `controls.md` or `connections.md`) over copying it here. If you must keep a local copy that should never reach Git, put it in `sources/private/`, which is gitignored.
6. **Keep the repository private.** Even without confidential files, this workspace describes your risks and control gaps.

Suggested names: `<yyyy-mm-dd>-<short-title>.md`, for example `2026-03-01-information-security-policy.md`.
