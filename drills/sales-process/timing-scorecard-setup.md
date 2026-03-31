---
name: timing-scorecard-setup
description: Create timeline scoring fields and pipeline routing rules in Attio for timing qualification
category: Qualification
tools:
  - Attio
  - PostHog
fundamentals:
  - attio-custom-attributes
  - attio-deals
  - attio-pipeline-config
  - posthog-custom-events
---

# Timing Scorecard Setup

Create the CRM infrastructure needed to score, categorize, and route deals based on buying timeline. Sets up custom fields on Attio Deals for timeline category, urgency drivers, confidence level, slippage risk, and target close date.

## Input

- Attio workspace with Deals object configured
- PostHog project for event tracking
- ICP definition with known timing triggers for your market

## Steps

### 1. Create timeline custom attributes on Attio Deals

Using the `attio-custom-attributes` fundamental, create the following fields on the Deals object:

| Field Name | Type | Options/Format |
|------------|------|----------------|
| `timeline_category` | Select | Immediate, Near-term, Medium-term, Long-term |
| `target_close_date` | Date | YYYY-MM-DD |
| `urgency_drivers` | Multi-select | Hard Deadline, Executive Mandate, Competitive Pressure, Pain Escalation, Budget Window, Seasonal |
| `timeline_confidence` | Number | 1-5 scale |
| `slippage_risk` | Select | High, Medium, Low |
| `consequence_of_inaction` | Text | Free-form |
| `timeline_qualified` | Checkbox | Boolean |
| `timeline_qualified_date` | Date | YYYY-MM-DD — set when `timeline_qualified` becomes true |
| `actual_close_date` | Date | YYYY-MM-DD — filled when deal closes for accuracy tracking |
| `forecast_accuracy_score` | Number | Computed: abs difference in days between target and actual close |

Use the Attio API:

```
POST https://app.attio.com/api/v2/objects/deals/attributes
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json

{
  "title": "Timeline Category",
  "api_slug": "timeline_category",
  "type": "select",
  "config": {
    "options": [
      {"title": "Immediate", "color": "red"},
      {"title": "Near-term", "color": "orange"},
      {"title": "Medium-term", "color": "yellow"},
      {"title": "Long-term", "color": "blue"}
    ]
  }
}
```

Repeat for each field.

### 2. Configure pipeline routing rules

Using the `attio-pipeline-config` fundamental, set up pipeline stages that account for timeline:

- **Immediate** deals route to "Fast Track" lane — daily follow-up cadence
- **Near-term** deals route to "Active Pipeline" — 2-3x/week cadence
- **Medium-term** deals stay in standard pipeline — weekly cadence
- **Long-term** deals route to "Future Pipeline" — biweekly nurture cadence

Create Attio automations to route deals based on `timeline_category`:

```
POST https://app.attio.com/api/v2/automations
{
  "trigger": {"type": "attribute_change", "attribute": "timeline_category"},
  "actions": [{
    "type": "move_to_stage",
    "conditions": {"timeline_category": "Immediate"},
    "stage": "Fast Track"
  }]
}
```

### 3. Set up PostHog tracking events

Using `posthog-custom-events`, create events for timeline qualification:

- `timeline_category_assigned` — properties: `deal_id`, `category`, `confidence`, `urgency_drivers[]`
- `timeline_validated` — properties: `deal_id`, `validation_method` (multi-stakeholder, re-confirmed, external signal)
- `timeline_shift_detected` — properties: `deal_id`, `old_category`, `new_category`, `shift_reason`
- `timeline_slippage` — properties: `deal_id`, `original_date`, `new_date`, `days_slipped`, `cause`
- `forecast_accuracy_logged` — properties: `deal_id`, `predicted_days`, `actual_days`, `accuracy_score`

### 4. Create Attio list views

Using `attio-lists`, create saved views:

- **"Urgent Pipeline"** — filter: `timeline_category` = Immediate AND `timeline_qualified` = true
- **"At Risk (Slippage)"** — filter: `slippage_risk` = High AND `timeline_category` in [Immediate, Near-term]
- **"Needs Timeline"** — filter: `timeline_qualified` = false AND deal age > 3 days
- **"Forecast Calibration"** — filter: `actual_close_date` is set — for tracking prediction accuracy

## Output

- Timeline scoring fields on Attio Deals
- Pipeline routing by timeline category
- PostHog events for timeline tracking
- Saved CRM views for pipeline management
