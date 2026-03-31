---
name: award-submissions-program-durable
description: >
  Industry Award Submissions — Durable Intelligence. Always-on AI agents autonomously optimize
  award targeting, submission content, amplification strategy, and social proof deployment.
  The autonomous-optimization loop detects anomalies, generates hypotheses, runs experiments,
  and auto-implements winners. Quarterly optimization briefs track convergence.
stage: "Marketing > SolutionAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Durable Intelligence"
time: "140 hours over 12 months"
outcome: "Sustained >=30 qualified leads annually from award credibility, with <2% variance in successive optimization cycles indicating convergence at the local maximum"
kpis: ["Sustained award-influenced leads/year", "Autonomous experiment win rate", "Win rate by category trend", "Social proof coverage score", "Amplification reach per win", "Optimization convergence rate"]
slug: "award-submissions-program"
install: "npx gtm-skills add marketing/solution-aware/award-submissions-program"
drills:
  - autonomous-optimization
---

# Industry Award Submissions — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

Always-on AI agents finding the local maximum. The award program runs autonomously: new awards are discovered monthly, submissions are prepared and routed for review, wins are amplified through automated PR workflows, and social proof placement is optimized based on impact data. The `autonomous-optimization` drill runs the core loop: detect anomalies in award program KPIs, generate hypotheses, run experiments, evaluate results, and auto-implement winners. Quarterly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement.

**Pass threshold:** Sustained >=30 qualified leads annually from award credibility, with <2% variance in successive optimization cycles indicating convergence at the local maximum.

## Leading Indicators

- Autonomous optimization loop runs monthly without manual intervention
- Quarterly optimization briefs are generated and posted to Slack
- At least 1 experiment per quarter is initiated, evaluated, and decided
- Award pipeline operates autonomously: discovery, scoring, preparation, review routing, submission
- Award-influenced leads per year are stable or improving
- Convergence signal: last 3 experiments each produced <2% improvement
- Win rate improving or stable at >30%

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the award program. Note: award programs operate on quarterly cycles (longer than content or ad plays), so the optimization loop runs monthly rather than daily.

**Configure the optimization loop:**

**Phase 1 — Monitor (monthly via n8n cron):**
- Use `posthog-anomaly-detection` to check award program KPIs:
  - Win rate by award category
  - Submissions per quarter (pipeline health)
  - PR placements generated per win
  - Award-influenced deals per quarter
  - Social proof impressions (badge views on website and in sales materials)
  - Cost per award-attributed lead (entry fees + time investment)
- Compare last quarter against 4-quarter rolling average
- Classify: normal (within +-10%), plateau (+-2% for 2+ quarters), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current award categories targeted, recent submission quality, win/loss patterns, amplification effectiveness, sales team feedback
- Pull 4-quarter metric history from PostHog
- Run `hypothesis-generation` with anomaly data and context
- Example hypotheses:
  - "Win rate dropped from 35% to 18% this quarter. Hypothesis: we are submitting to more competitive awards (Tier 1) without adjusting submission quality. Test: increase content customization for Tier 1 awards by adding 2 additional customer reference letters per submission."
  - "Award-influenced deals dropped despite stable win count. Hypothesis: recent wins are in categories the sales team does not reference. Test: survey the sales team on which award categories resonate most with prospects, then shift submission effort to those categories."
  - "PR amplification per win decreased 50%. Hypothesis: we are winning smaller, niche awards that journalists do not cover. Test: allocate 50% of paid entry budget to 2-3 high-profile awards (even if win probability is lower) for PR value."
  - "Social proof impressions flat despite adding new badges. Hypothesis: badge placement on website is below the fold on key pages. Test: move award badges above the fold on pricing page and measure badge_viewed events."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Implement the variant:
  - If testing submission quality: prepare the next 3 submissions with the enhanced approach (extra references, more metrics) while keeping 3 at standard quality
  - If testing category targeting: shift the next quarter's submission mix according to the hypothesis
  - If testing amplification strategy: try the new PR approach for the next 2 wins vs the standard approach for the following 2
  - If testing social proof placement: A/B test badge position on website using PostHog feature flags
- Set experiment duration: minimum 1 quarter (award cycles are slow)
- Log experiment in Attio with: hypothesis, start date, expected evaluation date, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the award playbook (targeting criteria, submission templates, amplification workflow). Log the change.
- If Iterate: generate new hypothesis. Return to Phase 2.
- If Revert: restore previous approach. Log failure. Return to Phase 1.
- Store full evaluation in Attio

