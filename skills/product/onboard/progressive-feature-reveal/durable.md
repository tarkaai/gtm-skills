---
name: progressive-feature-reveal-durable
description: >
  Progressive Feature Discovery — Durable Intelligence. AI agent autonomously
  optimizes gating criteria, reveal UX, and persona paths via continuous
  experimentation. Sustained or improving ≥40% adoption over 6 months.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving ≥40% adoption over 6 months via autonomous optimization"
kpis: ["Post-unlock adoption rate (rolling 30d)", "Experiment velocity", "AI lift (cumulative improvement from experiments)", "Time to convergence", "NPS by tier"]
slug: "progressive-feature-reveal"
install: "npx gtm-skills add product/onboard/progressive-feature-reveal"
drills:
  - autonomous-optimization
  - feature-adoption-monitor
  - nps-feedback-loop
---

# Progressive Feature Discovery — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Sustained or improving ≥40% post-unlock adoption rate over 6 months, driven by an autonomous AI agent that continuously experiments on gating criteria, reveal UX, nudge timing, and persona paths. The agent finds the local maximum and maintains it as user behavior and product surface evolve.

## Leading Indicators

- Autonomous optimization loop running: ≥2 experiments completed per month without human initiation
- Cumulative AI lift: ≥5pp improvement over Scalable baseline within first 3 months
- Weekly optimization briefs generated on schedule
- NPS by tier trending upward (promoters increasing at Advanced and Power tiers)
- Convergence signal: successive experiments producing <2% improvement (local maximum reached)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for progressive feature reveal. The agent loop operates on these play-specific parameters:

**Monitored metrics:**
- Post-unlock adoption rate per tier (primary)
- Time-to-unlock per tier (secondary)
- Stalled-user rate per tier (secondary)
- Unlock message CTR (secondary)
- Feature regression rate (guardrail)

**Experiment surface (what the agent can change):**
- Readiness criteria thresholds (e.g., change "3 Core actions in 2 sessions" to "2 Core actions in 2 sessions")
- Unlock message copy and format (banner vs. modal vs. tooltip)
- Nudge timing for stalled users (24h vs. 48h vs. 72h delay)
- Locked-state UX (hidden vs. teased vs. progress-bar)
- Persona routing thresholds (which properties determine persona assignment)

**What the agent CANNOT change without human approval:**
- Adding or removing features from a tier (structural product decision)
- Changing the tier model itself (e.g., merging Intermediate and Advanced)
- Any change that would gate a feature a paying user currently has access to
- Budget allocation or tool configuration changes

Configure the 5-phase loop:

**Phase 1 — Monitor (daily via n8n):** Query PostHog for all monitored metrics. Compare last 2 weeks against 4-week rolling average. Classify: normal, plateau, drop, or spike. If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):** Pull 8-week metric history from PostHog. Pull current configuration (readiness criteria, message copy, nudge timing) from Attio. Run `hypothesis-generation` with the anomaly data and configuration context. Receive 3 ranked hypotheses. Store in Attio. If top hypothesis is high-risk, alert human and stop.

**Phase 3 — Experiment (triggered by hypothesis acceptance):** Design a PostHog experiment using feature flags. Split traffic between control (current) and variant (hypothesis change). Minimum 7 days or 100+ samples per variant. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment end):** Pull results. Run `experiment-evaluation`. Decision: Adopt (implement winner), Iterate (new hypothesis), Revert (restore control), or Extend (more time). Store full evaluation in Attio.

**Phase 5 — Report (weekly via n8n):** Aggregate all optimization activity. Calculate net metric change from adopted changes. Generate weekly optimization brief: what changed, why, net impact, distance from local maximum, recommended focus. Post to Slack and Attio.

### 2. Upgrade the feature adoption monitor

Run the `feature-adoption-monitor` drill with expanded scope for Durable:

