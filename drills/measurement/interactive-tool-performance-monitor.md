---
name: interactive-tool-performance-monitor
description: Automated monitoring and reporting for interactive content tools — tracks tool funnel health, lead quality, and identifies optimization opportunities
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-retention-analysis
  - attio-reporting
  - n8n-workflow-basics
  - n8n-scheduling
  - anthropic-api-patterns
---

# Interactive Tool Performance Monitor

This drill builds the monitoring and reporting layer for the interactive-content-tools play at Durable level. It tracks tool-specific metrics across the full funnel from impression to revenue, detects changes, and generates actionable weekly briefs that feed into the `autonomous-optimization` drill.

## Input

- PostHog events flowing from interactive tools (at least 4 weeks of data): `tool_viewed`, `tool_started`, `tool_field_completed`, `tool_email_captured`, `tool_results_viewed`, `tool_cta_clicked`
- Nurture pipeline events: `nurture_email_sent`, `nurture_email_opened`, `nurture_cta_clicked`, `nurture_meeting_booked`
- Attio deal records with tool source attribution
- n8n instance for scheduled workflows
- Anthropic API key for brief generation

## Steps

### 1. Build the tool funnel dashboard

Using `posthog-dashboards`, create a dashboard: "Interactive Content Tools — Performance."

**Panel 1: Tool Funnel (weekly trend)**
Funnel: `tool_viewed` → `tool_started` → `tool_email_captured` → `tool_results_viewed` → `tool_cta_clicked` → `nurture_meeting_booked`
Show as weekly trend with conversion rates at each step. Break out by `tool_id`.

**Panel 2: Completion Rate by Tool (bar chart)**
Formula: `tool_results_viewed` / `tool_started` per tool. Target: ≥60% completion rate. Tools below 40% need UX review — likely too many fields or confusing calculation.

**Panel 3: Email Capture Rate (trend)**
Formula: `tool_email_captured` / `tool_started` per week, broken out by `tool_type`. Target: ≥50% capture rate.

**Panel 4: Drop-Off Heatmap (table)**
Group `tool_field_completed` events by `field_position`. Identify which specific fields cause the highest drop-off. This is the most actionable panel — it tells you exactly which question to fix or remove.

**Panel 5: Result Tier Distribution (pie chart)**
Group `tool_results_viewed` by `result_tier` (high/medium/low). Monitor for shifts — if the high-value tier shrinks, either your audience targeting changed or the tool thresholds need recalibration.

**Panel 6: Tool-to-Meeting Conversion (trend)**
Formula: `nurture_meeting_booked` (where source = interactive_tool) / `tool_email_captured` per week. This is the ultimate funnel metric. Target: ≥5% tool-to-meeting conversion.

**Panel 7: Revenue Attribution (number + trend)**
Query Attio deals sourced from tools: total pipeline value, closed-won revenue, average deal size. Compare to other lead sources.

### 2. Configure anomaly detection

Using `posthog-anomaly-detection`, set up monitoring:

- **Completion rate drop**: Any tool's weekly completion rate falls below 50% of its 4-week rolling average. Severity: high. Likely cause: UX issue, page load problem, or mobile breakage.
- **Email capture rate decline**: Weekly capture rate drops >20% from baseline. Severity: high. Likely cause: gate placement issue, form error, or trust deficit.
- **Field drop-off spike**: Any individual field shows >30% drop-off (compared to the previous field). Severity: medium. Likely cause: confusing question, too personal, or requires research to answer.
- **CTA click drop**: Post-result CTA click rate drops below 10%. Severity: medium. Likely cause: weak results display, irrelevant CTA, or result page design issue.
- **Tool-to-meeting rate decline**: Falls below 3% for 2+ consecutive weeks. Severity: high. Likely cause: nurture sequence fatigue, lead quality shift, or broken booking flow.
- **Traffic source shift**: Organic/direct traffic share changes by >20%. Severity: low. Monitor for SEO ranking changes.

### 3. Build the weekly brief generator

Using `n8n-scheduling`, create a workflow running every Monday at 8am:

1. **Pull tool data**: Query PostHog for last 7 days of all `tool_*` and `nurture_*` events. Query Attio for new deals sourced from interactive tools.

2. **Compute metrics**:
   - Total tool views, starts, completions, email captures, CTA clicks, meetings booked
   - Conversion rate at each funnel step (with week-over-week delta)
   - Per-tool breakdown: which tool is performing best/worst
   - Field-level drop-off analysis: which fields are killing completion this week
   - Revenue pipeline from tool leads this week vs last week

3. **Generate the brief**: Using `anthropic-api-patterns`:

```
System: "You are a GTM analyst generating a weekly performance brief for an interactive content tools play. Be direct. Prioritize actionable findings. Keep it under 400 words."

User: "Interactive Content Tools — Week of {DATE}

FUNNEL METRICS:
- Views: {N} ({delta}% WoW)
- Starts: {N} ({delta}% WoW) — Start rate: {X}%
- Completions: {N} ({delta}% WoW) — Completion rate: {X}%
- Email captures: {N} ({delta}% WoW) — Capture rate: {X}%
- Meetings booked: {N} ({delta}% WoW) — Tool-to-meeting: {X}%

PER-TOOL BREAKDOWN:
{tool_id}: {completions}, {capture_rate}%, {meeting_rate}%
{tool_id}: {completions}, {capture_rate}%, {meeting_rate}%

FIELD DROP-OFF (worst 3):
- {field_name} on {tool_id}: {drop_off_rate}% drop-off (position {N})
- {field_name} on {tool_id}: {drop_off_rate}% drop-off (position {N})

ANOMALIES: {list or 'None'}

PIPELINE: {N} new deals worth ${total}, {N} meetings from tool leads

Generate: (1) headline verdict, (2) top finding with recommended action, (3) which tool needs attention and why, (4) one optimization hypothesis to test this week."
```

4. **Distribute**: Post to Slack and log as Attio note.

### 4. Build per-tool health scoring

Using `n8n-workflow-basics`, create a health score for each tool that runs daily:

```
Tool Health Score (0-100):
- Completion rate vs baseline: 30 points (100% of baseline = 30, <50% = 0)
- Email capture rate vs baseline: 25 points
- Tool-to-meeting conversion vs baseline: 25 points
- Traffic trend (growing/stable/declining): 20 points
```

Store health scores in Attio as tool record properties. Alert when any tool drops below 50 health score for 3+ consecutive days.

### 5. Build the monthly attribution report

Using `attio-reporting` and `n8n-scheduling` (first of month):

- Total pipeline sourced from interactive tools this month
- Closed-won revenue attributed to tool leads
- Average deal size: tool leads vs all other lead sources
- Sales cycle length: tool leads vs all other sources
- Which tool generated the highest-value leads
- Which result tier (high/medium/low) produces the best win rate
- Cost per tool lead (hosting + tool platform costs / total email captures)

This report feeds strategic decisions: which tools to invest in, which to retire, and where to build next.

## Output

- PostHog dashboard with 7 panels tracking the complete interactive tool funnel
- Automated anomaly detection with field-level granularity
- Weekly AI-generated performance briefs
- Per-tool health scoring with daily updates
- Monthly attribution reports connecting tools to revenue

## Triggers

Dashboard updates in real-time. Anomaly detection runs daily. Weekly briefs generate every Monday. Monthly attribution on the first of each month. All outputs feed into the `autonomous-optimization` drill for experiment generation.
