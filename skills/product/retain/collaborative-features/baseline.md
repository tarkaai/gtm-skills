---
name: collaborative-features-baseline
description: >
  Multiplayer Product Features — Baseline Run. First always-on automation for collaboration
  adoption — automated invite prompts, sharing nudges, and feature announcements running
  continuously across all eligible users with full event tracking.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥40% collaboration usage, ≥20pp retention lift (team vs solo)"
kpis: ["Collaboration ratio (7d)", "Invite acceptance rate", "Retention lift (30d, team vs solo)", "Solo-to-Multiplayer funnel conversion"]
slug: "collaborative-features"
install: "npx gtm-skills add product/retain/collaborative-features"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---

# Multiplayer Product Features — Baseline Run

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Collaboration features run as always-on automation across all eligible users (not just a test cohort). At least 40% of active users engage in collaboration, and team users show a 20+ percentage-point retention lift over solo users at 30 days. The system runs continuously without manual intervention.

## Leading Indicators

- Automated collaboration prompts firing to all eligible solo users within 48 hours of deployment
- Invite acceptance rate stable above 40% across 2 weeks
- Solo-to-Multiplayer funnel showing improvement at the weakest step from Smoke
- Feature announcement reaching >80% of active users
- New collaboration events appearing daily without manual prompting

## Instructions

### 1. Expand event tracking to full taxonomy

Run the `posthog-gtm-events` drill to ensure the full collaboration event set is instrumented:

- Add co-editing events that were skipped at Smoke: `concurrent_session_started`, `concurrent_edit_made`, `concurrent_session_ended`
- Add team growth events: `workspace_created`, `team_member_added`, `team_member_removed`
- Add reaction events: `reaction_added`
- Verify all events from the collaboration instrumentation workflow (see instructions below) are firing correctly with complete properties

Build PostHog funnels showing the complete collaboration journey:

- **Full Solo-to-Multiplayer funnel:** signup → first core action → invite sent → invite accepted → concurrent session → second concurrent session within 7 days
- **Content sharing funnel:** content created → content shared → shared content viewed → viewer signed up → viewer first core action
- **Collaboration depth funnel:** first collaboration event → 3+ collaboration events in 7 days → collaboration in 2+ consecutive weeks

Create PostHog insights:
- `Collaboration Ratio (7d rolling)` — track daily
- `Invite Acceptance Rate (14d rolling)` — track daily
- `Retention: Team vs Solo (30d)` — track weekly
- `Avg Team Size (active workspaces)` — track weekly

Estimated time: 4 hours.

### 2. Launch collaboration feature announcement

Run the `feature-announcement` drill to drive awareness:

**Tier 1 announcement (all active users):**
- Intercom in-app message: banner at top of workspace highlighting collaboration features. Copy: "New: Work together in real time. Invite your team, share content, and collaborate — all inside [Product]." CTA: "Invite a teammate" (links directly to invite flow).
- Loops broadcast email to all active users: subject line "Your [Product] workspace just got multiplayer." Body: 3 specific collaboration use cases relevant to the user's content type. CTA: "Try it with your team."
- Segment the announcement: users who already collaborate get a "What's new in collaboration" message focused on new features (co-editing, reactions). Users who have never collaborated get the "Get started with your team" message.

**Track announcement effectiveness:**
- PostHog event: `collab_announcement_shown`, `collab_announcement_clicked`
- Measure: announcement shown → invite sent within 7 days
- Measure: announcement shown → content shared within 7 days

Estimated time: 3 hours.

### 3. Build always-on collaboration activation automation

Run the `activation-optimization` drill focused on collaboration:

**Identify the activation metric for collaboration:**
Using PostHog cohorts, find the collaboration action most correlated with 30-day retention. Test candidates:
- Sent at least 1 invite
- Had at least 1 concurrent editing session
- Shared at least 1 piece of content
- Received at least 1 comment on their content

The action with the highest retention correlation becomes the collaboration activation metric.

**Build the activation automation (n8n + Intercom + Loops):**

Create an n8n workflow that runs daily and targets solo users (no collaboration events, account age > 3 days, active in last 7 days):

- **Day 3 after signup (if solo):** Intercom product tour showing the invite flow. 3 steps: why teams are better → how to invite → what happens when they join.
- **Day 5 (if still solo):** Loops email with social proof: "Teams using [Product] together are {X}% more likely to stay active. Here's how to get started." Include a one-click invite link that pre-fills the inviter's workspace.
- **Day 10 (if still solo):** Intercom in-app message: "Working solo? Share your [most recent content type] with a colleague and see what they think." Deep-link to the share action for their most recent content.
- **Day 14 (if still solo):** Final Loops email: personal check-in. "Is [Product] working for you? Teams tell us collaboration is what made it click. Reply if you'd like help setting up your team."

**For users who invited but invitee did not accept:**
- Day 2 after invite sent: Remind inviter via Intercom tooltip: "Your invite to {name} is pending. Resend or try a shareable link instead."
- Day 5: Send invitee a second invite email with different copy via Loops.

**For users who collaborated once but stopped:**
- If no collaboration event in 7 days after first collaboration: Intercom in-app message highlighting what changed since they last collaborated (new content from teammates, new comments).

Estimated time: 6 hours.

### 4. Evaluate against threshold

Measure at the end of 2 weeks:

**Primary metrics:**
- Collaboration ratio: (users with ≥1 collaboration event in last 7 days) / (all active users in last 7 days). Threshold: ≥40%.
- Retention lift: 30-day retention of users with ≥1 collaboration event minus 30-day retention of solo users. Threshold: ≥20 percentage points.

**Secondary metrics:**
- Invite acceptance rate: target ≥40%
- Solo-to-Multiplayer funnel conversion: should show improvement over Smoke at the previously weakest step
- Average team size: should be trending upward

**Decision:**
- **Pass (≥40% collab ratio AND ≥20pp retention lift):** Collaboration automation works at scale. Document which automation touchpoints drive the most invites and shares. Proceed to Scalable.
- **Marginal (35-39% collab ratio OR 15-19pp retention lift):** Identify the weakest funnel step. Is the problem awareness (users not seeing prompts), motivation (users not caring), or friction (invite flow too hard)? Fix that step and run for another 2 weeks.
- **Fail (<35% collab ratio AND <15pp retention lift):** The always-on automation is not converting. Diagnose: is the collaboration feature itself compelling? Is the value of collaboration clear? Consider running user interviews (manual) to understand why users stay solo.

Estimated time: 3 hours.

## Time Estimate

- Full event tracking setup: 4 hours
- Feature announcement: 3 hours
- Activation automation build: 6 hours
- Threshold evaluation: 3 hours

**Total: ~16 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, retention analysis | Standard stack (excluded) |
| n8n | Always-on automation workflows, daily cohort targeting | Standard stack (excluded) |
| Intercom | Product tours, in-app messages, banners | Essential: $29/seat/mo. Proactive Support: $349/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Lifecycle emails, transactional invite emails, broadcasts | $49/mo (up to 5,000 contacts). [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost: ~$50-400/mo** (Loops $49/mo required; Intercom Proactive Support $349/mo if not already active — skip if using in-app messages only)

## Drills Referenced

- `posthog-gtm-events` — expands collaboration event tracking to full taxonomy, builds comprehensive funnels and daily tracking insights
- `feature-announcement` — coordinates the collaboration feature launch across in-app and email channels to drive initial awareness
- `activation-optimization` — identifies the collaboration activation metric, builds always-on automation that nudges solo users through the Solo-to-Multiplayer funnel
