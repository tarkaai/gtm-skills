---
name: map-risk-scoring
description: Score deal risk based on MAP adherence patterns, predict close probability, and identify optimal intervention points
category: Deal Management
tools:
  - Attio
  - PostHog
  - n8n
  - Claude API
fundamentals:
  - attio-deals
  - attio-custom-attributes
  - attio-reporting
  - posthog-funnels
  - posthog-dashboards
  - posthog-anomaly-detection
  - hypothesis-generation
  - n8n-workflow-basics
  - n8n-scheduling
---

# MAP Risk Scoring

This drill creates a predictive risk scoring system that uses MAP adherence data to forecast deal outcomes. It learns from historical MAP patterns — which delays are recoverable, which stall sequences predict loss, and which intervention points have the highest impact.

## Input

- Historical MAP data: at least 20 completed MAPs (won and lost deals) with milestone-level timing data
- PostHog events from `map-milestone-tracking` drill
- Attio deal records with MAP attributes

## Steps

### 1. Build the historical pattern database

Using `attio-reporting`, query all deals from the last 12 months where `map_created_date` is not null. For each deal, extract:

- Deal type (SMB/Mid-Market/Enterprise)
- Final outcome (Won/Lost)
- Total milestones and completion rate
- Which milestones were completed on time, late, or skipped
- Days between milestone completions
- Total MAP duration vs. planned duration
- Stall count and recovery rate
- Which stakeholder-owned milestones were delayed most

Store this as a structured dataset in Attio (as a note or export to a table).

### 2. Identify predictive patterns

Using Claude API, analyze the historical dataset to find patterns:

Prompt:
```
Analyze this historical MAP data for {n} deals. For each deal, I have:
- Outcome (won/lost)
- Milestone-by-milestone timing (on time, days late, skipped)
- Deal type and value
- Stall events and recovery

Find:
1. Which milestones are most predictive of deal outcome? (e.g., "if legal review is >10 days late, 75% of deals are lost")
2. What stall patterns predict loss? (e.g., "2+ buyer-owned milestones overdue = 80% loss rate")
3. What recovery actions correlate with wins after stalls? (e.g., "exec-to-exec call within 3 days of stall recovers 60% of deals")
4. What is the typical velocity per deal type and how does deviation predict outcome?

Output as structured risk rules with confidence percentages.
```

### 3. Create the risk scoring model

Based on the pattern analysis, build a scoring model. Default starting model (adjust with your data):

**Risk Score = 100 (healthy) minus deductions:**

| Signal | Deduction | Rationale |
|--------|-----------|-----------|
| Milestone 1-3 days overdue | -5 per milestone | Minor delay, often recoverable |
| Milestone 5+ days overdue | -15 per milestone | Significant delay, deal momentum loss |
| Buyer-owned milestone overdue | -10 extra | Buyer disengagement signal |
| 2+ consecutive milestones overdue | -20 | Stall pattern detected |
| No prospect communication in 7+ days | -15 | Ghost risk |
| Champion not responding to updates | -25 | Champion lost or deprioritized |
| Legal/procurement milestone delayed | -10 | Process delay, often recoverable |
| Completion rate below 50% past halfway point | -20 | Behind schedule |

**Risk classification:**
- 80-100: Healthy — deal on track
- 60-79: Watch — minor delays, monitor closely
- 40-59: At Risk — intervention needed
- 0-39: Critical — deal likely to stall or lose without executive action

### 4. Build the daily risk scoring workflow

Using `n8n-scheduling`, create a workflow that runs after the daily milestone checker:

**Step 1 — Score each active MAP:**
For each deal where `map_status` = "Active":
- Pull milestone status from Attio
- Apply the scoring model
- Calculate risk score

**Step 2 — Update Attio:**
Using `attio-custom-attributes`, write:
- `map_risk_score` (number, 0-100)
- `map_risk_level` (select: Healthy/Watch/At Risk/Critical)
- `map_predicted_close_pct` (number, 0-100% win probability)

**Step 3 — Predict close probability:**
Using historical data, map risk score to win probability:
- Risk 80-100 → 85% win probability (based on historical conversion at this risk level)
- Risk 60-79 → 55% win probability
- Risk 40-59 → 25% win probability
- Risk 0-39 → 8% win probability

**Step 4 — Fire alerts for risk transitions:**
When a deal's risk level changes (e.g., Watch → At Risk), send Slack alert to the deal owner with:
- Current risk score and what changed
- Specific milestones causing the risk
- Recommended intervention based on historical success patterns

### 5. Build the intervention recommendation engine

When a deal drops to "At Risk" or "Critical," use Claude API to generate specific intervention recommendations:

Prompt:
```
Deal: {company} (${value}, {deal_type})
Current risk score: {score} ({level})
Risk factors: {list of deductions and reasons}
Historical pattern: Deals with this risk profile recover {x}% of the time. Successful recoveries typically involve: {list of successful interventions from historical data}.

Recommend 2-3 specific actions the rep should take in the next 48 hours to recover this deal. Be specific: who to contact, what to say, what to offer.
```

Store recommendations as Attio notes. Send to the rep via Slack.

### 6. Calibrate the model monthly

Using `posthog-dashboards`, build a model accuracy dashboard:
- Predicted win probability vs. actual outcome for all scored deals
- Risk level distribution: what percentage of deals are at each level
- Intervention success rate: when we intervened on At Risk deals, what percentage recovered
- False positive rate: deals scored as At Risk that won without intervention
- False negative rate: deals scored as Healthy that were lost

Using `posthog-anomaly-detection`, detect when prediction accuracy drifts below 70%. When drift is detected, retrain the model by re-running the historical pattern analysis with updated data.

## Output

- Daily risk scores for all active MAP deals
- Win probability predictions based on MAP adherence
- Automated intervention recommendations for at-risk deals
- Monthly model calibration with accuracy tracking
- Risk factor dashboard showing which milestone patterns predict outcomes
