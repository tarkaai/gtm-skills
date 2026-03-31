---
name: customer-success-playbooks-smoke
description: >
  CS Intervention Playbooks -- Smoke Test. Build 5 repeatable intervention playbooks for the most
  common churn scenarios, validate each against one real at-risk customer, and measure whether
  the intervention produced any improvement in engagement or risk score.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "5 playbooks created, each validated against 1 real at-risk customer"
kpis: ["Playbook count", "Intervention success rate", "Risk score improvement"]
slug: "customer-success-playbooks"
install: "npx gtm-skills add product/retain/customer-success-playbooks"
drills:
  - churn-signal-extraction
  - support-ticket-analysis
  - threshold-engine
---

# CS Intervention Playbooks -- Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

5 documented, agent-executable CS intervention playbooks, each mapped to a specific churn signal. Each playbook validated against at least 1 real at-risk customer. At least 3 of 5 interventions produce a measurable reduction in churn risk score within 14 days.

## Leading Indicators

- Churn signal taxonomy completed (distinct signals identified from historical data)
- At-risk customers identified for each churn scenario
- Playbook steps executed without ambiguity or missing data
- Risk score movement detected within 7 days of intervention

## Instructions

### 1. Extract churn signals from historical data

Run the `churn-signal-extraction` drill to analyze churned vs. retained users in PostHog. The drill compares behavioral patterns between the two cohorts and outputs a ranked list of churn signals with their predictive strength.

From the output, select the 5 strongest churn signals. Typical signals for SaaS products:
- **Activity decay:** Weekly session count dropped >50% vs. user's 30-day average
- **Feature abandonment:** User stopped using a core feature they previously used 3+ times per week
- **Support escalation:** 3+ support tickets filed in 7 days, especially if severity is high
- **Billing concern:** Visited pricing page, cancellation page, or downgrade page in the last 7 days
- **Team shrinkage:** Removed 1+ team members from the account in the last 30 days

### 2. Analyze support ticket patterns

Run the `support-ticket-analysis` drill to classify recent Intercom conversations by category, severity, and sentiment. Cross-reference the classified tickets with the churn signals from step 1. This enriches the playbook design: for example, if "support escalation" is a top signal, the ticket analysis reveals which ticket categories (bug, billing, integration) are most correlated with churn.

### 3. Document 5 intervention playbooks

For each of the 5 churn signals, create a playbook document stored as an Attio note on the play's campaign record. Each playbook must contain:

**Playbook structure:**
```
# Playbook: [Signal Name] Intervention

## Trigger
- Signal: [exact PostHog event or condition that fires this playbook]
- Risk tier minimum: [medium/high/critical]
- Cooldown: 14 days since last intervention for this user

## Intervention Steps
1. [Specific action -- e.g., "Send Loops email template 'reengagement-activity-decay' with properties: user_name, last_active_date, top_feature_used"]
2. [Follow-up action if no response in 3 days -- e.g., "Trigger Intercom in-app message highlighting unused feature most correlated with retention"]
3. [Escalation action if risk score does not improve in 7 days -- e.g., "Create Attio task for account owner with context: risk score, signal data, intervention history"]

## Expected Outcome
- Risk score decreases by 10+ points within 14 days
- User resumes the behavior that was declining (sessions, feature use, etc.)

## Success Criteria
- Intervention completed (all steps executed): Y/N
- Risk score improved within 14 days: Y/N
- User still active 30 days later: Y/N (tracked in follow-up)
```

### 4. Validate each playbook against 1 real customer

For each of the 5 playbooks, identify 1 current at-risk customer whose primary churn signal matches that playbook. Query PostHog for users in the medium or high risk tier (from step 1) whose `primary_signal` matches.

Execute the playbook manually for each customer:
- Follow each step exactly as documented
- Log every action taken and the timestamp in Attio as a note on the customer's record
- Record the customer's churn risk score at intervention time and again 14 days later

**Human action required:** Review each playbook before executing against a real customer. Confirm the messaging tone is appropriate and the escalation path is correct. Execute the first intervention for each playbook yourself to verify the steps work end-to-end.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: 5 playbooks created, each validated against 1 real at-risk customer, with at least 3 of 5 producing risk score improvement.

If PASS, proceed to Baseline. If FAIL, diagnose which playbooks failed: was the signal wrong (user was not actually at risk), was the intervention wrong (steps did not address the user's concern), or was the timing wrong (intervention came too late)?

## Time Estimate

- 1.5 hours: Churn signal extraction and support ticket analysis
- 2 hours: Documenting 5 playbooks with specific steps, templates, and triggers
- 1 hour: Identifying test customers and executing 5 interventions
- 0.5 hours: Measuring outcomes and evaluating threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage analytics, churn signal extraction, cohort analysis | Free up to 1M events/mo; https://posthog.com/pricing |
| Attio | CRM for logging interventions and tracking outcomes | Free for small teams; https://attio.com/pricing |
| Intercom | Support ticket export and classification | From $39/seat/mo; https://www.intercom.com/pricing |

## Drills Referenced

- `churn-signal-extraction` -- extracts behavioral churn signals from PostHog and computes risk scores
- `support-ticket-analysis` -- classifies Intercom tickets to enrich churn signal understanding
- `threshold-engine` -- evaluates whether the play passed its success threshold
