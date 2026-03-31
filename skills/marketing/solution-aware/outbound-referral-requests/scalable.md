---
name: outbound-referral-requests-scalable
description: >
  Outbound Referral Requests — Scalable Automation. n8n workflows automate the full referral
  lifecycle — ask scheduling, follow-ups, intro tracking, and meeting attribution. Crossbeam
  account mapping identifies high-overlap partners. Volume scales to 200+ requests/month while
  maintaining intro rate.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=12% intro rate and >=30 qualified intros/month over 4 months"
kpis: ["Monthly intro volume", "Request-to-intro rate", "Intro-to-meeting rate", "Connector portfolio size", "Automation coverage"]
slug: "outbound-referral-requests"
install: "npx gtm-skills add marketing/solution-aware/outbound-referral-requests"
drills:
  - referral-network-mapping
  - referral-pipeline-automation
  - partner-relationship-scoring
  - referral-ask-copywriting
---

# Outbound Referral Requests — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

Scale outbound referral requests from 70/month to 200+/month via automation while maintaining a >=12% intro rate. n8n workflows handle ask scheduling, follow-ups, intro tracking, and meeting attribution. Crossbeam identifies high-overlap partners who expand your connector network beyond personal relationships. Monthly output: >=30 qualified intros converting to meetings at a rate that sustains pipeline.

## Leading Indicators

- Referral pipeline automation workflows deployed and processing asks within the first 2 weeks
- Connector portfolio expanded to 50+ active connectors (up from the 20-30 used at Baseline)
- Crossbeam connected with at least 3 partners, surfacing 50+ overlapping target accounts
- Automated ask scheduling firing 3-5 asks/day on Tuesday-Thursday without manual intervention
- Intro tracking automatically creating deals in Attio when intros are received
- Weekly referral pipeline summary generating in Slack by end of week 3
- Month 1 intro rate within 20% of Baseline benchmark (indicates automation is not degrading quality)

## Instructions

### 1. Deploy referral pipeline automation

Run the `referral-pipeline-automation` drill to build the n8n workflow suite:

**Ask Scheduling Workflow:**
- Daily cron (9am, Tue-Thu) queries Attio for pairs in "Ask Ready" status
- Selects max 3-5 asks/day, prioritized by composite score
- Routes to Loops (email) or creates Attio task (LinkedIn DM) based on connector preference
- Fires PostHog event `referral_ask_sent` with all properties
- Updates Attio pair status to "Ask Sent"

**Follow-up Workflow:**
- Triggers 7 days after `referral_ask_sent` if no `referral_intro_received` for the same pair
- Sends one gentle follow-up via the same channel
- After 21 total days with no response, marks pair as "No Response" and decrements connector willingness score

**Intro Received Workflow:**
- Triggered manually (founder marks in Attio) or via email parsing
- Creates deal in Attio pipeline, attributes to connector
- Fires PostHog event, sends automated thank-you to connector
- Increments connector's "Total Intros Made" field

**Meeting Attribution Workflow:**
- Fires when `meeting_booked` event has source "Warm Intro"
- Attributes the meeting back to the originating connector in Attio
- Updates deal stage

**Weekly Summary:**
- Friday 4pm n8n cron generates pipeline summary: asks sent, intros received, meetings booked, top connectors, overdue follow-ups
- Posts to Slack

Estimated time: 15 hours for full workflow suite.

### 2. Expand the connector network with Crossbeam

Set up Crossbeam to systematically find new connectors beyond your personal network:

1. Connect Attio to Crossbeam (CSV export of Companies collection, or REST API sync). Create populations: "Customers," "Open Pipeline," and "Target Accounts."
2. Invite 3-5 complementary companies (non-competing, same buyer persona) to connect on Crossbeam. Prioritize companies whose customer base overlaps your target account list.
3. Run overlap reports: identify which of your target accounts are customers of your Crossbeam partners. These partners can make introductions to their own customers — the strongest possible intro path.
4. For each overlap, identify the right person at the partner company to request the intro (account manager, founder, partnerships lead). Add them to Attio as connectors with source "Crossbeam."
5. Feed new Crossbeam-sourced connectors into the `referral-network-mapping` drill for scoring.

Repeat quarterly: invite new partners, re-run overlap reports, expand the connector pool.

Estimated time: 8 hours setup, 2 hours quarterly refresh.

### 3. Scale the referral network map

Run the `referral-network-mapping` drill monthly at Scalable level, now with Clay automation:

1. Set up a Clay workflow that automatically enriches new Attio contacts against target accounts (employment history, mutual connections, board seats)
2. Auto-score new connector-target pairs using Clay formula columns
3. Push scored pairs to Attio via Clay-Attio sync
4. Target: maintain 200+ viable pairs in the pipeline at all times (70+ asks/month x 3-month rolling pipeline)
5. Add new targets monthly from pipeline reviews, lost deals (try a warm intro approach), and Crossbeam overlap reports

Estimated time: 3 hours/month.

### 4. Score and tier your connector portfolio

Run the `partner-relationship-scoring` drill to build the connector scoring system:

