---
name: commitment-health-monitor
description: Monitor multi-year commitment program health — conversion rates, retention lift, LTV impact, and renewal pipeline
category: Product
tools:
  - PostHog
  - Stripe
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - billing-event-streaming
  - n8n-scheduling
  - attio-reporting
---

# Commitment Health Monitor

This drill builds the monitoring layer for the multi-year commitment program. It tracks whether committed accounts actually retain at higher rates, whether the LTV increase justifies the discount, and whether the offer funnel is performing. It runs continuously and surfaces anomalies that need intervention.

This is the measurement layer. It answers "is the commitment program working?" and "where is it breaking?" The `autonomous-optimization` drill acts on the anomalies this monitor detects.

## Input

- Multi-year commitment program live with at least 20 committed accounts
- PostHog events flowing from the `multiyear-offer-engine` drill
- Stripe billing data accessible via webhook or API
- n8n instance for scheduled monitoring
- Attio CRM with commitment deal data

## Steps

### 1. Build the commitment program dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Funnel metrics:**
- Offer funnel: qualified → shown → clicked → started → converted (by channel)
- Conversion rate by offer tier (Standard vs. Enhanced vs. Premium)
- Conversion rate by readiness score band (70-85, 85-100, 100+)
- Time from offer shown to conversion (distribution)

**Retention metrics:**
- Churn rate: committed accounts vs. monthly accounts (trailing 90 days)
- Retention curve: committed vs. monthly cohorts (month 1 through month 12+)
- Committed account health score distribution vs. monthly

**Revenue metrics:**
- ARR from committed accounts vs. total ARR (percentage)
- Average discount given (weighted by ARR)
- LTV: committed accounts vs. monthly accounts (actual, not projected)
- Net revenue impact: ARR gained from commitments minus discount cost

**Pipeline metrics:**
- Accounts in Ready tier not yet offered
- Accounts offered but not converted (by channel)
- Upcoming renewals for committed accounts (30/60/90 day windows)
- Renewal rate for committed accounts reaching end of term

### 2. Define anomaly thresholds

Using `posthog-anomaly-detection`, set alert rules:

| Metric | Alert Condition | Severity | Action |
|--------|----------------|----------|--------|
| Offer conversion rate | Drops >30% vs. 4-week average | High | Investigate offer fatigue or competitive pressure |
| Committed account churn | Any committed account cancels | Critical | Immediate review — committed churn is a program failure signal |
| Discount-to-retention ratio | Average discount > 20% AND retention lift < 10pp | High | Discounts are too generous for the retention they produce |
| Ready tier volume | Drops >40% vs. 4-week average | Medium | Fewer accounts becoming commitment-ready — upstream health issue |
| Renewal pipeline | >20% of renewals in 60-day window have no outreach logged | Medium | Renewal outreach is falling behind |
| In-app offer dismiss rate | Exceeds 90% for 2+ weeks | High | Offer placement or copy is wrong |

### 3. Build the monitoring workflow

Using `n8n-scheduling`, create a weekly n8n workflow:

1. **Pull commitment funnel data from PostHog:** Query the offer funnel events for the last 7 days. Calculate conversion rates at each step. Compare to 4-week rolling average.

2. **Pull billing data from Stripe:** Using `billing-event-streaming`, query:
   - New annual/multi-year subscriptions created this week
   - Committed subscriptions that cancelled or downgraded this week
   - Revenue from committed vs. monthly subscriptions
   - Upcoming commitment renewals in the next 90 days

3. **Compute program health metrics:**
   - Commitment penetration: (committed ARR / total ARR) x 100
   - Effective discount rate: (total discount given / total committed ARR) x 100
   - Retention lift: (monthly churn rate - committed churn rate) in percentage points
   - LTV multiplier: (committed account average LTV / monthly account average LTV)
   - Payback period: months until the retained revenue from a committed account exceeds the discount given

4. **Check anomaly thresholds** (Step 2 rules). For any triggered alert:
   - Log `commitment_anomaly_detected` in PostHog with properties: `metric`, `current_value`, `threshold`, `severity`, `recommended_action`
   - For Critical alerts: send immediate Slack notification
   - For High alerts: include in the weekly report with investigation notes
   - For Medium alerts: log and trend — alert only if sustained for 2+ consecutive weeks

5. **Update Attio with program metrics:** Using `attio-reporting`, update the commitment program record with this week's metrics. Tag accounts approaching renewal with `renewal_window` = 30/60/90.

6. **Generate the weekly commitment health report:**

   ```
   ## Multi-Year Commitment Program — Week of {date}

   ### Funnel Performance
   - Accounts qualified: {n} ({+/-X%} vs. avg)
   - Offers shown: {n} ({conversion from qualified}%)
   - Commitments signed: {n} ({conversion from shown}%)
   - Best channel: {channel} at {rate}%

   ### Retention Impact
   - Committed churn rate: {X}% (monthly: {Y}%, lift: {Z}pp)
   - Committed accounts at risk: {n} (score > 45)

   ### Revenue Impact
   - Committed ARR: ${X} ({Y}% of total)
   - Effective discount rate: {X}%
   - LTV multiplier: {X}x
   - Net revenue impact this month: +${X}

   ### Pipeline
   - Renewals in 30 days: {n} accounts, ${X} ARR
   - Renewals in 60 days: {n} accounts, ${X} ARR
   - Renewal outreach coverage: {X}%

   ### Anomalies
   {list of triggered alerts with recommended actions}

   ### Recommendation
   {one-sentence next action based on data}
   ```

### 4. Track committed account renewal pipeline

Using `posthog-cohorts`, create cohorts for committed accounts by renewal window:

- "Commitment Renewing — 30 Days" — committed accounts with term end in 0-30 days
- "Commitment Renewing — 60 Days" — committed accounts with term end in 31-60 days
- "Commitment Renewing — 90 Days" — committed accounts with term end in 61-90 days

Using `n8n-scheduling`, 90 days before each commitment term ends, trigger a renewal workflow:

1. Score the account's current health (usage trend, satisfaction, expansion signals)
2. If healthy: prepare a renewal offer (same or better terms)
3. If at-risk: flag for human intervention with context
4. Log `commitment_renewal_queued` event in PostHog

### 5. Measure program ROI

Monthly, compute the program's financial impact:

```
Revenue retained = (committed accounts that would have churned at monthly churn rate) x (their ARR)
Discount cost = sum of (committed account ARR x discount percentage)
Net program value = Revenue retained - Discount cost
Program ROI = Net program value / Discount cost
```

If ROI < 1.0, the program is destroying value — discounts exceed the retention benefit. If ROI > 3.0, the program is highly efficient — consider increasing offer volume or discount levels.

Log `commitment_program_roi` event in PostHog monthly with: `revenue_retained`, `discount_cost`, `net_value`, `roi`, `committed_accounts`, `commitment_penetration`.

## Output

- A PostHog dashboard with funnel, retention, revenue, and pipeline panels
- Weekly automated health reports with anomaly detection
- Renewal pipeline tracking with 90-day advance warning
- Monthly ROI calculation that validates the program's financial impact
- Anomaly events that feed the `autonomous-optimization` drill at Durable level

## Triggers

Dashboard updates in real-time. Health report generates weekly via n8n cron. Renewal pipeline check runs daily. ROI calculation runs monthly on the 1st.
