---
name: tech-stack-detection
description: Detect a company's technology stack via BuiltWith, Wappalyzer, or Clay enrichment
tool: Clay
product: Clay
difficulty: Config
---

# Tech Stack Detection

Identify the technologies a target company uses on their website and in their infrastructure. Tech stack data feeds personalization (integration angles), qualification (complementary tools), and competitive positioning (competing tools).

## Prerequisites

- Target company domain
- One of: Clay account with credits, BuiltWith API key, Wappalyzer API key

## Steps

### 1. Detect via Clay enrichment

In your Clay table, add a "BuiltWith" or "Wappalyzer" enrichment column. Input: company domain. Output: array of detected technologies with categories (analytics, CRM, marketing automation, payments, hosting, etc.).

Clay normalizes the output into a structured list. Cost: 1-2 Clay credits per lookup.

### 2. Detect via BuiltWith API (direct)

```
GET https://api.builtwith.com/v21/api.json
  ?KEY={BUILTWITH_API_KEY}
  &LOOKUP={domain}
```

Response structure:
```json
{
  "Results": [{
    "Paths": [{
      "Technologies": [
        {
          "Name": "Google Analytics",
          "Categories": ["Analytics"],
          "FirstDetected": 1609459200000,
          "LastDetected": 1711929600000
        }
      ]
    }]
  }]
}
```

Parse `Technologies[].Name` and `Technologies[].Categories` to build the stack profile. The `FirstDetected` and `LastDetected` timestamps reveal adoption timing.

Cost: BuiltWith Basic API starts at $295/month. For occasional lookups, use Clay as a proxy.

### 3. Detect via Wappalyzer API (alternative)

```
GET https://api.wappalyzer.com/v2/lookup/
  ?urls={domain}
Headers:
  x-api-key: {WAPPALYZER_API_KEY}
```

Response:
```json
{
  "technologies": [
    {
      "name": "Stripe",
      "categories": ["Payment processors"],
      "website": "https://stripe.com"
    }
  ]
}
```

Cost: Wappalyzer API offers 50 free lookups/month, then plans start at $100/month for 5,000 lookups.

### 4. Detect via Claygent (fallback for deeper stack)

For technologies not visible on the public website (internal tools, backend infrastructure), use Claygent:

```
Research the technology stack at {Company Name} ({domain}). Check:
1. Their job postings for technologies mentioned (Python, React, AWS, etc.)
2. Their engineering blog for tool mentions
3. GitHub repositories if public
4. G2 or TrustRadius reviews they've written

Return a JSON object:
{
  "website_tech": ["detected from website"],
  "job_posting_tech": ["mentioned in job postings"],
  "engineering_blog_tech": ["mentioned in blog"],
  "review_tech": ["tools they've reviewed on G2/TrustRadius"]
}
```

Cost: 5-10 Clay credits.

### 5. Classify technologies for sales relevance

After detection, classify each technology into one of:

| Classification | Definition | Action |
|---|---|---|
| Complementary | Integrates with your product | Personalization hook: "You use X, which integrates with us" |
| Competing | Direct or indirect competitor | Displacement angle: "Companies switch from X to us for Y reason" |
| Indicator | Signals sophistication or stage | Qualification signal: "Using enterprise tools = budget available" |
| Neutral | No sales relevance | Ignore |

Store the classified tech stack as a custom attribute on the Attio company record.

### 6. Set up refresh schedule

Technology stacks change. For active pipeline accounts, refresh monthly. For target account lists, refresh quarterly. Use Clay's scheduled enrichment or trigger via n8n cron.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay | BuiltWith/Wappalyzer enrichment columns | Easiest, credit-based |
| BuiltWith | Direct API | Most comprehensive, expensive |
| Wappalyzer | Direct API | Good coverage, cheaper |
| SimilarTech | API | Alternative to BuiltWith |
| Apollo | Tech stack enrichment | Included in Apollo plans |
| HG Insights | Technology intelligence API | Enterprise-grade |

## Error Handling

- **No technologies detected**: Domain may use server-side rendering or block crawlers. Try Claygent job-posting approach as fallback.
- **Stale data**: BuiltWith `LastDetected` timestamp older than 6 months means the technology may have been removed. Flag for re-verification.
- **Overwhelmingly large stack**: Enterprise companies can show 100+ technologies. Filter to only the categories relevant to your product (e.g., if you sell analytics, focus on the Analytics and Marketing Automation categories).
- **Rate limits**: BuiltWith allows 10 requests/second. Wappalyzer allows 1 request/second on free tier. Batch lookups with appropriate delays.
