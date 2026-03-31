---
name: funnel-optimization-durable
description: >
  Conversion Funnel Optimization — Durable Intelligence. Always-on AI agents that autonomously
  detect funnel anomalies, generate improvement hypotheses, run A/B experiments, evaluate
  results, and auto-implement winners. Converges on local maximum with weekly optimization
  briefs and <2% diminishing returns detection.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving funnel conversion over 6 months via autonomous AI optimization, with <2% experiment returns triggering convergence detection"
kpis: ["Funnel conversion rate", "Drop-off reduction", "Experiment velocity", "AI-driven lift", "Convergence detection"]
slug: "funnel-optimization"
install: "npx gtm-skills add product/retain/funnel-optimization"
drills:
  - autonomous-optimization
  - dashboard-builder
  - threshold-engine
---

# Conversion Funnel Optimization — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The funnel optimization system runs autonomously with minimal human intervention. AI agents detect when funnel metrics plateau, drop, or spike. They diagnose the root cause, generate improvement hypotheses, design and deploy A/B experiments, evaluate results, and auto-implement winners. The system finds the local maximum — the best possible funnel conversion given current product, market, and audience — and maintains it as conditions change. When successive experiments produce <2% improvement, the system detects convergence and reports it.

**Pass threshold:** Sustained or improving funnel conversion over 6 months via autonomous AI optimization, with convergence detection active and <2% diminishing returns triggering appropriate mode shift.

## Leading Indicators

- Autonomous optimization loop running daily without human intervention for 4+ consecutive weeks
- At least 2 autonomous experiments per month completed end-to-end (detect > hypothesize > test > evaluate > implement/revert)
- Weekly optimization briefs generated and posted automatically
- Guardrails never breached (no auto-revert due to >30% metric drop, no budget change without approval)
- Convergence detection functioning: system correctly identifies when a funnel has plateaued
- Net positive AI-driven lift: cumulative impact of agent-implemented changes is positive

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for funnel metrics. This is the core of Durable. It creates the always-on cycle:

**Monitor (daily via n8n cron):**
- Check all funnel KPIs using PostHog anomaly detection
- Compare last 2 weeks against 4-week rolling average
- Classify each funnel as: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal: log and continue monitoring
- If anomaly: trigger diagnosis

**Diagnose (triggered by anomaly):**
- Gather context: current funnel configuration, active feature flags, recent experiments, segment performance
- Pull 8-week metric history from PostHog
- Run Claude hypothesis generation with the anomaly data + full context
- Receive 3 ranked hypotheses with expected impact and risk levels
- If top hypothesis is high-risk: alert human via Slack and STOP
- If low/medium risk: proceed to experiment

**Experiment (triggered by accepted hypothesis):**
- Design the experiment: create PostHog feature flag with control/treatment split
- Implement the variant (e.g., change CTA copy, adjust form fields, modify pricing page layout)
- Set duration: minimum 7 days or 100+ samples per variant
- Log experiment start in Attio

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Run Claude experiment evaluation
- Decision: Adopt (implement winner), Iterate (new hypothesis from this result), Revert (restore control), or Extend (more data needed)
- Store full evaluation in Attio

**Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies, hypotheses, experiments, decisions
- Calculate net metric change from all adopted changes
- Generate weekly optimization brief
- Post to Slack and store in Attio

### 2. Configure funnel-specific monitoring

Extend the `autonomous-optimization` drill for Durable-level operation:

**Per-funnel anomaly baselines:**
- Signup funnel: baseline = Scalable-level conversion rate. Anomaly = >10% sustained deviation.
- Activation funnel: baseline = Scalable-level activation rate. Anomaly = >8% deviation (activation is more sensitive).
- Upgrade funnel: baseline = Scalable-level upgrade rate. Anomaly = >15% deviation (lower volume means higher natural variance).

**Per-segment monitoring:**
- The health monitor should track each of the 3 segment variants independently
- A segment-specific regression triggers a segment-specific diagnosis (not a general funnel diagnosis)
- If a segment variant degrades while the general funnel holds, the issue is segment-specific — the agent should investigate segment properties, not the funnel design

**Experiment interaction detection:**
- If 2 experiments are proposed for the same funnel (even different steps), the agent queues the second and runs them sequentially
- If a funnel improvement coincides with an external change (product deploy, marketing campaign change), the agent flags the confound in the evaluation

### 3. Build the optimization dashboard

Extend the `dashboard-builder` drill's Product dashboard with Durable-level panels:

**Autonomous loop health:**
- Days since last autonomous experiment
- Active experiment status (running/evaluating/implementing)
- Agent decision history (last 10 decisions with outcomes)
- Guardrail status (all green = no breaches)

**Convergence tracker:**
- Per-funnel convergence status: "optimizing" (active experiments producing >2% lifts), "converging" (last 2 experiments <2% lift), "converged" (3 consecutive experiments <2% lift)
- Distance from estimated local maximum (based on theoretical ceiling and current rate)
- Time since last significant improvement per funnel

