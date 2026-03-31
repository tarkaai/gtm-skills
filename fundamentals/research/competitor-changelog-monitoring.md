---
name: competitor-changelog-monitoring
description: Monitor competitor product changes, pricing updates, and positioning shifts via web scraping and API-based change detection
tool: Clay + n8n
difficulty: Config
---

# Monitor Competitor Product Changes

Set up automated monitoring of competitor websites, changelogs, pricing pages, and public communications to detect product changes, pricing shifts, and positioning updates that affect your competitive positioning.

## Prerequisites

- Clay account with Claygent enabled (for web scraping)
- n8n instance for scheduling and alerting
- Attio CRM with Competitors object configured
- List of competitors to monitor (names, website URLs, changelog URLs, pricing page URLs)

## Method 1: Clay Claygent Web Scraping (Recommended)

### 1. Create a Clay table for competitor monitoring

Set up a Clay table with one row per competitor, columns:
- `competitor_name` (text)
- `changelog_url` (URL) — e.g., `https://competitor.com/changelog` or `https://competitor.com/blog/category/product-updates`
- `pricing_url` (URL) — e.g., `https://competitor.com/pricing`
- `features_url` (URL) — e.g., `https://competitor.com/features`
- `last_changelog_hash` (text) — SHA-256 of last scraped changelog content
- `last_pricing_hash` (text) — SHA-256 of last scraped pricing content
- `last_checked` (date)

### 2. Add Claygent scraping columns

For each URL type, add a Claygent column with the prompt:

**Changelog scraper:**
```
Visit {changelog_url} and extract the 5 most recent product updates. For each update, return:
- Date
- Title/headline
- Summary (1-2 sentences)
- Category: feature_launch | improvement | deprecation | integration | pricing_change
Return as JSON array.
```

**Pricing scraper:**
```
Visit {pricing_url} and extract the current pricing structure. Return:
- Plan names and prices (monthly and annual)
- Key feature differences between plans
- Any free tier details
- Enterprise pricing (if listed or "contact sales")
Return as JSON.
```

### 3. Set up change detection in n8n

Create an n8n workflow triggered by cron (daily or weekly):

1. Pull current Clay scrape results for each competitor
2. Hash the content and compare against `last_changelog_hash` / `last_pricing_hash`
3. If hash differs: a change was detected
4. Send the diff to Claude for analysis:

```json
{
  "prompt": "Compare these two versions of a competitor's changelog/pricing page. What changed? Classify the change as: new_feature | price_increase | price_decrease | plan_restructure | feature_deprecation | messaging_shift. Rate the competitive impact on a scale of 1-5 (1 = irrelevant, 5 = major threat). Return JSON.",
  "previous": "{previous_content}",
  "current": "{current_content}"
}
```

5. If competitive_impact >= 3, send Slack alert and create Attio note on the Competitor record
6. Update the hash columns in Clay

## Method 2: RSS/Atom Feed Monitoring

Many competitors publish changelogs as RSS feeds:

1. Discover RSS feeds: Check `{competitor_url}/feed`, `{competitor_url}/rss`, `{competitor_url}/blog/feed`
2. In n8n, use the RSS Read node to poll each feed on a cron schedule
3. For each new entry, classify using Claude and alert if relevant

## Method 3: Review Site Monitoring

Monitor G2, Capterra, and TrustRadius for competitor reviews and feature mentions:

1. Use Clay to scrape the competitor's G2 profile page monthly
2. Extract: overall rating, recent review count, category rankings, recently mentioned features
3. Compare month-over-month for changes
4. Track competitor rating trends in PostHog

## Method 4: Social Listening

Monitor competitor mentions on LinkedIn and Twitter:

1. Use Clay's LinkedIn company search to check competitor company pages for product announcements
2. Set up n8n to poll for competitor name mentions using social listening APIs (Mention, Brand24, or Twitter API search)
3. Classify mentions as: product_launch | customer_win | partnership | hiring_signal | negative_press

## Output

For each detected change, produce:
```json
{
  "competitor_name": "...",
  "change_type": "new_feature|price_change|messaging_shift|deprecation",
  "change_summary": "...",
  "competitive_impact": 1-5,
  "our_positioning_affected": true/false,
  "recommended_action": "update_battlecard|no_action|escalate_to_team|test_new_positioning",
  "detected_date": "...",
  "source_url": "..."
}
```

Store in Attio on the Competitor record. Fire PostHog event: `competitor_change_detected`.

## Error Handling

- **Scrape fails (page structure changed):** Log error, alert team to update scrape prompt. Do not treat missing data as "no changes."
- **Rate limited by competitor site:** Reduce scraping frequency. Weekly is sufficient for most competitors.
- **False positive (page changed but content is same):** Improve hash to normalize whitespace and timestamps before hashing.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay + Claygent | Web scraping with AI interpretation | Most flexible, handles any website |
| Crayon | Purpose-built competitive intelligence | Auto-tracks competitor web changes, pricing, content. $15K+/yr |
| Klue | Competitive enablement platform | Battlecard management + change tracking. Enterprise pricing |
| Kompyte (Semrush) | Automated competitive tracking | Website change detection + content analysis |
| Visualping | Simple webpage change detection | Budget option, no AI analysis. Free tier available |
| Diffbot | Structured web data extraction | API-based, good for consistent page structures |
| Manual | Weekly competitor review | Fallback, time-intensive but reliable |
