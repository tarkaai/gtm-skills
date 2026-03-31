---
name: certification-program-baseline
description: >
  Product Certification Program — Baseline Run. Wire the certification into
  always-on automation: Intercom Product Tours for module delivery, Loops sequences
  for enrollment and stall nudges, n8n for badge issuance, and PostHog dashboards
  for continuous measurement. First always-on run targeting 50%+ of activated users.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥25% enrollment, ≥70% completion, ≥90% 30-day retention for certified users"
kpis: ["Enrollment rate", "Completion rate", "Certified 30-day retention", "Module drop-off rate", "Stall recovery rate"]
slug: "certification-program"
install: "npx gtm-skills add product/onboard/certification-program"
drills:
  - certification-delivery-automation
  - posthog-gtm-events
  - onboarding-sequence-design
---

# Product Certification Program — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

The certification program runs continuously without manual intervention. Activated users are automatically prompted, enrolled users receive guided Product Tours, stalled users get nudged, and badge issuance fires on completion. Prove the program sustains enrollment and completion rates over 2 weeks with a larger population.

## Leading Indicators

- Enrollment rate holds ≥25% week-over-week (prompt and email sequence are converting)
- Module completion rate does not decline after Week 1 (content is not a one-time novelty)
- Stall nudges recover ≥30% of stalled users (automation is effective)
- Certified users log in within 7 days post-badge at ≥90% rate (badge is not the end of engagement)

## Instructions

### 1. Establish the certification event taxonomy

Run the `posthog-gtm-events` drill to formalize the event naming:
- All certification events use the `cert_` prefix
- Define standard properties: `tier`, `module`, `assessment_type`, `passed`, `attempts`, `persona`, `cohort`
- Build PostHog funnels: enrollment funnel, per-tier completion funnel, stall detection funnel
- Create PostHog cohorts: "Enrolled not completed," "Stalled >7 days," "Certified," "Certified + retained"

### 2. Build the always-on delivery system

Run the `certification-delivery-automation` drill to wire the full automation:

**Enrollment automation:**
- Intercom banner targeting activated users who have not enrolled
- Loops 3-email enrollment nudge sequence for users who see the banner but do not enroll within 14 days
- PostHog tracking on all enrollment touchpoints

**Module delivery:**
- Intercom Product Tours for each module — guided walkthrough of the skill, ending with "Now try it yourself"
- Contextual in-app messages: start nudges when users enter the relevant product area, completion congratulations after each module
- Loops email per module: "You're X% through — next up: {module name}" for users who complete a module but do not start the next within 48 hours

**Stall detection and recovery:**
- n8n daily workflow: detect users stalled for 7, 14, or 21+ days
- Mild stall (7d): Intercom in-app nudge
- Moderate stall (14d): Loops email with the specific module they need to complete
- Hard stall (21d+): Loops email from a human offering help

**Badge issuance:**
- n8n webhook on `cert_tier_completed`: verify completion, update Attio contact, trigger celebration email via Loops, show in-app modal via Intercom

### 3. Design the certification onboarding sequence

Run the `onboarding-sequence-design` drill adapted for the certification context:
- The "activation" event is `cert_program_enrolled`
- Milestones: enrolled → first module completed → half modules done → all modules done → badge earned
- Build a 5-email behavioral sequence in Loops that guides enrolled users through the certification
- Skip logic: skip nudge emails when milestones are already reached
- Exit condition: badge earned

### 4. Remove the feature flag gate

Expand the certification from the Smoke test group to all activated users:
- Update the PostHog feature flag `cert_program_enabled` to target all users where `activation_reached = true` and `days_since_activation >= 7`
- Monitor the first 48 hours closely: enrollment rate should be within 20% of Smoke results. If dramatically lower, the Smoke cohort may have been unusually engaged — investigate.

### 5. Build the Baseline dashboard

Create a PostHog dashboard with:
- Enrollment funnel: viewed → enrolled → started (weekly trend)
- Completion funnel: started → each module → completed → badge earned
- Stall distribution: count of users in each stall category
- Stall recovery: % of nudged users who resumed within 7 days
- Certified retention: 30-day retention curve for certified vs non-certified users
- Module health: completion rate and avg attempts per module

### 6. Evaluate against threshold after 2 weeks

Measure:
- **Enrollment rate:** ≥25% of prompted users enroll
- **Completion rate:** ≥70% of enrollees earn the badge
- **Certified retention:** ≥90% of certified users are active at Day 30

If PASS: The certification works as an always-on system. Document the delivery architecture and proceed to Scalable.
If FAIL: Diagnose by stage:
- Low enrollment → enrollment prompt or email sequence is weak. Test different copy or timing.
- Low completion → specific module is too hard or too long. Check module-level drop-off.
- Low retention → certification is not teaching the right skills. Review which product actions correlate with retention and realign modules.

## Time Estimate

- 4 hours: Set up event taxonomy and PostHog funnels/cohorts
- 6 hours: Build delivery automation (Intercom tours, Loops sequences, n8n workflows)
- 3 hours: Design and implement the onboarding email sequence
- 2 hours: Expand flag, verify end-to-end, build dashboard
- 3 hours: Monitoring over 2 weeks (15 min/day) + final analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, funnels, cohorts, feature flags, dashboards | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app banners, Product Tours, contextual messages | Essential: $29/seat/mo; Proactive Support add-on: $349/mo for tours — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Enrollment sequence, stall nudges, celebration emails | Starter: $49/mo (up to 5K contacts) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Stall detection, badge issuance automation | Self-hosted: Free; Cloud: from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** Intercom Proactive Support add-on ~$349/mo + Loops ~$49/mo = ~$398/mo (PostHog and n8n on free/standard tiers)

## Drills Referenced

- `certification-delivery-automation` — wire the full certification delivery system (enrollment, tours, stall detection, badge issuance)
- `posthog-gtm-events` — establish the certification event taxonomy and standard funnels
- `onboarding-sequence-design` — design the behavioral email sequence for enrolled users
