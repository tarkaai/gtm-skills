---
name: pagespeed-insights-api
description: Measure Core Web Vitals and Lighthouse scores via the Google PageSpeed Insights API
tool: Google
product: PageSpeed Insights
difficulty: Setup
---

# PageSpeed Insights API

Programmatically audit any URL for Core Web Vitals (LCP, INP, CLS), Lighthouse performance scores, and specific optimization opportunities. Returns both field data (real user metrics from Chrome UX Report) and lab data (simulated Lighthouse audit).

## Authentication

PageSpeed Insights API requires a Google Cloud API key. No OAuth needed.

1. Create or select a Google Cloud project at `https://console.cloud.google.com/`
2. Enable the PageSpeed Insights API: `https://console.cloud.google.com/apis/library/pagespeedonline.googleapis.com`
3. Create an API key: `https://console.cloud.google.com/apis/credentials`
4. Store the key as `PAGESPEED_API_KEY` environment variable

## Core Operations

### Run a PageSpeed audit

```
GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed
  ?url=https://example.com/solutions/crm-for-startups
  &key={PAGESPEED_API_KEY}
  &strategy=mobile
  &category=performance
  &category=seo
  &category=accessibility
  &category=best-practices
```

Query parameters:
- `url` (required): Full URL to audit
- `strategy`: `mobile` or `desktop` (default: mobile)
- `category`: One or more of `performance`, `seo`, `accessibility`, `best-practices`

### Parse Core Web Vitals from response

Field data (real users) is at `loadingExperience.metrics`:

```json
{
  "LARGEST_CONTENTFUL_PAINT_MS": {
    "percentile": 2400,
    "category": "AVERAGE"
  },
  "INTERACTION_TO_NEXT_PAINT": {
    "percentile": 180,
    "category": "GOOD"
  },
  "CUMULATIVE_LAYOUT_SHIFT": {
    "percentile": 0.08,
    "category": "GOOD"
  }
}
```

Thresholds (from Google):
- LCP: Good < 2500ms, Poor > 4000ms
- INP: Good < 200ms, Poor > 500ms
- CLS: Good < 0.1, Poor > 0.25

Lab data (Lighthouse) is at `lighthouseResult.audits`. Key audits to extract:
- `lighthouseResult.categories.performance.score` (0-1, multiply by 100)
- `lighthouseResult.categories.seo.score`
- `lighthouseResult.audits.render-blocking-resources`
- `lighthouseResult.audits.unused-css-rules`
- `lighthouseResult.audits.unused-javascript`
- `lighthouseResult.audits.modern-image-formats`
- `lighthouseResult.audits.uses-responsive-images`
- `lighthouseResult.audits.server-response-time`
- `lighthouseResult.audits.redirects`
- `lighthouseResult.audits.dom-size`

Each audit object has `score` (0-1 or null), `displayValue`, and `details` with specific items to fix.

### Batch audit multiple URLs

The API supports one URL per request. To audit many pages, loop with rate limiting:

```python
import requests, time

urls = ["https://example.com/", "https://example.com/pricing", ...]
results = []
for url in urls:
    resp = requests.get(
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
        params={"url": url, "key": API_KEY, "strategy": "mobile", "category": "performance"}
    )
    results.append({"url": url, "data": resp.json()})
    time.sleep(1)  # Respect rate limits
```

## Rate Limits

- 400 queries per 100 seconds per API key
- 25,000 queries per day per API key
- Each request takes 10-30 seconds to complete (Lighthouse runs in real time)

## Error Handling

- `400 Bad Request`: URL is unreachable or malformed. Verify the URL loads in a browser.
- `429 Too Many Requests`: Rate limit exceeded. Implement exponential backoff.
- `500 Internal Server Error`: Lighthouse failed to audit the page (timeout, JS error). Retry once after 30 seconds.

## Pricing

Free. No charges for the PageSpeed Insights API.
Pricing page: https://developers.google.com/speed/docs/insights/v5/get-started

## Alternatives

- **WebPageTest API** (free/paid): More detailed waterfall analysis, multiple locations — https://www.webpagetest.org/
- **Lighthouse CLI** (free): Run Lighthouse locally via `npx lighthouse URL --output json` for unlimited audits
- **GTmetrix API** ($14.95/mo+): PageSpeed + Web Vitals with historical tracking — https://gtmetrix.com/api/
- **Calibre** ($45/mo+): Automated Lighthouse testing with alerting — https://calibreapp.com/
- **SpeedCurve** ($12/mo+): Real user monitoring + synthetic testing — https://speedcurve.com/
