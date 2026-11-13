# Obligations register

Lists every framework, law, regulation, contract clause, and public commitment the program must meet. `/start` fills it from questions G2 and G3. Legal and regulatory rows stay **draft until Legal validates them**. Record who validated each one in the Status column.

**Types:**
- `framework`: SOC 2, ISO 27001, NIST CSF, PCI DSS
- `law`: GDPR, HIPAA, CCPA/CPRA, sector regulators
- `contract`: MSA/DPA clauses, customer security addenda, BAAs
- `commitment`: trust page, past questionnaire answers, insurer attestations, investor representations

| ID | Obligation | Type | Applies because | Owner | Deadline | Status | Source |
|---|---|---|---|---|---|---|---|

**Status values:** `planned`, `in progress`, `met`, `at risk`, `draft - needs Legal validation`.
**Deadline:** `YYYY-MM-DD` or `TBD`. `python scripts/grc_os.py pulse` flags deadlines that have passed or are coming up.
