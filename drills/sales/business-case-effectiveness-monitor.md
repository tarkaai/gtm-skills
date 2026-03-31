---
name: business-case-effectiveness-monitor
description: Track business case approval rates, time-to-approval, and win rate impact to identify what business case elements drive executive buy-in
category: Sales
tools:
  - PostHog
  - Attio
  - Anthropic
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-deals
  - attio-notes
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# Business Case Effectiveness Monitor

This drill creates an always-on monitoring system that tracks business case effectiveness across all active deals. It identifies which elements of the business case drive executive approval, detects when approval rates decline, and generates actionable recommendations for improving business case quality.

This is the play-specific monitoring drill for the Durable level of `business-case-development`. It works alongside `autonomous-optimization` (which handles the generic experiment loop) by providing business-case-specific signals and context.

## Input

- PostHog events flowing from `business-case-assembly` and `roi-auto-generation` drills
- Attio deal records with `business_case_status`, `business_case_roi`, and outcome data
- n8n instance for scheduled monitoring
- At least 8 weeks of business case data (minimum 10 cases) for meaningful pattern analysis

## Steps

### 1. Build the business case effectiveness dashboard

Create a PostHog dashboard with these panels using `posthog-dashboards`:

**Conversion funnel:**
`business_case_assembled` -> `business_case_sent` -> `business_case_reviewed` -> `executive_approval_scheduled` -> `executive_approval_granted` -> `deal_won`

**Trend panels:**
- Business case approval rate (rolling 4-week average)
- Median time from business case sent to executive approval
- Win rate for deals with business case vs. without
- Average deal size for business-case-assisted deals vs. unassisted
- ROI accuracy: projected vs. realized (from `roi-prediction-accuracy` data)

**Segmentation panels:**
- Approval rate by industry vertical
- Approval rate by deal size tier (<$25K, $25-100K, >$100K)
- Approval rate by executive persona (CFO-led, CEO-led, CTO-led approval)
- Approval rate by strategic alignment score (high/medium/low)
- Time-to-approval by company headcount band

### 2. Set up weekly pattern analysis (n8n cron)

Create an n8n workflow triggered every Monday at 9am:

1. Query PostHog for all business case events from the last 4 weeks
2. Query Attio for all deals where `business_case_status` is set
3. Compute:
   - Overall approval rate this period vs. previous 4 weeks
   - Which business case sections executives engage with most (if tracked)
   - Common objections that emerge after business case review
   - Deals that stalled after business case delivery (sent > 10 days ago, no approval scheduled)
4. Run `hypothesis-generation` with the pattern data to identify improvement opportunities
5. Generate a weekly business case effectiveness brief

### 3. Configure stall detection alerts

Build n8n alert workflows:

- **Stalled deal alert:** If `business_case_sent` > 7 days ago AND no `executive_approval_scheduled` event → send Slack alert to deal owner with recommended re-engagement actions
- **Declining approval rate:** If 4-week rolling approval rate drops > 15% below the 12-week average → send alert to team lead with hypothesis for why
- **Low-ROI case sent:** If `business_case_roi < 200%` → alert: "Weak ROI case sent for {company}. Consider additional discovery before the approval meeting."
- **Blocker engagement needed:** If a deal has an identified Blocker who has not been engaged AND executive approval is scheduled within 7 days → alert to address the Blocker first

### 4. Build the element effectiveness tracker

Track which business case components correlate with approval. For each completed case, log:

```json
{
  "event": "business_case_outcome",
  "properties": {
    "deal_id": "...",
    "outcome": "approved|rejected|stalled|withdrawn",
    "had_strategic_alignment": true,
    "alignment_score": 0.0,
    "had_risk_mitigations": true,
    "risk_count_addressed": 0,
    "had_exec_narratives": true,
    "exec_personas_covered": ["CFO", "CEO"],
    "roi_percentage": 0,
    "payback_months": 0,
    "pain_to_price_ratio": 0,
    "days_to_decision": 0,
    "approval_chain_length": 0,
    "champion_engagement_score": 0
  }
}
```

After 20+ outcomes, run correlation analysis to identify which elements most strongly predict approval. Feed these findings into the `autonomous-optimization` loop as experiment hypotheses.

### 5. Generate monthly effectiveness report

On the 1st of each month, generate a comprehensive report:

- Total business cases delivered vs. approved vs. won
- Approval rate trend (3-month chart)
- Time-to-approval trend
- Top 3 elements that correlated with approval this month
- Top 3 reasons for rejection or stall
- ROI projection accuracy (projected at case creation vs. actual deal outcome)
- Recommendations: which templates, sections, or framing approaches to prioritize

Store the report in Attio and post to Slack.

## Output

- PostHog dashboard with real-time business case effectiveness metrics
- Weekly automated pattern analysis and stall detection
- Alert system for declining performance and stalled deals
- Element-level effectiveness tracking (which components drive approval)
- Monthly effectiveness reports with calibration recommendations

## Triggers

Runs continuously as n8n scheduled workflows. Weekly pattern analysis every Monday. Monthly report on the 1st. Stall detection checks run daily.
