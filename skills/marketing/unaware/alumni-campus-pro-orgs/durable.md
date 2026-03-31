---
name: alumni-campus-pro-orgs-durable
description: >
  Alumni & Campus Outreach — Durable Intelligence. Always-on AI agents find the local maximum for
  community engagement by running the autonomous optimization loop: detect metric anomalies,
  generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners.
  Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > Unaware"
motion: "Communities & Forums"
channels: "Communities, Other"
level: "Durable Intelligence"
time: "4 hours/month over 6 months"
outcome: "≥ 4 meetings/month sustained for 6 months with autonomous agent maintaining or improving performance; convergence detected when 3 consecutive experiments produce <2% improvement"
kpis: ["Meetings booked per month (trend)", "Cost per meeting (trend)", "Community health score (portfolio weighted average)", "Experiment velocity (experiments completed per month)", "Experiment win rate (%)", "Referral session volume (weekly trend)", "Agent auto-fix count (monthly)", "Time to convergence (weeks)"]
slug: "alumni-campus-pro-orgs"
install: "npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs"
drills:
  - autonomous-optimization
  - community-health-scoring
  - dashboard-builder
---

# Alumni & Campus Outreach — Durable Intelligence

> **Stage:** Marketing → Unaware | **Motion:** Communities & Forums | **Channels:** Communities, Other

## Outcomes

Deploy always-on AI agents that find and maintain the local maximum for community-driven meetings. The agent autonomously detects when metrics plateau or drop, generates hypotheses for what to change, runs controlled experiments, evaluates results, and auto-implements winners. Human involvement drops to reviewing weekly briefs and approving high-risk changes. The play converges when 3 consecutive experiments produce < 2% improvement — at that point, the agent shifts to maintenance monitoring.

## Leading Indicators

- Autonomous optimization loop running on daily cron without errors
- At least 2 experiments completed per month
- Community health scores trending stable or upward across the portfolio
- Weekly optimization briefs generated and posted to Slack on schedule
- Meeting volume holding steady at or above the Scalable baseline (≥ 4/month)
- Cost per meeting stable or declining
- No undetected metric anomalies (all significant changes trigger alerts)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific metrics and levers.

**Configure Phase 1 (Monitor):**
Build an n8n workflow on a daily cron (6am) that checks this play's primary KPIs:

| KPI | PostHog Query | Anomaly Thresholds |
|-----|---------------|--------------------|
| Weekly meetings booked | `alumni_campus_meeting_booked` events, last 7 days | Plateau: ±2% for 3+ weeks. Drop: >30% decline vs 4-week avg. Spike: >50% increase |
| Weekly referral sessions | `alumni_campus_referral_visit` events, last 7 days, grouped by `community_name` | Plateau: ±5% for 3+ weeks. Drop: >40% decline vs 4-week avg |
| Cost per meeting | (Tool costs + time invested) / meetings, last 30 days | Increase: >25% above 4-week avg |
| Conversion rate | Meetings / referral sessions, last 14 days | Drop: >20% decline vs 4-week avg |

Use the `posthog-anomaly-detection` fundamental to implement these checks. When any KPI triggers an anomaly, proceed to Phase 2.

**Configure Phase 2 (Diagnose):**
When an anomaly is detected, the agent gathers context and generates hypotheses:

1. Pull the community health scores (from `community-health-scoring` drill) to identify which specific communities are driving the anomaly
2. Pull the last 8 weeks of metric history from PostHog
3. Pull the current community engagement configuration from Attio: active communities, posting frequency, content types, CTA approaches, timing
4. Run the `hypothesis-generation` fundamental with the anomaly data + context

**Play-specific hypothesis templates:**

For meeting volume drop:
- "Community X's health score dropped from {score_before} to {score_after}; hypothesis: engagement frequency decreased. Test: increase posting to daily for 2 weeks."
- "Conversion rate in Tier 1 communities dropped {X}%; hypothesis: CTA approach fatigue. Test: switch from soft CTA to resource-offer CTA for 2 weeks."
- "Referral sessions stable but meetings declining; hypothesis: landing page or booking flow friction increased. Test: simplify the CTA link to go directly to Cal.com booking page."

