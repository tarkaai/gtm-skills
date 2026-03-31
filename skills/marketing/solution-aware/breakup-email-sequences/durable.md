---
name: breakup-email-sequences-durable
description: >
  Breakup Email Sequences — Durable Intelligence. Autonomous AI agents manage the
  breakup pipeline end-to-end: the optimization loop detects when re-engagement rates
  plateau or decay, generates hypotheses (copy fatigue, signal quality degradation,
  pool composition shift), runs experiments, and auto-implements winners. Play-specific
  monitoring tracks pool health, signal lift trends, and breakup-to-pipeline attribution.
  The founder's only role is taking meetings from re-engaged prospects.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Re-engagement rate sustained at ≥ 4% for 6 consecutive months with ≤ 30 min/week founder involvement"
kpis: ["Re-engagement rate trend (flat or improving over 6 months)", "Experiment win rate (target ≥ 25% of experiments produce significant lift)", "Pool sustainability index (net pool growth ≥ 0)", "Signal lift trend (stable or improving)", "Cost per meeting from breakup-recovered prospects"]
slug: "breakup-email-sequences"
install: "npx gtm-skills add marketing/solution-aware/breakup-email-sequences"
drills:
  - autonomous-optimization
---

# Breakup Email Sequences — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

The breakup email pipeline runs autonomously with an AI agent continuously optimizing every variable: copy angles, signal weighting, cool-off timing, asset selection, send timing, and ICP segment targeting. The `autonomous-optimization` drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. The `autonomous-optimization` drill tracks breakup-specific dynamics: pool health, signal lift trends, message fatigue curves, and breakup-to-pipeline attribution. Together, these drills find the local maximum of breakup re-engagement performance and maintain it as the market, prospect pool, and competitive landscape evolve.

Pass: Re-engagement rate ≥ 4% sustained for 6 consecutive months with the founder spending ≤ 30 minutes/week on breakup-related tasks.
Fail: Re-engagement rate drops below 4% for 3 consecutive weeks despite automated interventions, or the system requires more than 1 hour/week of founder time.

## Leading Indicators

- The `autonomous-optimization` loop detects anomalies within 48 hours of onset (monitoring is timely)
- At least 1 in 4 experiments produces a statistically significant winner (the system is still finding improvements)
- Message fatigue decay rate is slower than variant generation rate (the copy library refreshes faster than it decays)
- Signal lift remains above 1.5x (signal detection still adds value over generic breakups)
- Pool sustainability index stays positive (inflow of new silent prospects >= outflow of breakup sends + re-engagements + exhausted contacts)
- Cost per meeting from breakup-recovered prospects trends flat or downward

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the breakup email play. The core loop:

**Phase 1 — Monitor (daily via n8n cron):**

Configure the monitoring workflow to check breakup-specific KPIs daily:

- Pull from PostHog: re-engagement rate (7-day rolling), signal lift, open rates by variant, reply sentiment distribution
- Compare last 2 weeks against the 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)

Breakup-specific anomaly patterns to watch:
- **Re-engagement rate drops but open rate holds:** The emails are being read but the copy is not converting. Hypothesis: message fatigue or CTA weakness.
- **Signal-detected rate drops but no-signal rate holds:** Signal quality is degrading (false positives, stale signals, or over-used signal angles). Hypothesis: signal detection needs recalibration.
- **Open rate drops across all variants:** Deliverability issue or subject line fatigue. Check Instantly domain health scores.
- **Pool inflow drops:** Upstream outbound plays are sending less volume or converting more (fewer silent prospects). Not a breakup problem — flag to upstream play owners.

If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

Gather context:
1. Pull 8-week metric history from PostHog using `posthog-dashboards`
2. Pull the current breakup configuration from Attio: active variants, signal types, cool-off period, send volume
3. Run `hypothesis-generation` with the anomaly data + configuration context

The AI generates 3 ranked hypotheses. Common breakup-specific hypotheses:

- "Variant A's reply rate has decayed 35% from peak — message fatigue. Rotate in Variant E."
- "Signal lift dropped because job-change signals are 90+ days old by the time they reach the breakup queue — reduce cool-off for signal-detected to 21 days."
- "Email 2 asset conversion dropped — the case study is stale. Replace with fresh benchmark data."
- "Re-engagement rate dropped in the 50-100 employee ICP segment — competitors may have started their own breakup campaigns in this segment."
- "Cool-off period is too long — prospects contacted 60-90 days ago re-engage at half the rate of 30-45 day prospects."

