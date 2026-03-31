---
name: directory-listing-setup
description: Create, optimize, and manage product listings across software directories with keyword-targeted copy and UTM tracking
category: Directories
tools:
  - G2
  - Capterra
  - Product Hunt
  - TrustRadius
  - Clay
  - Attio
fundamentals:
  - directory-listing-api
  - clay-claygent
  - attio-contacts
  - google-ads-keyword-research
---

# Directory Listing Setup

This drill walks through identifying the right directories for your product, creating optimized listings on each, and tracking everything in your CRM. It is the foundation of the directories-marketplaces play.

## Input

- ICP definition (output from `icp-definition` drill) -- who your buyers are and where they search
- Product positioning: one-liner, key differentiators, pricing, screenshots, demo video
- Attio CRM access for logging directory presence

## Steps

### 1. Identify target directories

Use Clay with the `clay-claygent` fundamental to research which directories your ICP uses when evaluating tools in your category.

**Claygent prompt:**
```
For a {your_category} product targeting {your_ICP}, list the top 15 software directories and marketplaces where buyers compare and evaluate tools. For each, provide:
- Directory name and URL
- Estimated monthly unique visitors
- Whether free listing is available
- Whether the directory has a review/rating system
- Relevance to {your_ICP} (high/medium/low)
Rank by relevance and traffic.
```

**Priority tiers:**
- **Tier 1 (must-have):** G2, Capterra, Product Hunt -- highest traffic, strongest buyer intent
- **Tier 2 (strong):** TrustRadius, GetApp, SourceForge, AlternativeTo
- **Tier 3 (niche):** Industry-specific directories (e.g., BuiltWith for dev tools, SaaSWorthy, StackShare, Slant)

For Smoke test: list on 3-5 Tier 1 and Tier 2 directories.
For Scalable: expand to 10-15 across all tiers.

### 2. Research category keywords

Use the `google-ads-keyword-research` fundamental to find the terms buyers search within directories. Focus on:

- Category terms: "{category} software", "best {category} tool", "{category} alternatives"
- Problem terms: "how to {solve problem your product addresses}"
- Comparison terms: "{competitor} vs", "{competitor} alternative"

Incorporate these keywords into your listing titles, descriptions, and feature lists on each directory.

### 3. Create listing content per directory

For each target directory, prepare listing content using the `directory-listing-api` fundamental:

**Title:** Include your primary category keyword naturally. Example: "Acme -- AI-Powered {Category} Platform" not just "Acme."

**Short description (150 chars):** Lead with the outcome. "Reduce {pain point} by X% with automated {solution}."

**Long description:** Structure as:
1. The problem your ICP faces (2 sentences)
2. How your product solves it differently (3 sentences)
3. Key results customers achieve (2 sentences with specific numbers)
4. Core capabilities list (5-7 bullet points)

**Screenshots:** Minimum 3. Show: (1) main dashboard/workspace, (2) the key workflow that differentiates you, (3) results/analytics view. Add captions explaining what each screenshot shows.

**Video:** 60-90 second product walkthrough. Upload to YouTube with UTM-tagged link in description.

**Pricing:** Be transparent. Directories that show pricing get more qualified traffic. Include starting price, billing model, and whether a free trial or freemium tier exists.

**Feature checklist:** Fill out every comparison field the directory offers. Incomplete profiles rank lower and lose in head-to-head comparisons.

### 4. Submit listings with UTM tracking

Use the `directory-listing-api` fundamental to create each listing. For every outbound link, append UTM parameters:

```
?utm_source={directory_name}&utm_medium=directory&utm_campaign=listing
```

For PPC links (Capterra):
```
?utm_source=capterra&utm_medium=ppc&utm_campaign=listing
```

### 5. Log listings in CRM

Using the `attio-contacts` fundamental, create a record in Attio for each directory listing:

- Record type: Campaign or custom object
- Fields: directory_name, listing_url, date_created, listing_tier (1/2/3), has_ppc (boolean), review_count, current_rating, last_updated

This provides a central inventory of all directory presence.

## Output

- Active listings on 3-15 directories (depending on play level)
- All links UTM-tagged for attribution
- CRM records for each listing
- Keyword-optimized copy tailored to each directory's search algorithm

## Triggers

- Run once at Smoke level for initial setup
- Run again at Scalable level to expand to more directories
- Re-run quarterly to update listings with new features, pricing changes, or positioning shifts
