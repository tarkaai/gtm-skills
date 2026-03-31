---
name: industry-reports-research-durable
description: >
  Industry Reports & Research — Durable Intelligence. Always-on AI agents continuously
  optimize the report production, distribution, and lead conversion pipeline. The
  autonomous-optimization drill runs the core loop: detect metric anomalies, generate
  improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners.
  Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Social, Email"
level: "Durable Intelligence"
time: "100 hours over 6 months"
outcome: "Sustained or improving lead generation (>=40 qualified leads per report) over 6 months; autonomous optimization loop running with <=2% improvement between successive experiments indicating convergence"
kpis: ["Qualified leads per report (sustained)", "Autonomous experiment win rate", "Download-to-lead conversion trend", "Organic search traffic growth", "Cost per qualified lead trend", "Report-attributed pipeline value"]
slug: "industry-reports-research"
install: "npx gtm-skills add marketing/problem-aware/industry-reports-research"
drills:
  - autonomous-optimization
  - report-performance-monitor
  - industry-research-production
---

# Industry Reports & Research — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Content, Social, Email

## Outcomes

Durable is where the report motion runs itself. An always-on AI agent loop monitors the entire report pipeline -- production quality, distribution effectiveness, landing page conversion, lead quality, and long-tail organic performance -- detects anomalies, generates improvement hypotheses, runs experiments, evaluates results, and auto-implements winners. The goal is finding the local maximum of report-driven lead generation and maintaining it as the market shifts. The `autonomous-optimization` drill runs the core loop. The `report-performance-monitor` drill provides the data feeds. Topic selection, distribution timing, and follow-up sequences all evolve based on experiment results rather than guesswork.

**Pass threshold:** Sustained or improving lead generation (>=40 qualified leads per report) over 6 months. The autonomous optimization loop has run at least 12 experiments and reached convergence (successive experiments produce <2% improvement on the primary metric).

## Leading Indicators

- Anomaly detection catches metric changes within 24 hours of onset
- Hypothesis generation produces actionable, testable experiments (not vague suggestions like "improve content quality")
- At least 2 out of every 4 experiments produce positive results (>=50% win rate)
- Weekly optimization briefs generate no "critical" alerts for 4+ consecutive weeks
- Cost per qualified lead trends flat or downward over 3+ months
- Report-attributed pipeline value grows quarter-over-quarter
- Organic search traffic to report pages grows month-over-month (compounding asset)
- Report backlink portfolio grows to 20+ referring domains per report within 6 months
- Report refresh cycle produces measurable download lifts (updated reports outperform originals)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This creates the core agent loop applied to the report pipeline:

**Monitor (daily via n8n cron):**
The optimization agent checks all report KPIs against the 4-week rolling average using PostHog anomaly detection. It classifies each metric:
- **Normal** (within +/-10%): No action. Log to Attio.
- **Plateau** (+/-2% for 3+ weeks): Trigger hypothesis generation. The metric has stopped improving.
- **Drop** (>20% decline): Urgent. Trigger hypothesis generation with high priority.
- **Spike** (>50% increase): Investigate cause. If attributable to a specific change, document and replicate.

Metrics monitored daily:
- Weekly downloads per report (current vs rolling baseline)
- Landing page conversion rate per report
- Download-to-qualified-lead conversion rate
- Social share velocity per active distribution campaign
- Follow-up email reply rate

Metrics monitored weekly:
- Organic search impressions and clicks for report pages
- New backlinks acquired per report
- Report-attributed meetings booked
- Cost per qualified lead

**Diagnose (triggered by anomaly):**
The agent pulls 8 weeks of PostHog data plus the current report portfolio state from Attio (active reports, distribution status, landing page variants, follow-up sequence variants). It runs Claude to generate 3 ranked hypotheses. Each hypothesis includes:
- What to change (specific variable)
- Expected impact (quantified)
- Risk level (low/medium/high)
- Measurement approach

