---
name: collaborative-features-scalable
description: >
  Multiplayer Product Features — Scalable Automation. Find the 10x multiplier for collaboration
  adoption through viral loop optimization, A/B tested invite flows, network-effect amplification,
  and engagement-driven churn prevention — all running at full user base scale.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥50% collaboration usage at 500+ users, viral coefficient k ≥ 0.3"
kpis: ["Collaboration ratio (7d)", "Viral coefficient (k-factor)", "Invite propagation rate", "Retention lift (30d)", "Collaboration-driven signups"]
slug: "collaborative-features"
install: "npx gtm-skills add product/retain/collaborative-features"
drills:
  - ab-test-orchestrator
  - collaboration-network-effects
  - engagement-score-computation
---

# Multiplayer Product Features — Scalable Automation

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Collaboration features produce self-reinforcing growth. At least 50% of active users collaborate, the viral coefficient reaches k ≥ 0.3 (each user indirectly brings in 0.3 new users through invites and shares), and the system runs at 500+ user scale without proportional effort increases. Churn prevention uses collaboration engagement data to intervene before at-risk users leave.

## Leading Indicators

- A/B tests on invite flows producing statistically significant winners within 3 weeks
- Viral loop maps showing measurable conversion at every step
- Power collaborators identified and receiving amplification messages
- Solo-to-team nudges converting at ≥5% of targeted solo users
- Engagement scores incorporating collaboration signals and feeding churn prevention
- At least 10% of new signups attributed to collaboration network effects (invites or shared content)

## Instructions

### 1. Optimize viral loops through systematic testing

Run the `ab-test-orchestrator` drill to test the highest-leverage improvements to collaboration adoption. Run experiments sequentially (one at a time) with sufficient sample size (200+ per variant minimum).

**Experiment 1 — Invite timing:**
Using PostHog feature flags, test when to prompt the first invite:
- Control: Day 3 after signup (current from Baseline)
- Variant A: Immediately after first core action completion ("Great work! Now invite a teammate to see this.")
- Variant B: After the user's third session ("You're getting value from [Product]. Your team will too.")
Primary metric: `team_invite_sent` rate within 7 days. Run for 3 weeks or until 200+ users per variant.

**Experiment 2 — Invite mechanism:**
- Control: Email invite (current)
- Variant A: Shareable link with preview ("Copy this link to invite anyone — no email needed")
- Variant B: In-app invite panel with contact import (pull from Google Contacts or company directory)
Primary metric: `team_invite_accepted` rate. Secondary: time-to-acceptance.

**Experiment 3 — Invited user onboarding:**
- Control: Standard onboarding flow
- Variant A: Contextual onboarding — invited user lands directly in inviter's workspace with their content visible
- Variant B: Guided collaboration — invited user's first action is a collaborative task with the inviter
Primary metric: invitee 7-day retention. Secondary: invitee `team_invite_sent` rate (propagation).

**Experiment 4 — Share landing page:**
- Control: Full content visible on share page
- Variant A: Partial content visible with signup gate to see more
- Variant B: Full content visible with prominent "Create your own" CTA
Primary metric: share page view → signup conversion rate.

Log all experiment results in Attio. After each experiment, implement the winner and update the baseline for the next experiment.

Estimated time: 20 hours over 2 months (5 hours per experiment cycle).

### 2. Build and activate network-effect amplification

Run the `collaboration-network-effects` drill to find and amplify organic viral loops:

**Map existing loops:**
Query PostHog for the invite loop, share loop, and co-editing loop. For each loop, compute:
- Cycle time (days from one user's action to the next user's equivalent action)
- Conversion rate at each step
- Total volume passing through the loop per week

Identify the loop with the highest volume and most room for conversion improvement.

**Deploy the amplification engine:**

For power collaborators (users who shared 5+ items or invited 3+ people in 14 days):
- Intercom in-app notification: "Your shared content was viewed {N} times this week. {X} people signed up because of you."
- Loops monthly email: "Your collaboration impact this month" with stats on views, signups, and team growth attributed to their activity.
- If a power collaborator's shared content has >10% view-to-signup conversion, feature it in a "Popular templates" or "Featured content" section visible to other users.

For solo users with team potential (high engagement score, multiple projects, daily usage, but zero collaboration events):
- Intercom in-app message: "Teams who use [Product] together retain {X}% better. Here's what {similar company} did." Include a case study or example relevant to their usage pattern.
- PostHog feature flag: test the copy and CTA variations to find what converts solo-to-team users most effectively.

