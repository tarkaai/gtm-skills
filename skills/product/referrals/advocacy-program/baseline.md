---
name: advocacy-program-baseline
description: >
  Formal Advocacy Program — Baseline Run. First always-on automation: referral tracking,
  tier enrollment, nudge sequences, and reward delivery running continuously.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Events"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=30 advocates with >=5 referrals submitted and >=40% activation rate"
kpis: ["Advocate enrollment count", "Activation rate (first action within 30 days)", "Referrals submitted", "Referral conversion rate"]
slug: "advocacy-program"
install: "npx gtm-skills add product/referrals/advocacy-program"
drills:
  - posthog-gtm-events
  - referral-program
  - advocacy-activation-pipeline
---

# Formal Advocacy Program — Baseline Run

> **Stage:** Product -> Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Events

## Outcomes

30 or more enrolled advocates, 5 or more referrals submitted across the cohort, and a 40%+ activation rate (advocates who complete their first advocacy action within 30 days of enrollment). The key proof at Baseline: the program runs continuously without manual recruitment or follow-up.

## Leading Indicators

- Daily recruitment automation firing and enrolling new users crossing score thresholds
- Enrollment welcome sequences delivering with >= 50% open rate
- Nudge sequences triggering on schedule (day 7/14/21/30 cadence)
- Referral links being generated and attached to advocate records in Attio
- At least 1 referral conversion (referee signed up and activated)

## Instructions

### 1. Implement the event taxonomy

Run the `posthog-gtm-events` drill to establish the full event taxonomy for the advocacy program. Beyond the Smoke-level events, add:

- `advocacy_enrollment_invitation_sent` — tracks outbound recruitment
- `advocacy_enrollment_invitation_opened` — email/message engagement
- `advocacy_nudge_sent` — day 7/14/21/30 follow-up nudges
- `advocacy_nudge_clicked` — nudge engagement
- `advocacy_referral_link_shared` — advocate shared their link (distinct from referral submitted)
- `advocacy_referral_signed_up` — referee completed signup
- `advocacy_referral_activated` — referee reached activation milestone
- `advocacy_reward_issued` — reward delivered to referrer

Build PostHog funnels:
- **Enrollment funnel**: invitation_sent -> invitation_opened -> tier_enrolled -> first_action_completed
- **Referral funnel**: referral_link_shared -> referral_submitted -> referral_signed_up -> referral_activated -> reward_issued

### 2. Build the referral mechanism

Run the `referral-program` drill to set up the referral infrastructure:

- Generate unique referral links per advocate (tracked in Attio and PostHog)
- Implement two-sided rewards: referrer gets account credit, referee gets extended trial
- Configure referral tracking: link shared -> clicked -> signed up -> activated -> reward unlocked
- Build automated reward fulfillment via Loops transactional emails at each funnel stage
- Prompt referrals at moments of delight: after a successful workflow, after positive NPS, after usage milestones

Set up Intercom in-app referral prompts that trigger contextually based on PostHog events.

### 3. Deploy the always-on activation pipeline

Run the `advocacy-activation-pipeline` drill to automate the full advocacy lifecycle:

**Recruitment automation (daily n8n cron):**
- Query Attio for users with power_user_score >= 60 who are not yet enrolled
- Filter out: users < 30 days old, users who declined, users with open support tickets
- Auto-enroll Insiders (score 60-79), flag Advocates (score 80+) for review
- Enable feature flags, queue Intercom enrollment messages, start Loops welcome sequences

**Event-driven tier promotion:**
- When `power_user_score_computed` fires and score crosses a tier threshold (60, 80, 90), trigger enrollment or promotion immediately
- Update Attio contact: tier, enrolled date, notes

**First-action nudge sequence:**
- Day 7 post-enrollment: if no `advocacy_action_completed`, send Intercom in-app message with the easiest ask
- Day 14: Loops email with pre-filled testimonial template using the user's own usage data
- Day 21: switch the ask (e.g., referral link instead of testimonial)
- Day 30: if still no action, mark "Enrolled but Inactive" in Attio, pause nudges for 60 days

**Referral tracking and reward delivery:**
- Listen for `advocacy_referral_submitted` events via n8n
- Validate referee email, create linked record in Attio (referrer <-> referee)
- Notify referrer at each funnel stage via Loops transactional email
- Trigger reward delivery when referee reaches activation threshold

### 4. Monitor and evaluate

Build a PostHog dashboard with:
- Enrollment funnel conversion rates (weekly trend)
- Activation rate by enrollment cohort
- Referral pipeline: submitted -> signed up -> activated
- Tier distribution over time

Evaluate against threshold after 2 weeks:
- **Pass**: >= 30 advocates AND >= 5 referrals submitted AND >= 40% activation rate
- **Fail**: Diagnose which stage of the pipeline is underperforming. If enrollment is low, check the scoring pipeline. If activation is low, test different asks. If referrals are low, test the incentive structure.

If PASS, proceed to Scalable.

## Time Estimate

- 3 hours: event taxonomy implementation and funnel setup
- 4 hours: referral program build (links, tracking, reward automation)
- 6 hours: advocacy activation pipeline (4 n8n workflows + Intercom/Loops configuration)
- 2 hours: dashboard build and monitoring setup
- 1 hour: threshold evaluation and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, cohorts, dashboards | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Advocate CRM records, referral tracking, list management | Standard stack |
| Loops | Welcome sequences, nudge emails, referral notifications, reward emails | $49/mo for > 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app enrollment messages, referral prompts, nudge messages | $29/seat/mo Essential ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Cron-based recruitment, event-driven workflows, referral tracking | Standard stack |

**Estimated monthly cost: $49-78/mo** (Loops $49 + Intercom if not already on standard stack)

## Drills Referenced

- `posthog-gtm-events` — implement the full advocacy event taxonomy and build enrollment/referral funnels
- `referral-program` — set up referral links, tracking, incentive structure, and automated reward fulfillment
- `advocacy-activation-pipeline` — deploy always-on recruitment, enrollment, nudge sequences, and referral tracking automation
