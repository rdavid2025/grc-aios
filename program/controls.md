# Control baseline and evidence

`/start` fills this from question G9. It records which controls actually operate and where their evidence lives, linking obligations to proof.

| ID | Control | Framework refs | Owner | Evidence | Evidence location | Last evidence | Frequency | Status |
|---|---|---|---|---|---|---|---|---|

**Frequency:** `continuous`, `daily`, `weekly`, `monthly`, `quarterly`, `semiannual`, `annual`. The pulse check compares this with **Last evidence** to flag evidence that has gone stale.
**Status:** `operating`, `partially operating`, `designed - not evidenced`, `not implemented`, `not applicable`, `retired`.

**Evidence rules:**
- Missing evidence is a gap in proof. It does not show that the control failed.
- A vendor's SOC 2 report or marketing claim does not show that *your* organization implemented the control.
- Record where the evidence lives (system, folder, saved ticket query), not the evidence itself. Confidential artifacts stay in their system of record.
