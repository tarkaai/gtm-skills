---
name: list-swaps-adjacent-startups-durable
description: >
  List Swap With Partner — Durable Intelligence. Always-on AI agents monitor
  per-partner swap performance, detect audience fatigue, generate optimization
  hypotheses, run email A/B tests, and auto-implement winners. Weekly
  optimization briefs. Converges when successive experiments produce <2%
  improvement.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving clicks and meetings over 6 months; click-to-meeting conversion at or above Scalable peak; agents detect audience fatigue, email decay, reciprocity imbalance, and seasonal patterns, adapting automatically."
kpis: ["Click-through rate", "Email open rate", "Click-to-meeting rate", "Meetings per swap", "Partner retention rate", "Audience fatigue index", "Experiment win rate"]
slug: "list-swaps-adjacent-startups"
install: "npx gtm-skills add marketing/solution-aware/list-swaps-adjacent-startups"
drills:
  - autonomous-optimization
  - list-swap-performance-reporting
---

# List Swap With Partner — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

An always-on optimization system that manages the list swap partner portfolio autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies across partners and email variants, generate improvement hypotheses, run A/B experiments on swap email copy and landing pages, evaluate results, and auto-implement winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement — the play has reached its local maximum.

Sustained or improving click and meeting volume over 6 months. Click-to-meeting conversion rate at or above the Scalable peak. The agent detects and adapts to audience fatigue (declining clicks from a partner's list over repeated swaps), email decay (a once-effective subject line or copy angle losing impact), reciprocity imbalance (one side consistently giving more value), and seasonal patterns (conference season, holiday lulls, budget cycles).

## Leading Indicators

- Anomaly detection fires within 24 hours of a metric shift (signal: monitoring is working)
- At least 1 experiment runs per 2-week period (signal: optimization loop is active)
- Experiment win rate >= 30% (signal: hypotheses are well-targeted)
- No partner drops below 50% of their historical click average for 3+ consecutive swaps without a corrective action firing (signal: fatigue detection works)
- Weekly optimization brief posts on time every Friday (signal: reporting pipeline is stable)
- Time between anomaly detection and experiment launch <72 hours (signal: the loop is tight)
- Partner portfolio size stays at 10+ active partners (signal: replacement pipeline keeps pace with churn)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific metrics and levers:

**Monitor phase (daily via n8n cron):**
- Pull list swap KPIs from PostHog: clicks, meetings, click-to-meeting CVR, per-partner performance, email variant performance
- Compare last 2 weeks against 4-week rolling average
- Classify each metric as: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase)
- Per-partner anomaly detection: flag any partner whose clicks dropped >30% from their rolling average
- Per-variant anomaly detection: flag any email variant whose CTR dropped >25% from its historical average
- Reciprocity check: flag any partner where net swap value exceeds 3x in either direction for 2+ consecutive swaps
- If anomaly detected, trigger the Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context: which partners are affected, which email variants were used, when was the last swap, what is the partner's historical trend, how many times has this partner's audience seen your email
- Pull 8-week per-partner metric history from PostHog
- Run hypothesis generation with the anomaly data. Common hypotheses for this play:
  - "Partner X's audience is fatigued — same subscribers seeing similar swap emails for 3+ months. Prescribe: cooldown period or entirely new email angle."
  - "Email variant Y has decayed — CTR dropped 40% over 4 swaps. Prescribe: retire variant, generate new one."
  - "Landing page conversion dropped — swap traffic still arrives but does not convert. Prescribe: A/B test a new headline or CTA."
  - "Partner Z's list engagement is declining overall — their open rates are down across all content, not just our swaps. Prescribe: monitor, not our problem to fix."
  - "Reciprocity imbalance with Partner W — they get 3x more value. Prescribe: renegotiate cadence or request larger list segment."
  - "Seasonal effect — January ramp-up after holiday lull / conference season distraction. Prescribe: adjust expectations, do not over-react."
