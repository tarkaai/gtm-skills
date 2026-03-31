---
name: outbound-voice-messages-durable
description: >
  Outbound Voice Messages -- Durable Intelligence. Always-on AI agents autonomously
  optimize voice message scripts, delivery timing, channel allocation, and prospect
  targeting. The autonomous-optimization loop detects metric anomalies, generates
  hypotheses, runs experiments, and auto-implements winners to sustain >=5% response
  rates over 12 months.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained >=5% response rate over 12 months with autonomous script optimization and channel rebalancing"
kpis: ["Sustained response rate", "Experiment win rate", "Script refresh velocity", "Cost per meeting trend", "Autonomous intervention count"]
slug: "outbound-voice-messages"
install: "npx gtm-skills add marketing/solution-aware/outbound-voice-messages"
drills:
  - autonomous-optimization
  - voice-message-performance-monitor
  - signal-detection
---

# Outbound Voice Messages -- Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social

## Outcomes

The voice message outreach pipeline operates autonomously with AI agents monitoring performance, diagnosing degradation, generating script improvements, running experiments, and implementing winners -- all without human intervention for routine optimization. The `autonomous-optimization` drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce less than 2% improvement, signaling the local maximum has been reached.

Human involvement is limited to: reviewing weekly briefs, approving high-risk changes (audience targeting shifts affecting >50% of volume), and providing strategic direction (new markets, new product positioning).

## Leading Indicators

- Autonomous optimization loop runs daily without errors for 30+ consecutive days
- At least 2 experiments complete per month with statistically valid results
- Experiment win rate above 40% (at least 2 of every 5 experiments produce a measurable improvement)
- Script variants are refreshed automatically when decay is detected (no script runs longer than 6 weeks without improvement or replacement)
- Cost per meeting trends flat or downward over 6-month window
- No manual intervention required for routine optimization for 4+ consecutive weeks
- Response rate stays within 15% of the 3-month rolling average despite market changes

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. Configure it for the voice message play:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull voice message metrics from PostHog: response rate by channel, script variant performance, delivery rate, callback rate, meeting conversion
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal: log to Attio, no action needed
5. If anomaly detected: trigger Phase 2 (Diagnose)

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context from Attio: current script variants, channel allocation, delivery windows, prospect targeting criteria
2. Pull 8-week metric history from PostHog
3. Generate 3 ranked hypotheses using Claude (via `hypothesis-generation` fundamental):
   - Example hypotheses: "Script A has decayed due to market saturation -- test new value prop angle", "Tuesday delivery window has lost effectiveness -- test Thursday 10am", "LinkedIn channel is outperforming phone by 3x -- shift 20% of phone volume to LinkedIn"
4. Rank by expected impact and risk level
5. If top hypothesis is high-risk (e.g., changes targeting for >50% of volume): send Slack alert for human approval and STOP
6. If low or medium risk: proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags
2. For script experiments: generate a new script variant using Claude, synthesize it via ElevenLabs, and deploy to 50% of new prospects
3. For timing experiments: split delivery windows between control and test
4. For channel mix experiments: adjust the phone/LinkedIn allocation ratio for the test group
5. Run for minimum 7 days or 100+ sends per variant, whichever is longer
6. Log experiment start in Attio: hypothesis, start date, expected duration, success metric

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog using `experiment-evaluation` fundamental
2. Decision:
   - **Adopt**: Variant outperforms control by >2% with >90% confidence. Update the live configuration. Log the change. Move to Phase 5.
   - **Iterate**: Results inconclusive. Generate a refined hypothesis building on learnings. Return to Phase 2.
   - **Revert**: Variant underperforms. Disable the variant, restore control. Log the failure. Return to Phase 1.
3. Store the full evaluation in Attio with decision, confidence interval, and reasoning

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate a weekly optimization brief using Claude:
   - What changed and why
   - Net impact on response rate, cost per meeting, and meeting volume
   - Current distance from estimated local maximum
   - Convergence check: have the last 3 experiments produced <2% improvement?
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Configure voice-specific optimization targets

The `autonomous-optimization` drill is generic. Configure these play-specific parameters:

**Primary KPI**: Response rate (callbacks + LinkedIn replies + email replies referencing voice message)
**Secondary KPIs**: Cost per meeting, meeting conversion rate, script variant freshness
**Optimization variables** (what the agent can change):
- Script copy (value prop hook, signal reference, CTA phrasing)
- Script tone (via ElevenLabs voice settings: stability, similarity_boost, style)
- Delivery timing (day of week, time of day)
- Channel allocation (% of volume to phone VM vs LinkedIn voice notes)
- Follow-up email subject line and copy
- Prospect tier weighting (shift volume toward higher-responding segments)

