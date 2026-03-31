---
name: podcast-episode-repurposing
description: Extract short clips, audiograms, show notes, and social posts from a podcast episode recording
tool: Descript
difficulty: Config
---

# Podcast Episode Repurposing

Take a completed podcast episode recording and systematically extract derivative content: short video/audio clips, audiograms, blog-format show notes, pull quotes, and social posts. Each episode should produce 8-15 pieces of distribution content.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| Descript | Text-based editing, auto-transcription, clip extraction | Full control over edits, highest quality |
| Riverside | Built-in clips feature, separate tracks | Quick clips during/after recording |
| Opus Clip | AI-powered clip detection from long-form video | Automated viral clip extraction |
| Headliner | Audiogram generator (waveform + captions + image) | Audio-only podcast social clips |
| Castmagic | AI show notes + social posts from transcript | Automated written content extraction |

## Step 1: Transcribe the episode

Use Descript or your recording platform's built-in transcription:

### Descript transcription
1. Import the audio/video file into Descript
2. Descript auto-transcribes (typically 95%+ accuracy)
3. Review and correct speaker labels and key terms (product names, technical terms)
4. Export the corrected transcript as plain text and SRT (for captions)

### Alternative: Deepgram API (for programmatic transcription)
```http
POST https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&diarize=true
Authorization: Token {DEEPGRAM_API_KEY}
Content-Type: audio/mp3

{binary audio data}
```

Returns: JSON with `words` array (each word with start/end timestamp and speaker label). Pricing: $0.0043/min (Nova-2).

## Step 2: Extract short clips (video podcasts)

Identify 3-5 compelling moments from the transcript. Target clips are:
- **30-60 seconds** for LinkedIn, Twitter, Instagram Reels
- **60-90 seconds** for YouTube Shorts
- **2-3 minutes** for standalone LinkedIn video posts

Selection criteria for clip-worthy moments:
- Contrarian or surprising statement
- Specific data point or metric shared
- Actionable framework or tactic
- Emotional story or personal anecdote
- Guest's most quotable soundbite

### Descript clip extraction
1. In the transcript, highlight the text corresponding to the clip
2. Right-click > "Create new composition from selection"
3. Add a title card (topic/hook as text overlay)
4. Enable auto-captions (burned-in for social, SRT for YouTube)
5. Resize canvas: 1080x1920 (vertical) for Reels/Shorts, 1080x1080 (square) for feed posts
6. Export as MP4 at 1080p

### Opus Clip (automated extraction)
```
1. Upload full episode video to Opus Clip (opusclip.com)
2. Opus Clip's AI identifies high-engagement moments
3. Review the suggested clips — accept, reject, or adjust boundaries
4. Export selected clips with auto-captions
```

Pricing: Free tier (120 min/month), Pro $19/mo (unlimited).

## Step 3: Create audiograms (audio-only podcasts)

For audio-only podcasts, generate audiograms — animated waveform videos with captions:

### Headliner
1. Upload the episode audio to Headliner (headliner.app)
2. Select the segment to use (30-60 seconds)
3. Choose a background image or video (use episode cover art or custom branded template)
4. Headliner auto-generates captions from the audio
5. Customize colors, fonts, and waveform style to match your brand
6. Export as MP4 in platform-appropriate dimensions

Pricing: Free (5 audiograms/month), Pro $15/mo (unlimited).

### Alternative: ffmpeg + transcript (programmatic)
```bash
ffmpeg -i clip.mp3 -filter_complex \
  "[0:a]showwaves=s=1080x400:mode=cline:colors=white[wave]; \
   color=c=#1a1a2e:s=1080x1920:d=$(ffprobe -show_entries format=duration -of csv=p=0 clip.mp3)[bg]; \
   [bg][wave]overlay=(W-w)/2:(H-h)/2[out]" \
  -map "[out]" -map 0:a -c:v libx264 -c:a aac audiogram.mp4
```

## Step 4: Generate show notes

Transform the transcript into structured show notes for the episode page:

### Show notes template
```markdown
## Episode {{number}}: {{title}}

{{1-2 paragraph summary of the episode's key theme}}

### Key Takeaways
1. {{Takeaway 1 — 1-2 sentences}}
2. {{Takeaway 2 — 1-2 sentences}}
3. {{Takeaway 3 — 1-2 sentences}}

### Timestamps
- 00:00 — Introduction
- {{MM:SS}} — {{Topic discussed}}
- {{MM:SS}} — {{Topic discussed}}
- {{MM:SS}} — {{Topic discussed}}

### Resources Mentioned
- {{Resource 1}} — {{URL}}
- {{Resource 2}} — {{URL}}

### Connect
- {{Guest name}}: {{LinkedIn URL}} | {{Twitter URL}}
- {{Host name}}: {{LinkedIn URL}} | {{Twitter URL}}
- {{Product}}: {{website URL with UTM tracking}}
```

### Castmagic (automated show notes)
1. Upload audio to Castmagic (castmagic.io)
2. Castmagic generates: episode summary, key takeaways, timestamps, social posts, newsletter blurb, blog draft
3. Review and edit the outputs
4. Export to your CMS or copy into your hosting platform's episode description

Pricing: $23/mo (Starter), $49/mo (Pro).

## Step 5: Extract social post copy

From each episode, generate:

- **3 LinkedIn posts**: Each built around a single key insight. Use the hook-story-takeaway format. Reference the episode with a link.
- **3 Twitter/X posts**: Sharper, more provocative versions of the same insights. Under 280 characters for the hook, thread format optional.
- **1 newsletter blurb**: 100-150 words summarizing why someone should listen, with a direct link to the episode.
- **3-5 pull quotes**: Quotable sentences from the guest or host, formatted as image cards (use Canva API or a template).

### Pull quote image generation (Canva or programmatic)
Create a branded template with:
- Background: solid color or gradient matching your podcast brand
- Quote text: the pull quote in a large, readable font
- Attribution: guest name, episode number
- Podcast logo in corner

Export as 1080x1080 PNG for social sharing.

## Output per episode

| Asset | Count | Platform |
|-------|-------|----------|
| Short video clips | 3-5 | LinkedIn, Twitter, YouTube Shorts, Reels |
| Audiograms | 2-3 | LinkedIn, Twitter (audio podcasts only) |
| Show notes | 1 | Podcast website, hosting platform |
| LinkedIn posts | 3 | LinkedIn |
| Twitter posts | 3 | Twitter/X |
| Newsletter blurb | 1 | Email newsletter |
| Pull quote images | 3-5 | LinkedIn, Twitter, Instagram |

Total: 16-21 content pieces from a single episode.

## Error Handling

- **Transcript accuracy low**: Common with technical jargon or accents. Manually review first 5 minutes and add custom vocabulary to Descript/Deepgram.
- **Clip lacks context**: Add a 1-sentence title card at the start of each clip to set context. Viewers dropping into a 45-second clip need to understand what's being discussed.
- **Audiogram file too large**: Compress with `ffmpeg -i input.mp4 -b:v 1M -maxrate 1.5M output.mp4`. Target <15MB for Twitter, <100MB for LinkedIn.
