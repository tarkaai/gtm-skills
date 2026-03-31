---
name: quick-start-guide-smoke
description: >
  Quick Start Guide — Smoke Test. Build a concise, scannable quick-start guide for new users,
  deploy it in-app and via email, and validate that at least 40% of new signups view the guide
  within 3 days and at least 25% complete all steps within 7 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥ 40% guide view rate within 3 days and ≥ 25% guide completion rate within 7 days from ≥ 20 new signups"
kpis: ["Guide view rate (target ≥ 40% within 3 days)", "Guide completion rate (target ≥ 25% within 7 days)", "Post-guide activation rate"]
slug: "quick-start-guide"
install: "npx gtm-skills add product/onboard/quick-start-guide"
drills:
  - onboarding-sequence-design
  - threshold-engine
---

# Quick Start Guide — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

Prove that a concise, structured quick-start guide reduces onboarding friction and drives new users toward the product's activation metric. The guide must be scannable (under 5 minutes to read), action-oriented (every section ends with a specific user action), and accessible on at least two surfaces (in-app and email).

Pass: ≥ 40% of ≥ 20 new signups view the guide within 3 days, AND ≥ 25% complete all guide steps within 7 days.
Fail: < 40% view rate after 20+ signups, or < 25% completion rate, or fewer than 20 signups in the test window.

## Leading Indicators

- First user completes the full guide within 24 hours of deployment (the steps are clear and achievable)
- Per-step drop-off is < 30% between any two consecutive steps (no single step blocks users)
- At least 2 users who complete the guide reach the activation metric without contacting support (the guide is self-serve)
- Email version of the guide has an open rate > 35% (the subject line and timing work)
- At least 1 user clicks the "Was this helpful? Yes" feedback button (the feedback loop works)

## Instructions

### 1. Define the activation milestones

Run the `onboarding-sequence-design` drill. This produces:

- **The activation metric:** the single action that best predicts 30-day retention. Use PostHog cohort analysis (`posthog-cohorts` fundamental) to compare retained vs churned users. If you lack data, pick the action that delivers the core value promise.
- **The milestone ladder:** 3-5 intermediate steps from signup to activation. Each step must be trackable as a PostHog event, achievable in a single session, and on the critical path to activation.
- **The email sequence spec:** content, timing, and branching logic for the onboarding emails (the guide will be delivered as Email 2 in this sequence).

Document the milestones. These become the guide's sections.

### 2. Build and deploy the quick-start guide

Run the the quick start content pipeline workflow (see instructions below) drill. This produces:

- **Guide content:** 3-5 sections mapping to the milestone ladder. Each section has a clear action verb title, numbered steps referencing specific UI elements, expected time, and a confirmation statement. Total guide time under 5 minutes.
- **In-app deployment:** Guide published as an Intercom Help Center article in the "Getting Started" collection, pinned to the Messenger home screen. A targeted in-app message surfaces the guide to new users on their first session.
- **Email deployment:** Guide content included inline in the onboarding email sequence (Email 2, sent 24 hours after signup if the user has not reached Milestone 2). Each step links directly into the product at the relevant screen.
- **Web deployment:** Guide published as a standalone web page at `/quick-start` or `/docs/quick-start`.
- **Tracking:** PostHog events for `guide_viewed`, `guide_step_completed`, `guide_completed`, `guide_abandoned`, and `guide_feedback` across all surfaces.

**Human action required:** Review the guide content before launching. Verify every step instruction matches the current product UI. Verify screenshots are accurate. Deploy to a test group of 20-50 new signups.

### 3. Monitor guide engagement

Track these metrics in PostHog over 7 days:

| Metric | How to measure | Target |
|--------|---------------|--------|
| Guide view rate | `guide_viewed` / total new signups within 3 days | ≥ 40% |
| Guide completion rate | `guide_completed` / total new signups within 7 days | ≥ 25% |
| Per-step completion | `guide_step_completed` count per step | < 30% drop-off between steps |
| Post-guide activation | Users who completed guide AND reached activation metric | Higher than non-guide users |
| Surface breakdown | `guide_viewed` broken down by `surface` property | Identify which surface drives most views |

Log all data in PostHog. Check daily for the first 3 days, then at day 7.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass threshold.

- **PASS (≥ 40% view rate AND ≥ 25% completion rate from ≥ 20 users):** The guide works. Document: which surface drove the most views, which step had highest/lowest completion, median time-to-guide-completion, and post-guide activation rate vs users who did not view the guide. Proceed to Baseline.
- **MARGINAL (30-39% view rate OR 15-24% completion rate):** Identify the bottleneck. If low view rate: the in-app message is not visible enough or the email subject line needs work. If low completion rate: find the step with the largest drop-off and simplify it. Re-run with 20 fresh signups.
- **FAIL (< 30% view rate OR < 15% completion rate):** Diagnose: Did users see the in-app message (check `guide_viewed` events by surface)? Did they start but abandon (check `guide_abandoned` with `last_step_completed`)? Is the guide too long? Fix the root cause and re-test.

## Time Estimate

- Milestone definition and email sequence design: 1.5 hours
- Guide content creation, in-app and email deployment: 2 hours
- PostHog event instrumentation: 30 minutes
- Monitoring over 7 days and evaluation: 1 hour
- Total: ~5 hours of active work over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, guide completion measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Help Center article, in-app message to surface guide | Essential $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Onboarding email sequence with inline guide | Free under 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Smoke:** $29 (Intercom Essential, 1 seat). PostHog and Loops on free tiers.

## Drills Referenced

- the quick start content pipeline workflow (see instructions below) -- build the guide content (3-5 sections, under 5 minutes), deploy on 3 surfaces (Intercom, email, web), and instrument PostHog tracking for views, step completions, abandonment, and feedback
- `onboarding-sequence-design` -- map activation milestones, write the behavioral email sequence, define timing and branching logic (the guide maps to these milestones)
- `threshold-engine` -- evaluate guide view rate and completion rate against pass thresholds and recommend next action