For stalled invites (invite sent, not accepted after 48 hours):
- Automated reminder to inviter via Intercom tooltip
- Second invite email to invitee with different subject line and CTA via Loops
- If still not accepted after 7 days: suggest the inviter try a different invite method (shareable link if they used email, or vice versa)

Estimated time: 15 hours.

### 3. Incorporate collaboration into engagement scoring

Run the `engagement-score-computation` drill with collaboration signals weighted:

Update the engagement score model to include collaboration-specific dimensions:

**Standard dimensions (from existing drill):**
- Frequency (weight: 25%): active days in 14-day window
- Breadth (weight: 20%): distinct features used
- Depth (weight: 20%): events per session, session duration
- Recency (weight: 15%): days since last action

**New collaboration dimension (weight: 20%):**
```
collaboration_score = (
  min((team_invites_sent_14d / 3) * 25, 25) +        # inviting
  min((content_shared_14d / 5) * 25, 25) +            # sharing
  min((concurrent_sessions_14d / 3) * 25, 25) +       # co-editing
  min((comments_14d / 10) * 25, 25)                    # commenting
)
```

A user who invites 3+ people, shares 5+ items, has 3+ concurrent sessions, and makes 10+ comments in 14 days scores 100 on the collaboration dimension.

**Use collaboration-enriched scores for churn prevention:**
- Users with declining collaboration scores (were "Active Team" tier, now "Stalling") get prioritized intervention
- Users with high collaboration scores but declining individual engagement may indicate the product is working for their team but not for them individually — different intervention needed
- Users whose team members are churning get a proactive message: "We noticed some of your team hasn't been active. Here's how to re-engage them."

Write updated scores to Attio daily. Create Attio lists:
- "Collaboration Champions" — engagement score ≥80 with collaboration dimension ≥60
- "Team At Risk" — team size ≥2 but collaboration dimension dropped below 20

Estimated time: 10 hours.

### 4. Measure at scale and evaluate

At the end of 2 months, measure:

**Primary metrics:**
- Collaboration ratio at 500+ active users: (users with ≥1 collaboration event in last 7 days) / (all active users). Threshold: ≥50%.
- Viral coefficient: k = (invites_per_user/week × acceptance_rate × activation_rate) + (shares_per_user/week × view_to_signup_rate × activation_rate). Threshold: k ≥ 0.3.

**Secondary metrics:**
- Invite propagation rate: % of activated invitees who send their own invite. Target: ≥15%.
- Retention lift (30d): team users vs. solo users. Should maintain ≥20pp from Baseline.
- Collaboration-driven signups: % of new signups attributed to invites or shared content. Target: ≥10%.
- A/B test win rate: at least 2 of 4 experiments should produce statistically significant winners.

**Decision:**
- **Pass (≥50% collab ratio AND k ≥ 0.3):** Network effects are amplifying growth. The viral loops are measurable and improvable. Proceed to Durable.
- **Marginal (40-49% collab ratio OR k 0.2-0.29):** Identify which loop underperforms. Is the invite loop strong but sharing weak? Or vice versa? Double down on the stronger loop and optimize the weaker one.
- **Fail (<40% collab ratio AND k < 0.2):** Scale reveals that collaboration adoption does not grow virally. The feature may be useful for retention (team users stay longer) but does not produce network effects. Consider pivoting the play to focus purely on retention lift rather than viral growth.

Estimated time: 15 hours (analysis and documentation).

## Time Estimate

- Invite flow A/B testing (4 experiments): 20 hours
- Network-effect amplification: 15 hours
- Engagement scoring with collaboration: 10 hours
- Scale measurement and evaluation: 15 hours

**Total: ~60 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, funnels, engagement analytics | Standard stack (excluded) |
| n8n | Amplification engine automation, engagement scoring pipeline, stalled invite recovery | Standard stack (excluded) |
| Attio | Engagement scores, collaboration champion lists, team-at-risk tracking | Standard stack (excluded) |
| Intercom | In-app messages, tooltips, product tours for experiment variants and amplification | Proactive Support: $349/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Lifecycle emails for invite sequences, power collaborator engagement, solo-to-team nudges | $49/mo (up to 5,000 contacts). [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost: ~$50-400/mo** (Loops $49/mo; Intercom Proactive Support $349/mo if not already active)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on invite timing, invite mechanism, invitee onboarding, and share landing pages
- `collaboration-network-effects` — maps viral loops, identifies bottlenecks, builds the amplification engine, measures viral coefficient, and tracks network-effect attribution
- `engagement-score-computation` — adds collaboration dimension to engagement scores, feeds churn prevention with team-aware risk signals, creates Attio lists for champions and at-risk teams
