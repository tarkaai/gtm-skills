---
name: power-user-program-baseline
description: >
  Power User Program — Baseline Run. Launch a tiered advocacy program (Insider,
  Advocate, Ambassador) with automated enrollment, recognition, and first-action
  activation. Run always-on for 4 weeks and measure advocate activation rate.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=40% of enrolled Insiders complete their first advocacy action within 30 days"
kpis: ["Insider enrollment rate", "First-action activation rate (30-day)", "Referral submission rate", "Testimonial yield"]
slug: "power-user-program"
install: "npx gtm-skills add product/referrals/power-user-program"
drills:
  - advocacy-program-design
  - posthog-gtm-events
  - advocacy-activation-pipeline
---

# Power User Program — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

A tiered advocacy program runs always-on: power users are automatically enrolled as Insiders when they cross score 60, they receive in-app recognition and exclusive access, and automated sequences guide them toward their first advocacy action. After 4 weeks, at least 40% of enrolled Insiders have completed a testimonial, referral, or review.

## Leading Indicators

- Enrollment celebration messages have a >60% view rate in Intercom (users are seeing the program)
- Welcome email sequence has >40% open rate in Loops (messaging resonates)
- At least 30% of enrolled users click a referral link or testimonial CTA within 14 days
- At least 5 Insiders are promoted to Advocate within the first 4 weeks
- Referral links are being shared (link-click events in PostHog)

## Instructions

### 1. Design the advocacy program

Run the `advocacy-program-design` drill to produce the full program specification:

- Define the 3-tier structure: Insider (score 60-79), Advocate (score 80-89), Ambassador (score 90+, sustained 3 months)
- Design tier benefits: Insider gets early feature access + insider email + profile badge. Advocate adds roadmap preview + community channel + referral rewards. Ambassador adds advisory board + co-marketing + product leadership access.
- Define advocacy asks per tier: Insider opts into testimonial list and surveys. Advocate provides a testimonial, refers 1 lead/quarter, participates in case study. Ambassador speaks at events, provides ongoing referrals, serves as sales reference.
- Design the recognition system: in-app enrollment celebration, tier promotion modal, milestone thank-you messages
- Build email sequences: Insider welcome (3 emails / 2 weeks), Advocate activation (4 emails / 3 weeks)
- Define the event schema for all advocacy actions in PostHog

**Human action required:** Review the program specification. Approve tier benefits (especially anything that requires engineering: feature flags, badges, early access). Confirm the advocacy asks are realistic for your user base. Approve email sequence copy.

### 2. Instrument advocacy tracking

Run the `posthog-gtm-events` drill to set up comprehensive tracking:

- Implement all advocacy events: `advocacy_tier_enrolled`, `advocacy_action_completed`, `advocacy_referral_submitted`, `advocacy_tier_promoted`
- Set person properties: `advocacy_tier`, `advocacy_enrolled_date`, `advocacy_actions_count`, `advocacy_referrals_count`
- Build the advocacy funnel in PostHog: eligible -> enrolled -> first action -> active advocate
- Create the advocacy dashboard: enrollment rate trend, activation funnel, referral pipeline, tier distribution

### 3. Launch the automated activation pipeline

Run the `advocacy-activation-pipeline` drill to deploy the always-on automation:

- Configure the daily recruitment workflow in n8n: query Attio for score-60+ users not yet enrolled, filter out ineligible users (too new, declined, open tickets), auto-enroll in Insider tier
- Set up event-driven enrollment: when `power_user_score_computed` crosses a tier threshold, immediately trigger enrollment or promotion
- Deploy tier enrollment automations: enable PostHog feature flags for perks, queue Intercom celebration messages, add to Loops welcome sequences, update Attio records
- Configure the first-action nudge sequence: Day 7 in-app message, Day 14 email with pre-filled testimonial template, Day 21 alternative ask (referral link), Day 30 mark as enrolled-but-inactive
- Set up referral tracking: validate submitted referrals, track the referral funnel (submitted -> signed up -> activated), notify referrers at each stage, trigger reward delivery

### 4. Monitor for 4 weeks

Let the pipeline run without intervention for 4 weeks. Monitor the advocacy dashboard daily:

- Is enrollment happening? (daily new Insiders count)
- Are users seeing recognition messages? (Intercom delivery rates)
- Are users opening advocacy emails? (Loops sequence metrics)
- Are users completing advocacy actions? (PostHog funnel conversion)
- Are referrals being submitted and converting? (referral pipeline metrics)

Do not tweak the system during the first 4 weeks. Collect clean baseline data.

### 5. Evaluate against threshold

After 4 weeks, compute:

- **First-action activation rate**: count of Insiders who completed at least one advocacy action within 30 days of enrollment / total Insiders enrolled in the first 2 weeks (use the first 2 weeks to allow 30-day measurement window)
- **Pass threshold**: >=40%

If PASS: the advocacy program activates power users at a rate that justifies scaling. Proceed to Scalable.
If FAIL (30-39%): the program structure is sound but activation is slow. Diagnose where users drop off in the nudge sequence. Test different asks or timing. Re-run for 2 more weeks.
If HARD FAIL (<30%): the program benefits may not be compelling enough, or the scoring model is surfacing users who are not actually advocacy-ready. Review the top 20 enrolled users manually and check if they match the Smoke test profile.

## Time Estimate

- 6 hours: advocacy program design and specification review
- 4 hours: PostHog event instrumentation and dashboard setup
- 6 hours: n8n automation pipeline configuration and testing
- 2 hours: Intercom and Loops message/sequence creation
- 2 hours: 4-week monitoring and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring, cohorts, feature flags, funnels, dashboard | Free tier: 1M events/mo, 1M flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app enrollment celebrations, nudge messages, recognition | Essential: $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Welcome sequences, nudge emails, referral notifications | Starter: $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Recruitment automation, enrollment workflows, referral tracking | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Scored user records, advocacy tier tracking, pipeline management | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $50-100/mo (Intercom seat + Loops starter; n8n self-hosted is free)

## Drills Referenced

- `advocacy-program-design` — designs the 3-tier advocacy program with benefits, asks, recognition, and email sequences
- `posthog-gtm-events` — instruments all advocacy events and builds the measurement layer
- `advocacy-activation-pipeline` — automates recruitment, enrollment, first-action nudges, and referral tracking
