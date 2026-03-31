---
name: success-criteria-definition-baseline
description: >
  Success Criteria Definition — Baseline Run. First always-on automation for success criteria
  definition. When deals enter Connected stage with a recorded discovery call, AI extraction
  auto-generates draft criteria, workshop calls are auto-scheduled, and mutual success plans
  are generated and tracked. Event tracking measures the criteria-to-close-rate correlation.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=80% of Connected deals have defined criteria over 2 weeks, with >=70% achieving mutual stakeholder agreement on the success plan"
kpis: ["Success criteria definition rate", "Mutual agreement rate", "Average criteria count per deal", "Average achievability score", "Close rate correlation (criteria vs no-criteria)"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
drills:
  - success-criteria-workshop
  - posthog-gtm-events
  - threshold-engine
---

# Success Criteria Definition — Baseline Run

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

First always-on automation. When a deal enters Connected stage and has a discovery call recorded, the system auto-generates draft success criteria, schedules the workshop, and produces the mutual success plan. The agent manages the pipeline — the founder conducts the workshop calls and reviews plans before sending.

**Pass threshold:** >=80% of Connected deals have defined criteria over 2 weeks, with >=70% achieving mutual stakeholder agreement on the success plan.

## Leading Indicators

- Auto-extraction triggers within 24 hours of a discovery call being recorded
- Draft criteria are generated for >=90% of deals with transcripts
- Workshop scheduling emails achieve >=50% booking rate within 48 hours
- Prospects modify/add criteria during workshops (indicates engagement, not passive acceptance)
- At least 30% of mutual success plans are referenced in subsequent deal communications

## Instructions

### 1. Configure Event Tracking

Run the `posthog-gtm-events` drill to set up the success criteria event taxonomy:

| Event | Trigger |
|-------|---------|
| `criteria_extraction_started` | AI extraction triggered for a deal |
| `criteria_extraction_completed` | Draft criteria generated and stored |
| `criteria_workshop_scheduled` | Workshop booking link sent to prospect |
| `criteria_workshop_completed` | Workshop call recorded in Fireflies |
| `success_criteria_defined` | Final criteria stored in Attio |
| `mutual_success_plan_created` | Mutual plan document generated |
| `mutual_success_plan_agreed` | Prospect confirms agreement to the plan |
| `success_criteria_achieved` | Post-sale: criterion met |
| `success_criteria_missed` | Post-sale: criterion not met |

Connect PostHog events to Attio via n8n webhook so deal records update automatically when events fire.

### 2. Set Up CRM Automation

Create Attio custom attributes on the Deals object (if not already created from Smoke):
- `success_criteria_status`: select — none, draft, defined, agreed, tracking, achieved, missed
- `success_criteria_count`: number
- `avg_achievability_score`: number
- `mutual_plan_date`: date
- `next_review_date`: date
- `criteria_categories`: multi-select — efficiency, revenue, cost_savings, quality, time_to_value, adoption

Create an Attio automation: when deal stage changes to "Connected" AND the deal has a Fireflies transcript linked, fire a webhook to n8n.

### 3. Build the Auto-Extraction Workflow

Create an n8n workflow triggered by the Attio webhook:

1. Receive webhook → retrieve deal ID
2. Pull deal context from Attio: company, industry, headcount, champion, deal value
3. Retrieve the most recent Fireflies transcript for this deal
4. Run `success-criteria-extraction` with the transcript and deal context
5. Store the draft criteria in Attio as a note tagged `success-criteria-draft`
6. Update `success_criteria_status` to "draft"
7. Fire PostHog event `criteria_extraction_completed`
8. Generate a Cal.com booking link for the workshop
9. Queue a workshop scheduling email to the champion (use Attio email or Loops transactional)

**Human action required:** Review the auto-generated draft criteria before the workshop call. The agent flags any criteria with achievability < 50 for the founder to assess. The founder may add context the AI missed.

### 4. Run Workshops at Scale

The auto-scheduling creates a steady stream of 30-minute workshop calls. The founder conducts these — the system handles everything else.

For each workshop:
- Agent prepares a briefing 1 hour before the call: draft criteria, achievability assessment, talking points
- **Human action required:** Founder conducts the 30-minute call
- Agent processes the workshop transcript within 2 hours: refined extraction, mutual plan generation, Attio updates, PostHog events

Target: 3-5 workshops per week across all Connected deals.

### 5. Monitor and Iterate for 2 Weeks

Daily check (agent-automated):
- How many deals entered Connected without triggering extraction? (gap = missing transcripts or webhook failure)
- Workshop booking rate: are prospects scheduling? If <50%, test different scheduling messages
- Post-workshop: are mutual plans being generated? Check for extraction failures

Weekly review (founder reviews agent report):
- Definition rate: what % of Connected deals now have criteria? (target >=80%)
- Agreement rate: what % of defined criteria have mutual agreement? (target >=70%)
- Quality check: sample 3 mutual success plans — are the criteria specific and measurable, or vague?

Adjust mid-flight:
- If booking rate <40%: test a different workshop framing (e.g., "alignment call" vs "success planning session")
- If extraction quality is low: review transcripts — are discovery calls substantive enough to extract from?
- If agreement rate is low: the workshop conversation format may need adjustment — criteria may be too aggressive

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill after 2 weeks:
- Definition rate: % of Connected deals with defined criteria (target >=80%)
- Agreement rate: % of deals with mutual stakeholder agreement (target >=70%)
- Early close rate signal: do deals with criteria show different progression than those without?

If PASS: proceed to Scalable to add AI recommendations and A/B testing.
If FAIL: diagnose bottleneck — is it scheduling (prospects won't book), extraction (AI quality), or agreement (criteria don't resonate)?

## Time Estimate

- 3 hours: Event tracking setup and CRM attribute configuration (one-time)
- 3 hours: n8n workflow build for auto-extraction and scheduling (one-time)
- 8 hours: Workshop calls (~30 min each, ~16 calls over 2 weeks, founder time)
- 2 hours: Daily monitoring and mid-flight adjustments (10 min/day x 14 days)
- 2 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, automations, success criteria attributes | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Transcription — discovery and workshop calls | $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — event tracking, funnel analysis | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling — auto-generated workshop booking links | Free or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| n8n | Automation — extraction trigger, scheduling workflow | Self-hosted free or $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — criteria extraction from transcripts | ~$3/1M input tokens — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$50-100/mo. Primary incremental costs: Fireflies Pro ($18/mo), n8n Starter ($24/mo), Anthropic API (~$5-10/mo at this volume).

## Drills Referenced

- `success-criteria-workshop` — end-to-end workflow for auto-extracting, scheduling, conducting, and documenting success criteria conversations
- `posthog-gtm-events` — configure the success criteria event taxonomy in PostHog
- `threshold-engine` — evaluate results against pass/fail threshold