**What the agent cannot change without human approval:**
- ICP criteria (adding or removing entire segments)
- Budget allocation (increasing monthly tool spend by >20%)
- Voice clone (switching to a different person's voice)
- Total daily volume (increasing beyond LinkedIn safety limits)

### 3. Deploy advanced signal-based targeting

Run the `signal-detection` drill to configure Clay for real-time buying signal monitoring:

- Job changes at target accounts (new VP/Director in relevant department)
- Funding announcements (Series A/B/C within last 30 days)
- Technology stack changes (adopted or dropped a competitor)
- Hiring signals (3+ open roles in relevant department)
- Competitor mentions (company mentioned in a review or comparison)

Feed signals into the automated prospect pipeline. The autonomous optimization loop can adjust signal weighting based on which signals produce the highest response rates.

### 4. Build the voice message performance monitor for Durable

Run the `voice-message-performance-monitor` drill with Durable-level additions:

**Additional dashboard panels:**
- Experiment portfolio: active experiments, completed this month, win rate
- Script lifecycle: age of each active variant, response rate trend per variant, decay detection
- Channel efficiency: cost per meeting by channel, trended monthly
- Convergence tracker: rolling 3-experiment improvement delta

**Additional anomaly alerts:**
- Experiment has been running for 21+ days without reaching statistical significance (sample size issue)
- All 4 monthly experiments failed (trigger strategic review)
- Cost per meeting increased >25% from 3-month average
- Script variant has been active for 6+ weeks with no challenger (staleness risk)

**Monthly trend report (automated):**
- 90-day response rate trend by channel and script variant
- Script effectiveness heatmap (which value props work for which ICP segments)
- Channel ROI comparison: phone VM cost per meeting vs LinkedIn voice note cost per meeting
- Recommendations: which scripts to retire, which segments to expand, which channel to scale

### 5. Handle convergence

The optimization loop detects convergence when 3 consecutive experiments produce less than 2% improvement. When convergence is detected:

1. Reduce monitoring from daily to weekly
2. Reduce experiment frequency from 4/month to 1/month (maintenance experiments)
3. Generate a convergence report: "Voice message outreach has reached its local maximum. Current performance: {response_rate}% response rate, {cost_per_meeting} cost per meeting, {monthly_volume} messages/month. Further gains require strategic changes: new ICP segments, new product positioning, or new channels."
4. Post the convergence report to Slack and store in Attio
5. Continue monitoring for market changes that break convergence (competitor launches, market shifts, seasonal effects) and re-enter the optimization loop if performance drops >15%

### 6. Evaluate sustainability

This level runs continuously. Monthly checkpoint against threshold: **Sustained >=5% response rate over 12 months**.

Track:
- Rolling 3-month response rate (must stay above 5%)
- Experiment portfolio: experiments run, win rate, cumulative improvement
- Autonomous intervention count: how many times the agent adjusted something without human input
- Cost per meeting trend: should be flat or declining
- Script refresh velocity: average lifespan of a script variant before replacement

If response rate drops below 5% for 2 consecutive months despite optimization:
1. The agent triggers a strategic review request
2. **Human action required:** Evaluate whether the market has changed, the ICP needs updating, or the voice message channel is saturating. Decide whether to continue, pivot, or scale back.

## Time Estimate

- Month 1 -- Optimization loop setup: 25 hours
  - autonomous-optimization drill configuration: 8 hours
  - Voice-specific optimization parameters: 4 hours
  - Signal detection setup: 5 hours
  - Enhanced monitoring dashboard: 4 hours
  - Testing and validation: 4 hours
- Months 2-6 -- Active optimization: 60 hours (12 hours/month)
  - Weekly brief review: 2 hours/month
  - Experiment review and approval (high-risk only): 2 hours/month
  - Script quality review (spot-check AI-generated variants): 2 hours/month
  - Strategic adjustments: 3 hours/month
  - Pipeline maintenance: 3 hours/month
- Months 7-12 -- Steady state / convergence: 45 hours (7.5 hours/month)
  - Weekly brief review: 1.5 hours/month
  - Monthly experiment review: 1.5 hours/month
  - Quarterly strategic review: 2 hours/quarter
  - Pipeline maintenance: 2.5 hours/month

Total: ~180 hours over 12 months (front-loaded in Month 1, declining as system converges).

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ElevenLabs | AI voice generation + script variant synthesis | Pro: $99/mo for 500K chars (~1,250 messages) (https://elevenlabs.io/pricing) |
| VoiceDrop.ai | Ringless voicemail delivery | Growth: $495/mo for ~2,500 VMs (https://www.voicedrop.ai/pricing) |
| lemlist | LinkedIn voice note automation | Multichannel Expert: $99/user/mo (https://www.lemlist.com/pricing) |
| Clay | Enrichment, signal monitoring, script generation | Pro: $149/mo (https://www.clay.com/pricing) |
| Instantly | Follow-up email sequences | Growth: $30/mo (https://instantly.ai/pricing) |
| Anthropic | Claude API for hypothesis generation and evaluation | Pay-as-you-go: ~$15-30/mo at this volume (https://www.anthropic.com/pricing) |
| Attio | CRM for pipeline and experiment tracking | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Dashboards, experiments, anomaly detection | Free tier likely sufficient (https://posthog.com/pricing) |
| n8n | Orchestration of all automated workflows | Self-hosted: free; Cloud: $20/mo (https://n8n.io/pricing) |

**Estimated play-specific cost: ~$750-950/mo** (ElevenLabs Pro + VoiceDrop Growth + lemlist + Clay + Instantly + Anthropic API)

Note: Cost per meeting should trend downward as optimization improves conversion rates. At 500 messages/month with 5% response rate and 50% meeting conversion, expect ~12 meetings/month at ~$65-80/meeting.

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Convergence detection.
- `voice-message-performance-monitor` -- enhanced dashboards with experiment portfolio tracking, script lifecycle, convergence tracker, and monthly trend reports
- `signal-detection` -- real-time buying signal monitoring feeding the automated prospect pipeline with optimizable signal weighting
