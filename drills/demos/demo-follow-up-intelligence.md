---
name: demo-follow-up-intelligence
description: AI agent that analyzes demo transcripts, historical follow-up outcomes, and prospect behavior to predict optimal follow-up strategies per deal
category: Demos
tools:
  - Anthropic
  - PostHog
  - Attio
  - Fireflies
  - n8n
fundamentals:
  - hypothesis-generation
  - experiment-evaluation
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - attio-deals
  - attio-reporting
  - attio-notes
  - fireflies-transcription
  - n8n-workflow-basics
  - n8n-scheduling
---

# Demo Follow-Up Intelligence

This drill builds the AI intelligence layer that sits on top of the demo follow-up automation. Instead of applying the same cadence to every deal, this agent analyzes each demo's transcript, the prospect's behavioral signals, and historical outcome data to predict which follow-up strategy will work best for each specific deal. It continuously learns from outcomes and surfaces insights about what makes demo follow-ups convert.

## Input

- At least 30 completed follow-up sequences with outcome data (from `demo-follow-up-automation`)
- PostHog event history for all demo follow-up touches
- Attio deal records with demo signals, follow-up touches, and deal outcomes
- Fireflies transcripts for completed demos
- PostHog cohorts and funnels configured for the follow-up pipeline

## Steps

### 1. Build the deal intelligence scoring model

Using `n8n-scheduling`, create a workflow that runs after every demo transcript is processed:

1. Pull the demo transcript analysis (features shown, questions asked, concerns, interest signals, urgency, stakeholders) from Attio
2. Pull historical outcomes: for all past deals with similar characteristics, what follow-up approach produced the best result?
3. Send to Claude for deal-level follow-up strategy prediction:

```
POST https://api.anthropic.com/v1/messages

Prompt: "You are a sales follow-up strategist. Given this demo analysis and our historical follow-up performance data, predict the optimal follow-up strategy for this deal.

This demo:
{demo_extraction_json}

Historical patterns from our {N} completed follow-up sequences:
- Deals with {urgency_level} urgency: {conversion_rate}% booking rate, avg {touches} touches
- Deals where {concern_type} was raised: best performing asset was {asset_type}, best timing was {timing}
- Deals mentioning {stakeholder_count}+ stakeholders: {multi_thread_conversion}% higher conversion when exec summary sent on Day 3
- Deals from {industry}: respond best to {content_type} on touch 2
- Deals with {feature_interest}: highest conversion when {specific_follow_up_approach}

Return JSON:
{
  'deal_score': 1-100,
  'predicted_conversion_probability': 0.0-1.0,
  'recommended_cadence': {
    'recap_timing_hours': N,
    'touch_2_type': 'check_in|value_asset|question_answer',
    'touch_2_day': N,
    'touch_3_asset_type': 'case_study|integration_guide|roi_calculator|loom_video|exec_summary',
    'touch_3_day': N,
    'touch_4_approach': 'next_step_direct|different_angle|stakeholder_outreach',
    'touch_4_day': N,
    'touch_5_needed': true|false
  },
  'personalization_anchors': ['specific thing to reference from demo that predicts engagement'],
  'risk_factors': ['reasons this deal might stall'],
  'recommended_next_step_type': 'technical_deep_dive|proposal|stakeholder_demo|pilot',
  'reasoning': 'why this strategy for this deal'
}"
```

Store the prediction in Attio as a deal note tagged `follow-up-intelligence`.

### 2. Build the adaptive cadence engine

Using `n8n-workflow-basics`, modify the follow-up automation to consume intelligence predictions:

1. When the follow-up cadence starts for a new deal, check if a `follow-up-intelligence` prediction exists
2. If it does: override the default cadence timing, content selection, and approach with the predicted optimal strategy
3. If it doesn't (insufficient data or model not confident): fall back to the default cadence

For each touch, log which strategy was used (predicted vs default) so outcomes can be compared.

### 3. Build the outcome feedback loop

Using `n8n-scheduling`, create a weekly workflow that:

