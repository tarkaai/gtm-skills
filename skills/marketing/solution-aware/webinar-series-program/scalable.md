---
name: webinar-series-program-scalable
description: >
  Educational Webinar Series — Scalable Automation. Automate the bi-weekly webinar
  series into a self-running machine: topic scheduling, promotion engine, Clay-powered
  prospect discovery, and cross-event A/B testing to find the 10x format.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥200 registrations and ≥40 qualified leads per month from webinar series over 4 months"
kpis: ["Monthly registration volume", "Show rate", "Meetings booked per event", "Cost per qualified lead", "Automation ratio (automated vs manual hours per event)"]
slug: "webinar-series-program"
install: "npx gtm-skills add marketing/solution-aware/webinar-series-program"
drills:
  - webinar-series-automation
  - ab-test-orchestrator
---

# Educational Webinar Series — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Transform the proven bi-weekly webinar series into an automated machine that runs with minimal manual effort. The agent handles topic scheduling, multi-channel promotion, Clay-powered prospect discovery, and cross-event optimization. The human delivers the content. Pass threshold: ≥200 registrations AND ≥40 qualified leads per month, sustained for 4 consecutive months.

## Leading Indicators

- Promotion engine auto-executes ≥3 weeks before each event without manual intervention
- Clay prospecting adds ≥200 net-new ICP-matched contacts per event to the invite list
- Automation ratio drops below 3:1 (≤3 hours manual work per 1 hour of live event)
- A/B test win rate ≥40% (at least 2 out of 5 tests produce statistically significant improvement)
- Repeat attendee rate ≥15% by month 3 (community forming)

## Instructions

### 1. Deploy the webinar series automation engine

Run the `webinar-series-automation` drill. This builds the full automated lifecycle for a recurring webinar series:

**Content calendar**: Create an Attio "Event Calendar" list with 12 topics scored by ICP pain alignment, competitive differentiation, and funnel position. Schedule bi-weekly for the next 3 months.

**Automated promotion engine (n8n workflows)**:
- Day -21: Generate registration page, draft LinkedIn posts, queue email invitations in Loops
- Day -14: Send first email wave to most relevant Attio segment. Use Clay to find and enrich 200-500 net-new topic-relevant prospects.
- Day -7: Re-send to non-openers, post speaker spotlight on LinkedIn, send personal Attio invites to high-value pipeline prospects
- Day -1: Final reminder to all registrants
- Day 0: 1-hour reminder with join link, configure Riverside recording
- Day +1: Trigger the `webinar-attendee-nurture` drill (already configured at Baseline), export recording, update Attio

**Speaker coordination**: Automated prep email (14 days before), tech check reminder (3 days before), and thank-you (1 day after) for guest speakers.

**Cross-event analytics**: PostHog dashboard showing registrations by event (bar), show rate trend (line), meetings per event (bar), promotion channel breakdown (pie), and repeat attendee count.

### 2. Scale registration through Clay-powered prospecting

For each upcoming event, the `webinar-series-automation` drill uses Clay to discover net-new prospects:

1. Query `clay-people-search` for people matching the ICP who are active in the event's topic area (recent LinkedIn posts, job changes, conference talks)
2. Enrich contacts via `clay-enrichment-waterfall` (email, company data, tech stack)
3. Import into Attio tagged as "Webinar Prospect - [Event Slug]"
4. Add to the targeted invite segment in Loops

Target: 200-500 net-new, topic-relevant prospects per event. This supplements your existing subscriber list and prevents registration plateaus from list exhaustion.

### 3. Run systematic A/B tests on the event program

Run the `ab-test-orchestrator` drill to test one variable at a time across events. Test queue (run in order, one test per 2 events minimum):

**Test 1 — Event format**: Webinar (presentation + Q&A) vs Workshop (hands-on walkthrough). Measure: show rate, engagement rate, meetings booked.

**Test 2 — Promotion timing**: 3-week promotion window vs 2-week window. Measure: total registrations, registration velocity curve, cost per registrant.

**Test 3 — Day of week and time**: Tuesday 11am vs Thursday 2pm (or whatever your two strongest candidates are from Baseline data). Measure: show rate, engagement rate.

