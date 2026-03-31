---
name: conference-cfp-search
description: Discover open call-for-papers (CFP) at developer conferences and meetups via web scraping and CFP aggregator APIs
tool: Clay
difficulty: Config
---

# Conference CFP Search

Find open call-for-papers (CFP) at developer conferences, meetups, and community events. This fundamental feeds the `conference-cfp-pipeline` drill with a structured list of speaking opportunities.

## Authentication

- Clay account with Claygent credits
- Optional: Sessionize API access (if managing speaker profiles)

## Method 1: Claygent Web Scraping (Recommended)

1. **Create a Clay table** with seed columns: topic keywords (e.g., "AI agents", "developer tools", "LLMs"), target regions, and date range.

2. **Add a Claygent column** to discover open CFPs:
   ```
   Search the web for open call-for-papers (CFP) at developer conferences
   and tech meetups related to {Topic Keyword} in the next 120 days.
   Check these sources:
   - confs.tech
   - papercall.io/cfps
   - sessionize.com/explore
   - dev.events
   - cfpland.com
   - GitHub repos that aggregate CFPs (e.g., github.com/scraly/developers-conferences-agenda)
   For each open CFP found, return:
   - Conference name
   - Conference date
   - CFP deadline
   - Location (city or "Remote")
   - Expected audience size
   - Conference URL
   - CFP submission URL
   - Topics/tracks accepted
   Format as JSON array.
   ```

3. **Parse the output** using Clay's JSON extraction column to split multi-CFP results into rows.

4. **Enrich each CFP** with a second Claygent column:
   ```
   Visit {CFP URL} and extract:
   - Talk format options (lightning, standard, workshop)
   - Talk length (minutes)
   - Whether they cover speaker travel/hotel
   - Past speaker list (if available)
   - Estimated audience size per talk
   - Selection criteria or review process description
   - Whether they accept first-time speakers
   ```

## Method 2: Papercall.io Scraping

Papercall.io has no public API but its event listing is scrapable:

1. **Scrape** `https://www.papercall.io/cfps` filtered by category
2. **Extract**: event name, CFP deadline, event date, location, and submission link
3. Each listing links to the full CFP with format details and topic tracks

## Method 3: Sessionize (for managed speaker profiles)

If using Sessionize to manage your speaker profile:

1. **Browse** `https://sessionize.com/explore` for open CFPs
2. **Submit** talks directly through the Sessionize speaker profile, which pre-fills bio and photo
3. **Track** submission status via Sessionize dashboard

## Output Format

Each discovered CFP should be stored as a row with these fields:

| Field | Description |
|-------|-------------|
| `conference_name` | Full conference name |
| `conference_date` | Event start date (ISO 8601) |
| `cfp_deadline` | Submission deadline (ISO 8601) |
| `location` | City or "Remote" |
| `expected_audience` | Number or range |
| `conference_url` | Main conference page |
| `cfp_url` | Direct submission link |
| `talk_formats` | Array: lightning, standard, workshop |
| `covers_travel` | Boolean or "partial" |
| `topics_accepted` | Array of track/topic names |
| `accepts_first_time` | Boolean |
| `relevance_score` | 0-100 based on topic and audience overlap with ICP |

## Error Handling

- If Claygent returns stale CFPs (deadline already passed), filter by `cfp_deadline > today`
- If a CFP URL is dead, flag the row and skip enrichment
- Rate-limit Claygent queries: batch 15-20 CFPs at a time
- Papercall listings refresh weekly; re-run scrape every 7 days to catch new CFPs
