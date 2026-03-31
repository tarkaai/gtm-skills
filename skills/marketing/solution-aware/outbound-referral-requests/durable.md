---
name: outbound-referral-requests-durable
description: >
  Outbound Referral Requests — Durable Intelligence. Always-on AI agents continuously optimize
  referral ask messaging, connector selection, target prioritization, and ask timing. The
  autonomous-optimization drill runs the core loop: detect metric anomalies in referral
  performance -> generate improvement hypotheses -> run A/B experiments -> evaluate results ->
  auto-implement winners. Converges when successive experiments produce <2% improvement.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained referral rate (>=12%) and >=30 qualified intros/month over 12 months via autonomous connector portfolio optimization, ask experimentation, and relationship health management"
kpis: ["Sustained intro rate", "Agent experiment win rate", "Connector portfolio health score", "Intro-to-meeting rate trend", "Cost per qualified intro"]
slug: "outbound-referral-requests"
install: "npx gtm-skills add marketing/solution-aware/outbound-referral-requests"
drills:
  - autonomous-optimization
  - partner-relationship-scoring
---

# Outbound Referral Requests — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

The outbound referral system runs autonomously. AI agents continuously monitor referral performance, detect when intro rates plateau or decline, experiment with improved ask messaging, connector selection strategies, target prioritization, and ask timing, then auto-implement winners. The `autonomous-optimization` drill runs the core loop: detect metric anomalies -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement, indicating the referral play has reached its local maximum for your network and market.

## Leading Indicators

- Autonomous optimization loop running daily, generating at least 1 experiment per month
- Intro rate trending stable or upward above 12% for 3+ consecutive months
- Weekly optimization briefs generating and posting to Slack
- At least 1 experiment adopted in the first month (ask variant, timing change, connector routing change)
- Connector portfolio health score stable or improving (no net decline in Tier 1-2 connectors)
- Convergence detection active — system can identify when optimization has plateaued
- Intro-to-meeting rate stable or improving (indicates intro quality is not degrading)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the outbound referral requests play. This creates the always-on agent loop with 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks referral play KPIs daily using `posthog-anomaly-detection`:
- Request-to-intro rate (trailing 2-week vs 4-week average)
- Intro-to-meeting rate
- Average days from ask to intro
- Connector response rate by tier
- Ask variant performance (current A vs B)
- Connector portfolio health (% of asks going to Tier 1-2 vs Tier 3-4)
- Target coverage (% of target accounts with at least 1 viable intro path)

Classify each metric: normal (within +/-10% of 4-week average), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current ask templates, connector distribution, target selection criteria, recent interaction history) and 8-week metric history from PostHog. Runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples of referral-specific hypotheses:

- "Intro rate dropped because we exhausted Tier 1 connectors — 70% of recent asks went to Tier 3 connectors with historically low response rates. Hypothesis: pause Tier 3 asks, recruit 10 new Tier 1-2 connectors via Crossbeam overlap analysis."
- "Ask-to-intro time increased from 4 days to 9 days. Hypothesis: the current ask message is too long (average 120 words vs target 100 words). Shorten the ask and test whether faster reads produce faster action."
- "Intros from advisor connectors dropped 40% this month. Hypothesis: advisor network fatigue — same advisors are being asked every 2 weeks. Increase cooldown period from 2 weeks to 4 weeks for advisors."
- "Intro-to-meeting rate dropped from 60% to 35%. Hypothesis: the forwardable blurb is not compelling to the target. Test a new blurb format that leads with a specific data point relevant to the target's company."
- "Tuesday asks convert at 18% vs Thursday asks at 8%. Hypothesis: connectors are more responsive early in the week. Shift 80% of ask volume to Tuesday-Wednesday."

Store hypotheses in Attio. If risk = "high" (e.g., changing connector frequency caps, removing connectors from the portfolio), send Slack alert for human review. If risk = "low" or "medium", proceed automatically.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment using PostHog feature flags:

- **Ask message experiments**: Create a variant ask template. Split new asks between control (current template) and variant. Measure request-to-intro rate after 50+ asks per group.
- **Blurb experiments**: Create a variant forwardable blurb. Split asks between control and variant blurb. Measure intro-to-meeting rate after 20+ intros per group.
- **Timing experiments**: Shift ask sending days/times for the variant group. Measure response rate and response speed.
- **Connector routing experiments**: Change the connector selection algorithm for the variant group (e.g., weight industry proximity higher, or route targets to connectors who have made intros to similar companies). Measure intro rate.
- **Frequency cap experiments**: Adjust the connector frequency cap for the variant group (e.g., 3 asks/month vs 2 asks/month for Tier 1 connectors). Measure connector response rate and willingness trend.

