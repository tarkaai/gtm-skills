---
name: invite-viral-loop
description: Scale the invite mechanism into a self-reinforcing viral loop by optimizing viral coefficient, embedding invite triggers at delight moments, and segmenting invite strategies by user type
category: Advocacy
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-experiments
  - posthog-feature-flags
  - intercom-in-app-messages
  - loops-sequences
  - attio-lists
  - attio-custom-attributes
  - n8n-scheduling
  - n8n-workflow-basics
---

# Invite Viral Loop

This drill transforms the invite mechanism from a feature into a growth engine. A viral loop exists when invited users themselves invite more users at a rate that compounds. The viral coefficient (k) = (average invites per user) x (acceptance rate). If k > 1, the system is self-sustaining. If k < 1, each cohort decays — but even k = 0.3 means 30% more users for free.

## Input

- Invite mechanism running at Baseline level with 200+ total invitations sent
- PostHog tracking the full invite funnel (from `invite-flow-setup` drill)
- Acceptance rate at 50%+ (from `invite-acceptance-optimization` drill)
- Intercom, Loops, and n8n configured

## Steps

### 1. Measure the viral coefficient

Using `posthog-custom-events`, compute the viral metrics:

```sql
-- Viral coefficient for last 30 days
WITH invite_data AS (
  SELECT
    properties.account_id AS account_id,
    count(DISTINCT CASE WHEN event = 'invite_sent' THEN properties.invitee_email END) AS invites_sent,
    count(DISTINCT CASE WHEN event = 'invite_accepted' THEN properties.invited_user_id END) AS invites_accepted
  FROM events
  WHERE event IN ('invite_sent', 'invite_accepted')
    AND timestamp > now() - interval 30 day
  GROUP BY account_id
),
user_counts AS (
  SELECT count(DISTINCT person_id) AS total_active_users
  FROM events
  WHERE event = 'session_started'
    AND timestamp > now() - interval 30 day
)
SELECT
  sum(invites_sent)::float / (SELECT total_active_users FROM user_counts) AS avg_invites_per_user,
  sum(invites_accepted)::float / nullif(sum(invites_sent), 0) AS acceptance_rate,
  (sum(invites_sent)::float / (SELECT total_active_users FROM user_counts))
    * (sum(invites_accepted)::float / nullif(sum(invites_sent), 0)) AS viral_coefficient_k
FROM invite_data
```

Track weekly and segment by: user tenure, plan tier, number of existing team members, user role. The goal is to find which users are the best inviters and double down on them.

### 2. Identify and amplify super-inviters

Using `posthog-cohorts`, create cohorts based on invite behavior:

- **Super-inviters (3+ accepted invites):** These are your growth engine. Study their behavior. What do they do before inviting? What features do they use? What is their tenure?
- **Single-inviters (1 accepted invite):** The majority. Small nudges can push them to invite again.
- **Invite-attempted (sent but 0 accepted):** Their invites are not converting. Different problem — may need acceptance optimization or their invitees are not in the ICP.
- **Never-invited (active users, 0 invites):** The untapped pool. These users may not know the feature exists or may not see the value.

Using `attio-custom-attributes`, store per-account:
- `inviter_tier`: super | single | attempted | never
- `viral_coefficient`: account-level k value
- `invites_sent_30d`: count
- `invites_accepted_30d`: count
- `invited_users_retained_30d`: count of invited users still active after 30 days

Using `attio-lists`, maintain a list "Super-Inviters" for accounts with 3+ accepted invites.

### 3. Embed invite triggers at delight moments

The highest-converting invite prompts appear when a user just experienced value. Using `intercom-in-app-messages`, create contextual invite triggers:

**Post-milestone triggers:**
- After first successful workflow completion: "That worked! Want to invite a teammate to try this together?"
- After reaching a usage milestone (10th project, 100th record): "You've created {{count}} {{objects}}. Teams that collaborate here create {{multiplier}}x more."
- After positive NPS response: "Glad you are enjoying {{productName}}! Know someone who would benefit too?"

**Collaborative context triggers:**
- When user exports data: "Instead of exporting, invite {{recipientName}} so they can see this directly."
- When user copies a sharing link: "Want to give {{recipientName}} their own account? Invite them for real-time collaboration."
- When user comments on a resource: "{{resourceName}} has comments — invite your team to join the conversation."

