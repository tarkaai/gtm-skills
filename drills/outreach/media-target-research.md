---
name: media-target-research
description: Find, qualify, and rank journalists, newsletter editors, and podcast hosts for earned media pitching
category: Media
tools:
  - Muck Rack
  - BuzzSumo
  - ListenNotes
  - Clay
  - Attio
fundamentals:
  - media-database-search
  - podcast-directory-search
  - podcast-host-enrichment
  - clay-table-setup
  - clay-enrichment-waterfall
  - attio-lists
---

# Media Target Research

This drill builds a qualified, enriched list of media targets -- journalists, newsletter editors, and podcast hosts -- for earned media outreach. It combines database search, competitor coverage analysis, and contact enrichment into a pipeline that outputs a ready-to-pitch list segmented by outlet type and priority tier.

## Input

- Company description: what you do, your key differentiators, and why it matters
- ICP definition: who your customers are (industry, company size, job titles)
- 3-5 pitch angles: specific story ideas the founder can speak to (data-driven takes, contrarian views, unique experiences)
- 2-3 competitor company names (for cross-reference search)
- Target count: 10 for Smoke, 25 for Baseline, 75+ for Scalable

## Steps

### 1. Map the media landscape

Before searching databases, define three media target categories:

**Tier 1 -- Trade publications and industry blogs:**
Publications that your ICP reads daily. For B2B SaaS, this might be: SaaStr blog, First Round Review, Lenny's Newsletter, The Hustle, TechCrunch Startups, Product Hunt daily digest. These drive high-intent referral traffic because the audience matches your buyer.

**Tier 2 -- Micro-newsletters and niche podcasts:**
Smaller outlets (1K-25K subscribers/listeners) focused on your specific vertical. These are easier to land and often have highly engaged audiences. Search Substack, Beehiiv, and ListenNotes for your topic keywords.

**Tier 3 -- General business and tech media:**
Broader outlets (Hacker News, Axios, The Information, Forbes contributor network). Harder to land but high reach. Target these at Scalable level with data-driven stories.

### 2. Search journalist databases

Use `media-database-search` to run keyword searches:

**Search 1 -- Beat match:** Search for journalists covering your industry vertical (e.g., "B2B SaaS", "developer tools", "AI startups"). Filter to active journalists who published in the last 30 days.

**Search 2 -- Topic match:** Search for journalists who recently wrote about problems your product solves (e.g., "customer acquisition cost", "sales automation", "product-led growth"). These are the highest-intent targets -- they are actively reporting on your topic.

**Search 3 -- Competitor coverage:** Search for articles mentioning your competitors by name. Extract the journalist names. These writers already cover your space and may want a competing perspective or alternative to feature.

### 3. Search newsletter databases

Manually search for newsletters covering your vertical:

1. Substack: `https://substack.com/search/{topic}` -- browse top results by subscriber count
2. Beehiiv Discover: `https://www.beehiiv.com/discover` -- search by category
3. Newsletter databases: SparkLoop, Letterhead, newsletter.directory
4. Google: `"{topic}" newsletter subscribe site:substack.com OR site:beehiiv.com`

For each newsletter found, record: name, editor name, subscriber count (if visible), publishing frequency, whether they accept external pitches/guest posts, and contact info.

### 4. Search podcast databases

Use `podcast-directory-search` to find podcasts:

1. Keyword search for your topic on ListenNotes (listen_score >= 20)
2. Search for competitor founder names as episode guests
3. Verify each show accepts guest interviews

For each podcast, record: show name, host name, listen_score, last episode date, guest format confirmed, contact info.

### 5. Create and enrich the prospect table

Use `clay-table-setup` to create a Clay table called "Media Targets - {date}" with columns:

| Column | Type | Notes |
|--------|------|-------|
| contact_name | Text | Journalist, editor, or host name |
| outlet_name | Text | Publication, newsletter, or podcast name |
| outlet_type | Select | journalist / newsletter / podcast |
| beat_topics | Multi-select | Topics they cover |
| contact_email | Email | Primary contact |
| contact_twitter | URL | Twitter/X handle |
| contact_linkedin | URL | LinkedIn profile |
| recent_article_url | URL | Most recent relevant piece they published |
| recent_article_topic | Text | Summary of that piece (for pitch personalization) |
| audience_size | Number | Estimated reach (circulation, subscribers, listen_score) |
| relevance_score | Number 1-5 | How closely they cover your topics |
| accessibility_score | Number 1-5 | How easy it is to reach them (email = 5, form = 3, no info = 1) |
| competitor_covered | Boolean | Have they written about a competitor? |
| pitch_status | Select | not_pitched / pitched / responded / placed / declined |
| tier | Select | tier_1 / tier_2 / tier_3 |

Import all candidates from steps 2-4.

### 6. Enrich contacts

Run `clay-enrichment-waterfall` on the table:
- Email: Clay email finder > Hunter.io > Apollo > manual LinkedIn lookup
- Social: Extract Twitter and LinkedIn from Muck Rack or BuzzSumo author profiles
- Verify all emails before outreach (use Clay's built-in email verification or NeverBounce)

Run `podcast-host-enrichment` specifically for podcast rows: RSS feed email > Clay > Apollo > LinkedIn.

### 7. Score and rank

Calculate a composite score for each target:

- **Relevance** (40%): How closely does their coverage match your pitch angles?
- **Audience** (25%): Estimated reach (normalized to 1-5 scale within your list)
- **Accessibility** (20%): Verified email = 5, Twitter DM = 3, contact form = 2, no info = 1
- **Competitor coverage** (15%): Covered a competitor = +2 bonus. Actively covering the space = +1.

Sort by composite score. Assign tiers:
- Tier 1 (top 20%): Highest priority, maximum personalization
- Tier 2 (middle 50%): Standard personalization
- Tier 3 (bottom 30%): Template-based outreach at Scalable level

### 8. Push to Attio

Use `attio-lists` to create a list called "Media Targets - {date}". Push the ranked list from Clay with all enrichment data and scores. Tag each contact with their tier and outlet type.

## Output

- Scored, enriched list of media targets in Attio, segmented by outlet type and priority tier
- Contact info verified and ready for outreach
- Recent article references stored for pitch personalization
- Clear tier ranking for sequencing outreach efforts

## Triggers

- Run at the start of each play level
- Re-run monthly at Scalable/Durable to find new outlets and refresh stale contacts
- Re-run immediately when a major industry event creates new pitch opportunities
