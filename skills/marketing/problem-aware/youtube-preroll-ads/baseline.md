---
name: youtube-preroll-ads-baseline
description: >
  YouTube Pre-roll Ads — Baseline Run. Scale the winning smoke test to always-on with
  $1,000-2,500/mo budget, add lead routing automation, expand to 2 pain points, and
  run retargeting bumper ads. Prove repeatable lead generation with ≥ 15 qualified
  leads from 100,000+ views over 3 weeks.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Content"
level: "Baseline Run"
time: "18 hours over 3 weeks"
outcome: "≥ 100,000 views and ≥ 15 qualified leads from $2,000 budget over 3 weeks"
kpis: ["Cost per qualified lead (CPqL)", "View rate (VTR)", "View-to-lead conversion rate", "Lead-to-ICP match rate", "Lead-to-meeting conversion rate", "Video 75% completion rate"]
slug: "youtube-preroll-ads"
install: "npx gtm-skills add marketing/problem-aware/youtube-preroll-ads"
drills:
  - youtube-preroll-creative-pipeline
  - youtube-preroll-audience-builder
  - youtube-preroll-lead-routing
  - retargeting-setup
  - budget-allocation
  - posthog-gtm-events
  - threshold-engine
---

# YouTube Pre-roll Ads — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Content

## Outcomes

Generate at least 100,000 views and 15 qualified leads over 3 weeks with $1,000-2,500/mo ad spend. This proves YouTube pre-roll is a repeatable lead channel, not a one-time fluke. You also prove that automated lead routing works: every form submission lands in your CRM, gets enriched, scored, and receives a nurture email within 5 minutes. You also test retargeting: people who watched 75%+ of your ad but did not click get a 6-second bumper ad as a reminder.

## Leading Indicators

- VTR stays above 15% at higher volume (creative is not fatiguing)
- Lead-to-ICP match rate stays above 50% with expanded audiences (targeting quality holds)
- Nurture email open rate above 40% (leads are real and engaged)
- At least 1 lead replies to a nurture email or books via Cal.com (downstream signal)
- Retargeting audience growing (viewers who watched 75%+ are being captured)
- CPV trending stable or declining week-over-week (campaigns are learning)

## Instructions

### 1. Set up end-to-end tracking

Run the `posthog-gtm-events` drill to establish event tracking for the full YouTube pre-roll funnel:
- `yt_preroll_impression` — ad served (pulled from Google Ads API via n8n daily sync)
- `yt_preroll_view` — ad viewed (30 seconds or full video)
- `yt_preroll_click` — ad clicked through to landing page
- `yt_preroll_page_view` — landing page loaded (PostHog pageview with UTM params)
- `yt_preroll_form_submit` — form completed
- `yt_preroll_lead_enriched` — Clay enrichment completed
- `yt_preroll_lead_scored` — ICP score assigned
- `yt_preroll_meeting_booked` — meeting booked via Cal.com

Tag every event with properties: `campaign_type` (placement/custom-intent/topic), `pain_point`, `hook_type`, `variant_id`.

### 2. Build lead routing automation

Run the `youtube-preroll-lead-routing` drill to set up the full pipeline:
- n8n workflow on form submission webhook: deduplicate against Attio, enrich via Clay, score against ICP, create contact in Attio, trigger Loops nurture sequence
- High-value lead alert (ICP score >= 80): Slack notification with name, company, title, which ad variant they responded to
- Target: form submission to CRM entry in under 5 minutes

### 3. Expand creative from smoke test winners

Run the `youtube-preroll-creative-pipeline` drill at baseline volume:
- Take the winning hook type from smoke (stat/question/proof) and create 3 new scripts with different supporting data or angles
- Add a second pain point: create 3 scripts for it (one per hook type)
- Total: 6-9 active video ad variants across 2 pain points

**Human action required:** Produce the new videos. At baseline, consider investing in slightly better production: better lighting, on-screen graphics for stats, branded intro/outro. Still DIY-appropriate but more polished than smoke.

### 4. Expand audience targeting

Run the `youtube-preroll-audience-builder` drill at baseline volume:
- Expand placement list from 20-50 to 50-100 channels
- Add 20 specific high-performing video placements (individual videos, not just channels)
- Create a second custom intent segment for the new pain point
- Add topic targeting as a third ad group (broader reach, run in parallel)

Structure as 3 separate campaigns to isolate audience performance:
- Campaign 1: Placement targeting (50-100 channels). All variants.
- Campaign 2: Custom intent targeting (2 segments). All variants.
- Campaign 3: Topic targeting (B2B tech topics). All variants.

### 5. Set up retargeting with bumper ads

Run the `retargeting-setup` drill adapted for YouTube:
- Create a Google Ads remarketing list: people who viewed 75%+ of your pre-roll ad but did NOT click through
- Create 6-second bumper ad scripts that reinforce the CTA: "Still dealing with [problem]? Grab the free checklist. Link in the description."
- Run bumper ads to the retargeting audience at $5-10/day
- Also set up a display retargeting campaign (banner ads across Google Display Network) for people who visited your landing page but did not convert

