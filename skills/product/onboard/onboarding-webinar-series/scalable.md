---
name: onboarding-webinar-series-scalable
description: >
  Live Onboarding Webinars — Scalable Automation. Run 4+ webinars per month with
  fully automated series operations. Agent handles topic scheduling, persona-segmented
  promotion, cross-event analytics, and net-new prospect enrichment. Human delivers content.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email, Events"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "4+ webinars/mo, >=50% attendee activation, show rate >=35%, and >=8 meetings booked per month from webinar pipeline"
kpis: ["Webinars per month", "Registrations per webinar", "Show rate", "Attendee activation rate", "Meetings booked per webinar", "Repeat attendance rate", "Topic-to-pipeline correlation", "Promotion channel yield"]
slug: "onboarding-webinar-series"
install: "npx gtm-skills add product/onboard/onboarding-webinar-series"
drills:
  - webinar-series-automation
  - webinar-performance-monitor
---

# Live Onboarding Webinars — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Events

## Outcomes

Transform the validated webinar pipeline into a recurring, automated series running 4+ times per month. The agent automates the full series lifecycle: topic scheduling from a scored backlog, persona-segmented promotion, net-new prospect enrichment via Clay, automated registration ops, cross-event analytics, and speaker coordination. The human's only job is delivering the webinar content. Pass threshold: 4+ webinars/mo with >=50% attendee activation, show rate >=35%, and >=8 meetings booked per month from the webinar pipeline.

## Leading Indicators

- Content calendar populated with 12+ scored topics for the next quarter — confirms the series has enough fuel to sustain 4+/month cadence
- Automated promotion workflow fires on schedule for each event (Day -21, -14, -7, -1, 0, +1) without manual intervention — confirms the series automation is reliable
- Net-new prospect enrichment adds 100-300 topic-relevant contacts per webinar — confirms the audience is growing, not just recycling the same list
- Repeat attendance rate >=15% (users attending 2+ webinars in a quarter) — confirms the series is building ongoing engagement
- Cross-event dashboard shows improving metrics (registration, show rate, or activation) across 4+ consecutive webinars — confirms the iteration loop is working

## Instructions

### 1. Build the series content calendar and automation engine

Run the `webinar-series-automation` drill. This is the core of the Scalable level — it transforms one-off webinars into a machine.

**Topic backlog creation.** Build a scored backlog of 12+ webinar topics. For an onboarding webinar series, organize topics around the activation ladder:

| Week Pattern | Topic Type | Example |
|-------------|-----------|---------|
| Week 1 of month | Core activation workshop | "Build your first [core object] in 30 minutes" |
| Week 2 of month | Integration deep-dive | "Connect [top integration] and automate [workflow]" |
| Week 3 of month | Advanced use case | "How [customer persona] uses [product] for [outcome]" |
| Week 4 of month | Q&A / office hours | "Ask anything — live troubleshooting with the team" |

Score each topic using the drill's framework: ICP pain alignment (1-5), competitive differentiation (1-5), funnel position (1-3). Schedule the highest-scoring topics first.

Store the calendar in Attio as an "Event Calendar" list with fields: topic, date, speaker, target persona, promotion start date, status.

**Automated promotion engine.** The drill builds the full n8n workflow that fires at each milestone:
- Day -21: Generate registration page, draft LinkedIn posts, queue Loops invitations
- Day -14: First email wave to the most relevant Attio segment, Clay prospect enrichment for topic-relevant net-new contacts
- Day -7: Second email wave to non-openers, personal invites to high-value prospects
- Day -1: Final reminder to all registrants
- Day 0: 1-hour reminder with join link, Riverside recording setup
- Day +1: Trigger `webinar-attendee-nurture` drill (already automated from Baseline)

**Persona-segmented promotion.** Different webinar topics should be promoted to different user segments. Using PostHog cohorts, segment your user base by:
- Signup recency (last 7 days vs 8-21 days vs 22-60 days)
- Current milestone stage (signed up only, completed profile, partially activated)
- Product usage pattern (API-first users vs UI-first users vs integration-focused)

Match webinar topics to the persona most likely to benefit. Send targeted invitations only to the relevant segment — do not blast every webinar to your entire list.

### 2. Scale registration through prospect enrichment

For each upcoming webinar, use Clay to find net-new prospects:

Using `clay-people-search`, search for people whose job titles and companies match your ICP and who show interest in the webinar topic (recent LinkedIn posts about the problem your webinar solves, job changes into relevant roles, or company signals like funding rounds or hiring).

Using `clay-enrichment-waterfall`, enrich found contacts with verified email and company data. Target: 100-300 net-new, topic-relevant prospects per webinar.

Import enriched contacts into Attio tagged with "Webinar Prospect - [topic]" and add them to the targeted invite list in Loops.

This ensures the webinar audience grows with each event rather than shrinking as existing users activate.

### 3. Build cross-event analytics and monitoring

Run the `webinar-performance-monitor` drill to build always-on monitoring across the series:

**Per-event post-mortems.** The drill generates a structured post-mortem 14 days after each event, comparing every metric against targets and rolling averages. Store in Attio and post to Slack.

