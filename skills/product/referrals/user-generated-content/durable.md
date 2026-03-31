---
name: user-generated-content-durable
description: >
  UGC Campaign — Durable Intelligence. Autonomous AI agents manage the entire UGC system:
  detect anomalies in submission rates, creator engagement, and amplification performance;
  generate hypotheses for what to change; run A/B experiments on prompts, incentives, and
  amplification channels; auto-implement winners; and produce weekly optimization briefs.
  The system finds the local maximum for UGC volume, quality, and referral impact.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Referrals"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: ">=40 approved UGC pieces/month sustained for 6 months with >=150 referral visits/month and <=3 hours/week team involvement"
kpis: ["Monthly approved UGC volume trend (stable or growing over 6 months)", "Monthly unique creators (target >=15 sustained)", "Repeat creator rate (target >=30%)", "Monthly referral visits from UGC (target >=150)", "Monthly referral signups from UGC (target >=8)", "Cost per approved UGC piece trend (flat or decreasing)", "Creator program health index (% of metrics in healthy range)"]
slug: "user-generated-content"
install: "npx gtm-skills add product/referrals/user-generated-content"
drills:
  - autonomous-optimization
  - ugc-health-monitor
  - dashboard-builder
---

# UGC Campaign — Durable Intelligence

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Referrals

## Outcomes

The UGC system runs autonomously. AI agents monitor the entire pipeline — from prompt impressions through content creation, moderation, amplification, and referral conversion. When any metric anomaly is detected (submission rate drops, approval rate declines, referral traffic stalls, creator retention weakens), the agent diagnoses the cause, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. Weekly optimization briefs summarize what changed and why. The system finds the local maximum for UGC volume, content quality, and referral impact, then maintains it as user behavior and market conditions change.

Pass: >=40 approved UGC pieces per month sustained for 6 consecutive months, >=150 referral visits per month from UGC, >=30% repeat creator rate, and <=3 hours per week of team involvement (reviewing briefs only).
Fail: UGC volume declines below 25 pieces per month for 3 consecutive weeks despite automated interventions, or the system requires more than 5 hours per week of manual effort.

## Leading Indicators

- The `autonomous-optimization` loop produces a winning experiment at least once per month for the first 3 months (there is still optimization headroom)
- Creator program health index stays above 75% (>=6 of 8 metrics in healthy range)
- Referral visit volume from UGC grows or holds steady month-over-month for 4+ months (amplification is compounding)
- The repeat creator rate climbs above 30% (the incentive and recognition system creates lasting motivation)
- Successive experiments produce diminishing returns after month 4 (convergence toward local maximum — this is the goal)
- Weekly optimization briefs are generated and delivered without human triggering

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for the UGC pipeline. This is the core of Durable — an always-on agent that monitors, diagnoses, experiments, and implements.

**Configure the monitoring phase (daily via n8n cron):**

Use the `ugc-health-monitor` drill's 8 metrics as the primary KPIs for anomaly detection. The agent checks daily:

- Submission rate (weekly rolling vs 4-week rolling average)
- Approval rate (trailing 30-day)
- Prompt-to-submission conversion rate (by trigger type)
- Creator diversity (unique creators / total submissions)
- Repeat creator rate
- Amplification throughput (amplified / approved)
- Referral traffic from UGC (clicks and visits)
- Content quality trend (average moderation composite score)

Classification thresholds (from `autonomous-optimization`):
- **Normal:** within +/- 10% of 4-week rolling average
- **Plateau:** within +/- 2% for 3+ weeks
- **Drop:** >20% decline from rolling average
- **Spike:** >50% increase (investigate — could be a contest effect or could be spam submissions)

If anomaly detected on any metric: trigger the diagnosis phase.

**Configure the diagnosis phase (triggered by anomaly):**

The agent gathers context:
1. Pull current UGC system configuration from Attio: active prompt variants, contest status, tier distribution, amplification schedule
2. Pull 8-week metric history from PostHog via the `ugc-health-monitor` dashboard
3. Pull creator behavior breakdown: are new creators declining, or are existing creators stopping?
4. Pull amplification channel performance: did a specific channel stop driving traffic?
5. Run `hypothesis-generation` with the anomaly data + context

