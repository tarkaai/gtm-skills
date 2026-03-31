---
name: comparison-alternative-pages-durable
description: >
  Comparison and Alternative Pages — Durable Intelligence. Always-on AI agents autonomously
  optimize comparison pages: detect ranking and conversion anomalies, generate improvement
  hypotheses, run A/B experiments on page elements, auto-implement winners, and maintain
  competitive intelligence freshness.
stage: "Marketing > SolutionAware"
motion: "LeadCaptureSurface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "95 hours over 6 months"
outcome: "Sustained or improving organic traffic and conversion rate over 6 months; successive optimization experiments produce <2% improvement (local maximum reached)"
kpis: ["Organic traffic trend (MoM)", "Conversion rate trend", "Competitor keyword coverage (%)", "Feature comparison accuracy score", "Optimization experiment win rate"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
drills:
  - autonomous-optimization
  - competitive-intelligence-pipeline
---

# Comparison and Alternative Pages — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

The comparison page portfolio operates autonomously. AI agents monitor performance, detect anomalies, generate improvement hypotheses, run A/B experiments on page elements (headlines, feature table layouts, CTA copy, content depth), auto-implement winners, and keep competitive data current. The system converges on the local maximum — the best possible organic traffic and conversion rate given your competitive position — and maintains it as competitors and search algorithms change.

Pass threshold: sustained or improving organic traffic and conversion rate over 6 months. Convergence: when successive optimization experiments produce <2% improvement for 3 consecutive experiments, the portfolio has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop running: at least 2 experiments per month across comparison pages
- Experiment win rate >30% (at least 1 in 3 experiments produce measurable improvement)
- Competitive intelligence pipeline detecting and auto-updating competitor changes within 7 days
- Zero comparison pages with stale competitor data (>90 days old)
- Weekly optimization briefs generated automatically with actionable recommendations

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for comparison pages:

**Monitor phase (daily via n8n cron):**
- Pull comparison page KPIs from PostHog: organic traffic per page, conversion rate per page, feature table engagement rate, CTA click rate
- Compare last 2 weeks against 4-week rolling average
- Classify each page: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected on any page, trigger the diagnose phase

**Diagnose phase (triggered by anomaly):**
- Pull 8-week metric history for the anomalous page from PostHog
- Pull current ranking position and position history from GSC data
- Check if the competitor's data has changed recently (from `competitive-intelligence-pipeline`)
- Run hypothesis generation with Claude: given the anomaly data, page content, and competitive context, generate 3 ranked hypotheses for what to change
- Example hypotheses:
  - "H1 headline does not match the dominant search query — rewrite to match GSC's top impression query"
  - "Feature table places our weakest feature first — reorder to lead with strongest differentiators"
  - "CTA placement is below the fold on mobile — add a sticky CTA bar"
  - "Competitor launched a new feature we haven't addressed — update feature table"
- Store hypotheses in Attio. If top hypothesis is high-risk (changes >30% of page), require human approval.

**Experiment phase (triggered by hypothesis acceptance):**
- Use PostHog feature flags to split traffic on the target comparison page: 50% control (current), 50% variant (hypothesis change)
- Implement the variant: update page content, reorder table, change CTA copy, or modify layout via Webflow CMS API
- Run the experiment for minimum 14 days or until 200+ sessions per variant
- Track: conversion rate, engagement rate, time on page, bounce rate per variant

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog
- Evaluate with Claude: control vs variant data, statistical significance, confidence level
- Decision: **Adopt** (implement variant permanently), **Iterate** (refine hypothesis and re-test), **Revert** (restore control), **Extend** (run longer for more data)
- Log decision and reasoning in Attio

**Report phase (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from adopted changes this week
- Generate weekly optimization brief with Claude: what changed, net impact, current distance from estimated local maximum
- Post to Slack and store in Attio

### 2. Deploy comparison page health monitoring

Run the `autonomous-optimization` drill:

- Build the dedicated comparison page PostHog dashboard: traffic, conversion, engagement, rankings, content freshness
- Configure daily GSC sync tracking ranking positions for all target competitor keywords
- Configure weekly Ahrefs sync tracking total keyword footprint
- Set anomaly alerts: traffic drops, ranking crashes, conversion drops, stale content, new keyword opportunities
- Generate weekly health reports with top/bottom performing pages and recommended actions

The health monitor feeds signals to the autonomous optimization loop. When the health monitor flags a declining page, the optimization loop picks it up in the next daily monitoring cycle.

### 3. Maintain competitive intelligence freshness

Continue running the `competitive-intelligence-pipeline` drill from Scalable, with tighter parameters at Durable:

- Increase competitor scraping frequency from weekly to twice-weekly for top 10 competitors
- Auto-update comparison pages within 48 hours of detecting a competitor change (still with pricing-change human review guardrail)
- Expand new competitor discovery to run bi-weekly instead of monthly
- When a new competitor is discovered: auto-generate a comparison page draft, queue for human review, publish within 1 week
- Track competitive intelligence accuracy: every quarter, manually spot-check 5 comparison pages for data accuracy. If accuracy drops below 90%, adjust scraping targets or add manual verification steps.

### 4. Detect convergence

The autonomous optimization loop runs indefinitely. Monitor for convergence:

- Track the magnitude of improvement from each adopted experiment
- If 3 consecutive experiments produce <2% improvement on their target metric:
  1. The comparison page portfolio has reached its local maximum
  2. Reduce experiment frequency from 2/month to 1/month
  3. Shift optimization focus to maintaining freshness and defending rankings rather than improving them
  4. Generate a convergence report: "This play is optimized. Current portfolio performance: {traffic}/month, {conversion_rate}% conversion, {keywords_ranked} keywords in top 10. Further gains require strategic changes: entering a new content category, targeting a new competitor segment, or launching a different content format (video comparisons, interactive comparison tools)."

### 5. Evaluate sustainability

This level runs continuously. Monthly review:

- Is organic traffic sustained or improving month over month?
- Is conversion rate holding above the Scalable threshold (≥1.0%)?
- Are competitive intelligence updates keeping content accurate?
- Is the optimization loop finding improvements, or has it converged?
- Are new competitors being detected and covered within 2 weeks of emergence?

If metrics decay despite optimization, the root cause is likely external: algorithm change, new strong competitor, or market shift. Diagnose and recommend strategic response (not tactical page optimization).

## Time Estimate

- 20 hours: autonomous optimization loop setup (n8n workflows, PostHog experiments config, Claude prompts, Attio logging)
- 15 hours: comparison page health monitor dashboard and alert configuration
- 10 hours: competitive intelligence pipeline tuning (frequency increase, accuracy checks)
- 50 hours: ongoing over 6 months — experiment review (2 hrs/month), weekly brief review (1 hr/week), quarterly accuracy audit (3 hrs/quarter), strategic review (2 hrs/quarter)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, dashboards, anomaly detection, feature flags | Free up to 1M events/mo; paid for experiments — https://posthog.com/pricing |
| Firecrawl | Competitor page scraping (twice-weekly at Durable) | Standard $99/mo — https://firecrawl.dev/pricing |
| Ahrefs | Rank tracking, keyword monitoring, competitor discovery | Lite $99/mo — https://ahrefs.com/pricing |
| Anthropic (Claude) | Hypothesis generation, experiment evaluation, content updates, weekly briefs | ~$30-80/mo — https://anthropic.com/pricing |
| Webflow | CMS updates for experiment variants and content refreshes | CMS plan ~$23/mo — https://webflow.com/pricing |
| Google Search Console | Daily ranking data, indexation monitoring | Free — https://search.google.com/search-console |
| n8n | Orchestration of all automated workflows | Self-hosted free or Cloud $20/mo — https://n8n.io/pricing |

**Durable budget: Firecrawl ~$99/mo + Webflow ~$23/mo + Claude API ~$30-80/mo** (Ahrefs, PostHog, n8n assumed standard stack)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor metrics daily, diagnose anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — dedicated monitoring layer for comparison pages tracking rankings, traffic, conversions, and content freshness with anomaly alerts
- `competitive-intelligence-pipeline` — twice-weekly competitor monitoring with auto-update of comparison pages when competitor data changes
