---
name: analyst-target-research
description: Identify, research, and prioritize industry analysts and consultants who influence your buyers' purchase decisions
category: Research
tools:
  - Clay
  - Attio
  - Anthropic
fundamentals:
  - analyst-landscape-mapping
  - clay-people-search
  - clay-enrichment-waterfall
  - clay-scoring
  - attio-contacts
  - attio-lists
---

# Analyst & Consultant Target Research

This drill produces a scored, prioritized list of analysts and consultants who influence your target buyers. It combines Clay enrichment with web research to build a comprehensive map of the influencer landscape for your category.

## Input

- Your ICP definition (who are your buyers, what do they research before purchasing)
- Your market category (what analysts call your space — may differ from how you describe yourself)
- Known analysts or firms already on your radar (even partial lists help)
- Budget for Clay enrichment credits

## Steps

### 1. Map the analyst landscape

Run the `analyst-landscape-mapping` fundamental to identify analysts across all four tiers (industry analysts, boutique analysts, independent consultants, thought-leader influencers). Start broad: it is better to find 50 candidates and filter down than to miss relevant influencers.

For each analyst found, capture: name, firm, tier, coverage area, LinkedIn URL, email, recent publications, and buyer access type (direct advisory vs. content influence).

### 2. Enrich analyst profiles

For each analyst in your Clay table, run the `clay-enrichment-waterfall` fundamental to fill gaps:
- Email address (try Clearbit, then Hunter, then People Data Labs)
- LinkedIn URL (if not already found)
- Company firmographics (firm size, founding year, client focus)

Then use the `clay-people-search` fundamental to verify that each analyst is still active at their listed firm and still covers your category. Filter out anyone who has moved to a different coverage area or left the industry.

### 3. Research recent output

For each Tier 1-3 analyst, use Claygent to find their 3 most recent publications, speaking engagements, or social media posts related to your market. Log these in the Clay table. This context is essential for personalizing briefing requests and preparing briefing documents.

### 4. Score and prioritize

Use the `clay-scoring` fundamental to assign a composite score based on:
- **Coverage match (40%):** How directly do they cover your specific category?
- **Buyer access (30%):** Do they advise your ICP directly, or is influence indirect?
- **Accessibility (20%):** How easy is it to get a briefing? (Independents > boutique > large firms)
- **Recency (10%):** Have they published in your space in the last 6 months?

Set thresholds: Priority 1 (score >= 8), Priority 2 (score 6-7), Priority 3 (score 4-5). Discard scores below 4.

### 5. Export to Attio CRM

Push all scored analysts to Attio using the `attio-contacts` fundamental. Tag each contact with:
- Relationship Type: "Analyst/Consultant"
- Analyst Tier: 1-4
- Priority: 1-3
- Coverage Area: text field
- Briefing Status: "Not Contacted" (initial value)

Create an Attio list called "Analyst Briefing Targets" using the `attio-lists` fundamental. Add all Priority 1 and Priority 2 analysts. This list feeds into the briefing outreach workflow.

### 6. Identify warm paths

For each Priority 1 analyst, check your network for mutual connections:
- Query Attio for contacts who work at the analyst's firm or have interacted with the analyst
- Check LinkedIn mutual connections
- Check if any existing customers have relationships with the analyst

Log warm paths in the Attio contact notes. Analysts respond far better to warm introductions than cold briefing requests.

## Output

- Attio list "Analyst Briefing Targets" with 15-30 scored, prioritized analysts
- Each analyst record enriched with: contact info, coverage area, recent publications, relevance score, warm path notes
- Clear tier and priority assignments for outreach sequencing

## Triggers

- Run once at play start (Smoke level)
- Refresh quarterly: re-run landscape mapping, update scores, add new analysts, remove stale entries
