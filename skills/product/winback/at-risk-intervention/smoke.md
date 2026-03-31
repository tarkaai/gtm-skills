---
name: at-risk-intervention-smoke
description: >
  At-Risk User Intervention — Smoke Test. Identify users showing churn signals, send one
  manual intervention batch, and measure whether proactive outreach produces any save signal.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥30% response rate from intervened users"
kpis: ["Response rate", "Save rate", "Days to response"]
slug: "at-risk-intervention"
install: "npx gtm-skills add product/winback/at-risk-intervention"
drills:
  - churn-risk-scoring
  - churn-prevention
  - threshold-engine
---

# At-Risk User Intervention — Smoke Test

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

Prove that proactive outreach to users showing churn signals produces a measurable response. At Smoke, you are running one manual batch to validate that the signal (churn risk score) and the intervention (outreach) connect. No automation, no always-on systems.

Pass threshold: **≥30% of intervened users respond** (open + click, reply, or take the prompted action) within 7 days.

## Leading Indicators

- At-risk users can be identified from PostHog usage data (the scoring query returns results)
- Intervention messages are delivered without bounces or errors
- At least some users engage within 48 hours of receiving the intervention

## Instructions

### 1. Build a manual churn risk list

Run the `churn-risk-scoring` drill in manual mode. Instead of setting up the daily n8n workflow, run the PostHog HogQL query from step 1 of that drill directly via the PostHog API or MCP. Identify users who match at least 2 churn signals:
- Sessions dropped >50% vs. their 30-day average
- No core action in the last 7 days
- No login for 7+ days when they previously averaged 3+/week
- Visited billing or cancellation page in the last 7 days

Export a list of 20-30 users with their specific signals. For each user, note which signals fired and what their usage pattern was before the decline.

### 2. Design three intervention messages

Using the `churn-prevention` drill's tiered intervention design (step 3), write three message templates:

- **In-app (Intercom):** A short, specific message that acknowledges the user's situation without being creepy. Reference a feature or workflow relevant to their usage history. Under 40 words. Single CTA linking to the relevant feature or a help article.
- **Email (Loops):** A personal-feeling email from the founder or head of product. Reference what the user was doing before the decline. Offer a specific resource (not a generic "let us know if you need help"). Include a calendar link for a 15-minute call.
- **Direct (personal):** For the 3-5 highest-value users on the list, write a custom message referencing their specific account and usage.

**Human action required:** Review all three message templates before sending. Verify the tone is helpful, not desperate. Ensure no user receives more than one intervention type.

### 3. Send the intervention batch

Assign each user to one channel based on their risk tier and value:
- Medium risk users -> in-app message via Intercom
- High risk users -> email via Loops
- Critical risk users -> personal outreach

Send all interventions within a single day. Log each send as a PostHog custom event: `intervention_sent` with properties `user_id`, `channel`, `risk_tier`, `risk_score`, `signals`.

### 4. Track responses for 7 days

Monitor daily: email opens, email clicks, email replies, in-app message clicks, personal outreach replies, and any return-to-product activity from intervened users. Log each response as a PostHog event: `intervention_engaged` with properties `user_id`, `channel`, `engagement_type`.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure: of the 20-30 users who received intervention, what percentage engaged within 7 days?

- **Pass (≥30% response rate):** The signal-to-intervention connection works. Proceed to Baseline to automate it.
- **Fail (<30% response rate):** Diagnose: Were the signals accurate (did these users actually show declining usage)? Was the messaging relevant? Was the channel right? Adjust signals or messaging and run another batch.

## Time Estimate

- 2 hours: Run churn risk query, build user list, analyze signals
- 2 hours: Write intervention message templates, assign users to channels
- 1 hour: Send interventions, set up tracking events
- 1 hour: Review responses after 7 days, calculate metrics

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data queries, cohort analysis, event tracking | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app intervention messages | $29/seat/mo Essential — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered intervention emails | Free up to 1,000 contacts — [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost at Smoke:** Free (all tools within free tiers for a 20-30 user batch)

## Drills Referenced

- `churn-risk-scoring` — identify at-risk users from PostHog usage data and score by severity
- `churn-prevention` — design tiered intervention messages matched to risk level
- `threshold-engine` — evaluate response rate against the ≥30% pass threshold
