---
name: youtube-video-publish
description: Record, edit, optimize metadata, generate captions, and upload a video to YouTube with full SEO optimization
category: YouTube
tools:
  - OBS
  - Descript
  - YouTube Data API v3
fundamentals:
  - obs-recording-setup
  - descript-editing
  - descript-transcription
  - descript-clips
  - youtube-data-api-upload
  - youtube-data-api-metadata
  - youtube-captions-api
---

# YouTube Video Publish

End-to-end workflow: take a video topic from the keyword research calendar, record it, edit it, optimize all metadata for YouTube search, upload it, and set up captions. One run of this drill produces one published YouTube video.

## Input

- One row from the keyword matrix (target_keyword, video_title, content_angle, target_duration, related_keywords, cta)
- Recording environment set up (OBS configured via `obs-recording-setup`)
- YouTube channel with OAuth credentials configured

## Steps

### 1. Script the video

Write a structured outline based on the keyword matrix entry:

```
Hook (0:00-0:15): State the problem or question the viewer searched for.
                   Mention the target keyword naturally.
                   Promise what they'll learn by the end.

Body (0:15-{duration-0:45}):
  - Point 1: {first key insight}
  - Point 2: {second key insight}
  - Point 3: {third key insight}
  Include related_keywords naturally in speech (YouTube indexes spoken words via auto-captions).

CTA (last 30-45 seconds):
  - Summarize the key takeaway in one sentence
  - State the CTA: "{cta from keyword matrix}"
  - Ask viewers to subscribe and hit the bell
  - Mention the next video in the series (if applicable)
```

Store the script for caption correction later.

### 2. Record with OBS

Using the `obs-recording-setup` fundamental:

1. Start OBS with the configured scene (screen capture + webcam overlay for tutorials, webcam-only for thought leadership)
2. Record the video following the script outline
3. Aim for the `target_duration` from the keyword matrix. YouTube search favors videos 8-15 minutes for tutorial content, 3-7 minutes for quick tips
4. Record in one take if possible. Mark mistakes with a clap or verbal "retake" for easy editing

**Human action required:** The founder or subject matter expert must record the video. The agent prepares the script, configures OBS, and handles everything after recording.

### 3. Edit in Descript

Using the `descript-editing` fundamental:

1. Import the OBS recording into Descript
2. Descript auto-transcribes the audio
3. Edit the transcript to edit the video: remove filler words, long pauses, false starts, and "retake" sections
4. Trim the intro to start strong (no "hey guys, um, so today...")
5. Add chapter markers at each major section transition
6. Export the final video as MP4 (1080p, H.264)
7. Export the transcript as SRT for caption upload

Using the `descript-clips` fundamental:

8. Identify 2-3 compelling 30-60 second segments
9. Create vertical (1080x1920) clip versions with burned-in captions for YouTube Shorts, LinkedIn, Twitter
10. Export clips separately for cross-platform distribution

### 4. Optimize metadata for YouTube SEO

Using the keyword matrix data, prepare the upload metadata:

**Title** (max 100 chars, target keyword in first 60):
```
{target_keyword} — {unique angle or benefit}
```
Example: "How to Build an AI Agent in 10 Minutes — No Code Required"

**Description** (max 5000 chars):
```
Line 1: Restate the target keyword + what the viewer will learn
Line 2: Brief summary with related_keywords included

(blank line)

Timestamps:
0:00 Introduction
{chapter_time} {chapter_title}
...

(blank line)

{2-3 paragraphs expanding on the topic, naturally including related_keywords}

(blank line)

Resources mentioned:
- {link 1}
- {link 2}

(blank line)

Connect with us:
- Website: {url}
- LinkedIn: {url}
- Twitter: {url}
```

**Tags** (max 500 chars total):
Include: target_keyword, related_keywords, brand name, category terms. Order matters — put the target keyword first.

**Thumbnail:**
Design or generate a custom thumbnail. Requirements:
- 1280x720 pixels, 16:9 aspect ratio
- Large text readable at small sizes (the video title keyword or a compelling question)
- Human face with expressive emotion (increases CTR 30%+)
- High contrast colors that stand out in search results
- Consistent visual style across all channel videos

**Human action required:** Approve or adjust the thumbnail before upload.

### 5. Upload to YouTube

Using the `youtube-data-api-upload` fundamental:

1. Initiate resumable upload with the optimized metadata
2. Upload the video file
3. Set privacy to `private` initially (review before publishing)
4. Set `publishAt` to the scheduled time from the content calendar
5. Store the returned video ID for caption upload and tracking

### 6. Upload corrected captions

Using the `youtube-captions-api` fundamental:

1. Wait 1-2 hours for YouTube's auto-captions to generate
2. Download the auto-generated caption track
3. Compare against the Descript SRT export (which was corrected during editing)
4. Upload the corrected SRT as the primary English caption track
5. This replaces the error-prone auto-captions with accurate text that YouTube indexes for search

### 7. Configure end screens and cards

Using the `youtube-data-api-metadata` fundamental, note that end screens and cards must be set via YouTube Studio (no API support). Flag for manual setup:

**Human action required:** In YouTube Studio, add:
- End screen (last 20 seconds): subscribe button + "best for viewer" video suggestion
- Cards: link to related videos or playlists at relevant chapter points

### 8. Set to public

Once everything is configured:
- Change privacy status to `public` (or confirm the `publishAt` schedule)
- Share the video URL to your distribution channels

## Output

- One published YouTube video with optimized title, description, tags, thumbnail, and captions
- 2-3 short-form clips ready for cross-platform distribution
- Video ID stored for analytics tracking

## Triggers

- Run once per video in the content calendar
- Typically 1-2 times per week during Baseline and Scalable levels
