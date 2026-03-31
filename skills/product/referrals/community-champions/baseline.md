---
name: community-champions-baseline
description: >
  Champion Recognition Program — Baseline Run. Launch an automated recognition
  program with tiered perks (Recognized Contributor, Champion), automated
  enrollment from community scoring, and referral link activation. Run always-on
  for 4 weeks and measure referral activation rate.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Social"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=35% of enrolled champions share their referral link within 30 days of enrollment"
kpis: ["Champion enrollment rate", "Referral link activation rate (30-day)", "Referral submission rate", "Recognition message engagement rate"]
slug: "community-champions"
install: "npx gtm-skills add product/referrals/community-champions"
drills:
  - posthog-gtm-events
  - champion-recognition-pipeline
---

# Champion Recognition Program — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Outcomes

A tiered recognition program runs always-on: community members are automatically scored weekly, those crossing score 50 are enrolled as Recognized Contributors with perks (early feature access, contributor badge, community spotlight), and top scorers (75+) are promoted to Champions with enhanced perks and referral links. After 4 weeks, at least 35% of enrolled members have shared their referral link (link shared event, social post, or colleague introduction).

## Leading Indicators

- Champion scoring pipeline runs weekly without errors and produces stable cohort sizes
- Enrollment celebration messages in Intercom have >55% view rate (members are seeing the recognition)
- Welcome email sequence in Loops has >35% open rate (messaging resonates)
- At least 25% of enrolled members click a referral link CTA within 14 days
- At least 3 Recognized Contributors are promoted to Champion within 4 weeks
- Community channel posts celebrating new champions receive positive reactions from other members

## Instructions

### 1. Instrument champion tracking

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the champion program:

- Implement all champion events: `champion_score_computed`, `champion_enrolled`, `champion_tier_promoted`, `champion_referral_link_shared`, `champion_referral_submitted`, `champion_referral_converted`, `champion_perk_activated`
- Set person properties: `champion_recognition_tier`, `champion_enrolled_date`, `champion_score`, `champion_referrals_count`, `champion_questions_answered_30d`
- Build the champion funnel in PostHog: eligible (score>=50) -> enrolled -> referral link shared -> referral submitted -> referral activated
- Create the champion dashboard: enrollment rate trend, referral activation funnel, tier distribution, community channel recognition engagement

### 2. Launch the automated recognition pipeline

Run the `champion-recognition-pipeline` drill to deploy the always-on automation:

- Configure the weekly scoring workflow in n8n: run `champion-identification-scoring` every Sunday, then query Attio for score-50+ members not yet enrolled, filter out ineligible (too new, declined, escalated), auto-enroll in Recognized Contributor tier
- Set up event-driven tier promotion: when `champion_score_computed` crosses 75, immediately trigger Champion promotion
- Deploy tier enrollment automations:
  - Enable PostHog feature flags for tier perks (early feature access, priority support queue)
  - Queue Intercom recognition messages: "Your community contributions are making a difference. You've helped [N] people this month."
  - Add to Loops welcome sequences (Contributor: 3 emails over 2 weeks; Champion: 4 emails over 3 weeks with referral link activation)
  - Post community channel congratulations via Slack/Discord bot
  - Update Attio records with tier, enrollment date, and dimension scores
- Configure the referral activation nudge sequence for Champions:
  - Day 7: Intercom in-app message with referral link and simple CTA
  - Day 14: Loops email with pre-written social posts and shareable invite
  - Day 21: Loops email with alternative angle: "Know someone struggling with [problem]?"
  - Day 30: mark as "Champion but Inactive Referrer" in Attio, pause referral nudges for 60 days
- Set up referral tracking: validate submitted referrals, track the funnel (link shared -> clicked -> signed up -> activated), notify champions at each stage, trigger reward delivery

### 3. Monitor for 4 weeks

Let the pipeline run without intervention for 4 weeks. Monitor the champion dashboard daily:

- Is scoring running? (Weekly `champion_score_computed` event count)
- Are members being enrolled? (Daily new enrollment count)
- Are recognition messages being seen? (Intercom delivery and view rates)
- Are welcome emails being opened? (Loops sequence metrics)
- Are referral links being shared? (PostHog `champion_referral_link_shared` events)
- Are community congratulations posts getting positive reactions? (Slack/Discord reaction counts)

Do not tweak the system during the first 4 weeks. Collect clean baseline data.

### 4. Evaluate against threshold

After 4 weeks, compute:

- **Referral link activation rate**: count of enrolled members who shared their referral link within 30 days of enrollment / total members enrolled in the first 2 weeks (use the first 2 weeks to allow 30-day measurement window)
- **Pass threshold**: >=35%

If PASS: the recognition program activates community champions as referral sources. Proceed to Scalable.
If FAIL (20-34%): the recognition structure is sound but referral activation is slow. Diagnose where members drop off in the nudge sequence. Test different referral asks or timing. Re-run for 2 more weeks.
If HARD FAIL (<20%): the recognition perks may not be compelling enough, or the scoring model is surfacing members who are active in community but not willing to refer. Review the top 20 enrolled members manually and check if they match the Smoke test profile.

## Time Estimate

- 4 hours: PostHog event instrumentation and dashboard setup
- 6 hours: n8n automation pipeline configuration and testing (scoring, enrollment, nudges, referral tracking)
- 4 hours: Intercom and Loops message/sequence creation
- 4 hours: Slack/Discord bot configuration for community celebrations
- 2 hours: 4-week monitoring and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring events, cohorts, feature flags, funnels, dashboard | Free tier: 1M events/mo, 1M flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app recognition messages, enrollment celebrations, referral nudges | Essential: $29/seat/mo billed annually ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Welcome sequences, referral activation emails, reward notifications | Starter: $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Scoring automation, enrollment workflows, referral tracking | Self-hosted: free; Cloud: from $20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Scored member records, tier tracking, pipeline management | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $50-100/mo (Intercom Essential seat + Loops Starter; n8n self-hosted is free)

## Drills Referenced

- `posthog-gtm-events` — instruments all champion events (scoring, enrollment, referral, promotion) and builds the measurement layer
- `champion-recognition-pipeline` — automates scoring, enrollment, tier promotion, perk delivery, referral activation nudges, and referral tracking
