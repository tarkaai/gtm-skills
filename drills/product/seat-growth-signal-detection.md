---
name: seat-growth-signal-detection
description: Detect team growth signals — invitations sent, collaboration spikes, new user additions — and score accounts for seat expansion readiness
category: Revenue Ops
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-custom-attributes
  - attio-lists
---

# Seat Growth Signal Detection

This drill builds the detection layer that identifies accounts whose team dynamics signal they are ready to add seats. Unlike generic upgrade prompts, this operates on collaboration-specific signals — the behavioral patterns that precede natural team expansion.

## Input

- PostHog tracking active with per-user and per-account event data (minimum 14 days)
- Events capturing team-related actions: invitations, shared resources, @mentions, collaborative edits, permission changes
- n8n instance for scheduled detection runs
- Attio CRM for storing expansion readiness scores

## Steps

### 1. Define seat growth signals

Using the `posthog-custom-events` fundamental, identify and instrument the events that predict seat expansion. Good signals fall into three categories:

**Direct signals (someone is actively trying to add users):**
- `team_invite_sent` — user sent an invitation to a colleague
- `team_invite_failed` — invitation blocked by seat limit
- `seat_limit_hit` — user attempted an action requiring more seats
- `admin_viewed_billing` — admin visited the billing or seats page
- `team_settings_viewed` — user browsed team management settings

**Collaboration signals (usage patterns that outgrow current seats):**
- `resource_shared_external` — user shared a link or resource with someone not on the account
- `collaborative_edit_attempted` — user tried to collaborate on an asset
- `mention_non_member` — user @mentioned someone who is not on the team
- `export_for_colleague` — user exported data in a format suggesting they are sharing with others manually

**Growth signals (the account is scaling):**
- `project_count_increased` — account crossed a project count threshold (e.g., 5, 10, 20)
- `api_key_created` — new API key suggests new integrations or team members
- `workspace_created` — new workspace or environment suggests departmental expansion
- `usage_volume_spike` — weekly active usage jumped 50%+ compared to 4-week average

Instrument each event with these properties:
```javascript
posthog.capture('team_invite_sent', {
  account_id: accountId,
  inviter_user_id: userId,
  current_seat_count: currentSeats,
  seat_limit: planSeatLimit,
  seats_remaining: planSeatLimit - currentSeats,
  invite_target_domain: targetEmailDomain  // same company domain = strong signal
});
```

### 2. Build a seat expansion readiness score

Each signal carries a different weight. Compute a per-account `seat_expansion_score` using this model:

| Signal | Points | Decay |
|--------|--------|-------|
| `team_invite_failed` (seat limit hit) | 30 | 14 days |
| `seat_limit_hit` | 25 | 14 days |
| `team_invite_sent` (same domain) | 20 | 7 days |
| `admin_viewed_billing` | 15 | 7 days |
| `mention_non_member` | 10 | 7 days |
| `resource_shared_external` | 8 | 14 days |
| `usage_volume_spike` | 8 | 14 days |
| `project_count_increased` | 5 | 30 days |
| `workspace_created` | 5 | 30 days |

Points decay over time — a `team_invite_sent` from 6 days ago is worth 20 points, but one from 10 days ago is worth ~7 points (linear decay). This prevents stale signals from triggering prompts.

Run a HogQL query to compute the score:

```sql
SELECT
  properties.$group_0 AS account_id,
  sum(
    CASE event
      WHEN 'team_invite_failed' THEN 30 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 14)
      WHEN 'seat_limit_hit' THEN 25 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 14)
      WHEN 'team_invite_sent' THEN 20 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 7)
      WHEN 'admin_viewed_billing' THEN 15 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 7)
      WHEN 'mention_non_member' THEN 10 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 7)
      WHEN 'resource_shared_external' THEN 8 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 14)
      WHEN 'usage_volume_spike' THEN 8 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 14)
      WHEN 'project_count_increased' THEN 5 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 30)
      WHEN 'workspace_created' THEN 5 * greatest(0, 1 - dateDiff('day', timestamp, now()) / 30)
      ELSE 0
    END
  ) AS seat_expansion_score
FROM events
WHERE event IN (
  'team_invite_failed', 'seat_limit_hit', 'team_invite_sent',
  'admin_viewed_billing', 'mention_non_member', 'resource_shared_external',
  'usage_volume_spike', 'project_count_increased', 'workspace_created'
)
AND timestamp > now() - interval 30 day
GROUP BY account_id
HAVING seat_expansion_score > 15
ORDER BY seat_expansion_score DESC
```

### 3. Classify accounts into expansion tiers

Using `posthog-cohorts`, create three dynamic cohorts:

- **Hot (score >= 40):** Multiple strong signals in the last week. This account is actively trying to grow and hitting limits. Prompt immediately.
- **Warm (score 20-39):** Collaboration patterns suggest growth. Time a prompt when they next show a direct signal.
- **Watch (score 15-19):** Early indicators. Do not prompt yet. Monitor for score increase.

### 4. Store expansion data in CRM

Using the `attio-custom-attributes` fundamental, add these fields to the company record in Attio:

- `seat_expansion_score`: numeric score from the model
- `seat_expansion_tier`: hot | warm | watch | none
- `current_seat_count`: how many seats are in use
- `seat_limit`: plan seat limit
- `seat_utilization_pct`: current_seat_count / seat_limit * 100
- `last_expansion_signal`: timestamp of most recent qualifying signal
- `expansion_signal_count_30d`: total qualifying signals in last 30 days

Using `attio-lists`, maintain a list called "Seat Expansion — Ready" that auto-populates with all hot and warm accounts.

### 5. Build the scheduled detection workflow

Using `n8n-scheduling`, create a workflow that runs every 6 hours:

1. Query PostHog for all accounts with seat_expansion_score > 15 (Step 2 query)
2. Classify into tiers (Step 3 logic)
3. Update Attio records with current expansion data (Step 4)
4. For accounts that moved into the hot tier since last run, fire a webhook to trigger the `seat-expansion-prompt-delivery` drill
5. For accounts whose score dropped below 15, clear the tier and log the cooldown

Using `n8n-triggers`, add a webhook endpoint so the product can request an on-demand score recalculation for a specific account (useful when a user hits a seat limit in real time).

### 6. Track detection accuracy

Using `posthog-custom-events`, log every detection event:

```javascript
posthog.capture('seat_expansion_signal_detected', {
  account_id: accountId,
  expansion_tier: 'hot',
  score: 52,
  current_seats: 4,
  seat_limit: 5,
  top_signal: 'team_invite_failed'
});
```

After 30 days, measure: of accounts flagged as "hot," what percentage actually added seats within 14 days? Target: 35%+ of hot flags should convert. If false positive rate exceeds 65%, tighten the scoring weights or add exclusion rules (e.g., exclude accounts that just removed a seat).

## Output

- Per-account seat expansion readiness scoring running every 6 hours in n8n
- Three PostHog cohorts (hot, warm, watch) updated automatically
- Attio records enriched with expansion score and seat utilization data
- Webhook trigger for downstream prompt delivery
- Detection accuracy tracking via PostHog events

## Triggers

Runs every 6 hours via n8n cron. On-demand via webhook for real-time seat-limit events. Recalibrate scoring weights monthly based on actual conversion data.
