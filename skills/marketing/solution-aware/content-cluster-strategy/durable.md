---
name: content-cluster-strategy-durable
description: >
  Content Cluster Strategy — Durable Intelligence. Always-on AI agents monitor cluster
  performance, detect ranking anomalies, run A/B experiments on content and CTAs,
  auto-implement winners, and generate weekly optimization briefs to find the local
  maximum of organic traffic and conversion.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "110 hours over 6 months"
outcome: "Sustained or improving organic traffic and topical authority over 6 months via continuous AI-driven cluster optimization and market-responsive content expansion"
kpis: ["Organic traffic trend", "Keyword ranking distribution", "Topical authority score", "Internal link CTR", "Conversion rate", "Cluster refresh velocity"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
drills:
  - autonomous-optimization
  - cluster-gap-analysis
  - content-refresh-pipeline
---

# Content Cluster Strategy — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

Organic traffic and conversion rate are sustained or improving over 6 months without proportional human effort. The autonomous optimization loop detects metric anomalies, generates hypotheses (e.g., "title tag change on article X will improve CTR by 15%"), runs A/B experiments, auto-implements winners, and generates weekly briefs. The system converges when successive experiments produce < 2% improvement, indicating the cluster has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop running: daily anomaly detection, weekly experiments
- At least 2 successful experiments implemented per month (measurable improvement on targeted metric)
- Cluster health scores across all clusters maintained >= 80
- Content refresh velocity: underperforming articles refreshed within 7 days of detection
- No sustained traffic decline (> 2 weeks) without an active experiment or diagnosis
- Weekly optimization brief delivered on schedule

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the always-on optimization engine for your content clusters. This is the core loop that makes Durable fundamentally different from Scalable.

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks the cluster's primary KPIs against rolling baselines:
- Total organic traffic (compare last 2 weeks vs 4-week rolling average)
- Per-article ranking positions (detect drops > 5 positions)
- Conversion rate (detect drops > 15% from baseline)
- Indexation rate (detect any pages falling out of the index)

Classify each check: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (> 20% decline), **spike** (> 50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context (cluster map, article metadata, recent ranking data, competitor SERP analysis) and runs `hypothesis-generation` via the Anthropic API to produce 3 ranked hypotheses. Examples:

- "Article X dropped because competitor Y published a more comprehensive guide last week. Refresh with additional depth and updated data."
- "Cluster-wide CTR declined because Google changed SERP layout for these queries. Rewrite meta titles to match new featured snippet format."
- "Conversion rate dropped on pillar page because CTA is below the fold. Test moving CTA to after the first H2."

If top hypothesis is high-risk (budget change > 20%, targeting shift > 50%), send Slack alert for human approval. Otherwise proceed.

**Phase 3 — Experiment:**
The agent designs and runs the experiment using PostHog feature flags:
- For content changes: publish a variant version of the article and split organic traffic using PostHog's URL redirect experiment or create two meta title variants
- For CTA changes: A/B test CTA placement, copy, or design via PostHog feature flags
- For refresh experiments: refresh the article and measure position + CTR change over 14-28 days

Guardrails:
- Maximum 1 active experiment per cluster at a time
- If primary metric drops > 30% during experiment, auto-revert
- Minimum experiment duration: 7 days or 100+ samples per variant
- Maximum 4 experiments per month per cluster

**Phase 4 — Evaluate:**
After experiment duration completes, the agent runs `experiment-evaluation`:
- **Adopt**: variant outperformed control with statistical significance. Auto-implement the winner. Log the change with reasoning and impact data.
- **Iterate**: results inconclusive. Generate a refined hypothesis and return to Phase 2.
- **Revert**: variant underperformed. Restore control. Log the failure. Return to Phase 1.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week and their diagnoses
- Experiments running, completed, or reverted
- Net metric change from all adopted changes
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Run continuous cluster gap analysis

Run the `cluster-gap-analysis` drill on an automated monthly schedule (via n8n):

- Detect new keyword opportunities as the market evolves (new competitors, new search trends, seasonal topics)
- Identify articles losing ground to competitors
- Audit cross-cluster linking as the site grows
- Feed new subtopics directly into the automated content production pipeline from Scalable level

The gap analysis now runs without human intervention. New subtopics discovered are queued for production. Declining articles are queued for refresh. The agent handles the entire discovery-to-production cycle.

### 3. Maintain automated content refresh

The `content-refresh-pipeline` from Scalable level continues running weekly, now enhanced by the autonomous optimization loop:

- Refresh priorities are informed by anomaly detection (articles flagged by Phase 1 get priority)
- Refresh content is generated using insights from experiment results (if an experiment proved that adding FAQ schema improves CTR, apply that pattern to all refreshes)
- Refresh outcomes feed back into the hypothesis generator (build a knowledge base of what refresh strategies work for this site)

### 4. Detect convergence

The autonomous optimization loop monitors its own effectiveness:

- Track experiment win rate over time (% of experiments that result in Adopt decisions)
- Track magnitude of improvements per winning experiment
- When 3 consecutive experiments produce < 2% improvement, declare convergence

At convergence:
- The cluster has reached its local maximum for the current content, audience, and competitive landscape
- Reduce monitoring frequency from daily to weekly
- Reduce experiment frequency from 4/month to 1/month (maintenance mode)
- Generate a convergence report: current performance metrics, optimization history, what was tried and what worked

**Human action required at convergence:** Review the convergence report. Decide whether to:
- Accept the local maximum and maintain
- Invest in strategic changes (new clusters, different audience segments, product changes) to pursue a higher maximum
- Reallocate resources to other plays that have not yet converged

### 5. Evaluate sustainability

This level runs continuously. Monthly, verify:
- Organic traffic trend: flat or improving (no sustained declines > 2 weeks)
- Conversion rate: holding at or above 1.0%
- Topical authority score (Ahrefs Domain Rating for cluster-relevant keywords): stable or improving
- Cluster refresh velocity: underperforming articles refreshed within 7 days of detection

If any metric degrades for 4+ consecutive weeks without an active experiment addressing it, the agent escalates to human review.

## Time Estimate

- Autonomous optimization setup: 12 hours (n8n workflows, PostHog experiments, hypothesis templates)
- Monthly gap analysis oversight: 2 hours/month x 6 = 12 hours
- Weekly brief review: 30 min/week x 26 = 13 hours
- Experiment review and approval (high-risk only): ~2 hours/month x 6 = 12 hours
- Convergence analysis and strategic review: 8 hours
- Ongoing monitoring and escalation handling: ~10 hours/month, tapering as system stabilizes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Rank tracking, gap analysis, competitor monitoring | $199-399/mo (Standard/Advanced) — https://ahrefs.com/pricing |
| Ghost | CMS for content publishing and refresh | Free (self-hosted) or $25/mo — https://ghost.org/pricing |
| PostHog | Analytics, experiments, feature flags, dashboards | Free up to 1M events/mo, experiments on Scale plan $450/mo — https://posthog.com/pricing |
| Google Search Console | Search analytics, indexation monitoring | Free |
| Anthropic Claude API | Hypothesis generation, content refresh, experiment evaluation | ~$10-30/mo at durable scale — https://anthropic.com/pricing |
| n8n | Optimization loop automation, scheduling, alerts | Free (self-hosted) or $20/mo — https://n8n.io/pricing |
| Attio | Experiment audit trail, optimization brief storage | $29/seat/mo (Plus) — https://attio.com/pricing |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor > diagnose > experiment > evaluate > implement > report. Finds the local maximum through continuous, guardrailed experimentation.
- `cluster-gap-analysis` — monthly automated audit of keyword coverage, internal links, and content freshness across all clusters
- `content-refresh-pipeline` — weekly automated detection and refresh of underperforming cluster articles, now guided by experiment insights
