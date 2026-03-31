---
name: technical-requirements-discovery-scalable
description: >
  Technical Requirements Discovery — Scalable Automation. Automate tech stack research, transcript
  extraction, fit scoring, collateral matching, and deal routing via n8n workflows so technical
  discovery runs on every qualified deal without manual orchestration.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "Technical discovery automated on >=90% of qualified deals with <=48hr time-to-assessment and technical fit scores predicting outcomes within 15% accuracy"
kpis: ["Technical discovery completion rate", "Time-to-assessment (hours)", "Technical fit prediction accuracy", "Collateral follow-up speed", "Blocker resolution rate", "Technical win rate"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
drills:
  - tool-sync-workflow
  - technical-fit-scoring
  - technical-collateral-matching
  - dashboard-builder
  - threshold-engine
---

# Technical Requirements Discovery — Scalable Automation

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Remove human orchestration from technical discovery. When a deal enters "Qualified" in Attio, n8n automatically triggers tech stack research, generates a call prep brief, and queues a technical discovery call. After the call, transcript extraction, fit scoring, collateral matching, and routing all happen without manual intervention. The founder's only job is to conduct the call and review the agent's output. Scale to handling 20-50+ deals/month with consistent quality.

## Leading Indicators

- Tech stack research triggers automatically within 1 hour of deal entering "Qualified" (not waiting for someone to remember to run it)
- Post-call processing completes within 2 hours of the Fireflies transcript becoming available
- Collateral follow-up emails are generated and queued for review within 4 hours of each call
- The technical intelligence dashboard shows trends emerging across 30+ scored deals
- Solutions engineer calls are being auto-scheduled for "Needs SE Review" deals

## Instructions

### 1. Build the automated technical discovery pipeline in n8n

Run the `tool-sync-workflow` drill to create an n8n workflow that orchestrates the entire technical discovery process:

**Trigger:** Attio webhook fires when a deal's stage changes to "Qualified."

**Step 1 — Auto-research (runs immediately on trigger):**
- n8n receives the deal ID and company domain from the Attio webhook
- Calls the Clay API to create a Claygent enrichment row with tech stack, integration, security, and maturity prompts
- Waits for Clay enrichment to complete (poll every 60 seconds, timeout after 10 minutes)
- Sends enrichment results to Claude API to generate the technical intelligence profile and call prep brief
- Writes the profile and brief back to Attio as deal notes
- Sets `tech_stack_researched: true` and `tech_research_date` on the deal
- Fires PostHog event: `tech_stack_discovery_completed`

**Step 2 — Schedule call (triggered by research completion):**
- If the deal does not already have a technical discovery call scheduled (check Attio notes for tag `tech_discovery_scheduled`), send a notification to Slack/email: "Tech discovery ready for {Company} — call prep brief attached. Schedule a technical call with {contact name}."
- Include a Cal.com booking link pre-configured for "Technical Discovery" event type

**Step 3 — Post-call processing (triggered by Fireflies transcript webhook):**
- n8n receives the Fireflies transcript webhook when a new meeting is transcribed
- Match the meeting to an Attio deal by participant email or company name
- Call Claude API with the transcript and the `call-transcript-tech-requirements-extraction` prompt
- Parse the structured requirements JSON
- Write scores and requirements to the Attio deal record
- Apply routing logic: set `tech_routing_status` based on composite score and blockers
- Fire PostHog event: `tech_discovery_call_completed` and `tech_fit_score_applied`

**Step 4 — Collateral matching (triggered by score application):**
- Query the Technical Collateral Catalog from Attio
- Send requirements + catalog to Claude API for matching
- Generate the follow-up email draft
- Store matched collateral list and email draft as Attio notes
- Notify the founder: "Technical follow-up ready for {Company} — review and send."
- Fire PostHog event: `tech_collateral_matched`

**Step 5 — Routing actions (triggered by verdict):**
- If `tech_routing_status = "Needs SE Review"`: Create a task in Attio assigned to the SE team. Send Slack notification to #solutions-engineering.
- If `tech_routing_status = "Needs Product Review"`: Create a task in Attio assigned to the product team with a 1-week deadline. Send Slack notification to #product.
- If `tech_routing_status = "Technically Disqualified"`: Move deal to "Technically Disqualified" stage. Log the disqualification reason. Send notification to the founder.

### 2. Build the technical intelligence dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard called "Technical Requirements Intelligence" with panels:

- **Technical Fit Distribution:** Histogram of composite scores across all scored deals (last 90 days)
- **Category Weakness Map:** Average score per category (integration, security, infrastructure, performance, migration) — highlights your weakest area
- **Blocker Frequency:** Bar chart of most common blockers across deals
- **Time-to-Assessment:** Trend line showing hours from deal qualification to technical score applied
- **Technical Win/Loss Correlation:** Scatter plot of technical fit score vs. deal outcome for closed deals
- **Collateral Effectiveness:** Which documents are sent most often and whether deals that receive them progress faster

### 3. Implement technical routing intelligence

Using the `technical-fit-scoring` drill at scale, refine the scoring model:

- After 30+ scored deals with outcomes, analyze which scoring weights best predict wins. If security is more predictive than infrastructure for your market, adjust the weights.
- Build a "technical complexity tier" system: Simple (composite >80, 0 blockers), Standard (60-80, <=1 blocker), Complex (40-59 or 2+ blockers), Enterprise (<40 or critical blockers). Each tier gets a different SLA for response time.
- Auto-assign deals to technical resources: Simple deals need no SE involvement, Standard get async SE review, Complex get a live SE call, Enterprise get a solutions architect.

### 4. Scale to full pipeline coverage

Run the automated pipeline for 2 months across all qualified deals. Monitor:
- Completion rate: >=90% of qualified deals should get full technical discovery
- Time-to-assessment: <=48 hours from qualification to scored
- Prediction accuracy: technical fit scores should predict deal outcomes within 15%
- No human bottleneck: the founder should only be spending time on conducting calls and reviewing outputs, not on orchestration

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Set guardrails:
- Technical discovery completion rate must stay >=90%
- Time-to-assessment must stay <=48 hours
- If prediction accuracy falls below 15% for 2 consecutive weeks, recalibrate the scoring model
- If collateral gaps exceed 30% of requirements (too many unmatched requirements), pause and build missing collateral

If PASS after 2 months, proceed to Durable. If FAIL, identify the bottleneck: automation reliability (n8n errors), scoring accuracy (bad rubric), or throughput (too many calls for available resources).

## Time Estimate

- n8n workflow build and testing: 12-16 hours
- Dashboard setup: 2-3 hours
- Scoring model refinement: 3-4 hours
- Monitoring and iteration over 2 months: 2-3 hours/week
- Technical discovery calls (ongoing): 2-4 hours/week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with technical scoring, routing, and automation | Pro $59/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording with transcript webhook | Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Tech stack enrichment via Claygent and API | Launch $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking, dashboards, funnels | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation for the discovery pipeline | Pro EUR 60/mo (10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Transcript analysis, collateral matching, intelligence | Sonnet 4.6: $3/$15 per 1M tokens — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost:** $250-350/mo (Attio Pro $59, Fireflies $10, Clay $185, n8n ~$60, Anthropic API ~$20-40 for 20-50 transcripts/mo)

## Drills Referenced

- `tool-sync-workflow` — build n8n workflows connecting Attio, Fireflies, Clay, and PostHog into an automated pipeline
- `technical-fit-scoring` — apply and refine the 5-category scoring rubric at scale
- `technical-collateral-matching` — auto-match requirements to documentation and generate follow-ups
- `dashboard-builder` — create PostHog dashboard for technical intelligence visibility
- `threshold-engine` — evaluate metrics against pass thresholds and guardrails
