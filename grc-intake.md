# GRC AI OS Intake

This file is the source of truth for `/start`. You can fill it in three ways: type answers here, dictate them, or run `/start` for a guided interview that saves each answer as you go. However you do it, `/start` reads this file to build your context, program registers, and operating manual.

**Format:** up to 5 questions about you and your starting point, then 12 program discovery questions in three rounds of about 10 minutes each. You can stop between rounds and pick up later. Run `/start` again whenever you edit this file.

**For every program answer, record three things:**
- **Owner:** the person accountable for this area
- **Evidence:** a document, system, or record that supports the answer (put copies of documents in `sources/`)
- **Decision / action:** what the answer means you will do

**If you don't know an answer,** write `Unknown`. `/start` turns it into a discovery action with an owner and a due date in `program/actions.md`. An honest "unknown" is more useful than a guess.

**If a document already answers a question** (a SOC 2 report, a policy set, a past security questionnaire, an MSA), put it in `sources/` and write `See sources/<file>.md`. `/start` will read it and cite it instead of asking you.

---

## Round 0 - You and your starting point

### S1 - Who are you, and how do you work in GRC?

Give your role and title. Say whether you are in-house, a consultant/vCISO serving clients, or an internal auditor. Name the organization this workspace is for, and who reviews or approves your GRC work.

```
[Your answer here]
```

### S2 - Paste one or two things you have written recently. Do not edit them.

For example an executive update, a policy excerpt, an audit response, or a security questionnaire answer. **Paste the original text.** Text typed during the interview is already shaped by the conversation, so it doesn't capture your real voice.

```
[Sample 1 - paste raw]
```

```
[Sample 2 - paste raw]
```

### S3 - Is this an existing GRC program, or are you starting GRC from scratch?

Choose one: **existing** (policies, controls, or an audit or certification already in place), **partial** (some pieces exist but no running program), or **from scratch**. Briefly say what already exists. This shapes the rest of the interview: an existing program is documented from its evidence, and a new one is designed from your answers.

```
Answer:
What already exists:
```

### S4 - Which GRC and evidence tools do you already use?

List the tools you have, even if they are not yet connected to this workspace. Examples: GRC or compliance automation platforms (Vanta, Drata, Secureframe, OneTrust, ServiceNow GRC, AuditBoard), cloud providers (AWS, Azure, Google Cloud), identity (Okta, Entra ID, Google Workspace), ticketing (Jira, ServiceNow), code (GitHub, GitLab), and spreadsheets or documents (Google Sheets, Excel, SharePoint, Confluence). For each, say what it holds (controls, evidence, risks, vendors, policies). **Never paste credentials or API keys.**

```
Tool | What it holds | Who administers it
```

### S5 - (Existing or partial programs only) Do you have a system description?

A system description explains the in-scope system: services, infrastructure, software, people, data, processes, and boundaries. It is often Section III of a SOC 2 report or part of an ISO 27001 scope statement. If you have one, put a copy in `sources/` and write `See sources/<file>.md`. `/start` will read it to pre-fill scope, crown jewels, and data flows. Skip this question if you are starting from scratch.

```
Answer:
```

---

## Round 1 - Purpose and obligations

### G1 - What business outcomes must GRC support over the next 12 to 24 months, and how will leadership judge success?

Examples: winning enterprise deals, fundraising, entering a new market, passing a regulator exam, customer trust. Then say how leadership will measure whether GRC is helping (deal cycle time, audit result, incident rate, questionnaire turnaround) and how often they will review it.

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G2 - Which frameworks, certifications, or assurance reports do you maintain or plan to pursue, and by when?

Examples: SOC 2 Type I or II, ISO 27001, NIST CSF, PCI DSS, HITRUST, CMMC, ISO 42001. Include any audit dates already booked.

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G3 - Which laws and regulations apply, and what security, privacy, or compliance commitments have you already made?

Base the laws on your industry, locations, customers, and data. Commitments include contract clauses, DPAs, BAAs, trust page statements, past questionnaire answers, and insurer or investor attestations. **Legal must validate the regulatory list.** Until then, `/start` marks those rows as drafts.

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G4 - What should the initial program cover, and what is deliberately out of scope?

Consider business units, products, locations, and risk domains: security, privacy, operational, financial, ethical, and AI.

```
Answer:
Owner:
Evidence:
Decision / action:
```

---

## Round 2 - What you are protecting and from what

### G5 - Which processes, systems, and assets are most critical, and what would their disruption or compromise cost?

Your crown jewels. Include rough recovery expectations if you know them (how long you can be down, and how much data you can lose).

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G6 - What sensitive data do you collect, where does it flow, who can access it, and when is it deleted?

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G7 - What are your most significant risks, and what have incidents, near misses, audits, pen tests, or customer assessments already shown?

Base this on real events where you can.

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G8 - Who sponsors and owns the program, how much risk will leadership accept, and who can accept remaining risk or approve exceptions?

Include who settles competing priorities and how overdue remediation gets escalated. If no escalation rule exists, `/start` proposes a default for you to confirm.

```
Answer:
Owner:
Evidence:
Decision / action:
```

---

## Round 3 - How the program runs

### G9 - Which policies and controls already work in practice, what evidence shows it, and where does that evidence live?

Name the systems that hold evidence (build on the tools you listed in S4: identity provider, cloud console, MDM, HR system, ticketing, code repository, GRC platform, shared drive) and which evidence collection you would most like to automate.

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G10 - Which vendors and partners could materially affect your data, operations, or compliance, and how are they assessed today?

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G11 - How would you detect, escalate, respond to, and recover from a major incident, and when were those plans last tested?

```
Answer:
Owner:
Evidence:
Decision / action:
```

### G12 - What must you achieve in the first 90 days and the first year, with what budget, people, and tools, and what could block delivery?

Also say where you will need outside support (auditor, legal counsel, pen testers, a vCISO).

```
Answer:
Owner:
Evidence:
Decision / action:
```

---

## Deep-dive topics (after Day 1)

These topics matter, but they are too detailed for the first session. Run `/start deep-dive <topic>` once the core program exists. Each one asks 3 to 5 focused questions and updates the matching register.

| Topic | Covers | Updates |
|---|---|---|
| `workforce` | Joiner, mover, and leaver process for staff and contractors; access changes; security training; how people report concerns | controls, actions |
| `change-and-ai` | Risk checkpoints in product development, technology changes, AI adoption, and business expansion | controls, risks, governance |
| `evidence-automation` | Which evidence can be collected automatically, from which system, and how often | controls, connections |
| `metrics` | KPIs and KRIs for leadership reporting, with sources and targets | governance |
| `continuity` | BCP/DR detail, tabletop exercise history, recovery test results | scope, risks, actions |
| `questionnaires` | Standard answers for customer security questionnaires, with evidence for each claim | references, obligations |

---

When this file is complete, run `/start` (or run it again). It creates `context/`, `references/voice.md`, `references/eval-questions.md`, the filled `program/` registers, an updated `connections.md`, and a personalized `CLAUDE.md`.
