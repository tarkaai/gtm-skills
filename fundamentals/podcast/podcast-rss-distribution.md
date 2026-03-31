---
name: podcast-rss-distribution
description: Submit and manage podcast RSS feed listings across Apple Podcasts, Spotify, and other major directories
tool: Apple Podcasts Connect / Spotify for Podcasters / Google Podcasts Manager
difficulty: Setup
---

# Podcast RSS Distribution

Submit your podcast RSS feed to all major directories so listeners can find and subscribe to your show. This is a one-time setup per directory, after which new episodes auto-distribute via the RSS feed.

## Directory Submission Checklist

| Directory | Submission URL | Indexing Time | Audience Share |
|-----------|---------------|---------------|----------------|
| Apple Podcasts | `https://podcastsconnect.apple.com` | 1-5 days | ~35-40% of listeners |
| Spotify | `https://podcasters.spotify.com` | 1-3 days | ~30-35% of listeners |
| YouTube Music / YouTube | `https://studio.youtube.com` | 2-7 days | ~10-15% of listeners |
| Amazon Music / Audible | `https://podcasters.amazon.com` | 3-5 days | ~5-8% of listeners |
| Pocket Casts | Auto-indexed from Apple Podcasts | Automatic | ~3% of listeners |
| Overcast | Auto-indexed from Apple Podcasts | Automatic | ~2% of listeners |
| Castro | Auto-indexed from Apple Podcasts | Automatic | ~1% of listeners |
| Stitcher | Discontinued (merged into SiriusXM) | N/A | N/A |

Most smaller directories auto-index from Apple Podcasts. Submitting to Apple, Spotify, YouTube, and Amazon covers ~90% of listeners.

## Apple Podcasts Connect

### Step 1: Submit RSS feed

1. Sign in at `https://podcastsconnect.apple.com` with an Apple ID
2. Click the "+" button, select "New Show"
3. Paste your RSS feed URL (from your hosting platform)
4. Apple validates the feed: checks for required tags (`<itunes:image>`, `<itunes:category>`, `<itunes:author>`, `<itunes:owner>`)
5. If validation passes, submit for review

### Step 2: Verify ownership

Apple sends a verification email to the `<itunes:owner><itunes:email>` address in your RSS feed. Click the verification link.

### Step 3: Wait for review

Apple reviews new podcasts within 1-5 business days. Common rejection reasons:
- Missing or low-quality cover art (must be 3000x3000px, RGB, JPEG or PNG)
- Fewer than 1 episode published
- Description or title contains prohibited content
- RSS feed is malformed

### Step 4: Confirm listing

After approval, your show appears on Apple Podcasts. Note your Apple Podcasts URL: `https://podcasts.apple.com/podcast/id{APPLE_PODCAST_ID}`. Use this in marketing materials and show notes.

### Apple Podcasts API (for analytics)

```http
GET https://amp-api.podcasts.apple.com/v1/catalog/us/podcasts/{APPLE_PODCAST_ID}
```

Note: Apple Podcasts Connect provides a web dashboard for analytics (downloads, listeners, follower count, episode completion rates). There is no public REST API for analytics -- use the dashboard or scrape via Playwright.

## Spotify for Podcasters

### Step 1: Submit RSS feed

1. Sign in at `https://podcasters.spotify.com`
2. Click "Get Started" > "I have a podcast"
3. Paste your RSS feed URL
4. Spotify verifies the feed and sends a verification code to the email in the RSS

### Step 2: Claim your podcast

Enter the verification code. Spotify connects the feed to your Podcasters account.

### Step 3: Configure Spotify-specific settings

- Enable video episodes (if recording video)
- Set up Q&A and polls (Spotify-exclusive engagement features)
- Enable listener comments

Spotify typically indexes new shows within 1-3 days. Ongoing episodes appear within a few hours of RSS feed update.

### Spotify Analytics Dashboard

Key metrics available at `https://podcasters.spotify.com/pod/dashboard/episodes`:
- Starts (play button pressed)
- Streams (>60 seconds listened)
- Listeners (unique)
- Followers gained/lost
- Average consumption rate (% of episode listened)
- Audience demographics (age, gender, geography)
- Listening device breakdown

## YouTube / YouTube Music

### Step 1: Connect RSS feed

1. Go to `https://studio.youtube.com`
2. Navigate to Settings > Upload Defaults
3. Under Podcast settings, link your RSS feed

YouTube converts audio episodes into video posts with your cover art. If you record video, upload full video episodes directly.

### Alternative: Upload video episodes directly

For video podcasts, upload full-length episodes to YouTube as regular videos. Add them to a Podcast playlist. YouTube treats playlists marked as "Podcast" differently in search and recommendations.

## Amazon Music / Audible

### Step 1: Submit RSS feed

1. Go to `https://podcasters.amazon.com`
2. Sign in with an Amazon account
3. Click "Add Your Podcast"
4. Paste RSS feed URL, verify ownership via email

Amazon typically indexes within 3-5 business days.

## Automated Submission via Hosting Platform

Most hosting platforms (Buzzsprout, Transistor) offer one-click directory submission from their dashboard. This is the simplest path:

1. In your hosting platform's distribution settings, click "Submit to Apple Podcasts"
2. The platform handles the RSS validation and submission
3. Repeat for Spotify, Amazon, and other directories
4. The platform tracks which directories your show is listed on

## Monitoring Directory Listings

After initial submission, periodically verify your show is active and displaying correctly:

1. Search for your show name on each directory's app/website
2. Confirm cover art, description, and latest episodes are current
3. Check for listener reviews on Apple Podcasts (reviews affect ranking)
4. Monitor Apple Podcasts chart position in your category

## Error Handling

- **Feed validation fails**: Check your RSS with `https://castfeedvalidator.com/` -- it shows exactly which tags are missing or malformed
- **Show not appearing after 7 days**: Re-submit. If still blocked, email the directory's support (Apple: `podcasts@apple.com`)
- **Episodes not updating**: Verify your hosting platform's RSS feed includes the new episode. Some platforms cache the feed -- force a refresh.
- **Wrong cover art showing**: Directories cache images aggressively. Upload a new image file (do not overwrite the same URL) and update the RSS `<itunes:image>` tag.
