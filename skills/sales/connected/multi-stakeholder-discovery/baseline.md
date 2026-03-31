---
name: multi-stakeholder-discovery-baseline
description: >
  Multi-Stakeholder Discovery Process — Baseline Run. First always-on automation for multi-stakeholder
  discovery: automated stakeholder mapping triggers, post-call insight extraction, consensus tracking,
  and engagement gap alerting across all active deals at Connected stage.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=80% of complex deals (3+ stakeholder roles) have automated stakeholder maps, post-call extraction running, and consensus score >=50 within 2 weeks"
kpis: ["Stakeholder mapping automation rate", "Post-call extraction completion rate", "Average consensus score across pipeline", "Discovery coverage (% stakeholders engaged per deal)"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
drills:
  - stakeholder-discovery-call
  - stakeholder-consensus-tracker
  - threshold-engine
---

# Multi-Stakeholder Discovery Process — Baseline Run

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

First always-on automation for multi-stakeholder discovery. The agent automatically processes every discovery call transcript to extract per-stakeholder sentiment, tracks consensus across deals, and alerts when critical stakeholder gaps exist. The founder still runs discovery calls manually, but everything before and after the call is automated. Results should hold over 2 continuous weeks.

**Pass threshold:** >=80% of complex deals have automated stakeholder maps, post-call insight extraction running, and consensus score >=50 within 2 weeks.

## Leading Indicators

- Fireflies webhook triggers post-call extraction within 15 minutes of every discovery call ending
- Per-stakeholder sentiment, priorities, and concerns are auto-populated in Attio after each call
- Consensus scores recompute after every stakeholder interaction
- Gap alerts fire when a deal at Connected+ is missing the Economic Buyer or has <3 stakeholders engaged
- Question sets auto-refresh with new intelligence after each call
- Deals with higher consensus scores progress faster than deals with lower scores

## Instructions

### 1. Deploy Automated Post-Call Extraction

Run the `stakeholder-discovery-call` drill in always-on mode:

**Set up the Fireflies webhook in n8n:**
1. Create an n8n workflow triggered by the Fireflies `TRANSCRIPTION_COMPLETED` webhook
2. When a transcript arrives: match the meeting to a deal in Attio (by company name or attendee email)
3. Pull the deal's stakeholder map from Attio
4. Run the `stakeholder-sentiment-extraction` fundamental: extract per-stakeholder sentiment, support level, priorities, concerns, consensus areas, conflict areas
5. Run the `fireflies-action-items` fundamental: extract and attribute action items
6. Compare answers to the pre-call discovery questions (from the `discovery-question-bank` notes)
7. Update each stakeholder's Attio record with extracted data
8. If this is a repeat interaction with a stakeholder, detect sentiment changes and flag degradations
9. Route follow-up actions: create Attio tasks for unresolved items, flag emerging blockers

**Test the automation:** Run 3-5 discovery calls and verify the extraction pipeline produces accurate, useful output. Spot-check extracted sentiments against your own read of the calls. If accuracy is <80%, tune the extraction prompt.

### 2. Deploy Consensus Tracking

Run the `stakeholder-consensus-tracker` drill:

**Set up automated consensus computation:**
1. Create an n8n workflow triggered when any stakeholder attribute changes in Attio (via Attio webhook)
2. Recompute the consensus score for the affected deal
3. Store the new score on the deal record with timestamp
4. Log to PostHog: `consensus_score_computed` with deal_id, score, level, stakeholder_count

**Set up the monitoring workflow:**
1. Create an n8n workflow on a twice-weekly cron (Monday and Thursday)
2. For each deal at Connected+ stage, compare current consensus score to last computation
3. If score dropped >5 points: generate a diagnosis (which stakeholder changed?) and alert
4. If score dropped >15 points: urgent alert with intervention recommendation
5. Route alerts to Slack or email

**Set up the pre-proposal gate:**
1. Create an n8n workflow triggered by deal stage changes
2. If a deal moves toward Proposed and consensus score < 60: send a warning that the deal may be premature for proposal
3. If the Economic Buyer has not had a direct discovery conversation: flag as high risk

### 3. Automate Stakeholder Gap Detection

Build an n8n workflow on a daily cron:
1. For each deal at Connected+ stage for >7 days, check stakeholder coverage
2. Alert if: no Economic Buyer identified, <3 roles engaged, or any stakeholder with influence_score >= 7 is unengaged
3. For each gap, recommend the specific action: "Run stakeholder-map-assembly to find the Economic Buyer" or "Request an introduction to the technical team through your Champion"

### 4. Monitor for 2 Continuous Weeks

Let the automations run across all active deals. Track:
- How many deals get auto-processed correctly
- How often consensus scores update
- How many gap alerts are generated and acted on
- Whether deals with higher consensus scores actually progress faster

### 5. Evaluate Against Threshold

Run the `threshold-engine` drill:
- Count deals where: stakeholder map exists, post-call extraction ran at least once, and consensus score >= 50
- Divide by total complex deals (3+ stakeholders possible based on company size)
- Pass threshold: >=80% of complex deals meet all three criteria

If PASS: Automations are working reliably. Proceed to Scalable.
If FAIL: Diagnose — is the issue transcript quality (Fireflies missing speakers?), extraction accuracy (Claude misclassifying sentiment?), or coverage (not enough discovery calls happening)?

## Time Estimate

- 4 hours: Build and test the Fireflies webhook n8n workflow for post-call extraction
- 3 hours: Build and test consensus tracking n8n workflows (computation + monitoring)
- 2 hours: Build gap detection and pre-proposal gate workflows
- 2 hours: Test all automations with live discovery calls
- 7 hours: Run discovery calls over 2 weeks (founder's manual time)
- 2 hours: Threshold evaluation, accuracy auditing, and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — stakeholder data, deal tracking, consensus scores | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — stakeholder mapping for new deals entering pipeline | $185/mo (Launch) — [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies | Transcription — discovery call recording and webhook trigger | $10/user/mo (Pro, annual) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — consensus tracking, event logging | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — post-call extraction, consensus monitoring, gap alerts | $24/mo (Starter) or $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — sentiment extraction, question generation | Usage-based, ~$3/MTok input (Sonnet 4.6) — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost this level:** ~$70-120/mo incremental. Primary cost: n8n Pro ($60), Fireflies Pro ($10/user), Anthropic API (~$10-30/mo for extraction across all calls).

## Drills Referenced

- `stakeholder-discovery-call` — automated post-call workflow: transcript retrieval, per-stakeholder sentiment extraction, concern mapping, CRM updates, and follow-up routing
- `stakeholder-consensus-tracker` — continuous consensus score computation, degradation detection, intervention recommendations, and pre-proposal gate checking
- `threshold-engine` — evaluate automation effectiveness against the pass threshold
