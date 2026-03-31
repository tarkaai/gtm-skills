---
name: robots-txt-management
description: Audit, generate, and validate robots.txt rules for proper crawl control
tool: Dev Tools
product: Runtime
difficulty: Setup
---

# robots.txt Management

Programmatically audit, validate, and update robots.txt to ensure correct crawl directives. Misconfigured robots.txt is one of the most common technical SEO errors — blocking pages that should be indexed or allowing crawl budget waste on low-value paths.

## Core Operations

### Fetch and parse robots.txt

```bash
curl -s "https://example.com/robots.txt"
```

Or via Python:

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://example.com/robots.txt")
rp.read()

# Check if a specific URL is allowed for Googlebot
is_allowed = rp.can_fetch("Googlebot", "/solutions/crm-for-startups")
crawl_delay = rp.crawl_delay("Googlebot")
sitemaps = rp.site_maps()
```

### Validate robots.txt syntax

Use Google's robots.txt testing tool via the Search Console API:

```
GET https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/robots
Authorization: Bearer {access_token}
```

Or validate locally with the `robots-txt-guard` npm package:

```bash
npx robots-txt-guard validate https://example.com/robots.txt
```

### Common robots.txt audit checks

Run these checks against the fetched robots.txt content:

1. **Sitemap declaration exists**: File contains `Sitemap: https://...` line
2. **No blanket disallow**: `Disallow: /` without a User-agent qualifier would block all crawling
3. **Important paths are allowed**: `/`, `/blog/`, `/solutions/`, `/pricing/` are not disallowed for Googlebot
4. **Low-value paths are blocked**: `/admin/`, `/api/`, `/staging/`, `/internal/`, `/search?` query pages are disallowed
5. **No conflicting rules**: A more specific Allow rule should override a broader Disallow (Googlebot processes the most specific match)
6. **Crawl-delay is reasonable**: If set, should be 1-5 seconds. >10 seconds drastically slows indexation.
7. **File is accessible**: Returns 200 OK, not 404 or 500

### Generate an optimized robots.txt

```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /internal/
Disallow: /staging/
Disallow: /search?
Disallow: /_next/data/
Disallow: /preview/
Disallow: /draft/

User-agent: Googlebot
Allow: /

User-agent: AdsBot-Google
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Customize based on the site's URL structure. The principle: Allow everything important, Disallow paths that waste crawl budget or expose internal tooling.

### Test specific URL against robots.txt rules

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://example.com/robots.txt")
rp.read()

test_urls = [
    "/solutions/crm-for-startups",
    "/blog/technical-seo-guide",
    "/pricing",
    "/admin/dashboard",
    "/api/v1/users",
]

for url in test_urls:
    allowed = rp.can_fetch("Googlebot", url)
    print(f"{'ALLOWED' if allowed else 'BLOCKED'}: {url}")
```

### Deploy robots.txt changes

For static hosting (Vercel, Netlify): Place `robots.txt` in the `public/` directory.

For Next.js: Create `public/robots.txt` or generate dynamically via `app/robots.ts`:

```typescript
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: ['/admin/', '/api/', '/internal/'] },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

For Webflow: Add via Project Settings > Custom Code > robots.txt, or upload to the hosting root.

## Error Handling

- `404 Not Found`: robots.txt doesn't exist. Google treats this as "everything allowed." Create one to explicitly control crawling.
- `5xx Server Error`: Google treats 5xx responses as "disallow all" temporarily. Ensure your robots.txt endpoint is highly available.
- Encoding issues: robots.txt must be UTF-8 encoded plain text.

## Pricing

Free. robots.txt is a web standard with no tooling cost.

## Alternatives

- **Google Search Console robots.txt Tester** (free): GUI tool for testing rules in browser
- **Merkle robots.txt Tester** (free): https://technicalseo.com/tools/robots-txt/
- **Ryte robots.txt analyzer** (free): https://en.ryte.com/free-tools/robots-txt/
- **Screaming Frog** ($259/yr): Includes robots.txt validation in crawl analysis
- **Botify** (enterprise pricing): Full crawl budget analysis including robots.txt impact
