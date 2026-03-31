---
name: usage-milestones-baseline
description: >
  Usage Milestone Celebrations — Baseline Run. Expand celebrations to all milestone tiers, add email
  follow-ups via Loops, run a controlled A/B test (celebrated vs. uncelebrated cohort), and prove
  that celebrations produce at least 10 percentage points of retention lift at 14 days.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥70% celebration impression rate AND ≥10pp 14-day retention lift vs. control"
kpis: ["Celebration impression rate", "Celebration engagement rate", "14-day retention lift", "CTA conversion rate"]
slug: "usage-milestones"
install: "npx gtm-skills add product/retain/usage-milestones"
drills:
  - usage-milestone-rewards
  - posthog-gtm-events
  - feature-adoption-monitor
  - threshold-engine
---

# Usage Milestone Celebrations — Baseline Run

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Celebrations are live across all milestone tiers with both in-app and email channels. A controlled experiment proves that users who receive milestone celebrations retain at 10+ percentage points higher than users who do not, measured at 14 days post-milestone.

## Leading Indicators

- Celebration engagement rate (click/interact) above 25% across all tiers
- Email follow-up open rate above 40%
- Users in the celebrated cohort log more sessions in the 7 days after a milestone than the control cohort
- CTA conversion (referral ask, next-feature link, upgrade prompt) above 5%

## Instructions

### 1. Expand event tracking to all tiers

Run the `posthog-gtm-events` drill to add tracking for every milestone tier defined in Smoke. For each tier, ensure these events fire:

- `milestone_reached` — with `milestone_tier`, `milestone_name`, `cumulative_count`, `days_since_signup`
- `celebration_shown` — with `milestone_tier`, `celebration_type`, `channel` (in-app or email)
- `celebration_engaged` — with `milestone_tier`, `cta_type`, `channel`
- `celebration_cta_clicked` — with `milestone_tier`, `cta_type`, `destination_url`
- `celebration_dismissed` — with `milestone_tier`, `channel`, `seconds_visible`

Build PostHog funnels: `milestone_reached` -> `celebration_shown` -> `celebration_engaged` -> `celebration_cta_clicked`. Break down by `milestone_tier`.

### 2. Build celebrations for all tiers

Run the `usage-milestone-rewards` drill, Steps 3-5. Create tier-appropriate celebrations:

**Early tiers (1-10 actions):** In-app message only. Confetti animation or badge. CTA: suggest the next feature. Copy under 40 words. Tone: encouraging, lightweight.

**Mid tiers (50-100 actions):** In-app message PLUS a follow-up email via Loops 2 hours later. The email includes a usage summary: "You have completed X actions, created Y projects, and spent Z hours in the product this month." CTA: referral ask or review request. Use the `loops-transactional` fundamental to build the email template with variables `{{firstName}}`, `{{milestoneCount}}`, `{{usageSummary}}`, `{{ctaUrl}}`.

**Advanced tiers (500+ actions):** In-app message PLUS email PLUS personal note from the team. The email offers exclusive access: beta features, customer advisory board invitation, or a branded community badge. CTA: case study participation or upgrade.

### 3. Set up the controlled experiment

Using PostHog feature flags, create an experiment:
- **Treatment group (50%):** receives all milestone celebrations (in-app + email)
- **Control group (50%):** milestones are tracked in PostHog but no celebration message is shown and no email is sent

Run the `feature-adoption-monitor` drill to track how celebration exposure affects feature discovery. Users who celebrate milestones may explore more features — this is the retention mechanism.

Ensure the experiment runs for the full 2 weeks with at least 100 users per group reaching at least one milestone.

### 4. Attach strategic CTAs per tier

Run the `usage-milestone-rewards` drill, Step 4. For each tier, configure a specific CTA:

| Milestone Tier | CTA | Tracking Event |
|---------------|-----|----------------|
| Tier 1 (first action) | "Try [next feature]" deep link | `celebration_cta_clicked` with `cta_type=feature_discovery` |
| Tier 2 (10 actions) | "Invite a teammate" link | `celebration_cta_clicked` with `cta_type=team_invite` |
| Tier 3 (50 actions) | "Share your experience" referral link | `celebration_cta_clicked` with `cta_type=referral` |
| Tier 4 (100 actions) | "Leave a review on [platform]" | `celebration_cta_clicked` with `cta_type=review` |
| Tier 5 (500+ actions) | "Upgrade to unlock [feature]" | `celebration_cta_clicked` with `cta_type=upgrade` |

### 5. Evaluate against threshold

After 2 weeks, run the `threshold-engine` drill. Measure:

- **Primary metric 1:** Celebration impression rate across all tiers. Target: >=70%.
- **Primary metric 2:** 14-day retention rate for treatment group minus control group. Target: >=10 percentage points.
- **Secondary:** Engagement rate by tier, CTA conversion rate by tier, email open rate for mid/advanced tiers.

### 6. Pass/fail decision

**PASS** if both: impression rate >=70% AND retention lift >=10pp. Proceed to Scalable.

**FAIL scenarios and fixes:**
- Impression rate low but retention lift high: celebration delivery pipeline has gaps. Check Intercom targeting and Loops email triggers.
- Impression rate high but retention lift low: celebrations are seen but not moving behavior. Revise copy, timing, or CTA relevance.
- Both low: fundamental issue with milestone selection. Reassess whether the milestones represent meaningful user progress.

## Time Estimate

- 3 hours: expand event tracking and build funnels
- 5 hours: build celebrations for all tiers (in-app + email)
- 2 hours: configure experiment and feature flags
- 2 hours: implement CTA pipeline per tier
- 4 hours: analyze results, compare cohorts, generate report

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, funnels, feature flags, experiments | Free tier: 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app celebrations across tiers | Starter: $74/mo — https://www.intercom.com/pricing |
| Loops | Milestone follow-up emails | Free tier: 1,000 contacts — https://loops.so/pricing |

## Drills Referenced

- `usage-milestone-rewards` — builds celebrations for all tiers with strategic CTAs and the in-app + email notification pipeline
- `posthog-gtm-events` — configures the full event taxonomy for milestone tracking across all tiers
- `feature-adoption-monitor` — measures whether celebrations drive deeper feature discovery
- `threshold-engine` — evaluates the 70% impression rate and 10pp retention lift thresholds
