---
name: nps-program-baseline
description: >
  NPS Feedback System — Baseline Run. Deploy always-on NPS surveys triggered at lifecycle
  milestones with automated response routing that closes the loop with promoters,
  passives, and detractors within defined SLAs.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: "≥35% response rate over 200+ surveys sent AND detractor follow-up completed within 48 hours for ≥80% of detractors"
kpis: ["NPS response rate", "NPS score", "Detractor close-the-loop rate", "Promoter referral ask rate", "Median follow-up latency"]
slug: "nps-program"
install: "npx gtm-skills add product/referrals/nps-program"
drills:
  - nps-feedback-loop
  - posthog-gtm-events
  - nps-response-routing
---

# NPS Feedback System — Baseline Run

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

An always-on NPS survey system that automatically triggers at lifecycle milestones, routes every response to the correct follow-up action within SLA, and produces a rolling NPS score tracked weekly. The system handles 200+ surveys per month without manual intervention beyond detractor outreach.

## Leading Indicators

- Survey trigger automation fires correctly at each milestone (verified in n8n execution logs)
- Response routing delivers follow-up within 1 hour for promoters and passives (automated)
- Detractor alerts reach account owners within 15 minutes of submission
- NPS score stabilizes within a 10-point range after 100+ responses (signal, not noise)
- At least 1 promoter submits a review or referral from the automated ask

## Instructions

### 1. Set up NPS event tracking

Run the `posthog-gtm-events` drill to configure the NPS event taxonomy in PostHog:

- `nps_survey_triggered` — survey is queued for a user (properties: trigger_reason, channel, user_id)
- `nps_survey_sent` — survey is displayed in-app or email delivered (properties: channel, user_id)
- `nps_survey_submitted` — user submits a response (properties: score, segment, has_open_text, channel)
- `nps_response_routed` — follow-up action dispatched (properties: segment, action_type, latency_seconds)
- `nps_loop_closed` — follow-up completed (properties: segment, outcome, days_to_close)

Build a PostHog funnel: triggered > sent > submitted > routed > closed. This is the core measurement for the NPS program.

### 2. Deploy lifecycle-triggered surveys

Run the `nps-feedback-loop` drill steps 1-2 to deploy always-on surveys at these milestones:

| Trigger | Timing | Channel | Rationale |
|---------|--------|---------|-----------|
| Activation milestone | 45 days post-signup, if activated | In-app (Intercom) | First meaningful opinion point |
| Quarterly check-in | Every 90 days for users active in last 14 days | Email (Loops) | Ongoing sentiment tracking |
| Post-major-workflow | After completing a complex workflow for the first time | In-app (Intercom) | Capture peak experience moments |

Guardrails:
- Never survey a user more than once per 90 days
- Never survey during the first 14 days after signup
- Never survey within 7 days of an open support ticket
- Cap daily survey volume at 5% of active users

Using n8n, build a scheduling workflow that checks these rules before sending each survey.

### 3. Configure automated response routing

Run the `nps-response-routing` drill to build the full routing automation:

- **Promoter routing (9-10):** Automated thank-you email via Loops within 1 hour. Include a one-click review link (G2 or Capterra) and a referral link. Add to "Promoter Candidates" list in Attio. If user is a power user (top 20% usage), flag for advocacy pipeline.
- **Passive routing (7-8):** Automated email via Loops within 1 hour. Share a relevant resource based on their open-text feedback. Include a feedback call booking link via Cal.com. Log in Attio with the feedback theme.
- **Detractor routing (0-6):** Immediate Slack/email alert to the account owner with full context: score, open-text, usage data, MRR, open tickets. Create an Attio task with 48-hour SLA. If score ≤ 3 or MRR ≥ $500, escalate to urgent (24-hour SLA).

### 4. Build the NPS tracking dashboard

Using PostHog, create a dashboard with:

- **Rolling NPS score** (trailing 30 days) as the headline metric
- **Response rate** by channel (in-app vs email)
- **Segment distribution** (promoter/passive/detractor %) trended weekly
- **Close-the-loop rate** for detractors (% followed up within 48 hours)
- **Top detractor themes** (updated weekly from open-text analysis)
- **Promoter actions** (reviews submitted, referrals made)

### 5. Establish the feedback-to-product pipeline

Run `nps-feedback-loop` drill step 5 to aggregate open-text responses:

- Use Claude (via n8n AI node) to categorize each open-text response into themes: missing feature, usability issue, performance, pricing, support quality, integration request, other
- Aggregate themes weekly. Store in Attio as a note on the NPS program record.
- When a theme appears in 5+ detractor responses in a 30-day window, create a product feedback ticket in Attio tagged "NPS Signal" with the theme, count, representative quotes, and affected accounts.

### 6. Evaluate against threshold

After 4 weeks of always-on operation, measure:

- Response rate: total responses / total surveys sent. Pass: ≥35%.
- Volume: total surveys sent. Pass: ≥200.
- Detractor close rate: detractors with completed follow-up within 48 hours / total detractors. Pass: ≥80%.
- NPS score: record the 30-day rolling score. No specific threshold — establishing the baseline.

If PASS: document the baseline NPS score, response rates by channel, top themes, and close-the-loop performance. Proceed to Scalable.
If FAIL on response rate: analyze by channel. If in-app is low, test survey placement (modal vs slide-in). If email is low, test subject lines.
If FAIL on close rate: the routing or alerting is broken. Check n8n execution logs and Attio task creation.

## Time Estimate

- Event taxonomy and tracking setup: 4 hours
- Survey trigger automation: 6 hours
- Response routing automation: 6 hours
- Dashboard and theme analysis: 3 hours
- Monitoring and evaluation: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app NPS survey delivery | Proactive Support Plus: $99/mo (500 messages included). [Pricing](https://www.intercom.com/pricing) |
| PostHog | Event tracking, funnels, dashboards, cohorts | Surveys: 1,500 free/mo, then $0.10/response. Analytics: 1M events free. [Pricing](https://posthog.com/pricing) |
| Loops | Email survey delivery, automated follow-ups | From $49/mo. Transactional email free on paid plans. [Pricing](https://loops.so/pricing) |
| Attio | Response storage, task management, feedback pipeline | Free for 3 users. Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |
| n8n | Workflow automation for triggers and routing | Cloud: from $24/mo (2,500 executions). Self-hosted: free. [Pricing](https://n8n.io/pricing) |

**Estimated play-specific cost at this level:** ~$50-150/mo depending on survey volume and existing stack coverage. PostHog surveys stay free under 1,500 responses/mo. Intercom surveys use existing Proactive Support Plus allocation.

## Drills Referenced

- `nps-feedback-loop` — survey design, deployment at lifecycle milestones, segment analysis, and follow-up actions
- `posthog-gtm-events` — NPS event taxonomy setup for tracking the full survey lifecycle
- `nps-response-routing` — automated enrichment, classification, and routing of every NPS response to segment-specific actions
