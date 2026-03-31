---
name: quora-ads-targeting-durable
description: >
  Quora Ads — Durable Intelligence. Always-on AI agents continuously optimize Quora targeting,
  creative, budget allocation, and audience expansion. The autonomous optimization loop detects
  metric anomalies, generates improvement hypotheses, runs A/B experiments, and auto-implements
  winners. Weekly optimization briefs track convergence toward the local maximum.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Communities"
level: "Durable Intelligence"
time: "150 hours over 12 months"
outcome: "Sustained >=50 qualified leads/month and cost per qualified lead <=140 over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained monthly qualified leads", "Cost per qualified lead trend", "Autonomous experiment win rate", "Creative pipeline velocity", "Question/topic inventory growth", "Audience saturation index", "Optimization convergence rate"]
slug: "quora-ads-targeting"
install: "npx gtm-skills add Marketing/ProblemAware/quora-ads-targeting"
drills:
  - autonomous-optimization
---

# Quora Ads — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Communities

## Outcomes

Always-on AI agents finding the local maximum. The Quora Ads program runs itself: question and topic discovery, creative generation and rotation, targeting optimization, budget allocation, audience management, and performance reporting all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in Quora KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement — at that point, Quora Ads performance is near-optimal for the current market, audience, and competitive landscape.

**Pass threshold:** Sustained >=50 qualified leads/month and cost per qualified lead <=140 over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Creative pipeline operates autonomously: variants generated, uploaded, tested, rotated, retired
- Cost per qualified lead is stable or improving month over month
- Convergence signal: last 3 experiments produced <2% improvement each
- Question/topic inventory expands monthly without manual research (agent discovers new opportunities)
- Audience saturation index stays below threshold without manual intervention (audience rotation handles it)

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the Quora Ads program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check Quora program KPIs:
  - Cost per qualified lead (primary KPI)
  - CTR by targeting type (topic, question, keyword, retargeting, lookalike)
  - CPC by ad set
  - Creative velocity (new variants produced and launched per week)
  - Lead quality (% scoring 70+ on ICP scoring via Clay)
  - Audience frequency by targeting type (saturation risk)
  - Question targeting inventory freshness (% of questions added in last 30 days)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current targeting configuration, budget allocation, active ad variants, audience sizes, experiment history
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "CPC increased 25% across topic targeting ad sets. Hypothesis: core ICP topics are saturated — frequency has exceeded 4/week for 2 consecutive weeks. Test expanding to 10 new Tier 2 topics while maintaining bid level."
  - "CTR dropped from 1.2% to 0.7% on question targeting. Hypothesis: the top 20 questions have been targeted for 8 weeks and engagement has decayed. Test replacing 50% of questions with newly discovered high-traffic questions from adjacent topics."
  - "Conversion rate dropped from 5% to 2.8% on the landing page. Hypothesis: the offer (checklist) has been running for 12 weeks and is stale. Test a new offer (template or tool) with a fresh landing page."
  - "Cost per qualified lead increased 30%. Hypothesis: lead quality has declined because lookalike audience has drifted from ICP. Test rebuilding the lookalike from last 60 days of qualified leads only (excluding older, less representative data)."
  - "Text Ads suddenly outperforming Image Ads by 40% on CTR. Hypothesis: Quora may have changed ad placement or rendering. Test increasing Text Ad allocation from 50% to 80% of variants."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate mechanism:
  - If testing targeting changes: create a duplicate ad set with modified topics/questions/keywords
  - If testing creative: generate new ad variants using the creative playbook and launch alongside control ads
  - If testing budget allocation: split budget between current and proposed allocation
  - If testing offer/landing page: create a new landing page variant and split traffic via UTM routing
  - If testing bidding strategy: duplicate ad set with different bid type or amount
  - If testing audience changes: create modified audience (rebuild lookalike, adjust retargeting window, refresh list match)
- Set experiment duration: minimum 7 days or 200+ clicks per variant, whichever is longer
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update live campaign configuration, log the change, move to Phase 5
- If Iterate: generate new hypothesis building on this result, return to Phase 2
- If Revert: restore control configuration, log failure, return to Phase 1
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on cost per qualified lead and lead volume
  - Current distance from estimated local maximum
  - Creative pipeline health: variants in queue, average ad age, fatigue index
  - Question/topic inventory health: total questions targeted, % added in last 30 days, saturation levels
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy Quora Ads Performance Reporting

Run the `autonomous-optimization` drill at full Durable scope:

1. Build the PostHog dashboard (8 panels: spend/reach trends, click performance by targeting type, conversion funnel, CPA trend with optimization events annotated, creative performance decay curves, targeting type comparison, lead quality trend, full-funnel attribution)
2. Build Attio saved views (Quora-sourced contacts, Quora pipeline, Quora ROI by targeting type, experiment history log)
3. Deploy the weekly automated report (n8n workflow every Monday)
4. Deploy the monthly full-funnel attribution report (first Monday of each month)
5. Configure 5 real-time anomaly alerts (CPC spike, conversion rate drop, zero conversions, budget runaway, creative fatigue)
6. Maintain the question/topic performance tracking log with automatic recommendations for pruning and expansion

The reporting layer provides the data substrate that the autonomous optimization loop reads. Without accurate, timely reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the Quora program:

- **Rate limit:** Maximum 1 active experiment at a time on the Quora program
- **Revert threshold:** If cost per qualified lead exceeds 2x the 4-week average during any experiment, auto-revert immediately
- **Human approval required for:**
  - Budget changes exceeding 20% of current monthly spend
  - Targeting changes that affect more than 50% of impressions (e.g., removing a major topic cluster)
  - Changes to the landing page offer or value proposition
  - Any change the hypothesis generator flags as "high risk"
  - Adding or removing entire targeting types (e.g., dropping question targeting entirely)
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All Quora events must have PostHog tracking before experiments can target them. If a KPI lacks tracking, fix tracking first using the `posthog-gtm-events` drill

### 4. Autonomous Question and Topic Discovery

At Durable level, the agent should continuously discover new targeting opportunities:

1. **Weekly question mining** (n8n cron, every Wednesday):
   - For each high-performing topic, search Quora for new questions posted in the last 30 days
   - Score new questions by monthly views and relevance to ICP
   - Add questions with 500+ monthly views to the targeting recommendation queue
   - Flag new question clusters (3+ related new questions) as potential new ad sets

2. **Monthly topic expansion:**
   - Analyze which Tier 2 and Tier 3 topics produced qualified leads in the last 30 days
   - Search for related topics not yet in the targeting set
   - Recommend 5-10 new topics to test in the 10% exploration budget

3. **Competitive question monitoring:**
   - Track questions where competitors are mentioned (e.g., "alternatives to [competitor]")
   - Add these questions to a dedicated comparison-targeting ad set with comparison-hook creative
   - Monitor competitor mentions in Quora answers for emerging competitive threats

### 5. Autonomous Creative Pipeline

At Durable level, the creative pipeline should operate with minimal human touch:

1. **Agent generates ad variants** weekly using the evolving creative playbook (templates updated based on experiment results)
2. **Agent generates image assets** using design tools or AI image generation
3. **Marketer reviews** (15 min/week) and approves/rejects
4. **Approved variants enter the rotation queue**
5. **n8n workflow monitors** per-ad performance daily
6. **Fatigued ads auto-flagged** for replacement (CTR declining 5+ consecutive days)
7. **Top performers kept** until fatigue signals appear
8. **The optimization loop** continuously tests which templates, hooks, pain points, and formats produce the best results

Over time, the creative playbook evolves based on experimental data. The templates that produce the best-performing ads get weighted more heavily in the generation pipeline.

### 6. Monitor Convergence

The optimization loop should detect when the Quora Ads program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "Quora Ads program optimized. Current cost per qualified lead: $[X]. Monthly qualified leads: [Y]. Further gains require strategic changes (new platform, new audience market, product positioning changes, or channel diversification) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 7. Handle Platform and Market Shifts

Quora's ad platform, algorithm, and targeting capabilities evolve over time. The optimizer should detect shifts:

- If CPM increases across all targeting types by >20%: Quora may have changed auction dynamics. Test bidding strategy changes or shift budget to the most efficient targeting types.
- If CTR drops across all ad sets simultaneously: Quora may have changed ad placement or rendering. Test new ad formats or creative approaches.
- If conversion rate drops despite stable CTR: external factor (competitor entry, market saturation, seasonal shift). Alert for strategic review.
- If Quora adds new targeting options or ad formats: alert the team to evaluate and potentially add new ad sets leveraging the new capability.
- If Quora deprecates question targeting or changes topic taxonomy: alert immediately and redesign the targeting strategy.

In these cases: the optimizer flags the situation and recommends whether tactical optimization can address it or whether strategic human intervention is needed.

## Time Estimate

- 20 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails, hypothesis templates)
- 10 hours: Performance reporting dashboard, alerts, and monthly attribution reports
- 5 hours: Question/topic discovery automation
- 5 hours: Creative pipeline automation refinement
- 75 hours: Ongoing optimization over 12 months (~1.5 hours/week for monitoring, experiment design, evaluation, and creative review)
- 15 hours: Monthly strategic reviews (12 reviews at ~1.25 hours each)
- 10 hours: Convergence analysis and maintenance mode transition
- 10 hours: Platform shift response and strategic adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Quora Ads | Campaign management (agent-optimized) | Ad spend ($5,000-15,000/mo, agent-optimized across targeting types) |
| PostHog | Analytics — dashboards, experiments, anomaly detection, funnels | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead tracking, experiment logging, pipeline attribution | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring at scale | $349/mo (Explorer) or $699/mo (Pro) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences with A/B testing | $99/mo (Growth) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — optimization loop, creative pipeline, reporting, alerts | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — creative generation, hypothesis generation, experiment evaluation | Usage-based, ~$50-100/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** $5,000-15,000/mo ad spend + ~$650-1,100/mo tools + ~$50-100/mo AI API. Total: $5,700-16,200/mo.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in Quora KPIs (CPC spikes, CTR decay, targeting saturation, creative fatigue, lead quality drops), generate hypotheses, run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — comprehensive reporting on Quora Ads program: targeting type comparison, creative performance decay curves, question/topic effectiveness tracking, full-funnel attribution dashboards, weekly and monthly reports, real-time anomaly alerts. Provides the data layer the optimization loop reads from.