**Series-level dashboard.** Build a PostHog dashboard tracking:
- Registration trend across all events (bar chart)
- Show rate trend (line chart, 4-event moving average)
- Activation rate by webinar topic (grouped bar)
- Promotion channel effectiveness (email vs LinkedIn vs in-app vs personal invite)
- Meetings booked per event (bar chart with trend line)
- Repeat attendee count (growing counter)

**Anomaly alerting.** Configure alerts for:
- Show rate drops below 25% (vs target 35%) — immediate alert
- Registration declines for 3 consecutive events — topic fatigue alert
- Tier 1 reply rate drops below 15% — nurture quality alert

These monitoring signals feed into the `autonomous-optimization` drill at Durable level.

### 4. Automate speaker and guest coordination

For webinars with guest speakers (customer stories, integration partners):

Build an n8n workflow that handles:
- Speaker prep email 14 days before: event logistics, audience profile, talking points, Cal.com link for prep call
- Technical check 3 days before: Riverside test link, AV requirements, backup plan
- Thank-you email after: recording link, engagement stats, collaboration offer

This enables running expert panels and customer story webinars without additional coordination overhead.

### 5. Implement series-level optimizations

After every 4 events (monthly review), the agent should analyze:

- **Topic performance:** Which topics drove the most registrations? Highest activation? Most pipeline? Double down on high performers. Drop underperformers.
- **Timing optimization:** Which day of week and time slot produced the best show rate? Standardize on the winner.
- **Format comparison:** Workshop vs Q&A vs guest panel — which converts best?
- **Promotion channel analysis:** Which channel (email, LinkedIn, in-app, personal invite) has the highest registration-to-attendance conversion? Allocate more effort to the best channel.

Store findings in Attio. Adjust the upcoming month's calendar based on data.

### 6. Deliver webinars at cadence

**Human action required:** Deliver 4+ webinars per month. With the automated series engine handling everything else, the human's scope is:
- 30 minutes prep per webinar (review the topic brief the agent generates, update slides)
- 30-45 minutes delivery per webinar
- 15 minutes post-webinar debrief (note friction points the agent should analyze)

Total human time: ~4-5 hours per month for 4 webinars.

### 7. Evaluate against threshold

After 2 months of running the series at 4+/month cadence:

| Metric | Target |
|--------|--------|
| Webinars delivered per month | >=4 |
| Average registrations per webinar | >=30 |
| Show rate (series average) | >=35% |
| Attendee activation rate (series average) | >=50% |
| Meetings booked per month (from webinar pipeline) | >=8 |
| Repeat attendance rate | >=15% |
| Net-new prospects enriched per month | >=400 |

If PASS: The series is a reliable, scaled activation engine. Proceed to Durable to let the agent autonomously optimize every variable.

If FAIL on webinar volume: The automation is not reliable enough. Debug n8n workflows — check for failed triggers, API timeouts, or missing data. The agent should be able to run the series with zero manual intervention outside of content delivery.

If FAIL on activation rate at scale: The content quality may be degrading as you run more sessions. Check if the same host is doing all webinars (fatigue) or if topics are too broad (not targeted at the actual activation action). Review per-topic activation rates to find which topics work and which do not.

If FAIL on meetings booked: The nurture sequences may need refreshing. Check Tier 1 reply rates — if they dropped from Baseline levels, the follow-up personalization quality declined.

## Time Estimate

- 6 hours: Build the series content calendar, score and schedule 12+ topics
- 6 hours: Configure the full webinar-series-automation drill (n8n workflows, Clay enrichment, Loops sequences)
- 4 hours: Build the webinar-performance-monitor drill (PostHog dashboard, anomaly alerts, post-mortem automation)
- 2 hours: Set up speaker coordination automation
- 16 hours: Deliver 8+ webinars over 2 months (~2 hours each including prep)
- 4 hours: Monthly series reviews and calendar adjustments
- 2 hours: Final threshold evaluation and documentation

Total: ~40 hours spread over 2 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Promotional emails, reminders, tiered nurture at volume | $49/mo (5,000 contacts). [Pricing](https://loops.so/pricing) |
| PostHog | Full-funnel tracking, cross-event analytics, anomaly detection | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| Riverside | Weekly webinar recording and production | Standard: $19/mo or Pro: $29/mo for 4K. [Pricing](https://riverside.com/pricing) |
| Cal.com | Registration pages per event | Free for 1 user. Teams: $15/user/mo if multiple hosts. [Pricing](https://cal.com/pricing) |
| Intercom | In-app webinar promotion banners, persona-targeted | Essential: $29/seat/mo. [Pricing](https://www.intercom.com/pricing) |
| Clay | Net-new prospect enrichment per event | Launch: $185/mo for 2,500 data credits. [Pricing](https://clay.com/pricing) |
| Loom | Short clips for no-show follow-up | Free: 25 videos. Business: $12.50/user/mo. [Pricing](https://www.loom.com/pricing) |

**Estimated monthly cost: $280-350/mo** (Loops $49 + Riverside $19-29 + Clay $185 + Intercom $29. PostHog, Cal.com, and Loom free tiers likely sufficient at this scale.)

## Drills Referenced

- `webinar-series-automation` — automates the full recurring webinar lifecycle: topic scheduling, multi-wave promotion, registration ops, Clay prospect enrichment, speaker coordination, and cross-event analytics
- `webinar-performance-monitor` — builds always-on monitoring with per-event post-mortems, series health dashboards, and anomaly alerting that feeds data to Durable-level optimization
