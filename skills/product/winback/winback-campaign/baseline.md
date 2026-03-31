---
name: winback-campaign-baseline
description: >
  Churned User Win-back — Baseline Run. Automate winback email sequences per churn
  reason segment with triggered sends, in-app welcome-back messages for returning
  users, and continuous reactivation tracking. First always-on winback system.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥15% reactivation rate sustained over 2 consecutive weeks"
kpis: ["Reactivation rate", "Email open rate", "Reactivation rate by segment", "30-day retention of reactivated users"]
slug: "winback-campaign"
install: "npx gtm-skills add product/winback/winback-campaign"
drills:
  - posthog-gtm-events
  - winback-campaign
  - threshold-engine
---

# Churned User Win-back — Baseline Run

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

Turn the manual Smoke batch into an always-on automated winback system. The agent configures triggered email sequences per churn reason segment, in-app welcome-back messages for returning users, and continuous tracking of reactivation and retention. New churners enter the appropriate sequence automatically.

Pass threshold: **≥15% reactivation rate sustained over 2 consecutive weeks** across all active segments.

## Leading Indicators

- Automated sequences trigger within 24 hours of a user entering the "churned" state
- Email open rates exceed 35% across segments (indicates deliverability and subject lines are working)
- At least 2 segments produce reactivation rates above 10%
- Returning churned users see the welcome-back message and click through

## Instructions

### 1. Configure winback event tracking

Run the `posthog-gtm-events` drill to instrument the full winback lifecycle. Create these PostHog events:

- `winback_email_sent` — emitted when a winback email is triggered. Properties: `user_id`, `segment`, `churn_reason`, `email_step` (1, 2, or 3), `offer_type`, `days_since_churn`
- `winback_engaged` — emitted when a churned user responds. Properties: `user_id`, `engagement_type` (opened, clicked, replied, logged_in), `channel` (email, in_app), `email_step`
- `winback_reactivated` — emitted when a churned user re-subscribes or returns to active usage. Properties: `user_id`, `segment`, `offer_type`, `days_to_reactivation`, `reactivated_plan`
- `winback_retained_30d` — emitted 30 days after reactivation if the user is still active. Properties: `user_id`, `segment`, `reactivated_plan`
- `winback_rechurned` — emitted if a reactivated user churns again within 90 days. Properties: `user_id`, `segment`, `days_to_rechurn`, `original_offer_type`

Build a PostHog funnel: `winback_email_sent` -> `winback_engaged` -> `winback_reactivated` -> `winback_retained_30d`. This is the core conversion funnel for the play.

### 2. Build automated segment-specific sequences

Run the the winback offer personalization workflow (see instructions below) drill to create the full segmentation and offer system. Configure Loops sequences for each churn reason segment:

**Sequence trigger:** n8n workflow fires when an Attio record transitions to "churned" status. The workflow reads the churn reason, assigns the user to a segment, and enrolls them in the matching Loops sequence.

**Per-segment 3-email sequence (using validated Smoke messaging as the starting point):**

- **Email 1 (30 days post-churn):** Acknowledge departure. Share the most relevant improvement for their segment. No hard sell. Single CTA.
- **Email 2 (37 days post-churn, if no engagement on Email 1):** Social proof from a similar customer in their segment. Specific results. For price churners, include ROI data.
- **Email 3 (44 days post-churn, if no engagement on Emails 1-2):** Direct offer with 14-day expiration. Discount, free trial extension, or personal demo depending on segment.

**Exit conditions:** User reactivates (exit immediately), user unsubscribes (exit and mark as do-not-contact), user engages with Email 1 or 2 (let the sequence continue but skip the hard-sell Email 3).

### 3. Configure in-app welcome-back messages

Using the `winback-campaign` drill's step 4 (in-app touchpoints), set up Intercom in-app messages for returning churned users:

- Create a PostHog cohort: "Returning churned users" = users with `churned` lifecycle stage who trigger a new `session_started` event
- When a returning churned user logs in or visits the site, show a personalized Intercom banner:
  - "Welcome back, [name]. Here's what's new since [churn_date]: [2-3 bullet points based on their segment]."
  - One-click reactivation button. Pre-fill their previous plan. Offer data restoration.
  - If they are eligible for a discount (from their Email 3 offer), apply it automatically.

- Frequency cap: Show the welcome-back message once per user per 14 days. Do not nag.

### 4. Route high-value churned users to personal outreach

For users in the High Value sub-segment (top 25% by previous MRR), create an Attio task within 48 hours of churn. Include:
- Churn reason and date
- Pre-churn usage summary from PostHog
- What has shipped since they left that is relevant to their churn reason
- Recommended talking points and offer

The automated email sequence still runs for high-value users, but personal outreach is the primary channel.

### 5. Monitor for 3 weeks

Let the automated system run for 3 full weeks. During weeks 2-3, monitor:
- Are new churners being enrolled in sequences within 24 hours?
- Are emails being delivered? (Check Loops delivery stats for bounce rates)
- Are in-app messages firing when returning users log in?
- Is the reactivation rate trending toward 15%?

After week 1, check interim metrics. If reactivation rate is below 8%, diagnose:
- Are the right users being segmented correctly? (Spot-check 10 users in Attio)
- Are emails reaching inboxes? (Check open rates — below 20% indicates deliverability problems)
- Is the offer relevant to the churn reason? (Check click rates per segment)

### 6. Evaluate against threshold

Run the `threshold-engine` drill at the end of week 2 and again at the end of week 3:

- **Pass (≥15% reactivation for 2 consecutive weeks):** The automated system works. Document which segments perform best. Proceed to Scalable.
- **Marginal (10-15% reactivation):** Stay at Baseline. Test different subject lines or offer types for the worst-performing segment. Re-measure after 1 more week.
- **Fail (<10% reactivation):** Check if the problem is reach (low open rates = deliverability), relevance (low click rates = wrong message), or motivation (high click but no reactivation = weak offer). Fix the weakest link and re-run.

## Time Estimate

- 4 hours: Set up PostHog winback events and funnels
- 6 hours: Configure segment-specific Loops sequences and n8n trigger workflows
- 4 hours: Build Intercom welcome-back messages and high-value routing
- 3 hours: Monitor and debug during first week
- 3 hours: Evaluate metrics, diagnose issues, decide pass/fail

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, cohorts, funnels, returning user detection | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Automated winback email sequences per segment | $49/mo+ based on contacts — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app welcome-back messages for returning churned users | $29/seat/mo Essential; +$99/mo Proactive Support — [intercom.com/pricing](https://www.intercom.com/pricing) |
| n8n | Churn trigger workflow, sequence enrollment routing | Self-hosted free; Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | Churned customer records, high-value routing tasks | Free up to 3 seats — [attio.com/pricing](https://attio.com/pricing) |

**Play-specific cost at Baseline:** ~$75-175/mo (Loops paid tier + Intercom Proactive Support if >1,000 users)

## Drills Referenced

- `posthog-gtm-events` — winback lifecycle event tracking and core conversion funnel
- the winback offer personalization workflow (see instructions below) — segment-specific offer design and sequence configuration
- `winback-campaign` — email sequence templates and in-app welcome-back flow
- `threshold-engine` — evaluate reactivation rate against the ≥15% pass threshold
