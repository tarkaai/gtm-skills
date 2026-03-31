---
name: invite-mechanism-baseline
description: >
  Team Invite System — Baseline Run. Instrument the full invite funnel with standard
  GTM events, optimize the acceptance flow to reduce drop-off, and run the invite
  mechanism always-on for all eligible users. Prove that invite rate and acceptance rate
  hold at scale over 4 weeks.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=25% of active users send an invite AND >=55% acceptance rate sustained over 4 weeks"
kpis: ["Invite rate (% active users who invite)", "Acceptance rate", "Invitee activation rate", "Invitee 7-day retention", "Seats added per account"]
slug: "invite-mechanism"
install: "npx gtm-skills add product/upsell/invite-mechanism"
drills:
  - posthog-gtm-events
  - invite-acceptance-optimization
  - activation-optimization
---

# Team Invite System — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The invite mechanism is live for all eligible users (not just a test cohort). Event tracking follows the standard GTM taxonomy so invite metrics feed into cross-play dashboards. The invite-to-acceptance funnel is optimized — signup friction removed, email copy personalized, reminder sequence active. Over 4 consecutive weeks, at least 25% of active users send an invite and at least 55% of invitations are accepted.

## Leading Indicators

- Invite form abandonment rate decreasing week over week
- Invite email open rate above 60% (the subject line and sender work)
- Signup completion rate for invited users above 65% (the acceptance flow is frictionless)
- Invited users retain at the same rate or better than organic users at 7 days
- Accounts with invited members show higher engagement than solo accounts

## Instructions

### 1. Standardize event tracking

Run the `posthog-gtm-events` drill to align invite events with the standard GTM taxonomy. Map the invite-specific events to the standard schema:

| Invite Event | Standard GTM Event | Properties |
|-------------|-------------------|------------|
| `invite_form_opened` | `feature_engaged` | `feature: invite`, `entry_point`, `account_id` |
| `invite_sent` | `lead_created` | `source: invite`, `channel: product`, `invite_count`, `entry_point` |
| `invite_accepted` | `activation_reached` | `source: invite`, `was_invited: true`, `time_to_accept_hours` |
| `invited_user_first_action` | `feature_engaged` | `was_invited: true`, `action`, `time_to_first_action_minutes` |

Keep the invite-specific event names as well (they provide granularity). The standard GTM events allow invite metrics to appear in cross-play funnels and dashboards.

Build the PostHog funnels:
- **Invite send funnel:** active_user -> invite_form_opened -> invite_sent (measures intent-to-action conversion)
- **Invite acceptance funnel:** invite_sent -> invite_email_delivered -> invite_link_clicked -> invite_accepted -> invited_user_first_action (measures the full downstream pipeline)

Build PostHog cohorts:
- "Inviters — last 30 days" (users who sent at least one invite)
- "Invited users — active" (users who accepted an invite and are active in last 7 days)
- "Invited users — churned" (users who accepted but have not been active in 14+ days)

### 2. Optimize the acceptance funnel

Run the `invite-acceptance-optimization` drill. This is the highest-leverage work at Baseline — every percentage point of acceptance rate improvement multiplies across all invitations sent.

Focus areas based on Smoke test data:
- **If email click-through is below 50%:** Optimize the invitation email subject line and body. Test personalization (inviter name, team context, shared resource name).
- **If signup completion is below 60%:** Strip the invited-user signup to the bare minimum (name + password, email pre-filled). Remove email verification — the invite link is the verification.
- **If invitee activation is below 70%:** Build an invited-user-specific onboarding experience. Drop them into the shared context, not a generic dashboard.

Set up the reminder sequence in Loops: Day 2, Day 5, Day 12 reminders for unaccepted invitations. Track each reminder step separately.

### 3. Roll out to all eligible users

Remove the feature flag restriction from Smoke. Enable the invite surface for all users who:
- Have been active for at least 7 days
- Are on a plan with available seats OR are on a free plan with unlimited invites
- Have not been shown an invite prompt in the last 7 days (frequency cap)

**Human action required:** Monitor the first 48 hours after full rollout. Watch for spikes in invite email bounces (deliverability issue), invite form errors (product bug), or support tickets about the invite flow. Be ready to pause via feature flag if anything breaks.

### 4. Optimize invited user activation

Run the `activation-optimization` drill with a focus on invited users. Compare the activation funnel for invited users vs organic users:

- Do invited users reach the activation metric faster? (They should — they have social context.)
- Where do invited users drop off relative to organic users?
- Are invited users who land in the shared context more likely to activate than those who land on a generic page?

If invited user activation is lower than organic: the acceptance flow is sending them to the wrong place or the onboarding is not adapted for invited users. Fix the post-accept landing experience.

### 5. Measure for 4 weeks

Track weekly:
- Invite rate: unique users who sent an invite / total active users
- Acceptance rate: invites accepted / invites sent
- Invitee activation rate: invited users who completed first action / invited users who accepted
- Invitee 7-day retention: invited users active at Day 7 / invited users who accepted
- Seats added: net new seats added to accounts via invites

Evaluate against threshold at week 4:
- **>=25% invite rate** (sustained, not just first-week novelty)
- **>=55% acceptance rate** (averaged across all 4 weeks)

If PASS: Invite mechanism works at scale with repeatable results. Proceed to Scalable.
If FAIL on invite rate: Users are not finding or using the invite surface. Add more entry points or more contextual prompts at delight moments.
If FAIL on acceptance rate: The invite email or signup flow still has too much friction. Run another optimization cycle with the `invite-acceptance-optimization` drill.

## Time Estimate

- 4 hours: Standardize event tracking and build PostHog funnels/cohorts
- 8 hours: Optimize acceptance funnel (email, signup, onboarding) across 2-3 iterations
- 2 hours: Configure full rollout and monitor
- 4 hours: Optimize invited user activation
- 2 hours: Weekly measurement and evaluation (4 x 30 min)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature flags | Free up to 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, product tours for invited users | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Invite emails, reminder sequences | From $49/mo for paid plans; transactional email included free ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM contact and deal tracking | From $29/user/mo on Plus plan ([attio.com](https://attio.com)) |
| n8n | Workflow automation for invite routing | Free self-hosted; cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing/)) |

**Estimated play-specific cost at Baseline:** $50-150/mo (Loops paid plan + n8n cloud, if not self-hosted; PostHog and Attio likely within free tiers)

## Drills Referenced

- `posthog-gtm-events` — standardizes invite event tracking to the GTM taxonomy for cross-play dashboards
- `invite-acceptance-optimization` — systematically improves conversion at every step of the invite-to-acceptance funnel
- `activation-optimization` — identifies and improves the activation metric for invited users specifically
