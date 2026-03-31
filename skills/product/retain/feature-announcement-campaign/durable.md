---
name: feature-announcement-campaign-durable
description: >
  New Feature Announcements — Durable Intelligence. Always-on AI agent monitors
  announcement effectiveness, detects adoption anomalies, generates optimization
  hypotheses, runs experiments, and auto-implements winners. Weekly optimization
  briefs track convergence toward local maximum.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "20 hours setup + ongoing autonomous operation over 6 months"
outcome: "Feature trial rate sustained ≥35% and adoption decay ratio sustained ≥0.35 for 6 months with <5 hours/month human oversight"
kpis: ["Feature trial rate (6-month trend)", "Adoption decay ratio (6-month trend)", "Experiment velocity", "Autonomous improvement rate", "Human intervention frequency"]
slug: "feature-announcement-campaign"
install: "npx gtm-skills add product/retain/feature-announcement-campaign"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# New Feature Announcements — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The announcement system runs autonomously. An AI agent monitors all announcement metrics, detects when performance degrades, generates hypotheses about what to change, runs A/B experiments, and auto-implements winners. Feature trial rate and adoption decay ratio sustain at or above Scalable thresholds for 6 continuous months with less than 5 hours per month of human oversight. The system converges when successive experiments produce <2% improvement.

## Leading Indicators

- Anomaly detection firing within 24 hours of metric shifts
- Hypotheses generated and experiments launched within 48 hours of anomaly detection
- Weekly optimization briefs delivered on schedule
- Experiment win rate ≥30% (agents are generating useful hypotheses)
- Convergence signal: 3 consecutive experiments with <2% lift indicates local maximum reached

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill targeting the feature announcement campaign. Configure the optimization loop for these specific metrics:

**Primary KPIs to monitor:**
- Feature trial rate (target: ≥35%)
- Adoption decay ratio (target: ≥0.35)
- 7-day feature retention rate

**Variables the agent can experiment on (low/medium risk):**
- Announcement copy (headline, body, CTA text)
- In-app message format (banner vs. tooltip vs. modal)
- Email send timing (day of week, time of day)
- Segment targeting thresholds (which users see which tier of announcement)
- Follow-up nudge timing (days after initial announcement)
- Re-engagement message copy for stalled users

**Variables requiring human approval (high risk):**
- Changing which features get Tier 1 vs. Tier 2 classification
- Altering announcement frequency limits (fatigue thresholds)
- Adding or removing announcement channels
- Modifying the target segment definition

The agent runs the daily monitoring phase via n8n cron. When an anomaly is detected (trial rate drops >20% or decay ratio drops below 0.3), the agent diagnoses the cause, generates 3 ranked hypotheses, and launches an experiment on the top low/medium-risk hypothesis. Experiments run for minimum 7 days or 200+ users per variant.

### 2. Deploy the announcement health monitor

Run the `autonomous-optimization` drill to build the play-specific monitoring layer:

- Per-feature adoption funnels with channel breakdowns
- Adoption decay tracking for every announced feature
- Weekly health classification: Healthy, Fading, or Failed for each feature
- Automated re-engagement for Fading features (Intercom nudge + Loops follow-up)
- Announcement fatigue detection (dismiss rate across users)

This drill produces the data the autonomous optimization loop consumes. The health monitor detects the patterns; the optimization loop decides what to change about them.

### 3. Build the executive dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard for the feature announcement campaign:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Trial rate trend (6-month) | Line chart | Are announcements driving consistent adoption? |
| Decay ratio trend (6-month) | Line chart | Is post-announcement retention improving? |
| Active experiments | Table | What is the agent currently testing and status |
| Experiment history | Timeline | All experiments with outcomes (adopted/reverted/extended) |
| Channel effectiveness trend | Stacked area | How in-app vs. email contribution changes over time |
| Segment response heatmap | Heatmap | Which segments respond best to announcements this month |
| Convergence tracker | Gauge | How close to local maximum (based on recent experiment lift) |

Set threshold alerts:
- Trial rate below 30% for 7+ consecutive days
- Decay ratio below 0.25 for any feature launched in the last 30 days
- No experiment running for 14+ days (agent may be stuck)
- 4 consecutive experiments with <2% lift (convergence — reduce to weekly monitoring)

### 4. Establish the weekly optimization brief

The `autonomous-optimization` drill generates a weekly brief. For this play, ensure the brief includes:

```
## Feature Announcement Optimization — Week of {date}

### Key Metrics
- Feature trial rate: {X}% (target: ≥35%, trend: {up/down/flat})
- Adoption decay ratio: {X} (target: ≥0.35, trend: {up/down/flat})
- Announcements this week: {N} features, {N} users reached

### Experiment Activity
- Active experiment: {description, variant, days running, preliminary results}
- Last completed: {description, outcome, lift}
- Cumulative experiments: {N} total, {N} adopted, {N} reverted

### Feature Health
- Healthy: {N} features
- Fading: {N} features (interventions triggered for: {list})
- Failed: {N} features (flagged for product review: {list})

### Distance from Local Maximum
- Recent experiment lift: {X}% avg over last 3 experiments
- Convergence status: {Converging / Still optimizing / Diverging (investigate)}

### Human Actions Needed
- {List any high-risk hypotheses awaiting approval, or "None"}
```

### 5. Monitor for convergence and adapt

When the system detects convergence (3 consecutive experiments with <2% improvement):

1. Reduce monitoring from daily to weekly
2. Reduce experiment cadence from continuous to monthly check-ins
3. Generate a convergence report: "Feature announcement campaign has reached local maximum. Current performance: {metrics}. Further gains require strategic changes: new channels (push notifications, in-product changelog), new content formats (video, interactive), or product changes (better in-feature onboarding)."
4. Shift agent resources to other plays that have more optimization headroom

If metrics subsequently degrade (new user cohorts respond differently, product changes affect adoption patterns), the system detects the anomaly and re-enters active optimization automatically.

**Human action required:** Review the convergence report. Decide whether to pursue the strategic changes suggested or accept current performance. If strategic changes are approved (e.g., adding push notifications as a channel), update the agent's variable list and restart active optimization.

## Time Estimate

- 8 hours: autonomous optimization loop configuration and testing
- 6 hours: announcement health monitor setup
- 4 hours: executive dashboard build
- 2 hours: weekly brief template and Slack integration
- Ongoing: ~1 hour/week reviewing briefs and approving high-risk experiments (~20 hours over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app announcements, nudges, and re-engagement | https://www.intercom.com/pricing — Pro $99/seat/mo |
| Loops | Email announcements and lifecycle follow-ups | https://loops.so/pricing — Growth $99/mo |
| PostHog | Experiments, feature flags, funnels, anomaly detection | https://posthog.com/pricing — Free up to 1M events/mo |
| n8n | Optimization loop scheduling and intervention automation | https://n8n.io/pricing — Free self-hosted |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | https://www.anthropic.com/pricing — ~$15/1M input tokens |
| Attio | Campaign records, experiment logs, and optimization history | https://attio.com/pricing — Plus $119/seat/mo |

**Play-specific cost:** ~$150-350/mo (Anthropic API usage for hypothesis/evaluation, higher-tier Intercom and Loops)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, report weekly
- `autonomous-optimization` — play-specific monitoring: per-feature adoption funnels, decay tracking, health classification, and re-engagement automation
- `dashboard-builder` — builds the PostHog executive dashboard with trial rate trends, experiment history, and convergence tracking
