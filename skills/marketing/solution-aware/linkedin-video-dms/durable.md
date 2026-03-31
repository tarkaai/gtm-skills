---
name: linkedin-video-dms-durable
description: >
  LinkedIn Video DMs — Durable Intelligence. Always-on AI agents run the autonomous optimization
  loop: detect metric anomalies in video DM performance, generate hypotheses for improvement, run
  A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained >=8% response rate over 12 months via autonomous optimization of video scripts, DM copy, send timing, and prospect targeting"
kpis: ["Sustained response rate", "Experiment win rate", "Time to convergence", "Cost per meeting trend", "Signal-to-meeting conversion rate"]
slug: "linkedin-video-dms"
install: "npx gtm-skills add marketing/solution-aware/linkedin-video-dms"
drills:
  - autonomous-optimization
---

# LinkedIn Video DMs — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Social

## Outcomes

Deploy always-on AI agents that autonomously optimize every dimension of the LinkedIn video DM play. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in video DM performance, generate improvement hypotheses using Claude, design and run A/B experiments, evaluate results with statistical rigor, and auto-implement winners. The play reaches its local maximum when successive experiments produce <2% improvement for 3 consecutive cycles. At that point, reduce monitoring frequency and report convergence.

## Leading Indicators

- Autonomous optimization loop running without manual intervention for 4+ consecutive weeks
- Experiment win rate >=30% (at least 1 in 3 experiments produces a statistically significant improvement)
- Time from anomaly detection to experiment launch <=48 hours
- Weekly optimization briefs generated and posted to Slack every Monday
- Response rate variance <=2 percentage points month-over-month (stability signal)
- Cost per meeting trending flat or down over 6+ months

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the LinkedIn video DM play. This is the drill that makes Durable fundamentally different from Scalable. Instead of the founder manually reviewing A/B test results and deciding what to test next, an always-on agent loop handles the entire cycle:

**Phase 1 — Monitor (daily via n8n cron):**

1. Use PostHog anomaly detection to check the play's primary KPIs: response rate, video watch rate, watch completion, meeting booking rate, cost per meeting.
2. Compare last 2 weeks against 4-week rolling average.
3. Classify each KPI: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase).
4. If all normal: log to Attio, no action needed.
5. If anomaly detected: trigger Phase 2 automatically.

**Phase 2 — Diagnose (triggered by anomaly):**

1. Gather context: pull current play configuration from Attio (active video script template, DM copy variant, send timing, ICP segments, signal thresholds).
2. Pull 8-week metric history from PostHog for the video DM funnel.
3. Run `hypothesis-generation` with the anomaly data + context. Claude generates 3 ranked hypotheses. Examples:
   - "Response rate dropped 15% because the winning video hook from 8 weeks ago has saturated the target audience. Test a new hook pattern."
   - "Watch completion dropped because average video length crept from 60s to 85s as scripts accumulated more proof points. Test a trimmed 50-second version."
   - "Meeting booking rate dropped despite stable response rate because the Cal.com CTA button text 'Book 15 Minutes' has become stale. Test 'Quick Chat?' as CTA text."
4. Store hypotheses in Attio as campaign notes with risk rating (low/medium/high).
5. If top hypothesis risk = "high": send Slack alert for human review. STOP.
6. If risk = "low" or "medium": proceed to Phase 3 automatically.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis.
2. Design the experiment using PostHog experiments: create a feature flag that splits the prospect pool between control (current configuration) and variant (hypothesis change).
3. Implement the variant. For video DM experiments, this means:
   - Script changes: update the Clay AI formula column to generate the new hook/structure for variant prospects.
   - DM copy changes: update the DM template used for variant prospects.
   - Timing changes: route variant prospects to a different send window.
   - Targeting changes: adjust signal thresholds or ICP filters for variant prospects.
4. Set experiment duration: minimum 7 days or until 50+ sends per variant, whichever is longer.
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog.
2. Run `experiment-evaluation` with control vs variant data.
3. Decision:
   - **Adopt:** Variant beats control with >=95% confidence. Update live configuration to use winner. Log the change.
   - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this data. Return to Phase 2.
   - **Revert:** Control wins or variant causes harm (e.g., negative reply rate spikes). Disable variant. Log failure. Return to Phase 1.
   - **Extend:** Insufficient sample size. Keep experiment running 7 more days.
4. Store full evaluation in Attio: decision, confidence level, effect size, reasoning.

**Phase 5 — Report (weekly via n8n cron, Monday 8am):**

1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments run, decisions made.
2. Calculate net metric change from all adopted changes this week.
3. Generate weekly optimization brief using Claude:
   - What changed and why
   - Net impact on response rate, watch rate, and cost per meeting
   - Current distance from estimated local maximum (based on diminishing returns curve)
   - Active experiments and expected completion dates
   - Recommended focus for next week
4. Post brief to Slack and store in Attio.

### 2. Deploy the video outreach performance monitor

Run the `autonomous-optimization` drill to build the monitoring layer that feeds data to the autonomous optimization loop:

- PostHog dashboard with real-time video DM funnel: DM sent > video watched > watch completed > DM replied > meeting booked > deal created
- Video-specific panels: watch rate by ICP segment, watch completion by video length, CTA click rate by CTA text variant
- Anomaly alerts: watch rate drops below 30% for 5 consecutive days, response rate drops to 0 for 7+ days, negative reply rate exceeds 5%
- Weekly automated video performance briefs with script pattern analysis

