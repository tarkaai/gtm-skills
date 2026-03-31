---
name: account-intelligence-assembly
description: Pull and merge account data from CRM, enrichment, news, and social sources into a single structured intelligence profile
tool: Clay
difficulty: Config
---

# Account Intelligence Assembly

Assemble a comprehensive intelligence profile for a target account by pulling from multiple data sources and merging into a single structured document. This is the data-gathering step that feeds meeting brief generation.

## Prerequisites

- Clay account with credits (Claygent + Company Search)
- Attio CRM with deal records
- Target account identified (company name or domain)

## Steps

### 1. Pull CRM deal context from Attio

Query Attio for the deal and all associated contacts:

```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
attio.list_records({ object: "people", filter: { company: "{company_id}" } })
```

Extract: company name, deal stage, deal value, all contacts with titles, prior meeting notes, prior emails, any BANT/MEDDIC scores, pain points documented from prior calls, timeline mentioned, competitors mentioned.

### 2. Enrich the company in Clay

Use `clay-company-search` with the company domain. Add enrichment columns:

- **Firmographics**: headcount, revenue estimate, funding stage, investors, founding year
- **Tech stack**: technologies used (via BuiltWith or similar Clay enrichment)
- **Recent funding**: last round amount, date, lead investor
- **Job openings**: current open roles (signals growth areas and pain points)
- **Social presence**: LinkedIn followers, recent LinkedIn posts from company page

### 3. Pull recent news and signals via Claygent

Add a Claygent column with prompt:
```
Research {Company Name} ({domain}). Find:
1. News from the last 90 days (funding, product launches, partnerships, leadership changes, layoffs)
2. Recent blog posts or press releases they published
3. Earnings or financial disclosures (if public)
4. Industry trends affecting their sector
5. Competitor activity that might create urgency
Return each item with date, source, and a one-sentence summary.
```

Cost: 5-10 credits per company.

### 4. Research key contacts via Claygent

For each contact associated with the deal, add a Claygent column:
```
Research {Contact Name}, {Title} at {Company Name}. Find:
1. Recent LinkedIn posts or articles they authored
2. Conference talks or podcast appearances
3. Career trajectory (previous companies, roles)
4. Shared connections or interests with {your_founder_name}
5. Topics they engage with publicly
Return each item with date, source, and relevance.
```

Cost: 5-10 credits per contact.

### 5. Check for competitive intelligence

If the Attio deal record has a "Competitors" object linked, pull the competitive battlecard data (from `competitive-intel-aggregation` fundamental). If no structured competitive data exists, use Claygent:
```
What alternatives to {your_product} might {Company Name} be evaluating? Based on their tech stack, industry, and company size, which competitors are most likely? For each, note one strength they have and one weakness relative to {your_product_positioning}.
```

### 6. Structure the output

Merge all data into a single structured profile:

```json
{
  "company": {
    "name": "...",
    "domain": "...",
    "industry": "...",
    "headcount": 0,
    "revenue_estimate": "...",
    "funding_stage": "...",
    "last_funding": { "amount": "...", "date": "...", "investor": "..." },
    "tech_stack": ["..."],
    "recent_job_openings": ["..."]
  },
  "deal_context": {
    "stage": "...",
    "value": "...",
    "contacts": [
      { "name": "...", "title": "...", "role_in_deal": "...", "prior_interactions": "..." }
    ],
    "pain_points_documented": ["..."],
    "competitors_in_deal": ["..."],
    "bant_score": {},
    "meddic_score": {},
    "timeline": "..."
  },
  "recent_signals": [
    { "type": "news|hiring|funding|content", "date": "...", "summary": "...", "source": "..." }
  ],
  "contact_research": [
    { "name": "...", "recent_activity": ["..."], "shared_connections": ["..."], "interests": ["..."] }
  ],
  "competitive_landscape": [
    { "competitor": "...", "likelihood": "high|medium|low", "their_strength": "...", "our_advantage": "..." }
  ]
}
```

Store this profile as an Attio note on the deal tagged `account-intelligence`.

## Via Apollo (Alternative)

1. Search company in Apollo API: `GET /v1/organizations/enrich?domain={domain}`
2. Pull contacts: `GET /v1/mixed_people/search` with `organization_domains: ["{domain}"]`
3. Apollo provides firmographics, tech stack, headcount, and contact data
4. Does not provide news, social activity, or competitive inference -- supplement with Claygent

## Via ZoomInfo (Enterprise Alternative)

1. Company enrich: `POST /enrich/company` with domain
2. Contact search: `POST /search/contact` filtered by company
3. Provides intent data, org charts, and technographics
4. Most comprehensive but requires enterprise contract

## Tool Alternatives

| Tool | Capability | Notes |
|------|-----------|-------|
| Clay | Company + people enrichment, Claygent for news/research | Best all-in-one for startups |
| Apollo | Company + contact enrichment | Good data, no AI research layer |
| ZoomInfo | Full enrichment + intent | Enterprise, expensive |
| Clearbit (now HubSpot) | Company enrichment API | Good real-time enrichment |
| Cognism | EU-strong people data | Best for European accounts |
| LinkedIn Sales Navigator | Manual research | Deepest data, not API-accessible |

## Error Handling

- **Claygent returning sparse data**: Company is too new, private, or niche. Fall back to manual LinkedIn research. Log a `brief_data_sparse` event in PostHog.
- **Stale CRM data**: Compare Attio contact titles against Clay enrichment. Flag mismatches (title changed = potential role change signal).
- **Credit efficiency**: Run enrichment on accounts with meetings scheduled in the next 48 hours only. Do not batch-enrich accounts speculatively at Smoke/Baseline levels.
