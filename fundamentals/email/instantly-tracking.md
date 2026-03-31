---
name: instantly-tracking
description: Track replies and campaign performance in Instantly via API
tool: Instantly
difficulty: Beginner
---

# Track Campaign Performance in Instantly

## Prerequisites
- Active campaign in Instantly with at least 50 emails sent
- Understanding of cold email benchmarks

## Steps

1. **Pull campaign analytics via API.** Use the Instantly REST API to retrieve metrics:
   ```
   GET /api/v1/campaign/<id>/analytics
   ```
   Key metrics returned: total_sent, delivered, opened, replied, bounced, unsubscribed. Focus on reply rate as your primary success metric.

2. **Benchmark your metrics.** Healthy cold email benchmarks:
   - Delivery rate: >95%
   - Open rate: 45-65%
   - Reply rate: 3-8%
   - Bounce rate: <3%
   - Unsubscribe rate: <1%
   If any metric is significantly off, diagnose the issue before sending more.

3. **Analyze by email step.** Use the API to pull per-step performance:
   ```
   GET /api/v1/campaign/<id>/steps/analytics
   ```
   Step 1 should have the highest open and reply rates. If Step 3 or 4 outperforms Step 1, your opener needs work.

4. **Disable open tracking for deliverability.** Open tracking uses invisible pixels that spam filters detect. For best deliverability, disable open tracking via the API and rely on reply rate:
   ```
   PATCH /api/v1/campaign/<id>/settings
   { "track_opens": false }
   ```

5. **Track link clicks carefully.** If you include links, use Instantly's link tracking sparingly. Tracked links are rewritten through Instantly's domain, which some spam filters flag. Only track links in Step 3+ after the prospect has engaged.

6. **Export data for deeper analysis.** Export campaign data via the API (`GET /api/v1/campaign/<id>/leads?status=replied`) and combine with your CRM data to track downstream metrics: meetings booked, opportunities created, and revenue influenced. Push to PostHog via n8n for unified reporting.
