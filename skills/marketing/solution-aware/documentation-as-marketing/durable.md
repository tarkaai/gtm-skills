---
name: documentation-as-marketing-durable
description: >
  Documentation as Marketing — Durable Intelligence. Always-on AI agents monitor
  docs traffic, rankings, and conversions, autonomously running experiments to
  find the local maximum of docs-driven lead generation.
stage: "Marketing > Solution Aware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Durable Intelligence"
time: "20 hours over 6 months (ongoing agent compute)"
outcome: "Sustained >=10% quarter-over-quarter organic docs traffic growth and >=2% docs-to-lead conversion rate, maintained via autonomous optimization that converges when successive experiments produce <2% improvement"
kpis: ["QoQ organic traffic growth rate", "Docs-to-lead conversion rate", "Experiment win rate", "Time to ranking recovery", "Keyword coverage vs competitors", "Cost per docs-sourced lead"]
slug: "documentation-as-marketing"
install: "npx gtm-skills add marketing/solution-aware/documentation-as-marketing"
drills:
  - autonomous-optimization
---

# Documentation as Marketing — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

The docs-as-marketing play runs autonomously with AI agents monitoring all metrics, detecting anomalies, generating improvement hypotheses, running A/B experiments, and auto-implementing winners. Organic docs traffic grows >= 10% quarter-over-quarter. Docs-to-lead conversion rate sustains >= 2%. The system converges when successive experiments produce < 2% improvement, indicating the local maximum has been reached.

## Leading Indicators

- Anomaly detection fires within 24 hours of a meaningful traffic or ranking change
- Hypothesis generation produces 3 actionable hypotheses per anomaly within 1 hour
- Experiment win rate >= 30% (at least 1 in 3 experiments produces a measurable improvement)
- Failed experiments auto-revert within the defined experiment window (no lingering damage)
- Weekly optimization brief accurately summarizes changes and their impact
- Content health score across all docs pages averages >= 70

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for docs-as-marketing. This creates the always-on agent loop:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check docs KPIs: total organic traffic, conversion rate, top-page rankings
- Compare last 2 weeks against 4-week rolling average
- Classify each metric as: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current docs content portfolio, recent changes (new pages published, pages refreshed, algorithm updates), conversion funnel state
- Pull 8-week metric history from PostHog
- Run hypothesis generation with Claude: receive 3 ranked hypotheses with expected impact and risk
- Store hypotheses in Attio as notes on the docs campaign record
- If top hypothesis risk = "high": send Slack alert for human review, STOP
- If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags
- For docs-specific experiments, the variable types include:
  - **CTA experiments:** test different CTA copy, placement, or type on high-traffic pages
  - **Content experiments:** test a rewritten introduction, different heading structure, or expanded code examples
  - **Meta experiments:** test different meta titles or descriptions to improve CTR from search results
  - **Internal link experiments:** test different cross-linking patterns to improve navigation depth
- Set experiment duration: minimum 7 days or 200+ page views per variant, whichever is longer
- Log experiment start in Attio with hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Run experiment evaluation with Claude
- Decision:
  - **Adopt:** Implement the winning variant permanently. Log the change.
  - **Iterate:** Generate a refined hypothesis. Return to Phase 2.
  - **Revert:** Restore control. Log the failure. Return to Phase 1 monitoring.
  - **Extend:** Insufficient data. Keep running for another period.
- Store full evaluation in Attio (decision, confidence, reasoning, metrics delta)

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on organic traffic and conversion rate
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

**Guardrails (critical):**
- Maximum 1 active experiment per page at a time
- If primary metric drops > 30% during an experiment, auto-revert immediately
- Human approval required for: any change affecting > 50% of docs pages, any CTA change on a page generating > 20 leads/month, any content change that removes or modifies code examples
- Cooldown: 7 days after a failed experiment before testing the same variable again
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.

### 2. Deploy the docs content health monitor

Run the `autonomous-optimization` drill to create always-on content health scoring:

**Dashboard:** Live PostHog dashboard showing:
- Total organic docs traffic with 90-day trend
- Top and bottom 20 pages by traffic
- Conversion funnel (docs_page_viewed -> docs_cta_clicked -> account_created)
- Content freshness distribution (pages by last-updated age)
- Search analytics: top zero-result queries, low-CTR searches

**Daily health checks (n8n cron):**
- Traffic anomaly detection (>15% drop vs 7-day rolling average)
- Indexation monitoring (sample 20 random pages daily)
- Ranking decay detection (weekly, flag pages losing >5 positions)

**Per-page health scoring (daily):**
```
health = (traffic_score * 0.3) + (ranking_score * 0.25) + (freshness_score * 0.2) + (conversion_score * 0.25)
```

Pages scoring < 25 for 2 consecutive weeks are automatically queued for the content refresh pipeline. Zero-result search queries with > 10 searches/month are automatically queued for the content scaling pipeline.

**Weekly health report (Monday via n8n):**
- Overall docs health score (average across all pages)
- Top 3 wins (pages that improved most)
- Top 3 risks (pages that declined most)
- Recommended actions for critical pages
- Sent to Slack and stored in Attio

### 3. Detect convergence

The optimization loop runs continuously. The agent monitors for convergence:

- If 3 consecutive experiments produce < 2% improvement on their target metric, the play has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment cadence from 4/month to 1/month (maintenance experiments)
  3. Report: "Docs-as-marketing is optimized. Current performance: [organic traffic]/month, [conversion rate]% docs-to-lead, [leads]/month from docs. Further gains require strategic changes: new product capabilities to document, new integration partners, new content formats (video tutorials, interactive playgrounds), or new distribution channels."

### 4. Respond to market changes

Even after convergence, the agent remains alert for external shifts that reopen optimization:

- **Algorithm updates:** If organic traffic drops > 15% across all docs pages simultaneously, treat as an algorithm update. Run a full SEO re-audit. Generate hypotheses specific to algorithm changes (content freshness, E-E-A-T signals, Core Web Vitals).
- **Competitor moves:** If a competitor launches a docs site or expands into your keyword territory, trigger a gap analysis and accelerate content production for contested keywords.
- **Product changes:** When new product features ship, automatically detect (via changelog webhook or GitHub release) and queue getting-started and API reference pages for the new capability.

## Time Estimate

- Autonomous optimization setup: 6 hours (n8n workflows, PostHog experiments config, Attio integration)
- Content health monitor setup: 4 hours (dashboard, daily checks, scoring, alerting)
- Ongoing human oversight: 10 hours over 6 months (reviewing high-risk hypotheses, approving major changes, monthly strategic review)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Rank tracking, competitor monitoring, gap analysis | Standard $249/mo — https://ahrefs.com/pricing |
| Mintlify | Docs platform (if used) | $250/mo (Pro) — https://mintlify.com/pricing |
| PostHog | Analytics, experiments, feature flags, anomaly detection | Free up to 1M events; experiments add-on usage-based — https://posthog.com/pricing |
| Google Search Console | Search analytics, indexation data | Free — https://search.google.com/search-console |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, content refresh | ~$20-50/mo (agent compute for daily/weekly loops) — https://anthropic.com/pricing |
| n8n | Orchestration for all automated loops | Free (self-hosted) or Pro EUR 60/mo — https://n8n.io/pricing |
| Attio | CRM for experiment logging, lead tracking, campaign records | Free up to 3 users — https://attio.com/pricing |

## Drills Referenced

- `autonomous-optimization` — the always-on monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `autonomous-optimization` — per-page health scoring, anomaly alerts, weekly health reports, and automatic refresh/gap triggers
