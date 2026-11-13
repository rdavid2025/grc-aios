# Evaluation questions

These are the five questions this GRC AI OS must answer correctly from a **fresh session**, without you explaining anything. `/start` replaces the defaults below with versions tailored to your program. `/audit` uses them as its routing probes.

Keep your expected answers **outside this workspace**, for example in a private note. That way the AI can't read the answer key, and grading stays honest.

| # | Question | What a good answer shows |
|---|---|---|
| 1 | {{What does the organization do, for whom, and what must GRC deliver in the next 12 months?}} | Context from `context/` and the program snapshot, with sources |
| 2 | {{What is the status of our next audit or certification milestone, and what is blocking it?}} | The current obligation row, open actions, owners, and dates from the registers |
| 3 | {{What are our top three risks, who owns them, and when were they last reviewed?}} | Rows from the risk register with review dates, and stale reviews flagged |
| 4 | {{Where is the evidence that our quarterly access reviews actually happened?}} | The evidence location and last evidence date from the controls register, with gaps labeled as gaps |
| 5 | {{What did we decide about <a past decision>, and why?}} | The entry in `decisions/log.md` or `exceptions.md`, with the approver and expiry if relevant |

## Grading

For each question, record: correct / partly correct / wrong, whether every material claim had a source, and whether the answer separated fact from interpretation and unknowns. Two consecutive weeks with all five correct and no unsupported claims is a sensible bar for trusting the OS with more work. That bar is a proposed pilot standard, not a published benchmark.
