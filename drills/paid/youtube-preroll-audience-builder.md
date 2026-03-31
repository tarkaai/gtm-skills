---
name: youtube-preroll-audience-builder
description: Build YouTube video campaign audiences using channel placements, custom intent segments, topic targeting, and affinity layers via Google Ads API
category: Paid
tools:
  - Google Ads
  - YouTube Data API
  - Clay
  - Attio
  - SparkToro
fundamentals:
  - google-ads-youtube-audience-targeting
  - google-ads-youtube-reporting
  - youtube-data-api-metadata
  - clay-people-search
  - clay-scoring
  - attio-lists
---

# YouTube Pre-roll Audience Builder

Build targeted audiences for YouTube pre-roll ad campaigns. YouTube targeting differs fundamentally from LinkedIn/Meta: you target by what people watch (placements, topics) and what they search (custom intent), not by firmographic data. This means your ICP research must translate into content consumption patterns.

## Prerequisites

- Google Ads account with Video campaign capabilities
- YouTube Data API access (for channel discovery)
- ICP document with known pain points, job titles, and industry
- Attio CRM with customer data for Customer Match

## Input

- ICP definition: who are these people, what problems do they face, and what content do they consume on YouTube
- Competitor list: which companies advertise on YouTube or have YouTube channels your ICP watches
- Pain points: 2-3 specific problems your ICP is dealing with (these become custom intent keywords)

## Steps

### 1. Map your ICP to YouTube consumption patterns

YouTube does not have job title or company size targeting. You must infer ICP fit from content behavior. For each ICP attribute, identify the YouTube equivalent:

| ICP Attribute | YouTube Signal |
|---|---|
| VP/Director Engineering | Watches channels like Fireship, ThePrimeagen, Continuous Delivery, tech conference talks |
| SaaS companies 20-200 | Watches SaaStr talks, startup-focused tech channels, Y Combinator |
| Cares about data quality | Searches "data pipeline monitoring", "ETL best practices", watches data engineering channels |
| Series A-C funded | Watches fundraising content, startup scaling talks (less reliable; use as additive, not primary) |

Build a "content map" of your ICP: 20-50 YouTube channels and 20-30 search terms they likely use.

### 2. Discover placement targets

Use the YouTube Data API via `youtube-data-api-metadata` to search for channels related to your ICP's pain points:

```
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &type=channel
  &q=data engineering tutorial
  &maxResults=50
  &key={API_KEY}
```

For each returned channel, pull subscriber count and recent upload frequency:

```
GET https://www.googleapis.com/youtube/v3/channels
  ?part=statistics,contentDetails
  &id={CHANNEL_ID}
  &key={API_KEY}
```

Filter channels by:
- Subscriber count: 10,000-2,000,000 (large enough for reach, small enough to be niche)
- Upload frequency: at least 2 videos/month (active channel, not abandoned)
- Content relevance: manually verify 3-5 recent videos are relevant to your ICP's pain points

**Also use SparkToro** (if available) to find YouTube channels your audience follows. Input your ICP's job titles or industry terms and export the "frequently visited YouTube channels" list.

Compile a final placement list:
- **Smoke:** 20-50 channels, hand-verified
- **Baseline:** 50-100 channels + 20 specific high-performing video placements
- **Scalable:** 100-200 channels, auto-discovered via the YouTube Data API + agent curation

### 3. Build custom intent segments

Custom intent audiences target people who recently searched specific terms on Google. This is the most powerful B2B targeting on YouTube because you reach people actively researching the problem.

Create 2-3 custom intent segments using `google-ads-youtube-audience-targeting`:

**Segment A — Direct problem searchers:**
Keywords: the exact terms someone types when experiencing the pain point.
- "data pipeline keeps failing"
- "ETL job monitoring"
- "data quality issues production"
- "how to fix broken data sync"
- "data pipeline maintenance time"

**Segment B — Solution researchers:**
Keywords: terms someone types when starting to look for solutions (still problem-aware, not brand-aware).
- "best data pipeline tools 2026"
- "ETL tool comparison"
- "data integration platform features"
- "automated data quality monitoring"
- "data pipeline orchestration"

**Segment C — Competitor researchers (optional at Baseline+):**
Keywords: competitor brand names + category terms.
- "[competitor name] alternative"
- "[competitor name] pricing"
- "[competitor name] vs"

Each segment should contain 10-15 keywords. Google will expand them. Fewer, more precise keywords outperform long keyword lists.

### 4. Layer topic targeting

Add topic targeting as a broadening layer alongside placements:

Relevant B2B tech topics:
- Computers & Electronics > Software > Business & Productivity Software
- Business & Industrial > Business Services > IT Services
- Computers & Electronics > Software > Development Tools

Use `google-ads-youtube-audience-targeting` to find topic constant IDs and attach them to ad groups.

Topic targeting runs in a separate ad group from placement targeting so you can measure performance independently.

### 5. Configure demographic exclusions

YouTube supports basic demographics. Exclude segments unlikely to be B2B decision-makers:
- Exclude AGE_RANGE_18_24 (very few B2B buyers in this range)
- Exclude PARENTAL_STATUS_UNDETERMINED only if your audience is very narrow and you need to conserve budget

### 6. Set up audience exclusions

Using `attio-lists`, export:
- Current customers (by email). Upload as a Customer Match list to Google Ads. Exclude from all campaigns.
- Recent converters (people who filled out your lead form in the last 30 days). Exclude to avoid annoying them.
- Disqualified leads. Exclude to prevent wasted impressions.

Refresh exclusion lists weekly via n8n cron workflow.

### 7. Plan audience testing and rotation

Structure campaigns to isolate audience performance:
- **Campaign 1 — Placements:** Specific channel and video placements. Highest precision, lowest scale.
- **Campaign 2 — Custom Intent:** Search-based targeting. Medium precision, good scale.
- **Campaign 3 — Topics + Affinity:** Broadest targeting. Lower precision, highest scale.

Run Campaign 1 and 2 simultaneously at Smoke/Baseline. Add Campaign 3 at Scalable.

Track per-campaign metrics using `google-ads-youtube-reporting` to identify which audience type produces the best cost-per-qualified-lead, not just cheapest CPV.

## Output

- Placement list: 20-200 YouTube channel/video URLs organized by relevance tier
- 2-3 custom intent segments configured in Google Ads
- Topic targeting ad groups configured
- Exclusion lists uploaded and refresh schedule set
- Campaign structure isolating audience types for measurement
