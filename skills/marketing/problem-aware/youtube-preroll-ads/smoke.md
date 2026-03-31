---
name: youtube-preroll-ads-smoke
description: >
  YouTube Pre-roll Ads — Smoke Test. Run skippable in-stream video ads on YouTube
  targeting 20-50 hand-picked channels your ICP watches, with a $300-600 test budget.
  Validate that your ICP engages with video ads by getting at least 10,000 views
  and 3 qualified leads in 2-3 weeks.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Content"
level: "Smoke Test"
time: "6 hours over 2-3 weeks"
outcome: "≥ 10,000 views and ≥ 3 qualified leads from $300-600 test budget"
kpis: ["View rate (VTR)", "Cost per view (CPV)", "Click-through rate (CTR)", "Cost per lead (CPL)", "ICP match rate of leads"]
slug: "youtube-preroll-ads"
install: "npx gtm-skills add marketing/problem-aware/youtube-preroll-ads"
drills:
  - youtube-preroll-audience-builder
  - ad-campaign-setup
  - landing-page-pipeline
  - threshold-engine
---

# YouTube Pre-roll Ads — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Content

## Outcomes

Get at least 10,000 views and 3 qualified leads from a $300-600 YouTube pre-roll test in 2-3 weeks. This proves that your ICP watches YouTube content where your ads can appear, that they do not skip your ad within 5 seconds, and that a meaningful fraction clicks through to your landing page and converts. You are NOT trying to optimize CPV or prove ROI yet — you are testing whether YouTube pre-roll is a viable channel for reaching problem-aware prospects at all.

YouTube pre-roll is fundamentally different from LinkedIn or Meta paid social: you reach people based on what they watch and search, not who they are. This makes it uniquely powerful for problem-aware targeting (you show up when they are consuming content about the problem), but it requires a different creative approach (video, not image+copy).

## Leading Indicators

- Ad impressions served on the targeted channels/placements (confirms targeting is delivering)
- View rate (VTR) above 15% for skippable in-stream (confirms the first 5 seconds hook works)
- Video completion rate (75% quartile) above 25% (confirms the video message resonates beyond the hook)
- Landing page visits from ad clicks (confirms ad-to-page handoff works)
- Form submissions on the landing page (confirms the offer is compelling enough to convert)

## Instructions

### 1. Choose your strongest pain point

Pick the ONE pain point from your ICP that is most urgent and most clearly tied to a YouTube content ecosystem. Ask: "Does my ICP watch YouTube videos about this problem?" If yes, this pain point works for YouTube pre-roll.

Do not split a smoke test across multiple pain points. Pick one.

### 2. Research and build your placement list

Run the `youtube-preroll-audience-builder` drill in smoke mode:
- Use the YouTube Data API to search for channels related to your pain point
- Manually curate a list of 20-50 YouTube channels your ICP watches
- Add 1 custom intent segment with 5-10 search terms related to the pain point (people who recently Googled these terms)
- Set up audience exclusions: upload your current customer list from Attio

Run placement channels and custom intent as two separate ad groups so you can compare performance.

### 3. Create 3 video ad variants

Run the the youtube preroll creative pipeline workflow (see instructions below) drill in smoke mode. Produce 3 creative briefs for one pain point:
- Variant A: Stat hook (lead with a surprising data point about the problem)
- Variant B: Question hook (ask a question they will answer "yes" to)
- Variant C: Proof hook (lead with a specific customer/team result)

Each script should be 25-30 seconds for skippable in-stream. The first 5 seconds must contain the hook — this is the only part most viewers will see.

Each ad should offer something educational: a guide, checklist, framework, or data report. Do NOT pitch your product. Problem-aware prospects are not ready for that.

**Human action required:** Produce the 3 videos. Options:
- DIY with Descript or Loom (founder talking to camera + screen recording): $0, 2 hours
- AI avatar with Synthesia: $22/mo, 1 hour
- Professional production: $500-2,000, 1-2 weeks

For a smoke test, DIY is fine. You are testing messaging, not production quality.

### 4. Build a landing page

Run the `landing-page-pipeline` drill to build a single landing page with:
- Problem-focused headline that matches the video ad hook
- The educational resource offered in the ad (guide, checklist, etc.)
- Short form: name, email, company name
- PostHog tracking installed for `yt_preroll_page_view` and `yt_preroll_form_submit`
- Google Ads conversion tag firing on form submission

### 5. Set up the campaign