**Cumulative impact:**
- Total AI-driven lift since Durable launch (sum of all adopted experiment lifts)
- Comparison: AI-optimized period vs pre-AI period conversion rates
- Revenue impact estimate: additional conversions * average revenue per conversion

### 4. Implement convergence detection and mode shift

The autonomous optimization loop must detect when it has reached the local maximum for a funnel:

**Convergence criteria:** 3 consecutive experiments on the same funnel produce <2% improvement each.

**When convergence is detected:**
1. The agent reduces monitoring frequency from daily to weekly for that funnel
2. The agent posts to Slack: "Funnel {name} has converged. Current conversion: {X}%. Last 3 experiments produced {Y}%, {Z}%, {W}% lift. Further gains require strategic changes (new channels, product changes, pricing changes) rather than tactical optimization."
3. The agent shifts optimization resources to the next non-converged funnel
4. The converged funnel stays on weekly monitoring — if external changes cause a regression, the agent detects it and re-enters active optimization mode

**De-convergence trigger:** If a converged funnel's conversion drops >10% from its converged baseline for 2 consecutive weeks, re-enter active optimization mode.

### 5. Set up guardrails

The autonomous loop must not cause harm. Configure these guardrails in the n8n orchestration workflow:

- **Rate limit:** Maximum 1 active experiment per funnel. Maximum 3 active experiments total across all funnels.
- **Revert threshold:** If any funnel's primary metric drops >30% during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Changes that affect >50% of traffic (major funnel redesigns)
  - Changes to pricing page or checkout flow (revenue-sensitive)
  - Any hypothesis flagged as "high risk" by Claude
- **Cooldown:** After a reverted experiment, wait 7 days before testing on the same funnel step.
- **Monthly cap:** Maximum 4 experiments per funnel per month. If all 4 fail, pause and flag for human strategic review.
- **Never optimize unmeasured steps:** If a funnel step lacks PostHog tracking, fix instrumentation first.

### 6. Generate monthly strategic reports

Beyond the weekly optimization briefs, produce a monthly strategic analysis:

```markdown
# Monthly Funnel Optimization Report — {Month}

## Executive Summary
{3 sentences: overall funnel health, biggest win this month, current convergence status}

## Funnel Performance
| Funnel | Current CVR | Month Ago | 3 Months Ago | Trend | Status |
|--------|------------|-----------|--------------|-------|--------|
| Signup | | | | | optimizing/converging/converged |
| Activation | | | | | |
| Upgrade | | | | | |

## Autonomous Experiments This Month
| Experiment | Funnel | Hypothesis | Result | Decision | Lift |
|-----------|--------|-----------|--------|----------|------|

## Segment Performance
{Per-segment conversion with trends, any segment that diverged significantly}

## Convergence Analysis
{Which funnels are converging, estimated distance to local maximum, strategic recommendations for breaking through the ceiling}

## Recommendations
1. {Strategic recommendation with data backing — for human decision-making}
2. {Strategic recommendation}
```

### 7. Evaluate sustainability

This level runs continuously. Evaluate quarterly:

- Are funnel conversion rates sustained or improving vs 6 months ago?
- Is the autonomous loop producing net-positive changes? (More wins than reversions)
- Are the weekly briefs actionable and accurate?
- Has convergence been correctly detected and acted upon?
- What is the total revenue impact of AI-driven optimizations?

If all pass: the play is durable. If any degrades, use the agent's own analytical outputs to diagnose and correct.

## Time Estimate

- 20 hours: Configure autonomous optimization loop (n8n workflows, Claude prompts, guardrails)
- 15 hours: Extend monitoring for per-funnel/per-segment Durable-level operation
- 10 hours: Build convergence detection and mode-shift logic
- 10 hours: Build Durable dashboard panels and monthly report automation
- 5 hours: Guardrail testing and validation (deliberately trigger each guardrail to confirm it works)
- 50 hours: Ongoing monitoring, brief review, strategic adjustments over 6 months
- 20 hours: Quarterly evaluations, prompt tuning, experiment quality review
- 20 hours: Human review of agent proposals, approving high-risk experiments, strategic decisions

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, experiments, feature flags, session recordings, dashboards | Growth ~$100-300/mo at scale — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Autonomous optimization workflows, monitoring, reporting | Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | Agent-triggered in-app messages, segment-specific guidance | Essential $39/seat/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Agent-managed lifecycle sequences | Growth from $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Claude API | Hypothesis generation, experiment evaluation, report generation, convergence analysis | ~$30-60/mo — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** ~$300-550/mo (PostHog at scale + n8n + Intercom + Loops + Claude API)

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: monitor > diagnose > experiment > evaluate > implement. Finds the local maximum and detects convergence.
- `autonomous-optimization` — Extended for Durable with per-funnel/per-segment monitoring and convergence-aware alerting
- `dashboard-builder` — Durable-level dashboard with autonomous loop health, convergence tracking, and cumulative impact
- `threshold-engine` — Continuous evaluation of sustainability over 6 months
