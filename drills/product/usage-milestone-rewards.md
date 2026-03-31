---
name: usage-milestone-rewards
description: Celebrate user achievements at key usage milestones to drive engagement and retention
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
fundamentals:
  - posthog-custom-events
  - intercom-in-app-messages
  - loops-transactional
---

# Usage Milestone Rewards

This drill sets up a system that recognizes and celebrates users when they hit meaningful usage milestones. Milestone rewards reinforce positive behavior, increase product stickiness, and create natural moments to ask for referrals or upgrades.

## Prerequisites

- PostHog tracking core usage events with cumulative counts
- Intercom configured for in-app messages
- Loops configured for triggered emails
- Defined list of meaningful usage milestones for your product

## Steps

### 1. Define your milestone ladder

Map out milestones that represent increasing investment in your product. Good milestones are:

- **Achievable early**: First milestone within the first session (e.g., "First project created")
- **Progressively harder**: Each step requires more engagement (10 projects, 50 projects, 100 projects)
- **Meaningful to the user**: Tied to outcomes they care about, not vanity metrics
- **Spaced for motivation**: Not too close (feels trivial) or too far apart (feels unreachable)

Example ladder: First action completed, 10 actions, 50 actions, 100 actions, 500 actions, 1000 actions. For team products: first teammate invited, 5 team members, team completed 100 actions together.

### 2. Instrument milestone detection

Using `posthog-custom-events`, set up events that fire when a user crosses each milestone threshold. Use PostHog's person properties to store cumulative counts and flag which milestones have been reached. Ensure each milestone fires only once per user.

### 3. Design milestone celebrations

Create a celebration for each milestone tier:

- **Early milestones (1-10)**: In-app confetti or badge using `intercom-in-app-messages`. Keep it light and fun. "You just created your 10th project — you're on a roll!"
- **Mid milestones (50-100)**: In-app celebration plus an email from `loops-transactional` with a usage summary. "You've processed 100 workflows this month — here's what you've accomplished."
- **Advanced milestones (500+)**: Personal congratulations from a team member. Offer exclusive access to beta features or a community badge. These users are your champions.

### 4. Attach strategic CTAs to milestones

Each milestone is a moment of positive sentiment — use it wisely:

- **Early milestones**: Suggest the next feature to try. Guide them deeper into the product.
- **Mid milestones**: Ask for a referral or a review. "You've clearly found value — know someone who would too?"
- **Advanced milestones**: Prompt an upgrade if on a lower plan. Invite to a customer advisory board or case study.

Never make the CTA overshadow the celebration. The primary message is congratulations; the CTA is secondary.

### 5. Build the notification pipeline

Using `intercom-in-app-messages` for real-time celebrations and `loops-transactional` for follow-up summaries, create a coordinated notification flow. The in-app message fires instantly when the milestone is reached. The email arrives 1-2 hours later with a recap and the CTA. Both should feel personal, not automated.

### 6. Measure impact on retention

Track whether users who receive milestone celebrations retain at higher rates than those who do not. Use PostHog to compare cohorts. Also track: CTA conversion rates at each milestone, referral rates from milestone prompts, and upgrade rates from advanced milestone prompts. Adjust the milestone ladder based on which thresholds produce the most engagement.
