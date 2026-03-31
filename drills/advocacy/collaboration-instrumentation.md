---
name: collaboration-instrumentation
description: Instrument collaboration-specific events in PostHog — invites sent, shares created, co-editing sessions, comments, and team growth — to measure multiplayer adoption and network effects
category: Advocacy
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - posthog-retention-analysis
  - n8n-workflow-basics
---

# Collaboration Instrumentation

This drill sets up the event tracking foundation for any multiplayer product feature play. It defines the collaboration event taxonomy, builds the funnels that measure adoption, and creates the cohorts that feed downstream drills (churn prevention, engagement scoring, network-effect amplification).

## Input

- PostHog tracking installed with user identification (distinct_id tied to user accounts)
- Product has at least one collaboration feature (invites, sharing, co-editing, comments, or team workspaces)
- n8n instance for enrichment pipelines

## Steps

### 1. Define the collaboration event taxonomy

Using `posthog-custom-events`, instrument these events in your product. Every event fires server-side (not just client-side) to avoid ad-blocker data loss.

**Invite events:**
- `team_invite_sent` — Properties: `inviter_id`, `invitee_email`, `invite_method` (email/link/in-app), `workspace_id`, `team_size_at_send`
- `team_invite_accepted` — Properties: `inviter_id`, `invitee_id`, `time_to_accept_hours`, `workspace_id`, `team_size_after`
- `team_invite_expired` — Properties: `inviter_id`, `invitee_email`, `days_outstanding`

**Sharing events:**
- `content_shared` — Properties: `sharer_id`, `content_type` (document/project/dashboard/report), `share_scope` (team/public_link/specific_users), `recipient_count`, `content_age_days`
- `shared_content_viewed` — Properties: `viewer_id`, `is_new_user` (boolean), `sharer_id`, `content_type`, `share_scope`, `view_source` (direct_link/notification/feed)
- `shared_content_forked` — Properties: `viewer_id`, `sharer_id`, `content_type` (viewer copied or derived from shared content)

**Co-editing events:**
- `concurrent_session_started` — Properties: `user_ids` (array), `workspace_id`, `content_id`, `participant_count`
- `concurrent_edit_made` — Properties: `user_id`, `content_id`, `concurrent_users_count`, `edit_type`
- `concurrent_session_ended` — Properties: `session_duration_seconds`, `participant_count`, `edits_count`

**Comment/reaction events:**
- `comment_created` — Properties: `author_id`, `content_id`, `is_reply` (boolean), `mentioned_users` (array)
- `comment_resolved` — Properties: `resolver_id`, `author_id`, `time_to_resolve_hours`
- `reaction_added` — Properties: `user_id`, `content_id`, `reaction_type`

**Team growth events:**
- `workspace_created` — Properties: `creator_id`, `workspace_name`
- `team_member_added` — Properties: `workspace_id`, `adder_id`, `role_assigned`, `team_size_after`
- `team_member_removed` — Properties: `workspace_id`, `remover_id`, `team_size_after`

### 2. Build the collaboration adoption funnel

Using `posthog-funnels`, create:

**Primary funnel — Solo to Multiplayer:**
1. `user_signed_up` (or `account_created`)
2. `first_core_action_completed` (user did something valuable alone)
3. `team_invite_sent` (user attempted to bring someone else in)
4. `team_invite_accepted` (second user joined)
5. `concurrent_session_started` (both users active together)

**Secondary funnel — Sharing to Viral Growth:**
1. `content_shared` (where `share_scope` = `public_link`)
2. `shared_content_viewed` (where `is_new_user` = true)
3. `user_signed_up` (attributed to share)
4. `first_core_action_completed`
5. `content_shared` (new user shares — the loop closes)

Save both funnels as `Collaboration: Solo to Multiplayer` and `Collaboration: Sharing Viral Loop`.

### 3. Create collaboration cohorts

Using `posthog-cohorts`, create dynamic cohorts:

- **Solo users:** `team_invite_sent` count = 0 AND account age > 7 days
- **Inviters (pending):** `team_invite_sent` count >= 1 AND `team_invite_accepted` count = 0
- **Active teams:** `concurrent_session_started` count >= 1 in last 14 days
- **Power collaborators:** `content_shared` count >= 5 in last 14 days OR `comment_created` count >= 10 in last 14 days
- **Collaboration churning:** `concurrent_session_started` count dropped >50% week-over-week

### 4. Compute the collaboration ratio

Using `posthog-retention-analysis`, build a daily metric:

```
collaboration_ratio = (users with >=1 collaboration event in last 7 days) / (total active users in last 7 days)
```

Collaboration events = `team_invite_sent` OR `content_shared` OR `concurrent_session_started` OR `comment_created`.

Track this as a PostHog insight named `Collaboration Ratio (7d rolling)`. This is the primary KPI for the collaborative-features play.

### 5. Build the invite-to-activation pipeline

Using `n8n-workflow-basics`, create a workflow that fires when `team_invite_accepted` occurs:

1. Query PostHog for the new user's first 48-hour activity
2. Check if they completed `first_core_action_completed`
3. If yes: tag the invite as "activated" in PostHog (`team_invite_activation` event)
4. If no after 48 hours: tag as "stalled" and feed into onboarding intervention

This data tells you whether your invites produce activated users or dead accounts.

### 6. Measure network effect coefficient

Compute the viral coefficient (k-factor) weekly:

```
k = (invites_sent_per_user_per_week) × (invite_acceptance_rate) × (activation_rate_of_invitees)
```

Track as PostHog insight `Collaboration: Viral Coefficient (weekly)`. A k > 1 means organic growth from collaboration alone. Most products target k = 0.3-0.7 initially.

## Output

- Complete collaboration event taxonomy instrumented in PostHog
- Two adoption funnels (Solo-to-Multiplayer, Sharing Viral Loop)
- Five collaboration cohorts for targeting
- Collaboration ratio as primary metric
- Invite-to-activation pipeline tracking invitee quality
- Viral coefficient computation for network-effect measurement

## Triggers

- Event instrumentation: one-time setup
- Cohort refresh: automatic (PostHog real-time)
- Viral coefficient computation: weekly via n8n cron
- Invite-to-activation check: triggered by `team_invite_accepted` events
