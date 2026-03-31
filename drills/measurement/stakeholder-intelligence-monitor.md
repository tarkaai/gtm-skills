---
name: stakeholder-intelligence-monitor
description: Continuous monitoring of stakeholder dynamics — org changes, sentiment shifts, and engagement decay across all deals
category: Measurement
tools:
  - Clay
  - Attio
  - n8n
  - PostHog
  - Anthropic
fundamentals:
  - clay-claygent
  - clay-people-search
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-anomaly-detection
  - posthog-dashboards
  - hypothesis-generation
---

# Stakeholder Intelligence Monitor

This drill provides always-on monitoring of stakeholder dynamics across all active deals. It detects org changes (new hires, departures, promotions), tracks sentiment shifts from interaction data, identifies engagement decay before deals stall, and generates intelligence briefs that help the sales team take proactive action.

## Input

- All active deals with stakeholder maps populated in Attio
- Clay with recurring enrichment configured (from `stakeholder-org-mapping` drill)
- PostHog with stakeholder engagement events flowing
- n8n for orchestration and scheduling

## Steps

### 1. Monitor org changes (weekly)

Using `n8n-scheduling`, run a weekly workflow that:
1. Pulls the current people list from Clay for each active account (`clay-people-search`)
2. Compares against the stored stakeholder map in Attio
3. Detects:
   - **New arrivals**: People not in Attio but found in Clay (new hires)
   - **Departures**: People in Attio but missing from Clay (may have left)
   - **Title changes**: Same person, different title (promotion or lateral move)
4. For each change, run `clay-claygent` to research context: "Why did {Company} hire a new {Title}? Is this a newly created role or a backfill?"

### 2. Classify change impact on deals

For each org change detected, assess deal impact:
- **Champion departed**: CRITICAL. Deal is at severe risk. Alert immediately. Identify a new internal advocate or the deal may die.
- **New Economic Buyer arrived**: HIGH. The new budget holder may not inherit the previous one's priorities. Engage within 48 hours.
- **Influencer promoted to VP**: POSITIVE. Your contact now has more authority. Congratulate and re-engage.
- **Procurement contact added**: NEUTRAL-TO-NEGATIVE. May signal the deal is entering formal evaluation. Prepare for process requirements.
- **New IC hire in target department**: LOW. Potential End User to engage for product feedback.

Use Claude (`hypothesis-generation` pattern) to generate a one-paragraph impact assessment per change.

### 3. Track sentiment trajectories

Build a sentiment tracking system from interaction signals:
- After each meeting, use Fireflies transcript → extract sentiment per stakeholder (positive, neutral, negative)
- After each email exchange, classify reply tone (enthusiastic, professional, cold, combative)
- After each no-show or reschedule, log a negative signal

Using `attio-custom-attributes`, maintain a `sentiment_trend` field: Improving, Stable, Declining. Calculate from last 3 interactions.

### 4. Detect engagement decay

Using `posthog-anomaly-detection`, set up anomaly detection for:
- **Individual decay**: A stakeholder's engagement score drops from Active to Cold within 7 days
- **Deal-level decay**: deal_health_score drops >20 points in a single week
- **Role-specific decay**: All Influencers on a deal go Cold simultaneously (may indicate internal priority shift)

### 5. Generate weekly intelligence briefs

Schedule a weekly n8n workflow that compiles:

```
## Stakeholder Intelligence Brief — Week of {date}

### Critical Alerts
- {Company}: Champion {Name} appears to have left. No LinkedIn activity in 30 days. Recommend immediate re-engagement.
- {Company}: Economic Buyer {Name} has not responded to last 3 emails. Sentiment trend: Declining.

### Org Changes Detected
- {Company}: New VP Engineering hired — {Name}. Likely Influencer. Recommended action: LinkedIn connection + intro email.
- {Company}: {Name} promoted from Director to VP Product. Sentiment history: Supportive. Recommended action: Congratulate and re-engage.

### Deal Health Changes
- {Company}: deal_health_score dropped from 72 to 48. Cause: 2 of 3 engaged stakeholders went Cold.
- {Company}: deal_health_score improved from 55 to 78. Cause: New Champion identified and actively engaged.

### Multi-Threading Summary
- Deals with 3+ engaged stakeholders: {X}/{total} ({%})
- Deals with Economic Buyer engaged: {X}/{total} ({%})
- Deals at single-threaded risk: {list}
```

Post to Slack and store as a note in Attio on a "Stakeholder Intelligence" list.

### 6. Feed insights into the autonomous optimization loop

When the `autonomous-optimization` drill is running, this monitor's outputs serve as input signals:
- Engagement decay patterns inform hypotheses about messaging or cadence changes
- Org change frequency informs how often enrichment should refresh
- Sentiment trajectories help evaluate whether optimization experiments are working

## Output

- Weekly intelligence briefs with actionable stakeholder alerts
- Real-time critical alerts for Champion departures and Economic Buyer disengagement
- Org change detection with deal impact assessment
- Sentiment trajectory tracking per stakeholder
- Data feed for the autonomous optimization loop

## Triggers

- Weekly: Full intelligence brief generation (Mondays at 7 AM)
- Daily: Engagement decay detection
- Continuous: Critical alert monitoring via n8n webhook listeners