Minimum experiment duration: 14 days or 50 asks per variant, whichever is longer. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt:** Variant outperforms control by 5%+ with statistical confidence. Update the live configuration. Log the change.
- **Iterate:** Results inconclusive. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Control outperforms variant. Disable variant. Log the failure. Return to Phase 1.
- **Extend:** Insufficient data. Run for another period.

Store full evaluation in Attio with decision, confidence, reasoning.

**Phase 5 — Report (weekly via n8n cron):**
Generate weekly optimization brief:
```
## Referral Optimization Brief — Week of {date}

### Anomalies Detected
- {metric}: {classification} ({value} vs {4-week avg})

### Experiments Active
- {experiment_name}: {status}. {days remaining or results}

### Decisions Made
- {experiment_name}: {decision}. Net impact: {metric change}

### Referral Funnel Health
| Metric | This Week | 4-Week Avg | Trend |
|--------|-----------|------------|-------|
| Asks sent | {n} | {n} | {up/down/flat} |
| Intros received | {n} | {n} | {up/down/flat} |
| Request-to-intro rate | {pct}% | {pct}% | {up/down/flat} |
| Meetings booked | {n} | {n} | {up/down/flat} |
| Intro-to-meeting rate | {pct}% | {pct}% | {up/down/flat} |

### Connector Portfolio Health
| Tier | Active | Avg Response Rate | Avg Intros/Month | Trend |
|------|--------|-------------------|-------------------|-------|
| Tier 1 | {n} | {pct}% | {n} | {up/down/flat} |
| Tier 2 | {n} | {pct}% | {n} | {up/down/flat} |
| Tier 3 | {n} | {pct}% | {n} | {up/down/flat} |

### Top Connectors This Week
1. {connector}: {intros} intros, {meetings} meetings
2. {connector}: {intros} intros, {meetings} meetings

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Estimated distance from local maximum: {assessment}

### Recommended Focus Next Week
- {recommendation based on data}
```

Post to Slack and store in Attio.

Estimated time for setup: 15 hours. Then always-on.

### 2. Deploy warm intro performance reporting

Run the `autonomous-optimization` drill to build the monitoring and reporting layer specific to this play:

1. Build a PostHog dashboard "Warm Intros — Partner Performance" with per-connector intro volume, request-to-intro conversion, intro-to-meeting conversion, and full funnel visualization
2. Create partner performance cohorts: high-converting connectors, volume connectors, declining connectors, new connectors, dormant connectors
3. Build the weekly warm intro brief (Friday 3pm via n8n): per-connector metrics, ask template insights, and recommended actions
4. Maintain per-connector ROI fields in Attio (total asks, intros, meetings, rates, last activity, health score)
5. Configure performance alerts: connector intro rate drops below 20% for 2 weeks, new connector delivers first intro within 48 hours, total weekly meetings drop below Scalable baseline

This data feeds directly into the `autonomous-optimization` drill's anomaly detection.

Estimated time: 10 hours setup, then always-on.

### 3. Continuous connector portfolio optimization

Continue running the `partner-relationship-scoring` drill from Scalable. At Durable level, enhance it:

- **Proactive connector recruitment**: When the optimization loop detects that intro rate is dropping due to connector fatigue (declining Tier 1-2 pool), automatically trigger a Crossbeam overlap analysis to identify new potential connectors. Generate a brief for the founder: "Your Tier 1 connector pool dropped from 15 to 11 this quarter. Here are 8 Crossbeam-sourced connectors who overlap with 5+ of your target accounts. Recommend recruiting these via personal outreach."
- **Connector relationship health tracking**: Monitor the trajectory of each connector's scores over time. If a Tier 1 connector shows declining response rates over 3 consecutive months, flag for relationship repair — the agent drafts a "check in" message (no ask, just relationship maintenance) and schedules it.
- **Network expansion signals**: Detect when a connector changes jobs, joins a board, or is promoted — these events create new intro paths to companies they just joined. Clay enrichment runs monthly to detect job changes. When a connector joins a target account's company, flag as a high-priority intro opportunity.
- **Seasonal pattern detection**: Track connector response rates by month. Some connectors are more responsive in Q1 vs Q4 (budget cycles, travel schedules). Use seasonal patterns to optimize ask timing.