For cost per meeting increase:
- "Time invested increased {X}% but meetings flat; hypothesis: Tier 2/3 communities consuming disproportionate effort. Test: pause all Tier 3 engagement for 2 weeks and reallocate to Tier 1."
- "Tool costs increased due to Syften alert volume; hypothesis: keyword filters too broad. Test: tighten filters to reduce alerts by 50% while maintaining coverage of buying-intent signals."

For referral session plateau:
- "Referral sessions flat for 3 weeks across all communities; hypothesis: content topics are repeating. Test: introduce a new content pillar (e.g., industry data analysis) for 3 weeks."
- "Referral sessions flat in top communities but growing in new communities; hypothesis: audience saturation in established communities. Test: reduce frequency in saturated communities and reallocate to growing ones."

3 ranked hypotheses are generated, each with expected impact and risk level. Store in Attio. If top hypothesis is high-risk, send Slack alert for human review and STOP. Otherwise, proceed to Phase 3.

**Configure Phase 3 (Experiment):**
Take the top-ranked hypothesis. Use `posthog-experiments` to create a feature flag or tracking mechanism that splits the test:

- For content/CTA experiments: alternate the approach across comparable communities (not within a single community, to avoid confounding)
- For frequency experiments: change frequency in a subset of communities and keep others as control
- For community portfolio experiments: pause/add communities and compare against the stable set

Experiment constraints:
- Minimum duration: 7 days
- Minimum sample: 10 posts per variant (for content tests) or 50 referral sessions per variant (for conversion tests)
- Maximum 1 active experiment at a time
- Auto-revert if meeting rate drops >30% during the experiment

Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, control group, variant group.

**Configure Phase 4 (Evaluate):**
When the experiment reaches its planned duration or sample size:

1. Pull results from PostHog
2. Run `experiment-evaluation` fundamental with control vs variant data
3. Decision:
   - **Adopt:** Variant outperforms control with ≥95% confidence. Update the live configuration permanently. Log the change.
   - **Iterate:** Results inconclusive or variant slightly better. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Control outperforms variant. Restore original configuration. Log the failure. Wait 7 days before testing the same variable.
   - **Extend:** Insufficient sample size. Keep running for another 7 days.

Store the full evaluation in Attio: decision, confidence level, metric deltas, reasoning.

**Configure Phase 5 (Report):**
Weekly n8n cron (Monday 8am) generates the optimization brief:

```markdown
## Alumni & Campus Outreach — Weekly Optimization Brief ({date_range})

### Performance Summary
- Meetings booked this week: {count} (target: ≥ 1/week)
- Meetings booked (30-day rolling): {count} (target: ≥ 4/month)
- Cost per meeting (30-day rolling): ${amount}
- Portfolio health score: {score}/100

### Optimization Activity
- Anomalies detected: {count} ({list types})
- Hypotheses generated: {count}
- Experiments running: {count} (experiment name, day {X} of {Y})
- Experiments completed: {count} (outcome: Adopt/Iterate/Revert)
- Net metric impact from adopted changes: {±X%} on {metric}

### Community Portfolio Changes
- Communities promoted: {list}
- Communities demoted: {list}
- Communities archived: {list}
- New communities added: {list}

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Estimated distance from local maximum: {assessment}
- Recommended focus for next week: {recommendation}

### Human Actions Required
{List any items requiring human approval or intervention}
```

Post to Slack and store in Attio.

### 2. Deploy community health scoring

Run the `community-health-scoring` drill to maintain a living scorecard for every community in the portfolio. This runs on a weekly automated cadence and produces:

- A 0-100 health score for each community based on referral volume (30%), conversion rate (25%), engagement efficiency (20%), trend (15%), and pipeline attribution (10%)
- Community classification: thriving (80-100), healthy (60-79), watch (40-59), declining (20-39), dormant (0-19)
- Automated reallocation recommendations: which communities to invest more in, maintain, reduce, or archive
- Anomaly alerts for sudden changes in any community's performance

The health scoring data feeds directly into the autonomous optimization loop's hypothesis generation. When the optimization loop detects a portfolio-level anomaly, it uses community-level health data to pinpoint which specific communities are causing the change and generate targeted hypotheses.

### 3. Build the durable operations dashboard

