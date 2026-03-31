---
name: winback-campaign
description: Re-engage churned customers with targeted campaigns based on their churn reason and history
category: Product
tools:
  - Loops
  - PostHog
  - Attio
  - Intercom
fundamentals:
  - loops-broadcast-setup
  - loops-transactional-emails
  - posthog-cohort-analysis
  - attio-list-management
  - intercom-in-app-messages
---

# Winback Campaign

This drill builds targeted campaigns to re-engage customers who have cancelled or gone inactive. It segments churned users by reason and timing to deliver personalized winback messaging that addresses their specific concerns.

## Prerequisites

- Attio with churned customer records including churn reason and date
- Loops configured for broadcast and triggered emails
- PostHog with historical usage data for churned accounts
- At least 30 churned customers to segment meaningfully

## Steps

### 1. Segment churned customers

Using the `attio-list-management` fundamental, pull all churned customers and segment by:

- **Churn reason**: Price, missing feature, switched to competitor, no longer needed, poor experience
- **Churn recency**: Last 30 days, 30-90 days, 90+ days
- **Previous engagement**: Power users who churned vs. users who never fully activated
- **Account value**: High-value accounts get personal outreach, low-value get automated campaigns

Using `posthog-cohort-analysis`, enrich each segment with pre-churn usage data: what features they used, when usage declined, and what their last actions were.

### 2. Design segment-specific campaigns

Each segment gets a different winback approach:

- **Price churners**: Lead with a discount, extended trial, or a new lower-tier plan. "We've added a Starter plan that might be a better fit."
- **Missing feature churners**: Wait until you have shipped the feature (or something close). "You asked for X — we built it."
- **Competitor churners**: Lead with differentiation. Share what you have improved since they left. Include a comparison or case study.
- **Poor experience churners**: Acknowledge the issue directly. Explain what you fixed. Offer a personal walkthrough.
- **Inactive churners**: Re-educate on value. Share customer success stories similar to their profile.

### 3. Build the email sequences

Using `loops-broadcast-setup`, create a 3-email winback sequence per segment:

- **Email 1 (30 days post-churn)**: Acknowledge their departure. Share what has changed since they left. No hard sell.
- **Email 2 (45 days post-churn)**: Social proof from a customer in their segment. Specific results or testimonial.
- **Email 3 (60 days post-churn)**: Direct offer — discount, extended trial, or personal demo. Clear expiration on the offer.

### 4. Add in-app touchpoints for returning users

If a churned user returns to your site or logs into an expired account, use the `intercom-in-app-messages` fundamental to show a personalized welcome-back message. Highlight what is new and offer to restore their data or settings. Make it easy to reactivate with one click.

### 5. Route high-value winbacks to sales

For high-value churned accounts, do not rely on automated email alone. Create winback tasks in Attio for the account owner. Include the churn reason, usage history, and what has changed since they left. A personal call from someone who knows their history is worth more than any email sequence.

### 6. Measure winback rates

Track reactivation rate per segment, per email, and per channel. Calculate winback revenue as a percentage of churned revenue. Healthy target: 5-10% reactivation rate within 90 days of churn. If a segment consistently fails to reactivate, stop spending resources on it and focus on prevention via the `churn-prevention` drill.