1. Pulls all follow-up sequences completed in the last 7 days
2. For each, records the outcome: next step booked (win), no response (loss), deal stalled, competitor chosen
3. Matches outcomes to the intelligence predictions made at sequence start
4. Calculates prediction accuracy: how often did the AI's predicted strategy outperform the default?
5. Feeds outcomes back to refine future predictions

Using `posthog-cohorts`, build cohorts to track:
- Deals that followed AI-recommended strategy
- Deals that followed default strategy
- Compare conversion rates between cohorts

### 4. Build the cross-deal pattern detector

Using `n8n-scheduling`, create a weekly analysis workflow:

1. Pull all demo transcripts and follow-up outcomes from the last 90 days
2. Send to Claude for pattern detection:

```
Prompt: "Analyze these {N} demo follow-up sequences and their outcomes. Identify patterns:

1. WINNING PATTERNS: What do demos that convert to next steps have in common? (demo characteristics, follow-up timing, content choices)
2. LOSING PATTERNS: What do demos that stall have in common?
3. TIMING INSIGHTS: Is there an optimal follow-up cadence emerging? (specific days/hours that perform best)
4. CONTENT INSIGHTS: Which value assets produce the highest engagement by deal type?
5. PERSONALIZATION INSIGHTS: Which types of demo references in follow-ups correlate with responses?
6. RISK SIGNALS: What demo characteristics predict a deal will stall regardless of follow-up quality?

Return structured JSON with specific, actionable findings."
```

Store findings in Attio. Surface the top 3 actionable insights in the weekly report.

### 5. Build the real-time deal alert system

Using `n8n-triggers` and `posthog-anomaly-detection`, create alerts for follow-up opportunities:

- **Hot deal alert:** When a prospect who received a follow-up visits the pricing page, opens the recap video twice, or forwards the recap to a colleague — notify the founder immediately with recommended action.
- **Stall risk alert:** When a deal that the model predicted as high-probability has not responded to 2+ touches — flag for manual founder outreach with specific talking points from the demo.
- **Multi-thread signal:** When someone new from the prospect's company engages with follow-up content — suggest the founder reach out to this person directly, with context on who they likely are (from org chart data in Attio).

### 6. Build the follow-up intelligence dashboard

Using `posthog-dashboards`, create a dashboard with:

1. **Prediction accuracy:** AI-recommended strategy conversion rate vs default conversion rate (weekly trend)
2. **Follow-up funnel by strategy:** for each cadence variant, show the touch-by-touch dropout
3. **Optimal timing heatmap:** which day/hour combinations produce the most replies
4. **Asset effectiveness ranking:** conversion rate by value asset type
5. **Deal score distribution:** histogram of deal intelligence scores vs actual outcomes
6. **Pattern shift detection:** are winning patterns changing over time? (market shift detection)

### 7. Generate the weekly follow-up intelligence brief

Using `n8n-scheduling` (weekly, Monday 8 AM):

1. Aggregate all follow-up activity and outcomes from the past week
2. Calculate: sequences started, completed, converted, stalled
3. Evaluate: AI prediction accuracy, new patterns detected, anomalies
4. Generate a brief via Claude:

```
## Demo Follow-Up Intelligence Brief — Week of {date}

### Performance
- Sequences active: {N}
- Next steps booked: {N} ({pct}% of completed sequences)
- AI-predicted sequences: {N} at {pct}% conversion vs default at {pct}%

### Key Insight
{most_actionable_finding_this_week}

### Pattern Update
{any_new_patterns_detected_or_changes_to_existing_patterns}

### Deals Needing Attention
{list_of_stalled_high_score_deals_with_recommended_action}

### Recommendation
{one_specific_change_to_make_this_week_based_on_data}
```

Post to Slack and store in Attio.

## Output

- Per-deal follow-up strategy predictions based on demo analysis + historical outcomes
- Adaptive cadence that learns from every sequence
- Cross-deal pattern detection surfacing winning and losing follow-up approaches
- Real-time alerts for hot deals, stall risks, and multi-thread opportunities
- Weekly intelligence brief with actionable recommendations
- Follow-up intelligence dashboard

## Triggers

Deal-level prediction: runs automatically when a new demo transcript is processed. Pattern analysis: weekly. Alerts: real-time via PostHog webhooks. Intelligence brief: weekly Monday 8 AM.