This drill's output is the structured data the `autonomous-optimization` drill consumes.

### 3. Deploy the DM performance monitor

Run the the dm performance monitor workflow (see instructions below) drill to track DM-specific metrics alongside video metrics:

- DM delivery and read rate tracking (LinkedIn does not expose read receipts via API, so this is inferred from response timing)
- DM copy variant performance comparison
- Send timing heatmap: response rate by day of week and hour
- Channel health: connection acceptance rate trend (declining acceptance = profile or volume issue)
- Monthly channel health report comparing video DM performance against other outreach channels

### 4. Configure guardrails

The autonomous optimization loop must operate within safety bounds:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on the same variable.
- **Revert threshold:** If response rate drops >30% at any point during an experiment, auto-revert immediately and alert the founder.
- **Human approval required for:**
  - ICP targeting changes that affect >50% of the prospect pool
  - Any hypothesis flagged "high risk" by the hypothesis generator
  - Budget changes (e.g., upgrading LinkedIn plan, increasing Clay credits)
  - Changes to the Loom CTA destination (booking link changes)
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Volume guardrail:** Never exceed 20 video DMs per day to protect LinkedIn account health.
- **Never optimize what is not measured:** If a KPI does not have PostHog tracking, fix tracking first before running experiments on it.

### 5. Detect convergence

The optimization loop runs indefinitely. However, it detects convergence -- when successive experiments produce diminishing returns:

- Track the effect size of each adopted experiment over time.
- If 3 consecutive experiments produce <2% improvement on the primary KPI (response rate), the play has reached its local maximum.
- At convergence:
  1. Reduce monitoring frequency from daily to weekly.
  2. Reduce experiment frequency from 4/month to 1/month (maintenance experiments to detect market shifts).
  3. Generate a convergence report: "LinkedIn Video DMs has reached local maximum. Current performance: {response_rate}% response rate, {cost_per_meeting} cost per meeting. Further gains require strategic changes (new ICP segments, new channels, product-level changes) rather than tactical optimization."
  4. Post convergence report to Slack and store in Attio.

### 6. Handle market adaptation

Even after convergence, external conditions change. The monitoring system detects these shifts:

- **Audience fatigue:** Response rate declines 3+ weeks in a row. Hypothesis: current ICP segment is saturated. Test: expand to adjacent ICP segment or rotate messaging angle.
- **Platform changes:** LinkedIn algorithm or DM policy changes. Hypothesis: new restrictions or behavior changes. Test: adjust volume, timing, or message format.
- **Competitive pressure:** Similar companies start using video DMs (identified via competitive monitoring). Hypothesis: differentiation is eroding. Test: new video format (e.g., screen-only product demo instead of camera + screen).
- **Seasonal patterns:** Response rate dips during predictable periods (holidays, fiscal year-end). Action: reduce volume during known low-response periods, increase during high-response periods. Build a seasonal model after 6+ months of data.

## Time Estimate

- Autonomous optimization setup: 8 hours
- Video outreach performance monitor setup: 4 hours
- DM performance monitor setup: 3 hours
- Guardrail configuration: 2 hours
- Monthly recording and sending (ongoing): 15 hours/month x 12 = 180 hours (shared with Scalable; not additive)
- Weekly brief review: 30 min/week x 50 weeks = 25 hours
- Monthly strategic reviews: 2 hours/month x 12 = 24 hours
- Experiment intervention (when human approval needed): ~1 hour/month x 12 = 12 hours
- **Play management total: ~78 hours over 12 months** (excludes ongoing recording time which continues from Scalable)
- **Including recording time: ~180 hours over 12 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom Business | Personalized video recording with CTAs and analytics | $12.50/creator/mo (annual) — [pricing](https://www.atlassian.com/software/loom/pricing) |
| LinkedIn Sales Navigator Core | InMail, advanced search, buyer intent signals | $79.99/mo (annual) — [pricing](https://business.linkedin.com/sales-solutions/compare-plans) |
| Clay | Prospect enrichment, signal detection, AI hook generation | $185-$495/mo — [pricing](https://university.clay.com/docs/plans-and-billing) |
| n8n | Automation for optimization loop, follow-up routing, reporting | $24/mo (Starter) — [pricing](https://n8n.io/pricing) |
| PostHog | Event tracking, funnels, experiments, anomaly detection | Free up to 1M events/mo — [pricing](https://posthog.com/pricing) |
| Anthropic Claude | Hypothesis generation and experiment evaluation | ~$20-50/mo at optimization loop volume — [pricing](https://www.anthropic.com/pricing) |
| Attio | CRM, experiment logging, campaign notes | Included in standard stack |
| Cal.com | Booking links for video CTAs | Included in standard stack |

**Play-specific cost at Durable:** ~$140-$480/mo (Loom $12.50 + LinkedIn Sales Navigator $79.99 + n8n $24 + Claude API ~$20-50 + Clay $185-$495 if not already on standard stack). At sustained 300 DMs/month with 8% response rate and 25% meeting conversion: estimated $23-$80/meeting.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — PostHog dashboard, anomaly alerts, and weekly video performance briefs feeding the optimization loop
- the dm performance monitor workflow (see instructions below) — DM-specific funnel tracking, send-time heatmaps, and monthly channel health reports
