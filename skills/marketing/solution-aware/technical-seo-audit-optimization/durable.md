---
name: technical-seo-audit-optimization-durable
description: >
  Technical SEO Audit & Optimization — Durable Intelligence. AI agents autonomously
  optimize the site's technical SEO: detect metric anomalies, generate improvement
  hypotheses, run A/B experiments, evaluate results, and auto-implement winners.
  Converges when successive experiments produce < 2% improvement.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Durable Intelligence"
time: "Ongoing (2-4 hours/month oversight)"
outcome: "Sustained >= 10% QoQ organic traffic growth and green Core Web Vitals for 12+ months via autonomous optimization"
kpis: ["QoQ organic traffic growth", "Experiment win rate", "Mean time to fix regressions", "Core Web Vitals pass rate (all pages)", "Organic conversion rate", "Autonomous fix success rate"]
slug: "technical-seo-audit-optimization"
install: "npx gtm-skills add marketing/solution-aware/technical-seo-audit-optimization"
drills:
  - autonomous-optimization
  - seo-performance-monitor
---

# Technical SEO Audit & Optimization — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

The technical SEO system operates autonomously. The agent continuously monitors all metrics, detects anomalies and plateaus, generates hypotheses for improvement, designs and runs experiments, evaluates results, and auto-implements winners. Sustained >= 10% quarter-over-quarter organic traffic growth with all Core Web Vitals in the "Good" range across every page for 12+ months. The agent produces weekly optimization briefs documenting what changed, why, and the measured impact.

## Leading Indicators

- Agent generates at least 2 testable hypotheses per month
- Experiment win rate > 40% (4 out of 10 experiments produce measurable improvement)
- No CRITICAL regressions persist for more than 24 hours
- Organic conversion rate (visit -> lead) trends upward over 3+ months
- Weekly optimization briefs show continued progress toward local maximum
- Time between convergence detection and strategic review < 7 days

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for technical SEO metrics. The drill creates a continuous loop:

**Monitor (daily via n8n cron):**
1. Pull the play's primary KPIs from PostHog and GSC: organic clicks, impressions, average position, indexation rate, average performance score, CWV scores
2. Compare last 2 weeks against 4-week rolling average
3. Classify each metric: **normal** (within 10%), **plateau** (within 2% for 3+ weeks), **drop** (> 20% decline), **spike** (> 50% increase)
4. If all metrics are normal: log to Attio, no action needed
5. If anomaly or plateau detected: trigger the Diagnose phase

**Diagnose (triggered by anomaly detection):**
1. Gather context: current site configuration, recent deployments, GSC crawl stats, competitive landscape from Ahrefs
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with the anomaly data. For technical SEO, hypotheses may include:
   - "Switching to a different image CDN configuration could reduce LCP by 300ms"
   - "Adding preload hints for critical CSS could improve performance score by 10 points"
   - "Restructuring internal linking to pass more link equity to money pages could improve average position by 3 ranks"
   - "Implementing dynamic rendering for JavaScript content could increase indexed page count by 15%"
   - "Optimizing meta descriptions for top-20-by-impressions pages could increase CTR by 20%"
4. Receive 3 ranked hypotheses with expected impact and risk levels
5. Store hypotheses in Attio as notes on the play's campaign record
6. If the top hypothesis has risk = "high": send Slack alert for human review and STOP
7. If risk = "low" or "medium": proceed to Experiment

**Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment:
   - For performance changes: use PostHog feature flags to serve optimized vs. original page variants
   - For metadata changes: A/B test different title/description variants by deploying to a subset of pages
   - For structural changes: implement on a subset of pages and compare ranking/traffic trends vs. a control set
3. Set experiment duration: minimum 14 days or until 200+ organic sessions per variant
4. Log the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog and GSC
2. Run `experiment-evaluation` comparing control vs. variant
3. Decision:
   - **Adopt**: Variant wins. Roll out to all affected pages. Log the change and measured impact.
   - **Iterate**: Mixed results. Generate a refined hypothesis and return to Diagnose.
   - **Revert**: Variant loses. Remove the change. Log the failure.
   - **Extend**: Not enough data. Continue the experiment for another period.
