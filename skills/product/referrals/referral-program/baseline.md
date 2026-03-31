---
name: referral-program-baseline
description: >
  Incentivized Referral Program — Baseline Run. Deploy the referral program to all
  eligible users with automated reward fulfillment, lifecycle email triggers, and
  always-on funnel tracking. First always-on automation.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 3 weeks"
outcome: ">=8% referral rate among prompted users AND >=25% referee signup-to-activation conversion"
kpis: ["Referral rate (links shared / users prompted)", "Referee signup rate", "Referee activation rate", "Reward fulfillment rate", "Referral CAC"]
slug: "referral-program"
install: "npx gtm-skills add product/referrals/referral-program"
drills:
  - referral-program
  - feature-announcement
  - activation-optimization
---

# Incentivized Referral Program — Baseline Run

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

>=8% of prompted users share their referral link AND >=25% of referees who sign up reach activation. Reward fulfillment is automated and reliable (>=95% delivery rate). The referral program runs always-on without manual intervention.

## Leading Indicators

- Referral prompt delivery rate >90% (Intercom messages and Loops emails reaching users)
- Referral link share rate trending upward week over week
- Referee signup-to-completed rate >60% (registration flow is not losing referees)
- Reward delivery happening within 24 hours of qualification
- Referred users completing onboarding at similar or better rates than organic signups

## Instructions

### 1. Launch the referral program to all eligible users

Run steps 3-5 of the `referral-program` drill. Expand from the Smoke seed group to all users who meet eligibility criteria:
- Account age >14 days
- At least 3 sessions in the last 30 days
- Not in active churn risk (if health scoring exists)

Using Intercom, deploy always-on referral prompts at moments of delight:
- After completing a successful workflow
- After reaching a usage milestone (10th, 50th, 100th key action)
- After a positive NPS response (9-10)

Using Loops, add a referral CTA to the Day 14 lifecycle email for users who have activated.

### 2. Announce the referral program

Run the `feature-announcement` drill. Create coordinated announcements:
- In-app banner via Intercom visible to all eligible users for 7 days
- Dedicated Loops email to the eligible user base explaining the program, the reward, and how to share
- Changelog entry or blog post with the program details (for SEO and reference)

Track announcement engagement: `referral_announcement_seen`, `referral_announcement_clicked`. Measure how many users generate their referral link within 48 hours of seeing the announcement.

### 3. Automate reward fulfillment

Configure an n8n workflow triggered by `referral_activation_reached` events from PostHog:
1. Verify the referral chain: referrer -> link -> referee -> signup -> activation
2. Apply the reward to the referrer's account (credit, free month, feature unlock)
3. Apply the reward to the referee's account
4. Send a Loops transactional email to the referrer: "[Friend's name] just activated. Your reward: [reward details]. You've referred [count] people so far."
5. Send a Loops transactional email to the referee: "Welcome! Your [reward] is active."
6. Log `referral_reward_issued` to PostHog with reward details and referral chain IDs
7. Update the referrer's record in Attio with referral count and total reward value

**Human action required:** Verify the reward fulfillment workflow is correctly applying credits/features in your billing system. Test end-to-end with a test referral before launching.

### 4. Optimize the referral funnel

Run the `activation-optimization` drill focused on the referral funnel. Analyze the PostHog funnel:

`referral_link_shared` -> `referral_link_clicked` -> `referral_signup_started` -> `referral_signup_completed` -> `referral_activation_reached`

Identify the biggest drop-off point. Common fixes:
- **Shared -> Clicked low:** The share message needs better copy. Test pre-populated share text that explains the value to the referee, not just the reward.
- **Clicked -> Signup low:** The referral landing page is not compelling. Add the referrer's name ("Your colleague [name] invited you") and make the referee benefit prominent.
- **Signup -> Activation low:** Referred users may need a tailored onboarding path. Create a PostHog cohort for referred users and check if their activation rate differs from organic. If lower, add an Intercom product tour specifically for referred signups.

Test 2-3 variations of the highest-friction step over the 3-week evaluation period.

### 5. Evaluate against threshold

Measure after 3 weeks of always-on operation:
- Referral rate: links shared / users who saw a referral prompt. Target: >=8%.
- Referee activation: referees who activated / referees who signed up. Target: >=25%.
- Reward fulfillment: rewards delivered / rewards earned. Must be >=95%.

- **Pass:** Proceed to Scalable. Document the referral rate by prompt type, the best-performing referral surface, and the referral CAC.
- **Fail on referral rate:** The referral ask is not compelling enough or not reaching users at the right moment. Test different incentives, different prompt timing, or different eligible user criteria.
- **Fail on activation:** The referee experience is weak. Focus on referral-specific onboarding before scaling volume.

## Time Estimate

- 4 hours: expand referral program to all eligible users, configure always-on prompts
- 3 hours: build announcement campaign across Intercom, Loops, and changelog
- 4 hours: build and test automated reward fulfillment workflow in n8n
- 3 hours: analyze referral funnel, identify drop-off, design and deploy tests
- 2 hours: threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Referral funnel tracking, cohort analysis, feature flags | Free up to 1M events/mo; $0.00005/event after ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app referral prompts, announcement banner, product tours | From $29/seat/mo; Proactive Support add-on $349/mo for outbound messaging ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle email referral CTAs, reward notification emails | From $49/mo for up to 5,000 contacts; transactional email free on paid plans ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Reward fulfillment automation workflow | From EUR 24/mo Starter; free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Attio | Referrer records, referral count tracking | Free up to 3 users; $29/user/mo Plus ([attio.com](https://attio.com)) |

**Estimated play-specific cost at this level:** $49-100/mo (Loops paid plan + n8n Starter; Intercom and PostHog likely covered by existing stack spend)

## Drills Referenced

- `referral-program` -- expands referral program to all eligible users, configures always-on prompts, automates reward fulfillment
- `feature-announcement` -- coordinates the referral program launch announcement across in-app, email, and changelog
- `activation-optimization` -- identifies and fixes the biggest drop-off point in the referral funnel
