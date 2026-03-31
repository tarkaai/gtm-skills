---
name: podcast-tracking-links
description: Create UTM-tagged tracking links and vanity URLs for podcast guest appearances
tool: PostHog / Rebrandly / Dub.co
difficulty: Setup
---

# Podcast Tracking Links

Create unique, trackable URLs for each podcast appearance so you can attribute inbound traffic and leads back to specific episodes.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| PostHog + UTM params | Native analytics with UTM parsing | Default stack — no additional cost |
| Dub.co | Link management API with analytics | Vanity short links + click analytics |
| Rebrandly | Branded short links | Custom domain short URLs |
| Bitly | Short links with click tracking | Simple click counting |

## UTM Parameter Schema

Every podcast appearance gets a unique tracking URL. Format:

```
https://yoursite.com/?utm_source=podcast&utm_medium=guest&utm_campaign={{podcast_slug}}&utm_content={{episode_date}}
```

Parameters:
- `utm_source`: Always `podcast` (the channel)
- `utm_medium`: Always `guest` (the type — guest appearance, not your own show)
- `utm_campaign`: Slugified podcast name (e.g., `the-saas-podcast`, `founders-journal`)
- `utm_content`: Episode air date in YYYY-MM-DD format (differentiates repeat appearances)

## Create a Vanity URL

Podcast listeners hear URLs out loud. Complex UTM URLs are useless verbally. Create a short, memorable URL:

```
https://yoursite.com/podcast → redirects to the UTM-tagged URL
```

Or per-show:
```
https://yoursite.com/saas-podcast → redirects with that show's UTM params
```

### Dub.co API

```http
POST https://api.dub.co/links
Header: Authorization: Bearer {DUB_API_KEY}
Content-Type: application/json

{
  "url": "https://yoursite.com/?utm_source=podcast&utm_medium=guest&utm_campaign=the-saas-podcast&utm_content=2026-04-15",
  "key": "saas-podcast",
  "domain": "your-short-domain.co"
}
```

Response: `{ "shortLink": "https://your-short-domain.co/saas-podcast" }`

### Rebrandly API

```http
POST https://api.rebrandly.com/v1/links
Header: apikey: {REBRANDLY_API_KEY}
Content-Type: application/json

{
  "destination": "https://yoursite.com/?utm_source=podcast&utm_medium=guest&utm_campaign=the-saas-podcast",
  "slashtag": "saas-podcast",
  "domain": { "fullName": "your-brand.link" }
}
```

## PostHog Tracking

PostHog automatically parses UTM parameters from page views. No additional setup needed if PostHog JS snippet is installed. To query podcast traffic:

```
PostHog Insights → New Insight → Trends
Event: $pageview
Filter: utm_source = podcast AND utm_medium = guest
Breakdown by: utm_campaign (shows traffic per podcast)
```

To track conversions from podcast traffic:

```
PostHog Insights → New Insight → Funnel
Step 1: $pageview (where utm_source = podcast)
Step 2: lead_created OR meeting_booked OR trial_started
Breakdown by: utm_campaign
```

## CTA Script for Podcast Appearances

Give the founder a standard verbal CTA for every podcast appearance:

```
"If you want to check out [product], head to [yoursite.com/podcast-name] —
I set up a special link just for [podcast name] listeners."
```

This makes it natural, trackable, and gives the host a sense of exclusivity.

## Error Handling

- **Forgot to create link before episode airs**: Create it immediately and update the episode show notes. You lose verbal CTA traffic but capture show-notes clicks.
- **Short link domain expired**: Fall back to the full UTM URL in show notes.
- **UTM params stripped**: Some email clients strip UTMs. Use Dub.co or Rebrandly which track clicks server-side as a backup attribution method.