**Scarcity-based triggers (use sparingly):**
- "You have {{seatsRemaining}} seats remaining on your plan. Use them before your next billing cycle."
- Only show if seats_remaining > 0 and the user has not been prompted in the last 14 days.

Track each trigger: `invite_trigger_shown`, `invite_trigger_clicked`, `invite_trigger_dismissed` with the trigger_type property.

### 4. Build the invited-user-invites-others loop

The viral loop closes when invited users themselves become inviters. This requires specific treatment:

Using `posthog-feature-flags`, create a flag `invited_user_invite_prompt` that targets users whose `was_invited` property is true and who have been active for 7+ days.

When the flag is active, show these prompts using `intercom-in-app-messages`:
- Day 7 after accepting invite: "You've been on {{teamName}} for a week. Know someone else who should be here?"
- After their first significant action: "Nice work on {{action}}! Your team is growing — invite the next teammate."

The timing is critical: too early (before they have experienced value) and they will not invite. Too late (after they are a power user) and you missed the enthusiasm window. Test the timing window with PostHog experiments.

### 5. Segment invite strategies by account type

Not all accounts have the same viral potential. Using `posthog-experiments` and `posthog-feature-flags`, run different invite strategies by segment:

**High-seat-limit accounts (10+ seat limit):**
- Emphasize collaborative features and team value
- Show "Your team is {{seatUtilization}}% — fill the remaining seats"
- Frequency: prompt every 7 days until utilization reaches 80%

**Low-seat-limit accounts (2-5 seat limit):**
- Invites here drive seat expansion (upsell)
- When they hit the seat limit: "Add more seats to invite {{inviteeName}}"
- Pair with the `upgrade-prompt` drill for upsell conversion

**Free-tier accounts:**
- Invites are acquisition, not expansion
- Liberal invite limits (free users inviting is free growth)
- "Invite unlimited teammates on the free plan" — use invites as a reason to stay on free rather than churning

**Enterprise accounts:**
- Invites require admin approval (compliance)
- Route invite requests through the admin workflow
- Track org-wide adoption rate: unique active users / total seats provisioned

### 6. Optimize the viral cycle time

Viral cycle time = average time from a user signing up to their first invite being accepted. Shorter cycle times compound faster.

Using `posthog-custom-events`, measure:
```javascript
posthog.capture('viral_cycle_completed', {
  inviter_user_id: inviterUserId,
  inviter_signup_date: inviterSignupDate,
  invite_sent_date: inviteSentDate,
  invite_accepted_date: now(),
  cycle_time_days: daysSinceInviterSignup,
  generation: inviterGeneration + 1  // 0 = organic, 1 = first invite, 2 = invite of invite
});
```

Track the generation property to see how deep the viral chain goes. Most chains die at generation 1. If you see generation 2+ chains, study what those users have in common.

To shorten cycle time:
- Move invite prompts earlier in the user journey (but after activation)
- Make the invite form instantly accessible (keyboard shortcut, persistent button)
- Pre-populate invite suggestions based on email domain colleagues

### 7. Build the viral dashboard

Using `n8n-scheduling`, create a weekly viral metrics report:

1. Overall viral coefficient (k)
2. k by user segment (super/single/attempted/never)
3. k by acquisition source (organic, paid, invited)
4. Acceptance rate trend
5. Average invites per user trend
6. Viral cycle time trend
7. Deepest chain generation this week
8. Top 10 super-inviter accounts

Post to Slack and store in Attio. This dashboard drives Scalable-level decision-making: which segments to invest in, which triggers to amplify, which experiments to run next.

## Output

- Measured viral coefficient with weekly tracking
- User segments by invite behavior stored in Attio
- Contextual invite triggers at 5+ delight moments
- Invited-user-invites-others loop with optimized timing
- Segment-specific invite strategies (high-seat, low-seat, free, enterprise)
- Viral cycle time tracking with generational depth
- Weekly viral metrics dashboard

## Triggers

Run at Scalable level after Baseline metrics are proven. The viral loop is self-sustaining once built — the n8n workflows and PostHog tracking run continuously. Review and optimize the trigger set monthly based on conversion data.