Example hypotheses the agent might generate:
- "Submission rate dropped 25% because the post-activation prompt has been live for 8 weeks and users have seen it too many times. Hypothesis: rotate to a new prompt variant with different copy and a different ask (tip vs testimonial)."
- "Repeat creator rate declined from 28% to 18% because the Active Creator badge is not visible enough in the product UI. Hypothesis: add a notification when a non-creator sees content from a badged creator, highlighting the badge."
- "Referral traffic from LinkedIn UGC posts dropped 30% while in-product showcase referrals held steady. Hypothesis: LinkedIn algorithm change reduced post reach. Test video-format UGC posts (LinkedIn prioritizes native video)."
- "Approval rate dropped from 65% to 40% because the latest contest theme attracted low-effort submissions. Hypothesis: add a minimum quality guideline to the submission form ('include at least one specific result or number')."
- "Content quality trend declining. Hypothesis: the moderation threshold is too lenient. Increase the approve threshold from 3.5 to 3.8 composite score."

Store hypotheses in Attio. If risk = "high" (e.g., changing the moderation threshold, restructuring the tier system, pausing a contest), send Slack alert and wait for human approval. Otherwise proceed to experiment.

**Configure the experiment phase (triggered by hypothesis acceptance):**

Use PostHog feature flags to split traffic for prompt experiments. For incentive experiments, split by user cohort. The agent:
1. Creates the variant (new prompt copy, adjusted timing, modified incentive, new amplification format)
2. Sets up the PostHog experiment with control vs variant
3. Defines the primary metric (e.g., prompt conversion rate for prompt experiments, repeat rate for incentive experiments) and secondary metrics (content quality as a guard)
4. Sets experiment duration: minimum 14 days or 300 prompt impressions per variant, whichever is longer
5. Logs the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Configure the evaluation phase (triggered by experiment completion):**

The agent pulls PostHog experiment results and runs `experiment-evaluation`:
- **Adopt:** The variant wins with >=95% statistical significance and improvement >=5% relative. Content quality did not decline. Update the live system. Log in Attio.
- **Iterate:** Inconclusive or improvement <5%. Generate a refined hypothesis. Return to diagnosis.
- **Revert:** Variant performed worse, or content quality declined >15%. Restore control. Log the failure. Return to monitoring.

**Guardrails (enforced by n8n):**
- Maximum 1 active experiment per UGC subsystem at a time (prompts, incentives, and amplification can each have 1 concurrent experiment)
- If submission rate drops >40% during an experiment, auto-revert immediately
- If approval rate drops below 30% for 2 consecutive weeks, pause all experiments and alert the team
- Maximum 4 experiments per month total. If all 4 fail, pause optimization and flag for human strategic review
- Never auto-modify contest prize structures or creator tier definitions without human approval
- Always monitor content quality alongside volume. Optimizing submission rate at the expense of quality is a false win

### 2. Build the performance dashboard

Run the `dashboard-builder` drill to create the Durable-level PostHog dashboard:

**Dashboard panels:**
- **UGC pipeline funnel:** `ugc_prompt_shown` -> `ugc_prompt_clicked` -> `ugc_form_completed` -> `ugc_submitted` -> `ugc_moderated` -> `ugc_approved` -> `ugc_amplified` -> `ugc_amplified_clicked` (8-week trend with Scalable baseline)
- **Submission volume trend:** weekly approved pieces, 8-week rolling with 40/month threshold line
- **Creator ecosystem heatmap:** tier distribution (First-time, Active, Featured) over time
- **Creator health index:** percentage of 8 health metrics in healthy range
- **Repeat creator trend:** 4-week rolling repeat rate with 30% threshold line
- **Channel performance:** referral visits per amplification channel (LinkedIn, email, in-product, blog, community)
- **Contest impact:** submission volume before, during, and after each contest
- **Active experiment status:** current tests, variants, days running, interim metrics
- **Prompt fatigue tracker:** per-trigger prompt conversion rate over 8 weeks (declining rates signal copy fatigue)
- **Quality trend:** average moderation composite score, 8-week rolling with 3.5 threshold
- **Cost per UGC piece:** monthly trend (tool costs + contest prizes + credits / approved pieces)
- **Referral conversion funnel:** UGC click -> visit -> signup -> activation

