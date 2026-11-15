# Connections

This is the list of systems the GRC AI OS can reach for evidence and context. `/start` fills it from questions G9, S1, and S4, and you add to it as you wire new systems. `/audit` checks coverage, how each domain is accessed, and whether there is recent proof that reads succeed.

| # | Domain | Tool | Mechanism | Access scope | Last successful read | Guide |
|---|---|---|---|---|---|---|
| 1 | Identity & access (IdP, SSO, MFA) | _filled by /start_ | not yet connected | - | - | - |
| 2 | Cloud infrastructure | _filled by /start_ | not yet connected | - | - | - |
| 3 | Endpoints / MDM | _filled by /start_ | not yet connected | - | - | - |
| 4 | HR / people (joiners, leavers, training) | _filled by /start_ | not yet connected | - | - | - |
| 5 | Ticketing / change management | _filled by /start_ | not yet connected | - | - | - |
| 6 | Code & CI/CD | _filled by /start_ | not yet connected | - | - | - |
| 7 | Vulnerability & security monitoring | _filled by /start_ | not yet connected | - | - | - |
| 8 | GRC platform / evidence store | _filled by /start_ | not yet connected | - | - | - |
| 9 | Documents & policies | _filled by /start_ | not yet connected | - | - | - |
| 10 | Communication & calendar | _filled by /start_ | not yet connected | - | - | - |

**Mechanism options:** `mcp` (MCP server), `script` (a script in `scripts/` that calls an API), `export` (a regular CSV or JSON export dropped into `sources/`), `manual` (a person pulls the evidence on a schedule), `not yet connected`.

**Rules:**
- **Read-only by default.** Grant write access only after a workflow has proven it needs it, and record that scope here.
- Use a dedicated service identity with the minimum scope, never a personal account (the Intern Rule in `references/operating-principles.md`).
- Keep credentials in `.env` (gitignored) or a secrets manager. Never put them in Markdown.
- When you connect a system, also write `references/<tool>-guide.md` with the endpoints, auth method (no secrets), useful queries, and known limits. Research it once and keep it.
- Mark a domain `n/a` with a reason if it truly does not apply. Being disconnected is not a reason.
