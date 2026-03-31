---
name: invite-mechanism-scalable
description: >
  Team Invite System — Scalable Automation. Transform the invite mechanism into a viral
  growth loop by embedding invite triggers at every delight moment, running A/B tests on
  invite copy/timing/placement, detecting seat expansion signals, and measuring the viral
  coefficient. Scale to 500+ active users while maintaining invite and acceptance rates.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 8 weeks"
outcome: ">=25% invite rate at 500+ active users AND viral coefficient k >= 0.2 AND >=55% acceptance rate"
kpis: ["Invite rate at scale", "Acceptance rate", "Viral coefficient (k)", "Viral cycle time (days)", "Seats added per week", "Revenue from seat expansion"]
slug: "invite-mechanism"
install: "npx gtm-skills add product/upsell/invite-mechanism"
drills:
  - ab-test-orchestrator
  - seat-growth-signal-detection
---

# Team Invite System — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The invite mechanism operates as a self-reinforcing growth loop across 500+ active users. Invite triggers appear at 5+ product entry points timed to delight moments. A/B tests continuously optimize invite copy, timing, and placement. Seat expansion signals are detected and scored per account. The viral coefficient (k) is measured weekly and reaches >= 0.2, meaning every 5 users organically generate 1 additional user through invites. Acceptance rate holds at >= 55% despite higher volume.

## Leading Indicators

- Invite triggers at delight moments convert at 2x+ the rate of static entry points
- Invited users are themselves sending invites (generation 2+ chains exist)
- Seat expansion signals detected across 20%+ of active accounts
- A/B tests on invite copy/timing produce statistically significant winners within 2 weeks
- Revenue from seat expansion covers the cost of running the play

## Instructions

### 1. Run systematic A/B tests on the invite experience

Run the `ab-test-orchestrator` drill to test the highest-impact variables in the invite flow. Run one test at a time; do not stack experiments.

**Priority test sequence:**

**Test 1 — Entry point placement:**
- Control: Invite surface only in team settings
- Variant: Invite surface in team settings + post-milestone prompt + share-action prompt
- Metric: invites sent per active user per week
- Expected: Variant increases invites per user by 30%+

**Test 2 — Invite email subject line:**
- Control: "{{inviterName}} invited you to join {{teamName}} on {{productName}}"
- Variant A: "{{inviterName}} wants to collaborate with you"
- Variant B: "Join {{inviterName}} on {{productName}} — {{specificContext}}"
- Metric: email click-through rate (invite_link_clicked / invite_email_delivered)
- Expected: Context-specific subject lines increase CTR by 10%+

**Test 3 — Invited user landing experience:**
- Control: Land on generic product dashboard
- Variant: Land directly in the shared resource/workspace that triggered the invite
- Metric: invited_user_first_action rate within 30 minutes
- Expected: Contextual landing increases first-action rate by 20%+

**Test 4 — Invite prompt timing:**
- Control: Show invite prompt immediately after feature discovery
- Variant: Show invite prompt 24 hours after feature discovery (let the user experience value first)
- Metric: invite_sent conversion rate from the prompt
- Expected: Delayed prompt converts better because the user has internalized the value

Implement winning variants permanently before starting the next test. Log all results in Attio for the optimization audit trail.

### 2. Build the viral loop

Run the the invite viral loop workflow (see instructions below) drill to transform the invite mechanism from a feature into a compounding growth engine.

Key actions at Scalable level:
- Measure the viral coefficient (k) weekly and by segment
- Embed invite triggers at 5+ delight moments (post-milestone, post-share, post-NPS, post-collaborative-action, onboarding checklist)
- Build the invited-user-invites-others loop: prompt invited users to invite after they have been active for 7 days
- Segment invite strategies by account type (high-seat-limit, low-seat-limit, free tier, enterprise)
- Track viral cycle time and chain depth (generation tracking)
- Create the weekly viral metrics dashboard

Target: k >= 0.2 sustained over 4 weeks. This means for every 100 organic users, the invite mechanism generates 20 additional users for free. Even at k = 0.2, the compounding effect over 12 months is significant.

### 3. Detect and score seat expansion signals

