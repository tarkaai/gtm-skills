---
name: stakeholder-intelligence-reporting
description: Build dashboards and reporting for multi-stakeholder discovery effectiveness, coverage trends, and deal impact
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-custom-events
  - attio-reporting
  - attio-deals
  - n8n-workflow-basics
  - n8n-scheduling
---

# Stakeholder Intelligence Reporting

This drill builds the comprehensive reporting layer for the multi-stakeholder discovery play. It creates dashboards that track discovery effectiveness, coverage trends, consensus patterns, and the downstream impact on deal outcomes. This reporting is the data substrate that the `autonomous-optimization` drill reads from at the Durable level.

## Input

- PostHog events from stakeholder discovery activities
- Attio deal records with stakeholder data
- At least 4 weeks of stakeholder discovery data (for meaningful trends)

## Steps

### 1. Build PostHog "Multi-Stakeholder Discovery" Dashboard

Create a dashboard with 6 panels using `posthog-dashboards`:

**Panel 1: Discovery Coverage Funnel**
```
Funnel: stakeholder_mapped → stakeholder_outreach_sent → stakeholder_outreach_replied → stakeholder_discovery_scheduled → discovery_call_completed
```
Shows where stakeholder engagement drops off. Identify the biggest bottleneck.

**Panel 2: Consensus Score Distribution**
```
Insight: Distribution of consensus_score across all active deals
Breakdown by: deal stage
```
Shows the health of the pipeline from a stakeholder alignment perspective.

**Panel 3: Stakeholder Coverage Over Time**
```
Insight: Average stakeholders_engaged_pct per deal, trended weekly
Overlay: Average stakeholders_total per deal
```
Tracks whether multi-threading depth is improving over time.

**Panel 4: Discovery Impact on Win Rate**
```
Insight: Win rate for deals with consensus_score >= 60 at time of proposal vs deals with consensus_score < 60
Breakdown by: quarter
```
The ROI proof: do higher consensus scores predict more wins?

**Panel 5: Stakeholder Role Engagement Rates**
```
Insight: Engagement rate (replied or met) broken down by stakeholder_role
```
Shows which roles are hardest to engage. If Economic Buyers never reply, the outreach approach needs work.

**Panel 6: Time to Full Coverage**
```
Insight: Median days from deal creation to >=75% stakeholder engagement
Breakdown by: deal size, industry
```
Tracks efficiency of the discovery process.

### 2. Build Attio Saved Views

Create 4 Attio saved views:

**"Deals at Risk — Low Consensus"**
- Filter: consensus_score < 40 AND stage IN (Connected, Qualified)
- Sort by: deal value descending
- Columns: company, deal value, stakeholder count, engaged count, consensus score, days at current stage

**"Discovery Gaps — Missing Key Roles"**
- Filter: no Economic Buyer mapped OR no Champion identified
- Sort by: deal value descending
- Columns: company, deal value, roles mapped, missing roles, last activity date

**"Stakeholder Outreach Pipeline"**
- Filter: engagement_status = Unengaged AND influence_score >= 6
- Sort by: influence_score descending
- Columns: name, title, company, role, influence score, deal value

**"Consensus Champions — High Alignment Deals"**
- Filter: consensus_score >= 80 AND stage IN (Connected, Qualified, Proposed)
- Sort by: deal value descending
- Columns: company, deal value, consensus score, stakeholder count, days at stage

### 3. Build Weekly Metrics Export

Create an n8n workflow on a weekly cron (Mondays) that generates a structured metrics snapshot:

1. Query PostHog for the previous week's stakeholder events
2. Calculate:
   - New stakeholders mapped this week
   - Discovery calls completed this week
   - Average consensus score change (improving or degrading?)
   - Outreach reply rate
   - Coverage completeness trend
3. Query Attio for:
   - Deals that advanced stage this week (with their consensus scores)
   - Deals that stalled this week (with their consensus scores)
   - New deals entering the pipeline

4. Generate a structured report:
```
Multi-Stakeholder Discovery — Week of {date}

COVERAGE: {X} stakeholders mapped across {Y} active deals (avg {Z} per deal)
ENGAGEMENT: {A}% reply rate on stakeholder outreach ({B} replies from {C} sent)
CONSENSUS: Average consensus score across pipeline = {D} ({direction} from last week)
IMPACT: {E} deals advanced this week; avg consensus score of advancing deals = {F} vs stalled deals = {G}

TOP RISKS:
- {Deal 1}: consensus dropped {X} points — {reason}
- {Deal 2}: Economic Buyer unengaged for {Y} days

TOP WINS:
- {Deal 3}: consensus reached 85, ready for proposal
- {Deal 4}: successfully engaged {Z} stakeholder who was blocking
```

5. Post to Slack and store in Attio as a note

### 4. Build Monthly ROI Calculation

Create an n8n workflow on a monthly cron that computes the business impact:

1. Compare close rates: deals with comprehensive discovery (>=4 stakeholders engaged, consensus >= 60) vs deals without
2. Compare deal velocity: average days to close for high-discovery vs low-discovery deals
3. Compare deal size: average contract value for high-discovery vs low-discovery deals
4. Estimate monthly ROI: (incremental revenue from better close rate) - (time cost of discovery process)

Store the ROI report in Attio and post to Slack.

## Output

- PostHog dashboard with 6 panels tracking discovery effectiveness
- 4 Attio saved views for operational management
- Weekly metrics snapshot posted to Slack
- Monthly ROI calculation showing business impact
- Data layer that feeds the `autonomous-optimization` drill at Durable level

## Triggers

Run this drill:
- Once during initial setup (create dashboards and views)
- Weekly metrics export runs automatically via n8n
- Monthly ROI calculation runs automatically via n8n
- Dashboard data refreshes continuously as PostHog events arrive
