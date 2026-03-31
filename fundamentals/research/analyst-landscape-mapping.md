---
name: analyst-landscape-mapping
description: Identify and map industry analysts, consultants, and influencers who shape buyer decisions in a target market
tool: Clay
product: Clay
difficulty: Config
---

# Analyst & Consultant Landscape Mapping

Systematically identify the analysts, consultants, and advisory firms whose recommendations influence your buyer's purchase decisions. This is the foundation for any analyst relations program.

## Prerequisites

- Clay account with enrichment credits
- Defined ICP (you know which buyers you want analysts to influence)
- Understanding of your market category (what analysts call your space)

## Steps

### 1. Define analyst categories relevant to your market

Not all analysts are Gartner. For most startups, the relevant influencers fall into these buckets:

- **Tier 1 — Industry analysts:** Gartner, Forrester, IDC, 451 Research. Cover broad categories. Hard to access, high influence.
- **Tier 2 — Boutique analysts:** Focused on your specific niche. Examples: RedMonk (developer tools), Constellation Research (enterprise), Moor Insights (infrastructure). More accessible, deep domain expertise.
- **Tier 3 — Independent consultants:** Solo practitioners or small firms who advise buyers directly. Often former practitioners. Very accessible, direct buyer relationships.
- **Tier 4 — Thought-leader influencers:** Industry bloggers, newsletter authors, podcast hosts who are consulted during purchase decisions. Not formal analysts but shape opinions.

Decide which tiers to target based on your deal size and buyer sophistication. For startups with <$50K ACV, Tier 2-4 are usually the highest ROI.

### 2. Build the analyst target list in Clay

Create a Clay table with source "Import from CSV" or "Find People." Set up these columns:

| Column | Type | Purpose |
|--------|------|---------|
| Name | Text | Analyst/consultant name |
| Firm | Text | Company or independent |
| Tier | Select (1-4) | Influence tier from step 1 |
| Coverage Area | Text | What topics they cover |
| Relevance Score | Number (1-10) | How closely their coverage matches your category |
| LinkedIn URL | URL | For outreach and monitoring |
| Email | Email | For briefing requests |
| Twitter/X | URL | For content monitoring |
| Recent Publications | Text | Last 3 articles/reports |
| Buyer Access | Select (Direct/Indirect) | Do they advise buyers directly or influence through content? |

### 3. Populate via web research enrichment

Use Clay's "Find People" enrichment with these search strategies:

**Strategy A — Firm-first search:**
Search for people at known analyst firms (Gartner, Forrester, etc.) with titles containing "analyst," "research director," "VP research" AND coverage areas matching your category keywords.

**Strategy B — Content-first search:**
Use Clay's Claygent (`clay-claygent` fundamental) to search for:
- Authors of recent reports in your category (e.g., "Magic Quadrant for [your category]")
- Speakers at industry conferences on your topic
- Podcast guests discussing your market
- Newsletter authors covering your space

**Strategy C — Network-first search:**
Query your Attio CRM for contacts with titles containing "analyst," "consultant," "advisor," or "research." Check your LinkedIn network for mutual connections to known analysts.

### 4. Score and prioritize

For each analyst, calculate a Relevance Score (1-10) using Clay formulas:

- **Coverage match (40%):** Does their published coverage directly mention your category? Score 10 if exact match, 5 if adjacent, 1 if tangential.
- **Buyer access (30%):** Do they advise your specific buyer persona? Score 10 if they directly consult with your ICP, 5 if they publish content your ICP reads, 1 if influence is indirect.
- **Accessibility (20%):** Score 10 for independents who accept briefings freely, 5 for boutique firms, 1 for Tier 1 firms that require vendor relationships.
- **Recency (10%):** Have they published in your space in the last 6 months? Score 10 if yes, 5 if last year, 1 if older.

### 5. Export to Attio CRM

Push the scored analyst list to Attio as contact records. Tag them with a "Relationship Type" of "Analyst/Consultant." Create an Attio list called "Analyst Briefing Targets" containing all analysts with Relevance Score >= 6.

## Error Handling

- **Too few results:** Broaden your category keywords. Search for adjacent categories and analysts who have recently expanded their coverage.
- **No email found:** Use Clay's email waterfall enrichment. For analysts at large firms, the firm's website usually has a briefing request form — log that URL instead.
- **Stale data:** Set a reminder to re-run the landscape mapping quarterly. Analysts change coverage areas and firms frequently.

## Cost Estimates

- Clay enrichment: ~50-100 credits per analyst researched. For a list of 30-50 analysts, expect $20-50 in Clay credits.
- Time: 2-3 hours for initial mapping, 30 minutes quarterly refresh.