1. Score every active connector on 5 dimensions: Response Rate (1-10), Intro Quality (1-10), Deal Conversion (1-10), Response Speed (1-10), Volume Capacity (1-10)
2. Tier connectors: Tier 1 (40-50), Tier 2 (25-39), Tier 3 (10-24), Tier 4 (1-9)
3. Configure Attio fields for all scoring dimensions
4. Build monthly n8n workflow to auto-recalculate scores based on PostHog data
5. Use tiers to prioritize: send highest-value targets to Tier 1 connectors, reserve Tier 3-4 for lower-priority asks

Tiering prevents connector fatigue. Tier 1 connectors are your most valuable asset — never burn them on low-quality targets. Tier 4 connectors should stop receiving asks (move to general network nurture).

Estimated time: 5 hours setup, 1 hour/month maintenance.

### 5. Scale ask generation

Run the `referral-ask-copywriting` drill in batch mode monthly:

1. Pull all new "Ask Ready" pairs from Attio (pairs scored by `referral-network-mapping` but without ask messages yet)
2. Batch-generate asks using Claude with context from Attio (connector relationship, target company/role, previous interaction history)
3. Generate both variants (A and B) for continued A/B testing
4. Auto-store in Attio as connector notes, tagged by target company
5. Quality-check a random 10% sample manually. If quality drops, adjust the generation prompts.

At 200+ pairs/month, manual review of every message is not feasible. Rely on template constraints (100-word ask max, 60-word blurb max) and spot-check sampling.

Estimated time: 2 hours/month.

### 6. Build guardrails for scale

Implement these guardrails in n8n to protect quality as volume increases:

- **Connector frequency cap**: Maximum 2 asks to any single connector per month. Tier 1 connectors: max 3/month. Exceeding this causes fatigue and reduces willingness.
- **Target deduplication**: Never send 2 different connectors an ask for the same target in the same month. Route to the highest-scoring connector only.
- **Intro rate floor**: If the trailing 4-week intro rate drops below 10% (below the 12% target), automatically pause new asks and alert the team. Diagnose whether the issue is connector quality, target selection, or ask quality.
- **Negative response monitor**: If any connector explicitly declines or expresses annoyance, immediately remove them from the ask pipeline and flag for relationship repair.
- **Domain health**: If sending asks via email, monitor deliverability. If bounce rate exceeds 3%, pause email asks and investigate.

Estimated time: 3 hours to configure guardrails.

### 7. Evaluate at monthly cadence

At the end of each month, assess:

- **Monthly intro volume**: >=30 intros? (Target for Scalable pass threshold)
- **Request-to-intro rate**: >=12%? (Holding from Baseline)
- **Intro-to-meeting rate**: Improving, stable, or declining?
- **Connector portfolio health**: How many active Tier 1-2 connectors? Is the pool growing or shrinking?
- **Automation coverage**: What percentage of the lifecycle is automated vs. manual? Target: >80% automated at Scalable.
- **Ask variant performance**: Which variant (A or B) is winning? Rotate the winning variant into default and test new variants.

Pass threshold for Scalable: >=12% intro rate AND >=30 qualified intros/month sustained over 4 consecutive months.

If metrics hold, proceed to Durable. If intro rate is stable but volume is short, expand the connector network (more Crossbeam partners, more network mining). If intro rate is declining, diagnose connector fatigue vs. target quality vs. ask quality.

Estimated time: 2 hours/month.

## Time Estimate

- Referral pipeline automation setup: 15 hours
- Crossbeam setup and partner onboarding: 8 hours
- Monthly network mapping (3 months): 9 hours
- Connector scoring setup and maintenance: 8 hours
- Monthly ask generation (3 months): 6 hours
- Guardrails configuration: 3 hours
- Monthly evaluation (3 months): 6 hours
- Intro handling and relationship management: 20 hours

**Total: ~75 hours over 3 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector portfolio, referral map, deal pipeline, scoring fields | Standard stack (excluded) |
| PostHog | Referral funnel tracking, dashboards, anomaly detection | Standard stack (excluded) |
| n8n | Automation — ask scheduling, follow-ups, intro tracking, weekly summaries | Standard stack (excluded) |
| Clay | Network enrichment at scale — employment history, mutual connections | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Crossbeam | Partner account mapping — find overlapping target accounts | Free tier: 3 seats, basic mapping. Connector: $400/mo. [crossbeam.com/pricing](https://www.crossbeam.com/pricing) |
| Loops | Email delivery for automated referral asks | Free tier sufficient at this volume. [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost: ~$495-895/mo** (Clay Growth $495 + Crossbeam Free-$400)

## Drills Referenced

- `referral-network-mapping` — monthly Clay-enriched network mapping with auto-scoring of connector-target pairs
- `referral-pipeline-automation` — n8n workflow suite: ask scheduling, follow-ups, intro tracking, meeting attribution, weekly summaries
- `partner-relationship-scoring` — monthly connector scoring and tiering to optimize who gets asked for which targets
- `referral-ask-copywriting` — batch ask generation with A/B variants and quality sampling
