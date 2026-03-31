---
name: advocacy-activation-pipeline
description: Automate recruitment, onboarding, and activation of power users into advocacy actions at scale
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-feature-flags
  - n8n-scheduling
  - n8n-triggers
  - n8n-workflow-basics
  - intercom-in-app-messages
  - loops-sequences
  - loops-transactional
  - attio-lists
  - attio-contacts
  - attio-automation
---

# Advocacy Activation Pipeline

This drill automates the full lifecycle of converting scored power users into active advocates: recruitment, onboarding into the program, activation of their first advocacy action, and ongoing engagement. It runs continuously and scales without proportional manual effort.

## Prerequisites

- Power user scoring active and synced to Attio (run `power-user-scoring`)
- Advocacy program designed with tier structure (run `advocacy-program-design`)
- PostHog feature flags configured for gating advocacy perks
- n8n instance for automation workflows
- Intercom and Loops configured

## Steps

### 1. Build the recruitment automation

Using `n8n-scheduling`, create a daily workflow:

1. Query Attio using `attio-lists` for contacts in the "Power User Candidates" list (score >= 60) who are NOT yet in any advocacy tier
2. Filter out: users created less than 30 days ago (too new), users who previously declined enrollment, users with open support tickets (bad timing)
3. For qualifying users, check which tier they qualify for:
   - Score 60-79: enroll in Insider automatically
   - Score 80+: flag for Advocate invitation (requires manual review for first cohort; automated after calibration)
4. Set `advocacy_tier` on the Attio contact using `attio-contacts`
5. Trigger the appropriate enrollment sequence

Using `n8n-triggers`, also create an event-driven workflow: when `power_user_score_computed` fires in PostHog and the user's score crosses a tier threshold (60, 80, 90), immediately trigger the enrollment or promotion flow without waiting for the daily cron.

### 2. Automate tier enrollment

For each new Insider enrollment:
1. Using `posthog-feature-flags`, enable the `advocacy-insider-perks` feature flag for the user (grants early feature access)
2. Using `intercom-in-app-messages`, queue the enrollment celebration message (triggered on next login)
3. Using `loops-sequences`, add the user to the Insider welcome sequence
4. Using `attio-contacts`, update the contact: set `advocacy_tier = insider`, `advocacy_enrolled_date = now`, create a note with the enrollment details

For each Advocate promotion:
1. Enable `advocacy-advocate-perks` feature flag
2. Queue the tier promotion celebration in Intercom
3. Add to the Advocate activation sequence in Loops
4. Generate a unique referral link and attach to the contact in Attio
5. Create an Attio note: "Promoted to Advocate. Score: X. Recommended ask: [testimonial/case study/referral]."

### 3. Automate first advocacy action

The critical metric is time-to-first-advocacy-action: how quickly a new program member completes their first ask.

Using `n8n-scheduling`, create a follow-up workflow that runs 7 days after enrollment:

1. Check if the user has completed any advocacy action (event `advocacy_action_completed` in PostHog)
2. If YES: send a thank-you via `loops-transactional` and update Attio with the action details
3. If NO: trigger a nudge sequence:
   - Day 7: Intercom in-app message with the easiest ask (e.g., "Share what you love about [Product] in one sentence")
   - Day 14: Loops email with a specific testimonial template pre-filled with their usage data
   - Day 21: Final nudge with a different ask (e.g., referral link instead of testimonial)
   - Day 30: If still no action, mark as "Enrolled but Inactive" in Attio. Do not send further nudges for 60 days.

### 4. Build the re-engagement loop for inactive advocates

Using `n8n-scheduling`, create a monthly workflow for advocates who completed one action but have been inactive for 60+ days:

1. Query Attio for advocates where `last_advocacy_action_date` is 60+ days ago
2. Check PostHog: is the user still actively using the product? (If product usage also dropped, this is a churn risk, not an advocacy problem — route to churn prevention instead.)
3. For active-but-advocacy-inactive users, send a re-engagement email via `loops-transactional` with a new, contextual ask based on their recent product usage: "You've been building amazing [feature X] workflows. Would you share your setup with other users?"
4. If no response after 2 attempts, reduce cadence to quarterly check-ins

### 5. Automate referral tracking and reward delivery

Using `n8n-triggers`, listen for `advocacy_referral_submitted` events:

1. When a referral is submitted, validate the referee email (not an existing user, not a known spam domain)
2. Track the referral in Attio: create a linked record between referrer and referee
3. Monitor the referral funnel: submitted -> signed up -> activated -> retained 30 days
4. At each funnel stage, notify the referrer via `loops-transactional`: "Your referral just signed up!" / "Your referral is now active — your reward is on the way!"
5. When the referral reaches the reward threshold (e.g., referee activated), trigger reward delivery:
   - Account credits: update the user's account via your billing system
   - Feature unlock: enable a feature flag via `posthog-feature-flags`
   - Physical reward: create a fulfillment task in Attio

### 6. Build the pipeline dashboard

Using PostHog and Attio, create visibility into the pipeline:

- **Recruitment funnel**: eligible users -> enrolled -> first action completed -> active advocate
- **Tier distribution**: count and trend of users in each advocacy tier
- **Activation rate**: % of enrolled users who complete first action within 30 days (target: 40%+)
- **Advocacy velocity**: actions completed per advocate per quarter (target: 2+)
- **Referral pipeline**: referrals submitted -> signed up -> activated -> revenue attributed
- **Inactive rate**: % of enrolled advocates with no action in 60+ days

## Output

- Daily recruitment automation in n8n
- Event-driven tier enrollment and promotion workflows
- First-action nudge sequence (7/14/21/30 day cadence)
- Re-engagement loop for inactive advocates
- Referral tracking and reward delivery automation
- Pipeline dashboard with 6 key metrics

## Triggers

Recruitment runs daily. Enrollment is event-driven. Nudge sequences follow their own cadence. Re-engagement runs monthly. All workflows are always-on after initial setup.
