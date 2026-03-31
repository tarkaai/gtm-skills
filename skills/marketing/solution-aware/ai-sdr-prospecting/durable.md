---
name: ai-sdr-prospecting-durable
description: >
  AI SDR Prospecting — Durable Intelligence. Always-on AI agents monitor
  the full AI SDR pipeline, detect anomalies in research quality, outreach
  performance, and meeting conversion, generate improvement hypotheses,
  run A/B experiments, and auto-implement winners. The autonomous-optimization
  drill runs the core loop: detect metric anomalies, generate hypotheses,
  run experiments, evaluate results, auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained meeting rate >=1.6% over 12 months with declining cost per meeting, maintained by autonomous agent-driven optimization across research, personalization, and outreach"
kpis: ["Sustained meeting rate", "Cost per meeting trend", "AI experiment win rate", "Research quality trend", "Time to convergence"]
slug: "ai-sdr-prospecting"
install: "npx gtm-skills add marketing/solution-aware/ai-sdr-prospecting"
drills:
  - autonomous-optimization
  - outbound-performance-monitor
  - signal-detection
---

# AI SDR Prospecting — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

Durable is autonomous optimization. AI agents run the entire AI SDR pipeline continuously, finding the local maximum for meeting rate and cost per meeting. The `autonomous-optimization` drill creates the always-on loop: detect metric anomalies -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. What makes AI SDR Durable unique is that the optimization loop covers not just outreach (copy, timing, channel mix) but also the AI research layer itself (prompt quality, personalization depth, outreach angle effectiveness). The play sustains or improves meeting rate >=1.6% over 12 months while cost per meeting trends downward. Converges when successive experiments produce <2% improvement for 3 consecutive experiments.

## Leading Indicators

- Anomaly detection firing within 24 hours of metric shifts in research quality, reply rates, or meeting conversion
- Hypotheses generated and ranked within 1 hour of anomaly detection
- Experiments launching within 48 hours of hypothesis acceptance
- At least 2 winning experiments adopted per month in months 1-3
- Cost per meeting declining month-over-month
- Weekly optimization briefs delivered every Monday with actionable findings
- AI research quality score maintaining or improving as prospect volume grows
- Outreach angle mix shifting automatically toward highest-converting angles
- Message variant rotation preventing fatigue (no variant used for more than 4 weeks)
- Intent-signal-sourced prospects maintaining 2x+ conversion premium over cold-sourced

## Instructions

### 1. Deploy the outbound performance monitoring system

Run the `outbound-performance-monitor` drill. Build the monitoring layer specific to AI SDR:

1. **PostHog dashboard** — "AI SDR Prospecting — Performance" with panels for:
   - Weekly send volume by channel (email, LinkedIn) and by source (intent, cold)
   - Per-channel conversion funnels: email sent -> opened -> replied -> meeting_booked; LinkedIn connection_sent -> accepted -> message_replied -> meeting_booked
   - AI research quality distribution: histogram of research_quality_score across all prospects this month
   - Outreach angle performance: meeting rate by angle (trigger_event, competitive_displacement, pain_match, content_connection)
   - Cost per meeting trending weekly (total tool spend / meetings)
   - Pipeline value created from AI SDR outreach

2. **Anomaly detection** — alerts for:
   - Email reply rate drops below 2% for 5 consecutive business days
   - LinkedIn acceptance rate drops below 20% for 1 week
   - AI research quality score average drops below 60 for a weekly batch
   - Meeting volume drops to zero for 5 consecutive business days
   - Negative reply rate exceeds 5% on any channel
   - Email bounce rate exceeds 3% (domain health risk)
   - Cost per meeting exceeds 150% of 4-week rolling average
   - Intent signal pipeline drops below 100 new contacts/week

3. **Weekly automated briefs** — n8n workflow that pulls PostHog + Attio data every Monday 8am:
   - Channel-by-channel metrics summary with week-over-week deltas
   - Outreach angle breakdown: which angles are producing meetings, which are decaying
   - AI research quality metrics: accuracy rate, personalization specificity score, prompt performance
   - Best-performing message variants per channel and angle
   - Intent signal health: volume, source mix, conversion premium vs. cold
   - Recommended actions for next week

4. **Monthly trend reports** — cost per meeting by channel and by source, pipeline velocity, total ROI, and strategic recommendations for ICP refinement, research prompt evolution, and channel allocation.

All data stored as structured PostHog events so the autonomous optimization loop can consume them.

