---
name: best-practices-content-baseline
description: >
  In-App Best Practices — Baseline Run. Always-on automated delivery of best-practices
  cards via Intercom and Loops, with behavioral triggers, frequency caps, and full
  funnel tracking in PostHog. Proves engagement holds over 2 weeks with automation.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Content"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥30% engagement rate and ≥5pp retention lift vs. control group over 2 weeks"
kpis: ["Card engagement rate", "Card completion rate", "Retention lift vs. control", "Dismissal rate"]
slug: "best-practices-content"
install: "npx gtm-skills add product/retain/best-practices-content"
drills:
  - posthog-gtm-events
  - best-practices-delivery-automation
  - feature-adoption-monitor
---

# In-App Best Practices — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Content

## Outcomes

30% or more of eligible users engage with best-practices cards (click CTA) over 2 weeks of always-on automated delivery, with at least 5 percentage points higher 30-day retention compared to a control group that receives no tips. This proves that (a) automated delivery sustains the engagement signal from the Smoke test, and (b) the tips measurably improve retention, not just engagement.

## Leading Indicators

- Control group engagement rate stays below 20% for organic best-practices discovery (validates the automation is causing the lift, not just natural behavior)
- Delivery automation running daily without errors (n8n workflow health green for 14 consecutive days)
- No single card's dismissal rate exceeds 40% (cards are not perceived as spam)
- Email fallback conversion rate above 8% (users who missed the in-app tip engage via email)
- At least 15% of users who click a card CTA complete the practice within 24 hours (the tips are actionable, not just interesting)

## Instructions

### 1. Set up full event tracking

Run the `posthog-gtm-events` drill to instrument comprehensive tracking for the best-practices system:

| Event | When Fired | Key Properties |
|-------|-----------|---------------|
| `best_practice_shown` | Card displayed to user (any surface) | `card_id`, `category`, `surface` (in-app, email, web), `trigger_event`, `variant` (treatment/control) |
| `best_practice_clicked` | User clicks the CTA on the card | `card_id`, `category`, `surface` |
| `best_practice_completed` | User performs the recommended behavior within 24h | `card_id`, `category`, `surface`, `time_to_complete_seconds` |
| `best_practice_dismissed` | User dismisses or closes the card | `card_id`, `category`, `surface` |
| `best_practice_email_opened` | User opens the best-practices digest email | `card_id`, `email_template_id` |
| `best_practice_email_clicked` | User clicks a link in the best-practices email | `card_id`, `email_template_id` |

Build PostHog funnels:
- **In-app funnel:** `best_practice_shown` -> `best_practice_clicked` -> `best_practice_completed`
- **Email funnel:** `best_practice_email_opened` -> `best_practice_email_clicked` -> `best_practice_completed`
- **Cross-surface:** Break down both funnels by `card_id` and `surface`

Set up a PostHog A/B split using feature flags: 50% treatment (receives automated tips) vs. 50% control (no tips, tracked for organic behavior).

### 2. Deploy always-on delivery automation

Run the `best-practices-delivery-automation` drill to build the automated delivery system:

1. Create PostHog eligibility cohorts for each content card based on `trigger_event` and `exclude_event` criteria
2. Configure Intercom in-app messages for each card: tooltip or banner format, contextual placement on the relevant product screen, deep link CTA
3. Configure Loops email sequence as a fallback: users who saw the in-app tip 48+ hours ago but did not click receive an email with the tip content
4. Build the n8n orchestration workflow running daily at 09:00 UTC:
   - Query eligible users per card from PostHog
   - Apply frequency caps: maximum 1 tip per user per day (in-app), maximum 1 per week (email)
   - Rank cards by retention lift for each user and deliver the highest-value card first
   - Log delivery events back to PostHog
5. Set up delivery health alerts: low delivery rate (<10% of eligible users), high dismissal rate (>50% on any card), decreasing completion rate

**Critical:** Ensure the feature flag from Step 1 gates the delivery automation. Only users in the treatment group receive tips. Control group users are tracked but never shown tips.

### 3. Monitor feature adoption impact

Run the `feature-adoption-monitor` drill adapted for best-practices engagement:

- Build a PostHog dashboard tracking: tips delivered per day, engagement rate (treatment vs. control), completion rate by card, dismissal rate by card, retention curve (treatment vs. control)
- Configure stalled-user detection: users who were shown 3+ tips but clicked none in 14 days. These users may need a different content format or delivery surface.
- Set up n8n alerts: if treatment group engagement rate drops below the control group for 3 consecutive days, something is wrong — pause delivery and investigate.

### 4. Evaluate against threshold

At the end of 2 weeks, compare treatment vs. control:

- **Treatment engagement rate:** Users in treatment who clicked at least one card CTA / total treatment group size (target: >=30%)
- **Control organic rate:** Users in control who organically discovered and used best practices / total control group size
- **Retention lift:** 30-day retention of treatment group minus 30-day retention of control group (target: >=5pp)

- **Pass (>=30% engagement AND >=5pp retention lift):** Automated best-practices delivery reliably drives engagement and measurably improves retention. Proceed to Scalable to personalize across segments.
- **Fail:** Diagnose: If engagement is high but retention lift is low, the tips are interesting but not driving behavior change — rewrite tips to be more actionable with clearer steps. If engagement is low, the delivery mechanism is the bottleneck — test different formats (video tips, interactive walkthroughs) or different timing (trigger after a specific action instead of daily delivery). Re-run for another 2 weeks.

## Time Estimate

- 4 hours: Event taxonomy setup, PostHog funnels, feature flag A/B split configuration
- 4 hours: Delivery automation build (Intercom messages, Loops sequences, n8n orchestration workflow)
- 4 hours: Feature adoption monitor setup, dashboard, stalled-user detection, alerts
- 4 hours: Week 1 and Week 2 analysis, treatment vs. control comparison, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, cohorts, dashboards | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app message delivery with contextual placement | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Email fallback delivery for non-engagers | Free up to 1,000 contacts — https://loops.so/pricing |
| n8n | Daily orchestration workflow, frequency caps, alerts | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |

**Play-specific cost:** ~$0-24/mo (n8n Cloud if not self-hosted; everything else within free tiers)

## Drills Referenced

- `posthog-gtm-events` — instrument the full best-practices event taxonomy with treatment/control split
- `best-practices-delivery-automation` — always-on contextual delivery via Intercom and Loops with behavioral triggers and frequency caps
- `feature-adoption-monitor` — dashboard, stalled-user detection, and automated alerts for delivery health
