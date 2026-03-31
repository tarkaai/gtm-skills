---
name: empty-state-onboarding-baseline
description: >
  Empty State Guidance — Baseline Run. Expand empty state treatment to all P0 surfaces,
  add an onboarding email sequence that reinforces empty state CTAs, and validate that
  CTR holds at 50%+ with a 20pp lift over control across 50%+ of users.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=50% empty state CTR across all P0 surfaces AND >=20pp lift over control group"
kpis: ["Empty state CTR per surface", "Activation rate (treatment vs control)", "Time to first item created", "Email bridge conversion rate"]
slug: "empty-state-onboarding"
install: "npx gtm-skills add product/onboard/empty-state-onboarding"
drills:
  - empty-state-design
  - onboarding-sequence-design
  - activation-optimization
---

# Empty State Guidance — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

All P0 empty state surfaces have been redesigned and deployed. An onboarding email sequence bridges users who do not convert in-product back to the empty state CTA. A 50/50 feature flag split proves the treatment group achieves 50%+ CTR and a 20 percentage point lift in activation rate over the control group that sees the old empty states.

## Leading Indicators

- Treatment group's `empty_state_cta_clicked` rate is consistently higher than control within the first 3 days
- Users in the treatment group reach `first_item_created` faster (lower median time from signup to first item)
- The onboarding email sequence has >30% open rate and >5% click-through to the empty state deep link
- Session recordings show treatment group users moving through the product with less hesitation

## Instructions

### 1. Expand empty state design to all P0 surfaces

Run the `empty-state-design` drill for every remaining P0 empty state identified in the Smoke audit. For each surface:
1. Design the contextual CTA, templates or sample data, and secondary help link
2. Implement PostHog tracking (`empty_state_viewed`, `empty_state_cta_clicked`, `first_item_created`)
3. Deploy behind the same PostHog feature flag used at Smoke, so all P0 surfaces are treated together

Build a PostHog funnel per surface: `empty_state_viewed` -> `empty_state_cta_clicked` -> `first_item_created`. Save these as "[Surface Name] — Empty State Funnel."

### 2. Build the onboarding email bridge

Run the `onboarding-sequence-design` drill with a focus on empty state reinforcement. Design a 3-email sub-sequence that targets users who viewed P0 empty states but did not create their first item:

**Email 1 (trigger: 24h after `empty_state_viewed` if no `first_item_created`):**
- Subject: "Your [product area] is waiting for you"
- Body: Remind them what the empty state screen will look like once populated. Include a screenshot of a populated version. CTA: deep link directly to the empty state screen.

**Email 2 (trigger: 72h after first view if still no `first_item_created`):**
- Subject: "Most teams start with one of these templates"
- Body: Show the top 3 templates by selection rate from Smoke data. CTA: deep link to the template gallery.

**Email 3 (trigger: Day 5 if still no `first_item_created`):**
- Subject: "Need help getting started?"
- Body: Short message from a real person (founder or CSM) offering to set up a quick call. CTA: Cal.com booking link.

**Skip condition:** All emails skip if `first_item_created` fires at any point.

### 3. Launch the controlled experiment

Set up the PostHog feature flag for a 50/50 split:
- **Treatment group (50%):** Sees the new empty state designs on all P0 surfaces + receives the email bridge sequence
- **Control group (50%):** Sees the original empty state experience (whatever existed before this play) + no email bridge

Run for 14 days minimum. Do not peek at results or adjust the split during this period.

### 4. Optimize activation flow

Run the `activation-optimization` drill to identify the biggest drop-off point between empty state CTA click and activation. Common Baseline findings:

- Users click the CTA but abandon the creation flow halfway through — simplify the form or reduce required fields
- Users create one item but never return — the post-creation experience needs to reinforce the next step
- Users with certain persona types convert at half the rate of others — the CTA copy or templates may not match their use case

Focus optimization effort on the single biggest drop-off point. Do not try to fix everything at once.

### 5. Evaluate against threshold

After 14 days, compute:
- **Empty state CTR (treatment):** `empty_state_cta_clicked / empty_state_viewed` across all P0 surfaces
- **Empty state CTR (control):** same metric for the control group
- **Activation rate (treatment vs control):** percentage of users who reached the activation metric within 14 days
- **Lift:** treatment activation rate minus control activation rate

**Threshold:** CTR >= 50% AND lift >= 20 percentage points

If PASS: Roll out the treatment to 100% of users. Document per-surface CTR and the email bridge conversion rate. Proceed to Scalable.

If FAIL: Identify the weakest P0 surface (lowest CTR) and the weakest email (lowest click-through). Focus iteration there. Re-run for another 14-day cycle.

**Human action required:** Review the experiment results before rolling out to 100%. Confirm the lift is real and not driven by a single outlier surface. Check that the control group was not contaminated (no users switched groups mid-test).

## Time Estimate

- 4 hours: Design and implement remaining P0 empty states
- 3 hours: Build the onboarding email bridge sequence
- 2 hours: Configure the 50/50 feature flag experiment
- 3 hours: Run activation optimization analysis
- 2 hours: Monitor during the 2-week experiment period
- 2 hours: Evaluate results and document

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, session recordings | Free tier: 1M events + 1M feature flag requests/mo. [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Onboarding email bridge sequence | Free up to 1,000 contacts; $49/mo for unlimited sends. [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages for stuck users | Essential: $29/seat/mo (annual). [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated play-specific cost at this level:** $0-78/mo (Loops free tier likely sufficient; Intercom only if using in-app messages beyond basic)

## Drills Referenced

- `empty-state-design` — design and implement P0 empty states with tracking
- `onboarding-sequence-design` — build the 3-email bridge sequence for non-converting users
- `activation-optimization` — identify and fix the biggest drop-off between CTA click and activation
