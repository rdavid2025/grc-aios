# Operating principles: how to think about GRC work with AI

> Adapted for GRC from The Three Ms of AI™ (Mindset, Method, Machine) by Nate Herk, used under the MIT terms of the [AIS-OS](https://github.com/nateherkai/AIS-OS) starter kit. The Three Ms of AI™ is a trademark of Nate Herk. © 2026 Nate Herk.

The weekly `/feedback` loop works through these three layers in order. You don't need to memorize them. They are here so you and the AI apply them the same way.

**Governing rule: boring is beautiful.** Predictable beats clever. In GRC, a deterministic check that always runs is worth more than an impressive agent that sometimes hallucinates.

---

## 1. Mindset: how to think

- **Default shift.** Before doing a GRC task the old way, ask *"To what extent could AI help here?"* The answer is rarely all or nothing. Drafting a policy might be 70% AI. Deciding risk appetite is 0%.
- **Function breakdown.** You don't automate "compliance." You automate one task, such as "map this questionnaire's questions to our control list." Then the next one.
- **Curiosity rule.** Never accept output you can't explain to an auditor. Ask why, ask for the source, and ask what would change the conclusion. If you can't explain how a workflow reached its answer, it is a liability.
- **Expect the dip.** The first two weeks are slower. That's normal.

## 2. Method: how to decide what to improve

1. **Find the constraint.** Two questions:
   - *"If a major customer sent a 300-question security review tomorrow, what would break first?"* This finds bottlenecks.
   - *"What would cut our time-to-assurance in half?"* This finds leverage.
2. **EAD, in this order.**
   - **Eliminate:** *"What happens if we just stop doing this?"* Reports nobody reads and duplicate evidence requests should go. Don't automate waste. Check first that no obligation in `program/obligations.md` requires it.
   - **Automate:** aim for roughly 60% deterministic, 30% AI-drafted with human review, 10% manual.
   - **Delegate:** if it needs judgment, authority, or relationships, give it to a person.
3. **Map the process.** Write down the trigger, data sources, transformations, decision points, and destination. *If you can't explain it to a person, you can't explain it to an AI.*
4. **Pick the autonomy level.** Default to the **lowest** level that works.

| Level | Name | What happens | GRC ceiling |
|---|---|---|---|
| L0 | Manual | No AI | Risk acceptance, exception approval, attestations, legal judgment |
| L1 | Suggested | AI suggests, human decides each step | Risk ratings, control design |
| L2 | Drafted | AI drafts, human reviews and edits | **Maximum for anything external:** questionnaires, policies, customer and auditor responses |
| L3 | Supervised | AI runs, human checks periodically | Evidence freshness checks, register hygiene, internal reminders |
| L4 | Autonomous | AI handles it end to end | Deterministic scripts only (for example `scripts/grc_os.py review`) |

5. **Tie it to a measure.** Every improvement must move a number in one of three buckets:
   - **Reduce risk:** fewer overdue High actions, shorter time to remediate, fewer expired exceptions.
   - **Accelerate trust:** faster questionnaire turnaround, fewer audit findings, shorter deal security reviews.
   - **Cut effort:** fewer hours collecting evidence, fewer repeat requests to control owners.

   If you can't name a bucket and a metric, don't build it.

## 3. Machine: how to build and run it

**Build**
- **Lego principle:** small steps, one input and one output each. Do the non-AI steps first (fetch, format, route), then add AI where judgment helps.
- **Validation chain:** test each step on real output before connecting it to the next. Never build the whole pipeline and test it end to end for the first time.
- **Iteration:** deterministic checks can be finished. AI steps keep needing tuning.

**Operate**
- **Bike method:** every new workflow starts at phase 1 and only moves up when you deliberately edit it.
  1. Training wheels: run by hand and check everything.
  2. Guided: it runs, you review every output before it is used.
  3. Watched: it runs, you sample outputs and get alerts on anomalies.
  4. Hands-off: only for deterministic, low-impact work.
- **Intern rule:** treat the AI like a new hire on day one. It gets its own service identities, read-only by default, never your credentials, and a full audit trail. It never impersonates you.
- **Kill switch:** if a workflow keeps needing patches, produces outputs you don't trust, or costs more than it saves, retire it to `archives/`. Sunk cost is not a reason to keep it.

---

## Principles from the supplementary playbook

- **Provenance first.** Every source records its title, owner, origin, version date, and capture date (`sources/README.md`).
- **The validator is necessary but not sufficient.** A quote that matches its source shows the quote is real. It does not show the source is true or the interpretation is justified.
- **Local fingerprints don't watch the outside world.** `grc_os.py status` notices when *your copy* of a document changes. It cannot tell when a regulator updates guidance. Re-capture fast-changing sources on a schedule.
- **Recover with Git.** If a bad update was committed, run `git log --oneline` and then `git revert <commit>`. History is kept.
