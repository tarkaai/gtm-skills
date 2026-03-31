---
name: collaborative-features-smoke
description: >
  Multiplayer Product Features — Smoke Test. Instrument collaboration events, run a small
  cohort test of team invites and content sharing, and measure whether collaboration usage
  reaches 30% of active users with measurable retention lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥30% collaboration usage among test cohort"
kpis: ["Collaboration ratio (7d)", "Invite acceptance rate", "Retention lift (team vs solo)"]
slug: "collaborative-features"
install: "npx gtm-skills add product/retain/collaborative-features"
drills:
  - onboarding-flow
  - threshold-engine
---

# Multiplayer Product Features — Smoke Test

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

At least 30% of users in a small test cohort (10-50 accounts) use a collaboration feature (invite, share, co-edit, or comment) within 7 days of being prompted. Solo-user vs. team-user retention shows a measurable gap. This proves that collaboration drives engagement before investing in always-on automation.

## Leading Indicators

- Collaboration events firing correctly in PostHog (invite, share, comment events appear within 24 hours of instrumentation)
- At least 5 users send team invites during the test window
- At least 1 shared content item is viewed by a non-user
- Solo-to-Multiplayer funnel shows non-zero conversion at every step

## Instructions

### 1. Instrument collaboration events

Run the the collaboration instrumentation workflow (see instructions below) drill. Focus on the minimum viable event set for Smoke:

- `team_invite_sent` and `team_invite_accepted`
- `content_shared` and `shared_content_viewed`
- `comment_created`

Skip co-editing instrumentation at Smoke level — it requires more engineering effort than the test warrants. Verify events appear in PostHog by triggering each one manually in the product.

Build the Solo-to-Multiplayer funnel from the drill. At this level, you need the funnel to exist, not to have statistical volume.

Compute the baseline collaboration ratio before any prompting: what percentage of current active users already use collaboration features organically? Log this number — it is your control.

Estimated time: 2 hours.

### 2. Configure collaboration prompts for the test cohort

Run the `onboarding-flow` drill, scoped to collaboration. Do not build a full onboarding sequence — build one targeted prompt:

- Using Intercom product tours, create a 3-step tour that appears for test cohort users:
  - Step 1: "Your work is better with your team. Invite someone to collaborate."
  - Step 2: Show the invite mechanism (link or email invite).
  - Step 3: Show the share mechanism for their existing content.
- Using Intercom in-app messages, create a follow-up message for users who completed the tour but did not invite within 48 hours: "Still working solo? Here's what teams unlock: [specific benefit based on their usage]."

**Human action required:** Select the test cohort — 10-50 accounts that are active (logged in 3+ days in the last 14), have created content, but have NOT yet used collaboration features. Create a PostHog cohort for these users and target the Intercom tour to this cohort only.

**Human action required:** Review the tour copy and CTA before launching. Ensure the invite flow works end-to-end (invite sent, email delivered, acceptance lands invitee in the correct workspace).

Estimated time: 1.5 hours.

### 3. Run the test and collect data

Launch the product tour to the test cohort. Monitor for 7 days:

- Daily: Check PostHog for new collaboration events from the test cohort. Log the count of `team_invite_sent`, `team_invite_accepted`, `content_shared`, `shared_content_viewed`, and `comment_created`.
- Day 3: Check invite acceptance rate. If zero invites accepted, check invite email deliverability (spam folder, broken links). If invites sent but not accepted, the invite email copy or landing page may need revision.
- Day 7: Pull the final numbers.

Do not intervene during the test unless something is broken (events not firing, invite emails not delivering). The point is to see organic response to a single prompt.

Estimated time: 1 hour (spread across 7 days).

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure:

**Primary metric:** Collaboration ratio among test cohort = (users who performed at least 1 collaboration event) / (total users in test cohort). Threshold: ≥30%.

**Secondary metrics:**
- Invite acceptance rate: `team_invite_accepted` / `team_invite_sent`. Healthy: ≥40%.
- Retention lift: Compare 7-day retention of test cohort users who collaborated vs. those who did not. Any positive lift is signal.

**Decision:**
- **Pass (≥30% collab ratio):** Collaboration features drive adoption when prompted. Proceed to Baseline. Document: which prompt worked, what content type was shared most, what the invite acceptance rate was.
- **Marginal (20-29%):** Re-examine the test. Was the cohort well-targeted? Was the prompt clear? Was the collaboration feature easy to find? Iterate on the prompt and re-run with a fresh cohort.
- **Fail (<20%):** The collaboration surface may not be compelling enough for the current user base. Investigate: do users understand the value of collaboration? Is the feature discoverable? Is the invite flow frictionless? Consider simplifying the collaboration surface (e.g., just sharing, no invites) before re-testing.

Estimated time: 0.5 hours.

## Time Estimate

- Collaboration instrumentation: 2 hours
- Prompt configuration: 1.5 hours
- Monitoring (7 days): 1 hour
- Threshold evaluation: 0.5 hours

**Total: ~5 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, collaboration ratio computation | Standard stack (excluded) |
| n8n | Workflow orchestration for invite-to-activation pipeline | Standard stack (excluded) |
| Intercom | Product tours and in-app messages for collaboration prompts | Essential: $29/seat/mo. Proactive Support add-on for tours: $349/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |

**Play-specific cost: Free** (Intercom is standard stack; tours included in Proactive Support if already active. If not, Smoke can use in-app messages only at no additional cost.)

## Drills Referenced

- the collaboration instrumentation workflow (see instructions below) — instruments collaboration events, builds the Solo-to-Multiplayer funnel, creates collaboration cohorts, and computes the collaboration ratio
- `onboarding-flow` — configures the in-app product tour and follow-up messages that prompt collaboration adoption in the test cohort
- `threshold-engine` — evaluates the test results against the 30% collaboration ratio threshold and recommends pass/iterate/fail
