---
name: review-ask-to-early-users-durable
description: >
  Review Ask to Early Users — Durable. Always-on AI agents autonomously optimize review
  generation, detect metric anomalies, run experiments on ask copy and timing, and maintain
  review velocity at or above Scalable baseline.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Durable"
time: "200 hours over 6 months"
outcome: "Sustained or improving review velocity (≥ 3 reviews/week) and directory-sourced leads (≥ 8/month) over 6 months. Agents converge when 3 consecutive experiments yield <2% improvement."
kpis: ["Reviews per week (rolling 4-week avg)", "Directory-sourced leads per month", "Average rating across directories", "Experiment win rate", "Cost per review", "Category rank on G2"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - autonomous-optimization
---

# Review Ask to Early Users — Durable

> **Stage:** Marketing -> Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

The agent autonomously maintains and improves review generation without human intervention. It monitors review velocity and ratings daily, detects when metrics plateau or drop, generates hypotheses for improvement, runs A/B experiments, and auto-implements winners. The system finds the local maximum — the best achievable review velocity and directory-sourced lead rate given the current customer base and market. Convergence is declared when 3 consecutive experiments produce <2% improvement.

## Leading Indicators

- Daily anomaly detection firing correctly (no false positives for 2+ weeks)
- Experiment cadence: 1 active experiment at all times (unless converged)
- Experiment win rate: ≥ 40% of experiments produce a statistically significant improvement
- Review velocity holding within 10% of 4-week rolling average
- No directory with rating below 4.0 for more than 1 week without corrective action
- Review candidate pipeline depth: ≥ 4 weeks of eligible candidates at current ask rate

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to set up the continuous improvement cycle for this play. Configure with the following play-specific parameters:

**Primary KPIs to monitor:**
- `review_submitted` count per week (target: ≥ 3/week, from Scalable baseline)
- `directory_inquiry_submitted` count per month (target: ≥ 8/month)
- Average `review_rating` across all directories (floor: 4.0)

**Anomaly detection thresholds:**
- **Plateau:** review velocity within +/-2% for 3+ weeks
- **Drop:** review velocity declines >20% vs 4-week rolling average
- **Rating alert:** any directory average drops below 4.0
- **Spike:** review velocity jumps >50% (investigate — could be competitor gaming or a viral moment)

**Experiment variables the agent can test (low/medium risk, no human approval needed):**
- Review ask email subject line
- Review ask email body copy
- Ask timing (days after trigger event)
- Ask trigger type (which customer event initiates the sequence)
- Review directory routing (which directory to ask for based on customer attributes)
- Follow-up cadence (days between ask emails)
- Incentive amount ($10 vs $15 vs $25)
- Email sender name (founder vs CSM vs product team)

**Variables requiring human approval (high risk):**
- Adding or removing a directory from the program
- Changing the eligibility criteria for review candidates
- Modifying the quarterly ask frequency cap
- Changing incentive policy (adding or removing incentives entirely)
- Any change affecting >50% of the customer base

**Guardrails:**
- Maximum 1 active experiment at a time
- If average rating drops below 3.5 on any directory during an experiment, auto-revert immediately
- If review velocity drops >30% during an experiment, auto-revert immediately
- After a failed experiment (revert), wait 7 days before testing the same variable
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.
- Never send more than 1 review ask per customer per quarter regardless of experiment

### 2. Deploy play-specific review velocity monitoring

Run the `autonomous-optimization` drill to build the monitoring layer specific to this play:

**Review velocity dashboard:**
- Reviews per week by directory (trend)
- Ask-to-review funnel by ask channel (funnel visualization)
- Rating trends per directory (trend with 4.0 floor line)
- Review-to-lead attribution (correlation chart)
- Ask channel effectiveness (table sorted by conversion rate)

**Weekly review velocity report:**
- Generated automatically every Monday 8am via n8n
- Includes: velocity trend, rating trend, ask effectiveness, attribution data, optimization signals
- Posted to Slack and stored in Attio
- Feeds directly into `autonomous-optimization` Phase 2 (Diagnose) as context

**Anomaly alerts:**
- Zero reviews for 14+ days on any Tier 1 directory -> trigger optimization hypothesis
- Negative review (1-2 stars) -> immediate alert for human response within 24 hours
- Ask click-through rate drops below 5% -> signal ask fatigue, trigger copy refresh experiment
- Review candidate pipeline depth < 4 weeks -> alert team to examine customer growth

### 3. Deploy competitive tracking

Run the the directory performance monitor workflow (see instructions below) drill with competitive intelligence focus:

**Weekly competitive data collection:**
- Top 5 competitors' review counts on G2 and Capterra
- Competitor rating changes
- Competitor rank position changes
- Alert if a competitor gains 10+ reviews in a single week (possible review campaign — may need to respond)

**Competitive response playbook (agent-executed):**
- If competitor passes you in review count on G2 -> generate hypothesis to increase ask volume or expand eligible customer segments
- If competitor's rating drops -> opportunity. Increase review ask cadence temporarily to widen the gap.
- If competitor launches a new product -> monitor for their review campaign and pre-emptively increase your review velocity

### 4. Generate monthly optimization briefs

The `autonomous-optimization` drill generates weekly briefs. In addition, produce a monthly strategic brief:

```
# Review Program Monthly Brief -- {month}

## Performance Summary
- Total reviews collected: {count} (target: ≥ 12/month)
- Average rating: {avg} (floor: 4.0)
- Directory-sourced leads: {leads} (target: ≥ 8/month)
- Cost per review: ${cpr}
- Cost per directory-sourced lead: ${cpl}

## Experiments Run
| # | Hypothesis | Variable | Result | Impact |
|---|-----------|----------|--------|--------|
| 1 | {hypothesis} | {variable} | Won/Lost/Reverted | {+/-X%} |
| 2 | ... | ... | ... | ... |

## Competitive Position
- G2 rank: #{rank} (change: {+/-X})
- Capterra rank: #{rank} (change: {+/-X})
- Review gap vs top competitor: {gap} reviews

## Convergence Status
- Consecutive <2% experiments: {count}/3
- Status: {Optimizing | Approaching convergence | Converged}
- If converged: "Review program has reached local maximum. Current performance: {metrics}. Further gains require strategic changes (new customer segments, new directories, product improvements) rather than tactical optimization."

## Recommended Actions
- {data-driven next steps for the coming month}
```

### 5. Handle convergence

When the `autonomous-optimization` drill detects convergence (3 consecutive experiments with <2% improvement):

1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from continuous to monthly check-in
3. Continue the review velocity report (weekly) and competitive tracking (weekly)
4. Report to the team: "Review program optimized. Current velocity: {X} reviews/week. Current rating: {Y}. Directory-sourced leads: {Z}/month. The agent will continue monitoring for anomalies and competitive changes but will not run new experiments unless metrics degrade or market conditions shift."
5. Re-enter active optimization if any metric drops >15% below converged baseline for 2 consecutive weeks

## Time Estimate

- Autonomous optimization setup: 12 hours
- Review velocity monitor deployment: 8 hours
- Competitive tracking setup: 6 hours
- Monthly brief configuration: 4 hours
- Ongoing agent monitoring and experiment management (6 months): 120 hours
- Human review of experiments and briefs (~2 hours/week x 26 weeks): 52 hours
- **Total: ~200 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Review directory + analytics | Free basic; $299/mo Brand Starter (https://sell.g2.com/plans) |
| Capterra | Review directory + PPC | Free listing; PPC from $500/mo (https://www.capterra.com/vendors/) |
| Product Hunt | Review directory | Free; Pro $100/mo (https://www.producthunt.com/) |
| TrustRadius | Review directory | Free vendor profile (https://www.trustradius.com/vendors) |
| GetApp | Review directory | Free via Gartner Digital Markets |
| Loops | Automated review ask sequences | $49/mo (https://loops.so/pricing) |
| PostHog | Tracking, dashboards, experiments, anomaly detection | Free up to 1M events; ~$50/mo at scale (https://posthog.com/pricing) |
| n8n | Optimization loop, monitoring, alerting | Free self-hosted; $20/mo cloud (https://n8n.io/pricing) |
| Attio | CRM, review candidate pipeline, experiment log | $29/seat/mo (https://attio.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief writing | ~$20-50/mo at experiment cadence (https://www.anthropic.com/pricing) |
| Review incentives | Gift cards or account credits | ~$100-500/mo |

**Estimated play-specific cost at Durable: $500-1,500/mo** (Loops $49 + n8n $20 + PostHog ~$50 + Attio $29 + Anthropic ~$30 + incentives $100-500 + optional G2 Brand Starter $299 + optional Capterra PPC $500)

## Drills Referenced

- `autonomous-optimization` — continuous monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for review generation
- `autonomous-optimization` — play-specific monitoring of review velocity, ratings, ask effectiveness, and review-to-lead attribution
- the directory performance monitor workflow (see instructions below) — cross-directory KPI tracking and competitive intelligence
