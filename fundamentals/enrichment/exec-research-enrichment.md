---
name: exec-research-enrichment
description: Enrich an executive contact with strategic priorities, recent news, earnings highlights, and competitive context using Clay and web research
tool: Clay
difficulty: Config
---

# Executive Research Enrichment

Pull executive-specific intelligence for demo personalization: their stated priorities, recent company news, earnings call themes, competitive positioning, and strategic initiatives. Produces a structured exec profile that feeds into demo prep and ROI narrative generation.

## Prerequisites

- Clay account with credits
- Target executive contact in Clay or Attio (name, title, company)
- Optional: Anthropic API key for unstructured research synthesis

## Steps

### 1. Enrich company context in Clay

Add enrichment columns to the Clay table containing your executive contacts:

| Column | Clay Enrichment | Purpose |
|--------|----------------|---------|
| `company_description` | Company Enrichment | One-line summary of what the company does |
| `company_headcount` | Company Enrichment | Employee count for sizing ROI estimates |
| `company_revenue` | Company Enrichment | Revenue estimate for financial framing |
| `company_industry` | Company Enrichment | Industry vertical for case study matching |
| `company_funding` | Company Enrichment | Funding stage and total raised |
| `company_tech_stack` | Company Enrichment (BuiltWith) | Technologies in use for integration positioning |

### 2. Pull executive-specific intelligence via Claygent

Add a Claygent column with this prompt:

```
Research {Full Name}, {Title} at {Company Name}. Find:
1. Their stated priorities or strategic focus (from LinkedIn posts, conference talks, interviews, or company blog)
2. Recent company news in the last 90 days (funding, product launches, partnerships, leadership changes)
3. If publicly traded: key themes from the most recent earnings call (growth priorities, cost initiatives, strategic bets)
4. Competitive landscape: who are their main competitors and what is their market position
5. Any pain signals: hiring patterns suggesting scaling challenges, negative Glassdoor themes, public complaints about tools/processes

Return JSON:
{
  "exec_priorities": ["priority 1", "priority 2", "priority 3"],
  "recent_news": [{"headline": "...", "date": "...", "relevance": "..."}],
  "earnings_themes": ["theme 1", "theme 2"],
  "competitors": ["competitor 1", "competitor 2"],
  "pain_signals": ["signal 1", "signal 2"],
  "linkedin_summary": "one paragraph of their professional focus"
}
```

Cost: 10-20 Clay credits per executive.

### 3. Alternative: Apollo enrichment

If Clay credits are limited, use Apollo's People Enrichment API:

```
POST https://api.apollo.io/v1/people/match
Content-Type: application/json
x-api-key: {APOLLO_API_KEY}

{
  "first_name": "{first_name}",
  "last_name": "{last_name}",
  "organization_name": "{company_name}",
  "reveal_personal_emails": false
}
```

Apollo returns title, seniority, department, LinkedIn URL, and company details. Less strategic intelligence than Claygent but sufficient for basic exec profiling.

### 4. Alternative: Manual web research via Claude

For high-value exec targets where Clay/Apollo data is thin, use Claude to synthesize web research:

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1500,
  "messages": [{
    "role": "user",
    "content": "Research {exec_name}, {title} at {company}. Based on publicly available information, identify:\n1. Their likely top 3 strategic priorities based on their role and company context\n2. What metrics they are probably measured on (CEO: revenue/growth, CFO: margins/cash flow, CTO: uptime/velocity, COO: efficiency/scale)\n3. How our product category ({product_category}) connects to their priorities\n4. The strongest opening angle for a 15-minute executive demo\n\nReturn JSON:\n{\"priorities\": [...], \"metrics\": [...], \"product_connection\": \"...\", \"opening_angle\": \"...\"}"
  }]
}
```

### 5. Store enrichment data

Write the exec research to Attio using custom attributes on the contact record:

```json
{
  "data": {
    "values": {
      "exec_priorities": [{"value": "growth in EMEA market"}],
      "exec_research_date": [{"value": "2026-03-30"}],
      "exec_persona": [{"option": "CEO"}],
      "exec_demo_angle": [{"value": "competitive positioning and market share"}]
    }
  }
}
```

Also store the full research JSON as an Attio note on the associated deal record for the demo prep agent to consume.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay (Claygent) | AI research column | Best for deep exec research, 10-20 credits/exec |
| Apollo | People Enrichment API | Good for title/seniority, less strategic depth |
| Clearbit (HubSpot) | Enrichment API | Company-level data, limited exec-specific intel |
| LinkedIn Sales Navigator | SNAPI or manual | Best source for exec posts and priorities |
| Crunchbase | API | Funding, leadership changes, competitive landscape |
| ZoomInfo | API | Enterprise-grade exec intelligence, expensive |

## Error Handling

- **Exec has no public presence:** Fall back to role-based persona defaults (CEO cares about growth, CFO cares about margins, CTO cares about technical debt). Flag as "persona-based, not personalized."
- **Company is private with no news:** Rely on industry benchmarks and role-based assumptions. Note in the research output that personalization depth is limited.
- **Clay credits exhausted:** Use the manual Claude research alternative. It is slower but free beyond API cost (~$0.02 per exec).
- **Stale data:** Always check research date. Re-run enrichment if data is older than 30 days before a scheduled demo.
