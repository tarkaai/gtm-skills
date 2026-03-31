---
name: reseller-affiliate-program-durable
description: >
  Reseller & Affiliate Program — Durable Intelligence. Always-on AI agents monitor
  per-partner performance, optimize commission tiers, A/B test onboarding sequences
  and partner enablement assets, and auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained ≥20 partner-sourced paid conversions/quarter and ≥5x commission ROI over 12 months; agents detect partner fatigue, commission inefficiency, and market shifts, adapting automatically."
kpis: ["Sustained conversion volume", "Commission ROI trend", "Partner retention rate", "AI experiment win rate", "Revenue per active partner", "Activation rate trend"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - autonomous-optimization
---

# Reseller & Affiliate Program — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

An always-on optimization system that manages the affiliate/reseller portfolio autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies across partners, commission tiers, and onboarding sequences, generate improvement hypotheses, run A/B experiments on enablement assets and program structure, evaluate results, and auto-implement winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement — the program has reached its local maximum.

Sustained ≥20 partner-sourced paid conversions per quarter and ≥5x commission ROI over 12 months. The agent detects and adapts to partner fatigue (declining referral volume from long-tenured partners), commission inefficiency (partners earning commissions on customers who would have converted anyway), onboarding decay (new partners activating slower over time), and market shifts (new competitors launching rival affiliate programs, changes in partner audience behavior).

## Leading Indicators

- Anomaly detection fires within 24 hours of a metric shift (signal: monitoring is working)
- At least 1 experiment runs per 2-week period (signal: optimization loop is active)
- Experiment win rate ≥30% (signal: hypotheses are well-targeted)
- No partner drops below 50% of their historical average for 3+ consecutive months without a corrective action firing (signal: partner fatigue detection works)
- Weekly optimization brief posts on time every Friday (signal: reporting pipeline is stable)
- Time between anomaly detection and experiment launch <72 hours (signal: the loop is tight)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific metrics and levers:

**Monitor phase (daily via n8n cron):**
- Pull affiliate program KPIs from PostHog: clicks, signups, paid conversions, revenue, commission ROI, per-partner performance
- Pull commission and payout data from the Rewardful API
- Compare last 2 weeks against 4-week rolling average
- Classify each metric as: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase)
- Per-partner anomaly detection: flag any partner whose conversions dropped >40% from their rolling average
- Per-tier anomaly detection: flag if an entire tier's performance shifts (e.g., all Gold partners declining — may indicate market change vs. individual partner issue)
- If anomaly detected, trigger the Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context: which partners are affected, what tier they are in, when was their last referral, what onboarding cohort they belong to, what enablement assets they received
- Pull 8-week per-partner metric history from PostHog
- Pull commission history from Rewardful: are commissions correctly incentivizing behavior?
- Run hypothesis generation with the anomaly data. Common hypotheses for this play:
  - "Partner X's audience is saturated — they have promoted us 10+ times to the same audience"
  - "Gold tier commission rate is too high — partners at this level would refer regardless of the extra 5%"
  - "Onboarding sequence variant B is producing 30% slower activation than variant A"
  - "Competitor Y launched an affiliate program with 25% commission — our top partners may be considering switching"
  - "Seasonal effect — Q4 budget freezes reducing conversion rates across all partners"
  - "Partner type 'content creators' declining as a category — investigate whether their audiences have shifted"
- Store hypotheses in Attio. If risk = "high" (e.g., changing commission structure for all partners), alert for human review.

**Experiment phase (triggered by hypothesis acceptance):**
- Design the experiment. For this play, the primary experiment types are:
  1. **Onboarding A/B test**: Split new partners into two onboarding sequences (different drip timing, content, or activation incentives). Measure time-to-first-referral per variant.
  2. **Enablement asset A/B test**: Distribute different email blurb copy or social post templates to different partner segments. Track which assets produce more referral clicks.
  3. **Commission structure test**: Test a modified commission tier threshold or rate with a subset of partners. Measure whether the change affects referral volume and ROI.
  4. **Partner reactivation test**: For dormant partners, test different re-engagement approaches (bonus commission for 30 days, new product feature announcement, personalized performance summary showing their "missed earnings").
  5. **Recruitment channel test**: Test different outreach approaches or candidate sources for partner recruitment. Measure qualified partner yield.
- Use PostHog experiments for onboarding and enablement tests (feature flags split traffic). For commission tests, use Rewardful campaign segments.
- Minimum experiment duration: 14 days or 20+ partners per variant, whichever is longer.

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog and Rewardful
- Run experiment evaluation:
  - **Adopt**: Winning variant becomes the new default. Update onboarding sequence, enablement assets, or commission structure. Log the change.
  - **Iterate**: Result was inconclusive or showed a promising direction. Generate a refined hypothesis and re-test.
  - **Revert**: Variant performed worse. Restore the control. Wait 14 days before testing the same variable.
- Store the full evaluation in Attio with decision, confidence, and reasoning.

