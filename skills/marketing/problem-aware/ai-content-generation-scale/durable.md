---
name: ai-content-generation-scale-durable
description: >
  AI Content Generation — Durable Intelligence. Always-on AI agents autonomously monitor content
  performance, detect anomalies, generate optimization hypotheses, run A/B experiments, and
  auto-implement winners. The autonomous-optimization loop finds the local maximum for content
  traffic and conversion, then maintains it as market conditions shift.
stage: "Marketing > Problem Aware"
motion: "FounderSocialContent"
channels: "Content"
level: "Durable Intelligence"
time: "100 hours over 6 months"
outcome: "Sustained ≥8,000 page views/month and ≥1.0% conversion rate for 6 consecutive months, with autonomous optimization producing measurable improvements until convergence (<2% gain for 3 consecutive experiments)"
kpis: ["Organic traffic trend", "Conversion rate", "Content production velocity", "Time on page", "Content refresh rate", "Experiment win rate", "Time to convergence"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - autonomous-optimization
  - content-refresh-pipeline
---

# AI Content Generation — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** FounderSocialContent | **Channels:** Content

## Outcomes

The play runs itself. AI agents continuously monitor content performance, detect when metrics plateau or decline, generate hypotheses for improvement, run controlled experiments, and auto-implement winners. The `autonomous-optimization` drill creates the core loop that finds the local maximum -- the best possible content performance given current market conditions -- and maintains it as conditions change. Founder involvement drops to reviewing a weekly optimization brief and approving high-risk changes. Success = sustained 8,000+ page views/month and 1.0%+ conversion rate for 6 consecutive months, with the optimization loop eventually converging.

## Leading Indicators

- Optimization loop running: at least 1 experiment active at all times (until convergence)
- Anomaly detection firing correctly: no metric drops >20% without an alert within 24 hours
- Experiment cycle time: new experiments launching within 48 hours of previous experiment completion
- Weekly optimization briefs generated on schedule every Monday
- Content refresh pipeline processing 5-10 pages per week
- Social content performance monitor dashboard showing stable or improving trends
- Founder time under 1 hour/week (brief review + high-risk approvals only)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the drill that makes Durable fundamentally different from Scalable. Configure it for the AI content generation play:

**Phase 1 — Monitor (daily via n8n cron):**

Build an n8n workflow triggered daily at 8am:

1. Use `posthog-anomaly-detection` to check primary KPIs:
   - Weekly page views (compare last 7 days vs 4-week rolling average)
   - Conversion rate (last 7 days vs 4-week rolling average)
   - Average engagement rate per social post (last 7 days vs 4-week rolling average)
   - Organic search traffic (last 7 days vs 4-week rolling average)
2. Classify each KPI: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
3. If all KPIs are normal: log to Attio, no action. The system is healthy.
4. If any anomaly detected: trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

1. Gather context from Attio: current content pillars, posting cadence, recent A/B test results, keyword rankings
2. Pull 8-week metric history from PostHog using `posthog-dashboards`
3. Run `hypothesis-generation` via Anthropic API:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2048,
  "system": "You are a content strategist analyzing performance data for an AI content generation program. Generate hypotheses for why a metric changed and what to test next. Be specific and actionable.",
  "messages": [
    {
      "role": "user",
      "content": "Anomaly detected: {ANOMALY_TYPE} on {KPI_NAME}.\nCurrent value: {CURRENT_VALUE}\n4-week average: {BASELINE_VALUE}\nChange: {PERCENT_CHANGE}%\n\nContext:\n- Content pillars: {PILLARS}\n- Posting cadence: {CADENCE}\n- Recent test results: {RECENT_TESTS}\n- Top performing content last 30 days: {TOP_CONTENT}\n- Underperforming content last 30 days: {BOTTOM_CONTENT}\n\nGenerate 3 ranked hypotheses. For each:\n1. What changed and why (root cause theory)\n2. What to test (specific experiment design)\n3. Expected impact (% improvement if hypothesis is correct)\n4. Risk level (low/medium/high)\n5. Time to test (days)"
    }
  ]
}
```

4. Store hypotheses in Attio as notes on the content campaign record
5. If top hypothesis has risk = "high": send Slack alert for founder review and STOP
6. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis
2. Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
3. Implement the variant. Content-specific experiment types:
   - **Hook style change:** Generate next 10 posts with the new hook pattern, compare engagement rate
   - **CTA change:** Swap the CTA on existing blog posts via Ghost API, compare conversion rate
   - **Content pillar shift:** Increase posts on a rising pillar by 50%, decrease underperformer by 50%, compare total leads
   - **Posting time change:** Shift schedule by 2 hours, compare impressions
   - **Content length change:** Generate posts at different word counts, compare time on page
4. Set experiment duration: minimum 7 days or 100+ observations per variant (whichever is longer)
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog
2. Run `experiment-evaluation` via Anthropic API with control vs variant data
3. Decision:
   - **Adopt:** Variant wins with 95% confidence. Update live configuration permanently. Log the change.
   - **Iterate:** Results inconclusive but directionally positive. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant lost or no significant difference. Restore control. Log the failure. Return to Phase 1.
   - **Extend:** Insufficient sample size. Keep running for another period.
4. Store full evaluation in Attio: decision, confidence level, net metric impact, reasoning

**Phase 5 — Report (weekly via n8n cron, Monday 9am):**

1. Aggregate all optimization activity for the week
2. Generate a weekly optimization brief via Claude:
   - Anomalies detected this week and their status
   - Experiments running: hypothesis, current data, projected completion
   - Experiments completed: decision and net impact
   - Cumulative metric change from all adopted changes this month
   - Distance from estimated local maximum
   - Recommended focus for next week
3. Post to Slack and store in Attio

### 2. Deploy the content performance monitor

Run the `autonomous-optimization` drill to build the always-on monitoring dashboard:

**Dashboard panels:**
1. **Publishing Cadence:** posts per week by platform, posts by content pillar, target overlay
2. **Engagement Health:** 4-week rolling engagement rate, impressions per post, follower growth, engagement by pillar and format
3. **Lead Generation Funnel:** post_published -> engagement -> profile_visit -> dm_received -> lead_captured -> meeting_booked
4. **Content-to-Pipeline Attribution:** pipeline value from content, top posts by leads generated
5. **Efficiency:** leads per hour of founder time, pipeline value per hour

**Anomaly alerts (feed into autonomous-optimization Phase 2):**
- Engagement rate drops >25% vs 4-week average
- Zero leads captured in 7 days (when baseline is 3+/week)
- Follower growth stalls or goes negative
- High-performer alert: post exceeds 3x average engagement (trigger DM follow-up)

**Automated reports:**
- Weekly performance report: Monday 9am via n8n
- Monthly deep-dive: first Monday of each month
- Content pillar rankings updated monthly

### 3. Deploy the content refresh pipeline

Run the `content-refresh-pipeline` drill to keep published content performing:

**Weekly n8n workflow:**
1. Pull Google Search Console data via API: clicks, impressions, CTR, position per page
2. Pull Ahrefs rank tracking data: position changes over 30 days
3. Categorize pages:
   - **Declining:** position worsened >5 spots in 30 days or clicks dropped >30% MoM. Urgent refresh.
   - **Stuck:** ranking positions 11-30 for >60 days. Needs a push.
   - **Low engagement:** page 1 ranking but engagement rate <20%. Content-intent mismatch.
4. For each flagged page, generate refreshed content via Anthropic API:
   - More comprehensive than top 3 competing results
   - Updated data, examples, and statistics
   - Improved introduction matching search intent
   - Strengthened H2 headings with related keywords
5. Update Ghost CMS via API with refreshed content
6. Log `blog_post_refreshed` event to PostHog
7. Track impact: compare pre/post refresh metrics after 14-28 days

**Target:** refresh 5-10 pages per week. Score each refresh as success/neutral/failure to improve future diagnostics.

### 4. Configure guardrails

**Rate limit:** maximum 1 active experiment per content channel at a time. Never stack experiments on the same variable.

**Revert threshold:** if primary metric (page views or conversion rate) drops >30% during any experiment, auto-revert immediately.

**Human approval required for:**
- Content pillar changes affecting >50% of production
- Budget changes >20% (e.g., upgrading Ahrefs plan, adding new tools)
- Any hypothesis flagged as "high risk" by the diagnosis phase

**Cooldown:** after a failed experiment (revert), wait 7 days before testing the same variable again.

**Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for founder strategic review.

**Convergence detection:** when 3 consecutive experiments produce <2% improvement:
1. The content play has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Generate convergence report: current steady-state metrics, what was tested, why further tactical optimization is unlikely to help
4. Recommend strategic changes if growth is still needed: new channels, new content types, product changes, audience expansion

### 5. Establish the monthly review cycle

**Human action required:** Founder reviews the monthly deep-dive report (generated by the social-content-performance-monitor):
- Which content experiments succeeded this month
- Which topics to retire (declining engagement despite optimization)
- Which new topics to test (emerging ICP pain points, industry trends)
- Content-to-pipeline ROI: is the content investment producing pipeline at an acceptable cost?
- Approve or modify the next month's optimization focus areas

This review takes 30-60 minutes per month. All other operations are autonomous.

## Time Estimate

- Autonomous optimization loop setup: 15 hours
- Content performance monitor dashboard: 8 hours
- Content refresh pipeline setup: 8 hours
- Guardrail configuration: 4 hours
- Monthly founder reviews (6 months x 1 hour): 6 hours
- Weekly brief review (24 weeks x 15 min): 6 hours
- Ongoing monitoring, debugging, and adjustment: 30 hours
- Convergence analysis and documentation: 5 hours
- Final evaluation and playbook documentation: 8 hours
- Emergency intervention buffer: 10 hours
- **Total: ~100 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Anthropic Claude API | Hypothesis generation, experiment evaluation, content refresh, weekly briefs | ~$15-30/mo at Durable volume (https://platform.claude.com/docs/en/about-claude/pricing) |
| Ghost | Blog CMS with API for automated publishing and refresh | $15/mo Starter (https://ghost.org/pricing/) |
| PostHog | Analytics, anomaly detection, experiments, feature flags, dashboards | Free tier or Growth (https://posthog.com/pricing) |
| Taplio | LinkedIn scheduling, analytics, engagement monitoring | $65/mo Standard for analytics (https://taplio.com/pricing) |
| Ahrefs | Keyword tracking, rank monitoring, SERP analysis, content gap detection | $29/mo Starter or $108/mo Lite for API (https://ahrefs.com/pricing) |
| n8n | Automation (optimization loop, refresh pipeline, reports) | Standard stack (excluded) |
| Attio | Campaign records, experiment logs, optimization audit trail | Standard stack (excluded) |

**Play-specific cost: ~$124-218/mo** (Taplio $65 + Ahrefs $29-108 + Ghost $15 + Claude API $15-30)

## Drills Referenced

- `autonomous-optimization` — the always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds and maintains the local maximum for content performance
- `autonomous-optimization` — real-time dashboard with 5 panels, anomaly detection, content-to-pipeline attribution, and automated weekly/monthly reports
- `content-refresh-pipeline` — detect underperforming blog posts, diagnose issues, generate refreshed content, and track refresh impact
