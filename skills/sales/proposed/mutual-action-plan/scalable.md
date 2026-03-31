---
name: mutual-action-plan-scalable
description: >
  Mutual Action Plan (MAP) — Scalable Automation. Scale MAPs to 50+ deals per quarter with
  predictive risk scoring, MAP-based close date forecasting, automated template optimization
  via A/B testing, and a real-time deal health dashboard.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=70% MAP adoption and >=35% faster close time with >=25% higher win rate for MAP deals over 2 months"
kpis: ["MAP adoption rate", "Milestone completion rate", "Deal velocity improvement", "Forecast accuracy by MAP adherence"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
drills:
  - map-auto-generation
  - ab-test-orchestrator
  - dashboard-builder
---

# Mutual Action Plan (MAP) — Scalable Automation

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale MAP coverage to 50+ deals per quarter. Add predictive risk scoring that uses milestone adherence patterns to forecast deal outcomes. Build MAP-based close date forecasting that replaces gut-feel pipeline estimates. A/B test MAP templates and communication cadences to find the structures that produce the highest completion rates. A real-time dashboard gives the team visibility into MAP health across the entire pipeline.

Pass: >= 70% MAP adoption, MAP deals close >= 35% faster with >= 25% higher win rate, and forecast accuracy from MAP data >= 75% over 2 months.
Fail: Adoption below 70%, velocity improvement below 35%, or MAP-based forecasts are less accurate than historical averages.

## Leading Indicators

- Risk scores correctly identify at-risk deals 5+ days before visible stalls (predictive power)
- MAP-based close date predictions are within 7 days of actual close for >= 60% of deals
- A/B tests on MAP templates produce statistically significant differences in milestone completion rates
- Dashboard is checked by the team at least 3x per week (it drives decisions)
- Automated risk alerts trigger rep action within 24 hours (alerts are trusted and actionable)
- Template optimization produces >= 10% improvement in milestone adherence rate per quarter

## Instructions

### 1. Deploy predictive risk scoring

Run the the map risk scoring workflow (see instructions below) drill to build the deal health prediction system.

**Build the historical pattern database:**
Query Attio for all deals from the last 12 months with MAP data. For each deal, extract the milestone-by-milestone timeline, outcome, and any stall events. This requires >= 20 completed MAPs from the Baseline run.

If you have fewer than 20 completed MAPs, start with the default scoring model from the drill and plan to calibrate after month 1 when you have more data.

**Configure the scoring model:**
The risk scoring model applies deductions from a base score of 100:

| Signal | Deduction | Rationale |
|--------|-----------|-----------|
| Milestone 1-3 days overdue | -5 per milestone | Minor delay |
| Milestone 5+ days overdue | -15 per milestone | Significant momentum loss |
| Buyer-owned milestone overdue | -10 extra | Buyer disengagement signal |
| 2+ consecutive milestones overdue | -20 | Stall pattern |
| No prospect communication 7+ days | -15 | Ghost risk |
| Champion not responding to updates | -25 | Champion lost |
| Completion rate < 50% past halfway | -20 | Behind schedule |

Risk levels: Healthy (80-100), Watch (60-79), At Risk (40-59), Critical (0-39).

**Deploy the daily scoring workflow:**
Create an n8n workflow that runs after the daily milestone checker (from Baseline). For each active MAP:
- Calculate the risk score
- Write `map_risk_score` and `map_risk_level` to Attio
- Calculate win probability from risk score (80-100 = 85%, 60-79 = 55%, 40-59 = 25%, 0-39 = 8%)
- Fire alerts when risk level changes (e.g., Watch -> At Risk)
- Generate intervention recommendations for At Risk and Critical deals using Claude API

**Build the close date predictor:**
Using historical milestone velocity data, predict close dates:
- For each deal, calculate the average days-per-milestone based on completed milestones
- Project remaining milestones at that velocity
- Compare the MAP-predicted close date with the rep-estimated close date
- Write `map_predicted_close` to Attio

Track prediction accuracy in PostHog: fire `map_forecast_updated` events with predicted date, rep-estimated date, and (after close) actual date.

### 2. Scale MAP auto-generation to 50+ deals

Extend the `map-auto-generation` workflow from Baseline to handle volume:

**Template refinement:**
Using milestone completion data from Baseline, adjust templates:
- Which milestones are consistently completed faster than estimated? Shorten them.
- Which milestones consistently slip? Add buffer or split into sub-milestones.
- Are there milestones that never complete because they don't apply? Remove or make conditional.

**Industry-specific templates:**
If your pipeline spans multiple industries, create variant templates. Clone the base templates and adjust milestone names and durations. For example, healthcare deals may need a compliance review milestone that SaaS deals don't.

**Conditional milestone logic:**
Add logic to the generation workflow:
- If deal value > $50K, include POC milestone
- If prospect is in a regulated industry, include compliance review
- If multiple stakeholders, include stakeholder alignment meeting
- If prospect has mentioned budget constraints, include budget approval milestone

**Error handling at scale:**
- Deals missing expected close date: Queue for rep to add, don't generate MAP without it
- Deals with no champion contact: Alert rep to identify champion before MAP delivery
- Duplicate MAPs: Check if a MAP already exists on the deal before generating a new one

### 3. Run A/B tests on MAP structure

Run the `ab-test-orchestrator` drill to test MAP variations.

**Test 1 — Milestone granularity:**
- Control: Standard template (8-12 milestones)
- Variant: Streamlined template (5-6 key milestones only)
- Metric: Milestone completion rate and deal velocity
- Hypothesis: Simpler MAPs have higher adherence because prospects aren't overwhelmed

**Test 2 — Update cadence:**
- Control: Weekly MAP progress emails
- Variant: Twice-weekly MAP progress emails
- Metric: Milestone completion rate and prospect response rate
- Hypothesis: More frequent check-ins maintain momentum

**Test 3 — Escalation timing:**
- Control: Escalate after 5 days overdue
- Variant: Escalate after 2 days overdue
- Metric: Milestone recovery rate and deal velocity
- Hypothesis: Earlier escalation catches stalls before momentum is lost

**Test 4 — MAP delivery format:**
- Control: MAP in email body as a formatted table
- Variant: MAP as a shared Google Doc / Notion page with live updates
- Metric: Prospect engagement (opens, edits, comments) and milestone completion rate
- Hypothesis: A living document drives more engagement than static email updates

Use PostHog feature flags to randomly assign new MAP deals to control or variant. Run each test for >= 4 weeks or >= 20 deals per variant, whichever is longer. Evaluate using `experiment-evaluation`.

### 4. Build the MAP health dashboard

Run the `dashboard-builder` drill to create the Scalable-level PostHog dashboard.

**Dashboard panels:**

- **Pipeline MAP coverage:** Percentage of proposal-stage deals with active MAPs (target >= 70%), with weekly trend
- **Risk distribution:** Count of deals at each risk level (Healthy / Watch / At Risk / Critical), updated daily
- **Milestone adherence heatmap:** Completion rate by milestone type (e.g., "Legal Review" is completed on time 45% of the time). Color-coded green (>= 80%), yellow (50-79%), red (< 50%)
- **Deal velocity comparison:** Average days-to-close for MAP deals vs non-MAP deals, 8-week rolling trend
- **Win rate comparison:** Win rate for MAP deals vs non-MAP deals, 8-week rolling trend
- **Forecast accuracy:** MAP-predicted close date vs actual close date, distribution chart showing prediction error in days
- **Stall analysis:** Number of stalled deals per week, recovery rate, average stall duration
- **Active experiments:** Current A/B tests with interim results
- **MAP funnel:** `map_created` -> first milestone completed -> 50% completion -> 100% completion -> deal won. Shows where MAPs break down.
- **Top risk factors:** Which scoring signals are contributing most to risk scores across the pipeline

**Alerts (via n8n):**

- MAP adoption drops below 60% for 2 consecutive weeks -> investigate why reps aren't using MAPs
- Risk distribution shifts: > 40% of deals are At Risk or Critical -> pipeline health problem
- Milestone adherence drops below 50% for any milestone type -> template problem, review milestone definitions
- Forecast accuracy drops below 65% -> model calibration needed
- A/B test reaches statistical significance -> review and implement winner

### 5. Implement MAP-based forecasting

Replace gut-feel pipeline forecasting with MAP data:

**Weekly forecast workflow (n8n, every Monday):**
1. Query all active MAP deals from Attio
2. For each deal, calculate:
   - MAP-predicted close date (from milestone velocity)
   - Win probability (from risk score)
   - Expected value = deal value x win probability
3. Aggregate: sum expected value by week/month
4. Generate forecast report:
   - This month's expected revenue (sum of expected values for deals predicted to close this month)
   - Next month's expected revenue
   - High-confidence deals (risk score >= 80, close date this month)
   - At-risk revenue (deals with risk score < 60 that are supposed to close this month)
5. Send via Slack to leadership, store in Attio

**Track forecast accuracy monthly:**
Compare MAP-based forecast to actual closed revenue. Log the comparison in PostHog. Target: MAP-based forecast is within 15% of actual revenue (better than historical rep-estimated accuracy).

### 6. Evaluate at 2 months

After 2 months, measure:

**MAP adoption:** >= 70% of proposal-stage deals have MAPs

**Deal velocity:** MAP deals close >= 35% faster than non-MAP deals (or non-MAP historical baseline)

**Win rate:** MAP deals win >= 25% more often than non-MAP deals

**Forecast accuracy:** MAP-predicted close dates within 7 days of actual for >= 60% of deals. MAP-based revenue forecast within 15% of actual.

**Risk scoring accuracy:** Deals scored as "Healthy" should win at >= 75% rate. Deals scored as "Critical" should win at < 20% rate.

If **PASS:** MAP automation drives measurable sales performance at scale. Proceed to Durable for autonomous optimization of templates, scoring models, and communication strategies.

If **FAIL:** Diagnose:
- **Adoption stalled:** Reps find MAPs burdensome. Simplify the review process or auto-approve low-risk MAPs.
- **Velocity plateaued:** MAPs may have hit a ceiling. The bottleneck is likely buyer-side (procurement, legal). Focus optimization on those milestones.
- **Risk scoring inaccurate:** Not enough historical data, or the wrong signals are weighted. Retrain the model.
- **Forecast off:** Milestone velocity varies too much by deal type. Build separate prediction models per deal type.

## Time Estimate

- Risk scoring model setup: 8 hours
- MAP generation scaling and template refinement: 6 hours
- A/B test configuration: 4 hours
- Dashboard and alerts: 6 hours
- Forecasting workflow: 4 hours
- Testing and debugging: 6 hours
- Ongoing monitoring (2 months x 4 hours/week): 32 hours
- Evaluation: 4 hours
- **Total: ~70 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MAP data, risk scores, custom attributes, forecast data | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Automation — risk scoring, MAP generation, milestone tracking, forecasting, A/B test routing | Pro $60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| PostHog | Analytics — MAP funnels, velocity comparisons, risk dashboards, experiments, forecast tracking | Free (1M events/mo); paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| Claude API | MAP personalization, risk intervention recommendations | Sonnet: $3/$15 per M input/output tokens ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Loops | Prospect MAP delivery and update emails | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at Scalable:** ~$150-250/mo (n8n Pro $60 + Claude API ~$20-50 for MAP generation and risk recommendations + Loops $49 + PostHog likely within free tier)

## Drills Referenced

- the map risk scoring workflow (see instructions below) — Predictive risk scores based on milestone adherence patterns, win probability estimates, and intervention recommendations for at-risk deals
- `map-auto-generation` — Scaled MAP generation with conditional milestone logic, industry-specific templates, and error handling for high-volume pipelines
- `ab-test-orchestrator` — Run controlled experiments on MAP template structure, update cadence, escalation timing, and delivery format
- `dashboard-builder` — Build the MAP health dashboard with risk distribution, velocity comparison, forecast accuracy, and stall analysis
