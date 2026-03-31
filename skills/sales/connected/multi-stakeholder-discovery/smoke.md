---
name: multi-stakeholder-discovery-smoke
description: >
  Multi-Stakeholder Discovery Process — Smoke Test. Map the buying committee at 5 active deals,
  classify stakeholder roles, generate tailored discovery questions, and run discovery calls with
  each stakeholder group. Validate that multi-threaded discovery produces stronger consensus and
  faster deal progression than single-threaded deals.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=3 of 5 test deals achieve consensus score >=60 with >=3 stakeholder roles engaged per deal in 1 week"
kpis: ["Stakeholder roles mapped per deal", "Discovery call completion rate by role", "Consensus score achieved", "Deal progression rate (test vs control)"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
drills:
  - stakeholder-map-assembly
  - discovery-question-bank
  - threshold-engine
---

# Multi-Stakeholder Discovery Process — Smoke Test

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Prove that mapping multiple stakeholders, tailoring discovery questions per role, and engaging diverse buying committee members produces a measurable consensus signal and faster deal progression. At this level, the agent handles research, mapping, and question generation — the founder runs the discovery calls manually. No automation, no always-on workflows.

**Pass threshold:** >=3 of 5 test deals achieve a consensus score >=60 with >=3 distinct stakeholder roles engaged per deal in 1 week.

## Leading Indicators

- Stakeholder maps produced for all 5 deals with >=4 contacts per account classified into roles
- At least 1 Economic Buyer or Influencer identified at each account (not just the initial contact)
- Discovery question sets generated for each stakeholder, with must-ask questions specific to their role
- Discovery calls completed with >=3 stakeholder groups per deal
- Consensus areas and conflict areas documented after each call
- Test deals show any forward movement (new meeting booked, additional stakeholder engaged, proposal requested) relative to control deals

## Instructions

### 1. Select 5 Active Deals for the Test

Query Attio for 5 deals currently at the "Connected" stage. Choose deals that are:
- At companies with 50+ employees (enough organizational complexity for multi-stakeholder dynamics)
- Currently single-threaded (only 1-2 contacts engaged so far)
- Similar in deal size (to control for value differences)

Log these 5 deals as the test cohort. Identify 5 comparable single-threaded deals as the control group (run no multi-stakeholder discovery on these).

### 2. Run Stakeholder Map Assembly

Run the `stakeholder-map-assembly` drill for each of the 5 test deals:
- Research the org chart at each target company using Clay
- Find 15-25 people at Director+ level in relevant departments
- Classify each contact into buying committee roles: Economic Buyer, Champion, Influencer, Blocker, End User, Gatekeeper
- Score influence level (1-10) for each stakeholder
- Push all contacts to Attio with role, confidence, and influence score
- Generate a gap report identifying missing roles

Review the output for each deal. For each account, identify the 3-5 highest-priority stakeholders to engage in discovery (prioritize: Economic Buyer, then Influencer, then Champion candidates).

### 3. Generate Discovery Questions

Run the `discovery-question-bank` drill for each prioritized stakeholder:
- Generate 8-12 role-specific discovery questions per stakeholder
- Prioritize into must-ask, should-ask, nice-to-ask
- Each question includes the rationale and signal interpretation (what a good vs bad answer looks like)
- Store the question sets in Attio as notes tagged `discovery-prep`

Review the questions before each call. Adjust any that do not fit the specific deal context.

### 4. Execute Discovery Calls

**Human action required:** The founder personally runs discovery calls with each stakeholder group. This is intentionally manual — the goal is to test whether multi-stakeholder discovery produces better outcomes before investing in automation.

For each deal, schedule and run 2-3 discovery calls targeting different stakeholder groups:
1. Use the generated questions as the call guide
2. Record each call with Fireflies
3. After each call, note which stakeholders participated and your initial read on their sentiment
4. If a stakeholder reveals a new contact ("you should also talk to our security team"), add them to the map

### 5. Process Discovery Call Insights

After each call, manually extract:
- Per-stakeholder sentiment (Positive, Neutral, Cautious, Negative)
- Per-stakeholder support level (Champion, Supporter, Neutral, Skeptic, Blocker)
- Top priorities and concerns per stakeholder
- Consensus areas (where stakeholders agree)
- Conflict areas (where stakeholders disagree)
- Unresolved questions that need follow-up

Log all of this in Attio on the deal record. Use the fields: `stakeholder_sentiment`, `stakeholder_support_level`, `stakeholder_priorities`, `stakeholder_concerns`.

### 6. Compute Consensus Scores

For each deal, compute a consensus score by hand using the formula:
- Assign influence weights by role (Economic Buyer 0.35, Champion 0.25, Influencer 0.15, End User 0.10, Blocker 0.10, Gatekeeper 0.05)
- Assign support scores (Champion=100, Supporter=75, Neutral=50, Skeptic=25, Blocker=0)
- weighted_score = sum(influence_weight * support_score) for each stakeholder
- Subtract penalties for unengaged stakeholders and conflict areas
- Store the score on the deal record in Attio (`consensus_score` field)

### 7. Evaluate Against Threshold

Run the `threshold-engine` drill to compare test vs control:
- Count deals where consensus score >= 60 with >= 3 stakeholder roles engaged
- Compare deal progression for test deals vs control deals over the same week
- Pass threshold: >=3 of 5 test deals achieved consensus score >=60 AND test deals showed meaningful forward movement

If PASS: Multi-stakeholder discovery validated. Proceed to Baseline.
If FAIL: Diagnose — was the issue mapping (wrong people identified), questions (wrong angle for the role), access (couldn't get meetings with key stakeholders), or timing (not enough time for multiple calls)?

## Time Estimate

- 1 hour: Select test and control deals, configure Attio fields
- 2.5 hours: Run stakeholder map assembly across 5 deals (Clay enrichment + classification)
- 1 hour: Generate and review discovery question sets
- 2 hours: Execute 10-15 discovery calls (15-20 min each)
- 0.5 hours: Extract insights and compute consensus scores
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, stakeholder attributes, notes | Free (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — org chart research, people search, role inference | $185/mo (Launch, 2.5K data credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Analytics — event tracking for threshold evaluation | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Fireflies | Transcription — discovery call recording | Free (800 min/mo) or $10/user/mo (Pro, annual) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |

**Estimated play-specific cost this level:** $0 incremental if Clay and Attio are already in your stack. If Clay is new: ~$185/mo.

## Drills Referenced

- `stakeholder-map-assembly` — map all buying committee contacts at each target account, classify into roles, score influence, and identify gaps
- `discovery-question-bank` — generate tailored discovery questions for each stakeholder based on their role, with signal interpretation for each answer
- `threshold-engine` — evaluate test results against the pass threshold using Attio and PostHog data
