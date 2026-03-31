---
name: advocacy-program-design
description: Design a tiered power user advocacy program with recognition, exclusive access, and reward mechanics that drive referrals
category: Advocacy
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - intercom-in-app-messages
  - intercom-checklists
  - loops-sequences
  - attio-lists
  - attio-custom-attributes
---

# Advocacy Program Design

This drill produces the complete specification for a power user advocacy program: tier structure, recognition mechanics, exclusive access perks, referral integration, and the full event schema. The output is a document an agent or engineer can implement directly.

## Prerequisites

- Power user scoring active (run `power-user-scoring` first)
- PostHog with cohort data showing Champion, Power User, and Rising Star tiers
- Attio with scored users synced
- Product team aligned on what exclusive access or perks are feasible

## Steps

### 1. Define the advocacy tier structure

Map program tiers to the power user score tiers. Each tier gets escalating benefits and asks:

**Tier 1 — Insider (Power Users, score 60-79)**
- Benefits: early feature access via PostHog feature flags, monthly product insider email, badge on profile
- Asks: opt-in to testimonial request list, accept occasional survey invitations
- Entry: automatic enrollment when score crosses 60 (with opt-out)

**Tier 2 — Advocate (Champions, score 80-89)**
- Benefits: all Insider perks + quarterly roadmap preview call, dedicated Slack/Discord channel, advocate badge visible to other users
- Asks: provide a written testimonial or short video review, refer 1 qualified lead per quarter, participate in case study interview
- Entry: invitation-only from Insider tier based on engagement with Insider program

**Tier 3 — Ambassador (Champions, score 90+, sustained 3 months)**
- Benefits: all Advocate perks + annual advisory board seat, co-marketing opportunity (guest blog, webinar, podcast), free plan upgrade or credit, direct line to product leadership
- Asks: speak at an event or webinar once per year, provide ongoing referrals, serve as reference customer for sales
- Entry: nomination by account team, requires 3-month sustained Champion score

### 2. Design the recognition system

Using `posthog-custom-events`, define events for advocacy actions:

```javascript
posthog.capture('advocacy_tier_enrolled', {
  tier: 'insider',
  power_user_score: 72,
  enrollment_type: 'automatic'
});

posthog.capture('advocacy_action_completed', {
  action_type: 'testimonial_submitted',
  tier: 'advocate',
  reward_issued: 'feature_credit_50'
});

posthog.capture('advocacy_referral_submitted', {
  referrer_tier: 'advocate',
  referee_email_domain: 'company.com',
  referral_source: 'advocacy_program'
});

posthog.capture('advocacy_tier_promoted', {
  from_tier: 'insider',
  to_tier: 'advocate',
  months_in_previous_tier: 2
});
```

### 3. Build the in-product recognition layer

Using `intercom-in-app-messages`, create recognition touchpoints:

- **Enrollment celebration**: when a user qualifies for Insider, show an in-app message: "You're one of our top users. Welcome to the [Product] Insider program." Include what they get and a CTA to view their perks.
- **Tier promotion**: when moving from Insider to Advocate, show a celebration modal with the new benefits and a clear ask (testimonial CTA).
- **Milestone recognition**: when an advocate completes their first referral or testimonial, in-app thank you with a reward notification.
- **Community visibility**: badge or icon next to the user's name in any collaborative features. Other users should see that this person is a recognized advocate.

### 4. Design the advocacy communication sequences

Using `loops-sequences`, build automated email sequences for each tier:

**Insider welcome sequence (3 emails over 2 weeks):**
1. Welcome + perks summary + link to early access features
2. How the program works + first ask (quick survey about favorite feature)
3. Spotlight: "Meet other Insiders" + community channel invitation

**Advocate activation sequence (4 emails over 3 weeks):**
1. Congratulations on promotion + new benefits + testimonial request CTA
2. Referral program introduction with unique referral link
3. Case study invitation (short form: 3 questions about their experience)
4. Reminder of upcoming roadmap preview call with calendar link

**Ambassador onboarding sequence (2 emails + 1 personal):**
1. Personal congratulations from product leadership (template, but personalized with specific usage data)
2. Advisory board details + annual event calendar
3. **Human action required:** Account team sends a personal video or schedules a 1:1 call

### 5. Integrate with the referral mechanism

Link the advocacy program to the existing referral infrastructure. Each tier gets a unique referral link with tracking:

Using `attio-lists`, maintain a "Active Advocacy Referrers" list. Track:
- Referrals submitted per advocate per quarter
- Referral conversion rate (referred -> signed up -> activated)
- Revenue attributed to advocacy referrals

Reward structure:
- Insider: standard referral reward (if referral program exists)
- Advocate: 2x referral reward + recognition in community channel
- Ambassador: 3x referral reward + co-marketing credit

### 6. Document the specification

Produce a structured specification:
- Complete tier definitions (entry criteria, benefits, asks, escalation path)
- Event schema for PostHog instrumentation
- In-app message templates with copy and trigger conditions
- Email sequence outlines with send timing
- Referral reward structure per tier
- Metric targets: Insider enrollment rate, Insider-to-Advocate conversion, testimonials per quarter, referrals per advocate per quarter

## Output

- Advocacy program specification document
- PostHog event schema for all advocacy actions
- 3 tier definitions with benefits, asks, and entry criteria
- In-app recognition message templates
- Email sequence designs for each tier
- Referral integration plan

## Triggers

Run this drill once at play setup. Re-run when adding new tiers, changing benefits, or when advocacy metrics indicate the program structure needs redesign.