- Store hypotheses in Attio. If risk = "high" (e.g., changing the landing page for all swap traffic, or retiring a top-3 partner), alert for human review.

**Experiment phase (triggered by hypothesis acceptance):**
- Design the experiment. For this play, the primary experiment types are:
  1. **Email A/B test**: Send variant A to half the partner portfolio, variant B to the other half. Measure click-to-meeting CVR per variant after 2 weeks. Tag each variant with a unique `utm_content`.
  2. **Subject line A/B test**: Same email body, different subject lines across similar partners. Measure open rate and CTR.
  3. **Landing page A/B test**: Use PostHog feature flags to show different landing page variants to swap traffic. Measure conversion rate per variant.
  4. **CTA test**: Test different CTA copy and commitment levels (e.g., "See the 2-minute walkthrough" vs. "Book a 15-minute demo") across partners.
  5. **Partner rotation test**: Replace an underperforming partner with a new prospect from the pipeline and compare results over 2 swaps.
  6. **Send time test**: Test Tuesday vs. Thursday sends across similar partners. Measure open rate and click velocity.
- Use PostHog experiments for landing page and CTA tests. For email and subject line tests, track by `utm_content` variant.
- Minimum experiment duration: 7 days or 4+ swaps across the test group, whichever is longer.

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation:
  - **Adopt**: Winning variant becomes the new default. Update email templates or landing page. Log the change in Attio.
  - **Iterate**: Result was inconclusive or showed a promising direction. Generate a refined hypothesis and re-test.
  - **Revert**: Variant performed worse. Restore the control. Wait 7 days before testing the same variable.
  - **Extend**: Insufficient data (too few swaps in the test period). Keep the experiment running for another cycle.
- Store the full evaluation in Attio with decision, confidence level, and reasoning.

