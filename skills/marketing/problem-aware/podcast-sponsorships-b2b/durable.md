---
name: podcast-sponsorships-b2b-durable
description: >
  B2B Podcast Sponsorships — Durable Intelligence. AI agents autonomously monitor
  podcast sponsorship performance, detect anomalies, generate optimization hypotheses,
  run experiments on script angles and podcast mix, and auto-implement winners to
  sustain ≥35 qualified leads per quarter at declining CPL.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Content"
level: "Durable Intelligence"
time: "120 hours over 12 months"
outcome: "Sustained ≥35 qualified leads/quarter over 12 months with CPL trending down via AI-driven podcast selection and script optimization"
kpis: ["Sustained qualified leads per quarter", "CPL trend (quarter-over-quarter)", "AI experiment win rate", "Podcast portfolio churn rate", "Attribution signal accuracy"]
slug: "podcast-sponsorships-b2b"
install: "npx gtm-skills add marketing/problem-aware/podcast-sponsorships-b2b"
drills:
  - autonomous-optimization
  - podcast-sponsor-research
---

# B2B Podcast Sponsorships — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Content

## Outcomes

The AI agent autonomously manages the podcast sponsorship program: monitoring performance across all placements, detecting when metrics plateau or decline, generating hypotheses for improvement, running experiments on ad scripts, podcast mix, CTA formats, and landing pages, evaluating results, and auto-implementing winners. The program sustains at least 35 qualified leads per quarter over 12 months with CPL trending down quarter-over-quarter. The agent generates weekly optimization briefs and converges to the local maximum — the best possible performance given the current podcast landscape and ICP.

## Leading Indicators

- The `autonomous-optimization` loop runs daily without errors and triggers Phase 2 (diagnose) when anomalies are detected (signal: monitoring is operational)
- At least 1 experiment runs per month with a clear result (adopt, iterate, or revert) (signal: the optimization engine is active)
- Experiment win rate is above 30% (signal: hypotheses are data-informed, not random)
- CPL has not increased for 3 consecutive months (signal: optimization is maintaining or improving performance)
- New podcasts enter and exit the portfolio quarterly without disrupting overall lead volume (signal: the portfolio is resilient to individual show changes)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the podcast sponsorship play. This is the core loop that makes Durable fundamentally different from Scalable:

**Phase 1 — Monitor (daily via n8n cron):**
- Query PostHog for the play's primary KPIs: total leads (14-day rolling), blended CPL, per-podcast CPL, click volume, promo redemption rate
- Compare last 2 weeks against the 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current podcast portfolio (Tier 1/2/3 breakdown), recent ad scripts, CTA formats, landing page conversion rates, promo code redemption rates by podcast
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with anomaly data and play context
- Receive 3 ranked hypotheses. Examples:
  - "Podcast X's audience is saturated — CPL increased 40% over 3 placements. Test pausing X and redirecting budget to 2 new Tier 3 podcasts."
  - "Problem-led scripts are declining. Test story-led scripts on the next 3 placements."
  - "Promo code redemptions dropped 30%. Test a stronger offer (20% discount vs current 10%)."
  - "Mid-roll placements outperform pre-roll by 2x. Convert remaining pre-roll bookings to mid-roll."
- If top hypothesis is high-risk (budget change >20%, major portfolio shift): send alert for human review and STOP
- If low/medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment. For podcast sponsorships, experiments are run across placements (not within a single placement):
  - **Script experiment**: Use variant A on the next 2 placements and variant B on the following 2. Compare CPL.
  - **Podcast experiment**: Book 2 new podcasts from Tier 3 pipeline and compare CPL against a Tier 1 rerun.
  - **CTA experiment**: Switch half the upcoming placements to a new CTA format and compare lead attribution signal breakdown.
  - **Landing page experiment**: Split traffic from upcoming placements between 2 landing page variants using PostHog feature flags.
- Set experiment duration: minimum 4 placements or 4 weeks, whichever is longer (podcast experiments need sufficient sample size)
- Log experiment in Attio: hypothesis, start date, placements assigned, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog and Attio
- Run `experiment-evaluation` with control vs. variant data
- Decision:
  - **Adopt**: Update the default script template, CTA format, or portfolio composition. Log the change.
  - **Iterate**: Generate a refined hypothesis based on this result. Return to Phase 2.
  - **Revert**: Discard the variant. Restore previous defaults. Return to Phase 1.
  - **Extend**: Keep testing for 2 more placements if results are inconclusive.
- Store the full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments running, decisions made
- Calculate net metric change from adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on leads and CPL
  - Current experiment status and expected completion date
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Run continuous podcast portfolio management

Run the `autonomous-optimization` drill as the always-on monitoring layer:

- PostHog dashboard updated in real-time across all placements
- Automated 14-day performance collection for every placement
- Biweekly report with rebooking recommendations, fed into the autonomous optimization loop
- Podcast scoring model continuously updated with actual performance data
- Tier promotions and demotions happen automatically based on the scoring model:
  - If a Tier 2 podcast delivers Tier 1 CPL for 2 consecutive placements: auto-promote to Tier 1
  - If a Tier 1 podcast's CPL exceeds target by 30% for 2 consecutive placements: auto-demote to Tier 2
  - If a Tier 3 test podcast delivers CPL below target on first placement: fast-track to Tier 1

### 3. Maintain the podcast discovery pipeline

Run the `podcast-sponsor-research` drill quarterly (automated via n8n trigger):

- Search marketplaces and directories for new podcasts matching ICP
- Cross-reference against current portfolio to avoid duplicates
- Score and add 5-10 new prospects to the Tier 3 pipeline each quarter
- Identify podcasts that have stopped publishing or changed format — remove from portfolio
- Detect new competitor sponsors — flag the podcasts they are sponsoring for evaluation

### 4. Build long-term podcast relationships

As the portfolio matures, the agent should:

- Identify the top 3-5 podcasts by lifetime value (total leads generated, CPL, relationship longevity)
- Negotiate annual sponsorship packages with these top performers for better rates and guaranteed slots
- Develop podcast-specific ad scripts that reference the ongoing relationship ("You have heard me talk about {product} before — here is what is new...")
- Track audience overlap: if 2 podcasts share a high percentage of listeners, reduce frequency on one to avoid ad fatigue

**Human action required:** Approve annual sponsorship commitments. Review relationship-tier negotiations. Sign multi-episode contracts.

### 5. Detect convergence

The autonomous optimization loop converges when:
- Successive experiments produce <2% improvement for 3 consecutive experiments
- CPL has been stable (within +/-5%) for 2+ consecutive quarters
- Podcast portfolio composition has been stable (no Tier changes) for 2 months

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from monthly to quarterly
3. Generate a convergence report: "This play has reached its local maximum. Current performance: {leads/quarter}, {CPL}, {portfolio size}. Further gains require strategic changes — new market segment, new ad format (e.g., custom integrations), or expanded budget for larger shows."
4. Maintain the monitoring loop at reduced frequency to detect external changes (new competitor, podcast audience shift, market trend) that warrant reactivation

## Time Estimate

- Autonomous optimization loop setup: 8 hours (one-time)
- Monthly oversight and human approvals: 4 hours/month
- Quarterly research refresh: 3 hours/quarter
- Annual relationship negotiations: 4 hours/year
- Agent compute time: runs automatically via n8n + PostHog + Claude

Total: ~120 hours over 12 months (~10 hours/month including setup, declining to ~6/month after convergence)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Attribution, anomaly detection, experiments | Growth: $0/mo up to 1M events, then usage-based ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation: daily monitoring, experiment triggers, reports | Pro: $50/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, script writing | ~$20-50/mo at Durable volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Attio | CRM: portfolio management, deal tracking, experiment logging | Plus: $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Quarterly podcast enrichment | Explorer: $385/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Dub.co | Vanity URL management | Pro: $24/mo ([dub.co/pricing](https://dub.co/pricing)) |
| Podscribe (optional) | Pixel-based podcast attribution | $250/mo + $1.50 CPM ([podscribe.com](https://podscribe.com)) |
| Podcast placements (8-15/mo) | Paid sponsorships | $1,500-6,000/mo at negotiated annual rates |

**Estimated cost for this level: $2,000-7,500/mo** (sponsorship placements + tools + agent compute)

## Sustain Threshold

**Sustained: >= 35 qualified leads/quarter AND CPL trending down or stable quarter-over-quarter for 12 months**

This level runs continuously. The autonomous optimization loop detects and corrects performance degradation automatically. Review monthly: what experiments ran, what improved, what converged.

- **Sustained**: Leads and CPL meet targets for 4 consecutive quarters. The play is durable. Reduce to maintenance mode at convergence.
- **Degrading**: Leads or CPL miss targets for 2 consecutive quarters despite active experiments. Diagnose: market saturation, audience fatigue, or competitive pressure. The agent escalates with a strategic review brief.
- **Converged**: Successive experiments produce <2% improvement. The play has reached its local maximum. Reduce monitoring to weekly and experiments to quarterly.

## Drills Referenced

- `autonomous-optimization` — the core loop: monitor metrics daily, diagnose anomalies, generate hypotheses, run experiments across placements, evaluate results, auto-implement winners, report weekly
- `autonomous-optimization` — always-on multi-signal attribution dashboard, automated performance collection, biweekly reports, podcast scoring model
- `podcast-sponsor-research` — quarterly pipeline refresh to discover new podcasts and maintain portfolio health
