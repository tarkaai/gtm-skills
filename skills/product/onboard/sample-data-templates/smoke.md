---
name: sample-data-templates-smoke
description: >
  Sample Data Acceleration — Smoke Test. Build a minimal sample data package for one persona,
  inject it into 10-50 test accounts, and measure whether pre-populated accounts increase
  interaction rate compared to empty-state accounts.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥70% of seeded users interact with at least 1 sample record within 48 hours"
kpis: ["Sample data interaction rate", "Time to first action", "Activation rate (seeded vs. control)"]
slug: "sample-data-templates"
install: "npx gtm-skills add product/onboard/sample-data-templates"
drills:
  - onboarding-flow
  - threshold-engine
---

# Sample Data Acceleration — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Success at Smoke means: pre-populated accounts produce measurably higher interaction rates than empty accounts. At least 70% of users who receive sample data interact with at least one sample record within 48 hours of signup.

## Leading Indicators

- Users click on sample records within the first session (not just loading the dashboard)
- Time to first meaningful action drops compared to empty-state users
- Users who view sample data proceed to create their own first object at a higher rate
- Sample data orientation walkthrough completion rate exceeds 50%

## Instructions

### 1. Design and build the sample data package

Run the the sample data seeding workflow (see instructions below) drill. For the Smoke test, focus on:

- **One persona only**: Pick your highest-volume ICP segment. If you serve multiple industries, pick the one with the most signups.
- **Minimum viable data**: 3-5 primary objects in different states (one completed, one in-progress, one empty/not-started). Include enough supporting objects to make each primary object look realistic (comments, tags, assignments).
- **One hero record**: One sample record should be fully completed and showcase the product's core value. This is what the user sees first — it answers "what does a good result look like in this product?"

**Human action required:** Review the sample data content before deployment. Check that names, dates, and domain references are appropriate for your ICP. Approve the seed file.

### 2. Deploy to a small test group

Implement the injection endpoint from the the sample data seeding workflow (see instructions below) drill. For Smoke, use the simplest injection method:

- If your signup flow is code you control: add the seed call after account creation, gated behind a hardcoded list of test account IDs or a PostHog feature flag
- Deploy to 10-50 new signups. Keep an equal-sized control group (empty accounts with no sample data) for comparison
- Use PostHog feature flags to split: 50% get sample data, 50% get the current empty-state experience

### 3. Build the first-run orientation

Run the `onboarding-flow` drill, specifically the in-app guidance component. For sample data accounts, the orientation should:

1. Show a welcome message on first login: "We set up a sample [workspace/project/pipeline] so you can explore how [Product] works."
2. Point to the hero record: "Start here — this is what a completed [object] looks like."
3. Provide a clear next step: "Try [specific action] on this sample, or create your own [object] when you are ready."
4. Include a "Clear sample data" link in the orientation and in the account settings.

Track each step: `sample_data_orientation_started`, `sample_data_orientation_completed`, `sample_data_first_interaction`.

### 4. Measure and evaluate

Run the `threshold-engine` drill to check results after 1 week (or after 50 users per group, whichever comes first).

Compute:
- **Sample data interaction rate**: % of seeded users who viewed or clicked at least 1 sample record within 48 hours. Target: ≥70%.
- **Time to first action**: Median time from signup to first meaningful interaction. Compare seeded vs. control.
- **Activation rate lift**: % of seeded users who reached activation vs. % of control users. Even a small lift is a positive signal.

**Pass threshold: ≥70% of seeded users interact with at least 1 sample record within 48 hours.**

If PASS: Document the seed file, persona, and injection method. Proceed to Baseline.
If FAIL: Diagnose where users drop off. Common failures:
- Users never see the sample data (discoverability problem — fix the orientation)
- Users see it but do not click (content problem — the sample records are not interesting)
- Users click but bounce immediately (relevance problem — the persona does not match)

## Time Estimate

- 2 hours: Design sample data schema and generate content
- 1 hour: Implement injection endpoint and feature flag
- 1 hour: Build first-run orientation messages
- 0.5 hours: Set up PostHog tracking events
- 1.5 hours: Monitor results over 1 week, analyze, document

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, funnel analysis | Free tier: 1M events/mo, 5K recordings ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app orientation messages | Early Stage: up to 90% off year 1; Essential: $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |

**Estimated monthly cost: Free** (within PostHog and Intercom free/startup tiers)

## Drills Referenced

- the sample data seeding workflow (see instructions below) — design the sample data schema, generate content, build injection and cleanup endpoints
- `onboarding-flow` — build the in-app orientation that guides users through sample data
- `threshold-engine` — evaluate ≥70% interaction rate against the pass threshold