**Human action required:** Produce 2-3 bumper videos (6 seconds each). These are simpler: one stat + CTA, or brand mention + CTA.

### 6. Allocate and pace budget

Run the `budget-allocation` drill with baseline-specific settings:
- Total budget: $1,000-2,500 for the 3-week period
- Split: 50% to the campaign/audience type that won in smoke, 30% to the second campaign type, 10% to the new audience type, 10% to retargeting
- Set daily budget caps on each campaign to prevent front-loading
- If one campaign type has cost per lead 2x+ the others after 7 days, shift 15% of its budget to the winner

### 7. Monitor weekly and adjust once

At the end of week 1, review:
- CPV and VTR by campaign type and variant
- Lead quality: what % of leads match ICP? Are enriched leads converting to meetings?
- Creative performance: which variants have the highest 75% completion rate and lowest CPL?
- Retargeting: any conversions from bumper ads or display retargeting?
- Placement report: which channels/videos drove the most conversions? Any irrelevant placements to exclude?

Make ONE set of adjustments:
- Pause variants with VTR below 10% after 5,000+ impressions
- Exclude channels that are clearly irrelevant (kids content, gaming, etc.) from the placement list
- Shift budget toward the best-performing campaign type
- Add negative placements for any channels driving views but zero conversions

Do NOT make daily changes. YouTube Video campaigns need time to learn.

### 8. Evaluate against threshold

Run the `threshold-engine` drill at the end of week 3. Compare to: **≥ 100,000 views and ≥ 15 qualified leads from $2,000 budget over 3 weeks**.

Check quality metrics alongside volume:
- Lead-to-ICP match rate: target ≥ 50%
- Lead-to-meeting conversion rate: target ≥ 15% of ICP-matching leads
- Video 75% completion rate: target ≥ 25% (message quality held at scale)
- CPqL (cost per qualified lead): benchmark against LinkedIn/Meta CPL — YouTube should be within 1.5x

Decision:
- **PASS:** 15+ qualified leads, ≥50% ICP match, lead routing working, retargeting live. Proceed to Scalable.
- **MARGINAL:** 8-14 leads or 15+ leads but <50% ICP match. Stay at Baseline. Test new pain points, improve targeting with placement exclusions, or try different video formats (e.g., screen recording demo vs. talking head).
- **FAIL:** <8 leads despite $2,000+ spend. Diagnose: Is it targeting (check placement report for irrelevant channels)? Creative (low VTR means the hook fails)? Landing page (high clicks but no conversions)? Offer (try a different resource type)?

## Time Estimate

- 3 hours: Lead routing automation setup (n8n workflows, Loops sequences)
- 2 hours: Tracking setup (PostHog events, Google Ads conversion tracking)
- 3 hours: Creative expansion (6-9 new scripts + production coordination)
- 3 hours: Video production — **human time**
- 2 hours: Audience expansion and retargeting setup
- 1 hour: Budget allocation and campaign configuration
- 1 hour: Week 1 review and adjustments
- 2 hours: Final evaluation, documentation, and reporting
- 1 hour: Bumper ad production — **human time**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (YouTube) | Video ad platform | $1,000-2,500/mo ad spend. CPV $0.02-0.10. [Pricing](https://ads.google.com/home/pricing/) |
| YouTube | Video hosting | Free. [YouTube Studio](https://studio.youtube.com) |
| Clay | Lead enrichment and ICP scoring | $149/mo Starter (1,000 credits). [Pricing](https://clay.com/pricing) |
| Loops | Nurture email sequences | Free up to 1,000 contacts. [Pricing](https://loops.so/pricing) |
| Webflow | Landing pages | $14/mo Basic. [Pricing](https://webflow.com/pricing) |
| PostHog | Funnel tracking and analytics | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| n8n | Lead routing automation | Free self-hosted or $20/mo cloud. [Pricing](https://n8n.io/pricing) |
| Descript | Video production | $24/mo. [Pricing](https://www.descript.com/pricing) |

**Estimated baseline monthly cost:** $1,000-2,500 ad spend + ~$225 tooling = $1,225-2,725/mo

## Drills Referenced

- `youtube-preroll-creative-pipeline` — expand winning smoke creative to 6-9 variants across 2 pain points
- `youtube-preroll-audience-builder` — expand to 50-100 placements, 2 custom intent segments, and topic targeting
- `youtube-preroll-lead-routing` — automate lead flow from landing page form to CRM with enrichment and nurture
- `retargeting-setup` — capture 75%+ viewers and landing page visitors for bumper ad and display retargeting
- `budget-allocation` — distribute budget across 3 campaign types and retargeting
- `posthog-gtm-events` — set up end-to-end event tracking for the YouTube pre-roll funnel
- `threshold-engine` — evaluate baseline results against the pass threshold
