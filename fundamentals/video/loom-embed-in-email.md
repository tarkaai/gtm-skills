---
name: loom-embed-in-email
description: Embed Loom video GIF thumbnails in cold emails for high-engagement outreach
tool: Loom
product: Loom
difficulty: Setup
---

# Embed Loom Video in Cold Email

Email clients (Gmail, Outlook, Apple Mail) do not support embedded video players. The correct approach is to embed an animated GIF thumbnail that links to the Loom video page. This keeps the email lightweight (good deliverability) while giving the visual impact of video in the inbox.

## Prerequisites

- Loom video recorded and available at `https://www.loom.com/share/{video-id}`
- Cold email tool (Instantly, Smartlead, or equivalent) for campaign management
- Email sending domain with healthy warmup (2+ weeks, 50+ daily sends)

## Steps

### 1. Get the GIF thumbnail from Loom

For each Loom video:

1. Open the video in your Loom dashboard
2. Click "Share" button
3. Select "Embed" tab
4. Click "Copy GIF Thumbnail"
5. This copies an HTML snippet to your clipboard containing an animated GIF preview linked to the video

The GIF URL format is: `https://cdn.loom.com/sessions/thumbnails/{video-id}-with-play.gif`

The direct link to the video is: `https://www.loom.com/share/{video-id}`

### 2. Build the email HTML with thumbnail

For Instantly campaigns, construct the email body with the GIF embedded as a clickable image:

```html
<p>Hey {first_name},</p>

<p>I recorded a quick video for you — takes 60 seconds:</p>

<a href="https://www.loom.com/share/{video-id}?utm_source=instantly&utm_medium=email&utm_campaign={campaign-slug}">
  <img src="https://cdn.loom.com/sessions/thumbnails/{video-id}-with-play.gif"
       alt="Watch my video for {first_name}"
       width="400"
       style="border-radius: 8px; border: 1px solid #e0e0e0;" />
</a>

<p>{one-line context sentence referencing their company or signal}</p>

<p>{your_name}<br>{your_title}, {your_company}</p>
```

### 3. Configure in Instantly

1. Create a new campaign in Instantly
2. In the email editor, switch to HTML mode
3. Paste the HTML template above
4. Map merge fields: `{first_name}`, `{video-id}`, `{campaign-slug}`, context sentence
5. For personalized videos (one per prospect): each row in your prospect CSV must include the unique Loom video-id
6. For semi-personalized (one video per ICP segment): use the same video-id for all prospects in that segment

### 4. Deliverability safeguards

- **Image-to-text ratio:** Keep at least 2 lines of plain text above and below the GIF. Email filters flag image-heavy emails.
- **GIF file size:** Loom's default thumbnails are optimized (<500KB). Do not use custom GIFs above 1MB.
- **Alt text:** Always include descriptive alt text on the image tag. Some email clients block images by default.
- **Link tracking:** Instantly wraps links for tracking. Verify the Loom link still resolves correctly after Instantly's redirect.
- **Test send:** Send a test to yourself on Gmail, Outlook, and Apple Mail before launching. Verify the GIF displays and the link opens the Loom video.

### 5. Track clicks

Instantly's built-in link tracking will capture when a prospect clicks the Loom thumbnail. Log this event as `video_email_clicked` in PostHog via n8n webhook. The Loom video page itself tracks view duration if the viewer is identified.

## Merge Field Reference

| Field | Source | Example |
|-------|--------|---------|
| `{first_name}` | Clay/Apollo enrichment | Jane |
| `{video-id}` | Loom dashboard after recording | abc123def456 |
| `{campaign-slug}` | Your campaign naming convention | q1-outbound-devtools |
| Context sentence | Clay AI-generated personalization | "Saw Acme just closed Series B — congrats!" |

## Error Handling

- If GIF fails to render: the alt text displays as a clickable link (still functional)
- If Loom video is deleted: the link returns a 404. Always verify videos exist before campaign launch
- If email lands in spam: reduce image size, add more plain text, check domain reputation with mail-tester.com