**Report phase (weekly, Friday 3pm via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted experiments
- Generate the weekly optimization brief (see step 2)

### 2. Deploy play-specific monitoring and reporting

Run the `list-swap-performance-reporting` drill to build the monitoring layer specific to this play:

**Swap dashboard in PostHog:**
- Clicks by partner (bar chart, last 30 days)
- Meetings by partner (bar chart, last 30 days)
- Click-to-meeting CVR by partner (table, sorted descending)
- Clicks over time (trend line, last 90 days)
- Email variant performance (table, clicks and meetings by `utm_content`)
- Swap funnel for list-swap traffic (pageview → CTA click → meeting booked)
- Reciprocal performance (how your list responded to each partner's email)
- Audience fatigue tracker (click trend per partner over last 6 swaps)

**Weekly swap brief (automated, Friday 3pm):**
```
## List Swap Weekly Brief — {date}

**This week**: {total_clicks} clicks, {total_meetings} meetings ({cvr}% click-to-meeting)
**vs 4-week avg**: {change_pct}% {up/down}
**Swaps completed**: {count} | **Partner portfolio**: {active_count} active

### Top partners by meetings
1. {partner_1}: {clicks} clicks, {meetings} meetings ({cvr}%)
2. {partner_2}: {clicks} clicks, {meetings} meetings ({cvr}%)

### Anomalies detected
- {partner/metric}: {description} — {hypothesis generated}

### Reciprocity check
- Imbalanced partners: {list with net value ratios}

### Experiments this week
- {experiment}: {status} — {result or ETA}

### Adopted changes
- {change}: {impact on metrics}

### Audience fatigue status
- Partners in cooldown: {list}
- Partners approaching fatigue threshold: {list}

### Convergence status
{distance from local maximum estimate}
{recommended focus for next week}
```

**Per-partner ROI tracking in Attio:**
- Total swaps, clicks, meetings, click-to-meeting rate, net swap value, best email variant, audience fatigue index, partner health score
- Updated weekly by n8n automation

**Performance alerts:**
- Partner clicks drop >50% swap-over-swap → investigate fatigue or list quality decline
- New partner's first swap exceeds 40 clicks → flag for fast-track to monthly cadence
- Total meetings drop below Scalable baseline for 2 consecutive weeks → trigger autonomous optimization investigation
- Email variant achieves >8% CTR → mark as "proven template"
- Your list's unsubscribe rate exceeds 0.5% on any inbound swap → pause swaps with that partner and review

### 3. Manage partner portfolio health

The agent autonomously manages the partner portfolio:

- **Audience fatigue detection**: If a partner's click rate declines for 3 consecutive swaps, the agent pauses swaps with that partner for 6 weeks (cooldown period). After cooldown, test with a completely new email angle and subject line. If the second attempt also shows fatigue, retire the partner and source a replacement.
- **Partner graduation**: Partners consistently generating >3 meetings per swap get escalated to deeper partnerships (joint webinars, co-created content, referral agreements, product integrations). Log the recommendation in Attio for human review.
- **Partner replacement**: When a partner is retired (fatigue, declining list quality, or low ROI), the agent triggers the `partner-prospect-research` drill to source a replacement from the pipeline. Maintain 10+ active partners at all times.
- **Seasonal adjustment**: The agent learns seasonal patterns (lower engagement in December, higher in January/September, dips during major conference weeks) and adjusts swap cadence accordingly rather than flagging expected dips as anomalies.
- **Reciprocity management**: If a partner consistently receives 3x+ more value than they provide over 3+ swaps, the agent recommends: (a) requesting a larger segment of their list, (b) reducing cadence, or (c) negotiating additional value (social media shoutout, product mention). Log the recommendation for human action.

### 4. Guardrails

- **Maximum 1 active experiment at a time.** Never stack email tests with landing page tests simultaneously.
- **Revert threshold**: If total clicks drop >30% during an experiment period, auto-revert immediately.
- **Human approval required for:**
  - Retiring a partner that generates >25% of total meetings
  - Landing page changes affecting non-swap traffic
  - Any experiment the hypothesis generator flags as "high risk"
  - Proposing partnership escalation (joint webinars, integrations)
- **Cooldown**: After a failed experiment, wait 7 days before testing the same variable.
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for human strategic review.
- **Never retire more than 2 partners in the same month** without human approval (prevents portfolio collapse).
- **List protection**: Never exceed 4 inbound swaps per month to your own list. If experiment design requires more, use a subset of partners.

### 5. Convergence detection

The optimization loop runs continuously. It detects convergence when:
- 3 consecutive experiments produce <2% improvement in the primary metric (meetings per swap)
- The play has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per month (maintenance mode)
3. Report: "List swaps has converged. Current performance: {metrics}. Anchor partners: {list}. Further gains require strategic changes (new partner categories, different audience segments, different swap formats like joint webinars or co-created content) rather than tactical email/landing page optimization."

## Time Estimate

- Autonomous optimization setup: 20 hours
- List swap performance reporting setup: 10 hours
- Initial monitoring and tuning (month 1): 20 hours
- Ongoing oversight (months 2-6, ~6 hours/month): 30 hours
- Experiment design and evaluation: 40 hours
- Partner portfolio management: 30 hours
- Strategic reviews and course corrections: 50 hours

Total: ~200 hours over 6 months (heavily front-loaded; agent handles most ongoing work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop orchestration, scheduling, alerts | Cloud Pro: ~EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, experiment logs, ROI tracking | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, briefs | Sonnet 4.6 API: ~$15-30/mo at this usage ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Loops | Reciprocal swap sends to your list | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Crossbeam | Partner account overlap (ongoing portfolio optimization) | Free tier for basic; Connector from ~$400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |

**Estimated cost for this level: ~$150-350/mo** (n8n Pro + Attio Plus + Anthropic API + Loops required; Crossbeam and PostHog within free tiers for most usage)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum
- `list-swap-performance-reporting` — per-partner dashboards, weekly briefs, ROI tracking, fatigue detection, and alerts specific to this play
