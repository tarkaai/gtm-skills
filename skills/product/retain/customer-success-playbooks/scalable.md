---
name: customer-success-playbooks-scalable
description: >
  CS Intervention Playbooks -- Scalable Automation. Expand from 5 to 10+ playbooks covering all
  major churn scenarios. A/B test intervention variants per playbook. Maintain >=55% success rate
  across 500+ interventions per month.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=55% success rate across 500+ monthly interventions with 10+ active playbooks"
kpis: ["Playbook success rate", "Monthly intervention volume", "Scenario coverage", "Save rate by segment", "Cost per save"]
slug: "customer-success-playbooks"
install: "npx gtm-skills add product/retain/customer-success-playbooks"
drills:
  - ab-test-orchestrator
  - health-score-model-design
  - health-score-alerting
---

# CS Intervention Playbooks -- Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

10+ active CS playbooks covering >90% of at-risk customers' churn signals. Each playbook has been A/B tested with at least 2 intervention variants. Success rate maintained at >=55% across 500+ monthly interventions. Health score model providing multi-dimensional risk assessment that routes users to playbooks with higher precision than signal-only scoring.

## Leading Indicators

- Scenario coverage >90% (percentage of at-risk users matched to a playbook)
- A/B tests producing statistically significant winners within 2-week test cycles
- Health score model back-testing accuracy >70% (correctly identifies at-risk accounts 30 days before churn)
- Cost per save declining as winning variants replace underperformers
- New playbooks covering previously unmatched churn signals

## Instructions

### 1. Expand playbook coverage

Analyze the Baseline data to identify coverage gaps. Query PostHog for at-risk users (medium+ tier) whose `primary_signal` did not match any existing playbook during the Baseline period. Group unmatched signals by frequency:

For each unmatched signal with 10+ occurrences in the last 30 days, create a new playbook following the structure from Smoke. Target signals that the 5 original playbooks do not cover:

- **Engagement narrowing:** User's distinct event types dropped below 50% of their historical average (they are only using one feature when they used to use many)
- **Integration disconnect:** User removed or disabled an integration they previously used
- **Champion departure:** The user who invited the most team members has gone inactive
- **Downgrade page visit:** User viewed the downgrade or plan comparison page
- **Export spike:** User exported data 3+ times in 7 days (data portability signal preceding churn)

For each new playbook, design signal-specific intervention steps. Example for "champion departure": Step 1: Intercom in-app message to the next most active user -- "Your team lead set up [feature]. Here's how to get the most from it." Step 2: Loops email to the account admin with a "team health check" framing. Step 3: Attio task for account owner if no re-engagement in 7 days.

Deploy each new playbook through the existing `churn-intervention-routing` n8n workflow by adding the signal-to-playbook mapping.

### 2. Build the composite health score model

Run the `health-score-model-design` drill to replace single-signal churn scoring with a multi-dimensional health score. The health score weighs 4 dimensions:

- **Usage (35%):** Weekly active users per account, session frequency, usage trend, login gap
- **Engagement (25%):** Feature breadth, depth of use, collaboration signals, content consumption
- **Support (20%):** Ticket volume, sentiment, resolution satisfaction, escalation rate
- **Adoption (20%):** Core feature adoption, integration status, team penetration, milestone completion

The composite score (0-100) provides a more nuanced risk assessment than individual signals. A user with a single bad signal but strong scores in other dimensions is lower risk than a user with moderate signals across all four dimensions.

Deploy the scoring pipeline in n8n to run daily. Sync scores to Attio and PostHog. Back-test the model against the last 90 days of churn data -- target >70% accuracy at predicting churners 30 days before they cancel.

### 3. Deploy health score alerting

Run the `health-score-alerting` drill to connect health score changes to intervention routing. This adds a layer of intelligence above the signal-based routing:

- **Score drop interventions:** When a previously healthy account (80+) drops to monitor (60-79), trigger a proactive nudge even if no single churn signal has fired yet. The composite score catches multi-dimensional decline that individual signals miss.
- **Expansion signals:** When a healthy account (80+) has high team penetration and growing usage, flag for expansion outreach instead of retention intervention. Do not waste intervention resources on accounts that are thriving.
- **Tier transition alerts:** When an account drops from Monitor to At Risk, or At Risk to Critical, the urgency level of the matching playbook escalates automatically.

### 4. A/B test intervention variants per playbook

Run the `ab-test-orchestrator` drill to systematically test variants of each playbook's interventions. For each of the 10+ playbooks, create at least 2 variants that differ on one dimension:

Test dimensions (one at a time per playbook):
- **Messaging:** Different subject lines, copy tone, or value proposition in the intervention email/in-app message
- **Timing:** Intervention 24 hours after signal fires vs. 72 hours (immediate vs. allowing natural recovery)
- **Channel:** Email-first vs. in-app-message-first for the same risk tier
- **Escalation speed:** Wait 7 days before escalating to human vs. 3 days

Use PostHog feature flags to split at-risk users between control and variant for each test. Run each test for 2 weeks or until 50+ interventions per variant, whichever is longer. Measure success rate as the primary metric and time-to-resolution as the secondary metric.

When a variant wins with statistical significance (p < 0.05), implement it as the new default for that playbook. Log the change in Attio.

### 5. Segment-specific playbook variants

Using health score data and PostHog cohorts, identify whether playbook effectiveness varies by customer segment:

- **Plan type:** Do enterprise customers respond differently to interventions than SMB?
- **Account age:** Do newer accounts (0-90 days) need different interventions than mature accounts (365+ days)?
- **Usage pattern:** Do power users (top 20% by volume) respond to different messaging than casual users?

Where segment differences are significant (>15% difference in success rate), create segment-specific playbook variants. Deploy them through the routing workflow with segment-based branching.

### 6. Evaluate against threshold

After 2 months, measure:
- 10+ active playbooks (count playbooks with >10 interventions in the last 30 days)
- Scenario coverage >90% (percentage of at-risk users matched to a playbook)
- 500+ monthly interventions (total interventions in the most recent 30-day window)
- >=55% success rate across all playbooks

If PASS, proceed to Durable. If FAIL, focus on the playbooks with the lowest success rates -- can they be improved through further A/B testing, or should they be retired and replaced?

## Time Estimate

- 10 hours: Analyzing coverage gaps and creating 5+ new playbooks
- 12 hours: Building and deploying the composite health score model
- 8 hours: Deploying health score alerting and connecting to intervention routing
- 15 hours: Designing, deploying, and analyzing A/B tests across playbooks
- 8 hours: Segment analysis and segment-specific variant creation
- 7 hours: Ongoing monitoring, evaluation, and iteration over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, cohorts, feature flags for A/B tests, health score events | Free up to 1M events/mo; https://posthog.com/pricing |
| Attio | CRM for health scores, intervention logging, segment tracking | Free for small teams; https://attio.com/pricing |
| Intercom | In-app messaging for proactive nudges and tier-specific interventions | From $39/seat/mo; https://www.intercom.com/pricing |
| Loops | Email sequences for multi-step intervention playbooks | Free up to 1K contacts; https://loops.so/pricing |
| n8n | Workflow automation for scoring, routing, A/B test management | Free self-hosted; cloud from $20/mo; https://n8n.io/pricing |

## Drills Referenced

- `ab-test-orchestrator` -- designs and runs A/B tests on playbook intervention variants using PostHog feature flags
- `health-score-model-design` -- builds the 4-dimension composite health score that improves intervention precision
- `health-score-alerting` -- routes health score changes to interventions, adding composite scoring to signal-based routing
