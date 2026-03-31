---
name: guest-post-blog-discovery
description: Find, qualify, and rank industry blogs that accept guest posts using Ahrefs Content Explorer and Clay enrichment
category: GuestPosting
tools:
  - Ahrefs
  - Clay
  - Attio
fundamentals:
  - ahrefs-content-explorer
  - ahrefs-backlink-analysis
  - clay-table-setup
  - clay-enrichment-waterfall
  - attio-lists
---

# Guest Post Blog Discovery

This drill builds a qualified, scored list of blogs that accept guest posts in your niche. It combines Ahrefs Content Explorer searches with Clay enrichment to produce a tiered target list ready for pitch outreach.

## Input

- Company description and positioning
- ICP definition: who your customers are, what they read, what problems they search for
- 2-3 competitor company names (for cross-reference discovery)
- Target list size: 15 for Smoke, 50 for Baseline, 200 for Scalable
- Niche keywords: 5-10 terms your ICP would search (e.g., "sales automation", "cold email", "B2B marketing")

## Steps

### 1. Search for blogs with guest post pages

Using `ahrefs-content-explorer`, run multiple queries to cast a wide net:

**Query set 1 — Explicit guest post signals:**
- `"write for us" AND "{niche_keyword_1}"`
- `"guest post guidelines" AND "{niche_keyword_2}"`
- `"submit an article" AND "{niche_keyword_3}"`
- `"contribute" AND "guest" AND "{niche_keyword_4}"`
- `"become a contributor" AND "{niche_keyword_5}"`

Filter: `domain_rating >= 30` and `organic_traffic >= 500`.

**Query set 2 — Blogs that have published guest content:**
- `intitle:"guest post by" AND "{niche_keyword}"`
- `intitle:"guest author" AND "{niche_keyword}"`
- `"this is a guest post" AND "{niche_keyword}"`

These find blogs that already publish guest content, even if they lack a formal "write for us" page.

**Query set 3 — Competitor guest posts:**
- `"{competitor_founder_1}" -site:{competitor_domain_1}`
- `"{competitor_company_2}" AND "guest" -site:{competitor_domain_2}`

Find where competitors have placed guest posts. These blogs are high-probability targets.

Deduplicate results by domain. Keep a master list of unique blog domains.

### 2. Analyze each blog's profile

For each candidate blog domain, use `ahrefs-content-explorer` with `site:` queries to pull:
- Top-performing content (by organic traffic)
- Average word count of published articles
- Publishing frequency (estimate from `published_date` spread)
- Whether guest authors appear (check `author` field for non-staff names)

Use `ahrefs-backlink-analysis` to pull:
- Domain rating
- Total referring domains
- Organic traffic estimate

### 3. Create and enrich the prospect table in Clay

Use `clay-table-setup` to create a table called "Guest Post Targets - {date}" with columns:

| Column | Type | Notes |
|--------|------|-------|
| blog_domain | URL | Root domain of the blog |
| blog_name | Text | Publication or blog name |
| domain_rating | Number | From Ahrefs (0-100) |
| organic_traffic | Number | Monthly estimated organic traffic |
| guest_post_page_url | URL | Link to "write for us" or guidelines page |
| editor_name | Text | Editor or content manager name |
| editor_email | Email | Contact email for pitching |
| editor_linkedin | URL | LinkedIn profile |
| content_topics | Multi-select | Topics the blog covers |
| avg_word_count | Number | Typical article length |
| publishing_frequency | Select | daily / 2-3x_week / weekly / biweekly / monthly |
| accepts_guest_posts | Boolean | Confirmed via guidelines page or past guest posts |
| competitor_published | Boolean | Has a competitor published here? |
| recent_article_url | URL | Most relevant recent article for pitch personalization |
| recent_article_topic | Text | Summary of that article |
| relevance_score | Number 1-5 | How well blog audience matches your ICP |
| tier | Select | tier_1 / tier_2 / tier_3 |
| pitch_status | Select | not_pitched / pitched / accepted / declined / published |

Import all candidate blogs from step 1.

### 4. Enrich editor contacts

Run `clay-enrichment-waterfall` on the table:
- Editor email: Clay email finder > Hunter.io > Apollo > Scrape the blog's about/contact page
- Editor LinkedIn: Clay LinkedIn enrichment > manual search
- Verify all emails before outreach

For blogs where you cannot find an editor email: check the blog's contact page, about page, or the "write for us" page itself. Many list a specific submission email.

### 5. Score and tier the list

Calculate a composite score for each blog:

- **Domain Rating** (30%): Higher DR = more valuable backlink. Normalize to 1-5 scale (DR 30-39 = 1, DR 40-49 = 2, DR 50-59 = 3, DR 60-74 = 4, DR 75+ = 5)
- **Audience Relevance** (30%): How closely does the blog's readership match your ICP? Score 1-5 based on topic overlap with your niche keywords.
- **Traffic** (20%): Monthly organic traffic indicates readership. Normalize to 1-5 scale.
- **Accessibility** (10%): Confirmed guest post page + verified email = 5. Past guest posts but no guidelines = 3. No clear signal = 1.
- **Competitor presence** (10%): Competitor published here = +2 bonus.

Sort by composite score. Assign tiers:
- **Tier 1** (top 20%): DA 50+, strong audience match, confirmed guest posts. Maximum pitch personalization.
- **Tier 2** (middle 50%): DA 30-50, decent audience match. Standard personalization.
- **Tier 3** (bottom 30%): DA 20-30, moderate match. Template-based pitching at Scalable level only.

### 6. Push to Attio

Use `attio-lists` to create a list called "Guest Post Targets - {date}". Push the scored and tiered list from Clay with all enrichment data. Tag each entry with tier and discovery source.

## Output

- Scored, tiered list of blogs accepting guest posts, stored in Attio
- Editor contact info verified and ready for outreach
- Recent article references for pitch personalization
- Clear tier ranking for prioritizing pitch effort

## Triggers

- Run at play start (Smoke and Baseline)
- Run monthly at Scalable/Durable to discover new blogs and refresh stale contacts
- Run immediately when a new niche keyword or competitor emerges
