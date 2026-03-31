---
name: best-practices-content-durable
description: >
  In-App Best Practices — Durable Intelligence. Autonomous optimization loop that detects
  engagement anomalies, generates hypotheses, runs experiments, and auto-implements winners
  to sustain and improve best-practices engagement and retention lift across all personas.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Content"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving engagement ≥30% and retention lift ≥5pp over 6 months via autonomous optimization"
kpis: ["Overall engagement rate", "Experiment velocity", "Optimization lift", "Content freshness index", "Distance from local maximum"]
slug: "best-practices-content"
install: "npx gtm-skills add product/retain/best-practices-content"
drills:
  - autonomous-optimization
  - nps-feedback-loop
---

# In-App Best Practices — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Content

## Outcomes

Best-practices engagement rate sustained at or above 30% and retention lift sustained at or above 5pp for 6 consecutive months. The autonomous optimization loop continuously detects engagement changes, diagnoses root causes, generates improvement hypotheses, runs A/B experiments, and auto-implements winners. Weekly health reports track content freshness, stalled users, and progress toward the local maximum. When successive experiments produce less than 2% improvement, the system has converged and shifts to maintenance mode.

## Leading Indicators

- Anomaly detection catching metric shifts within 24 hours (the monitoring loop is working)
- At least 2 experiments completed per month with documented outcomes
- Winning experiments producing measurable lift (>3% improvement in targeted metric)
- Content freshness index: fewer than 20% of active cards are older than 90 days without refresh
- Stalled-user count declining month over month (interventions are working)
- NPS feedback from best-practices users trending positive (the tips deliver real value)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor-diagnose-experiment-evaluate-implement cycle for the best-practices system:

**Monitor (daily via n8n cron):**
- Query PostHog for the system's primary KPIs: overall engagement rate, per-persona engagement rates, card completion rate, dismissal rate, retention lift, email fallback conversion rate
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics normal, log to Attio and take no action
- If any anomaly detected, proceed to diagnosis

**Diagnose (triggered by anomaly):**
- Pull the system's current configuration from Attio: active personas, card assignments, delivery schedule, copy variants, experiment history
- Pull 8-week metric history from PostHog broken down by persona, maturity tier, card, and surface
- Generate 3 ranked hypotheses using Claude. Examples of hypotheses the agent might generate:
  - "Engagement dropped 15% in the Builder persona because the top-performing card has been active for 12 weeks and 70% of eligible Builders have already seen it — test 2 new cards targeting recently shipped features"
  - "Dismissal rate spiked in the Casual persona because tips are being shown on login when the user has a specific task in mind — test delaying delivery until the user completes their first action"
  - "Email fallback conversion rate is plateauing because the same subject line formula is used for all cards — test persona-specific subject lines that reference the user's most-used feature"
  - "Completion rate dropped for configuration tips because a recent product update changed the settings UI — refresh affected cards with updated screenshots and step instructions"
- Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of traffic or requires removing a card that >100 users have engaged with), send Slack alert for human review and stop.

**Experiment (triggered by hypothesis acceptance):**
- Create a PostHog feature flag splitting the affected segment between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis targets copy, update the Intercom message or Loops email via API; if the hypothesis targets timing, adjust the n8n trigger; if the hypothesis targets a new card, create and deploy it to the variant group
- Run for minimum 7 days or until 100+ samples per variant, whichever is longer
- Log experiment start in Attio: hypothesis, affected persona, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog experiments API
- Decision tree:
  - **Adopt:** Variant outperforms control with >95% confidence and >3% improvement. Update the live configuration. Log the change.
  - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this result. Return to diagnosis.
  - **Revert:** Variant underperforms control. Disable the variant, restore control. Log the failure. Wait 7 days before testing the same variable.
  - **Extend:** Insufficient sample size. Continue for another period.

**Guardrails:**
- Maximum 1 active experiment per persona at a time
- If overall engagement rate drops >30% during any experiment, auto-revert immediately
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review
- Never experiment on metrics without PostHog tracking — if a new card lacks event instrumentation, fix tracking first

### 2. Generate weekly health reports

Run the the best practices health report workflow (see instructions below) drill to produce a structured weekly brief every Monday:

The report covers:
- **Card performance table:** Per-card delivery rate, CTR, completion rate, dismissal rate, and trend vs. 4-week average. Sorted by retention lift contribution.
- **Persona performance table:** Per-persona engagement rate, completion rate, and retention lift with trend arrows
- **Stalled user analysis:**
  - Tip-resistant users (shown 3+ tips, dismissed all) — count and recommended intervention
  - Viewed-not-acted users (clicked 2+ tips, completed none) — count and recommended intervention
  - Exhausted users (seen all cards for their persona/tier) — count and content gap identified
- **Content freshness flags:** Cards with decaying engagement, cards nearing population exhaustion, cards older than 90 days without refresh
- **Experiment outcomes:** What was tested, what happened, what was decided, net impact
- **AI-generated recommendation:** One specific experiment to run next week with hypothesis and expected impact
- **Distance from local maximum:** Current engagement rate vs. estimated ceiling based on diminishing experiment returns

The report is posted to Slack and stored in Attio. "ACT"-severity signals (stalled-user count exceeding 20% of active users, content freshness below 80%, persona engagement below 20%) automatically feed into the optimization loop as the next hypothesis to test.

### 3. Close the feedback loop with engaged users

Run the `nps-feedback-loop` drill targeted specifically at best-practices engagers:

- Survey users who completed 3+ tips in the last 60 days: "How useful are the product tips you receive?" (1-10 scale) + "What tip or workflow improvement would be most valuable to you?" (open text)
- Route responses:
  - **Promoters (9-10):** Their open-text responses become input for new card creation. Ask if they have their own tips to contribute (user-generated best practices).
  - **Passives (7-8):** Analyze what they request — gaps in the current card library. Feed into the content pipeline as new card candidates.
  - **Detractors (0-6):** Personal outreach. If engaged users find the tips unhelpful, the content quality needs improvement. Identify which specific cards they disliked and why.
- Track NPS by persona: if one persona's tip-engagers score consistently lower, the persona-specific copy variants may need reworking or the card-persona mapping may be wrong.
- Feed all open-text responses into Claude to identify thematic clusters. The top-requested themes become the next batch of cards to produce.

### 4. Detect convergence and shift to maintenance

The optimization loop runs indefinitely until it detects convergence: 3 consecutive experiments producing less than 2% improvement. At convergence:

1. The best-practices system has found its local maximum for the current product, user base, and content library
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment velocity to 1 per month (maintenance testing for product changes and user base evolution)
4. Generate a convergence report: "Best-practices system optimized. Current engagement rate: [X]%. Retention lift: [Y]pp. Content library: [Z] active cards. Further gains require: new product features creating new best practices, significant user base changes, or product UX improvements that make existing practices unnecessary."
5. Shift agent resources to other plays that have not yet converged

### 5. Continuous evaluation

This level runs continuously. Monthly check-in metrics:
- Is overall engagement rate holding at or above 30%?
- Is retention lift holding at or above 5pp?
- Is the optimization loop producing at least one experiment per month?
- Are weekly health reports being generated and reviewed?
- Is content freshness above 80% (fewer than 20% of cards stale)?

If any metric degrades for 2 consecutive months despite optimization, escalate to human review. The system may have hit external limits (major product redesign, user base composition shift, competitive landscape change) that require strategic intervention, not tactical optimization.

## Time Estimate

- 20 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiment infrastructure, Claude integration for hypothesis generation)
- 10 hours: Weekly health report automation setup (PostHog queries, Claude report generation, Slack distribution)
- 10 hours: NPS feedback loop configuration for best-practices engagers
- 110 hours: Ongoing optimization cycles, experiment management, content refresh, and reporting over 6 months (~4.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, funnels, dashboards, cohorts | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app message variants for experiments, NPS surveys, Help Center | ~$150-500/mo at scale — https://www.intercom.com/pricing |
| Loops | Email sequence variants for experiments, digest emails | Starter $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, report generation, webhook orchestration | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, report summarization, card content | ~$20-50/mo based on usage — https://www.anthropic.com/pricing |
| Attio | Campaign records, experiment audit trail, NPS data | From $0/mo (free tier) — https://attio.com/pricing |

**Play-specific cost:** ~$250-600/mo (Intercom at scale + Anthropic API usage + PostHog Growth tier)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that finds the local maximum for best-practices engagement and retention
- the best practices health report workflow (see instructions below) — weekly structured report with card performance, stalled user analysis, content freshness, and experiment outcomes
- `nps-feedback-loop` — collect and act on feedback from best-practices engagers to validate the system delivers real value and identify content gaps
