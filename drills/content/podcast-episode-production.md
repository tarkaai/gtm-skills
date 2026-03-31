---
name: podcast-episode-production
description: End-to-end workflow for recording, editing, and publishing a single podcast episode
category: Podcast
tools:
  - Riverside
  - Descript
  - Buzzsprout
  - Transistor
fundamentals:
  - riverside-recording
  - descript-editing
  - descript-transcription
  - podcast-hosting-platform
---

# Podcast Episode Production

This drill covers the full lifecycle of producing a single podcast episode: scheduling the recording, recording the session, editing the audio/video, writing metadata, and publishing to your hosting platform.

## Input

- Episode topic and guest (if interview format) confirmed
- Talking points or question list prepared (see `podcast-guest-preparation` drill for guest-facing prep)
- Recording date and time confirmed with guest
- Hosting platform account configured (Buzzsprout/Transistor)

## Steps

### 1. Set up the recording session

Use `riverside-recording` to configure a Riverside studio for the episode:
- Create a new studio session named `{podcast-name}-ep{number}-{guest-last-name}`
- Set recording quality to highest available (4K video if video podcast, 48kHz audio)
- Generate and send the guest join link at least 24 hours before recording
- Test your own audio/video setup 15 minutes before the scheduled time

For audio-only podcasts, Riverside is still recommended over Zoom/Google Meet because it records locally on each participant's device, producing higher-quality separated tracks.

### 2. Record the episode

During recording:
- Start with 10 seconds of silence (room tone) for noise reduction in editing
- Do a brief audio check with the guest: "Can you hear me clearly? Can you confirm your mic is working?"
- Record the intro separately (or mark the timestamp where the real conversation begins)
- Use Riverside's timestamp feature to mark key moments during the conversation
- If a segment needs a re-take, note the timestamp and re-record. Editing out bad takes is easier than trying to salvage them.
- Record for 1.2x your target episode length (a 30-minute episode needs ~36 minutes of raw audio to allow for cuts)

### 3. Download and organize files

After recording:
1. Download all tracks from Riverside: host audio, guest audio, combined audio, video (if applicable)
2. Name files consistently: `ep{number}_{guest-name}_{track-type}.{ext}`
3. Store in a consistent folder structure: `episodes/ep{number}/raw/`

### 4. Edit the episode

Use `descript-editing` to edit the episode:
1. Import the combined audio (or video) into Descript
2. Descript auto-transcribes the recording
3. Edit by deleting text in the transcript — Descript removes the corresponding audio:
   - Remove filler words ("um", "uh", "like", "you know") using Descript's auto-filler-word removal
   - Cut tangents, repeated points, and long pauses
   - Remove the pre-recording audio check and any off-topic chatter
   - Tighten transitions between topics
4. Add intro and outro music/clips (import pre-recorded brand assets)
5. Level audio volumes across speakers (Descript's Studio Sound feature normalizes automatically)
6. Export the final episode as:
   - MP3 at 128kbps mono for podcast platforms (standard podcast format)
   - WAV at 44.1kHz/16-bit as archive
   - MP4 at 1080p if video podcast

### 5. Write episode metadata

Prepare the metadata for publishing:

```
Title: {Episode number}: {Episode title} with {Guest name}
Description: {2-3 paragraph description with key topics covered, guest bio, and links}
Summary: {1-2 sentence hook that makes someone want to listen}
Tags: {3-5 relevant topic tags}
Season: {season number}
Episode number: {sequential episode number}
Explicit: false
Published at: {scheduled publish datetime, typically Tuesday or Wednesday 6am ET}
```

Optimal publish days for B2B podcasts: Tuesday, Wednesday, or Thursday morning. Avoid Mondays (inbox overload) and Fridays (weekend mode).

### 6. Publish to hosting platform

Use `podcast-hosting-platform` to upload and publish:
1. Upload the final MP3 to your hosting platform (Buzzsprout or Transistor)
2. Set all metadata fields from step 5
3. Upload episode-specific cover art if applicable (some shows use unique art per episode)
4. Set the publish time (schedule for optimal day/time)
5. Verify the episode appears correctly in the RSS feed
6. Confirm the episode propagates to Apple Podcasts and Spotify (typically within 1-4 hours of RSS update)

### 7. Create the episode page

If your podcast has a dedicated website (Ghost, Webflow, or hosted on the platform):
1. Create a new page for the episode with show notes (see `podcast-episode-repurposing` fundamental for show notes template)
2. Embed the podcast player (most hosting platforms provide an embed code)
3. Include timestamps, key takeaways, resources mentioned, and guest links
4. Add a CTA: newsletter signup, free resource, or product link with UTM tracking

## Output

- Published episode live on all podcast directories via RSS
- Episode page with show notes on your website
- Raw recordings archived for future clip extraction
- Episode metadata logged in your CRM (Attio) for performance tracking

## Triggers

- Run once per episode, starting 1-2 days before the scheduled recording date
- For weekly podcasts, this drill runs weekly on a consistent schedule