### 2. Deploy autonomous optimization

Run the `autonomous-optimization` drill. Configure the 5-phase loop for AI SDR prospecting:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` fundamental to check: meeting rate, reply rate (email), acceptance rate (LinkedIn), AI research quality score, cost per meeting, intent signal conversion premium
2. Compare last 2 weeks against 4-week rolling average
3. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal -> log, no action. If anomaly -> trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current outreach angle distribution, active email variants per angle, LinkedIn message variants, Claygent prompt version, prospect volume by source, ICP segment mix
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` fundamental with anomaly data + context
4. Receive 3 ranked hypotheses. Examples the agent may generate for AI SDR:
   - "Email reply rate for trigger_event angle dropped because the Claygent prompt is surfacing stale events (>90 days old). Hypothesis: tightening the recency filter to 60 days will recover reply rate by 2+ percentage points."
   - "LinkedIn acceptance rate dropped because connection notes are too long and feel templated at scale. Hypothesis: shortening to 120 characters with a question format will improve acceptance by 5+ points."
   - "Meeting rate for competitive_displacement angle dropped because the competitor released a major update, weakening the gap messaging. Hypothesis: updating the displacement messaging to reference the remaining gaps will restore conversion."
   - "AI research quality score declined because Claygent is hitting rate limits and returning partial results. Hypothesis: reducing batch size from 100 to 50 and adding retry logic will restore quality above 75%."
   - "Intent-signal-sourced prospects are no longer converting at a premium because the signal scoring model has not been recalibrated in 8 weeks. Hypothesis: re-weighting signals based on last 8 weeks of meeting data will restore the 2x conversion premium."
5. Store hypotheses in Attio as campaign notes.
6. If top hypothesis is high-risk -> Slack alert for human review and STOP.
7. If low/medium-risk -> proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using `posthog-experiments` fundamental: feature flag splitting traffic between control (current) and variant (hypothesis change)
2. Implement the variant depending on what is being tested:
   - For Claygent prompt changes: create a B variant Clay table with the new prompt. Route 50% of new prospects to each table via n8n.
   - For email copy changes: create B variant campaigns in Instantly using `instantly-campaign` fundamental
   - For LinkedIn changes: create B variant in Dripify using `linkedin-automation-sequence` fundamental
   - For timing/cadence changes: update the n8n workflow schedule for the variant group
   - For targeting changes: adjust Clay scoring model and intent signal thresholds
   - For outreach angle rebalancing: shift the angle distribution for the variant group
3. Set experiment duration: minimum 7 days or until 100+ prospects per variant, whichever is longer
4. Log experiment in Attio: hypothesis, start date, expected duration, success criteria, variables changed

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull results from PostHog experiment
2. Run `experiment-evaluation` fundamental with control vs variant data
3. Decision:
   - **Adopt**: Update live configuration to use winner. Log the change. Example: winning Claygent prompt becomes the default for all new research. Winning email variant replaces the control in Instantly.
   - **Iterate**: Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert**: Disable variant, restore control. Log failure. Return to Phase 1.
   - **Extend**: Keep running — insufficient data. Set reminder for re-evaluation.
4. Store full evaluation in Attio (decision, confidence, reasoning, metric impact)

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on meeting rate and cost per meeting
   - AI research quality trend and any prompt changes
   - Outreach angle performance shift
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 3. Deploy signal-based prospecting refresh

Run the `signal-detection` drill to keep the prospect pipeline fresh and high-quality:

1. Configure Clay tables with automated daily enrichment: monitor for job changes at target accounts (new VP/C-level = budget unlocked), funding events in last 90 days, hiring signals (3+ roles in your domain), technology signals (adopted/dropped competitor tool).
2. Score signals by recency (last 30 days strongest) and intensity (multiple signals from one account).
3. Route high-score signals directly into the AI research pipeline. The Claygent research runs automatically, and the prospect enters the appropriate outreach angle campaign.
4. The autonomous optimization loop monitors signal-to-meeting rate by signal type and adjusts signal thresholds weekly. If a signal type (e.g., job change) produces below-average meeting rates, reduce its priority or tighten the qualifying criteria. If a new signal type emerges (e.g., competitor pricing increase creates displacement opportunities), add it.
5. Monthly: compare meeting rates for signal-sourced vs. cold-sourced prospects. If the premium narrows below 1.5x, the signal model needs recalibration. If the premium widens above 3x, shift more volume toward signal-sourced prospects.

