---
name: partnerships-warm-intros-scalable
description: >
  Partnerships & Warm Intros — Scalable Automation. Expand from 20 to 50+ connectors using
  systematic partner discovery, automate the intro request pipeline with n8n workflows,
  and build Crossbeam account mapping to find the highest-overlap partners. 10x intro volume
  without proportional manual effort.
stage: "Sales > Qualified"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 20 intros received and ≥ 16 meetings booked over 2 months"
kpis: ["Intro requests sent", "Intros received", "Meetings booked from intros", "Request-to-intro rate", "Intro-to-meeting rate", "Pipeline value from warm intros"]
slug: "partnerships-warm-intros"
install: "npx gtm-skills add sales/qualified/partnerships-warm-intros"
drills:
  - partner-prospect-research
  - partner-pipeline-automation
  - follow-up-automation
---

# Partnerships & Warm Intros — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

Scale warm intros from a manual process to a systematic, partially automated pipeline. At Scalable, you expand your connector network using data-driven partner discovery, automate the request-to-meeting pipeline, and use Crossbeam account mapping to find connectors with the highest overlap with your target list. The 10x multiplier comes from having more connectors, better targeting, and less manual overhead per intro.

Pass threshold: **>= 20 intros received AND >= 16 meetings booked over 2 months.**

## Leading Indicators

- Active connector count (target: 50+ connectors with at least one request in the last 60 days)
- Automated workflow reliability (target: >95% of events fire correctly)
- New connectors activated per week (target: 3+ per week for first 4 weeks)
- Request-to-intro rate holding or improving vs. Baseline (target: >35%)
- Intro-to-meeting rate holding vs. Baseline (target: >55%)
- Average pipeline value per warm intro meeting (track for ROI calculation)

## Instructions

### 1. Systematically discover new connectors

Run the `partner-prospect-research` drill adapted for warm intro connectors:

**Source connectors from 4 channels:**

1. **Existing network expansion:** Export your full Attio contact list and LinkedIn connections. Use Clay enrichment (`clay-enrichment-waterfall` fundamental) to tag contacts by: industry, seniority, company stage, and network size. Filter for people who overlap with your target prospect list (shared industries, shared company stage, shared geography).

2. **Customer referrals:** Query Attio for happy customers (NPS >= 8, active usage, expanded). These customers know other companies with similar problems. Add them to your connector list with the "Customer" tag.

3. **Investor and advisor network:** If you have investors, ask them for their portfolio company contacts. Each investor connection can unlock 10+ target companies. Add with the "Investor" tag.

4. **Crossbeam account mapping:** Run the `crossbeam-account-mapping` fundamental to find partners whose customer/prospect lists overlap with your target accounts. Partners with high account overlap are the highest-value connectors because their contacts are literally your prospects. Add with the "Crossbeam Partner" tag.

**Target: Build a connector list of 50+ qualified connectors in Attio with:**
- Contact info (email, LinkedIn)
- Connector type (advisor/investor/customer/partner/weak-tie)
- Estimated network overlap with your targets
- Best ask template (A/B/C from Baseline)
- Communication channel preference

### 2. Automate the intro request pipeline

Run the `partner-pipeline-automation` drill adapted for warm intros:

**Build these n8n workflows:**

**Workflow A — Weekly Intro Request Batch:**
- Trigger: Weekly cron (Monday 9am)
- Action 1: Query Attio for connectors with status "Active" and last request date >14 days ago
- Action 2: For each connector, find the best unmatched target (highest ICP score, not yet requested through any connector)
- Action 3: Generate a personalized intro request using the appropriate template (A/B/C) and the target's specific context from Attio
- Action 4: Queue the request for human review and send
- Action 5: Log `warm_intro_request_sent` in PostHog with all properties
- Action 6: Update Attio: connector last-request date, target request status

**Human action required:** Review and approve each queued intro request before sending. The agent drafts the personalized message; you review for tone, accuracy, and relationship context before it goes out. As you build confidence in the templates, you can batch-approve.