- Add per-experiment cohort tracking: users who experienced each experiment variant get a cohort so you can measure long-term effects (did Experiment 3's winner sustain at Day 30?)
- Add feature regression alerting: if a user who was using an Advanced feature stops for 7+ days, the agent evaluates whether this correlates with a recent experiment change
- Add a "reveal effectiveness" panel to the dashboard: for each unlock message variant currently live, show the CTR and 7-day adoption rate side by side

### 3. Launch NPS by tier

Run the `nps-feedback-loop` drill segmented by feature tier:

- Survey users at Intermediate tier after 14 days of active use
- Survey users at Advanced tier after 21 days of active use
- Survey users at Power tier after 30 days of active use

Segment NPS analysis by tier to detect satisfaction differences. If Advanced-tier users have lower NPS than Intermediate, the Advanced features may be confusing or under-documented. Feed qualitative feedback (open-text responses) into the autonomous optimization loop as hypothesis input: "5 users said Templates are hard to find" becomes a hypothesis to test a more prominent reveal moment for Templates.

### 4. Configure convergence detection

The autonomous optimization loop should detect when the play has reached its local maximum. Convergence criteria:

- 3 consecutive experiments produce <2% improvement on the primary metric
- Post-unlock adoption rate has been stable (±2pp) for 4+ weeks
- No anomalies detected for 3+ weeks

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Generate a convergence report: current performance, all experiments run, cumulative lift, and what would be needed for further gains (product changes, new features, new personas)
3. The agent enters maintenance mode: monitors weekly, only triggers new experiments if a metric drops below threshold

### 5. Maintain and defend the local maximum

Even after convergence, the agent continues monitoring for external disruptions:

- **Product changes:** New feature shipped? The agent evaluates which tier it belongs in and whether readiness criteria need updating.
- **User mix shifts:** Signup source changes (e.g., viral spike from Product Hunt) bring different personas. The agent detects the shift via cohort analysis and tests whether existing persona paths work for the new mix.
- **Seasonal patterns:** Usage drops during holidays or industry events. The agent distinguishes seasonal dips from real declines by comparing to prior-period patterns.

When a disruption causes metrics to drop below threshold, the agent exits maintenance mode and re-enters the full optimization loop.

### 6. Evaluate sustainability

This level runs continuously. Monthly review:

- Is post-unlock adoption rate ≥40% (rolling 30-day)?
- How many experiments ran this month, and what was the net impact?
- Is NPS by tier stable or improving?
- Has the agent reached convergence, or is it still finding improvements?

**Sustained pass:** Adoption ≥40% for 6 consecutive months. The play is durable.
**Decay detected:** If adoption drops below 40% for 2 consecutive months despite active optimization, escalate for strategic review — the issue may be product-level (feature quality, competitive pressure) rather than reveal-strategy-level.

## Time Estimate

- 16 hours: autonomous optimization loop setup (n8n workflows, PostHog experiments integration, Attio logging, Slack reporting)
- 8 hours: feature adoption monitor expansion (per-experiment cohorts, regression alerting, reveal effectiveness panel)
- 6 hours: NPS by tier setup (survey triggers, segmented analysis, feedback routing)
- 4 hours: convergence detection configuration
- 4 hours/month ongoing: review weekly briefs, approve high-risk hypotheses, adjust experiment surfaces (24 hours x 4 months post-setup)
- Total: ~120 hours over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| [PostHog](https://posthog.com/pricing) | Feature flags, experiments, funnels, cohorts, dashboards | Free up to 1M events/mo; ~$50-200/mo at scale depending on volume |
| [Intercom](https://www.intercom.com/pricing) | Unlock messages, stalled-user nudges, NPS surveys, product tours | Essential $29/seat/mo + Proactive Support Plus $99/mo + usage ~$50-200/mo |
| [Loops](https://loops.so/pricing) | Stalled-user and churn-prevention emails | $49/mo (up to 5,000 contacts) |
| [Anthropic API](https://www.anthropic.com/pricing) | Hypothesis generation, experiment evaluation, weekly briefs | ~$20-50/mo (Claude API for autonomous optimization loop) |
| [n8n](https://n8n.io/pricing) | Optimization loop scheduling, all automation workflows | Standard stack (not counted) |

**Estimated play-specific cost:** $250-500/mo (Intercom at scale + Loops + Anthropic API for autonomous optimization)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, weekly briefs
- `feature-adoption-monitor` — expanded with per-experiment cohort tracking, feature regression alerting, and reveal effectiveness dashboard
- `nps-feedback-loop` — tier-segmented NPS surveys feeding qualitative insights into the optimization loop