Store hypotheses in Attio. If risk = "high" (e.g., major targeting change), alert human for approval. Otherwise, proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis
2. Design the experiment using `posthog-experiments`: create a feature flag that splits breakup traffic between control (current) and variant (hypothesis change)
3. Implement the variant:
   - For copy changes: use the `breakup-email-copy` drill to generate a new variant and load into Instantly
   - For timing changes: adjust the n8n cool-off workflow for the variant cohort
   - For signal changes: update Clay enrichment thresholds for the variant
   - For asset changes: swap the Email 2 asset for the variant cohort
4. Set experiment duration: minimum 7 days or until 100+ samples per variant, whichever is longer
5. Log experiment start in Attio with hypothesis, start date, expected duration, and success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs. variant data
3. Decision:
   - **Adopt:** Apply the winning variant to all breakup traffic. Log the change. Archive the losing variant.
   - **Iterate:** The result was promising but not significant. Generate a refined hypothesis and return to Phase 2.
   - **Revert:** Variant performed worse. Disable it, restore control. Log the failure. Return to Phase 1.
   - **Extend:** Results are trending but sample size is insufficient. Continue for another 7 days.
4. Store full evaluation in Attio (decision, confidence, reasoning, metric impact)

**Phase 5 — Report (weekly via n8n cron):**

Generate a weekly optimization brief:
1. Anomalies detected this week and their classifications
2. Hypotheses generated and ranked
3. Active experiments: status and interim results
4. Completed experiments: winners implemented, losers reverted
5. Net metric change from all adopted changes this week
6. Current distance from estimated local maximum (estimated by the rate of improvement from recent experiments)
7. Pool health: sustainability index, inflow vs. outflow, projected months of runway

Post to Slack and store in Attio.

### 2. Deploy breakup-specific monitoring

Run the `autonomous-optimization` drill to build the monitoring layer that tracks dynamics unique to breakup sequences:

**PostHog dashboard (6 panels):**
1. Weekly re-engagement rate trend (signal vs. no-signal vs. blended) with Scalable baseline reference line
2. Breakup-to-meeting funnel (segmented by signal vs. no-signal)
3. Pool health: stacked area showing available prospects, breakups sent, re-engaged, permanently exhausted
4. Variant performance table with fatigue indicators
5. Signal type attribution (re-engagement rate by signal category)
6. Cost efficiency: cost per re-engaged prospect over time

**Automated alerts:**
- Re-engagement rate drops below 70% of 4-week average for 2 consecutive weeks
- Pool runway drops below 2 months at current send rate
- Any variant's reply rate drops below 50% of its peak
- Bounce rate exceeds 2% or unsubscribe rate exceeds 0.5%

**Weekly report:** Delivered every Friday to Slack with one-paragraph summary and actionable recommendation.

**Pipeline attribution:** Track breakup-originated deals separately in Attio. Calculate average deal size, close rate, and time-to-close for breakup-recovered prospects vs. fresh outbound prospects. This data determines the play's true ROI.

### 3. Build the copy rotation engine

Message fatigue is the primary threat to breakup Durable performance. Every breakup variant eventually decays because:
- Prospects in the same network share "I got this breakup email" stories
- The same ICP segments see similar messaging patterns
- Loss-aversion framing wears off with repeated exposure across the market

Create a copy library with a rotation system:

- Maintain at least 6 active Email 1 variants (3 no-signal, 3 signal-detected)
- Maintain at least 3 active Email 2 asset variants
- When any variant's reply rate drops below 60% of its peak over a 30-day window, the n8n workflow:
  1. Pauses the variant
  2. Triggers the `breakup-email-copy` drill to generate a replacement
  3. Rotates in the next variant from the library
  4. Logs the rotation event in PostHog

New variant generation uses insights from the `autonomous-optimization` loop: which angles resonated recently, which signal types are producing lift, and what the re-engaged prospects are saying in their replies (extract themes via Claude API).

