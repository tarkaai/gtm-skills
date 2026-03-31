---
name: champion-recognition-pipeline
description: Automate recognition, exclusive access delivery, and referral activation for community champions
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
  - Slack API
fundamentals:
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
  - slack-api-write
---

# Champion Recognition Pipeline

This drill automates the full lifecycle of recognizing community champions and activating them as referral engines: enrollment, recognition delivery, perk activation, referral link provisioning, and ongoing engagement. It runs continuously and scales without proportional manual effort.

## Prerequisites

- Champion identification scoring active and synced to Attio (run `champion-identification-scoring`)
- PostHog feature flags configured for gating champion perks
- n8n instance for automation workflows
- Intercom and Loops configured
- Slack/Discord bot with write access to your community channels

## Steps

### 1. Build the enrollment automation

Using `n8n-scheduling`, create a weekly workflow (runs after champion scoring completes):

1. Query Attio using `attio-lists` for contacts in the "Community Champion Candidates" list (score >= 50) who are NOT yet enrolled in any recognition tier
2. Filter out: users who joined the community less than 30 days ago (too new), users who previously declined enrollment, users with active support escalations
3. For qualifying users, check which tier they qualify for:
   - Score 50-74: enroll in Recognized Contributor automatically
   - Score 75+: flag for Champion invitation (manual review for first cohort; automated after calibration)
4. Set `champion_recognition_tier` on the Attio contact using `attio-contacts`
5. Trigger the appropriate enrollment sequence

Using `n8n-triggers`, create an event-driven workflow: when `champion_score_computed` fires in PostHog and the user's score crosses a tier threshold (50, 75), immediately trigger the enrollment or promotion flow.

### 2. Automate tier enrollment

For each new Recognized Contributor enrollment:
1. Using `posthog-feature-flags`, enable the `champion-contributor-perks` feature flag for the user (grants early feature access, extended trial features, or priority support queue)
2. Using `intercom-in-app-messages`, queue the recognition message (triggered on next login): "Your community contributions are making a difference. You've helped [N] people this month. Welcome to the [Product] Champions program."
3. Using `loops-sequences`, add the user to the Contributor welcome sequence (3 emails over 2 weeks)
4. Using `attio-contacts`, update the contact: set `champion_recognition_tier = contributor`, `champion_enrolled_date = now`, create a note with enrollment details
5. Using `slack-api-write`, post a congratulations message in the community champions channel (or a general announcements channel): "[User] has been recognized as a top contributor this month. Thank you for helping the community!"

For each Champion promotion:
1. Enable `champion-program-perks` feature flag (adds roadmap preview access, direct product team channel, champion badge)
2. Queue the tier promotion celebration in Intercom: "You're one of our most impactful community members. Welcome to the Champion tier."
3. Add to the Champion activation sequence in Loops
4. Generate a unique referral link and attach to the contact in Attio
5. Create an Attio note: "Promoted to Champion. Score: [X]. Helpfulness: [Y]. Users helped: [Z]. Recommended first ask: referral."
6. Using `slack-api-write`, create a dedicated recognition thread in the champion channel with their contribution highlights

### 3. Design and deliver recognition perks

Each tier gets escalating perks:

**Recognized Contributor (score 50-74):**
- Product: early feature access via PostHog feature flag
- Community: contributor badge visible in community channels (configure via Slack/Discord role or custom emoji)
- Communication: monthly contributor digest email highlighting their impact stats
- Reward: small product credit (e.g., 1 month free of paid feature) upon enrollment

**Champion (score 75+):**
- All Contributor perks plus:
- Product: extended trial or free upgrade to next tier, priority support queue
- Community: champion badge, pinned thank-you post, featured in community spotlight
- Communication: quarterly roadmap preview call, direct Slack/Discord channel with product team
- Co-marketing: invitation to guest blog, webinar, or social media collaboration
- Referral: unique referral link with 2x standard reward (referrer and referee both benefit)

### 4. Automate the referral activation for champions

The critical conversion is champion -> active referrer. Using `n8n-scheduling`, create a follow-up workflow that runs 7 days after Champion enrollment:

1. Check if the champion has shared their referral link (event `champion_referral_link_shared` in PostHog)
2. If YES: send a thank-you via `loops-transactional` and update Attio with sharing details
3. If NO: trigger a nudge sequence:
   - Day 7: Intercom in-app message: "Your referral link is ready. Share it and earn [reward] for each person who signs up."
   - Day 14: Loops email with pre-written social media posts and a shareable link the champion can copy-paste
   - Day 21: Loops email with a different angle: "Know someone struggling with [problem]? Here's your personal invite to help them."
   - Day 30: If still no referral activity, mark as "Champion but Inactive Referrer" in Attio. Do not send further referral nudges for 60 days. Continue recognition perks.

### 5. Build the referral tracking layer for champions

Using `n8n-triggers`, listen for `champion_referral_submitted` events:

1. When a referral link is clicked and a new user signs up, validate the referee (not an existing user, not spam)
2. Track the referral in Attio: create a linked record between champion (referrer) and referee
3. Monitor the referral funnel: link shared -> clicked -> signed up -> activated -> retained 30 days
4. At each funnel stage, notify the champion via `loops-transactional`: "Your referral just signed up!" / "Your referral is now active, your reward is on the way!"
5. When the referral reaches the reward threshold (referee activated):
   - Account credits: apply to the champion's account
   - Feature unlock: enable a feature flag via `posthog-feature-flags`
   - Notify the champion and publicly thank them in the community channel (with permission)

### 6. Build the recognition pipeline dashboard

Using PostHog and Attio, create visibility into the pipeline:

- **Recognition funnel**: eligible members -> enrolled contributor -> promoted champion -> active referrer
- **Tier distribution**: count and trend of users in each recognition tier
- **Referral pipeline**: links shared -> clicked -> signed up -> activated -> revenue attributed
- **Champion impact**: aggregate questions answered, users helped, and content created by all champions this month
- **Recognition ROI**: revenue attributed to champion referrals / cost of champion perks
- **Inactive rate**: % of enrolled champions with no referral activity in 60+ days

## Output

- Weekly enrollment automation in n8n
- Event-driven tier promotion workflows
- Recognition perk delivery for 2 tiers
- Referral activation nudge sequence (7/14/21/30 day cadence)
- Referral tracking and reward delivery automation
- Pipeline dashboard with 6 key metrics

## Triggers

Enrollment runs weekly after champion scoring. Promotion is event-driven. Nudge sequences follow their own cadence. All workflows are always-on after initial setup.
