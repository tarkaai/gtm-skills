---
name: partner-relationship-scoring
description: Score and rank connector relationships by intro quality, responsiveness, and deal conversion to optimize partner portfolio
category: Partnerships
tools:
  - Attio
  - PostHog
  - n8n
fundamentals:
  - attio-automation
  - attio-contacts
  - attio-notes
  - posthog-custom-events
  - n8n-scheduling
---

# Partner Relationship Scoring

This drill builds a scoring system that ranks your connectors (advisors, angels, partners, customers) by their actual value as warm intro sources. It prevents wasted time on low-yield relationships and focuses attention on connectors who reliably produce meetings.

## Input

- Attio records for all connectors with intro request history
- PostHog tracking for warm intro events (requests, intros, meetings, deals)
- At least 8 weeks of intro data across 5+ connectors

## Steps

### 1. Define the scoring dimensions

Score each connector on 5 dimensions (each 1-10 scale, 50 max):

**Response Rate (1-10):** What percentage of intro requests does this connector act on?
- 10: >80% of requests result in an intro
- 7: 50-80%
- 4: 20-50%
- 1: <20%

**Intro Quality (1-10):** What percentage of intros convert to meetings?
- 10: >75% of intros convert to meetings
- 7: 50-75%
- 4: 25-50%
- 1: <25%

**Deal Conversion (1-10):** What percentage of meetings from this connector's intros advance past discovery?
- 10: >60% advance to proposal
- 7: 40-60%
- 4: 20-40%
- 1: <20%

**Response Speed (1-10):** How quickly does the connector make the intro after being asked?
- 10: Within 24 hours
- 7: 2-3 days
- 4: 4-7 days
- 1: >7 days or needs multiple follow-ups

**Volume Capacity (1-10):** How many intros can this connector realistically provide per quarter?
- 10: 10+ intros/quarter
- 7: 5-9 intros/quarter
- 4: 2-4 intros/quarter
- 1: 1 intro/quarter

### 2. Build the scoring automation in n8n

Using the `n8n-scheduling` fundamental, create a monthly workflow (1st of each month):

1. Query Attio for all connector records with intro activity in the last 90 days
2. For each connector, pull PostHog data:
   - Count of `warm_intro_request_sent` events where `partner_name` = connector
   - Count of `warm_intro_received` events where `partner_name` = connector
   - Count of `meeting_booked` events where `source = warm_intro` and `partner_name` = connector
   - Count of `deal_created` events where `source = warm_intro` and `partner_name` = connector
   - Average time between `warm_intro_request_sent` and `warm_intro_received` for this connector
3. Calculate scores for each dimension using the thresholds above
4. Compute the composite score (sum of 5 dimensions, max 50)
5. Write scores back to Attio connector records using `attio-automation`

### 3. Classify connectors into tiers

Based on composite score:

- **Tier 1 (40-50):** Elite connectors. Prioritize their relationship. Send them the best prospects to introduce. Thank them proactively. Never let an ask sit without follow-up.
- **Tier 2 (25-39):** Good connectors. Reliable but room to improve. Analyze which dimension is weakest and address it (better ask framing, different prospect types, relationship deepening).
- **Tier 3 (10-24):** Low-yield connectors. Reduce request frequency. Only ask for their strongest connections. Consider whether the relationship needs investment or should be deprioritized.
- **Tier 4 (1-9):** Ineffective connectors. Stop sending intro requests. Move relationship to general network nurture only.

### 4. Configure Attio fields for scoring

Using the `attio-contacts` fundamental, add these fields to connector records:

- `connector_score`: Number (0-50) — composite score
- `connector_tier`: Select (Tier 1 / Tier 2 / Tier 3 / Tier 4)
- `score_response_rate`: Number (1-10)
- `score_intro_quality`: Number (1-10)
- `score_deal_conversion`: Number (1-10)
- `score_response_speed`: Number (1-10)
- `score_volume_capacity`: Number (1-10)
- `last_scored_date`: Date
- `score_trend`: Select (Improving / Stable / Declining)

### 5. Build trend detection

Using the `posthog-custom-events` fundamental, log each monthly scoring as a `connector_scored` event with all dimension scores. Over time, this shows:

- Which connectors are improving (invest more)
- Which connectors are declining (investigate why — relationship cooling, job change, network fatigue)
- Seasonal patterns (some connectors are more active in certain quarters)

Compare current month score to 3-month average. If the score dropped >20%, mark the connector as "Declining" and flag for investigation.

### 6. Generate monthly portfolio report

Using the `attio-notes` fundamental, create a monthly note on your master partnerships record:

```
## Connector Portfolio Report — {month}

**Active connectors**: {count}
**Tier 1**: {count} ({names})
**Tier 2**: {count}
**Tier 3**: {count}
**Tier 4**: {count} (recommended for removal)

### Score changes
- {connector} improved from {old_score} to {new_score} (moved from Tier 3 to Tier 2)
- {connector} declined from {old_score} to {new_score} — investigate

### Pipeline from connectors this month
- Total intros: {count}
- Total meetings: {count}
- Total deals created: {count}
- Estimated pipeline value: ${amount}

### Recommended actions
1. Promote {connector} to Tier 1 outreach cadence
2. Reduce asks to {connector} (declining scores)
3. Recruit new connectors in {industry} (gap in current portfolio)
```

## Output

- Scored and tiered connector records in Attio
- Monthly scoring automation via n8n
- Trend detection for relationship health
- Monthly portfolio report with actionable recommendations
- Data feed for the `autonomous-optimization` drill to optimize connector selection and ask strategies

## Triggers

Run the full scoring once at the start of Durable level to establish baselines. Scoring automation runs monthly. Portfolio report generates on the 1st of each month.