**Human action required:** The founder reviews and approves new breakup copy variants once per month (~15 minutes). The agent drafts variants based on reply analysis and market context.

### 4. Optimize signal detection and cool-off timing

Two variables unique to breakup sequences that the `autonomous-optimization` loop should continuously test:

**Signal weighting optimization:**
Not all signals produce equal re-engagement lift. Track re-engagement rate by signal type over time:
- Job change -> [X]% re-engagement
- Funding event -> [Y]% re-engagement
- Hiring signals -> [Z]% re-engagement
- Content engagement -> [W]% re-engagement

Re-allocate Clay enrichment credits toward the highest-converting signal types. Deprecate signal types that produce <1.2x lift over no-signal (they are not worth the enrichment cost).

Run an experiment quarterly: add one new signal type (e.g., competitor G2 review, conference attendance, technology adoption) and measure its lift over 4 weeks.

**Cool-off period optimization:**
The optimal gap between the last outbound touch and the breakup send may shift over time as your brand awareness and market position change. Run an experiment semi-annually:
- Control: current cool-off period (e.g., 35 days)
- Variant A: shorter (25 days)
- Variant B: longer (50 days)
- Measure by: re-engagement rate and reply sentiment (shorter cool-off might get more replies but more hostile ones)

### 5. Manage pool sustainability at Durable scale

At Durable level, pool management is strategic:

**Monthly pool audit (automated via n8n):**
1. Total silent prospects entering the breakup queue from all outbound plays
2. Breakup sends completed this month
3. Re-engaged prospects (exits via positive reply)
4. Exhausted prospects (received breakup, no reply, 180-day cooldown before eligible for another breakup)
5. Stale prospects (email no longer valid, left company, etc.)
6. Net pool size trend

