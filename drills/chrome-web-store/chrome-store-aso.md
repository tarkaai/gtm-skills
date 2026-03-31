---
name: chrome-store-aso
description: App Store Optimization for Chrome Web Store — keyword research, listing copy testing, and conversion rate optimization
category: Chrome Web Store
tools:
  - Chrome Web Store
  - PostHog
  - n8n
fundamentals:
  - chrome-web-store-listing-optimization
  - chrome-web-store-api
  - posthog-custom-events
  - n8n-scheduling
---

# Chrome Store ASO (App Store Optimization)

This drill systematically optimizes a Chrome Web Store listing for search visibility and install conversion rate. It covers keyword research, listing copy iteration, screenshot optimization, and performance tracking.

## Input

- Published Chrome extension with at least 2 weeks of listing data
- Access to Chrome Web Store Developer Dashboard
- PostHog tracking configured for extension events
- List of competitor extensions in the same category

## Steps

### 1. Keyword research

Identify the search terms your ICP uses to find extensions:

1. Search the Chrome Web Store for 10-15 candidate terms related to your problem space
2. For each term, record: number of results, top 3 extensions by position, their titles and short descriptions
3. Identify underserved keywords — terms with meaningful search intent but fewer than 50 competing extensions
4. Cross-reference with Google Trends: compare search volume between alternative phrasings (e.g., "tab manager" vs "tab organizer" vs "tab grouper")
5. Rank keywords by: relevance to your ICP (high/medium/low) x competition level (high/medium/low)
6. Select 3 primary keywords and 5 secondary keywords

### 2. Optimize listing copy

Using the `chrome-web-store-listing-optimization` fundamental:

**Title (test every 2 weeks):**
- Version A: `[Primary Keyword] - [Brand]`
- Version B: `[Brand]: [Primary Keyword]`
- Version C: `[Primary Keyword] [Modifier] - [Brand]` (modifier = "Pro", "AI", "Smart", etc.)

**Short description (test every 2 weeks):**
- Lead with user benefit, not feature
- Include primary and one secondary keyword
- A/B test by publishing one version for 2 weeks, measuring CTR, then switching

**Detailed description:**
- Use all primary and secondary keywords naturally in the first 2 paragraphs
- Structure: problem → solution → features → use cases → privacy
- Update monthly based on user reviews (address common questions in the description)

### 3. Screenshot optimization

Create 3-5 screenshots (1280x800):
- Screenshot 1: Hero shot — the extension solving the user's problem (this appears in search results)
- Screenshot 2: Key feature demonstration
- Screenshot 3: Before/after comparison (if applicable)
- Screenshot 4: Settings or customization options
- Screenshot 5: Social proof or user count (if available)

Test screenshot sets by swapping the hero screenshot every 2 weeks and comparing install rate.

### 4. Competitor monitoring

Set up an n8n workflow using `n8n-scheduling` to run weekly:
1. Scrape the Chrome Web Store search results for your primary keywords
2. Record your position and the top 5 competitors' positions
3. Track competitor listing changes (new screenshots, description updates, version bumps)
4. Alert if your ranking drops by 3+ positions for any primary keyword
5. Log competitive intelligence in Attio

### 5. Conversion tracking

Using `posthog-custom-events`, build a tracking model:
- Log listing changes as PostHog events: `listing_updated` with properties: `element_changed` (title, description, screenshots), `old_value`, `new_value`, `change_date`
- After each change, compare 2-week pre/post metrics: impressions, CTR (visits/impressions), install rate (installs/visits)
- Build a changelog in Attio linking each listing change to its measured impact

### 6. Review management

- Respond to every user review within 24 hours (responding improves CWS ranking)
- For negative reviews: acknowledge the issue, state what you are doing about it, ask for follow-up
- For positive reviews: thank the user, ask if they would share in their network
- Track review sentiment over time as a PostHog event: `review_received` with `rating` and `sentiment` properties
- Never incentivize reviews on the Chrome Web Store (violates CWS policy)

## Output

- Keyword-optimized listing copy with tracked versions
- Competitor position tracking running on weekly schedule
- Screenshot test results with install rate impact
- Review response workflow
- A changelog mapping every listing change to its metric impact

## Triggers

Run at Scalable level. Continue keyword and competitor monitoring at Durable level (feeds into `autonomous-optimization`).