Run the `seat-growth-signal-detection` drill to build the detection layer that identifies accounts ready to add seats.

Configure the seat expansion readiness score based on invite-specific signals:
- `team_invite_sent` with same-domain invitee: 20 points (7-day decay)
- `invite_blocked_seat_limit`: 30 points (14-day decay) — strongest signal
- `invite_form_opened` but not submitted: 10 points (7-day decay) — intent without follow-through
- `resource_shared_external`: 8 points (14-day decay)
- `admin_viewed_billing` after an invite attempt: 25 points (7-day decay)

Build the n8n workflow that runs every 6 hours:
1. Compute per-account seat expansion scores from PostHog
2. Classify into tiers: hot (>= 40), warm (20-39), watch (15-19)
3. Update Attio records with expansion data
4. For hot accounts: trigger the `seat-expansion-prompt-delivery` drill or the `upgrade-prompt` drill
5. For warm accounts: schedule a contextual in-app prompt for their next login

Track seat expansion conversion: of accounts flagged as "hot," what percentage added seats within 14 days? Target: 30%+ conversion of hot flags.

### 4. Scale to 500+ users and measure

With all systems running (A/B tests, viral loop, seat expansion detection), monitor the invite mechanism across your full user base.

Weekly metrics to track:
- **Invite rate:** unique inviters / total active users (target: >= 25%)
- **Acceptance rate:** invites accepted / invites sent (target: >= 55%)
- **Viral coefficient (k):** (avg invites per user) x (acceptance rate) (target: >= 0.2)
- **Viral cycle time:** median days from signup to first invite accepted (target: < 14 days)
- **Seats added per week:** net new seats from invite-driven expansion
- **Revenue impact:** additional MRR from seat expansion attributable to invites

Evaluate at week 8:
- **>=25% invite rate at 500+ active users** (proves the mechanism works at scale, not just with early adopters)
- **>=0.2 viral coefficient** (proves the loop compounds)
- **>=55% acceptance rate** (proves acceptance does not degrade at volume)

If PASS: The invite mechanism is a scalable growth lever. Proceed to Durable.
If FAIL on invite rate at scale: Invite fatigue or wrong audience. Segment users more aggressively — focus prompts on users whose behavior signals collaborative intent.
If FAIL on viral coefficient: Invited users are not inviting others. The invited-user experience is not generating enough delight for them to want to share.
If FAIL on acceptance rate: Volume is exposing deliverability issues or the invitee audience has shifted (e.g., external domains converting worse than same-company domains).

## Time Estimate

- 12 hours: Run 4 A/B tests over 8 weeks (3 hours each: setup, monitor, implement winner)
- 12 hours: Build viral loop (instrument triggers, measure k, track generations, build dashboard)
- 8 hours: Build seat expansion detection (scoring model, n8n workflow, Attio sync, prompt routing)
- 8 hours: Weekly measurement and optimization (8 x 1 hour)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, funnels, dashboards | Free up to 1M events/mo; 1M experiment requests free; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages at 5+ entry points, product tours | From $29/seat/mo; Proactive Support add-on $349/mo for high-volume messaging ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Invite emails, reminder sequences, transactional sends | From $49/mo; scales with contact count ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM for expansion scoring, deal tracking, lists | From $29/user/mo on Plus; Pro at $59/user/mo for advanced automation ([attio.com](https://attio.com)) |
| n8n | Scheduled workflows for seat expansion detection, viral metrics | Free self-hosted; Pro cloud at $60/mo for 10K executions ([n8n.io/pricing](https://n8n.io/pricing/)) |

**Estimated play-specific cost at Scalable:** $150-500/mo (driven primarily by Intercom Proactive Support if using high-volume in-app messaging; PostHog experiments and feature flags are free at moderate volume)

## Drills Referenced

- `ab-test-orchestrator` — runs rigorous A/B tests on invite copy, timing, placement, and landing experience
- the invite viral loop workflow (see instructions below) — transforms the invite mechanism into a compounding growth loop with viral coefficient tracking
- `seat-growth-signal-detection` — detects team growth signals and scores accounts for seat expansion readiness
