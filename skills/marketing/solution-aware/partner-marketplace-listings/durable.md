---
name: partner-marketplace-listings-durable
description: >
  Partner Marketplace Listings — Durable Intelligence. Always-on AI agents find
  the local maximum of each marketplace listing through the autonomous optimization
  loop: detect metric anomalies, generate improvement hypotheses, run experiments,
  evaluate results, and auto-implement winners.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "20 hours setup + 1 hour/week monitoring over 12 months"
outcome: "Marketplace-sourced MRR grows or holds >=90% of peak for 6 consecutive months with <4 hours/week human involvement"
kpis: ["Marketplace-attributed MRR trend (6-month)", "Experiment win rate", "Time from anomaly detection to resolution", "Review response time (p50 and p95)", "Portfolio average rating", "Autonomous optimization cycle count"]
slug: "partner-marketplace-listings"
install: "npx gtm-skills add marketing/solution-aware/partner-marketplace-listings"
drills:
  - autonomous-optimization
  - partner-marketplace-monitor
---

# Partner Marketplace Listings — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Always-on AI agents finding the local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies across all marketplace listings, generate improvement hypotheses, run A/B experiments on listing copy and landing pages, evaluate results, and auto-implement winners. The `partner-marketplace-monitor` drill provides the continuous data feed. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.

The goal is not to grow forever -- it is to find the best possible performance for each marketplace listing given the current market conditions and maintain it as conditions change (new competitors, marketplace algorithm updates, seasonal demand shifts).

**Pass threshold:** Marketplace-sourced MRR grows or holds >=90% of peak for 6 consecutive months with <4 hours/week human involvement.

## Leading Indicators

- Autonomous optimization loop running on schedule (daily monitoring, weekly experiments)
- First A/B experiment launched within 2 weeks of Durable setup
- Anomaly detection catching issues before they become visible in monthly reports
- Review response time under 24 hours for negative reviews, under 48 hours for positive
- Competitive intelligence surfacing marketplace changes within 1 week of occurrence
- Optimization briefs delivered weekly with specific data and actionable recommendations
- Experiment velocity: at least 2 experiments per month across the portfolio

## Instructions

### 1. Deploy the partner marketplace monitoring system

Run the `partner-marketplace-monitor` drill to build the continuous data collection and reporting infrastructure:

1. Configure comprehensive PostHog tracking events for the full marketplace-to-revenue funnel across all listings
2. Build the weekly n8n data collection workflow pulling analytics from every marketplace API
3. Set up the PostHog dashboard with 5 panels: portfolio overview, per-marketplace performance, full conversion funnel, review health, competitive landscape
4. Configure anomaly detection thresholds: install drops >30% WoW, conversion drops >25%, rating below 4.0, rank drops by 3+ positions, uninstall spikes >20% of active base
5. Route anomaly alerts to Slack with context and recommended investigation steps
6. Generate weekly performance reports with competitive intelligence

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill, configured specifically for partner marketplace listings:

**Phase 1 -- Monitor (daily via n8n):**
The monitoring system from step 1 feeds directly into the optimization loop. The agent checks all marketplace KPIs daily:
- Install volume per marketplace (7-day rolling average vs 4-week rolling average)
- Install-to-signup conversion rate per marketplace
- Signup-to-paid conversion rate per marketplace
- Average rating and review velocity
- Category ranking position

Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). Anomalies trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
When an anomaly is detected, the agent gathers context and generates hypotheses:

1. Pull the specific marketplace listing's current configuration from Attio (title, description, keywords, screenshots, pricing, landing page)
2. Pull 8-week metric history from PostHog
3. Check competitive intelligence: did a new competitor launch? Did a top competitor update their listing?
4. Generate 3 ranked hypotheses with expected impact and risk level

**Example hypotheses for common marketplace anomalies:**

| Anomaly | Likely hypothesis | Experiment |
|---------|------------------|------------|
| Install drop, no competitive change | Listing description no longer matches trending search terms | Update listing keywords and title |
| High installs, low signup conversion | Landing page doesn't match marketplace user expectations | A/B test marketplace-specific landing page vs current |
| Rating decline | Recent product change or integration bug frustrating users | Investigate recent reviews for patterns; fix integration issue |
| Rank drop despite stable installs | Competitor gained reviews/installs faster | Accelerate review generation for that marketplace |
| Conversion drop across all marketplaces | Product-level issue, not marketplace-specific | Escalate to product team; pause marketplace experiments |

If top hypothesis risk = "high" (e.g., requires pricing change or major integration update): send Slack alert for human review. Stop.
If risk = "low" or "medium": proceed to Phase 3.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
Design and run the experiment:

1. For listing copy changes: create A/B variant of the listing description. Some marketplaces don't support native A/B testing -- in that case, run a time-based test (2 weeks current -> 2 weeks variant -> compare)
2. For landing page changes: use PostHog feature flags to split marketplace-sourced traffic between control and variant landing pages
3. For review strategy changes: adjust the review request cadence or targeting and measure review velocity delta
4. Set experiment duration: minimum 14 days or until 50+ installs per variant, whichever is longer
5. Log experiment in Attio: hypothesis, start date, duration, success criteria, marketplace

**Phase 4 -- Evaluate (triggered by experiment completion):**
Pull experiment results and decide:

- **Adopt (variant wins by >=10% with >=90% confidence):** Implement the winning variant as the new default. Update Attio. Move to Phase 5.
- **Iterate (inconclusive or variant wins by <10%):** Generate a refined hypothesis building on this result. Return to Phase 2.
- **Revert (control wins):** Restore the original configuration. Log the failure. Apply 7-day cooldown on that variable. Return to Phase 1.

**Phase 5 -- Report (weekly via n8n):**
Generate the weekly optimization brief:

```
# Partner Marketplace Optimization Brief -- Week of {date}

## Optimization Activity
- Anomalies detected: {count} ({list with marketplace and metric})
- Hypotheses generated: {count}
- Experiments running: {count} ({details})
- Experiments completed: {count} ({results})
- Changes implemented: {count} ({what changed and expected impact})

## Net Impact
- Install volume: {change}% vs last week
- Signup conversion: {change}% vs last week
- Marketplace-attributed MRR: ${mrr} ({change}% vs last month)

## Convergence Status
{For each marketplace: current performance vs estimated local maximum}
- {marketplace_1}: performing at {X}% of estimated ceiling. {Status: optimizing / converging / converged}
- {marketplace_2}: ...

## Next Week
- Experiments to launch: {list}
- Human review needed: {list or "none"}
```

Post to Slack. Store in Attio.

### 3. Implement convergence detection

The optimization loop should detect when a marketplace listing has reached its local maximum:

**Convergence criteria:** 3 consecutive experiments on the same marketplace produce <2% improvement each.

**When converged:**
1. Reduce monitoring frequency for that marketplace from daily to weekly
2. Shift experiment budget to non-converged marketplaces
3. Continue competitive monitoring (a new competitor or marketplace algorithm change can break convergence)
4. Report: "Marketplace {X} is optimized. Current performance: {metrics}. Further gains require strategic changes (new integration features, new marketplace categories, or product-level improvements) rather than tactical optimization."

### 4. Maintain the review ecosystem

Continue automated review management at scale:

- Review response within 24 hours for negative reviews (critical for rating maintenance)
- Review response within 48 hours for positive reviews
- Continue the review generation cadence from Scalable, adjusted based on per-marketplace review completion rates
- Monitor for review patterns that indicate product issues (clustering of similar complaints)
- When the agent detects 2+ negative reviews mentioning the same issue within 30 days: escalate to product team as a potential integration bug

### 5. Adapt to marketplace ecosystem changes

The monitoring system should detect and adapt to:

- **Marketplace algorithm changes:** Sudden rank shift across all listings without corresponding metric changes. Response: re-research marketplace ranking factors, update listing strategy.
- **New marketplace features:** Partner marketplaces regularly add new listing features (badges, certifications, featured sections). Response: adopt new features early for ranking advantage.
- **Seasonal patterns:** Some marketplaces see demand cycles (e.g., Shopify around holiday seasons, Salesforce around Dreamforce). Response: increase review generation and listing optimization before peak periods.

## Time Estimate

- 10 hours: Partner marketplace monitor setup (data collection, dashboard, anomaly detection)
- 8 hours: Autonomous optimization loop configuration (n8n workflows, hypothesis templates, experiment framework)
- 2 hours: Convergence detection and reporting setup
- Ongoing: ~1 hour/week for reviewing optimization briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Dashboards, anomaly detection, experiments, feature flags | Free up to 1M events/mo; paid from $0 usage-based ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Audit trail for all optimization activity | Plus $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Scheduling the monitoring and optimization loops | Pro $50/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Review request sequences | Growth $99/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Clay | Competitive intelligence scraping | Launch $185/mo or periodic usage ([clay.com/pricing](https://clay.com/pricing)) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Usage-based; ~$5-20/mo for this play's volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Partner marketplaces | 5+ platform listings | $0-19 total |

**Estimated monthly cost at this level:** ~$200-400/mo (same tools as Scalable + Anthropic API for hypothesis generation). Cost should decrease over time as marketplaces converge and optimization frequency drops.

## Drills Referenced

- `autonomous-optimization` -- the core detect-diagnose-experiment-evaluate-implement loop that finds the local maximum for each marketplace listing
- `partner-marketplace-monitor` -- continuous data collection, dashboard, anomaly detection, competitive intelligence, and weekly reporting across the full marketplace portfolio
