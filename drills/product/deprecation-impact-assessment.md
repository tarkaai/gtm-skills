---
name: deprecation-impact-assessment
description: Analyze feature usage data to quantify deprecation blast radius, identify affected user segments, and produce a risk-scored deprecation brief
category: Product
tools:
  - PostHog
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-funnels
  - posthog-retention-analysis
  - attio-contacts
  - attio-custom-attributes
---

# Deprecation Impact Assessment

This drill quantifies the impact of deprecating a feature before any communication goes out. It answers three questions: how many users rely on this feature, how heavily they rely on it, and what will they lose if it disappears without a migration path. The output is a risk-scored deprecation brief that drives every downstream decision.

## Input

- The feature to be deprecated (name, PostHog event names associated with it)
- PostHog tracking active for at least 30 days covering the feature's events
- Attio CRM with user/company records

## Steps

### 1. Identify all users of the deprecated feature

Using the `posthog-cohorts` fundamental, create a cohort of users who have triggered the feature's events in the last 90 days. Query via HogQL:

```sql
SELECT
  person_id,
  count() AS feature_uses_90d,
  count() / 13 AS weekly_avg,
  dateDiff('day', max(timestamp), now()) AS days_since_last_use,
  min(timestamp) AS first_use_ever
FROM events
WHERE event IN ('{feature_event_1}', '{feature_event_2}')
  AND timestamp > now() - interval 90 day
GROUP BY person_id
HAVING feature_uses_90d >= 1
ORDER BY feature_uses_90d DESC
```

Store this as a PostHog cohort: `deprecation-blast-radius-{feature_slug}`.

### 2. Classify user dependency tiers

Segment the cohort into dependency levels based on usage intensity:

| Tier | Criteria | Risk Level |
|------|----------|------------|
| Power dependents | Weekly avg >= 10 uses AND used in last 7 days | Critical |
| Regular dependents | Weekly avg 3-9 uses AND used in last 14 days | High |
| Occasional users | Weekly avg 1-2 uses AND used in last 30 days | Medium |
| Lapsed users | No use in last 30 days but used in last 90 days | Low |

Using `posthog-cohorts`, create a sub-cohort for each tier. These cohorts will drive segmented communication later.

### 3. Assess alternative feature overlap

Using `posthog-funnels`, check whether power and regular dependents also use the replacement feature (if one exists). Build a funnel:

```
deprecated_feature_used -> replacement_feature_used (within 30 days)
```

If overlap is high (>50% already use both), migration friction will be low. If overlap is low (<20%), expect resistance and plan heavier migration support.

### 4. Calculate revenue exposure

Using `attio-contacts`, pull the subscription tier and MRR for each affected user. Sum the MRR by dependency tier:

- Critical tier total MRR: $X
- High tier total MRR: $X
- Medium tier total MRR: $X
- Low tier total MRR: $X

This quantifies the revenue at risk if migration fails. If critical + high tier MRR exceeds 5% of total MRR, escalate the deprecation timeline and increase migration support resources.

### 5. Map feature workflows

Using `posthog-custom-events`, trace what users do immediately before and after using the deprecated feature. This reveals the workflows the feature is embedded in:

```sql
SELECT
  event AS next_action,
  count() AS frequency
FROM events
WHERE person_id IN (SELECT person_id FROM cohort WHERE name = 'deprecation-blast-radius-{feature_slug}')
  AND timestamp > (
    SELECT max(timestamp) FROM events
    WHERE event = '{deprecated_feature_event}'
      AND person_id = events.person_id
  )
  AND timestamp < (
    SELECT max(timestamp) + interval 5 minute FROM events
    WHERE event = '{deprecated_feature_event}'
      AND person_id = events.person_id
  )
GROUP BY event
ORDER BY frequency DESC
LIMIT 10
```

Understanding these workflows is essential for designing migration paths that preserve the user's end-to-end process, not just replace one button with another.

### 6. Store assessment in CRM

Using `attio-custom-attributes`, tag each affected user's record with:

- `deprecation_{feature_slug}_tier`: critical | high | medium | low
- `deprecation_{feature_slug}_weekly_avg`: their usage frequency
- `deprecation_{feature_slug}_assessed_date`: timestamp

Using `attio-contacts`, create tasks for account owners of critical-tier users so they can plan personal outreach.

### 7. Produce the deprecation brief

Generate a structured brief containing:

- **Total affected users:** count by tier
- **Revenue at risk:** MRR by tier
- **Replacement overlap:** percentage already using the alternative
- **Workflow dependencies:** top 5 workflows the feature appears in
- **Recommended deprecation timeline:** based on risk (critical tier > 10 users = minimum 90 days notice; otherwise 30-60 days)
- **Migration complexity score:** 1-5 based on workflow depth and replacement overlap

Store the brief as an Attio note on the product record.

## Output

- Four PostHog cohorts (one per dependency tier) for the deprecated feature
- Revenue exposure calculation by tier
- Workflow dependency map
- Attio records tagged with deprecation tier and usage data
- A structured deprecation brief with timeline recommendation and complexity score

## Triggers

Run once when a deprecation decision is made. Re-run if the deprecation timeline extends beyond 90 days (usage patterns may shift).
