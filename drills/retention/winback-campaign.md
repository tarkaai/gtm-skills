---
name: winback-campaign
description: Build and send targeted winback campaigns to churned users segmented by churn reason, with multi-channel delivery and reactivation tracking
category: Retention
tools:
  - Loops
  - PostHog
  - Attio
  - Intercom
  - n8n
fundamentals:
  - loops-broadcasts
  - loops-sequences
  - loops-transactional
  - posthog-cohorts
  - posthog-custom-events
  - attio-lists
  - attio-contacts
  - intercom-in-app-messages
  - n8n-triggers
  - n8n-workflow-basics
---

# Winback Campaign

This drill builds targeted campaigns to re-engage customers who have cancelled or gone inactive. It segments churned users by reason and timing, delivers personalized winback messaging through email and in-app channels, and tracks reactivation through to retention.

## Input

- Attio with churned customer records including churn reason and date
- PostHog with historical usage data for churned accounts
- Loops configured for broadcast and triggered emails
- Intercom configured for in-app messaging
- At least 30 churned customers to segment meaningfully
- Output from the `churn-signal-extraction` drill (churn reasons and pre-churn behavior data)

## Steps

### 1. Segment churned customers

Using `attio-lists`, pull all churned customers. Using `posthog-cohorts`, enrich each record with pre-churn behavior. Classify into segments:

- **Price churners:** Cancelled citing cost. Billing-related events in last 30 days before churn.
- **Missing feature churners:** Cancelled because the product lacked something they needed. Feature request tickets or support conversations mentioning specific capabilities.
- **Competitor churners:** Switched to a competitor. Mentioned competitor in exit survey or abrupt usage stop.
- **Poor experience churners:** Cancelled due to bugs, poor support, or frustration. High support ticket volume or error events before churn.
- **Inactive churners:** Never fully activated or gradually stopped using the product. Low feature breadth, declining sessions for 8+ weeks.
- **Business change churners:** Company closed, role changed, or project ended. Exclude from winback — mark as do-not-contact.

Sub-segment by recency: Fresh (0-30 days), Mid (31-90 days), Stale (91-180 days), Cold (180+ days).
Sub-segment by value: High (top 25% by previous MRR), Standard (middle 50%), Low (bottom 25%).

### 2. Design segment-specific campaigns

Each segment gets a different approach and offer:

- **Price churners:** Lead with a discount, extended trial, or a new lower-tier plan. "We launched a Starter plan at $X/mo — everything you used, at a price that works." Include specific features they used.
- **Missing feature churners:** Only contact when the requested feature has shipped. "You asked for X — we built it. Here is a 14-day free pass to try it." Link directly to the feature.
- **Competitor churners:** Lead with differentiation. Share what has improved since they left. Include a comparison or case study.
- **Poor experience churners:** Acknowledge the issue directly. Explain what was fixed. Offer a personal walkthrough.
- **Inactive churners:** Re-educate on value. Share a case study from a similar company. Offer a new onboarding experience.

### 3. Build email sequences

Using `loops-sequences`, create a 3-email winback sequence per segment:

- **Email 1 (trigger: segment assignment or 30 days post-churn):** Acknowledge their departure. Share the most relevant improvement for their segment. No hard sell. Single CTA.
- **Email 2 (7 days after Email 1, if no engagement):** Social proof from a similar customer. Specific results or testimonial relevant to their churn reason.
- **Email 3 (14 days after Email 1, if no engagement):** Direct offer with 14-day expiration. Discount, free trial, or personal demo depending on segment.

Exit conditions: User reactivates (exit immediately). User unsubscribes (exit and mark do-not-contact). User engages with Email 1 or 2 (continue sequence but skip hard-sell Email 3).

For Smoke level, use `loops-broadcasts` for manual one-time sends instead of automated sequences.

### 4. Add in-app touchpoints for returning users

Using `intercom-in-app-messages`, set up welcome-back messages for churned users who return to the site or log into an expired account:

- Detect returning churned users via PostHog cohort: users with `churned` lifecycle stage who trigger a new `session_started` event
- Show a personalized banner: "Welcome back, [name]. Here's what's new since [churn date]: [2-3 bullet points based on their segment]."
- One-click reactivation CTA. Pre-fill their previous plan. Offer data and settings restoration.
- If eligible for a discount, apply it automatically on reactivation.
- Frequency cap: Show once per user per 14 days.

### 5. Route high-value winbacks to personal outreach

For High Value sub-segment churned accounts, create Attio tasks for the account owner. Include:
- Churn reason and date
- Pre-churn usage summary from PostHog (features used, engagement level)
- What has changed since they left (product improvements relevant to their churn reason)
- Recommended offer and talking points

Automated email sequence still runs, but personal outreach is the primary channel for high-value accounts.

### 6. Track winback metrics

Using `posthog-custom-events`, track the full lifecycle:

- `winback_email_sent`: Properties: user_id, segment, email_step, offer_type, days_since_churn
- `winback_engaged`: Properties: user_id, engagement_type (opened, clicked, replied, logged_in), channel
- `winback_reactivated`: Properties: user_id, segment, offer_type, days_to_reactivation, reactivated_plan
- `winback_retained_30d`: Properties: user_id, segment, reactivated_plan
- `winback_rechurned`: Properties: user_id, segment, days_to_rechurn, original_offer_type

Calculate reactivation rate per segment, per email step, and per channel. Target: 10-15% overall reactivation rate. If a segment consistently fails to reactivate (<3% for 8+ weeks), stop spending resources on it and focus upstream on the `churn-prevention` drill.

## Output

- Segment-specific winback email sequences configured in Loops
- In-app welcome-back messages configured in Intercom
- High-value winback tasks routed to account owners in Attio
- Full lifecycle event tracking in PostHog
- Reactivation funnel: email_sent -> engaged -> reactivated -> retained_30d

## Triggers

- **Smoke:** Run once manually with a batch of 30-50 churned users
- **Baseline:** Automated: new churners enrolled in sequences within 24 hours of churn
- **Scalable:** Automated with multi-channel escalation for non-responders and A/B testing
- **Durable:** Autonomous optimization of offers, timing, and messaging
