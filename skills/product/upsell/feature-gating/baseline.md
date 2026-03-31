---
name: feature-gating-baseline
description: >
  Premium Feature Gating — Baseline Run. Always-on gate with automated trial provisioning,
  trial-to-upgrade nurture sequences, and full funnel tracking to prove gates drive
  sustained upgrade conversions.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥25% trial-to-upgrade conversion rate with ≥10pp lift over non-gated organic upgrades"
kpis: ["Trial-to-upgrade conversion rate", "Lift vs. organic", "Gate funnel completion rate", "Trial engagement depth", "Time to upgrade"]
slug: "feature-gating"
install: "npx gtm-skills add product/upsell/feature-gating"
drills:
  - posthog-gtm-events
  - upgrade-prompt
  - feature-adoption-monitor
---

# Premium Feature Gating — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

25% or more of users who start a trial of the gated premium feature convert to a paid upgrade, with at least 10 percentage points lift over the organic upgrade rate (users who upgrade without encountering the gate). The gate-to-upgrade pipeline runs always-on for 2 weeks with automated trial provisioning, email nurture during the trial, and expiration-triggered upgrade prompts. This proves that feature gating reliably converts trial users into paying customers, not just creates momentary interest.

## Leading Indicators

- Organic upgrade rate stays below 15% (validates the gate is causing the lift, not just correlating with users who would have upgraded anyway)
- Trial engagement depth increasing: users who use the premium feature 5+ times during the trial convert at 2x the rate of those who use it 1-2 times
- Nurture email open rates above 40% (trial users are paying attention to guidance)
- Time-to-upgrade decreasing week over week (the trial experience is accelerating the decision)
- Trial abandonment rate below 30% (most trial users engage with the feature)

## Instructions

### 1. Set up full gate event tracking

Run the `posthog-gtm-events` drill to instrument comprehensive tracking for the feature gating pipeline:

| Event | When Fired | Key Properties |
|-------|-----------|---------------|
| `gate_impression` | User encounters the locked feature | `feature`, `user_plan`, `page`, `impression_count` (nth time this user has seen this gate) |
| `gate_preview_engaged` | User interacts with value preview | `feature`, `preview_type`, `engagement_seconds` |
| `gate_trial_started` | User starts a trial | `feature`, `trial_duration_days`, `source` (gate vs. email vs. settings page) |
| `gate_trial_feature_used` | User uses the premium feature during trial | `feature`, `action`, `usage_count` (running total during this trial) |
| `gate_trial_expired` | Trial period ends without upgrade | `feature`, `feature_used_count`, `last_feature_use` |
| `gate_upgrade_started` | User begins upgrade checkout | `feature`, `source` (gate/email/trial-expiry/settings), `user_plan`, `target_plan` |
| `gate_upgrade_completed` | User completes payment | `feature`, `plan`, `mrr_delta`, `trial_duration_days` |
| `gate_dismissed` | User dismisses the gate | `feature`, `impression_count`, `time_on_gate_seconds` |

Build PostHog funnels:
- **Gate-to-trial:** `gate_impression` -> `gate_preview_engaged` -> `gate_trial_started`
- **Trial-to-upgrade:** `gate_trial_started` -> `gate_trial_feature_used` (3+ times) -> `gate_upgrade_completed`
- **Full funnel:** `gate_impression` -> `gate_trial_started` -> `gate_upgrade_completed`

Break each funnel down by `feature` and by `source` to identify which gate entry points convert best.

### 2. Automate trial provisioning and nurture

Extend the Smoke test's manual trial flow into an always-on automated system:

**Trial provisioning (n8n workflow):**
1. PostHog webhook fires on `gate_trial_started`
2. Enable the PostHog feature flag for the user (premium feature becomes accessible)
3. Create a trial record in Attio: user, feature, start date, end date, status = "active"
4. Enroll the user in the trial nurture sequence in Loops

**Trial nurture sequence (Loops):**
- **Email 1 (immediate):** "Your trial of [feature] is active. Here is the single best thing to try first: [specific action with deep link]." Short, action-focused.
- **Email 2 (Day 2):** "Users who [specific action] during their trial see [quantified benefit]. Here is how: [brief walkthrough or link to 60-second video]." Include the user's current trial usage count.
- **Email 3 (Day 5):** "Your trial ends in 2 days. Here is what you accomplished: [personalized usage summary]. Upgrade to keep [feature] — [one-click upgrade link]." Only send if the user has engaged with the feature. If they have not engaged, send a different email: "You have not tried [feature] yet — here is a 2-minute guide to get started before your trial ends."
- **Email 4 (Day 7, trial expired):** "Your trial of [feature] has ended. During your trial, you [summary]. Upgrade to Pro to restore access — [upgrade link]." Include a 48-hour extension offer for users who engaged heavily but did not upgrade.

