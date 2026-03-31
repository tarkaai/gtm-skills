---
name: twitter-x-ads-creative
description: Create and manage promoted tweet copy, media cards, and creative variants for X Ads campaigns
tool: Twitter/X Ads
difficulty: Config
---

# Twitter/X Ads Creative

Create promoted tweet variants and media cards optimized for B2B engagement on X. X ads perform best when they look like organic content — no stock photos, no corporate jargon.

## Promoted Tweet Types

### Text-only promoted tweets

Best for engagement and thought-leadership positioning:

```
POST /12/accounts/{account_id}/tweet

{
  "text": "We analyzed 500 deploys across 47 teams.\n\nThe #1 predictor of deploy failure? Not code quality.\n\nIt's whether the team has a rollback plan before they start.\n\nFull breakdown: {LANDING_PAGE_URL}?utm_source=twitter&utm_medium=paid&utm_campaign={CAMPAIGN_SLUG}",
  "as_user_id": "{USER_ID}"
}
```

Then promote:
```
POST /12/accounts/{account_id}/promoted_tweets

{
  "line_item_id": "{LINE_ITEM_ID}",
  "tweet_ids": ["{TWEET_ID}"]
}
```

Character limit: 280. Links use up to 23 characters (X shortens all URLs).

### Image cards (Website Cards)

Drive clicks with a preview image and CTA:

```
POST /12/accounts/{account_id}/cards/website

{
  "name": "Deploy Checklist Card",
  "website_title": "Free Deploy Checklist - Used by 200+ Teams",
  "website_url": "{LANDING_PAGE_URL}?utm_source=twitter&utm_medium=paid&utm_campaign={CAMPAIGN_SLUG}",
  "media_key": "{MEDIA_KEY}"
}
```

First upload the image:
```
POST https://upload.x.com/1.1/media/upload.json
Content-Type: multipart/form-data

media_data: {BASE64_IMAGE}
media_category: tweet_image
```

Image specs: 800x418px (1.91:1) or 800x800px (1:1). Max 5MB. PNG or JPG.

Use the returned `media_key` in the card creation.

### Video cards

For short-form video ads (15-30 seconds):

```
POST /12/accounts/{account_id}/cards/video_website

{
  "name": "Product Demo 15s",
  "title": "See how teams deploy 10x faster",
  "video_url": "{VIDEO_URL}",
  "website_url": "{LANDING_PAGE_URL}?utm_source=twitter&utm_medium=paid&utm_campaign={CAMPAIGN_SLUG}",
  "media_key": "{VIDEO_MEDIA_KEY}"
}
```

Video specs: MP4, H.264, AAC audio. 15s ideal, 2:20 max. Minimum 720x720px. Add captions — 85% of X video is watched muted.

## Creative Best Practices for B2B

### Hook patterns that work on X

1. **Data hook**: "We analyzed [N] [things]. Here's what we found:" — works because X users love data and contrarian takes
2. **Question hook**: "Why do [ICP role] still [painful manual process] when [better alternative exists]?" — works when the question triggers recognition
3. **Contrarian hook**: "Hot take: [common industry belief] is wrong. Here's the data:" — works for engagement and shares
4. **Thread-style hook**: Open with a bold claim, deliver in subsequent lines. Even single tweets can use line breaks to create a thread feel.

### Copy structure for promoted tweets

```
Line 1: Hook (data point, question, or bold claim) — grabs attention in the timeline
Line 2-3: Context (why this matters to the reader)
Line 4: CTA + link (what to do next)
```

### What to avoid

- Corporate jargon: "synergize", "leverage", "best-in-class"
- Stock photo image cards — use screenshots, data charts, or plain text on colored background
- Hashtags in promoted tweets (they leak clicks away from your CTA)
- Asking for a demo in an awareness-stage ad (offer value first: guide, checklist, benchmark)

## A/B Testing Creative

Create 3-5 variants per ad group to test:

| Variant | Hook Type | CTA | Goal |
|---------|----------|-----|------|
| A | Data hook | "Get the guide" | Test if data resonates |
| B | Question hook | "See the breakdown" | Test if question triggers curiosity |
| C | Contrarian take | "Read the full analysis" | Test if controversy drives clicks |
| D | Social proof | "Join 200+ teams" | Test if proof builds trust |

X Ads auto-optimizes toward the best performer within an ad group. After 500+ impressions per variant, pause variants with CTR below 0.5%. After 2,000 impressions, declare a winner and create 3 new variants inspired by the winning angle.

## Reporting on Creative Performance

```
GET /12/stats/accounts/{account_id}/promoted_tweets?granularity=DAY&metric_groups=ENGAGEMENT,BILLING

&start_time=2026-04-01T00:00:00Z&end_time=2026-04-08T00:00:00Z
&promoted_tweet_ids={PT_ID_1},{PT_ID_2}
```

Key metrics:
- `impressions`: Total views
- `engagements`: Likes + retweets + replies + clicks
- `url_clicks`: Clicks to your landing page
- `engagement_rate`: engagements / impressions (target >1% for B2B)
- `cost_per_engagement`: Total spend / engagements
- `cost_per_url_click`: Total spend / url_clicks

## Error Handling

- `MEDIA_NOT_FOUND`: Media upload failed or expired. Re-upload.
- `TWEET_TEXT_TOO_LONG`: Over 280 characters. Shorten.
- `CARD_ALREADY_ATTACHED`: Tweet already has a card. Create a new tweet.
- `INVALID_MEDIA_CATEGORY`: Wrong media type for the card. Use `tweet_image` for images, `tweet_video` for videos.
