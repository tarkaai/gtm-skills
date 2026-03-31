---
name: cta-testing-durable
description: >
  CTA Optimization -- Durable Intelligence. AI agent autonomously monitors CTA performance,
  detects metric anomalies, generates variant hypotheses, runs A/B experiments, and auto-implements
  winners. The autonomous-optimization loop finds the local maximum for each CTA surface and
  maintains it as user behavior and traffic patterns shift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + continuous autonomous operation over 6 months"
outcome: "CTR lift sustained or improving over 6 months with zero manual experiment management"
kpis: ["Cumulative CTR lift (all surfaces)", "Experiment velocity (autonomous)", "Win rate", "Time to detect and correct CTR regressions", "Convergence status per surface"]
slug: "cta-testing"
install: "npx gtm-skills add product/retain/cta-testing"
drills:
  - autonomous-optimization
  - cta-variant-pipeline
---

# CTA Optimization -- Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An AI agent runs the complete CTA optimization loop autonomously: monitor metric health -> detect anomalies -> generate hypotheses -> deploy experiments -> evaluate results -> ship winners. Human involvement is limited to weekly brief review and approving high-risk changes. Each CTA surface converges toward its local maximum CTR. When all surfaces converge, the agent reduces monitoring frequency and reports that CTA optimization is mature.

## Leading Indicators

- The agent detects a CTR anomaly and generates a hypothesis within 24 hours of the metric shift
- The agent auto-ships its first winning variant within the first 4 weeks of Durable operation
- Weekly optimization briefs arrive on schedule with accurate cumulative lift calculations
- At least one surface shows convergence (3 consecutive experiments with < 2% lift) within 3 months

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for CTA testing. This is the core loop that makes Durable fundamentally different from Scalable. Configure it with:

**Play-specific parameters:**
- **Primary KPIs to monitor:** per-surface CTR (`cta_clicked / cta_impression`) and per-surface conversion rate (`cta_converted / cta_impression`)
- **Anomaly detection scope:** check each of the 5 instrumented CTA surfaces independently (a drop on one surface should not be masked by gains on another)
- **Experiment constraint:** maximum 1 active CTA experiment at a time across all surfaces (never run parallel CTA tests -- variant interactions make results uninterpretable)
- **Hypothesis source:** feed the agent the full experiment history from Scalable (what was tested, what won, what lost, and why) so it builds on prior learnings rather than re-testing failed approaches
- **Revert threshold:** if any variant causes CTR to drop > 25% vs control after 3 days with 150+ samples per variant, auto-revert immediately

The `autonomous-optimization` drill orchestrates:

1. **Daily monitoring** (n8n cron): query PostHog for each surface's CTR and conversion rate. Compare last 2 weeks against the 4-week rolling average. Classify as normal, plateau, drop, or spike.
2. **Anomaly diagnosis**: when an anomaly is detected, pull the surface's configuration (current CTA text, placement, variant history) and 8-week metric history. Generate 3 ranked hypotheses with expected impact and risk level.
3. **Experiment execution**: take the top hypothesis (if risk is low/medium), create a PostHog feature flag and experiment, deploy the variant. If risk is high, send an alert for human review.
4. **Result evaluation**: when the experiment reaches significance, adopt the winner (roll to 100%), iterate (refine the hypothesis), revert (restore control), or extend (more data needed).
5. **Weekly reporting**: aggregate all optimization activity, compute cumulative lift, assess convergence status, recommend focus areas.

### 2. Configure play-specific monitoring

Run the `autonomous-optimization` drill to add CTA-specific health tracking on top of the generic autonomous loop. This drill adds:

- **Experiment velocity tracking:** are autonomous experiments running at 2-4/month? If the agent is not testing fast enough, diagnose whether it is stuck in the monitoring phase (no anomalies detected because the play is already well-optimized) or stuck in the experiment phase (tests running too long due to insufficient traffic).
- **Surface coverage tracking:** ensure the agent is not over-optimizing high-traffic surfaces while neglecting lower-traffic ones. If a surface has not been tested in 60+ days and its CTR is below median, flag it.
- **Diminishing returns detection:** for each surface, track the lift from each successive experiment. When 3 consecutive experiments produce < 2% lift, the surface has converged.
- **Cumulative impact dashboard:** a single view showing total CTR improvement across all surfaces since optimization began, with estimated downstream revenue impact.