Run the `dashboard-builder` drill to create: "Alumni & Campus Outreach — Durable Operations"

**Panel layout:**

Row 1 — Key metrics (large number tiles):
- Meetings booked (30-day rolling)
- Cost per meeting (30-day rolling)
- Portfolio health score (weighted average)
- Active experiments count

Row 2 — Trends:
- Meetings per week (line chart, 12 weeks, with Scalable baseline as reference line)
- Referral sessions per week by community tier (stacked area chart, 12 weeks)
- Cost per meeting (line chart, 12 weeks, with $50 target as reference line)

Row 3 — Community portfolio:
- Community health leaderboard (table: community name, health score, classification, trend arrow, meetings, efficiency)
- Community tier distribution (pie chart: Tier 1/2/3/Archived)

Row 4 — Optimization:
- Experiment history (table: experiment name, hypothesis, start date, duration, outcome, metric impact)
- Convergence tracker (line chart: improvement % from each experiment over time)

Set dashboard alerts:
- Portfolio health score drops below 60 → Slack alert
- No experiments completed in 14 days → Slack alert (optimization stalled)
- Meeting volume drops below Scalable baseline for 2 consecutive weeks → Slack alert + flag for human review

### 4. Configure convergence detection

The optimization loop runs indefinitely until convergence. Convergence is detected when **3 consecutive experiments produce < 2% improvement** on the primary metric (meetings booked).

At convergence:
1. The agent posts a convergence report: "This play has reached its local maximum. Current performance: {X} meetings/month at ${Y} cost per meeting. The community portfolio is producing at maximum efficiency given the current market, audience, and competitive landscape."
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment frequency to 1 per month (maintenance testing)
4. Continue community health scoring weekly to detect external changes (new competitor entering communities, community platform changes, audience shifts)

If post-convergence monitoring detects a significant metric change (>15% decline sustained for 2+ weeks), the agent re-enters the full optimization loop and resets the convergence counter.

### 5. Establish human review cadence

**Human action required (monthly):**
- Review the last 4 weekly optimization briefs
- Approve or reject any queued high-risk experiments
- Review community health scores and approve any recommended archiving of communities
- Assess whether strategic changes are needed (new community types, new content pillars, product changes that affect community messaging)
- Estimated time: 1 hour/month

**Human action required (quarterly):**
- Full portfolio review: are we in the right communities for our current ICP?
- Re-run `community-reconnaissance` to discover new communities
- Assess whether the play should be expanded (more budget for premium community memberships) or consolidated (fewer communities with deeper engagement)
- Estimated time: 2 hours/quarter

## Time Estimate

- Autonomous optimization loop setup: 6 hours (one-time)
- Community health scoring setup: 3 hours (one-time)
- Dashboard build: 3 hours (one-time)
- Monthly human review: 1 hour/month x 6 months = 6 hours
- Quarterly strategic review: 2 hours/quarter x 2 = 4 hours
- Incident response (estimated): 2 hours over 6 months
- **Total: ~4 hours/month over 6 months (24 hours total, including one-time setup)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, funnels | Free tier: 1M events/mo; paid: usage-based (https://posthog.com/pricing) |
| n8n | Optimization loop cron, monitoring workflows, alert routing | €60/mo Pro cloud for 10K executions; free self-hosted (https://n8n.io/pricing) |
| Syften | Real-time keyword monitoring across community platforms | $99.95/mo Pro plan (https://syften.com/) |
| Attio | Community portfolio management, experiment log, contact attribution | Free tier or paid (https://attio.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, content adaptation | Usage-based; ~$10-30/mo at this play's volume (https://anthropic.com/pricing) |
| Clay | Quarterly community rediscovery | $185/mo Launch plan; run only during quarterly reviews (https://clay.com/pricing) |

**Estimated play-specific cost at Durable level:** $170-390/mo (n8n Pro + Syften Pro + Anthropic API + Clay during quarterly reviews)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop that detects anomalies, generates hypotheses, runs experiments, evaluates results, and auto-implements winners
- `community-health-scoring` — weekly automated scoring and ranking of every community in the portfolio by engagement ROI
- `dashboard-builder` — build the PostHog operations dashboard with real-time visibility into play performance, community health, and optimization activity