Run the `ad-campaign-setup` drill with YouTube-specific settings:
- **Campaign type:** VIDEO (via Google Ads). Subtype: VIDEO_ACTION (optimized for conversions)
- **Budget:** $300-600 total over 2-3 weeks. Set as $15-30/day.
- **Bidding:** Maximize Conversions (if you have conversion tracking set up) or Maximum CPV ($0.10 cap) if you do not
- **Geographic targeting:** Match your ICP's geography (typically US, or US + UK + Canada)
- **Exclusions:** Exclude ages 18-24. Exclude your customer list.

Create two ad groups:
- Ad Group 1: Placement targeting (your 20-50 channels). All 3 ad variants.
- Ad Group 2: Custom intent targeting (your 5-10 search terms). All 3 ad variants.

### 6. Launch and do NOT touch it for 10 days

**Human action required:** Upload the 3 videos to YouTube (Public or Unlisted). Provide video IDs to the agent. The agent creates the ads in Google Ads. Activate the campaign.

Set a calendar reminder for 10 days. Do NOT optimize mid-flight. YouTube Video campaigns need 7-10 days to exit the learning phase. Pausing or changing ads during this period resets the learning.

### 7. Collect and log results

After 2-3 weeks, pull results from Google Ads via the `google-ads-youtube-reporting` fundamental:
- Total impressions, views, VTR per variant and per ad group
- Total clicks, CTR per variant
- Video completion rates (25%, 50%, 75%, 100%) per variant
- Total conversions (form submissions) and cost per conversion
- Placement performance: which specific channels drove the most views and conversions

Pull lead quality data from PostHog and Attio:
- Total form submissions
- For each lead: name, company, title (from the form + any enrichment)
- ICP match: check each lead against your ICP criteria

Log aggregate results in PostHog: `yt_preroll_smoke_views`, `yt_preroll_smoke_leads`, `yt_preroll_smoke_complete`.

### 8. Evaluate against threshold

Run the `threshold-engine` drill. Compare results to: **≥ 10,000 views and ≥ 3 qualified leads from $300-600 test budget**.

Also check video engagement quality:
- VTR above 15% (viewers are not skipping immediately)
- 75% completion rate above 25% (message is holding attention)
- At least 50% of leads match ICP criteria

Decision:
- **PASS (10K+ views, 3+ qualified leads, VTR >= 15%):** Proceed to Baseline. Document which variant and audience type performed best.
- **MARGINAL (10K+ views but 1-2 leads, OR 3+ leads but low ICP match):** The channel works for impressions but the creative or landing page needs iteration. Test a different hook type or offer. Re-run smoke.
- **FAIL (VTR < 10% or 0 leads):** If VTR is low, the hook is not working — test entirely different messaging in the first 5 seconds. If VTR is fine but no clicks, the CTA is weak — try a more compelling offer. If the platform cannot spend your budget, your placement list is too narrow — expand to 50+ channels or add topic targeting.

## Time Estimate

- 1 hour: Placement research and audience setup
- 1 hour: Creative brief generation (3 variants)
- 2 hours: Video production (DIY) — **human time**
- 30 minutes: Landing page setup
- 30 minutes: Campaign setup and launch
- 10-14 days: Campaign runs (no active time)
- 1 hour: Results analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (YouTube) | Video ad platform | $15-30/day. Expect CPV $0.02-0.10. Budget: $300-600 for smoke test. [Pricing](https://ads.google.com/home/pricing/) |
| YouTube | Video hosting for ad creatives | Free. [YouTube Studio](https://studio.youtube.com) |
| Descript | DIY video production | $24/mo or free tier for basic editing. [Pricing](https://www.descript.com/pricing) |
| Webflow | Landing page | $14/mo Basic plan. [Pricing](https://webflow.com/pricing) |
| PostHog | Conversion tracking and analytics | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |

**Estimated smoke test cost:** $300-600 ad spend + $0-38 tooling = $300-638 total

## Drills Referenced

- `youtube-preroll-audience-builder` — research and build 20-50 channel placements + 1 custom intent segment
- the youtube preroll creative pipeline workflow (see instructions below) — generate 3 video ad scripts and creative briefs for the smoke test
- `ad-campaign-setup` — configure the Google Ads Video campaign, ad groups, and tracking
- `landing-page-pipeline` — build a landing page with form and PostHog tracking
- `threshold-engine` — evaluate smoke test results against the pass threshold
