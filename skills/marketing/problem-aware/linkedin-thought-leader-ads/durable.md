---
name: linkedin-thought-leader-ads-durable
description: >
  Thought Leader Ads — Durable Intelligence. Always-on AI agents continuously optimize TLA content,
  targeting, budget allocation, and creative rotation. The autonomous optimization loop detects metric
  anomalies, generates improvement hypotheses, runs A/B experiments, and auto-implements winners.
  Weekly optimization briefs track convergence toward the local maximum.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Durable Intelligence"
time: "150 hours over 12 months"
outcome: "Sustained >=60 qualified leads/month and cost per qualified lead <=100 over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained monthly qualified leads", "Cost per qualified lead trend", "Autonomous experiment win rate", "Content pipeline health", "Audience fatigue index", "Optimization convergence rate"]
slug: "linkedin-thought-leader-ads"
install: "npx gtm-skills add marketing/problem-aware/linkedin-thought-leader-ads"
drills:
  - autonomous-optimization
---

# Thought Leader Ads — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

Always-on AI agents finding the local maximum. The TLA program runs itself: content generation, post selection, campaign management, audience optimization, budget allocation, and performance reporting all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in TLA KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement -- at that point, TLA performance is near-optimal for the current market, audience, and competitive landscape.

**Pass threshold:** Sustained >=60 qualified leads/month and cost per qualified lead <=100 over 12 months, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Content pipeline operates autonomously: drafts generated, reviewed, published, selected, promoted, retired
- Cost per qualified lead is stable or improving month over month
- Convergence signal: last 3 experiments produced <2% improvement each
- Audience fatigue index stays below threshold without manual intervention (auto-rotation handles it)

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the TLA program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 -- Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check TLA program KPIs:
  - Cost per qualified lead (primary KPI)
  - Engagement rate by thought leader
  - CPC by audience segment
  - Content velocity (posts promoted per week)
  - Lead quality (% scoring 70+ on ICP scoring)
  - Audience frequency by segment
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
- Gather context from Attio: current audience segments, budget allocation, active thought leaders, content templates in rotation
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "CPC increased 30% this week. Hypothesis: audience segment 'Core ICP' has reached saturation at frequency 6.2/week. Test expanding the audience by adding 2 new industries while maintaining seniority filter."
  - "Engagement rate dropped from 2.1% to 1.4%. Hypothesis: the last 3 promoted posts all used the 'stat hook' template. Test promoting a 'personal story' template post instead."
  - "Cost per qualified lead increased 25%. Hypothesis: the educational nurture sequence has not been updated in 8 weeks and open rates dropped. Test refreshing the nurture sequence emails."
  - "Thought Leader B's posts consistently underperform Thought Leader A's by 40% on CPC. Hypothesis: Thought Leader B's content pillars do not align with the audience segments they are being promoted to. Test swapping audience assignments."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate mechanism:
  - If testing audience changes: create a duplicate campaign with the modified audience via LinkedIn Marketing API
  - If testing content templates: generate posts using the new template and promote them in a parallel campaign
  - If testing budget allocation: split budget between current and proposed allocation
  - If testing nurture sequences: create a Loops A/B test on the nurture emails
  - If testing bidding strategy: duplicate campaign with different bidding configuration
- Set experiment duration: minimum 7 days or 500+ impressions per variant, whichever is longer
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update live configuration, log the change, move to Phase 5
- If Iterate: generate new hypothesis building on this result, return to Phase 2
- If Revert: restore control configuration, log failure, return to Phase 1
- Store full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on cost per qualified lead and lead volume
  - Current distance from estimated local maximum
  - Content pipeline health: posts in queue, average ad age, thought leader activity
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy TLA Performance Reporting

Run the `autonomous-optimization` drill:

1. Build the PostHog TLA dashboard (8 panels: spend/reach trends, per-post engagement, CPC trends, audience comparison, format performance, hook type analysis, conversion funnel, pipeline attribution)
2. Build Attio saved views (TLA-sourced contacts, TLA pipeline, TLA ROI by thought leader)
3. Deploy the weekly automated report (n8n workflow every Monday)
4. Deploy the monthly ROI report (first Monday of each month)
5. Configure 5 real-time anomaly alerts (CPC spike, engagement drop, zero conversions, budget runaway, audience fatigue)