Run the `upgrade-prompt` drill to configure in-app upgrade prompts that fire during the trial based on usage signals, not just time:
- After 3rd use of the premium feature: subtle banner — "Enjoying [feature]? Upgrade to keep it."
- After 5th use: modal with usage summary — "You have used [feature] [N] times. Upgrade to make it permanent."
- On trial expiration: full-screen gate returns with personalized copy — "You [accomplished X] with [feature]. Upgrade to continue."

### 3. Set up always-on monitoring

Run the `feature-adoption-monitor` drill adapted for the gate-to-upgrade pipeline:

**Daily automated checks (n8n):**
- Count of active trials, new trials started today, trials expiring in next 48 hours
- Trial engagement rate: percentage of active trial users who used the premium feature in the last 24 hours
- Gate fatigue detection: users who have seen the gate 5+ times without starting a trial — suppress the gate for 14 days and try an email approach instead

**Automated alerts:**
- Trial-to-upgrade conversion rate drops below 15% for 3 consecutive days
- Trial abandonment rate (zero feature usage during trial) exceeds 40%
- Gate dismissal rate exceeds 60% for any feature (the gate is annoying users without converting them)

**Stalled trial intervention:**
- Users who started a trial but have not used the feature after 48 hours: trigger an Intercom in-app message when they next log in: "Your trial of [feature] is waiting. Here is the quickest way to try it: [deep link to specific action]."

### 4. Measure with control group

Using PostHog feature flags, split gate-eligible users 80/20:
- **Treatment (80%):** See the gate, can start trials
- **Control (20%):** See the feature listed in the pricing page but do not encounter the in-product gate. Track their organic upgrade rate.

This split validates that the gate is actually causing upgrades, not just intercepting users who would have upgraded anyway. Compare treatment upgrade rate vs. control upgrade rate after 2 weeks.

### 5. Evaluate against threshold

At the end of 2 weeks:

- **Trial-to-upgrade conversion rate:** `gate_upgrade_completed` / `gate_trial_started`. Target: >=25%.
- **Lift vs. organic:** Treatment upgrade rate minus control upgrade rate. Target: >=10 percentage points.

**Pass:** The gate-to-trial-to-upgrade pipeline reliably converts. Proceed to Scalable to gate multiple features and segment the experience.

**Fail:** Diagnose which funnel stage is weakest:
- Low trial starts (gate-to-trial <20%): The gate UX is not compelling. Test a different value preview format (video vs. screenshot vs. interactive demo).
- Low trial engagement (trial feature usage <60%): Users start trials but do not use the feature. The feature's first-run experience needs simplification or guided onboarding.
- Low trial-to-upgrade (<25%): Users engage during trial but do not pay. The price-to-value perception is off. Test different pricing displays on the gate, or extend trial duration.
- Low lift vs. control: The gate is not creating incremental upgrades. Users would have upgraded anyway. Test gating a different feature that is not already on the upgrade consideration path.

## Time Estimate

- 4 hours: Event taxonomy setup, funnel configuration, control group feature flag setup
- 4 hours: Trial provisioning automation (n8n workflow, Loops nurture sequence, trial expiration handling)
- 4 hours: Upgrade prompt configuration, monitoring setup, stalled-trial intervention
- 4 hours: Week 1 and Week 2 analysis, control group comparison, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, experiments | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app messages for trial guidance and upgrade prompts | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Trial nurture email sequence (4 emails) | Free up to 1,000 contacts — https://loops.so/pricing |
| n8n | Trial provisioning, expiration, and monitoring workflows | Free self-hosted — https://n8n.io/pricing |
| Attio | Trial records and upgrade deal tracking | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$0-50/mo (PostHog may need paid tier if event volume exceeds free tier)

## Drills Referenced

- `posthog-gtm-events` — instrument the full gate event taxonomy with gate, trial, and upgrade events
- `upgrade-prompt` — configure contextual in-app upgrade prompts triggered by trial usage signals
- `feature-adoption-monitor` — always-on monitoring with trial health checks, stalled-trial detection, and gate fatigue alerts
