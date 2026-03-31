---
name: change-readiness-scoring
description: Predictive scoring of organizational change readiness using deal signals, enrichment data, and historical change outcome patterns
category: Qualification
tools:
  - Attio
  - Clay
  - n8n
  - Anthropic
  - PostHog
fundamentals:
  - attio-deals
  - attio-custom-attributes
  - clay-enrichment-waterfall
  - n8n-scheduling
  - n8n-workflow-basics
  - change-resistance-diagnosis
  - posthog-custom-events
  - posthog-funnels
---

# Change Readiness Scoring

This drill builds a predictive model that scores each deal's likelihood of successful change adoption BEFORE the change objection is raised. It runs daily against the pipeline, flagging deals likely to face change resistance so the seller can prepare proactively instead of reacting.

## Input

- Attio CRM with deal pipeline and enrichment data
- Clay for additional company enrichment
- n8n instance for scheduled execution
- PostHog with historical change objection events (from `change-objection-extraction`)
- 4+ weeks of change resistance data from Baseline level

## Steps

### 1. Define the scoring model

Configure scoring weights in the n8n workflow. These are the initial defaults; the autonomous optimization loop at Durable level will refine them.

**Organizational Factors (max 40 points):**
| Signal | Points | Source | Logic |
|--------|--------|--------|-------|
| Company > 200 employees | +10 | Clay/Attio | Larger orgs have more change inertia |
| Regulated industry (finance, healthcare, gov) | +10 | Clay | Compliance adds switching friction |
| Current solution used > 3 years | +8 | Attio | Longer tenure = higher switching cost |
| Current solution used > 5 years | +12 (replaces 3yr) | Attio | Deep entrenchment |
| Multiple departments using current solution | +8 | Attio notes / enrichment | Cross-functional dependencies |
| Prior failed migration mentioned | +15 | Attio notes | Past failure predicts future resistance |

**Deal Factors (max 40 points):**
| Signal | Points | Source | Logic |
|--------|--------|--------|-------|
| No champion identified | +10 | Attio | No internal advocate for change |
| Champion is not a decision maker | +5 | Attio | Need to sell up |
| Economic buyer not engaged | +8 | Attio | Budget authority not aligned |
| Competitor evaluation active | +5 | Attio | Multiple options = harder to commit |
| Pain-to-price ratio < 5x | +12 | Attio | Weak value story makes change harder to justify |
| No quantified pain data | +15 | Attio | Cannot make the cost-of-staying argument |

**Enrichment Signals (max 20 points):**
| Signal | Points | Source | Logic |
|--------|--------|--------|-------|
| Recent executive turnover | -5 | Clay | New leadership = more open to change |
| Recent funding round | -5 | Clay | Growth mode = more willing to invest |
| Company growing > 30% YoY | -5 | Clay | Growth forces tool upgrades |
| Deep vendor integrations detected | +10 | Clay tech stack | Technical lock-in |
| Company blog/PR mentions "digital transformation" | -3 | Clay | Signals change appetite |

**Score interpretation:**
- 0-25: **Change Ready** — proceed normally, low risk of change resistance
- 26-50: **Moderate Risk** — prepare change support materials proactively
- 51-75: **High Risk** — run `change-objection-call-prep` before next interaction; prepare pilot proposal
- 76-100: **Critical** — flag for human review; consider whether deal is worth pursuing without significant change support investment

### 2. Build the daily scoring workflow

Using `n8n-scheduling`, create a daily cron workflow:

1. Query Attio for all active deals in stages: "Discovery," "Evaluation," "Proposal," "Negotiation"
2. For each deal, pull enrichment data from Clay using `clay-enrichment-waterfall` (cache for 7 days; don't re-enrich daily)
3. Calculate the change readiness score using the model above
4. Compare with the deal's previous score (stored in Attio custom attribute)
5. Update the deal in Attio using `attio-custom-attributes`:
   - `change_readiness_score`: the calculated score
   - `change_readiness_tier`: "ready" / "moderate" / "high_risk" / "critical"
   - `change_readiness_date`: today's date
   - `change_readiness_delta`: change from previous score

6. Fire PostHog events for each scored deal:
```json
{
  "event": "change_readiness_scored",
  "properties": {
    "deal_id": "...",
    "score": 62,
    "tier": "high_risk",
    "delta": +5,
    "top_risk_factor": "current_solution_5yr_tenure",
    "deal_stage": "evaluation"
  }
}
```

### 3. Set up proactive alerts

For deals crossing tier boundaries, send Slack notifications:

- Deal moves from "moderate" to "high_risk": "Deal {name} change readiness score increased to {score}. Top factor: {factor}. Consider preparing change support materials."
- Deal enters "critical": "Deal {name} is at critical change risk ({score}). Recommend running `change-objection-call-prep` before next interaction."
- Deal score decreases by 15+ points: "Deal {name} change readiness improved ({old_score} -> {new_score}). Reason: {factor that changed}."

### 4. Build proactive intervention triggers

Using `n8n-workflow-basics`, create workflows that auto-trigger based on score:

- Score crosses 50 (enters high_risk): auto-run `change-objection-call-prep` drill for the next scheduled meeting
- Score crosses 75 (enters critical): auto-generate a draft pilot proposal using `change-support-plan-generation` with `rollout_strategy = "pilot_first"`
- Score drops below 25 after being high: auto-notify seller that change resistance has decreased; validate with the prospect

### 5. Calibrate the model

After 4 weeks, compare predicted risk with actual outcomes:
- For deals scored "high_risk" or "critical": did change resistance actually surface?
- For deals scored "ready": were there surprise change objections?

Calculate:
- **True positive rate:** deals scored high-risk that actually faced change resistance
- **False positive rate:** deals scored high-risk that had no change resistance
- **False negative rate:** deals scored low-risk that had change resistance

Adjust weights to maximize true positive rate while keeping false positive rate < 20%.

Log calibration results in PostHog:
```json
{
  "event": "change_readiness_calibration",
  "properties": {
    "period": "last_4_weeks",
    "true_positive_rate": 0.78,
    "false_positive_rate": 0.15,
    "false_negative_rate": 0.10,
    "weight_adjustments": {"signal": "delta"}
  }
}
```

## Output

- Daily change readiness scores on every active deal
- Proactive alerts when deals cross risk thresholds
- Auto-triggered prep and support plan generation for high-risk deals
- Model calibration data for the autonomous optimization loop

## Triggers

Runs daily via n8n cron (7 AM). Proactive interventions trigger in real-time when score thresholds are crossed.