Examples of the kinds of hypotheses the system should generate:
- "Download conversion dropped 22% after adding a third form field. Hypothesis: removing the 'job title' field will restore conversion to baseline. Expected impact: +15-25% conversion. Risk: low (easy to revert)."
- "Organic traffic to the Q1 report has plateaued. Hypothesis: updating the report with Q2 data and republishing will generate a new ranking signal. Expected impact: +30-50% organic traffic within 4 weeks. Risk: low."
- "Follow-up email reply rate dropped from 12% to 6%. Hypothesis: the follow-up references a finding that is now 3 months old. Updating the email to reference the most recent report finding will improve relevance. Expected impact: +50% reply rate. Risk: low."

Low/medium risk hypotheses proceed automatically to experiment. High risk hypotheses (e.g., changing the gating model, budget changes >20%, topic pivot) trigger a Slack alert for human review.

**Experiment (triggered by hypothesis acceptance):**
The agent creates a PostHog experiment with feature flag to split traffic between control and variant. It implements the variant using the appropriate tool:
- Landing page changes: PostHog feature flag to show variant page
- Email changes: n8n workflow to route new leads to variant follow-up
- Distribution changes: alternate social post variants on consecutive days
- Topic/content changes: queue as a manual task for the next production cycle

Minimum experiment duration: 7 days or 200 visitors per variant (for landing page tests) / 50 sends per variant (for email tests), whichever is longer. Never run more than 1 experiment per report at a time.

**Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog, runs statistical evaluation, and decides:
- **Adopt:** Implement the winner permanently. Update the default configuration. Log the change and impact.
- **Iterate:** The result showed a directional signal but was not conclusive. Generate a refined hypothesis and re-run.
- **Revert:** Roll back. Log the failure with reasoning. Return to Monitor.
- **Extend:** The experiment needs more data. Keep running for another period.

Store every evaluation (decision, confidence level, reasoning, raw metrics) in Attio for audit trail.

**Report (weekly via n8n cron):**
Generate a weekly optimization brief summarizing: anomalies detected, experiments run, decisions made, net KPI impact, current distance from estimated local maximum, and recommended focus areas for the coming week.

### 2. Deploy the report performance monitoring layer

Run the `report-performance-monitor` drill. This builds:

- **Master dashboard** in PostHog with 5 panels: download funnel per report, lead generation trend, distribution channel performance, long-tail organic performance, and content-to-pipeline attribution.
- **Anomaly detection** feeding into the autonomous optimization loop: download declines, conversion drops, lead droughts, channel decay, and SEO ranking losses.
- **Automated weekly briefs** posted to Slack every Monday: headline performance, per-report metrics, distribution channel breakdown, anomalies detected, and recommended actions.
- **Quarterly deep-dive reports:** Report portfolio review ranking all published reports by total pipeline value. Recommendations for which reports to refresh, which to retire, and what topic to cover next.

The performance monitor feeds structured signals into the autonomous optimization loop. When the monitor detects an anomaly, it passes a structured signal (metric, current value, baseline, change, context) that the optimizer uses to generate targeted hypotheses.

### 3. Optimize the report production pipeline

Run the `industry-research-production` drill on a quarterly cadence, but with optimization-driven improvements:

- **Topic selection via data:** The agent analyzes download patterns, lead quality, and pipeline value from past reports to recommend topics. It cross-references with search volume trends, competitor report gaps, and ICP pain point frequency from Clay enrichment data.
- **Data collection optimization:** Track survey response rates and completion rates across reports. The agent tests different survey lengths, incentive types, and distribution methods to maximize response rates.
- **Report format optimization:** Based on download-to-lead conversion data, the agent recommends format changes: shorter vs longer reports, more vs fewer charts, gated vs ungated access models.
- **Production efficiency:** Track founder time per report. Identify which production steps consume the most time and prioritize automation or template creation for those steps.

**Report refresh cycle:** For existing reports, the agent monitors organic search performance. When a report's organic traffic plateaus, it queues a refresh task: update the data with new findings, republish with the current year, and re-promote. Refreshed reports often outperform the original because the existing backlinks and search authority carry forward.

