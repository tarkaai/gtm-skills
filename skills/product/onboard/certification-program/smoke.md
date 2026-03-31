---
name: certification-program-smoke
description: >
  Product Certification Program — Smoke Test. Build a single-tier certification for
  power users with 3-5 modules, action-based assessments, and basic tracking.
  Run with 10-20 users to prove certification drives completion and retention signal.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥20% enrollment rate from prompted users, ≥60% completion rate among enrollees"
kpis: ["Enrollment rate", "Completion rate", "Module drop-off points", "Certified user retention at Day 14"]
slug: "certification-program"
install: "npx gtm-skills add product/onboard/certification-program"
drills:
  - lead-capture-surface-setup
  - threshold-engine
---

# Product Certification Program — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

Prove that a certification program produces signal: users who are prompted will enroll, enrolled users will complete modules, and certified users show early retention signal. No automation, no always-on. This is a one-time local run with a small cohort.

## Leading Indicators

- Users click the certification prompt (enrollment intent)
- Users complete at least Module 1 within 48 hours of starting (momentum)
- Assessment pass rate on first attempt >50% (content clarity)
- At least one certified user returns to the product within 7 days of certification (retention signal)

## Instructions

### 1. Design a single-tier certification curriculum

Run the the certification curriculum design workflow (see instructions below) drill with these constraints:
- Build only Tier 1 (Foundations) — 3-5 modules covering core product workflows
- Each module must have an action-based assessment: the user performs a real action in the product and PostHog captures the event
- Define the scoring rubric: all modules must be completed + all assessments passed to earn the badge
- Set the time limit to 7 days from enrollment start
- Document every PostHog event name and property for the certification funnel

**Human action required:** Review the curriculum before launching. Ensure each module's learning objective maps to a skill that genuinely makes the user more successful with the product. Remove any module that feels like filler.

### 2. Build the certification entry point

Run the `lead-capture-surface-setup` drill to create the enrollment surface:
- Deploy an in-app prompt (Intercom banner or product page) that explains the certification and has a single "Start Certification" CTA
- Target: activated users (activation event fired, active 7+ days, not yet enrolled)
- Track `cert_program_viewed` and `cert_program_enrolled` events in PostHog
- Do NOT build email sequences yet — Smoke is in-app only

### 3. Instrument the certification funnel

Set up PostHog tracking for the full funnel:
- `cert_program_viewed` — user saw the prompt
- `cert_program_enrolled` — user clicked Start
- `cert_tier_started` — user began Tier 1
- `cert_module_completed` — user finished a module (one event per module with module name as property)
- `cert_assessment_completed` — assessment result (passed/failed, attempts, time spent)
- `cert_tier_completed` — all modules done
- `cert_badge_earned` — badge issued

Build a PostHog funnel from `cert_program_viewed` through `cert_badge_earned`.

### 4. Launch to a small test group

Using PostHog feature flags, gate the certification to 10-20 activated users:
- Create a feature flag `cert_program_enabled` that targets a specific user list or random 10% of activated users
- Show the enrollment prompt only to flagged users
- Monitor the PostHog Live Events feed to confirm events fire correctly on the first enrollee

**Human action required:** Manually verify end-to-end flow with one test user before expanding. Complete the certification yourself to confirm every assessment event fires and the badge logic works.

### 5. Monitor for 7 days

Track daily:
- How many prompted users enrolled (enrollment rate)
- How many enrollees completed each module (progression)
- Where users dropped off (which module, which assessment)
- Assessment pass rates per module

Do not intervene during the 7-day run unless tracking is broken. The point is to observe natural behavior.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- **Primary:** ≥20% enrollment rate (enrolled / viewed) AND ≥60% completion rate (badge earned / enrolled)
- **Secondary:** Certified users have higher 14-day retention than non-certified users in the same cohort

If PASS: Document the curriculum, funnel metrics, and any qualitative observations. Proceed to Baseline.
If FAIL: Diagnose — was enrollment low (prompt is not compelling) or completion low (content too long, assessments too hard, modules unclear)? Fix the weakest point and re-run Smoke.

## Time Estimate

- 2 hours: Curriculum design (modules, assessments, scoring rubric)
- 1 hour: Build enrollment prompt and PostHog tracking
- 0.5 hours: Configure feature flag and launch to test group
- 0.5 hours: Verify end-to-end flow with test user
- 2 hours: Daily monitoring over 7 days (15 min/day) + final analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, cohorts | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app enrollment prompt | Essential: $29/seat/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated play-specific cost:** Free (within PostHog free tier + existing Intercom seat)

## Drills Referenced

- the certification curriculum design workflow (see instructions below) — design the tier structure, modules, assessments, and scoring rubric
- `lead-capture-surface-setup` — build and deploy the enrollment prompt with tracking
- `threshold-engine` — evaluate pass/fail against enrollment and completion thresholds