### 3. Configure the variant generation pipeline for autonomous use

Run the `cta-variant-pipeline` drill in autonomous mode. At Scalable level, a human reviewed and prioritized variant hypotheses. At Durable level, the agent:

1. Pulls the surface's current CTA configuration, its full test history, and the latest session recording insights
2. Uses `hypothesis-generation` to produce variant ideas that avoid re-testing previously failed approaches
3. Ranks variants by expected impact, accounting for diminishing returns (if 4 copy variants have been tested on a surface, suggest a placement or timing change instead)
4. Auto-selects the top variant and deploys it

**Human action required:** The first time the agent proposes a variant category it has not tested before on any surface (e.g., the first placement change, the first urgency framing test), review and approve. After the first approved instance of each category, the agent can auto-deploy that category on other surfaces.

**Human action required:** Review the weekly optimization brief every Monday. If the agent's decisions look wrong (e.g., shipping a variant with marginal significance, or testing the same variable repeatedly), adjust the configuration or pause for strategic review.

### 4. Handle convergence

When a CTA surface converges (3 consecutive experiments with < 2% lift):

1. The agent reports: "Surface {X} has reached its local maximum at {CTR}%. Successive experiments are producing diminishing returns."
2. Reduce monitoring frequency for that surface from daily to weekly.
3. Continue monitoring for regressions (traffic pattern changes, product updates, or seasonal shifts can move the optimum).
4. If the surface's CTR drops > 15% from its converged level, re-enter the full optimization loop.

When all 5 surfaces converge:
1. The agent reports: "CTA optimization is mature. All surfaces are at or near their local maximum. Current cumulative lift: {X}%. Further gains require strategic changes: new CTA surfaces, different page layouts, new value propositions, or changes to the upstream traffic mix."
2. Switch to maintenance mode: weekly monitoring, monthly optimization briefs, immediate alerts only for regressions > 15%.

### 5. Evaluate sustainability

This level runs continuously. Monthly evaluation:

- **Cumulative lift sustained:** compare current per-surface CTR to the pre-optimization baselines from Smoke. If any surface has regressed to within 5% of its original baseline, the optimization gains are eroding -- re-enter the active optimization loop for that surface.
- **Autonomous operation health:** is the agent running experiments without human intervention? Are weekly briefs arriving on time? Are guardrail alerts firing correctly when they should?
- **Zero manual experiment management:** the success criterion for Durable is that no human needs to generate hypotheses, configure experiments, or make ship/revert decisions. The agent does it all, and the human reviews the weekly brief.

If CTR lift is sustained or improving over 6 months with zero manual experiment management, the play is durable.

## Time Estimate

- 8 hours: configure autonomous-optimization drill with CTA-specific parameters
- 4 hours: set up cta-experiment-health-monitor dashboard and alerts
- 4 hours: configure cta-variant-pipeline for autonomous hypothesis generation
- 4 hours: test the full loop end-to-end (trigger an artificial anomaly and verify the agent responds correctly)
- Ongoing: 1 hour/week reviewing the weekly optimization brief
- Ongoing: 0.5 hours/month for strategic review when surfaces converge

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, anomaly detection, dashboards | Free tier: 1M events/mo, 1M flag requests/mo. At Durable volume, expect usage-based charges for experiments and flag evaluations ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Daily monitoring cron, experiment queuing, alert routing | Self-hosted: free. Cloud: from EUR 24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief generation | Claude API: usage-based, ~$3-15/1M tokens depending on model. Estimate $10-30/mo for weekly optimization cycles ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop that detects anomalies, generates hypotheses, runs experiments, evaluates results, and auto-implements winners. This is what makes Durable fundamentally different from Scalable.
- `autonomous-optimization` -- CTA-specific monitoring layer that tracks experiment velocity, surface coverage, diminishing returns, and cumulative impact across all surfaces
- `cta-variant-pipeline` -- generates and deploys CTA variants. At Durable level, runs autonomously with the agent selecting and deploying variants without human intervention (except for new variant categories)
