---
name: expansion-signal-qualification
description: Manually qualify usage-limit signals from PostHog into sales-worthy expansion opportunities by enriching with account context and scoring urgency
category: Sales
tools:
  - PostHog
  - Attio
  - Clay
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - attio-deals
  - attio-custom-attributes
  - attio-lists
  - clay-company-search
  - clay-people-search
---

# Expansion Signal Qualification

This drill takes raw usage-limit signals (accounts approaching or exceeding plan limits) and qualifies them for sales-led outreach. Not every limit-hit account is a sales opportunity — some will self-serve, some are not expansion-ready, and some are low-value. This drill separates the accounts that warrant a personal sales conversation from those that should stay in the automated upgrade flow.

## Input

- PostHog usage data showing accounts at 70%+ of any plan limit (from `usage-threshold-detection` or a manual query)
- Attio CRM with account records (plan tier, MRR, account owner, lifecycle stage)
- Clay workspace for enrichment (optional for Smoke, required for Baseline+)

## Steps

### 1. Pull the raw expansion signal list

Query PostHog for accounts at 70%+ of any plan limit in the last 7 days:

```sql
SELECT
  properties.account_id AS account_id,
  properties.resource_type AS resource_type,
  properties.current_count AS current_count,
  properties.plan_limit AS plan_limit,
  properties.plan_tier AS plan_tier,
  round(properties.current_count / properties.plan_limit * 100, 1) AS pct_used,
  count() AS signal_count
FROM events
WHERE event = 'resource_consumed'
  AND timestamp > now() - interval 7 day
  AND properties.plan_limit > 0
  AND properties.current_count / properties.plan_limit >= 0.7
GROUP BY account_id, resource_type, current_count, plan_limit, plan_tier
ORDER BY pct_used DESC
```

Export to a working list. This is the raw signal set.

### 2. Enrich with account context from CRM

For each flagged account, pull from Attio using the `attio-deals` fundamental:

- Current MRR and plan tier
- Days since signup (accounts < 30 days old are likely still onboarding, not expanding)
- Account owner or CSM if assigned
- Previous expansion conversations (avoid re-pitching accounts already in an active deal)
- Support ticket history in last 30 days (high ticket volume = fix-first, not upsell)
- Number of active users vs. total seats

Using `attio-custom-attributes`, check for existing expansion-related fields. If they do not exist yet, create them:

- `expansion_signal_type`: limit_proximity | feature_gate | growth_velocity
- `expansion_signal_date`: when the signal was first detected
- `expansion_qualified`: yes | no | pending
- `expansion_disqualify_reason`: text field for documenting why an account was skipped

### 3. Enrich with firmographic data

Using `clay-company-search` and `clay-people-search`, pull:

- Company size and growth trajectory (is headcount increasing?)
- Recent funding or revenue signals (do they have budget to expand?)
- Technology stack (are they using complementary tools that suggest sophistication?)
- Decision-maker contact info (who can authorize a plan upgrade?)

For Smoke level, this step can be done manually via LinkedIn and the company website. For Baseline+, automate via Clay tables.

### 4. Apply qualification criteria

Score each account against these qualification gates:

**Must-have (all required):**
- MRR >= $100 (below this, self-serve is more efficient)
- Active for >= 30 days (exclude new accounts still onboarding)
- No active expansion deal in CRM (avoid duplicate outreach)
- No critical support tickets open (fix problems before asking for money)

**Scoring (sum of applicable points):**
- At 95%+ of a limit: +30 points (critical urgency)
- At 85-94% of a limit: +20 points (imminent)
- At 70-84% of a limit: +10 points (approaching)
- Multiple resources near limits: +15 points per additional resource
- Usage velocity increasing (consumption rate grew 20%+ in last 30 days): +15 points
- Team size growing (seats added in last 60 days): +10 points
- High engagement (daily active usage): +10 points
- Enterprise firmographics (100+ employees or funded): +10 points
- Admin visited billing page in last 14 days: +20 points (active buying intent)

**Qualification tiers:**
- **Sales-ready (60+ points):** Immediate outreach. This account needs a conversation.
- **Nurture (30-59 points):** Add to expansion watch list. Monitor for score increase.
- **Self-serve (<30 points):** Route to automated upgrade prompts, not sales outreach.

### 5. Create qualified expansion opportunities

For accounts scoring 60+ points, create expansion deals in Attio using `attio-deals`:

- Deal title: "Usage Expansion — {{companyName}} — {{resource_type}}"
- Stage: "Expansion Qualified"
- Value: estimated expansion ARR (calculate from next tier price minus current)
- Context notes: which limits are being hit, current usage numbers, consumption velocity, firmographic highlights, decision-maker info
- Assigned to: account owner, or founder if no owner assigned

Using `attio-lists`, add to the "Expansion Pipeline — Usage Triggered" list.

### 6. Document disqualifications

For accounts that do not qualify, log the reason in Attio using `attio-custom-attributes`:

- Set `expansion_qualified` to "no"
- Set `expansion_disqualify_reason` with specific reasoning (e.g., "MRR $20 — route to self-serve", "Active support tickets — revisit after resolution", "Already in expansion deal EXP-0042")

This prevents re-qualifying the same accounts and builds a dataset to refine qualification criteria over time.

## Output

- A qualified list of expansion-ready accounts with deal context and decision-maker info
- Expansion deals created in Attio for sales-ready accounts
- Disqualified accounts documented with reasoning
- Attio list "Expansion Pipeline — Usage Triggered" populated

## Triggers

Run manually at Smoke level (once per week, or on demand when reviewing expansion signals). At Baseline+, this qualification logic is embedded in the automated detection pipeline.