**Report phase (weekly, Friday 3pm via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted experiments
- Generate the weekly optimization brief (see step 2)

### 2. Deploy play-specific monitoring and reporting

Run the `autonomous-optimization` drill to build the monitoring layer specific to this play:

**Affiliate program dashboard in PostHog:**
- Referrals by partner (bar chart, last 30 days)
- Revenue by partner (bar chart, last 30 days)
- Click-to-paid conversion rate by partner (table, sorted descending)
- Referral volume over time (trend line, last 90 days)
- Commission ROI by partner (table, revenue / commissions)
- Full affiliate funnel (click → signup → trial → paid → renewal)
- Performance by partner tier (Standard / Silver / Gold)
- Onboarding cohort analysis (activation rate by month of enrollment)

**Weekly program brief (automated, Friday 3pm):**
```
## Affiliate Program Weekly Brief — {date}

**This week**: {clicks} clicks, {signups} signups, {conversions} paid conversions
**Revenue attributed**: ${revenue} ({commissions} in commissions, {roi}x ROI)
**vs 4-week avg**: {change_pct}% {up/down}
**Active experiments**: {count} ({status summary})

### Top partners
1. {partner_1}: {conversions} conversions, ${revenue} revenue
2. {partner_2}: {conversions} conversions, ${revenue} revenue

### Anomalies detected
- {partner/metric}: {description} — {hypothesis generated}

### Experiments this week
- {experiment}: {status} — {result or ETA}

### Adopted changes
- {change}: {impact on metrics}

### Program health
- Active partners: {count} (Tier breakdown: {standard}/{silver}/{gold})
- Activation rate (30-day): {pct}%
- Partner churn rate (90-day): {pct}%
- Revenue per active partner: ${amount}

### Convergence status
{distance from local maximum estimate}
{recommended focus for next week}
```

**Per-partner ROI tracking in Attio:**
- Total clicks, signups, conversions, revenue, commissions, commission ROI, best-performing content, partner health score
- Updated weekly by n8n

**Performance alerts:**
- Partner conversions drop >60% week-over-week → investigate in Slack
- New partner generates first paid conversion within 14 days → flag as fast activator
- Total program revenue drops below Scalable baseline for 2 consecutive weeks → trigger autonomous optimization investigation
- Partner achieves >30% signup-to-paid conversion → flag as star partner, investigate their approach
- Commission ROI drops below 3x for any tier → flag commission structure for review

### 3. Manage partner portfolio health

The agent autonomously manages the partner portfolio:

- **Partner fatigue detection**: If a partner's conversion rate declines for 3 consecutive months, the agent diagnoses whether it is audience saturation (same audience seeing repeated promotions) or partner disengagement (they stopped actively promoting). For saturation: suggest the partner target a new audience segment or use a different channel. For disengagement: trigger reactivation sequence.
- **Tier optimization**: The agent monitors whether tier thresholds are correctly set. If too many partners cluster at the bottom of a tier (doing the minimum to qualify but not more), the agent proposes adjusting thresholds or adding intermediate incentives (bonuses for hitting stretch goals).
- **Commission efficiency analysis**: Monthly, the agent estimates "would this customer have converted without the affiliate?" by comparing affiliate-sourced customers' behavior to organic customers. If a partner's referrals behave identically to organic traffic (same sources, same pages visited before signup), they may be claiming credit for organic demand. Flag for investigation.
- **Competitive monitoring**: The agent periodically checks whether competitors have launched or changed their affiliate programs (search for "{competitor} affiliate program" or "{competitor} partner program" monthly). If a competitor offers materially better terms, flag for strategic response.
- **Partner graduation**: Partners consistently generating >$5K/month in attributed revenue get flagged for deeper partnership discussions (co-selling, integration partnerships, strategic alliances). Log the recommendation in Attio for human review.

### 4. Guardrails

- **Maximum 1 active experiment at a time.** Never stack onboarding tests with commission tests simultaneously.
- **Revert threshold**: If total program conversions drop >30% during an experiment, auto-revert immediately.
- **Human approval required for**: Commission rate changes affecting >25% of active partners, payout processing (monthly review), retiring a partner who generates >15% of total program revenue, any budget increase.
- **Cooldown**: After a failed experiment, wait 14 days before testing the same variable.
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for human strategic review.
- **Never change commission rates retroactively.** All commission changes apply to future referrals only.
- **Payout integrity**: Never delay or reduce a payout for an earned commission. Trust is the foundation of partner relationships.

### 5. Convergence detection

The optimization loop runs continuously. It detects convergence when:
- 3 consecutive experiments produce <2% improvement in the primary metric (conversions or commission ROI)
- The program has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per month (maintenance mode)
3. Report: "Affiliate program has converged. Current performance: {metrics}. Further gains require strategic changes (new partner categories, product-led referral features, different commission models, geographic expansion) rather than tactical optimization of the existing program."

## Time Estimate

- Autonomous optimization setup: 25 hours
- Affiliate performance reporting setup: 10 hours
- Initial monitoring and tuning (month 1-2): 25 hours
- Ongoing oversight (months 3-12, ~5 hours/month): 50 hours
- Experiment design and evaluation: 30 hours
- Partner portfolio management: 20 hours
- Strategic reviews and course corrections: 20 hours

Total: ~180 hours over 12 months (heavily front-loaded; agent handles most ongoing work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Rewardful | Affiliate tracking, commissions, payouts | Growth: $99/mo ([rewardful.com/pricing](https://www.rewardful.com/pricing)) |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events; paid from $0.00031/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop orchestration, scheduling, alerts | Cloud Pro: ~$60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, experiment logs, ROI tracking | Plus: $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, briefs | API: ~$15-30/mo at this usage ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Crossbeam | Partner account overlap (ongoing) | Free tier for basic use; Connector from $400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |
| Clay | Ongoing partner candidate sourcing | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |

**Estimated cost for this level: ~$210-410/mo** (Rewardful Growth + n8n Pro + Attio + Anthropic API required; Clay and Crossbeam optional at Durable level if recruitment is automated from Scalable)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum
- `autonomous-optimization` — per-partner dashboards, weekly briefs, ROI tracking, and alerts specific to this play