**Phase 5 — Report (quarterly via n8n cron):**
- Generate quarterly optimization brief:
  - Anomalies detected this quarter
  - Experiments running, completed, decided
  - Net impact on award-influenced leads
  - Current distance from estimated local maximum
  - Award pipeline health: upcoming deadlines, submissions in progress
  - Social proof coverage: where awards are displayed, engagement data
  - Recommended focus for next quarter
- Post to Slack, store in Attio

### 2. Deploy Award Performance Reporting

Run the `autonomous-optimization` drill at full scale:

1. Maintain the 4-panel PostHog dashboard (submission pipeline, win tracking, social proof, attribution)
2. Keep anomaly detection thresholds calibrated annually
3. Quarterly automated reports continue generating
4. Annual deep-dive: total awards won, ROI (entry fees vs pipeline influenced), year-over-year comparison

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill, adapted for award program cycles:

- **Rate limit:** Maximum 1 active experiment per quarter (award cycles are slow)
- **Revert threshold:** If win rate drops below 10% for 2 consecutive quarters during an experiment, auto-revert
- **Human approval required for:**
  - Entry fee commitments exceeding $500 per award
  - Submitting to awards that require public disclosure of revenue or other sensitive metrics
  - Changes to customer reference processes
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 1 quarter before testing the same variable
- **Maximum experiments per year:** 4 (one per quarter). If 2 consecutive fail, pause and flag for human strategic review.

### 4. Autonomous Award Intelligence

At Durable level, the system proactively identifies opportunities:

1. **Competitor award monitoring:** n8n workflow tracks competitor award announcements. When a competitor wins an award you have not submitted to, auto-add it to the pipeline for next cycle.
2. **New award detection:** Monthly Claygent scan for new awards in your industry. New awards often have lower competition in their first 1-2 years.
3. **Award organizer relationship:** Track interactions with award organizers. Some provide advance notice of new categories or changes to criteria.
4. **Content freshness monitoring:** Flag when content blocks are >90 days old and metrics need updating.
5. **Customer reference rotation:** Track which customers have been used as references and ensure no single customer is over-used. Auto-suggest rotation.

### 5. Monitor Convergence

Track the magnitude of improvement from each adopted experiment:

- If the last 3 consecutive experiments each produced <2% improvement:
  1. The award program is converged — current performance is near-optimal
  2. Reduce discovery frequency from monthly to quarterly
  3. Reduce experiment frequency to 1-2 per year (maintenance mode)
  4. Generate a convergence report: "Award program optimized. Annual wins: [X]. Win rate: [Y]. Award-influenced leads/year: [Z]. Cost per award-attributed lead: [$A]. Further gains require strategic changes (entering new industry categories, pursuing higher-tier awards requiring case studies or advisory board nominations, or creating your own award program for brand authority) rather than tactical optimization."

Post convergence report to Slack and store in Attio.

### 6. Handle Market Shifts

The optimizer should detect external shifts:

- If a new award emerges in your category with high ICP overlap: prioritize and submit immediately
- If an established award changes its criteria or category structure: update submission content blocks
- If peer review platforms (G2, Capterra) become more influential: shift effort toward G2 Best Software badges and Capterra Shortlist (these are always-on, not one-time submissions)
- If competitors win awards you previously held: draft stronger re-submission with new evidence

## Time Estimate

- 15 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 8 hours: Award monitoring refinement and intelligence automation
- 40 hours: Ongoing submission preparation and review over 12 months (~3.5 hours/month)
- 30 hours: Win amplification and PR outreach over 12 months
- 20 hours: Quarterly optimization reviews (5 hours/quarter x 4)
- 15 hours: Sales integration maintenance, content block refresh, and annual analysis
- 12 hours: Convergence monitoring and strategic adaptation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — submission pipeline, experiment logging, deal attribution | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — award discovery, competitor monitoring | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Automation — discovery, amplification, optimization loop | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Email — award announcement distribution | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Instantly | Media outreach for win amplification | $30/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Claude API | Submission drafting, hypothesis generation, evaluation | ~$40-70/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Entry fees ~$1,000-3,000/year. Loops ~$49/mo + Instantly ~$30/mo = ~$79/mo play-specific tools. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `autonomous-optimization` — the core optimization loop (monthly cadence): detect anomalies in award KPIs, generate hypotheses (category targeting, submission quality, amplification strategy, social proof placement), run experiments, evaluate results, auto-implement winners. Quarterly optimization briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — continuous monitoring of submission pipeline, win rates, social proof impact, and award-to-pipeline attribution. Provides the data layer the optimization loop reads from.
