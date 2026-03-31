---
name: qualified-prospect-calls-scalable
description: >
  Founder calls to prospects — Scalable Automation. 10x the prospect volume without
  proportional founder time. Agent automates list refresh, signal-triggered prioritization,
  multi-channel sequencing, A/B testing on every variable, and tool sync. Founder only
  calls the highest-signal prospects; everything else runs on autopilot.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "Meeting rate ≥ 1.6% over 2 months at 200-500 prospects/month volume"
kpis: ["Meeting rate", "Connect rate", "Meetings booked per week", "Cost per meeting", "Pipeline value per month", "Founder hours per meeting booked"]
slug: "qualified-prospect-calls"
install: "npx gtm-skills add sales/qualified/qualified-prospect-calls"
drills:
  - signal-detection
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
  - cold-call-framework
  - meeting-booking-flow
  - threshold-engine
---

# Founder Calls to Prospects — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Sustain a 1.6% or higher meeting rate while scaling to 200-500 prospects per month. The founder's call time stays constant or decreases while total meetings increase — automation handles list building, sequencing, follow-up, and A/B testing. The founder only makes calls to the top-tier, signal-triggered prospects.

## Leading Indicators

- Automated list refresh produces 50+ new scored prospects per week without manual work
- Signal-detected prospects convert to meetings at 2x the rate of non-signal prospects
- A/B tests on email subject lines, call times, and LinkedIn messaging produce statistically significant winners within 2 weeks
- Tool sync workflows run with < 1% error rate (no data falling between systems)
- Founder hours per meeting booked decreases month over month

## Instructions

### 1. Deploy continuous signal-based prospecting

Run the `signal-detection` drill to configure always-on signal monitoring in Clay:

- **Job change signals**: New VP/C-level hires at target accounts (Clay + LinkedIn enrichment, refreshed daily)
- **Funding signals**: Series A-C closed in last 60 days (Clay + Crunchbase enrichment, refreshed weekly)
- **Hiring signals**: 3+ open roles in your product's domain (Clay + job board scrapers, refreshed weekly)
- **Technology signals**: Adopted a complementary tool or churned from a competitor (Clay + BuiltWith, refreshed monthly)

Each signal fires a webhook to n8n which scores the prospect, enriches with phone number, and routes to the appropriate call tier in Attio:

- **Tier 1 (score 80+, strong signal)**: Goes to founder's call list. Max 10 per week.
- **Tier 2 (score 60-79, moderate signal)**: Goes to automated email + LinkedIn sequence. Founder calls only if they engage.
- **Tier 3 (score 40-59, weak signal)**: Goes to email-only nurture. No call unless they respond.

### 2. Build the automated multi-channel sequencing engine

Run the `follow-up-automation` drill to create n8n workflows that orchestrate the full cadence without manual intervention:

**Tier 1 cadence (founder calls):**
- Day 0: Email 1 (pre-warm) auto-sent via Instantly
- Day 0: LinkedIn connection request auto-sent
- Day 3: Founder call (agent creates the call brief in Attio, sends Slack notification to founder's call queue)
- Day 4: If voicemail or no answer, auto-send follow-up email referencing "tried to reach you"
- Day 7: If no response on any channel, auto-send Email 3 with Cal.com link
- Day 10: LinkedIn follow-up message if connected
- Day 14: Breakup email

**Tier 2 cadence (automated with optional call):**
- Day 0-14: Full 4-step email sequence via Instantly + 3-step LinkedIn sequence
- If prospect opens email 3+ times or clicks a link: promote to Tier 1 call list
- If prospect replies positively on any channel: route to Attio deal + Slack alert

**Tier 3 cadence (email only):**
- 4-step email sequence via Instantly
- If engagement detected: promote to Tier 2

### 3. Connect your full tool stack

Run the `tool-sync-workflow` drill to build bidirectional sync workflows in n8n:

- Clay enriched contacts -> Attio contacts (new records + enrichment updates)
- Instantly email events (sent, opened, replied, bounced) -> PostHog events + Attio activity log
- LinkedIn connection/message events -> Attio activity log (manual log via n8n form or LinkedIn export)
- Cal.com bookings -> Attio deals at "Meeting Booked" stage + PostHog `qpc_meeting_booked` event
- Attio deal stage changes -> PostHog events for funnel tracking
- PostHog engagement signals -> n8n tier promotion triggers

Run the `meeting-booking-flow` drill to ensure all Cal.com bookings auto-create deals and send prep materials.

Verify sync integrity: after setup, run 5 test prospects through the full flow and confirm every event appears in both Attio and PostHog.

### 4. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill. Set up experiments on these variables, one at a time:

**Email variables:**
- Subject line variants (test 2 at a time, 100+ sends per variant before declaring winner)
- Email length: 60 words vs 120 words
- Personalization depth: signal-only vs signal + company research
- CTA type: question vs Cal.com link vs "reply if interested"

**Call variables:**
- Call time: morning (8-10am) vs afternoon (4-5pm)
- Opener style: signal-reference vs mutual connection vs industry insight
- Day of week: Tuesday vs Thursday

**LinkedIn variables:**
- Connection note: with signal reference vs without
- Follow-up timing: Day 3 vs Day 7 after acceptance

Use PostHog feature flags to randomly assign variants. Run each test for minimum 100 prospects per variant. Document every test result in Attio as campaign notes.

### 5. Scale volume to 200-500 prospects per month

With automation handling sequencing and signal detection feeding the list:

- Increase Clay enrichment budget to sustain 50-125 new prospects per week
- Add 2-3 more warmed-up Instantly sending accounts to handle volume (use the `cold-email-sequence` drill warmup process)
- Keep founder call volume capped at 10-15 calls per week (only Tier 1) — this is the leverage point. Automation handles the other 90%+.

Monitor n8n execution logs daily for the first 2 weeks. After that, check weekly. Set up n8n error alerts in Slack.

### 6. Evaluate against threshold

Run the `threshold-engine` drill monthly and at the 2-month mark. Compute:

- Total prospects entered cadence over 2 months
- Total meetings booked (broken down by tier and channel)
- Meeting rate = meetings / total prospects contacted
- Cost per meeting = (tool costs + founder time valued at hourly rate) / meetings
- Founder hours per meeting = total call time / meetings from calls

**Pass: meeting rate >= 1.6% sustained over 2 months.** Proceed to Durable.

**Fail: meeting rate < 1.6%.** Diagnose:
- If Tier 1 (call) meeting rate is high but Tier 2/3 drag the average down: the automation messaging needs work. Run more A/B tests on email and LinkedIn copy.
- If overall volume is high but conversion dropped vs Baseline: you scaled too fast before optimizing. Reduce volume, run A/B tests, then re-scale.
- If signal-detected prospects do not outperform non-signal: your signal definitions are wrong. Revisit which triggers actually predict meetings.

## Time Estimate

- Signal detection + automation setup: 8 hours (agent)
- Tool sync workflows: 4 hours (agent)
- A/B test design + implementation: 6 hours (agent)
- Ongoing monitoring + test analysis: 2 hours/week x 8 weeks = 16 hours (agent)
- Founder call execution: 1.5 hours/week x 8 weeks = 12 hours (human)
- Volume scaling + infrastructure: 4 hours (agent)
- Threshold evaluation: 2 hours (agent)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, deal tracking, activity hub | Pro: $29/user/mo (https://attio.com/pricing) |
| Clay | Enrichment + signal detection + scoring | Pro: $349/mo for 10k credits (https://clay.com/pricing) |
| Instantly | Email sequencing + warmup (3 accounts) | Hypergrowth: $77.6/mo (https://instantly.ai/pricing) |
| Cal.com | Meeting booking | Team: $12/user/mo (https://cal.com/pricing) |
| PostHog | Event tracking + experiments + funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| n8n | Workflow automation | Starter: $24/mo (https://n8n.io/pricing) |
| Apollo | Prospect sourcing at scale | Basic: $49/mo (https://apollo.io/pricing) |
| LinkedIn Sales Navigator | Prospecting + engagement | Core: $99/mo (https://business.linkedin.com/sales-solutions/compare-plans) |

**Estimated play-specific cost at this level:** $350-650/mo

## Drills Referenced

- `signal-detection` — always-on buying signal monitoring and prospect routing
- `follow-up-automation` — n8n workflows for multi-channel cadence orchestration
- `tool-sync-workflow` — bidirectional sync between Clay, Instantly, Attio, PostHog, Cal.com
- `ab-test-orchestrator` — systematic A/B testing on email, call, and LinkedIn variables
- `cold-call-framework` — call script and logging structure for Tier 1 founder calls
- `meeting-booking-flow` — Cal.com booking, CRM sync, and meeting prep automation
- `threshold-engine` — 1.6% meeting rate evaluation at scale