**Pool expansion strategies** (when net pool growth is negative):
- Coordinate with upstream outbound plays to increase total send volume (the breakup play benefits from every outbound play's volume)
- Expand the eligible pool: include prospects who replied "not now" to the original sequence 90+ days ago (they expressed interest but did not convert — different from total silence)
- Extend the breakup eligibility window from 90 to 120 days (reaches prospects who went silent longer ago)
- Test re-breakup: send a second breakup to prospects who received a breakup 180+ days ago with an entirely new angle. Run this as an experiment first — re-breakup fatigue is a real risk.

**Pool contraction strategies** (when pool grows faster than you can process):
- Tighten ICP scoring: only breakup the highest-scoring silent prospects
- Increase signal detection coverage: more signal-detected breakups means better re-engagement rate per send
- Add a pre-breakup qualification step: only breakup prospects who opened at least 1 email in the original sequence (they showed some interest)

### 6. Run monthly deep review

Build an n8n workflow that runs on the 1st of each month:

1. Pull 30-day aggregate metrics for the breakup play
2. Compare to prior month, to Scalable baseline, and to the 6-month trend
3. Identify: best-performing breakup angle, best-performing signal type, winning A/B test variants, and any metric that worsened
4. Calculate breakup play ROI: total pipeline value from breakup-recovered deals / total play cost (tools + agent compute + founder time)
5. Generate monthly brief with recommendations:
   - Which variants to retire and what to replace them with
   - Which signal types to invest more/less in
   - Pool health projection for next 3 months
   - Whether cool-off timing needs adjustment
   - Comparison of breakup play ROI vs. other outbound plays' ROI
6. Flag convergence: if the last 3 experiments all produced <2% improvement, the play has found its local maximum. Recommend reducing monitoring frequency and reallocating optimization effort to other plays.

**Human action required:** The founder reviews the monthly brief (~15 minutes) and approves any strategic changes: new ICP segments for breakup eligibility, cool-off period changes, or budget adjustments.

### 7. Sustain for 6 months

The system runs continuously. Agent responsibilities:
- Ensure all n8n workflows execute daily/weekly without errors
- Respond to anomaly alerts within 4 hours
- Run the autonomous optimization loop: monitor, diagnose, experiment, evaluate, implement
- Rotate copy variants when fatigue threshold is triggered
- Maintain signal detection quality (deprecate low-lift signals, test new ones)
- Generate weekly and monthly reports
- Manage pool sustainability

Founder responsibilities:
- Respond to positive breakup replies forwarded via Slack (~15 min/week)
- Take meetings from re-engaged prospects
- Approve new copy variants once per month (~15 min)
- Review monthly brief and make strategic decisions (~15 min)

### 8. Evaluate sustainability after 6 months

Compute over the full 6-month period:
- Monthly re-engagement rate for each of the 6 months
- Re-engagement rate trend: stable, improving, or decaying?
- Total meetings booked from breakup-recovered prospects
- Average deal size and close rate for breakup-originated deals vs. fresh outbound deals
- Signal lift trend: is signal-based personalization still adding value?
- Total experiments run, winners, losers, and net metric impact
- Pool sustainability: is the pool growing, stable, or depleting?
- Total cost / total meetings = cost per meeting from breakup
- Total founder hours / total meetings = founder time per meeting

- **PASS (re-engagement rate ≥ 4% for all 6 months, founder ≤ 30 min/week):** The breakup play is durable. It produces consistent pipeline from prospects that other plays failed to convert. Consider: expanding to new outbound channels (breakup LinkedIn DMs to complement breakup emails), applying breakup sequencing to inbound leads who went cold, or licensing the breakup copy library to the sales team for manual use on high-value stalled deals.
- **CONVERGED (re-engagement rate held but 3+ consecutive experiments produced <2% improvement):** The play has found its local maximum. Reduce optimization frequency to bi-weekly. The play still produces value but further gains require strategic changes (new channels, new ICP segments, product changes that create new proof points).
- **DECLINING (re-engagement rate held for 4+ months then decayed below 4%):** Diagnose: Is the pool depleting (fewer silent prospects entering)? Is the market saturated with breakup-style emails? Has your brand perception changed (making breakup emails feel incongruent)? Options: reduce volume and increase quality, pivot to a different re-engagement format (breakup voicemail, breakup direct mail), or pause the play and re-launch in 6 months with fresh copy.
- **FAIL (re-engagement rate below 4% for 3+ consecutive weeks at any point):** The optimization loop is not adapting fast enough. Diagnose: Are hypotheses accurate? Are experiments running at sufficient volume? Is the copy rotation engine catching fatigue in time? Fix the specific broken component or accept that this play requires more manual oversight than Durable allows.

## Time Estimate

- Autonomous optimization loop setup: 10 hours (Month 1)
- Breakup-specific monitoring setup: 8 hours (Month 1)
- Copy rotation engine: 4 hours (Month 1)
- Signal optimization pipeline: 4 hours (Month 1)
- Pool sustainability system: 3 hours (Month 1)
- Monthly review workflow: 2 hours (Month 1)
- Setup subtotal: 31 hours
- Weekly agent monitoring and optimization: 4 hours/week x 24 weeks = 96 hours
- Weekly founder time: 30 min/week x 24 weeks = 12 hours
- Monthly founder review: 15 min x 6 months = 1.5 hours
- Copy variant generation (ongoing): 3 hours/month x 6 months = 18 hours
- Ongoing subtotal: ~128 hours (110 agent, 14 founder)
- Grand total: ~200 hours over 6 months (141 agent, 14 founder, 45 buffer/troubleshooting)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Breakup email delivery, variant rotation, conditional steps, reply detection | Hypergrowth plan $97/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, weekly pipeline refresh, email re-verification | Growth plan $495/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal attribution, experiment logging, pipeline tracking | Plus plan $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Dashboards, funnel analysis, A/B test measurement, anomaly detection, alerting | Free tier: 1M events/mo, usage-based beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | All automation: optimization loop, reply routing, reporting, copy rotation, alerts | Pro plan $60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Claude API (Anthropic) | Hypothesis generation, experiment evaluation, reply classification, copy generation | ~$20-40/mo at this volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Cal.com | Meeting booking for re-engaged prospects | Free plan ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated monthly cost for Durable:** ~$700-720/mo (shares sending infrastructure with primary outbound plays)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop that detects metric anomalies, generates hypotheses, runs experiments, evaluates results, and auto-implements winners. This is what makes Durable fundamentally different from Scalable.
- `autonomous-optimization` — breakup-specific monitoring: pool health, signal lift trends, variant fatigue curves, and breakup-to-pipeline attribution