### 4. Configure guardrails

**These guardrails are non-negotiable and override any optimization decision:**

- **Rate limit**: Maximum 1 active experiment per variable at a time. Never stack experiments on the same variable (e.g., do not test Claygent prompt and email subject line simultaneously for the same prospect group).
- **Revert threshold**: If meeting rate drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for**: budget changes >20%, ICP changes affecting >50% of prospects, any change the hypothesis generator flags as high-risk, adding or removing an outreach channel, Claygent prompt changes that alter the research scope (not just phrasing).
- **Cooldown**: After a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Max experiments per month**: 4 (one per week maximum). If all 4 fail in a month, pause optimization and flag for human strategic review.
- **Deliverability protection**: If email bounce rate exceeds 5% or Instantly reports a domain reputation warning, pause all email automation immediately. Do not resume until resolved manually.
- **Volume caps**: Never exceed sending limits set in Scalable. Optimization improves conversion, not volume.
- **Research quality floor**: If AI research quality score drops below 50 for any batch, pause that batch and investigate before sending outreach based on low-quality research. Bad personalization is worse than no personalization.

### 5. Monitor convergence

The optimization loop runs indefinitely. However, the agent detects **convergence** — when successive experiments produce diminishing returns:

- Track improvement magnitude per experiment over time
- If 3 consecutive experiments produce <2% improvement each, the play has reached its local maximum
- At convergence: reduce monitoring frequency from daily to weekly, reduce experiment cadence from weekly to monthly
- Generate a convergence report: "AI SDR Prospecting is optimized at [current meeting rate] with [current cost per meeting]. AI research quality is stable at [score]. The top-performing outreach angle is [angle] at [rate]. Further gains require strategic changes (new ICP segments, new channels, product changes, or new AI research capabilities) rather than tactical optimization."

**Human action required:** Review the convergence report. Decide whether to: maintain current performance, expand to new ICP segments, add new outreach channels (e.g., calls), invest in deeper AI research capabilities (e.g., custom fine-tuned models), or reallocate budget to other plays.

## Time Estimate

- Outbound performance monitor setup: 8 hours
- Autonomous optimization loop configuration: 12 hours
- Signal detection setup: 6 hours
- Guardrail configuration: 4 hours
- Weekly monitoring, brief review, and human decisions: 60 hours (1.5 hrs/week over 12 months)
- Monthly strategic review and ICP refresh: 24 hours (2 hrs/month)
- Experiment design, implementation, and evaluation: 30 hours
- AI research prompt evolution and quality audits: 16 hours
- Convergence review and adjustment: 8 hours
- Buffer for manual interventions and debugging: 12 hours

Total: ~180 hours over 12 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | AI research via Claygent at scale + enrichment + signal monitoring | Growth: $495/mo (https://www.clay.com/pricing) |
| Instantly | Cold email at scale (multiple accounts, A/B variants) | Hypergrowth: $97/mo (https://instantly.ai/pricing) |
| Apollo | Contact sourcing | Professional: $79/user/mo annual (https://www.apollo.io/pricing) |
| Dripify | LinkedIn automation sequences | Pro: $59/user/mo annual (https://dripify.com/pricing) |
| LinkedIn Sales Navigator | Prospecting + advanced search | Core: $99.99/mo or $79.99/mo annual (https://business.linkedin.com/sales-solutions) |
| RB2B / Koala | Website visitor identification | RB2B: $99/mo; Koala: $99/mo (https://www.rb2b.com/pricing) |
| n8n | Orchestration + optimization loop workflows | Starter: $20/mo (https://n8n.io/pricing) |
| Attio | CRM + optimization audit trail | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Analytics + experiments + anomaly detection | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Anthropic API | Claude for hypothesis generation + experiment evaluation | ~$50-150/mo at optimization frequency (https://www.anthropic.com/pricing) |
| Cal.com | Meeting booking | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$1,030-1,250/mo** (Clay + Instantly + Apollo + Dripify + Sales Nav + RB2B/Koala + Anthropic)

## Drills Referenced

- `autonomous-optimization` — the core monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for meeting rate, cost per meeting, and AI research quality
- `outbound-performance-monitor` — always-on dashboards, weekly briefs, monthly trend reports, and anomaly detection across email, LinkedIn, research quality, and intent signals
- `signal-detection` — continuous buying signal monitoring to keep the prospect pipeline fresh, high-quality, and converting at a premium versus cold-sourced prospects
