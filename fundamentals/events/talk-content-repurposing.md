---
name: talk-content-repurposing
description: Extract blog posts, social clips, and quote graphics from recorded conference talks using AI transcription and editing
tool: Descript
product: Descript
difficulty: Config
---

# Talk Content Repurposing

Transform a recorded conference talk into multiple content assets: blog post, social media clips, quote graphics, and a companion resource page. This fundamental takes a talk recording and produces a structured content package.

## Authentication

- Descript account (Creator plan or above for full transcription)
- Alternative: Fireflies.ai for transcription-only workflow
- Alternative: Riverside.fm if you recorded the talk yourself

## Method 1: Descript (Recommended)

### Step 1: Import and Transcribe

1. Import the talk recording into a Descript project
2. Descript auto-transcribes the video with speaker identification
3. Review and correct any transcription errors (especially product names, technical terms)

### Step 2: Extract Blog Post

1. Export the full corrected transcript as plain text
2. Feed transcript to Claude API:

```
POST https://api.anthropic.com/v1/messages
Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "Convert this conference talk transcript into a blog post.\n\nRules:\n- Keep the conversational tone but remove filler words and verbal tics\n- Add section headers matching the talk's natural structure\n- Include code examples if mentioned in the talk\n- Add a TL;DR at the top with the 3 key takeaways\n- End with a CTA to the companion resource (link placeholder: {resource_url})\n- Target 1,200-1,800 words\n\nTranscript:\n{transcript}"
  }]
}
```

### Step 3: Extract Social Clips

In Descript, use text-based editing to find clip-worthy segments:

1. Search the transcript for: strong opinions, surprising data points, counterintuitive advice, memorable one-liners
2. For each clip candidate, select the text range in Descript (this selects the corresponding video)
3. Export as individual video clips (30-90 seconds each, 1080x1080 for LinkedIn/Twitter, 1080x1920 for vertical)
4. Add captions using Descript's auto-caption feature
5. Target: 3-5 clips per talk

### Step 4: Extract Quote Graphics

From the transcript, extract 3-5 quotable statements. For each quote:

1. The quote text (under 150 characters for readability)
2. Speaker name and title
3. Conference name and date
4. These feed into a design tool (Figma, Canva API, or HTML/CSS generation) for social graphics

## Method 2: Fireflies.ai (Transcription Only)

If you only have audio or do not need video clips:

1. Upload the recording to Fireflies via API:
   ```
   POST https://api.fireflies.ai/graphql
   Headers: Authorization: Bearer {FIREFLIES_API_KEY}
   Body: mutation { uploadAudio(input: { url: "{recording_url}", title: "{talk_title}" }) { id } }
   ```
2. Poll for transcription completion
3. Retrieve transcript via: `query { transcript(id: "{id}") { sentences { text start_time end_time speaker_name } } }`
4. Use the timestamped transcript to identify clip boundaries, then extract from the original recording using ffmpeg

## Method 3: Manual with ffmpeg

If no editing platform is available:

1. Transcribe with Whisper API or Deepgram
2. Identify clip timestamps from transcript
3. Extract clips: `ffmpeg -i talk.mp4 -ss {start} -to {end} -c copy clip_{n}.mp4`
4. Add captions: `ffmpeg -i clip.mp4 -vf "subtitles=captions.srt" clip_captioned.mp4`

## Output Format

Each repurposed talk produces:

| Asset | Format | Quantity |
|-------|--------|----------|
| Blog post | Markdown | 1 |
| Video clips (square) | MP4 1080x1080 | 3-5 |
| Video clips (vertical) | MP4 1080x1920 | 3-5 |
| Quote graphics | PNG 1200x1200 | 3-5 |
| Full transcript | Plain text | 1 |

## Error Handling

- If transcription quality is low (technical jargon mangled), manually correct the 20% of words that carry 80% of the meaning before generating blog post
- If talk recording has poor audio, run through Descript Studio Sound or Adobe Podcast Enhance before transcribing
- If no video exists (audio-only), produce blog post + quote graphics only; skip video clips