### 4. Establish guardrails for autonomous operation

**Critical guardrails the agent must never override:**

- Maximum 1 active experiment per report at any time. Never stack experiments.
- If primary metric (download-to-lead conversion) drops >30% during any experiment, auto-revert immediately.
- Human approval required for: budget changes >20%, gating model changes (gated to ungated or vice versa), topic selection for new reports, any hypothesis flagged as high risk.
- Cooldown: after a failed experiment (revert), wait 7 days before testing the same variable.
- Maximum 4 experiments per month across the entire report portfolio. If all 4 fail in a month, pause optimization and alert the founder for strategic review.
- Never change the report content itself without founder review. The agent can test distribution, landing pages, follow-ups, and promotion -- but not the research findings or analysis.
- Report production requires founder review of all data points, findings, and conclusions before publication. This is never automated away.

### 5. Monitor for convergence

The autonomous loop runs indefinitely. Watch for convergence signals:

- 3 consecutive experiments produce <2% improvement on the primary metric (qualified leads per report)
- Weekly optimization briefs show "no anomalies" for 4+ consecutive weeks
- Cost per qualified lead has been flat (+/-5%) for 8+ weeks
- Landing page conversion has been stable for 6+ weeks

At convergence:
1. The report motion has reached its local maximum
2. Reduce monitoring from daily to weekly
3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
4. Report to the team: "Report-driven lead gen is optimized at [current metrics]. Further gains require strategic changes -- new report formats (video reports, interactive tools), new distribution channels (paid promotion, conference partnerships), or new audience segments -- not tactical optimization."

The agent continues monitoring to detect market shifts (competitor report launches, search algorithm changes, ICP pain point evolution) that may disrupt convergence and require a new optimization cycle.

## Time Estimate

- Autonomous optimization setup: 12 hours
- Report performance monitor setup: 8 hours
- Quarterly report production (2 reports x 12 hours): 24 hours
- Monthly review and human approvals (3 hrs/month x 6 months): 18 hours
- Experiment review and decision logging (2 hrs/month x 6 months): 12 hours
- Quarterly strategic reviews (4 hrs x 2): 8 hours
- Report refresh cycles (4 hrs x 2 refreshes): 8 hours
- Distribution optimization and testing: 10 hours
- **Total: ~100 hours over 6 months** (front-loaded: 32 hours in month 1, then ~14 hrs/month)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Data collection, enrichment, lead scoring | Growth: $495/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Typeform | Surveys at scale | Business: $50/mo ([typeform.com/pricing](https://www.typeform.com/pricing)) |
| Ghost | Report hosting, blog, newsletters | Creator: $25/mo ([ghost.org/pricing](https://ghost.org/pricing/)) |
| Loops | Email broadcasts and nurture sequences | Growth: $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| PostHog | Analytics, experiments, anomaly detection | Free tier up to 1M events; ~$50/mo for 2M ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation (optimization loop, monitoring, distribution) | Pro: ~$60/mo — 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM, pipeline tracking, experiment logging | Pro: $59/user/mo ([attio.com](https://attio.com)) |
| Ahrefs | SEO monitoring, backlink tracking, keyword research | Lite: $99/mo ([ahrefs.com/pricing](https://ahrefs.com/pricing)) |
| Anthropic API | Hypothesis generation, report production, optimization briefs | ~$15-25/mo for weekly optimization + quarterly production ([anthropic.com](https://www.anthropic.com)) |

**Estimated monthly cost: ~$900-1,000/mo** (Clay Growth + Typeform Business + Ghost Creator + Loops Growth + PostHog + n8n Pro + Attio Pro + Ahrefs Lite + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-report loop that finds the local maximum
- `report-performance-monitor` — dashboard, anomaly detection, weekly briefs, and content-to-pipeline attribution specific to reports
- `industry-research-production` — quarterly report production with optimization-driven topic selection and format improvements