The reporting layer provides the data substrate that the autonomous optimization loop reads. Without accurate reporting, the optimizer cannot generate meaningful hypotheses.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the TLA program:

- **Rate limit:** Maximum 1 active experiment at a time on the TLA program
- **Revert threshold:** If cost per qualified lead exceeds 2x the 4-week average during any experiment, auto-revert immediately
- **Human approval required for:**
  - Budget changes exceeding 20% of current monthly spend
  - Adding or removing a thought leader from the program
  - Changes to audience targeting that affect more than 50% of impressions
  - Any change the hypothesis generator flags as "high risk"
  - Changes to the thought leader's content voice or pillar strategy
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All TLA events must have PostHog tracking before experiments can target them. If a KPI lacks tracking, fix tracking first using the `posthog-gtm-events` drill

### 4. Autonomous Content Pipeline

At Durable level, the content pipeline should operate with minimal human touch:

1. **AI generates post drafts** weekly using the evolving content playbook (templates are updated based on experiment results)
2. **Thought leaders review** (30 min/week each) and approve/edit
3. **Posts publish** via Taplio on schedule
4. **n8n workflow auto-scores** new posts after 48 hours of organic performance
5. **Top performers auto-queue** for TLA promotion
6. **Fatigue monitor auto-retires** underperforming ads
7. **The optimization loop** continuously tests which content templates, hook types, and pain points produce the best TLA results

Over time, the content playbook evolves based on experimental data. The templates that produce the best-performing TLAs get weighted more heavily in the draft generation pipeline.

### 5. Monitor Convergence

The optimization loop should detect when the TLA program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged -- current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report: "TLA program optimized. Current cost per qualified lead: $[X]. Monthly qualified leads: [Y]. Further gains require strategic changes (new thought leaders, new audience markets, product positioning changes, or channel diversification) rather than tactical optimization."

Post the convergence report to Slack and store in Attio.

### 6. Handle Market and Platform Shifts

LinkedIn's ad platform, algorithm, and TLA feature set evolve over time. The optimizer should detect shifts:

- If CPM increases across all segments by >20%: LinkedIn may have changed auction dynamics. Test bidding strategy changes.
- If organic engagement drops across all thought leaders: LinkedIn algorithm may have shifted. Test new post formats or lengths.
- If conversion rate drops despite stable engagement: external factor (competitor entry, market saturation). Alert for strategic review.
- If LinkedIn adds new TLA features (e.g., Lead Gen Form support for TLAs): alert the team to evaluate and potentially redesign the lead capture flow.

In these cases: the optimizer flags the situation and recommends whether tactical optimization can address it or whether strategic human intervention is needed.

## Time Estimate

- 20 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 10 hours: Performance reporting dashboard and monthly ROI calculation
- 5 hours: Content pipeline automation refinement
- 80 hours: Ongoing optimization over 12 months (~1.5 hours/week for monitoring, experiment design, evaluation)
- 15 hours: Monthly strategic reviews (12 reviews at ~1.25 hours each)
- 10 hours: Convergence analysis and maintenance mode transition
- 10 hours: Platform shift response and strategic adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | TLA campaign management (agent-optimized) | Ad spend ($5,000-20,000/mo, agent-optimized across segments) |
| PostHog | Analytics — dashboards, experiments, anomaly detection, funnels | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead tracking, experiment logging, pipeline attribution | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring at scale | $349/mo (Explorer) or $699/mo (Pro) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences with A/B testing | $99/mo (Growth) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — optimization loop, content pipeline, reporting | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Taplio | LinkedIn analytics and scheduling | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |
| Anthropic API | AI — content generation, hypothesis generation, experiment evaluation | Usage-based, ~$50-100/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** $5,000-20,000/mo ad spend + ~$700-1,100/mo tools + ~$50-100/mo AI API. Total: $5,750-21,200/mo.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in TLA KPIs, generate hypotheses (audience saturation, content fatigue, nurture sequence staleness, thought leader mismatch), run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — comprehensive reporting on TLA program effectiveness: content, audience, and pipeline performance dashboards, weekly and monthly automated reports, real-time anomaly alerts. Provides the data layer the optimization loop reads from.