4. Store the full evaluation (decision, confidence, reasoning) in Attio

**Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments running/completed, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate a weekly optimization brief:
   - What changed and why
   - Net impact on organic traffic, rankings, CWV scores
   - Current estimated distance from local maximum
   - Recommended focus for next week
4. Post the brief to Slack and store in Attio

### 2. Maintain regression defense

The `autonomous-optimization` drill continues running at full coverage:

1. All monitors from Scalable level remain active (robots.txt, indexation, CWV, sitemap, deployment-triggered)
2. Add experiment-aware monitoring: the regression monitor knows which experiments are active and excludes those pages from regression alerts (to avoid false positives during experiments)
3. If a regression is detected on a non-experiment page, the agent fixes it immediately using the automated fix pipeline from Scalable level
4. MTTF target: < 24 hours for CRITICAL, < 48 hours for HIGH

### 3. Track organic conversion attribution

The `seo-performance-monitor` drill at Durable level adds conversion attribution:

1. Track the full organic funnel: `organic_visit` -> `page_engaged` -> `cta_clicked` -> `lead_created` -> `opportunity_created`
2. Attribute leads and pipeline revenue to specific pages and keywords
3. Use conversion data to inform optimization priorities: pages with high traffic but low conversion rate are optimization candidates
4. Feed conversion data into the autonomous optimization loop as an additional signal for hypothesis generation

### 4. Detect convergence

The autonomous optimization loop runs indefinitely. However, it detects convergence:

1. If 3 consecutive experiments produce < 2% improvement on the target metric, the play has reached its local maximum
2. At convergence:
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment frequency from monthly to quarterly
   - Report to the team: "Technical SEO is optimized. Current performance: [metrics]. Further organic growth requires strategic changes — new content, new backlinks, new markets — rather than tactical technical optimization."
3. Continue regression monitoring at full frequency even after convergence (the site still needs protection from regressions)

### 5. Respond to algorithm updates

When the agent detects a sudden ranking or traffic change that doesn't correlate with any deployment or site change:

1. Check industry news and Google announcements for algorithm updates
2. If an algorithm update is confirmed:
   - Increase monitoring frequency temporarily (daily CWV checks, hourly indexation checks)
   - Run a full site crawl immediately
   - Compare before/after rankings at the page level
   - Generate hypotheses specifically targeted at the update's known focus areas
   - Resume the standard optimization loop with algorithm-specific context

## Time Estimate

- Autonomous optimization loop setup: 4 hours (one-time)
- Ongoing human oversight: 2-4 hours/month (reviewing weekly briefs, approving high-risk experiments, strategic decisions)
- Algorithm update response: 2-4 hours per event (estimated 2-4 per year)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Screaming Frog SEO Spider | Automated crawling and regression detection | $259/year — https://www.screamingfrog.co.uk/seo-spider/pricing/ |
| Google Search Console | Indexation, search analytics, re-indexing | Free — https://search.google.com/search-console |
| Google PageSpeed Insights | CWV monitoring and experiment measurement | Free — https://pagespeed.web.dev/ |
| Ahrefs | Ranking data, competitive monitoring, experiment evaluation | $199/mo (Standard) — https://ahrefs.com/pricing |
| PostHog | Experimentation platform, dashboards, conversion funnels | Free up to 1M events/mo — https://posthog.com/pricing |
| n8n | Optimization loop scheduling, alert routing, deployment hooks | Free (self-hosted) or $20/mo — https://n8n.io/pricing |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, brief generation | ~$10-30/mo — https://anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` — the core detect-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `autonomous-optimization` — always-on regression defense with experiment-aware filtering
- `seo-performance-monitor` — organic performance tracking with conversion attribution