**Workflow B — Intro Response Handler:**
- Trigger: Attio webhook when a connector record's "Last Intro Date" field is updated (manually logged when intro is made)
- Action 1: Fire `warm_intro_received` in PostHog
- Action 2: Create a task in Attio: "Follow up on intro from {connector} to {target} — respond within 2 hours"
- Action 3: Generate a draft response to the target using the intro context
- Action 4: If no meeting is booked within 5 days, trigger the follow-up automation

**Workflow C — Meeting Outcome Tracker:**
- Trigger: Cal.com webhook for meetings with `utm_source=warm_intro`
- Action 1: After meeting date, create an Attio task: "Log warm intro meeting outcome — {target}"
- Action 2: When outcome is logged, fire `warm_intro_meeting_held` in PostHog
- Action 3: If outcome = "deal created," fire `warm_intro_deal_created` and notify the connector with a thank-you
- Action 4: Update connector record: total intros, total meetings, total deals

### 3. Automate follow-up sequences

Run the `follow-up-automation` drill for two follow-up paths:

**Path 1 — Connector follow-up:**
- If an intro request gets no response after 5 days: send one gentle nudge
- If the nudge gets no response after 7 days: mark connector as "Unresponsive for this request," do not ask again for 30 days
- If the connector declines: thank them, mark the request as declined, do not ask for the same target again

**Path 2 — Target follow-up after intro:**
- If the target does not respond within 3 days after intro: send a follow-up referencing the introduction and the connector
- If the target responds but does not book: send a Cal.com link with 2-3 proposed times
- If the target no-shows: send a reschedule request within 2 hours

Build both paths in n8n with appropriate guardrails: never follow up more than twice with a connector per request, never follow up more than twice with a target after intro.

### 4. Evaluate against threshold

After 2 months, measure:

- **Intro requests sent:** >= 60 (target volume)
- **Intros received:** >= 20 (pass threshold)
- **Meetings booked:** >= 16 (pass threshold)
- **Request-to-intro rate:** Compare to Baseline (should hold >35%)
- **Intro-to-meeting rate:** Compare to Baseline (should hold >55%)
- **Pipeline value:** Total deal value from warm intro meetings
- **Connector portfolio health:** What % of connectors produced at least 1 intro?

**PASS (>= 20 intros AND >= 16 meetings):** Document:
- Top 10 connectors by intro volume and conversion rate
- Best-performing ask templates with conversion data
- Average deal size from warm intro pipeline
- Automation reliability metrics
Proceed to Durable.

**FAIL:** Diagnose:
- If connector count is high but intro rate is low: Ask quality needs improvement, or you are over-asking connectors
- If intro count is high but meeting rate is low: Target qualification or follow-up needs work
- If pipeline is growing but slowly: Increase connector activation rate or request frequency

## Time Estimate

- 15 hours: Partner discovery, Crossbeam setup, connector list expansion (weeks 1-2)
- 10 hours: Build n8n automation workflows (weeks 1-2)
- 25 hours: Execute intro requests, handle intros, book meetings (weeks 1-8)
- 5 hours: Weekly reviews, follow-ups, connector relationship management
- 5 hours: Evaluate results, optimize templates and targeting

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector management, deal pipeline, task automation | Free for 3 users; $29/user/mo Plus ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking — full warm intro funnel with per-connector attribution | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Cal.com | Meeting booking with UTM-tagged links | Free for 1 user; $15/user/mo Teams ([cal.com/pricing](https://cal.com/pricing)) |
| n8n | Automation — request pipeline, response handling, follow-ups | Free self-hosted; Cloud from ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Crossbeam | Account mapping — find highest-overlap partners | Free tier (3 seats); Connector from $400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |
| Clay | Connector enrichment — tag contacts by industry, seniority, network | Launch plan $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |

**Estimated Scalable cost: $0-209/mo** (Crossbeam free tier, Clay only needed for initial enrichment batch, n8n self-hosted, free tiers for PostHog/Cal.com/Attio)

## Drills Referenced

- `partner-prospect-research` — systematic connector discovery across 4 channels with Crossbeam account mapping
- `partner-pipeline-automation` — n8n workflows for request batching, response handling, and meeting tracking
- `follow-up-automation` — automated follow-up sequences for both connectors and targets
