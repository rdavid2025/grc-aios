---
sources: []
updated: TBD
status: draft
---
# Governance

`/start` fills this from questions G1 and G8. It sets out who sponsors the program, who makes which decisions, how much risk is acceptable, and how results are reported.

## Sponsor and decision rights

- **Executive sponsor:** {{Name, role}}
- **Program owner:** {{Name, role}}
- **Settles competing priorities:** {{Name or forum}}

| Decision | Who can make it | Threshold / limit | Escalates to |
|---|---|---|---|
| Accept a risk | {{role}} | {{e.g. residual rating Medium or below}} | {{role}} |
| Approve a policy exception | {{role}} | {{e.g. maximum 6 months}} | {{role}} |
| Approve a new tier-1 vendor | {{role}} | {{limit}} | {{role}} |
| Publish an external security or compliance statement | {{role}} | {{limit}} | {{role}} |

## Risk appetite

{{One short paragraph for each relevant domain (security, privacy, operational, compliance), in leadership's own words.}}

**Rating scale:** {{e.g. Likelihood 1-5 x Impact 1-5. Low 1-6, Medium 8-12, High 15-25.}}

## Ownership (RACI summary)

| Area | Accountable | Responsible | Consulted |
|---|---|---|---|

## Remediation and escalation

This default applies until leadership sets its own rule. Every finding becomes an action in [actions.md](actions.md) with an owner and a due date. High findings are due within 30 days, Medium within 90, and Low within 180. Overdue High actions go to the program owner every week, and to the sponsor once they are 14 days late.

## Success measures and reporting

| Measure | Why leadership cares | Target | Reviewed by | Frequency |
|---|---|---|---|---|

## Review cadence

| Review | Frequency | Owner |
|---|---|---|
| Program pulse (`python scripts/grc_os.py review`) | Weekly | {{owner}} |
| `/audit` of the GRC AI OS | Weekly during setup, then monthly | {{owner}} |
| Risk register review | Monthly | {{owner}} |
| Exception review | Monthly | {{owner}} |
| Vendor reviews by tier | Tier 1 yearly, Tier 2 every 2 years | {{owner}} |
| Leadership report | Quarterly | {{owner}} |
