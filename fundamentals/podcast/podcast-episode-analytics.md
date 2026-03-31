---
name: podcast-episode-analytics
description: Pull episode download counts and listener metrics from podcast hosting platforms
tool: Spotify for Podcasters / Buzzsprout / Transistor / RSS Analytics
difficulty: Config
---

# Podcast Episode Analytics

Retrieve listener/download data for episodes where the founder appeared as a guest. Since you do not control the host's podcast dashboard, this requires a combination of approaches.

## The Attribution Problem

When you are a guest, you typically do not have access to the host's download numbers. Workarounds:

1. **Ask the host**: After the episode airs, email the host and ask for download numbers at 7 days and 30 days. Most hosts will share this.
2. **Use your own tracking**: Measure inbound traffic via your UTM-tagged links (see `podcast-tracking-links` fundamental).
3. **Estimate from public data**: Use ListenNotes `listen_score` and episode count to estimate per-episode downloads.
4. **Chartable/OP3**: If the host uses prefix analytics, you may see data.

## Requesting Stats from the Host

Send this email 7 days after the episode airs:

```
Subject: Re: {{podcast_name}} episode — quick stats question

Hi {{host_first_name}},

Thanks again for having me on! The response has been great on my end.

Would you mind sharing the download numbers for our episode? I'm tracking which podcasts drive the most engagement so I can send you relevant guests in the future (win-win).

Even a rough number at 7 days and 30 days would be super helpful.

{{founder_name}}
```

The "I'll send you guests" angle gives them a reason to share.

## ListenNotes Episode Data

```http
GET https://api.listennotes.com/api/v2/episodes/{episode_id}
Header: X-ListenAPI-Key: {LISTENNOTES_API_KEY}
```

Response includes:
- `audio_length_sec`: Episode duration
- `pub_date_ms`: Publish timestamp
- `listennotes_url`: Episode page on ListenNotes

ListenNotes does not provide download counts, but the podcast-level `listen_score` combined with typical download-per-episode ratios gives a rough estimate:
- listen_score 20-30: ~100-500 downloads/episode
- listen_score 30-40: ~500-2,000 downloads/episode
- listen_score 40-50: ~2,000-5,000 downloads/episode
- listen_score 50+: ~5,000+ downloads/episode

## Spotify for Podcasters (If Host Shares Access)

Some hosts will add you as a contributor. If they do:

Dashboard URL: `https://podcasters.spotify.com/pod/dashboard/episodes`

Key metrics:
- Starts: Number of listeners who pressed play
- Streams: Total stream count
- Listeners: Unique listeners
- Completion rate: % who listened to >90% of the episode
- Audience demographics: Age, gender, geography

## Your Own Analytics (Primary Measurement)

Since you control your own website and CRM, measure podcast impact through:

1. **PostHog referral traffic**: Filter `$pageview` events by `utm_source=podcast` and `utm_campaign={{podcast_slug}}`
2. **Lead attribution**: Count `lead_created` events where `utm_source=podcast`
3. **Meeting attribution**: Count `meeting_booked` events from podcast referral traffic
4. **Direct traffic spike**: Compare your site's direct traffic in the 48 hours after episode air date vs. baseline — podcast listeners often type the URL directly

## Tracking Spreadsheet Schema

Maintain a tracking record per episode:

| Field | Example |
|-------|---------|
| Podcast name | The SaaS Podcast |
| Episode air date | 2026-04-15 |
| Host-reported downloads (7d) | 1,200 |
| Host-reported downloads (30d) | 3,400 |
| UTM clicks (7d) | 45 |
| UTM clicks (30d) | 82 |
| Leads attributed | 3 |
| Meetings attributed | 1 |
| Notes | Strong audience fit, host offered return invite |

Store this in Attio as notes on a "Podcast Appearances" list, or in a dedicated Clay table for analysis.

## Error Handling

- **Host won't share stats**: Rely entirely on your own UTM tracking and traffic spike analysis
- **Episode not yet indexed on ListenNotes**: Wait 24-48 hours after publish. ListenNotes crawls RSS feeds periodically.
- **No UTM traffic despite airing**: Check that the vanity URL redirect is working. Check if the host included the link in show notes. If not, ask them to add it.
