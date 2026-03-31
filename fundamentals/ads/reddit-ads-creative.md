---
name: reddit-ads-creative
description: Create Reddit ad creative (promoted posts) optimized for authenticity and community norms
tool: Reddit
product: Reddit Ads
difficulty: Config
---

# Reddit Ads — Creative

Create ad creative for Reddit that respects community culture and outperforms generic ad copy. Reddit users are highly skeptical of overt marketing. Ads that look and feel like genuine Reddit posts dramatically outperform polished corporate creative.

## Ad Formats

### Promoted Posts (Primary for B2B)

Standard promoted posts appear in subreddit feeds and look like regular Reddit posts with a "Promoted" label. This is the workhorse format for B2B lead generation.

```
POST https://ads-api.reddit.com/api/v3/accounts/{account_id}/campaigns/{campaign_id}/adgroups/{adgroup_id}/ads
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "ad-text-post-variant-a",
  "headline": "We analyzed 500 deploys to find why Friday releases fail",
  "body": "Turns out it's not the code. It's the process. We documented the 5 patterns that cause 80% of deploy failures and built a free checklist. No signup, no email gate.",
  "click_url": "https://yoursite.com/deploy-checklist?utm_source=reddit&utm_medium=paid&utm_campaign=paid-reddit-ads&utm_content=friday-deploys",
  "call_to_action": "LEARN_MORE",
  "configured_status": "PAUSED"
}
```

### Image Ads

Promoted posts with an image thumbnail. Higher click-through rates than text-only.

```json
{
  "name": "ad-image-variant-a",
  "headline": "The deploy failure pattern nobody talks about",
  "thumbnail_url": "https://yoursite.com/images/deploy-infographic.png",
  "click_url": "https://yoursite.com/deploy-checklist?utm_source=reddit&utm_medium=paid&utm_campaign=paid-reddit-ads&utm_content=infographic",
  "call_to_action": "LEARN_MORE"
}
```

Image specs:
- Recommended: 1200x628 pixels (landscape)
- Minimum: 600x315 pixels
- Format: PNG or JPG
- File size: Under 3MB
- Avoid text-heavy images (Reddit penalizes in quality score)
- Screenshots, data visualizations, and diagrams outperform stock photos

### Video Ads

Short-form video in the feed. Best for awareness.

- Duration: 15-60 seconds (15s optimal for completion rate)
- Format: MP4 or MOV, 720p minimum
- Captions mandatory (most Reddit video is watched muted)
- Hook in first 3 seconds

### Carousel Ads

Multiple image cards users can swipe through. Good for step-by-step content.

- 2-6 cards per carousel
- Each card: 1080x1080 pixels
- Each card can have its own headline and destination URL

## Creative Principles for Reddit

Reddit audiences penalize anything that feels like a traditional ad. Follow these rules:

### 1. Write like a Redditor, not a marketer

Bad: "Unlock the power of AI-driven deployment automation with our industry-leading platform."
Good: "We tracked 500 deploys across 50 teams. Here's what actually causes Friday failures."

Use first person. Be specific. Lead with data or a story, not a value proposition.

### 2. Offer genuine value without gating

Reddit users hate email gates. Offer ungated content: free tools, public checklists, open-source resources. The landing page can have an optional email capture, but the value must be accessible without it.

### 3. Match the subreddit's tone

Ads targeting r/devops should sound technical. Ads targeting r/startups should sound founder-to-founder. Ads targeting r/smallbusiness should sound practical. Create separate ad variants for different subreddit clusters.

### 4. Use social proof that Redditors trust

Skip corporate testimonials. Use: specific numbers ("used by 200+ teams"), community recognition ("top post on HN last month"), open metrics ("our open-source tool has 5k GitHub stars").

### 5. Enable comments on promoted posts

Reddit lets users comment on promoted posts. Enable this. Respond to comments authentically. Ads with active comment threads get higher quality scores and lower CPMs. Assign a team member or schedule comment monitoring.

## Creative Testing Framework

For each subreddit cluster, create 3 ad variants:

| Variant | Hook Type | Example Headline |
|---|---|---|
| A | Data/statistic | "We analyzed 500 deploys to find why Friday releases fail" |
| B | Question | "Anyone else spending half their sprint fixing deployment issues?" |
| C | Story/result | "How we went from 3 outages/month to zero in 6 weeks" |

Run all 3 simultaneously. After 500 impressions per variant, pause any with CTR below 0.4%. After 1,000 impressions, declare a winner and create 2 new variants inspired by the winning hook type.

## UTM Parameter Standard

Every ad URL must include:

```
?utm_source=reddit&utm_medium=paid&utm_campaign=paid-reddit-ads&utm_content={variant_id}&utm_term={subreddit_cluster}
```

This enables PostHog to attribute conversions to specific ad variants and subreddit targets.

## Ad Approval and Compliance

Reddit reviews all ads before serving. Common rejection reasons:
- Misleading claims or exaggerated statistics
- Clickbait headlines that do not match landing page content
- Prohibited content (tobacco, weapons, etc.)
- Landing pages with excessive pop-ups or auto-play video with sound
- Review time: typically 24-48 hours

## Refresh Cadence

Ad creative fatigues faster on Reddit than other platforms because the same users see the same subreddits daily:
- Weeks 1-2: Run initial 3 variants per ad group
- Week 3: Replace bottom performer with a new variant
- Week 4: Refresh all variants if CTR has declined 20%+ from week 1
- Ongoing: Produce 2-3 new variants every 2 weeks
