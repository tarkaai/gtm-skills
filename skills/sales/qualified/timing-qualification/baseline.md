---
name: timing-qualification-baseline
description: >
  Timing Qualification Process — Baseline Run. First always-on timing qualification system.
  Expand to 50-100 opportunities over 2 weeks with automated timeline tracking, trigger-specific
  engagement cadences, and timeline validation across multiple stakeholders. Prove that urgency
  categorization holds over time and predicts deal velocity.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: ">=80% of opportunities timeline-qualified over 2 weeks with forecast accuracy within 30 days of predicted close date"
kpis: ["Timeline qualification rate", "Timeline accuracy (predicted vs actual close)", "Deal velocity by timeline category", "Slippage rate"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
drills:
  - timing-discovery-call
  - posthog-gtm-events
  - follow-up-automation
  - timing-qualification-reporting
---

# Timing Qualification Process — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

Scale timing qualification from a one-time smoke test to an always-on process. Every opportunity that enters the pipeline gets timeline-qualified within 48 hours. The system should show that Immediate deals close 2-3x faster than Medium-term deals, validating that the categorization has predictive value. Forecast accuracy should be within 30 days of predicted close date for >=60% of deals that close during the evaluation period.

## Leading Indicators

- Qualification rate exceeds 80% (fewer than 20% of deals sit unscored for more than 48 hours)
- Timeline categories correlate with deal velocity: Immediate deals move to proposal faster than Long-term
- Slippage events are being detected and logged (the system is tracking when timelines shift)
- Timeline-specific cadences are running: Immediate deals get daily touches, Long-term get monthly nurture
- At least 1 deal that was categorized as Immediate has closed, providing the first forecast accuracy data point

## Instructions

### 1. Expand timing qualification to all new opportunities

Continue using the `timing-discovery-call` drill from Smoke, but now apply it to every new opportunity:

1. Every discovery call gets timing questions woven in — not as a separate "timing call" but as a standard part of the qualification flow
2. After each call, the agent auto-extracts timing signals and scores the deal
3. Any deal that enters the pipeline without a discovery call (inbound, referral, etc.) gets flagged for a timing-focused follow-up within 48 hours

Set up an n8n workflow that checks daily: "Are there deals older than 48 hours without a `timeline_category`?" If yes, Slack-alert the founder.

### 2. Configure tracking for all timing events

Run the `posthog-gtm-events` drill to set up event tracking:

- `timeline_category_assigned` — fires when a deal gets its first timeline score
- `timeline_validated` — fires when timeline is confirmed by a second stakeholder or re-confirmed in a follow-up
- `timeline_shift_detected` — fires when a deal's timeline category changes (e.g., Near-term slides to Medium-term)
- `timeline_slippage` — fires when target close date is pushed back
- `forecast_accuracy_logged` — fires when a deal closes and actual vs predicted dates are compared

Connect PostHog to Attio via n8n webhook so CRM deal stage changes fire the right events.

### 3. Build timeline-specific follow-up cadences

Run the `follow-up-automation` drill to create cadences based on timeline category:

- **Immediate (0-30 days):** Daily email or call touchpoint. Urgency-reinforcing content: "Your {deadline} is in {X} days — here's how we can help you hit it." Auto-schedule next meeting within 48 hours of previous.
- **Near-term (1-3 months):** 2-3 touches per week. Mix of email and LinkedIn. Content focused on evaluation process: case studies, ROI calculators, technical docs.
- **Medium-term (3-6 months):** Weekly touchpoint. Educational content, industry insights. Monthly check-in call to see if timeline has accelerated.
- **Long-term (6+ months):** Biweekly nurture email. Quarterly re-qualification call. Add to newsletter/content drip.

Use Instantly for email sequences and Attio automations for CRM-triggered actions.

### 4. Implement timeline validation

For Immediate and Near-term deals, validate the timeline with additional stakeholders:

1. After the initial discovery call, identify at least one other stakeholder (champion, economic buyer, technical evaluator)
2. In follow-up conversations, confirm the timeline: "Your colleague mentioned you need this by Q3. Is that the same timeline you're working toward?"
3. If timelines conflict between stakeholders, flag the deal as `slippage_risk = High` and note the discrepancy

Fire `timeline_validated` events in PostHog when validation occurs.

### 5. Build initial reporting

Run the `timing-qualification-reporting` drill to create:

- PostHog dashboard: timeline distribution, qualification rate trend, slippage events
- Weekly Slack report: deals qualified this week, category breakdown, slippage alerts
- Attio pipeline views: "Urgent Pipeline" (Immediate), "At Risk" (High slippage), "Needs Timeline" (unqualified)

### 6. Analyze timing patterns

After 2 weeks, examine:

- **Which timing questions worked best?** Compare effective question data from `timing-discovery-call` across all calls. Identify the top 3 questions that consistently produce timeline clarity.
- **Which urgency drivers are most common?** If "budget expiration" appears 5x more than any other driver, build your outreach messaging around it.
- **Which ICP segments have the most urgency?** If funded startups are 80% Immediate/Near-term but enterprise is 80% Long-term, adjust your prospecting to weight funded startups more heavily.
- **Are timelines accurate?** For any deals that have closed, compare predicted vs actual close date.

### 7. Evaluate against threshold

Measure against: >=80% of opportunities timeline-qualified over 2 weeks with forecast accuracy within 30 days for closed deals.

If PASS, proceed to Scalable. If FAIL, diagnose:
- Low qualification rate: founder is not asking timing questions consistently — create a checklist
- Poor forecast accuracy: timeline confidence scores are not calibrated — tighten criteria
- No Immediate deals: ICP is not targeting active buyers — adjust targeting

## Time Estimate

- Tracking and automation setup: 3 hours
- Follow-up cadence configuration: 2 hours
- Discovery calls (expanded volume): 6 hours over 2 weeks
- Reporting and analysis: 2 hours
- Pattern analysis and iteration: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with timeline pipeline | Free or Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call transcription | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Instantly | Timeline-specific email sequences | Growth $30/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation: cadences, alerts, syncing | Starter $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Event tracking and dashboards | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Transcript timing extraction | ~$5-15/mo at baseline volume — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** ~$50-100/mo (Fireflies $18 + Instantly $30 + n8n $24 + Anthropic ~$5-15)

## Drills Referenced

- `timing-discovery-call` — structured discovery call with timing extraction on every new opportunity
- `posthog-gtm-events` — set up event tracking for all timing qualification events
- `follow-up-automation` — n8n workflows for timeline-specific engagement cadences
- `timing-qualification-reporting` — dashboards, weekly reports, and anomaly alerts
