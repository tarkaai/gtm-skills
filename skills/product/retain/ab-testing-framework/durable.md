---
name: ab-testing-framework-durable
description: >
  Product A/B Testing — Durable Intelligence. Autonomous agent loop that monitors experiment program
  health, generates improvement hypotheses grounded in historical learnings, runs experiments,
  auto-implements winners, and detects convergence. The autonomous-optimization drill runs the core
  loop: detect metric anomalies, generate hypotheses, run A/B experiments, evaluate results,
  auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce
  <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving experiment program performance over 6 months via autonomous AI optimization"
kpis: ["Experiment velocity", "Win rate", "Cumulative lift", "Convergence detection", "AI lift"]
slug: "ab-testing-framework"
install: "npx gtm-skills add product/retain/ab-testing-framework"
drills:
  - autonomous-optimization
  - experiment-learnings-database
---

# Product A/B Testing — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The A/B testing program operates autonomously. An always-on agent loop monitors experiment program health, detects when metrics plateau or decline, generates improvement hypotheses grounded in a cumulative learnings database, runs experiments, evaluates results, and auto-implements winners without human intervention. The agent produces weekly optimization briefs. The system detects convergence per product area -- when successive experiments produce <2% improvement, the area has reached its local maximum. The agent shifts resources to unconverged areas and enters maintenance mode for converged ones. Over 6 months, the program sustains or improves upon the cumulative lift achieved at Scalable level.

## Leading Indicators

- Autonomous optimization loop runs continuously for 4+ weeks without human intervention
- At least 2 experiments per month are auto-designed, launched, evaluated, and decided by the agent
- Weekly optimization briefs are generated and posted automatically
- The learnings database is queried before every new hypothesis (no repeated failures)
- Convergence is detected in at least 1 product area (proving the system can find local maxima)
- No manual calibration needed -- the agent handles stalls, empty backlogs, and win rate anomalies

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the A/B testing program. The optimization loop has 5 phases:

**Phase 1 -- Monitor (daily via n8n cron):**
The agent runs `posthog-anomaly-detection` on the testing program's core KPIs: experiment velocity, win rate (rolling 8-week), cumulative lift trend, and cycle time. It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal, plateau, drop, or spike. If any anomaly is detected, the loop triggers Phase 2.

Examples of anomalies the agent detects:
- Velocity plateau: experiments per month has been flat at 4 for 6 weeks (target is 5+)
- Win rate drop: rolling win rate fell from 35% to 18% over the last 4 weeks
- Lift stagnation: no adopted experiment in the last 3 weeks produced more than 0.5pp lift
- Cycle time spike: median days from hypothesis to result increased from 14 to 25

**Phase 2 -- Diagnose (triggered by anomaly):**
The agent gathers context: current experiment pipeline status, backlog composition, recent experiment results, learnings database patterns. It queries the `experiment-learnings-database` for relevant historical context. It runs `hypothesis-generation` to produce 3 ranked hypotheses for what to change. Examples:

- "Shift experiments from onboarding (converged at 68% activation, last 3 experiments <1% lift) to feature adoption (untested in 6 weeks, user engagement data shows 40% drop-off at feature X discovery)"
- "Increase minimum detectable effect threshold from 2pp to 4pp -- the last 5 experiments were underpowered because they targeted small effects. Bolder changes will reach significance faster and restore velocity"
- "Replace sequential experiment execution with parallel experiments on non-overlapping surfaces -- current queue depth is 8 hypotheses and cycle time is 21 days, running 2 experiments simultaneously will cut backlog drain time in half"

If the top hypothesis is high-risk (e.g., changing experiment methodology, testing on a high-revenue surface), the agent sends a Slack alert and waits for human approval.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
The agent implements the improvement. For program-level changes (like shifting product area focus or adjusting methodology), it updates the pipeline configuration in n8n and Attio. For product-level experiments, it creates the PostHog experiment with feature flags, implements the variant, and sets duration based on sample size calculation.

Guardrails:
- Maximum 1 active experiment per product surface at a time
- Maximum 2 experiments running simultaneously across different surfaces
- If primary metric drops >30% at any point during an experiment, auto-revert immediately
- Never run experiments on surfaces where an experiment reverted in the last 7 days (cooldown)