Estimated time: 8 hours enhancement, then always-on.

### 4. Guardrails (CRITICAL)

The autonomous optimization loop must respect these constraints:

- **Rate limit**: Maximum 1 active experiment per optimization variable at a time. Never test ask message changes and timing changes simultaneously — you cannot isolate the variable that caused the result.
- **Revert threshold**: If request-to-intro rate drops >25% during any experiment, auto-revert immediately and alert the founder.
- **Human approval required for:**
  - Changing connector frequency caps (affects relationship health)
  - Removing connectors from the active portfolio (relationship risk)
  - Changing the composite scoring formula (affects which pairs get prioritized)
  - Any experiment the hypothesis generator flags as "high risk"
  - Budget changes >20% (e.g., upgrading Crossbeam tier)
- **Cooldown**: After a failed experiment, wait 14 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Connector protection**: Never auto-send asks to a connector who has explicitly declined a previous ask or expressed annoyance. These connectors require manual relationship repair before re-entering the pipeline.
- **Never optimize what is not measured**: If a new connector type (e.g., customer success managers) enters the pipeline without PostHog tracking configured, fix tracking first before including them in experiments.

### 5. Convergence detection

The optimization loop runs indefinitely but should detect convergence — when the referral system has reached its local maximum:

- Track the improvement percentage of each successive adopted experiment
- When 3 consecutive experiments produce <2% improvement on their target metric, declare convergence for that variable
- At convergence for all variables (ask messaging, timing, connector routing, blurb format):
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency to 1 per quarter (maintenance mode)
  3. Report: "Referral requests are optimized. Current performance: {intro rate}% intro rate, {intros/month} intros/month, {meeting rate}% intro-to-meeting rate. Connector portfolio: {tier1} Tier 1, {tier2} Tier 2. Further gains require strategic changes (new market, new connector sources, product positioning changes) rather than tactical optimization."
- Continue watching for events that break convergence: connector job changes, market shifts, new competitors, seasonal patterns

### 6. Evaluate sustainability

Measure against threshold: Sustained referral rate (>=12%) and >=30 qualified intros/month over 12 months.

Monthly review checklist:
- Intro rate: Still >=12%? Trending up, flat, or down?
- Monthly intro volume: Still >=30? Pipeline sufficient to sustain?
- Intro-to-meeting rate: Quality holding?
- Connector portfolio: Net growth or shrinkage in Tier 1-2 connectors?
- Autonomous optimization: Experiments running and producing results?
- Cost efficiency: Cost per qualified intro trending down or stable?
- Connector satisfaction: Any relationship damage signals?

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay, the autonomous optimization loop diagnoses whether the issue is connector fatigue, target exhaustion, market shift, or model drift, and either self-corrects or escalates to the founder.

## Time Estimate

- Autonomous optimization setup: 15 hours
- Warm intro performance reporting setup: 10 hours
- Connector portfolio optimization enhancement: 8 hours
- Ongoing monitoring, experiment review, and strategic oversight: ~147 hours over 12 months (~3 hours/week)

**Total: ~180 hours over 12 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector portfolio, referral pipeline, experiment logs, scoring fields | Standard stack (excluded) |
| PostHog | Dashboards, funnels, feature flags, experiments, anomaly detection | Standard stack (excluded) |
| n8n | Orchestration — optimization loop, performance reporting, pipeline automation | Standard stack (excluded) |
| Clay | Monthly network enrichment, job change detection, connector-target scoring | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Crossbeam | Partner account mapping for connector recruitment | Connector: $400/mo. [crossbeam.com/pricing](https://www.crossbeam.com/pricing) |
| Loops | Automated ask delivery via email | Pro: $49/mo at Durable volume. [loops.so/pricing](https://loops.so/pricing) |
| Anthropic API | Claude for optimization loop (hypothesis generation, experiment evaluation, weekly briefs, ask copywriting) | ~$50-100/mo at Durable volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$994-1,044/mo** (Clay $495 + Crossbeam $400 + Loops $49 + Anthropic ~$50-100)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor referral metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — per-connector dashboards, performance cohorts, weekly briefs, ROI tracking, and alert system feeding the optimization loop
- `partner-relationship-scoring` — enhanced at Durable with proactive connector recruitment, relationship health tracking, network expansion signals, and seasonal pattern detection
