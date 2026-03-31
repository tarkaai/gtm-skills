---
name: feature-deprecation-management-smoke
description: >
  Feature Sunset Communication — Smoke Test. Quantify the blast radius of a planned
  feature deprecation, build tiered communication, and validate that affected users
  acknowledge and begin migrating within a 1-week test window.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥80% of test cohort acknowledges deprecation notice AND ≥50% begins migration"
kpis: ["Notice acknowledgement rate", "Migration start rate", "Churn from sunset (test cohort)", "Communication engagement by tier"]
slug: "feature-deprecation-management"
install: "npx gtm-skills add product/retain/feature-deprecation-management"
drills:
  - deprecation-communication-setup
  - threshold-engine
---

# Feature Sunset Communication — Smoke Test

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Prove that you can identify affected users, communicate a deprecation clearly, and get them to start migrating — all before committing to an always-on system. The smoke test targets a small cohort (10-50 users) of one planned deprecation. Success means the communication system produces signal: users see the notice, understand what to do, and take the first migration step.

## Leading Indicators

- Deprecation notice shown to 100% of test cohort within 48 hours
- Notice click-through rate above 40%
- At least 3 users complete the migration product tour
- Zero support tickets from test cohort asking "what happened to [feature]?" (meaning communication was proactive enough)

## Instructions

### 1. Assess the deprecation blast radius

Run the the deprecation impact assessment workflow (see instructions below) drill against the feature you plan to deprecate. This produces:

- A PostHog cohort of all affected users segmented by dependency tier (critical, high, medium, low)
- Revenue exposure by tier
- Workflow dependency map
- A deprecation brief with recommended timeline and complexity score

From the full cohort, select 10-50 users as your test cohort. Include at least 2 users from each dependency tier to validate that the tiered messaging works for all levels.

**Human action required:** Review the deprecation brief. Confirm the sunset date and verify the replacement feature is ready. If the complexity score is 4-5, consider extending the timeline or simplifying the migration path before proceeding.

### 2. Build the deprecation communication system

Run the `deprecation-communication-setup` drill, but scope it to the test cohort only. This builds:

- Tier-segmented in-app deprecation banners (persistent for critical/high, tooltip for medium)
- A guided migration product tour for critical-tier users
- Email sequences (3-email for critical, 2-email for high, single for medium/low)
- PostHog events tracking every communication touchpoint

Use PostHog feature flags to limit all communication to the test cohort. No one outside the test group should see deprecation notices.

**Human action required:** Review all communication copy before activating. Ensure the migration guide is accurate. Test the product tour manually to verify each step works.

### 3. Activate and observe for 7 days

Activate all communication channels simultaneously. Over 7 days, monitor:

- How many users saw the deprecation notice (target: 100% of test cohort)
- How many clicked through to learn more (target: 40%+)
- How many started the migration (used replacement feature at least once)
- How many completed the migration product tour
- Whether any users churned or filed confused support tickets

Do not intervene during the test. The point is to see whether the communication system drives migration on its own.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure:

- **Primary threshold:** ≥80% of test cohort acknowledged the deprecation notice (saw it and either clicked or dismissed after reading)
- **Secondary threshold:** ≥50% of test cohort began migration (used the replacement feature at least once)

If PASS: The communication system works. Document what tier messages performed best, which channels drove the most migration starts, and any user feedback. Proceed to Baseline.

If FAIL: Diagnose where the funnel breaks. If acknowledgement is low, the notices are not visible enough or are being ignored. If acknowledgement is high but migration starts are low, the migration path is unclear or the replacement feature is not compelling. Fix the specific failure point and re-run.

## Time Estimate

- 2 hours: Impact assessment and brief review
- 1.5 hours: Communication setup and copy review
- 0.5 hours: Activation and flag configuration
- 1 hour: 7-day monitoring check-ins and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohorts, events, feature flags, funnels | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app banners, product tours | Essential $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences | Free under 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM records, deprecation brief storage | Standard stack — excluded from play budget |
| n8n | Automation | Standard stack — excluded from play budget |

**Estimated play-specific cost:** Free (all tools within free tier limits for a 10-50 user test)

## Drills Referenced

- the deprecation impact assessment workflow (see instructions below) — quantifies which users are affected and how heavily, produces the deprecation brief
- `deprecation-communication-setup` — builds tiered in-app and email deprecation notifications segmented by user dependency
- `threshold-engine` — evaluates notice acknowledgement and migration start rates against pass/fail thresholds
