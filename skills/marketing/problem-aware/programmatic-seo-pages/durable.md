---
name: programmatic-seo-pages-durable
description: >
  Programmatic SEO Pages — Durable Intelligence. Always-on AI agents autonomously optimizing content,
  rankings, and conversions. Detects anomalies, generates hypotheses, runs experiments, and auto-implements
  winners to find the local maximum of organic search performance.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to search algorithm changes"
kpis: ["Organic traffic trend", "Pages indexed", "Conversion rate", "Average position", "Click-through rate", "Content refresh velocity", "Ranking stability"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - autonomous-optimization
  - content-refresh-pipeline
  - seo-performance-monitor
---

# Programmatic SEO Pages — Durable Intelligence

> **Stage:** Marketing → ProblemAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

The programmatic SEO machine runs itself. AI agents monitor every metric, detect when rankings plateau or drop, generate hypotheses about what to change, run A/B experiments on content and CTAs, evaluate results, and auto-implement winners. The goal is to find and maintain the local maximum of organic search performance — the best possible traffic and conversion rate given the current market, competition, and search algorithm landscape.

This level is fundamentally different from Scalable. Scalable builds and publishes pages. Durable optimizes what is already published and adapts to change.

## Leading Indicators

- Autonomous optimization loop running: ≥2 experiments completed per month
- Ranking stability: <5% of pages experiencing position drops >5 spots in any month
- Content refresh cycle maintaining <10% of pages in "declining" status at any time
- Convergence detection: the system identifies when experiments produce <2% improvement and reduces experiment frequency
- Weekly optimization briefs generated automatically with clear cause-and-effect reasoning

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the programmatic SEO play:

**Monitor phase (daily via n8n):**
- Pull metrics from GSC and PostHog: organic traffic, average position, CTR, conversion rate, pages indexed
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger the diagnosis phase

**Diagnose phase (triggered by anomaly):**
- Gather context: which pages are affected, which keywords moved, what changed in the competitive landscape
- Use Ahrefs to check if competitors published new content for the same keywords
- Check GSC for crawl errors or indexation changes
- Run `hypothesis-generation` with the anomaly data + context
- Receive 3 ranked hypotheses with expected impact and risk level
- If risk = "high" (e.g., "delete and rebuild all pages in this category"), send alert for human review and STOP
- If risk = "low" or "medium", proceed to experiment

**Experiment phase (1 active experiment at a time):**
- Design the experiment based on the top hypothesis. Examples:
  - Hypothesis: "Meta titles without years get lower CTR" → Test: add "2026" to titles for 50 pages, keep 50 as control
  - Hypothesis: "Pages with <800 words rank worse than competitors" → Test: expand 30 pages to 1,200+ words, keep 30 as control
  - Hypothesis: "FAQ sections improve position" → Test: add FAQ schema to 50 pages, keep 50 as control
  - Hypothesis: "CTA placement below the fold reduces conversions" → Test: move CTA above fold for 50 pages
- Use PostHog feature flags for CTA experiments; use Webflow CMS updates for content experiments
- Run each experiment for minimum 14 days or until 200+ sessions per variant
- Maximum 1 active experiment per metric at a time. Never stack experiments.

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog and GSC
- Run `experiment-evaluation`: compare control vs variant on primary metric (position, CTR, or conversion rate) and guard metrics
- Decision:
  - **Adopt:** Variant wins by ≥5% with statistical significance. Roll out to all pages. Log the change.
  - **Iterate:** Results inconclusive but promising. Generate a refined hypothesis. Return to diagnose.
  - **Revert:** Variant loses or guard metrics worsen. Restore control. Log the failure. Cooldown 14 days before testing the same variable.
  - **Extend:** Not enough data. Keep running for another period.

**Report phase (weekly via n8n):**
- Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Estimate distance from local maximum (based on diminishing returns trend)
- Post weekly optimization brief to Slack and store in Attio

### 2. Run the advanced content refresh cycle

Run the `content-refresh-pipeline` drill at Durable intensity:

- Expand refresh triggers beyond rankings: detect search intent shifts (new "People Also Ask" patterns), seasonal relevance changes, competitor content updates
- Auto-refresh pages within 7 days of detecting a decline (vs. 14 days at Scalable)
- For pages that fail to recover after 2 refresh cycles, flag for strategic review: should the page target a different keyword? Should it be merged with another page? Should it be retired?
- Track refresh success rate over time. If refresh success rate drops below 50%, the refresh strategy itself needs optimization — feed this into the autonomous optimization loop.

### 3. Maintain and expand the SEO performance monitor

Run the `seo-performance-monitor` drill with enhanced Durable-level features:

- Add algorithm update detection: monitor a set of "canary" keywords (stable, high-volume terms) for sudden position changes that indicate a Google algorithm update
- When an algorithm update is detected, pause all experiments, take a snapshot of all rankings, and wait 14 days for the update to settle before resuming
- Add competitive monitoring: track 5-10 competitor domains' organic keyword counts and top pages. Alert when a competitor launches programmatic pages targeting the same keywords.
- Build a long-term trend dashboard: 6-month view of organic traffic, pages indexed, average position, and conversion rate

### 4. Detect convergence

The optimization loop runs indefinitely, but it should detect when the local maximum is reached:

- Track the magnitude of improvement from each successive experiment
- If 3 consecutive experiments produce <2% improvement on any metric, that metric has converged
- When all primary metrics have converged:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency from 2/month to 1/month (maintenance mode)
  3. Focus remaining experiments on conversion rate optimization rather than traffic growth
  4. Report: "Organic traffic has reached its local maximum at [X visits/month]. Further growth requires strategic changes: new keyword patterns, new content formats, or product changes."

### 5. Guardrails (CRITICAL)

- **Rate limit:** Maximum 1 active content experiment + 1 active CTA experiment at a time
- **Revert threshold:** If organic traffic drops >30% during any experiment, auto-revert immediately
- **Human approval required for:**
  - Deleting or unpublishing any page
  - Changes affecting >200 pages simultaneously
  - Keyword pattern changes (adding new patterns or retiring old ones)
  - Any hypothesis flagged as "high risk"
- **Cooldown:** After a failed experiment, wait 14 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause and flag for human strategic review.
- **Never experiment on what is not measured:** If a metric lacks tracking, fix tracking first (use `posthog-gtm-events`) before running experiments.

## Time Estimate

- Autonomous optimization setup: 20 hours
- Advanced content refresh configuration: 15 hours
- Enhanced monitoring and competitive tracking: 15 hours
- Ongoing experiment management (6 months): 50 hours
- Convergence analysis and reporting: 10 hours
- Strategic reviews and human checkpoints: 10 hours
- **Total: 120 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Webflow | CMS hosting and page updates | Business $39/mo ([pricing](https://webflow.com/pricing)) |
| Google Search Console | Indexation, rankings, CTR data | Free ([pricing](https://developers.google.com/webmaster-tools/pricing)) |
| PostHog | Tracking, experiments, feature flags, dashboards | Growth tier ~$50-150/mo at scale ([pricing](https://posthog.com/pricing)) |
| Ahrefs | Rank tracking, competitor monitoring, keyword data | Standard $199/mo or Advanced $399/mo ([pricing](https://ahrefs.com/pricing)) |
| Anthropic Claude | Content refresh generation, hypothesis generation, experiment evaluation | ~$30-100/mo ([pricing](https://www.anthropic.com/pricing)) |
| n8n | Automation for optimization loop, monitoring, refresh pipeline | Cloud $20/mo or self-hosted free ([pricing](https://n8n.io/pricing)) |
| Attio | Logging experiment decisions and optimization history | Free tier for notes and records ([pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at Durable:** $250-550/mo (Ahrefs + PostHog Growth are the main cost drivers).

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor → diagnose → experiment → evaluate → implement. Finds the local maximum of organic search performance.
- `content-refresh-pipeline` — advanced content refresh with 7-day SLA, competitive analysis, and strategic page retirement
- `seo-performance-monitor` — enhanced with algorithm update detection, competitive monitoring, and long-term trend dashboards
