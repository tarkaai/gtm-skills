---
name: clay-intent-scoring
description: Build a weighted intent scoring model in Clay that combines first-party and third-party signals into a single priority score
tool: Clay
difficulty: Config
---

# Clay Intent Scoring

Build a composite intent score in Clay that merges multiple signal sources (website visits, G2 research, job changes, funding, hiring) into a single numeric priority score. This score drives outreach prioritization — higher scores get contacted first and with more personalized messaging.

## Prerequisites

- Clay account with Explorer plan or above ($149+/mo for AI enrichment columns)
- At least one intent signal source configured (website visitor ID tool, G2, Bombora, or manual signal tracking)
- Target account list loaded in Clay

## Setup

### 1. Create the scoring table

Using the Clay UI or API, create a new table with these columns:

| Column | Type | Source |
|--------|------|--------|
| company_domain | Text | Import |
| company_name | Text | Enrichment |
| contact_email | Text | Enrichment |
| contact_title | Text | Enrichment |
| website_visits_30d | Number | Visitor ID webhook |
| pricing_page_viewed | Boolean | Visitor ID webhook |
| g2_signal_type | Text | G2 webhook |
| g2_activity_level | Text | G2 webhook |
| bombora_surge_score | Number | Bombora API |
| recent_funding | Boolean | Clay enrichment |
| funding_amount | Number | Clay enrichment |
| new_exec_hire | Boolean | Clay enrichment |
| job_postings_count | Number | Clay enrichment |
| competitor_tech_used | Boolean | Clay enrichment |
| days_since_last_signal | Number | Computed |
| intent_score | Number | Formula |
| intent_tier | Text | Formula |

### 2. Configure signal ingestion

Set up Clay webhook columns or HTTP enrichment columns to pull data from your signal sources:

**Website visitor data** (via n8n webhook relay):
```
POST https://api.clay.com/v1/tables/TABLE_ID/rows
Authorization: Bearer CLAY_API_KEY
Content-Type: application/json

{
  "data": {
    "company_domain": "acme.com",
    "website_visits_30d": 5,
    "pricing_page_viewed": true
  },
  "match_on": "company_domain"
}
```

**G2 intent data** (via webhook or scheduled pull):
```
POST https://api.clay.com/v1/tables/TABLE_ID/rows
Authorization: Bearer CLAY_API_KEY
Content-Type: application/json

{
  "data": {
    "company_domain": "acme.com",
    "g2_signal_type": "alternatives",
    "g2_activity_level": "high"
  },
  "match_on": "company_domain"
}
```

### 3. Build the scoring formula

Create a formula column `intent_score` using Clay's formula editor. The scoring model:

```
// Signal weights (total = 100)
website_score = min(website_visits_30d * 5, 25)                    // max 25 pts
pricing_page_bonus = pricing_page_viewed ? 15 : 0                  // 15 pts
g2_score = g2_activity_level == "high" ? 20 : (g2_activity_level == "medium" ? 10 : 0)  // max 20 pts
bombora_score = min(bombora_surge_score * 0.2, 15)                 // max 15 pts
funding_score = recent_funding ? 10 : 0                            // 10 pts
hiring_score = min(job_postings_count * 2, 10)                     // max 10 pts
exec_hire_score = new_exec_hire ? 5 : 0                            // 5 pts

// Decay: signals lose value over time
decay_multiplier = days_since_last_signal <= 7 ? 1.0 :
                   days_since_last_signal <= 14 ? 0.85 :
                   days_since_last_signal <= 30 ? 0.6 : 0.3

raw_score = website_score + pricing_page_bonus + g2_score + bombora_score + funding_score + hiring_score + exec_hire_score
intent_score = round(raw_score * decay_multiplier)
```

### 4. Build the tier formula

Create a formula column `intent_tier`:

```
intent_tier = intent_score >= 70 ? "Hot" :
              intent_score >= 40 ? "Warm" :
              intent_score >= 15 ? "Cool" : "Cold"
```

### 5. Validate the model

Pull your last 20 closed-won deals and score them retroactively. If fewer than 70% score "Hot" or "Warm," adjust weights. Pull your last 20 lost/stalled deals — if more than 50% score "Hot," the model is too generous. Tighten thresholds until there is clear separation between won and lost accounts.

## Updating Scores

Set up a Clay automation or n8n workflow to refresh scores:
- **Real-time**: Website visits and G2 signals update via webhooks as they arrive
- **Daily**: Recalculate `days_since_last_signal` and apply decay
- **Weekly**: Refresh Bombora surge scores, job posting counts, and funding data via scheduled Clay enrichment runs

## Error Handling

- **Missing signals**: If a signal source is not configured (e.g., no Bombora), set that component to 0. The model still works with fewer signals but with less precision.
- **Score inflation**: If too many accounts score Hot, raise thresholds or reduce weights on high-frequency signals like website visits.
- **Stale data**: The decay multiplier prevents old signals from inflating scores. If an account was Hot 60 days ago but has gone silent, the score drops to near-zero.
- **Credit costs**: Each Clay enrichment row costs credits. Budget approximately 5-10 credits per row for full enrichment. At $149/mo (Explorer), you get ~2,400 credits/mo — enough for ~250-480 accounts.
