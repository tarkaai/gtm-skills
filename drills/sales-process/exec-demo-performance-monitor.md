---
name: exec-demo-performance-monitor
description: Monitor executive demo effectiveness by persona, track deal velocity impact, and detect conversion degradation patterns
category: Demos
tools:
  - PostHog
  - n8n
  - Attio
  - Fireflies
fundamentals:
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-dashboards
  - n8n-scheduling
  - n8n-triggers
  - attio-deals
  - attio-reporting
  - fireflies-transcription
---

# Executive Demo Performance Monitor

This drill builds an always-on monitoring system for executive-focused demos. Unlike the generic `demo-performance-monitor`, this drill tracks persona-level effectiveness, measures how exec engagement impacts deal velocity and close rates, and surfaces which ROI narratives and demo structures produce the best outcomes by executive persona.

## Input

- PostHog events from `exec-demo-prep` drill (`exec_demo_prep_generated`, `exec_demo_completed`)
- Attio deal records with exec engagement data and BANT scores
- Fireflies transcripts for exec demo calls
- At least 2 weeks of baseline exec demo data (minimum 5 exec demos)

## Steps

### 1. Define the exec demo event taxonomy

Using `posthog-custom-events`, ensure these events are captured:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `exec_demo_prep_generated` | Prep doc created | `deal_id`, `exec_persona`, `research_depth`, `roi_narrative_generated` |
| `exec_demo_scheduled` | Cal.com booking confirmed | `deal_id`, `exec_persona`, `exec_title`, `days_since_discovery`, `attendee_count` |
| `exec_demo_completed` | Demo call ended and logged | `deal_id`, `exec_persona`, `outcome`, `duration_minutes`, `questions_asked`, `sentiment_score`, `next_step_type` |
| `exec_followup_sent` | Follow-up email/summary sent | `deal_id`, `exec_persona`, `followup_type`, `time_since_demo_hours` |
| `exec_nextstep_committed` | Exec agreed to next meeting | `deal_id`, `exec_persona`, `next_step_type` |
| `exec_proposal_requested` | Exec requested pricing/proposal | `deal_id`, `deal_value` |
| `exec_deal_accelerated` | Deal velocity increased post-exec engagement | `deal_id`, `velocity_delta_days`, `exec_personas_engaged` |

### 2. Build the exec demo funnel in PostHog

Using `posthog-funnels`, create a saved funnel:

`exec_demo_scheduled` -> `exec_demo_completed` -> `exec_nextstep_committed` -> `exec_proposal_requested` -> `deal_closed_won`

Break down by:
- `exec_persona` -- which persona converts best (CEO vs CFO vs CTO)
- `research_depth` -- does deeper research improve conversion
- `roi_narrative_generated` -- do demos with ROI narratives outperform those without
- `duration_minutes` buckets (10-15, 15-20, 20-30) -- optimal demo length
- `attendee_count` -- single exec vs multi-exec demos

Save as: "Executive Demo -- Full Funnel by Persona"

### 3. Build the exec demo effectiveness dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

1. **Exec demo conversion by persona**: Bar chart of nextstep rate per exec persona (CEO, CFO, CTO, etc.)
2. **Deal velocity: exec-engaged vs non-exec**: Line chart comparing days-in-pipeline for deals with and without exec engagement
3. **Close rate: exec-engaged vs non-exec**: Side-by-side conversion rates
4. **ROI narrative effectiveness**: Conversion rate for demos with vs without ROI narrative generation
5. **Exec demo volume trend**: Weekly count of exec demos by persona
6. **Optimal demo duration**: Scatter plot of demo duration vs next-step rate
7. **Sentiment score trend**: Average exec sentiment score over time
8. **Multi-exec alignment**: Conversion rate by number of execs engaged per deal
9. **Research depth impact**: Conversion rate by research_depth (full, partial, persona_only)
10. **Time-to-demo**: Days from scheduling to demo, correlated with outcome

### 4. Build n8n monitoring workflows

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 7 days of exec demo funnel data
2. Compute per-persona conversion rates:
   - CEO demos: nextstep rate, proposal rate
   - CFO demos: nextstep rate, proposal rate
   - CTO demos: nextstep rate, proposal rate
3. Compute exec engagement impact:
   - Average deal velocity for exec-engaged deals vs all deals
   - Close rate for exec-engaged deals vs all deals
4. Compare to baseline using `posthog-anomaly-detection`:
   - **Normal**: within +/-15% of 4-week rolling average
   - **Warning**: 15-30% below average for 3+ consecutive days
   - **Critical**: >30% below average for 2+ consecutive days
5. For Warning/Critical: send Slack alert with per-persona degradation details and probable cause

### 5. Build the ROI narrative effectiveness report

Create a weekly n8n workflow that:

1. Pulls all `exec_demo_completed` events from the last 30 days
2. Groups by `exec_persona` and `roi_narrative_generated`
3. For each persona, calculates:
   - Nextstep rate with ROI narrative vs without
   - Proposal rate with ROI narrative vs without
   - Average sentiment score with vs without
4. Identifies which ROI narratives (key_numbers, opening hooks) correlate with highest conversion
5. Generates a ranking report: "For CFOs, payback period framing converts at 85% vs 60% for NPV framing"
6. Stores the report in Attio as a campaign note

### 6. Track exec demo quality from transcripts

After each exec demo, use Fireflies transcript + Claude to auto-score quality:

| Dimension | Score 1-5 | How measured |
|-----------|-----------|-------------|
| Strategic framing | Did the rep lead with business outcomes, not features? | Count of strategic vs tactical statements |
| Persona alignment | Was the language appropriate for the exec's role? | Match between talking points and persona expectations |
| ROI delivery | Were quantified ROI estimates presented? | Presence of specific numbers |
| Engagement | Did the exec ask questions and engage? | Count of exec questions and positive signals |
| Time discipline | Did the demo stay within 15-20 minutes? | Duration check |
| Close quality | Was a clear, specific next step proposed? | Presence of concrete proposal |

Store scores on the deal in Attio. Correlate quality scores with deal outcomes to find which dimensions matter most per persona.

### 7. Detect competitive signals

Monitor exec demo transcripts for competitive mentions:
- If an exec names a competitor, log it with context
- If multiple execs across different deals mention the same competitor in the same week, flag a competitive trend alert
- Feed competitor mention data into the demo prep workflow so future exec demos proactively address competitive concerns

## Output

- Real-time exec demo conversion funnel with persona breakdown
- Daily automated monitoring with per-persona anomaly alerts
- Weekly ROI narrative effectiveness ranking by persona
- Exec demo quality scoring from transcript analysis
- Deal velocity impact measurement (exec-engaged vs non-exec)
- Competitive signal detection from exec demo transcripts

## Triggers

- Daily monitoring: runs every day at 9 AM via n8n cron
- Weekly effectiveness report: runs every Monday at 8 AM via n8n cron
- Event-triggered: fires on every `exec_demo_completed` event for quality scoring
- Ad-hoc: fires when a competitive signal threshold is crossed (3+ mentions of same competitor in 7 days)