**Alerts (via n8n):**
- Submission rate drops below 3 per week for 2+ consecutive weeks -> investigate prompt performance
- Approval rate drops below 40% for 2 consecutive weeks -> investigate content quality or moderation calibration
- Repeat creator rate drops below 20% for 3 weeks -> investigate incentive effectiveness
- Referral traffic declines >25% month-over-month -> investigate amplification channel performance
- No experiments completed in 21+ days -> check if the optimization loop is running
- Zero submissions for 5 consecutive days -> pipeline may be broken, check webhooks

### 3. Deploy the UGC-specific monitoring layer

Run the `ugc-health-monitor` drill as the play-specific complement to `autonomous-optimization`. This provides the 8 UGC health metrics, diagnostic triggers, automated interventions, and weekly health reports that feed the optimization loop.

Configure the interventions:
- **Prompt fatigue:** auto-rotate to next prompt variant when conversion drops below 2% for 2 weeks
- **Repeat rate stall:** trigger "comeback creator" email to First-time Creators who submitted 30-60 days ago
- **Amplification backlog:** alert content team when >10 approved pieces remain unshared for 7+ days
- **Quality decline:** add quality guidance to submission form when average drops below 3.0

The weekly health report feeds directly into the `autonomous-optimization` diagnosis phase. If a metric consistently underperforms after 2+ optimization attempts, the agent recommends a strategic change (new contest format, restructured tiers, new amplification channel) and escalates to the team.

### 4. Generate weekly optimization briefs

Build an n8n workflow (configured in `autonomous-optimization` Phase 5) that runs every Monday and delivers:

1. **Status summary:** Approved UGC this week, total referral visits, comparison to prior 4-week average and Scalable baseline
2. **Creator ecosystem:** New creators this week, tier promotions, top contributor spotlight
3. **Pipeline health:** 8-metric health check summary (healthy/warning/critical counts)
4. **Experiment update:** What experiment ran, what the result was, what was implemented or reverted
5. **Content quality check:** Average composite score this week vs baseline. Any quality concerns?
6. **Amplification report:** Per-channel metrics (impressions, clicks, referral visits)
7. **Anomaly report:** Any anomalies detected and how the agent responded
8. **Next week plan:** What the agent plans to test or investigate next
9. **Distance from local maximum:** Are experiments still producing improvements, or has the system converged?

Deliver via Slack to the team. Store in Attio as a note on the UGC program record.

**Human action required:** The team reads the weekly brief (5 minutes). If the brief recommends a strategic change (new contest type, tier restructure, new amplification channel), the team decides. All tactical changes (prompt copy rotation, amplification scheduling, incentive tuning within approved parameters) execute automatically.

### 5. Run monthly deep review

Build an n8n workflow that runs on the 1st of each month:

1. Pull 30-day aggregate metrics across the entire UGC pipeline
2. Compare to prior month and to the Scalable baseline
3. Creator ecosystem analysis: growth in each tier, churn from the program, creator lifetime value (total approved pieces per creator)
4. Content portfolio analysis: which content types generate the most referral traffic? Which amplification channels have the best ROI?
5. Contest analysis: participation trends, quality trends, post-contest retention
6. Calculate: cost per approved piece, cost per referral visit, cost per referral signup
7. Flag convergence: if 3 consecutive experiments produced <2% improvement, the UGC system has reached its local maximum. Recommend reducing experimentation frequency.

**Human action required:** The team reviews the monthly brief (~15 minutes) and decides on program-level changes.

### 6. Sustain for 6 months

The system runs continuously. The agent's responsibilities:
- Monitor the full UGC pipeline daily for anomalies
- Run the optimization loop: detect -> diagnose -> experiment -> evaluate -> implement
- Generate weekly optimization briefs and monthly deep reviews
- Rotate prompt copy when fatigue is detected
- Manage contest lifecycle automatically each month
- Monitor creator engagement and trigger re-engagement when creators go dormant
- Track content quality alongside volume (never sacrifice quality for volume)
- Detect convergence and reduce optimization intensity when the local maximum is reached

The team's responsibilities:
- Read the weekly Slack brief (5 minutes)
- Approve strategic changes flagged in the monthly review (~15 minutes/month)
- Approve high-risk experiments (tier changes, contest restructuring, moderation threshold changes)
- Fulfill manual rewards (swag shipping for Featured Creators)

