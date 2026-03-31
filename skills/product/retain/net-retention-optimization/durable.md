---
name: net-retention-optimization-durable
description: >
  Net Retention Optimization — Durable Intelligence. Always-on AI agents find the local
  maximum for each NDR component. Autonomous optimization loop detects metric drift,
  generates hypotheses, runs experiments, and auto-implements winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "Ongoing (20 hours setup, then autonomous)"
outcome: "NDR >=115% sustained for 3+ months with autonomous optimization"
kpis: ["Net dollar retention", "Gross retention rate", "Experiment velocity", "Experiment win rate", "Component convergence status", "Intervention save rate", "AI lift vs. Scalable baseline"]
slug: "net-retention-optimization"
install: "npx gtm-skills add product/retain/net-retention-optimization"
drills:
  - autonomous-optimization
  - ndr-health-monitor
  - nps-feedback-loop
---

# Net Retention Optimization — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Always-on AI agents finding the local maximum for every NDR component. The `autonomous-optimization` drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners. The `ndr-health-monitor` drill feeds it NDR-specific intelligence: which component is degrading, which segments are affected, and what has worked historically. The `nps-feedback-loop` drill captures qualitative signals that quantitative data misses.

The system converges when successive experiments on a component produce <2% improvement for 3 consecutive experiments. At convergence, monitoring frequency reduces and the agent shifts focus to the next component with room for improvement. The play is durable when NDR sustains at >=115% for 3+ months with the agent handling optimization autonomously.

## Leading Indicators

- Autonomous optimization loop fires at least 2 experiments per month per active NDR component
- NDR health monitor emits daily health signals with per-component status
- At least 50% of experiments produce a statistically significant result (not all inconclusive)
- Intervention save rate improves quarter over quarter (the agent is learning what works)
- Weekly optimization briefs are generated and contain actionable recommendations
- NPS trends stable or improving (retention interventions are not annoying users)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with the net-retention-optimization play configuration:

**Phase 1 — Monitor (daily via n8n cron):**
The drill uses `posthog-anomaly-detection` to check all NDR-related KPIs daily. It compares the last 2 weeks against the 4-week rolling average and classifies: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). For NDR, the monitored metrics are:
- Revenue churn rate (weekly, annualized)
- Contraction MRR rate
- Expansion MRR rate
- Intervention save rate (from health-score-alerting)
- Upgrade conversion rate (from upgrade-prompt)

If anomaly detected, Phase 2 triggers automatically.

**Phase 2 — Diagnose (triggered by anomaly):**
The drill gathers context from the `ndr-health-monitor` (step 2 below), pulls 8-week metric history from PostHog, and runs `hypothesis-generation` with Claude. It receives 3 ranked hypotheses with expected impact and risk levels.

Example hypotheses the agent might generate for NDR:
- "Churn save rate dropped because intervention emails are going to spam — switch to in-app-only for High risk tier" (low risk)
- "Expansion stalled because upgrade prompts fire too early in the usage curve — delay trigger from 80% to 90% of plan limit" (medium risk)
- "Contraction surged in the starter-plan cohort — offer an annual discount at the moment of downgrade intent" (medium risk)

If risk = "high", the agent sends a Slack alert for human review and stops. Otherwise, it proceeds to Phase 3.

**Phase 3 — Experiment:**
The agent creates a PostHog feature flag to split traffic between control and variant. It implements the variant using the appropriate fundamental (Loops for email changes, Intercom for in-app changes, PostHog for behavioral targeting changes). Minimum experiment duration: 7 days or 100+ samples per variant, whichever is longer.

**Phase 4 — Evaluate:**
After the experiment completes, the agent runs `experiment-evaluation`. Decision: Adopt (implement winner), Iterate (new hypothesis building on this result), Revert (restore control), or Extend (keep running). All decisions logged in Attio.

**Phase 5 — Report (weekly):**
Aggregates all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made. Calculates net impact on NDR. Posts the weekly optimization brief to Slack and stores in Attio.

**Guardrails (CRITICAL):**
- Maximum 1 active experiment per NDR component at a time
- If any NDR component drops >30% during an experiment, auto-revert immediately
- Human approval required for: intervention frequency changes affecting >50% of users, pricing-related experiments, any change flagged as high risk
- Cooldown: 7 days after a revert before testing the same variable again
- Maximum 4 experiments per component per month. All 4 fail = pause and flag for human review.

### 2. Deploy the NDR health monitor

Run the `ndr-health-monitor` drill to feed the optimization loop with NDR-specific intelligence:

1. **Daily signal pipeline:** Computes rolling 7-day NDR components (annualized), compares against 30-day averages, classifies each component as Normal/Watch/Alert, and emits `ndr_health_signal` events to PostHog
2. **Intervention effectiveness tracking:** Creates PostHog cohorts for each intervention type (churn prevention, upgrade prompt, health alert) and tracks 30-day and 90-day outcomes. Computes save rates and expansion rates per intervention type.
3. **Component drift detection:** Analyzes 14-day trend for each NDR component. When a component enters "Degrading" status (3+ consecutive days worsening), generates a context package for the `autonomous-optimization` drill's hypothesis generation: degrading component, affected segments, recent intervention effectiveness, historical experiment results.
4. **Convergence detection:** After each adopted experiment, tracks the measured NDR impact. When the last 3 consecutive experiments on a component produce <2% improvement, the component has reached its local maximum. Monitoring frequency reduces from daily to weekly. The agent shifts focus to the next underperforming component.
5. **Weekly NDR optimization brief:** Synthesized by Claude with component health, experiment status, intervention effectiveness, convergence status, and recommended focus. Posted to Slack and stored in Attio.

### 3. Launch the NPS feedback loop

Run the `nps-feedback-loop` drill to capture qualitative signals:

1. Deploy NPS surveys via Intercom at key milestones: after 30 days of active use, after completing a major workflow, and quarterly for long-term customers
2. Cross-reference NPS scores with health scores and risk tiers in PostHog. Detractors with declining health scores are highest-priority for intervention.
3. Route promoter responses to the expansion pipeline — promoters who are not on the highest plan are upgrade candidates
4. Feed detractor themes into the `autonomous-optimization` loop as qualitative context for hypothesis generation. If 30%+ of detractors cite the same issue, that issue becomes a prioritized hypothesis.
5. Track NPS by segment monthly. A declining NPS in a specific segment is an early warning even if their NDR has not moved yet.

**Human action required:** Review detractor follow-up responses monthly. The NPS feedback loop can automate responses, but detractor themes should inform product roadmap decisions that are beyond the optimization agent's scope.

### 4. Monitor convergence and sustainability

The system runs autonomously. Check monthly:

- **Convergence progress:** How many NDR components have reached their local maximum? When all three (churn, contraction, expansion) converge, NDR is fully optimized under current conditions.
- **AI lift:** Compare current NDR to the Scalable-level baseline. The difference is the AI lift — the value the autonomous optimization adds.
- **Intervention fatigue:** Are save rates declining over time? If so, the agent may be over-messaging. Reduce intervention frequency or refresh messaging templates.
- **NPS correlation:** Is NPS stable or improving? If NPS declines while NDR improves, the agent may be saving revenue through aggressive tactics that hurt user sentiment. Adjust guardrails.

When all components converge:
1. The play has reached its local maximum
2. Reduce optimization loop frequency to weekly monitoring with monthly experiments
3. Log the final optimized NDR and component values
4. Report: "NDR optimization has converged at [X%]. Churn component: [Y%], Contraction: [Z%], Expansion: [W%]. Further gains require strategic changes (new pricing model, new product features, new market segment) rather than tactical optimization."

### 5. Evaluate against threshold

NDR >=115% sustained for 3+ months with the autonomous optimization loop handling experiments. This level runs continuously. Monthly review: what improved, what converged, what new experiments to run.

If NDR drops below 115% after sustained performance, the agent should diagnose: external factor (market shift, competitor move) or internal degradation (feature regression, support quality decline). External factors may require a strategic pivot. Internal degradation should trigger a new round of optimization experiments.

## Time Estimate

- 8 hours: configure autonomous optimization loop with NDR-specific parameters
- 6 hours: deploy NDR health monitor and verify daily signals
- 4 hours: launch NPS feedback loop and connect to optimization pipeline
- 2 hours: validate end-to-end flow (anomaly -> hypothesis -> experiment -> evaluation -> report)
- Ongoing: 1-2 hours/month reviewing optimization briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | NDR tracking, experiments, feature flags, cohort analysis, anomaly detection | Free up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app interventions, NPS surveys, expansion prompts | From $99/mo (Advanced) for targeting and surveys — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered retention emails, intervention follow-ups | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Anthropic API (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$0.01-0.05/optimization cycle ($3/$15 per 1M input/output tokens) — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated cost for Durable: $150-400/mo** (Intercom Advanced + Loops + ~$20-50/mo Anthropic API for daily monitoring + weekly briefs)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `ndr-health-monitor` — NDR-specific monitoring that feeds the optimization loop: daily component health signals, intervention effectiveness tracking, drift detection, convergence detection, and weekly NDR optimization briefs
- `nps-feedback-loop` — captures qualitative signals via NPS surveys, routes detractor themes to the optimization pipeline, tracks sentiment alongside retention metrics