**Test 4 — Email subject line formula**: Pain-point lead ("Why your [X] is failing") vs outcome lead ("How to achieve [Y] in 30 days"). Measure: email open rate, registration conversion.

**Test 5 — Follow-up sequence length**: 3-email nurture (current) vs 5-email nurture with additional resource sharing. Measure: reply rate, meetings booked, unsubscribe rate.

For each test:
1. Form a hypothesis with predicted outcome and reasoning
2. Calculate minimum sample size (usually 2 events per variant for event-level tests)
3. Run the test using PostHog feature flags for audience splitting where possible, or sequential A/B (event N uses variant A, event N+1 uses variant B) for format tests
4. Evaluate using PostHog experiment analysis at 95% confidence
5. Implement winners permanently, document losers with reasoning

### 4. Build operational guardrails

Configure n8n alerts for:

- Registration velocity: If registrations are <50% of target at Day -7, fire alert. Action: send an additional promotion wave, activate paid LinkedIn promotion, or send personal outreach to high-value prospects.
- Show rate: If live attendance drops below 25% for 2 consecutive events, fire alert. Action: investigate reminder cadence, event timing, and topic relevance.
- Unsubscribe rate: If any promotion email triggers >1% unsubscribes, pause and review targeting/frequency.
- Nurture quality: If Tier 1 reply rate drops below 20%, fire alert. Action: review personalization quality and follow-up timing.
- Budget: If paid promotion spend exceeds $500/mo without proportional registration increase, pause paid and reallocate to organic channels.

### 5. Evaluate against threshold

After 4 months of bi-weekly events (8 events total), measure:

- Average monthly registrations (target: ≥200)
- Average monthly qualified leads (target: ≥40)
- Show rate trend (must be stable or improving)
- Cost per qualified lead (should be declining as automation matures)
- Automation ratio: hours of manual work per event (target: ≤3 hours, down from 6 at Baseline)

**PASS → Durable**: Consistently hitting ≥200 registrations and ≥40 leads per month for 4 months, with a proven automated promotion engine and data-backed format choices from A/B testing.
**MARGINAL → Optimize**: Hitting volume but not quality (or vice versa). Stay at Scalable. Focus A/B testing on the weakest metric.
**FAIL → Restructure**: Automation is running but results are declining. Diagnose: is the audience fatigued (declining registrations), is content quality dropping (declining show rate), or is conversion breaking (declining meetings)? Fix the root cause before proceeding.

## Time Estimate

- Series automation setup (one-time): 12 hours
- Clay prospecting pipeline setup: 4 hours
- A/B test design and setup (5 tests): 8 hours
- Per-event manual work (×16 events over 4 months): ~2.5 hours × 16 = 40 hours
- Cross-event analysis and optimization: 6 hours
- Guardrail configuration: 3 hours
- Threshold evaluation: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Webinar recording + production | ~$25/mo (Standard) — https://riverside.fm/pricing |
| Clay | Prospect discovery + enrichment | $149/mo (Explorer) for ~2,500 credits — https://clay.com/pricing |
| n8n | Automation orchestration (promotion, nurture, alerts) | $20/mo (cloud Starter) or free self-hosted — https://n8n.io/pricing |
| Loops | Email sequences + broadcasts | $49/mo (up to 5,000 contacts) — https://loops.so/pricing |
| Loom | Personalized video follow-ups | $15/mo (Business) — https://www.loom.com/pricing |
| PostHog | Funnel analytics + A/B experiments | Free up to 1M events — https://posthog.com/pricing |
| Attio | CRM for pipeline tracking | Free up to 3 seats — https://attio.com/pricing |
| Cal.com | Event scheduling | Free tier — https://cal.com/pricing |
| LinkedIn (organic) | Promotion posts | Free |

**Estimated play-specific cost: $260-360/mo** (Clay + Riverside + n8n + Loops + Loom)

## Drills Referenced

- `webinar-series-automation` — automates the full bi-weekly series lifecycle: topic calendar, multi-channel promotion engine, Clay prospect discovery, speaker coordination, and cross-event analytics
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on event format, timing, promotion, and nurture to find the highest-performing configuration
