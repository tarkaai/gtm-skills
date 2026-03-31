---
name: report-performance-monitor
description: Always-on monitoring and reporting for industry report performance including downloads, leads, backlinks, and content-to-pipeline attribution
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - ahrefs-backlink-analysis
---

# Report Performance Monitor

This drill builds the always-on monitoring and reporting system specific to industry reports and research plays. It tracks the full funnel from report publication through pipeline creation, monitors long-tail performance (reports generate leads for months after publication), and provides the data feeds required by the `autonomous-optimization` drill for experiment prioritization.

## Input

- PostHog with report events flowing (from `posthog-gtm-events` drill)
- Attio with lead records attributed to report downloads
- At least 1 published report with 4+ weeks of data (baseline for anomaly detection)
- n8n instance for automated monitoring
- Ahrefs or equivalent for backlink monitoring (optional but recommended at Scalable+)

## Steps

### 1. Build the Report Performance Dashboard

Using the `posthog-dashboards` fundamental, create an "Industry Reports" dashboard:

**Panel 1 -- Download Funnel:**
- Funnel: report_page_viewed -> report_form_started (if gated) -> report_downloaded -> report_shared
- Trend: downloads per week (8-week rolling, by report)
- Conversion rate: page view to download
- Breakdown by traffic source (organic, social, email, direct, referral)

**Panel 2 -- Lead Generation:**
- Trend: leads captured from reports per week
- Trend: leads by report (which report generates the most leads over time)
- Funnel: report_downloaded -> lead_enriched (ICP match confirmed) -> meeting_booked -> deal_created
- Conversion rate: download to qualified lead, lead to meeting, meeting to deal

**Panel 3 -- Distribution Channel Performance:**
- Bar chart: downloads by distribution channel (LinkedIn, email, blog, community, PR)
- Bar chart: leads by distribution channel
- Efficiency: cost per download and cost per lead by channel
- Social share count per report

**Panel 4 -- Long-Tail Performance:**
- Trend: downloads per week by report age (weeks since publication)
- Identify which reports continue generating downloads after 30, 60, 90 days (evergreen vs spike)
- SEO traffic trend to report landing pages (organic search as persistent lead source)

**Panel 5 -- Content-to-Pipeline Attribution:**
- Number: total pipeline value attributed to reports this quarter
- Trend: pipeline value per report per month
- Table: all reports ranked by total pipeline value generated
- Average deal size from report-sourced leads vs other sources

### 2. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, monitor:

**Download anomalies (check daily):**
- Weekly downloads drop >30% vs 4-week rolling average -> trigger: "download-decline"
- Landing page conversion rate drops >20% -> trigger: "conversion-decline"
- Gated form abandonment rate spikes >50% -> trigger: "form-friction"

**Lead anomalies (check daily):**
- Zero qualified leads from reports in 14 days (when baseline is 2+/week) -> trigger: "lead-drought"
- Download-to-lead conversion drops below historical baseline -> trigger: "quality-decline"

**Distribution anomalies (check weekly):**
- A distribution channel that previously drove 20%+ of downloads drops below 5% -> trigger: "channel-decay"
- Social share velocity drops to zero for 2+ weeks -> trigger: "virality-stall"

**Long-tail anomalies (check monthly):**
- Report that was generating steady organic downloads suddenly stops -> trigger: "seo-decline" (investigate ranking loss)
- Backlink velocity stalls on most recent report -> trigger: "backlink-stall"

Each anomaly trigger feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose) with context about which report and which metric.

### 3. Implement the event taxonomy

Using `posthog-custom-events`, implement these report-specific events:

1. `report_page_viewed` -- properties: report_slug, report_title, source, utm_source, utm_campaign, utm_medium
2. `report_form_started` -- properties: report_slug (for gated reports, fires when form receives focus)
3. `report_downloaded` -- properties: report_slug, email, company, title, source
4. `report_scroll_depth` -- properties: report_slug, depth_percent (25/50/75/100), time_on_page
5. `report_shared` -- properties: report_slug, platform (linkedin/twitter/email/other)
6. `report_lead_qualified` -- properties: report_slug, lead_email, icp_score, enrichment_data
7. `report_meeting_booked` -- properties: report_slug, lead_email, days_from_download
8. `report_deal_created` -- properties: report_slug, deal_value, lead_email

Build a PostHog funnel from events 1-8 to visualize full-funnel conversion per report.

### 4. Automate weekly performance reports

Using `n8n-scheduling` and `n8n-workflow-basics`, build a weekly report workflow:

**Trigger:** Monday at 9am

**Data collection:**
1. Pull last 7 days of report events from PostHog API
2. Pull lead and meeting data from Attio using `attio-reporting`
3. Pull backlink data from Ahrefs API using `ahrefs-backlink-analysis` (weekly)

**Report generation via Claude API:**
```
Prompt: "You are analyzing industry report performance for the past week. Data: {DATA}. 4-week baseline: {BASELINE}. Generate:
1. Executive summary (2 sentences)
2. Per-report performance table (downloads, leads, meetings this week vs 4-week avg)
3. Distribution channel breakdown (which channels drove the most downloads)
4. Long-tail report: which older reports are still generating downloads
5. Backlink update: new backlinks acquired this week
6. Anomalies detected and recommended actions
7. Recommended next report topic based on download patterns and lead quality
Keep under 500 words. Use specific numbers."
```

**Delivery:**
- Post to Slack
- Store in Attio as a note on the reports campaign record
- If anomaly detected, prepend "ANOMALY:" section with severity and recommended action

### 5. Build quarterly deep-dive reports

Monthly on the first Monday, generate an expanded report:

- **Report portfolio review**: Rank all published reports by total pipeline value generated. Recommend which to refresh (update data), which to retire (no longer generating leads), and which topic to cover next.
- **Topic performance analysis**: Which pain points/topics generate the highest quality leads (measured by downstream conversion)?
- **Distribution effectiveness**: Which channels have the best download-to-lead and lead-to-meeting ratios?
- **Competitive landscape**: Have competitors published competing reports? Is your report still the most cited/linked source?
- **SEO performance**: Organic search rankings for report landing pages. Keyword positions trending up or down.
- **Backlink portfolio**: Total backlinks per report, referring domains, domain authority of linkers.

### 6. Feed optimization signals to autonomous-optimization

Structure the monitoring output to directly feed the `autonomous-optimization` drill:

For each anomaly detected, output a structured signal:
```json
{
  "play": "industry-reports-research",
  "metric": "download_rate",
  "current_value": 42,
  "baseline_value": 67,
  "change_pct": -37,
  "anomaly_type": "drop",
  "context": "Landing page conversion rate dropped after changing form fields",
  "suggested_experiment_area": "form_fields",
  "affected_report": "state-of-ai-ops-2026"
}
```

This structured output lets the optimizer generate targeted hypotheses rather than generic improvement suggestions.

## Output

- Real-time PostHog dashboard with 5 panels covering downloads, leads, channels, long-tail, and pipeline
- Anomaly detection feeding into autonomous optimization loop
- Full report-to-pipeline attribution tracking
- Automated weekly and quarterly performance reports
- Structured optimization signals for the `autonomous-optimization` drill

## Triggers

Dashboard is always-on. Anomaly detection runs daily via n8n. Weekly reports fire every Monday at 9am. Quarterly deep-dives fire first Monday of each quarter. Alert routing fires in real-time for critical anomalies.
