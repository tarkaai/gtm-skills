---
name: podcast-prospect-research
description: Find and qualify relevant podcasts for founder guest appearances using directory APIs and enrichment
category: Podcast
tools:
  - ListenNotes
  - Podchaser
  - Rephonic
  - Clay
  - Attio
fundamentals:
  - podcast-directory-search
  - podcast-host-enrichment
  - clay-table-setup
  - attio-lists
---

# Podcast Prospect Research

This drill builds a qualified list of podcasts to pitch for founder guest appearances. It combines directory search, audience analysis, and host contact enrichment into a pipeline that outputs a ready-to-pitch list.

## Input

- Founder's area of expertise (topics they can speak on)
- ICP definition (who should be listening — job titles, company size, industry)
- Target number of podcasts to find (5 for Smoke, 20 for Baseline, 50+ for Scalable)
- Names of 2-3 competitor founders or industry peers who have been podcast guests (for cross-reference search)

## Steps

### 1. Search directories by topic

Use `podcast-directory-search` to run keyword searches across ListenNotes. Execute 3-5 searches with different keyword combinations:
- Primary topic (e.g., "B2B SaaS growth")
- Adjacent topics (e.g., "startup marketing", "developer tools")
- Problem-focused terms (e.g., "customer acquisition for startups")

Filter results: English language, actively publishing (episode within last 30 days), listen_score >= 20 (for Smoke; adjust threshold up for later levels).

### 2. Cross-reference competitor guest appearances

Use `podcast-directory-search` episode search to find where competitor founders or industry peers have appeared as guests. Search for their names as episode guests. Every podcast that hosted a competitor is a high-probability target — they already book founders in your space.

### 3. Check guest format

For each candidate podcast, verify it accepts guest interviews. Check:
- Recent episode titles: do they include guest names or "interview with" language?
- Podcast website: is there a "Be a Guest" or "Guest Application" page?
- Episode descriptions: do they credit guest speakers?

Remove podcasts that are solo-host-only, co-host conversational, or news-recap formats without guests.

### 4. Create and enrich the prospect table

Use `clay-table-setup` to create a Clay table with columns:
- Podcast name
- Host name
- Website URL
- ListenNotes listen_score
- Last episode date
- Episode count
- Guest format confirmed (yes/no)
- Topic fit score (1-5, based on keyword match and audience overlap)
- Contact method (email / form / Twitter / LinkedIn)
- Host email (to be enriched)
- Pitch status (not pitched / pitched / replied / booked / declined)

Import all candidate podcasts from step 1-3.

### 5. Enrich host contacts

Run `podcast-host-enrichment` on the Clay table. Priority: RSS feed email > Clay email finder > Apollo lookup > LinkedIn manual find. Verify all emails before outreach.

### 6. Score and rank

Sort the list by a composite score:
- Topic fit (40%): How closely does the show's content match the founder's expertise?
- Audience size (30%): ListenNotes listen_score as a proxy
- Accessibility (20%): Verified email = high, form = medium, no contact = low
- Recency (10%): More recent episodes = more active show

### 7. Push to Attio

Use `attio-lists` to create a list called "Podcast Targets — {date}". Push the top-ranked podcasts from Clay. Tag each with priority tier: Tier 1 (top 20%), Tier 2 (middle 40%), Tier 3 (bottom 40%).

## Output

- A scored, enriched list of qualified podcasts in Attio
- Host contact info verified and ready for outreach
- Clear priority ranking for pitch sequencing

## Triggers

- Run once at the start of each play level
- Re-run monthly at Scalable/Durable levels to find new shows and remove stale ones
