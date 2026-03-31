---
name: winback-campaign-smoke
description: >
  Churned User Win-back — Smoke Test. Manually segment a batch of churned users by
  churn reason, send personalized winback messages, and measure whether any reactivate.
  Proves the signal: can targeted outreach bring churned users back?
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥10% reactivation rate from a 30-50 user batch"
kpis: ["Reactivation rate", "Email response rate", "Days to reactivation"]
slug: "winback-campaign"
install: "npx gtm-skills add product/winback/winback-campaign"
drills:
  - churn-signal-extraction
  - winback-campaign
  - threshold-engine
---

# Churned User Win-back — Smoke Test

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

Prove that personalized outreach to churned users based on their churn reason produces reactivation. At Smoke, you are running one manual batch — no automation, no always-on. The agent helps identify churned users, segment them by reason, draft messages, and track responses. A human reviews and sends.

Pass threshold: **≥10% of contacted churned users reactivate** (re-subscribe, re-login to active session, or re-engage with core feature) within 7 days.

## Leading Indicators

- Churned user list can be pulled from Attio and enriched with PostHog pre-churn data
- Churn reason segmentation produces at least 3 distinct segments with 5+ users each
- Winback emails achieve >40% open rate (indicates subject lines and sender are resonating)
- At least some users click through or reply within 48 hours

## Instructions

### 1. Extract and segment churned users

Run the `churn-signal-extraction` drill in manual mode. Instead of configuring the daily n8n workflow, run the PostHog HogQL query directly via the PostHog API or MCP to pull all users who churned in the last 90 days.

For each churned user, extract:
- Churn date
- Last active date
- Features they used most before churning
- Support ticket history in the 30 days before churn
- Whether they visited billing/cancellation pages
- Cancellation survey response (if available from Attio)

Segment each user into exactly one churn reason: price, missing feature, competitor, poor experience, inactive, or business change. Exclude business change users — they are not winback candidates.

Select 30-50 users across at least 3 segments. Aim for 10-15 users per segment so you can compare response rates.

### 2. Design segment-specific winback messages

Run the `winback-campaign` drill's step 2 (design segment-specific campaigns). For each segment, write one email:

- **Price churners:** Lead with a discount or mention of a new lower-tier plan. "We launched a Starter plan at $X/mo — everything you used, at a price that works." Include specific features they used.
- **Missing feature churners:** Only include users whose requested feature has shipped or has an equivalent. "You asked for [feature] — we built it. Here is a 14-day free pass to try it." Link directly to the feature.
- **Competitor churners:** Lead with what has improved since they left. Include a specific comparison point. "Since you left, we shipped [X, Y, Z]. Here is how we compare now: [link]."
- **Poor experience churners:** Acknowledge the issue by name. Explain what was fixed. "You had trouble with [issue]. We fixed it — here is what changed: [details]. Want a personal walkthrough?"
- **Inactive churners:** Re-educate on value. "Most teams like yours get the most value from [feature]. Here is a 5-minute guide to get started: [link]."

Each email: under 150 words, one clear CTA, personal sender (founder or product lead), no marketing template. These should read like a real person wrote them.

**Human action required:** Review all message drafts before sending. Verify tone is helpful, not desperate. Ensure each email references something specific to the user's history.

### 3. Send the winback batch

Send all emails within a single day via your email client or Loops (manual send, not automated sequence). Log each send as a PostHog custom event: `winback_email_sent` with properties: `user_id`, `segment`, `churn_reason`, `churn_date`, `days_since_churn`, `offer_type`.

### 4. Track responses for 7 days

Monitor daily:
- Email opens and clicks
- Email replies
- Return-to-product activity (new sessions from contacted users in PostHog)
- Reactivations (re-subscription or return to active usage)

Log each engagement as a PostHog event: `winback_engaged` with properties: `user_id`, `engagement_type` (opened, clicked, replied, logged_in, reactivated). Log each reactivation as: `winback_reactivated` with properties: `user_id`, `segment`, `offer_type`, `days_to_reactivation`.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure: of the 30-50 churned users contacted, what percentage reactivated within 7 days?

- **Pass (≥10% reactivation):** Personalized winback works for your product. Note which segments performed best. Proceed to Baseline.
- **Marginal (5-10% reactivation):** Check segment-level performance. If one segment drives all reactivations, that segment works — focus Baseline on it and re-test other segments with different messaging.
- **Fail (<5% reactivation):** Diagnose: Were the segments accurate? Was the messaging specific enough? Were you reaching users who are actually reachable (valid email, not unsubscribed)? Adjust and re-run with a new batch.

Also note: which segments had the highest response rate? Which had zero? This data shapes the Baseline automation.

## Time Estimate

- 2 hours: Extract churned users from Attio and PostHog, segment by churn reason
- 2 hours: Write segment-specific winback emails, review with team
- 1 hour: Send emails, configure PostHog event tracking
- 1 hour: Review responses after 7 days, calculate metrics, evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Pre-churn usage data, event tracking, response monitoring | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Churned customer records, churn reason data | Free up to 3 seats — [attio.com/pricing](https://attio.com/pricing) |
| Loops | Email sending (optional, can use personal email for Smoke) | Free up to 1,000 contacts — [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost at Smoke:** Free (all tools within free tiers for a 30-50 user batch)

## Drills Referenced

- `churn-signal-extraction` — pull churned users from PostHog, extract pre-churn behavior signals, segment by churn reason
- `winback-campaign` — design segment-specific winback messaging and offers
- `threshold-engine` — evaluate reactivation rate against the ≥10% pass threshold
