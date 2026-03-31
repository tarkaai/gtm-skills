---
name: champion-health-monitoring
description: Continuous monitoring of champion engagement health with automated alerts for disengagement and re-engagement triggers
category: Deal Management
tools:
  - Attio
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - attio-champion-tracking
  - attio-reporting
  - champion-engagement-scoring
  - posthog-custom-events
  - posthog-dashboards
  - n8n-scheduling
  - n8n-triggers
  - n8n-crm-integration
---

# Champion Health Monitoring

This drill sets up an always-on monitoring system that tracks champion engagement health, detects disengagement early, and triggers re-engagement workflows before a deal loses its internal advocate.

## Input

- Active champions in Attio (`champion_status` = "Active" or "Recruited")
- PostHog tracking configured for champion events
- n8n instance for scheduling monitoring workflows

## Steps

### 1. Define Champion Health Events in PostHog

Using `posthog-custom-events`, create these events:

| Event Name | When to Fire | Properties |
|------------|--------------|------------|
| `champion_email_sent` | Outbound email to champion | deal_id, champion_id, template |
| `champion_email_replied` | Champion replies to email | deal_id, champion_id, sentiment |
| `champion_meeting_held` | Meeting with champion occurs | deal_id, champion_id, attendees |
| `champion_material_forwarded` | Champion forwards enablement material | deal_id, champion_id, asset_type |
| `champion_introduced_colleague` | Champion makes an internal introduction | deal_id, champion_id, new_contact_title |
| `champion_score_updated` | Engagement score recalculated | deal_id, champion_id, old_score, new_score |
| `champion_status_changed` | Status transition | deal_id, champion_id, old_status, new_status |

### 2. Build Health Check Workflow in n8n

Using `n8n-scheduling` and `n8n-crm-integration`, create a workflow that runs daily at 9:00 AM:

**Step 1:** Query Attio for all People where `champion_status` IN ("Active", "Recruited"):
```
POST https://api.attio.com/v2/objects/people/records/query
{
  "filter": {
    "champion_status": {"in": ["Active", "Recruited"]}
  }
}
```

**Step 2:** For each champion, gather interaction data from the last 14 days:
- Pull notes from Attio (meeting logs, email logs)
- Pull email engagement data from Instantly/Loops
- Pull Loom view data if videos were sent

**Step 3:** Run `champion-engagement-scoring` for each champion using the gathered interaction data. Get back the composite score and health status.

**Step 4:** Compare new score to previous score:
- If score dropped >15 points: trigger "Champion At Risk" alert
- If score increased >10 points: trigger "Champion Strengthening" log
- If no interaction in 14+ days: trigger "Champion Dark" alert

**Step 5:** Update Attio records:
- Write new `champion_score`
- Update `champion_last_engaged`
- If health changed, update `champion_health` on the linked Deal
- Fire `champion_score_updated` event to PostHog

### 3. Configure Alert Routing

Using `n8n-triggers`, set up alert handling:

**Champion At Risk (score dropped >15 or no contact in 14 days):**
1. Send Slack notification to deal owner: "Champion {name} at {company} is disengaging. Score: {old} → {new}. Last interaction: {date}. Suggested action: {recommended_action from scoring}"
2. Create a task in Attio on the Deal: "Re-engage champion — {name}"
3. If champion has been at risk for 7+ consecutive days, escalate: trigger the `champion-recruitment-sequence` drill for a backup champion at the same account

**Champion Dark (no interaction in 21+ days):**
1. Update `champion_status` to "Disengaged"
2. Update Deal's `champion_health` to "At Risk"
3. Immediately trigger `champion-profiling` drill for replacement candidates at this account
4. Alert: "Champion {name} at {company} has gone dark. Replacement profiling initiated."

**Champion Strengthening (score increased >10):**
1. Log the improvement in Attio notes
2. If champion made an introduction, fire `champion_introduced_colleague` event
3. No alert needed — positive trend is captured in dashboards

### 4. Build Champion Health Dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

- **Active Champions by Health:** Pie chart showing Strong/Healthy/At Risk/No Champion distribution
- **Champion Score Trend:** Line chart showing average champion score over time
- **Deals Without Champions:** Table of active deals where `champion_count` = 0
- **Champion Recruitment Funnel:** Funnel from Candidate → Recruited → Active (by week)
- **At-Risk Alert Volume:** Bar chart of at-risk alerts per week (should trend downward)

### 5. Weekly Champion Digest

Every Monday at 8:00 AM, the n8n workflow generates a summary:

```
"Champion Health Digest — Week of {date}

Active Champions: {count} across {deal_count} deals
Average Health Score: {avg_score} ({change} from last week)
Champions At Risk: {at_risk_count}
Champions Gone Dark: {dark_count}
New Champions Recruited: {recruited_count}
Deals Without Champions: {no_champion_count}

Action Items:
{list of at-risk and dark champions with recommended actions}"
```

Post to Slack and store in Attio as a note on the team's pipeline view.

## Output

- Daily automated health checks for all active champions
- Real-time alerts for disengagement (at-risk, dark)
- PostHog dashboard for champion health visibility
- Weekly champion digest with action items
- Automated triggers for replacement champion profiling when a champion goes dark

## Triggers

- Daily health check: n8n cron, 9:00 AM
- Weekly digest: n8n cron, Monday 8:00 AM
- On-demand: when deal owner requests a champion health check
