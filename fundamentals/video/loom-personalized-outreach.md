---
name: loom-personalized-outreach
description: Record personalized Loom videos for prospect outreach with naming conventions and CTA configuration
tool: Loom
product: Loom
difficulty: Setup
---

# Record Personalized Loom Videos for Prospect Outreach

Record short (60-120 second) personalized Loom videos addressed to individual prospects. These are NOT generic demos. Each video references the prospect by name, their company, and a specific pain point or signal discovered during enrichment.

## Prerequisites

- Loom Business account ($15/user/month) for unlimited recordings and CTA buttons
- Prospect list with enrichment data: name, company, role, pain point, recent signal
- Cal.com booking link for CTA button
- Quiet environment with webcam and mic

## Steps

### 1. Prepare the recording template

Before batch-recording, create a repeatable structure for each video:

- **Opening (5-10 sec):** "Hey {first_name}, this is {your_name} from {your_company}."
- **Hook (10-15 sec):** Reference a specific signal or pain point: "I saw {company} just {signal — raised a round, hired for X, launched Y}..."
- **Value prop (20-30 sec):** Connect the signal to your product: "We help companies like yours {specific outcome} by {mechanism}."
- **Proof (15-20 sec):** Brief social proof: "We helped {similar_company} achieve {result} in {timeframe}."
- **CTA (10 sec):** "I'd love to show you how — there's a link below to grab 15 minutes."
- **Total: 60-90 seconds.** Never exceed 120 seconds for outbound.

### 2. Configure Loom workspace settings

1. Open Loom desktop app > Preferences
2. Set default recording mode: Camera + Screen (screen shows prospect's website/LinkedIn as visual backdrop)
3. Set default privacy: "Anyone with the link"
4. Enable viewer identity: captures email of viewers who are logged into Loom
5. Set workspace folder: create a folder named `outbound-video/{campaign-date}`

### 3. Record each video

For each prospect in your batch:

1. Open the prospect's company website or LinkedIn profile on screen (visual personalization the viewer sees immediately)
2. Hit record in Loom
3. Follow the template structure above, substituting prospect-specific details from your enrichment data
4. Stop recording
5. In the Loom editor: trim dead space at start/end
6. Name the video: `{company}-{first_name}-{campaign_slug}` (e.g., `acme-jane-q1-outbound`)

### 4. Add CTA button to each video

1. Open the Loom video page
2. Click "Add a call to action" in the right panel
3. Set CTA type: "Link"
4. Set CTA text: "Book 15 Minutes" (or your preferred copy)
5. Set CTA URL: your Cal.com booking link with UTM params: `https://cal.com/{you}/15min?utm_source=loom&utm_medium=video&utm_campaign={campaign_slug}`
6. Enable "Show CTA at end of video"

### 5. Copy the share link

The share URL format is: `https://www.loom.com/share/{video-id}`

Copy this link. You will embed it in your outreach email using the `loom-embed-in-email` fundamental.

### 6. Batch recording workflow

For recording 10-20 videos in a session:

1. Print or display your prospect list with enrichment data side by side
2. Pre-open each prospect's website in browser tabs
3. Record sequentially, switching tabs between recordings
4. Target: 2-3 minutes per video including setup and trimming
5. A 20-prospect batch should take 40-60 minutes

## Naming Convention

All Loom videos for outbound MUST follow: `{company}-{firstname}-{campaign-slug}`

This enables searching and filtering in the Loom dashboard and matching videos to prospects in your CRM.

## Error Handling

- If recording fails mid-video, delete and re-record (partial videos are worse than none)
- If prospect's website is down, use their LinkedIn profile instead
- If you stumble on the prospect's name, re-record — mispronouncing their name kills personalization trust
