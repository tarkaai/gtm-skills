---
name: viral-loop-design-durable
description: >
  Built-In Virality — Durable Intelligence. Always-on AI agents monitor viral health, detect decay
  signals, generate optimization hypotheses, run experiments, and auto-implement winners. The viral
  loop converges on its local maximum and self-maintains as conditions change.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Viral coefficient ≥0.4 sustained or improving over 6 months via autonomous optimization"
kpis: ["Viral coefficient (K)", "Invites sent per active user", "Invite-to-signup conversion rate", "Experiment velocity (tests/month)", "AI lift (cumulative improvement from auto-implemented changes)"]
slug: "viral-loop-design"
install: "npx gtm-skills add product/referrals/viral-loop-design"
drills:
  - autonomous-optimization
  - viral-coefficient-monitor
---

# Built-In Virality — Durable Intelligence

> **Stage:** Product → Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The viral loop runs on autopilot. AI agents continuously monitor viral health metrics, detect when K-factor plateaus or decays, generate hypotheses for improvement, run A/B experiments, and auto-implement winners. The system finds the local maximum of viral performance and sustains it as user behavior, competitive landscape, and product features evolve. Human intervention is only required for high-risk changes (audience targeting shifts, budget changes >20%, or strategic pivots).

## Leading Indicators

- Autonomous optimization loop runs without intervention for 4+ consecutive weeks
- Experiments produce measurable lifts (>2% improvement in target metric) at least twice per month
- Viral coefficient remains within ±10% of its 4-week rolling average (stability)
- Weekly optimization briefs are generated and posted automatically
- Channel-level decay signals are detected and addressed before they materially impact overall K
- Convergence detection identifies when successive experiments produce <2% improvement

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the viral loop play. The drill creates the always-on cycle:

**Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check viral KPIs: K-factor, invite volume, invite-to-signup conversion, referee activation rate
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal, log to Attio and take no action
- If anomaly detected, trigger the Diagnose phase

**Diagnose (triggered by anomaly):**
- Pull current viral configuration from Attio: active surfaces, reward structure, gamification settings, channel mix
- Pull 8-week metric history from PostHog viral dashboard
- Run Claude hypothesis generation with anomaly data + context
- Receive 3 ranked hypotheses with expected impact and risk levels
- Store hypotheses in Attio as notes on the play's campaign record
- If top hypothesis is high-risk (affects >50% of traffic or changes reward economics), send Slack alert for human review and STOP
- If low or medium risk, proceed to Experiment

**Experiment (triggered by hypothesis acceptance):**
- Take top-ranked hypothesis
- Use PostHog experiments to create a feature flag splitting traffic between control and variant
- Implement the variant (e.g., new invite copy via Intercom, new landing page layout, adjusted reward timing via Loops)
- Run for minimum 7 days or 100+ samples per variant
- Log experiment start in Attio: hypothesis, start date, duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run Claude experiment evaluation with control vs. variant data
- Decision: Adopt (implement winner), Iterate (new hypothesis), Revert (restore control), or Extend (more data needed)
- Store full evaluation in Attio: decision, confidence, reasoning, net impact

**Report (weekly via n8n cron):**
- Aggregate optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate weekly optimization brief: what changed, why, net impact on K and conversion rates, distance from estimated local maximum, recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy viral-specific health monitoring

Run the `viral-coefficient-monitor` drill. This creates the viral-specific signal detection layer:

**Daily viral health checks:**
- Primary metrics monitored: K-factor (rolling 7-day), invite volume, invite-to-signup conversion, referee activation rate
- Secondary metrics monitored weekly: channel-level K, loop depth, time-to-share, referrer concentration
- Decay signals triggering immediate investigation: K below threshold for 7 days, conversion drop >25% WoW, active referrer count drop >30% MoM, zero loop-close events for 14 days

**Weekly viral health report:**
- K-factor with WoW change and status
- Top performing channels with K and volume
- Signals: warnings, critical alerts, or all-clear
- Auto-generated recommendation: no action, investigate specific metric, optimize specific channel

**Channel decay detection:**
- Isolates platform-specific problems (email deliverability, social algorithm changes) from product-wide viral decay
- Compares each channel's 2-week conversion against its 8-week rolling average
- Flags channels with >20% decline for targeted investigation

**Referrer pipeline health:**
- New referrers this month vs. lapsed referrers vs. churned referrers
- Alerts when new referrer growth falls below replacement rate for 2 consecutive weeks

### 3. Configure guardrails

The autonomous loop operates within strict boundaries:

- **Rate limit:** Maximum 1 active experiment on the viral loop at a time. Never stack experiments.
- **Revert threshold:** If K drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for:** reward structure changes affecting cost per referral by >20%, targeting changes affecting >50% of users, any change flagged as high risk.
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Budget guardrail:** If referral reward cost per acquired user exceeds 2x the organic CAC, pause reward experiments and review economics.

### 4. Monitor for convergence

The optimization loop detects convergence — when the viral loop has reached its local maximum:

- Track the cumulative improvement from adopted experiments over rolling 3-month windows
- If 3 consecutive experiments produce <2% improvement each, the loop has converged
- At convergence: reduce monitoring from daily to weekly, generate a convergence report ("Viral loop is optimized at K=[value]. Further gains require strategic changes: new mechanic types, new sharing channels, or product changes."), and notify the team

### 5. Evaluate sustainability

**Pass threshold:** Viral coefficient ≥0.4 sustained or improving over 6 consecutive months via autonomous optimization.

Also verify:
- The autonomous loop has run for 6 months without requiring manual intervention more than once per month
- At least 8 experiments were run, with at least 3 producing adopted improvements
- AI lift is measurable: current K is higher than K at the start of Durable level, or K has been maintained despite external changes (seasonal shifts, competitive pressure, user base growth)
- Weekly optimization briefs have been generated consistently

This level runs continuously. Review monthly: what the autonomous loop changed, what converged, what new strategic experiments to consider.

## Time Estimate

- 20 hours: autonomous optimization loop setup (n8n workflows, PostHog configuration, Claude prompts, Attio logging)
- 15 hours: viral coefficient monitor setup (daily checks, weekly reports, channel detection, referrer tracking)
- 10 hours: guardrail configuration and testing
- 5 hours: convergence detection setup
- 100 hours: ongoing monitoring, brief review, and monthly strategic assessments (spread over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, feature flags | Free tier: 1M events/mo. Paid: usage-based from $0.00005/event. Experiments require paid plan. https://posthog.com/pricing |
| n8n | Daily/weekly cron workflows for monitoring, experiment orchestration, reporting | Community (self-hosted): free. Cloud Pro: ~$60-120/mo for higher execution volume. https://n8n.io/pricing |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, weekly brief generation | API usage-based. Estimate $50-150/mo for daily monitoring + weekly reports. https://anthropic.com/pricing |
| Intercom | Experiment variant delivery (in-app message A/B tests) | Advanced: $85/seat/mo for workflow automation. https://intercom.com/pricing |
| Loops | Experiment variant delivery (email sequence A/B tests), reward emails | Paid from $49/mo. https://loops.so/pricing |
| Attio | Experiment logging, hypothesis storage, optimization audit trail | Free tier available. Paid from $29/seat/mo. https://attio.com/pricing |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `viral-coefficient-monitor` — viral-specific health monitoring: K-factor trends, channel decay detection, referrer pipeline health, and weekly viral health reports
