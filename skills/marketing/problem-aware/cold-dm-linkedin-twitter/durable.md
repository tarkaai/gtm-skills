---
name: cold-dm-linkedin-twitter-durable
description: >
  Cold DMs on LinkedIn/Twitter — Durable Intelligence. Always-on AI agents monitor DM outreach
  metrics, detect anomalies, generate improvement hypotheses, run A/B experiments, and auto-implement
  winners. The autonomous-optimization loop finds the local maximum of DM performance.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Social"
level: "Durable Intelligence"
time: "20 hours setup + 5 hours/month ongoing"
outcome: "Meeting rate sustained at or above Scalable baseline (>=1.5%) for 6 months via autonomous optimization. Converges when 3 consecutive experiments produce <2% improvement."
kpis: ["Meeting rate (rolling 4-week)", "Reply rate by channel (rolling 4-week)", "Cost per meeting trend", "Experiment win rate", "Optimization cycle count"]
slug: "cold-dm-linkedin-twitter"
install: "npx gtm-skills add marketing/problem-aware/cold-dm-linkedin-twitter"
drills:
  - autonomous-optimization
  - signal-detection
---

# Cold DMs on LinkedIn/Twitter — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Social

## Outcomes

Deploy an always-on AI agent loop that continuously optimizes the cold DM play. The agent monitors performance metrics, detects when reply rates or meeting rates plateau or drop, generates hypotheses for improvement, runs controlled experiments, evaluates results, and auto-implements winners. The play reaches its local maximum -- the best possible DM performance given the current market, audience, and competitive landscape -- and sustains it as conditions change.

**Pass threshold:** Meeting rate sustained at or above >=1.5% (Scalable baseline) for 6 consecutive months. Convergence declared when 3 consecutive experiments produce <2% improvement.

## Leading Indicators

- Anomaly detection latency: anomalies detected within 24 hours of metric change
- Hypothesis generation: >=1 actionable hypothesis per anomaly detected
- Experiment cadence: 2-4 experiments per month
- Auto-implementation rate: >=50% of experiments produce a clear winner that is auto-implemented
- Convergence trajectory: diminishing returns visible over time (experiment impact decreasing)
- No manual intervention required for >=90% of optimization cycles

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. Configure it specifically for the cold DM play:

**Phase 1 -- Monitor (daily via n8n cron):**

Build an n8n workflow triggered at 8am daily:

1. Use `posthog-anomaly-detection` to check these DM-specific KPIs:
   - Reply rate by channel (LinkedIn, X) -- compare last 7 days vs 4-week rolling average
   - Meeting rate (combined) -- compare last 7 days vs 4-week rolling average
   - DM volume per channel -- compare to expected daily volume
   - Positive reply rate -- compare to 4-week baseline
   - Cost per meeting -- compare to 4-week baseline

2. Classification thresholds:
   - **Normal:** metric within +/-10% of 4-week average
   - **Plateau:** metric within +/-2% for 3+ consecutive weeks
   - **Drop:** metric declined >15% vs 4-week average
   - **Spike:** metric increased >30% vs 4-week average

3. If normal: log to Attio, no action.
4. If anomaly detected: trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**

1. Gather context from Attio: current message variants in rotation, ICP segments active, channel split, engagement warm-up duration, prospect list freshness (days since last Clay refresh).
2. Pull 8-week metric history from PostHog using `posthog-dashboards`.
3. Run `hypothesis-generation` with the anomaly data + context. Prompt structure:

   ```
   Anomaly: [reply rate on LinkedIn dropped 18% vs 4-week average]
   Current config: [message variant C, 5-day warm-up, targeting Series A CTOs]
   8-week trend: [reply rate: 14%, 15%, 13%, 14%, 12%, 11%, 10%, 9%]
   Question: What are the 3 most likely causes and what experiment would test each?
   ```

4. Receive 3 ranked hypotheses. Example hypotheses for DM plays:
   - "Message variant C has fatigued. Reply rate for variant C specifically dropped 25% while others held steady. Test: rotate in new variant D."
   - "ICP segment Series A CTOs is saturated in your target geography. Test: expand to Series B or add a new vertical."
   - "LinkedIn algorithm change reduced connection request acceptance. Test: shorten connection note from 200 to 100 characters."

5. Store hypotheses in Attio as notes on the campaign record.
6. If top hypothesis risk = "high" (e.g., changing ICP entirely): send Slack alert for human review. STOP.
7. If risk = "low" or "medium": proceed to Phase 3.

**Phase 3 -- Experiment (auto-triggered):**

1. Take the top-ranked hypothesis.
2. Design the experiment using `posthog-experiments`:
   - Create a feature flag that splits new prospects between control (current config) and variant (hypothesis change).
   - For DM copy experiments: create the new variant in Dripify/PhantomBuster. Route 50% of new prospects to each.
   - For timing experiments: adjust the warm-up duration or send time for the variant group.
   - For targeting experiments: add the new ICP segment as the variant group while maintaining the current segment as control.
3. Set experiment duration: minimum 7 days AND minimum 100 DMs per variant, whichever is longer.
4. Log experiment start in Attio: hypothesis, start date, expected end date, success criteria.

**Phase 4 -- Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog.
2. Run `experiment-evaluation`:
   - Statistical significance: 95% confidence required.
   - Practical significance: improvement must be >=5% relative to control to be worth implementing.
   - Guard metrics: negative reply rate must not increase by >3pp. DM delivery rate must not drop.