### 7. Evaluate sustainability after 6 months

Compute over the full 6-month period:
- Monthly approved UGC volume for each of the 6 months (target: >=40 every month)
- Monthly unique creators for each month (target: >=15 every month)
- Repeat creator rate trend (target: stable or improving toward 30%+)
- Monthly referral visits from UGC for each month (target: >=150 every month)
- Monthly referral signups attributed to UGC (target: >=8 every month)
- Creator tier distribution at month 6 vs month 1 (is the ecosystem growing?)
- Total cost / total approved pieces = cost per piece
- Total cost / total referral signups = cost per referral acquisition
- Number of A/B experiments run, number that produced significant improvements
- Convergence status: has the system found its local maximum?
- Team hours per week average over the 6 months (target: <=3 hours)

- **PASS (>=40 pieces/month and >=150 referral visits/month for all 6 months, <=3 hours/week team time):** The UGC system is a self-optimizing referral engine. The flywheel of prompts, creation, moderation, amplification, and social proof runs autonomously. Consider: expanding to new content types (video tutorials, template libraries), launching a formal creator partnership program, or syndicating UGC to third-party platforms for broader reach.
- **CONVERGED (volume stable at 40+ pieces but experiments no longer produce gains):** The local maximum has been found. Reduce the optimization loop from daily to weekly monitoring. Shift experiment resources to other plays. The UGC system is in maintenance mode.
- **DECLINING (volume held for 4+ months then decayed):** Creator fatigue or market change. The agent should detect this via anomaly monitoring and recommend strategic changes: new contest formats, restructured incentives, new content types, or a creator refresh campaign.
- **FAIL (volume below 25 pieces/month for 3+ consecutive weeks at any point):** The optimization loop is not adapting fast enough. Diagnose: Is the user base still growing? Are prompts being shown to enough new users? Has a product change reduced the number of success events that trigger prompts? Fix the specific broken component or accept that this play requires more manual curation than autonomous optimization.

## Time Estimate

- Autonomous optimization loop setup: 16 hours (Month 1)
- Dashboard and alert system: 8 hours (Month 1)
- UGC health monitor deployment: 6 hours (Month 1)
- Weekly brief and monthly review workflows: 4 hours (Month 1)
- Setup subtotal: 34 hours
- Weekly agent monitoring and optimization: 3 hours/week x 24 weeks = 72 hours
- Weekly team time: 20 min/week x 24 weeks = 8 hours
- Monthly team review: 15 min x 6 months = 1.5 hours
- Monthly contest management (agent-automated): 4 hours/month x 6 months = 24 hours
- Experiment execution: 2 hours/month x 6 months = 12 hours
- Ongoing subtotal: ~117.5 hours
- Grand total: ~160 hours over 6 months (140 agent, 10 team, 10 buffer)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, A/B experiments, feature flags, anomaly detection, dashboards | Free tier: 1M events/mo; paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | All automation: optimization loop, monitoring, contests, amplification | Pro EUR60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM: UGC Library, creator records, experiment log, optimization history | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Intercom | In-app prompts, UGC showcases, contest banners | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Creator sequences, newsletter features, contest and re-engagement emails | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | AI moderation + hypothesis generation + experiment evaluation + brief generation | Usage-based ~$3/1M input tokens for Sonnet ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Durable:** $275-425/mo (n8n Pro + Attio Plus + Intercom + Loops + contest prizes ~$100/month + Anthropic API usage)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect anomalies in UGC submission rates, creator engagement, and amplification performance; generate improvement hypotheses; run A/B experiments on prompts, incentives, and channels via PostHog; evaluate results; auto-implement winners; and produce weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `ugc-health-monitor` — play-specific monitoring for the UGC pipeline: 8 health metrics (submission rate, approval rate, prompt conversion, creator diversity, repeat rate, amplification throughput, referral traffic, quality trend) with diagnostics, automated interventions, and weekly reports that feed the optimization loop
- `dashboard-builder` — build the Durable PostHog dashboard with full pipeline funnel, creator ecosystem heatmap, channel performance, experiment status, quality trends, and cost-per-piece tracking
