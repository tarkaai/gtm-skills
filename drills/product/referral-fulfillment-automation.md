---
name: referral-fulfillment-automation
description: Automate the referral reward lifecycle from link generation through reward delivery and tracking
category: Product
tools:
  - PostHog
  - Loops
  - Intercom
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - loops-transactional
  - loops-sequences
  - intercom-in-app-messages
  - n8n-triggers
  - n8n-workflow-basics
  - attio-lists
---

# Referral Fulfillment Automation

This drill automates the full referral reward lifecycle: generating unique referral links per user, tracking every stage of the referral funnel, delivering rewards when criteria are met, and notifying both referrer and referee at each milestone. The goal is zero manual fulfillment once a referral is in flight.

## Prerequisites

- Referral program designed (incentive structure, eligibility rules, reward type) from the `referral-program` drill
- PostHog tracking referral events
- Loops configured for transactional email
- Intercom configured for in-app messages
- n8n instance for orchestration
- Ability to generate unique referral links or codes per user (via your product backend or a link shortener API)

## Steps

### 1. Generate and distribute unique referral links

Each eligible user gets a unique referral link. The link format encodes the referrer's user ID: `https://yourproduct.com/r/{referrer_code}`.

Using `n8n-workflow-basics`, build a workflow that:

1. Queries PostHog or Attio for users eligible to refer (active, past the activation milestone, positive engagement)
2. Calls your product API to generate a referral code for each eligible user (or creates one via a deterministic hash of user ID)
3. Stores the referral code in Attio using `attio-lists` as a custom attribute on the contact record
4. Triggers the initial referral invitation via both channels (step 2 below)

Track link generation in PostHog:

```javascript
posthog.capture('referral_link_generated', {
  referrer_id: 'user_123',
  referral_code: 'abc789',
  incentive_type: 'two_sided',
  referrer_reward: 'free_month',
  referee_reward: 'free_month'
});
```

### 2. Deliver the referral prompt at moments of delight

Using `intercom-in-app-messages`, trigger the referral ask when users hit moments of delight:

- After completing a key workflow successfully
- After an NPS response of 9 or 10
- After reaching a usage milestone (e.g., 100th action, 30-day streak)
- After inviting a team member (collaboration signal)

Message template:
- Title: "Know someone who'd love this?"
- Body: "Share your link and you both get {reward}."
- CTA: Copy referral link to clipboard
- Display: show once per trigger event, maximum once per week

Using `loops-sequences`, enroll promoters in a 3-email referral reminder sequence:

- Email 1 (day 0): "You've been doing great work in [product]. Share the love and earn {reward}." Include referral link.
- Email 2 (day 7): "Your referral link is ready. {X} users like you have already referred friends this month."
- Email 3 (day 21): "Last reminder: your referral link earns you {reward} for each friend who joins."

### 3. Track the referral funnel

Using `posthog-custom-events`, instrument every stage:

```javascript
// Referrer shares their link
posthog.capture('referral_link_shared', {
  referrer_id: 'user_123',
  share_channel: 'email' // or 'social', 'copy', 'dm'
});

// Referee clicks the referral link
posthog.capture('referral_link_clicked', {
  referrer_id: 'user_123',
  referee_session_id: 'sess_456'
});

// Referee signs up
posthog.capture('referral_signup', {
  referrer_id: 'user_123',
  referee_id: 'user_789',
  signup_method: 'email'
});

// Referee activates (hits the product activation milestone)
posthog.capture('referral_activated', {
  referrer_id: 'user_123',
  referee_id: 'user_789',
  days_to_activate: 3
});

// Reward issued
posthog.capture('referral_reward_issued', {
  referrer_id: 'user_123',
  referee_id: 'user_789',
  reward_type: 'free_month',
  reward_value_usd: 29
});
```

Using `posthog-funnels`, build the referral conversion funnel: link_generated -> link_shared -> link_clicked -> referral_signup -> referral_activated -> reward_issued. This funnel is the core measurement artifact for the play.

### 4. Automate reward fulfillment

Using `n8n-triggers`, build a workflow triggered by the `referral_activated` event:

1. Verify the referral is valid: referee is a new user, not a duplicate account, not self-referral
2. Apply the reward to the referrer's account via your product API (credit, free month, feature unlock)
3. Apply the reward to the referee's account if two-sided
4. Update Attio: increment the referrer's `referral_count` attribute, add the referee to the "Referred Users" list
5. Fire the `referral_reward_issued` PostHog event
6. Trigger reward notifications (step 5)

Fraud prevention rules:
- Same email domain for referrer and referee: flag for manual review (may be valid for different companies, but check)
- Referee account created but never activated: do not issue reward (require activation)
- More than 10 referrals in 24 hours from one user: pause and review
- Referee signed up then immediately churned within 7 days: claw back reward if possible

### 5. Send reward notifications

Using `loops-transactional`, send notifications at each stage:

**To referrer when referee signs up:**
- Subject: "{referee_name} just joined using your link"
- Body: "{referee_name} signed up. Once they activate their account, you'll both get {reward}."

**To referrer when reward is issued:**
- Subject: "You earned {reward}!"
- Body: "Thanks for referring {referee_name}. Your {reward} has been applied to your account. You've referred {total_referrals} people so far."
- CTA: "Refer another friend" with referral link

**To referee on signup:**
- Subject: "Welcome! {referrer_name} thought you'd love this"
- Body: "Your friend {referrer_name} referred you. Complete your setup to unlock your {reward}."
- CTA: "Get started"

### 6. Build the referral leaderboard data

Using `n8n-workflow-basics`, create a weekly workflow that:

1. Queries Attio for all users with referral_count > 0
2. Ranks them by referral count
3. Updates a "Top Referrers" list in Attio with the top 20
4. Fires a PostHog event for the leaderboard snapshot:

```javascript
posthog.capture('referral_leaderboard_updated', {
  top_referrer_id: 'user_123',
  top_referrer_count: 14,
  total_active_referrers: 87,
  total_referrals_this_month: 203
});
```

The leaderboard data feeds into gamification (if using tiered rewards) and into the `referral-health-monitor` drill at Durable level.

## Output

- Unique referral link generation and distribution pipeline
- Multi-channel referral prompts (Intercom in-app + Loops email sequence)
- Full referral funnel instrumented in PostHog with 6 stages
- Automated reward fulfillment with fraud prevention
- Transactional notifications at each referral milestone
- Weekly leaderboard data aggregation

## Triggers

The n8n reward fulfillment workflow runs continuously, triggered by PostHog events via webhook. The email sequence enrolls users at referral program entry. Leaderboard aggregation runs weekly. Re-run the full drill setup when changing the incentive structure or adding new reward types.