3. Decision matrix:
   - **Adopt:** Variant wins at 95% confidence with >=5% improvement and no guard metric violations. Auto-implement: update Dripify/PhantomBuster config to use the winning variant for all prospects. Log in Attio.
   - **Iterate:** Result is directionally positive but not statistically significant. Generate a refined hypothesis and return to Phase 2.
   - **Revert:** Variant loses or guard metric violated. Disable variant, restore control. Log the failure. 7-day cooldown before testing the same variable again. Return to Phase 1.
   - **Extend:** Insufficient sample size at planned end date. Extend experiment 7 more days.

4. Store evaluation in Attio: decision, confidence level, effect size, reasoning.

**Phase 5 -- Report (weekly via n8n cron):**

1. Aggregate all optimization activity for the week.
2. Generate a weekly optimization brief:
   - Anomalies detected this week
   - Experiments in progress (status, preliminary data)
   - Experiments completed (decision, effect size)
   - Net metric change from all adopted changes
   - Current performance vs Scalable baseline
   - Estimated distance from local maximum (based on diminishing experiment returns)
3. Post to Slack, store in Attio.

### 2. Deploy the DM performance monitor

Run the `autonomous-optimization` drill. This creates the always-on monitoring layer that feeds the autonomous optimization loop:

1. Build the PostHog DM performance dashboard with panels:
   - Funnel: dm_sent > dm_replied > dm_meeting_booked > dm_deal_created (by channel)
   - Reply rate trend (12-week by channel)
   - Message variant performance comparison
   - Day/time heatmap for optimal send windows
   - Channel comparison (LinkedIn vs X side-by-side)
   - Cost per meeting trend
   - Pipeline value from DM outreach

2. Configure threshold alerts:
   - Reply rate drops below 8% on either channel (7-day rolling)
   - Daily DM volume drops below 50% of 4-week average
   - Negative sentiment exceeds 15% of replies
   - Meeting no-show rate exceeds 30%

3. Set up the weekly performance brief (automated via n8n Monday 8am).
4. Set up the monthly channel health report (first Monday of each month).

### 3. Maintain signal-based targeting

Run the `signal-detection` drill in continuous mode:

1. Clay monitors for buying signals daily: job changes, funding events, hiring activity, competitor mentions.
2. High-score signals inject prospects directly into the DM pipeline.
3. Track signal-to-meeting conversion rate separately. If signal-triggered outreach outperforms standard outreach by >2x, increase the proportion of signal-based DMs.
4. The autonomous optimization loop should test: "Does increasing signal-triggered DMs from 20% to 40% of volume improve overall meeting rate?"

### 4. Implement convergence detection

The optimization loop must recognize when the play has reached its local maximum:

1. Track the effect size of each completed experiment.
2. If 3 consecutive experiments produce <2% improvement (regardless of pass/fail), the play has converged.
3. At convergence:
   - Reduce monitoring frequency from daily to weekly.
   - Reduce experiment cadence from 2-4/month to 1/month (maintenance experiments).
   - Generate a convergence report: "Cold DM play has reached its local maximum. Current performance: [metrics]. Further gains require strategic changes: new channels, new ICP segments, or product positioning changes."
4. Continue weekly monitoring even after convergence. If market conditions change (metric drops >20%), re-enter active optimization.

### 5. Guardrails (critical)

These limits protect against automation causing damage:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on the same play.
- **Revert threshold:** If reply rate drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Budget changes >20% (adding new tools or upgrading plans)
  - ICP changes that affect >50% of the prospect pipeline
  - Any hypothesis flagged as "high risk" by the hypothesis generator
  - Channel abandonment (stopping outreach on LinkedIn or X entirely)
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Prospect experience:** Never send more than 3 DMs total to any single prospect across all channels. The agent must check Attio before every send.

## Time Estimate

- Autonomous optimization loop setup (n8n workflows, PostHog config): 8 hours
- DM performance monitor setup (dashboard, alerts, briefs): 6 hours
- Signal detection continuous mode configuration: 3 hours
- Convergence detection setup: 2 hours
- Testing and validation: 1 hour
- **Setup total: ~20 hours**
- **Ongoing: ~5 hours/month** (weekly brief review, experiment approval for high-risk hypotheses, monthly strategic review)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Sales Navigator | Advanced search, InMail | $119.99/mo ([pricing](https://business.linkedin.com/sales-solutions/compare-plans)) |
| Dripify | LinkedIn automation | $39-59/mo ([pricing](https://dripify.io/pricing)) |
| PhantomBuster | X engagement + DM automation | $56/mo Starter ([pricing](https://phantombuster.com/pricing)) |
| X API | DM send/receive, engagement via API | $200/mo Basic ([pricing](https://developer.x.com/en/products)) |
| Clay | Prospect enrichment + signal detection | $149/mo Explorer ([pricing](https://www.clay.com/pricing)) |
| Attio | CRM, campaign records, audit trail | Free tier up to 3 users ([pricing](https://attio.com/pricing)) |
| PostHog | Analytics, experiments, anomaly detection | Free tier: 1M events/mo ([pricing](https://posthog.com/pricing)) |
| n8n | Orchestration (optimization loop, syncs, alerts) | Free self-hosted / $20/mo cloud ([pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation | ~$20-50/mo at optimization cadence ([pricing](https://www.anthropic.com/pricing)) |

**Total play-specific cost: ~$605-855/mo** (plus ~$20-50/mo for AI agent compute)

## Drills Referenced

- `autonomous-optimization` -- the core monitor > diagnose > experiment > evaluate > implement loop that finds the local maximum
- `autonomous-optimization` -- always-on dashboard, alerts, and reporting for DM outreach across LinkedIn and X
- `signal-detection` -- continuous buying signal monitoring feeding the DM pipeline
