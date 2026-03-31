---
name: collaboration-adoption-monitor
description: Health monitor for collaboration metrics — tracks team growth, sharing velocity, co-editing frequency, and collaboration-driven retention lift with automated alerting
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-retention-analysis
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
  - attio-lists
---

# Collaboration Adoption Monitor

This drill builds an always-on health monitor for multiplayer product features. It tracks whether collaboration adoption is growing, stable, or declining — and alerts when intervention is needed. Designed for the Durable level of the collaborative-features play.

## Input

- Collaboration event taxonomy fully instrumented (run `collaboration-instrumentation` first)
- At least 4 weeks of collaboration event data in PostHog
- n8n instance for monitoring workflows
- Attio CRM with workspace/account records

## Steps

### 1. Build the collaboration health dashboard

Using `posthog-dashboards`, create a dashboard called `Collaboration Health`:

**Row 1 — Primary metrics (trend lines, 90-day view):**
- Collaboration ratio (7d rolling) — % of active users who used a collaboration feature
- Team invite acceptance rate — `team_invite_accepted` / `team_invite_sent`
- Viral coefficient (k-factor) — weekly computation
- Average team size — mean of `team_size_after` across all workspaces

**Row 2 — Adoption funnels:**
- Solo-to-Multiplayer funnel conversion (from `collaboration-instrumentation`)
- Sharing Viral Loop funnel conversion

**Row 3 — Retention comparison:**
- 30-day retention: solo users vs. active-team users (side-by-side)
- 60-day retention: solo users vs. active-team users
- Retention lift: percentage-point difference between team and solo retention

**Row 4 — Feature breakdown:**
- Sharing volume by content type (stacked bar)
- Co-editing sessions per week (trend)
- Comments per active user per week (trend)
- Invite-to-activation rate (trend)

### 2. Set up anomaly detection

Using `posthog-anomaly-detection`, configure alerts for:

- **Collaboration ratio drop:** Collaboration ratio falls below 4-week average by >15%. Severity: high.
- **Invite acceptance decline:** Acceptance rate drops below 40% (2-week window). Severity: medium.
- **Team shrinkage spike:** `team_member_removed` events increase >100% week-over-week. Severity: high.
- **Sharing velocity drop:** `content_shared` count drops >25% week-over-week. Severity: medium.
- **Retention lift erosion:** Gap between team-user retention and solo-user retention narrows by >5pp. Severity: high.

### 3. Build the weekly health digest

Using `n8n-scheduling`, create a workflow that runs every Monday at 08:00 UTC:

1. Query PostHog for all collaboration metrics from the past 7 days
2. Compare to prior 7-day period and 4-week rolling average
3. Generate a health digest:

```
## Collaboration Health Digest — Week of {date}

### Key Metrics
| Metric | This Week | Last Week | 4-Week Avg | Trend |
|--------|-----------|-----------|------------|-------|
| Collaboration Ratio | {pct}% | {pct}% | {pct}% | {up/down/flat} |
| Invite Acceptance Rate | {pct}% | {pct}% | {pct}% | {up/down/flat} |
| Viral Coefficient (k) | {value} | {value} | {value} | {up/down/flat} |
| Avg Team Size | {value} | {value} | {value} | {up/down/flat} |
| Retention Lift (30d) | {pp}pp | {pp}pp | {pp}pp | {up/down/flat} |

### Anomalies
- {anomaly description or "None detected"}

### Cohort Sizes
- Solo users: {count} ({pct}% of active)
- Inviters (pending): {count}
- Active teams: {count}
- Power collaborators: {count}
- Collaboration churning: {count}

### Top-Performing Content Types (by share rate)
1. {content_type}: {share_rate}%
2. {content_type}: {share_rate}%

### Recommended Actions
- {action based on data, e.g., "Invite acceptance rate declining — review invite email copy and landing page" or "No action needed — all metrics stable"}
```

4. Post to Slack and store in Attio using `attio-notes`

### 4. Build per-workspace health scoring

Using `posthog-cohorts` and `attio-lists`, score each workspace on collaboration health:

**Score dimensions:**
- **Team growth:** Net new members this month (added - removed)
- **Collaboration depth:** Concurrent sessions per week
- **Sharing breadth:** Unique content types shared
- **Engagement velocity:** Comments + reactions per active member per week

**Score tiers:**
- **Thriving (80-100):** Growing team, deep collaboration, high sharing
- **Healthy (60-79):** Stable team, regular collaboration
- **Stalling (40-59):** No team growth, declining collaboration frequency
- **At risk (20-39):** Team shrinkage or collaboration stopped
- **Silent (0-19):** No collaboration events in 14+ days

Write scores to Attio using `attio-lists`:
- "Collaboration: Thriving Workspaces" — expansion candidates
- "Collaboration: At Risk Workspaces" — intervention needed

### 5. Trigger intervention routing

Using `n8n-triggers`, create automated responses:

- **Stalling workspaces (score 40-59):** Fire an Intercom in-app message highlighting an underused collaboration feature. Use PostHog data to pick the feature most likely to re-engage based on their content type.
- **At-risk workspaces (score 20-39):** Create a task in Attio for manual outreach. Include workspace size, last collaboration event date, and decline trajectory.
- **Silent workspaces (score 0-19):** Trigger a Loops re-engagement email sequence focused on collaboration value props. Include a "bring your team back" CTA.

## Output

- Collaboration health dashboard in PostHog
- Anomaly detection alerts for 5 critical metrics
- Weekly health digest posted to Slack and stored in Attio
- Per-workspace collaboration health scores in Attio
- Automated intervention routing for stalling/at-risk/silent workspaces

## Triggers

- Dashboard: always-on (PostHog real-time)
- Anomaly detection: always-on (PostHog real-time)
- Weekly health digest: Monday 08:00 UTC via n8n cron
- Per-workspace scoring: daily via n8n cron
- Intervention routing: triggered by score tier changes