**Phase 4 -- Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` on the results:
- **Adopt:** Roll out the winning variant to 100%. Monitor for 7 days to confirm sustained lift. Log the result in the learnings database. Update cumulative lift metrics.
- **Iterate:** The result is directionally interesting but not significant. Generate a new hypothesis building on this finding. Return to Phase 2.
- **Revert:** The variant hurt performance. Disable the feature flag. Log the failure in the learnings database with detailed context so this approach is not retried.
- **Extend:** Insufficient data. Keep the experiment running for another cycle.

All decisions are logged in Attio with full context: hypothesis, variants, results, confidence, reasoning, and the historical evidence that informed the hypothesis.

**Phase 5 -- Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net metric change from all adopted changes this week
- Convergence status per product area
- Current distance from estimated local maximum per area
- Recommended focus for next week
- Learnings database highlights: patterns emerging from recent experiments

Post to Slack and store in Attio.

### 2. Deploy the experiment portfolio health monitor

Run the `autonomous-optimization` drill with Durable-level configuration:

- **Health check frequency:** weekly (Monday 08:00 UTC)
- **Velocity monitoring:** alerts if no experiment completed in 10+ days (stricter than Scalable's 14-day threshold)
- **Backlog monitoring:** alerts if fewer than 3 hypotheses queued (automatic trigger to generate more)
- **Coverage monitoring:** flags product areas with no experiment in 60+ days (stricter than Scalable's 90 days)
- **Convergence tracking:** per-area analysis of diminishing returns across the last 3 winning experiments

The health monitor feeds signals directly into the autonomous optimization loop. When it detects a stall, empty backlog, or coverage gap, that becomes an anomaly in Phase 1 that the loop diagnoses and acts on.

### 3. Maintain the experiment learnings database

Run the `experiment-learnings-database` drill to create and maintain the cumulative knowledge base:

- **After every experiment:** log the structured record (hypothesis, results, decision, key learning, transferable insight, related experiments)
- **Every 5 experiments:** run pattern extraction to update "what works" and "what doesn't" for each product area
- **Before every hypothesis generation:** query the database for related experiments and patterns. The pre-hypothesis check prevents the agent from retesting failed approaches and biases it toward historically effective change types.
- **Quarterly:** full pattern refresh and experimentation retrospective

At Durable level, this database becomes the agent's institutional memory. Over 6 months and 20+ experiments, the database accumulates enough evidence to substantially improve hypothesis quality. Early experiments may have a 25-35% win rate. By month 6, hypothesis quality should push the win rate above 40% because the agent knows what works for this specific product.

### 4. Configure testing-program-specific guardrails

In addition to the standard `autonomous-optimization` guardrails:

- **Velocity floor:** If experiment velocity drops below 3/month for 2 consecutive months, pause optimization and flag for strategic review (the testing program may be blocked by engineering capacity, not hypothesis quality)
- **Win rate ceiling alert:** If win rate exceeds 60% for 4 consecutive weeks, the agent is testing changes that are too safe. Trigger a hypothesis generation run targeting bolder, higher-risk changes.
- **Cumulative lift verification:** Every 30 days, verify that the cumulative claimed lift matches actual metric movements in PostHog. If there is a >20% discrepancy (lifts are not additive due to interaction effects), recalibrate the impact model.
- **Budget cap:** Anthropic API spend for hypothesis generation + experiment evaluation must not exceed $50/mo without human approval.

### 5. Detect convergence and manage local maxima

The autonomous optimization loop monitors for convergence per product area:

- Track the lift of the last 3 winning experiments in each area
- If lifts are declining (e.g., +4pp, +1.5pp, +0.3pp), the area is converging
- If 3 consecutive experiments produce <2% lift, declare the area converged

When an area converges:
1. Reduce experiment frequency to monthly maintenance checks
2. Shift experimentation resources to unconverged areas
3. Generate a convergence report: current performance, total improvement since program start, recommended strategic changes for further gains (product redesigns, new features, new user segments that require different approaches)

Full convergence (all tested product areas converged) triggers a shift to maintenance mode:
- The experiment pipeline continues at reduced pace (1-2 experiments/month for verification)
- The autonomous optimization loop monitors for external disruptions (product changes, competitor moves, traffic pattern shifts) that could break convergence
- Weekly briefs shift from "optimization" to "surveillance" mode

### 6. Evaluate sustainability

After 6 months, measure:
- Experiment velocity: maintained at 4+ experiments/month during active optimization
- Win rate trend: improving over time (learnings database effect)
- Cumulative lift: measurable, sustained improvement across primary metrics
- Convergence: at least 1 product area reached local maximum
- AI lift: measurable improvement attributable to autonomous optimization vs. the manual Scalable approach
- Program ROI: total revenue impact of adopted experiments vs. total program cost (tools + API + time)

This level runs continuously. Review monthly: what improved, what converged, what external factors changed.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations, guardrails)
- 10 hours: set up experiment portfolio health monitor with Durable-level thresholds
- 10 hours: initialize and configure the experiment learnings database
- 80 hours: ongoing monitoring, hypothesis review, guardrail management, convergence analysis (~3 hours/week)
- 20 hours: monthly strategic reviews, convergence reports, stakeholder communication
- 10 hours: documentation, maintenance mode setup, final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, anomaly detection, dashboards, event tracking | Free up to 1M events/mo; paid from $0.00005/event -- [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation, experiment evaluation, pattern extraction, weekly briefs | ~$20-50/mo at Durable volume ($3/$15 per 1M input/output tokens) -- [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| n8n | Autonomous optimization loop, pipeline automation, health monitoring | Self-hosted free; cloud from EUR20/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Loops | Email-based experiment variants (subject line tests, nurture flow experiments) | $49/mo for up to 5K contacts -- [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app experiment variants (message copy, tooltip placement, tour flow experiments) | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated play-specific cost: $120-350/mo** (Anthropic API for autonomous optimization + n8n cloud + Loops + Intercom)

## Drills Referenced

- `autonomous-optimization` -- the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for each product area
- `autonomous-optimization` -- monitors program health including velocity, win rates, coverage gaps, and convergence signals; feeds anomalies to the optimization loop
- `experiment-learnings-database` -- cumulative knowledge base of experiment outcomes and patterns; queried before every hypothesis to prevent repeated failures and improve hypothesis quality over time
