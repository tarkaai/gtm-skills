---
name: youtube-preroll-creative-pipeline
description: Produce, test, and iterate YouTube pre-roll video ad creatives with variant briefs, companion banners, and landing page CTAs
category: Paid
tools:
  - Google Ads
  - Anthropic
  - Descript
  - YouTube
fundamentals:
  - google-ads-youtube-creative
  - google-ads-youtube-video-campaign
  - google-ads-youtube-reporting
  - ai-content-ghostwriting
---

# YouTube Pre-roll Creative Pipeline

This drill produces video ad creatives for YouTube pre-roll campaigns targeting problem-aware prospects. The agent does NOT produce video (that requires human action). The agent produces structured creative briefs, scripts, CTA copy, companion banner copy, and landing page UTM schemes. It also manages the testing rotation: tracking which variants are live, when to pause fatigued creatives, and which patterns to replicate.

## Prerequisites

- Pain points documented from ICP research (2-3 specific problems)
- Google Ads Video campaign set up (see `google-ads-youtube-video-campaign`)
- Video production capability (Descript, Loom, Synthesia, or professional videographer)
- Companion banner design tool (Canva, Figma, or similar)

## Input

- ICP pain points: 2-3 problem statements your audience faces
- Brand voice guidelines (if any)
- Existing ad performance data (if iterating from previous creative)
- Landing page URL for the CTA destination

## Steps

### 1. Define the creative matrix

For each pain point, generate 3 hook variants. This gives you a structured test matrix:

| Pain Point | Stat Hook | Question Hook | Proof Hook |
|---|---|---|---|
| Pain Point 1 | PP1-Stat | PP1-Question | PP1-Proof |
| Pain Point 2 | PP2-Stat | PP2-Question | PP2-Proof |
| Pain Point 3 | PP3-Stat | PP3-Question | PP3-Proof |

For Smoke, produce 3 variants (one per hook type on your strongest pain point).
For Baseline, produce 6-9 variants (all hooks on 2-3 pain points).
For Scalable, produce 12-15 variants with additional format variations (length, CTA style).

### 2. Generate video ad scripts

Use the Anthropic API via `ai-content-ghostwriting` to generate scripts for each variant. Each script must follow this exact structure:

**HOOK (0-5 seconds):**
The first 5 seconds determine whether the viewer skips. Must contain one of:
- Stat hook: A surprising data point. "83% of data teams spend more than 20 hours a week just keeping pipelines running."
- Question hook: A direct question. "How many hours did your team lose to pipeline failures last month?"
- Proof hook: A concrete result. "A 50-person engineering team cut their data downtime by 90% in 30 days."

Rules for hooks:
- Never start with your company name (nobody cares yet)
- Never start with "Hey there" or "Hi, I'm..."
- Always address the pain, not the solution
- Use specific numbers, not vague claims

**BODY (5-20 seconds):**
Educate on the problem, not your product. This is problem-aware positioning.
- Explain WHY the problem exists (root cause)
- Quantify the cost of inaction (time, money, opportunity)
- Hint at the category of solution (not your specific product)

**CTA (20-30 seconds):**
Problem-aware CTAs offer education, not demos:
- "Download the free checklist"
- "Watch the full breakdown"
- "Get the 5-step framework"
- "See the data behind this stat"

Never: "Book a demo", "Start free trial", "Sign up today" (those are solution-aware CTAs).

**ON-SCREEN TEXT:**
For every script, also generate on-screen text overlays for sound-off viewing:
- Second 0-5: Hook text (matches spoken hook)
- Second 5-15: 1-2 supporting stat lines
- Second 15-30: CTA text + URL

### 3. Generate companion banner copy

For each video variant, create companion banner copy (300x60px banner shown next to the ad on desktop):
- Headline: max 25 characters. Rephrase the CTA.
- The banner should reinforce the CTA, not repeat the hook.

### 4. Generate UTM parameters

Every variant needs unique UTM tracking:
```
?utm_source=youtube
&utm_medium=preroll
&utm_campaign={pain-point-slug}
&utm_content={hook-type}-{variant-number}
&utm_term={audience-type}
```

Example: `?utm_source=youtube&utm_medium=preroll&utm_campaign=pipeline-failures&utm_content=stat-hook-v1&utm_term=custom-intent`

### 5. Hand off to human for video production

**Human action required:** The agent outputs a creative brief package per variant:
1. Full script with timing markers
2. On-screen text overlay specifications
3. Companion banner copy
4. Final URL with UTM parameters
5. Target video length (30s for skippable, 15s for non-skip, 6s for bumper)

The human (or video contractor) produces the video. Once the video is uploaded to YouTube, the human provides the video ID back to the agent.

### 6. Upload creatives to Google Ads

Once video IDs are available, use `google-ads-youtube-creative` to:
1. Link each YouTube video as an asset
2. Upload companion banner images
3. Create ad group ads in PAUSED status
4. Set final URLs with UTM parameters

### 7. Launch and monitor creative performance

After ads are activated:
- Wait 5 days or 2,000+ impressions per variant before judging
- Pull performance using `google-ads-youtube-reporting`
- Key metrics per variant: view rate (VTR), 25% completion rate, 75% completion rate, CTR, cost per conversion
- A variant "wins" if it has the lowest cost per conversion with at least 500 impressions

### 8. Manage creative rotation

**Fatigue detection (run weekly):**
- For each active variant, compare last 7-day VTR to first-week VTR
- If VTR declined 25%+ and the variant has run for 14+ days: flag as fatigued
- Pause fatigued variants via the API
- Queue replacement variants from the creative matrix

**Iteration (bi-weekly at Scalable+):**
- Identify the top 3 performing variants (lowest cost per conversion)
- Extract their pattern: which pain point + hook type + CTA won
- Generate 3 new variants that extend the winning pattern
- Generate 2 experimental variants with a different angle
- Repeat the handoff-to-human-for-production cycle

## Output

- Creative brief package for each variant (script, on-screen text, companion banner copy, UTMs)
- Ad creatives configured in Google Ads (PAUSED, awaiting human activation after video upload)
- Creative performance tracker: variant_id, pain_point, hook_type, VTR, CTR, cost_per_conversion, status (active/paused/fatigued)
- Rotation calendar: which variants to refresh and when

## Triggers

- **Initial run:** When a new YouTube pre-roll campaign is being set up
- **Bi-weekly:** Creative refresh cycle at Scalable and Durable levels
- **On fatigue detection:** When the performance monitor flags creative fatigue
