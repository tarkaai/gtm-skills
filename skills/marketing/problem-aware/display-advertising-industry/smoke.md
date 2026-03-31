---
name: display-advertising-industry-smoke
description: >
  Display Advertising — Smoke Test. Run a $300-500 test budget across Google Display Network
  targeting 15-20 industry publications where your ICP reads. Validate that display banners on
  relevant sites produce measurable traffic and at least 5 qualified leads at an acceptable CPC.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=20,000 impressions, CTR >=0.15%, and >=5 qualified leads from $300-500 test budget on industry sites"
kpis: ["Impressions", "CTR", "CPC", "Landing page conversion rate", "Qualified leads from ICP titles"]
slug: "display-advertising-industry"
install: "npx gtm-skills add Marketing/ProblemAware/display-advertising-industry"
drills:
  - ad-campaign-setup
  - threshold-engine
---

# Display Advertising — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Prove that running banner ads on industry publications and relevant websites produces measurable traffic from problem-aware prospects at a cost per click that justifies scaling. At this level, the agent assists with placement research, creative copy, and tracking setup. Campaign creation in Google Ads is manual. No automation, no always-on spend. One platform (GDN), one campaign, one week.

**Pass threshold:** >=20,000 impressions, CTR >=0.15%, and >=5 qualified leads from $300-500 test budget within 1 week.

## Leading Indicators

- Display CTR exceeds 0.15% (vs 0.05-0.10% benchmark for untargeted GDN display)
- CPC is below $3 (display clicks are typically cheaper than search or LinkedIn)
- Landing page receives visitors from ICP-matching companies (check PostHog session recordings)
- At least 1 managed placement produces CTR above 0.25% (signal that the specific publication is a strong fit)
- Form submissions include people with ICP job titles (VP, Director, Head of)
- Bounce rate on landing page from display traffic is below 70%

## Instructions

### 1. Confirm Prerequisites

Verify the following before starting:

1. Google Ads account is active with billing configured
2. Google Ads conversion tracking is installed on your landing pages (see `google-ads-conversion-tracking` fundamental)
3. PostHog is installed on all landing pages with form tracking events
4. At least one landing page exists with a clear CTA (download, demo, webinar registration). If not, run the `landing-page-pipeline` drill first.
5. Banner creative assets are available: at minimum, a landscape image (1200x628) and square image (1200x1200) with your logo. For the Smoke test, use Canva or Figma to create 2-3 simple bold-text-on-brand-color banners.

If any prerequisite is missing, resolve it first. Do not launch display ads without conversion tracking -- you will have impressions data but no way to measure what matters.

### 2. Research Industry Placements

Identify 15-20 industry websites and publications where your ICP audience reads:

1. **Start with known publications:** List the top 5 industry blogs, news sites, and trade publications in your vertical. For B2B SaaS, examples: TechCrunch, The New Stack, InfoQ, DZone, Dev.to, Hacker Noon, SaaStr.
2. **Mine your analytics:** Check PostHog referral data -- which sites already send you organic traffic? These are proven ICP-relevant placements.
3. **Check competitor ad placements:** Use tools like SEMrush, SpyFu, or Similarweb to see where competitors run display ads. Or simply visit competitor sites and note which ad networks they use.
4. **Research via Google Ads Placement Planner:** Enter your product URL and competitor URLs. Google suggests related placements with estimated reach.
5. **Compile the list:** 15-20 domains with estimated monthly traffic and audience relevance score (1-5). Prioritize sites with smaller, more focused audiences over giant sites with low relevance.

Store the placement list in a spreadsheet or Attio note with columns: domain, estimated_monthly_traffic, relevance_score, ICP_alignment_notes.

### 3. Create Banner Creative

Build 3 responsive display ad variants, each targeting a different ICP pain point:

**For each variant, prepare:**
- 3 headlines (under 30 characters each): one stat hook, one question hook, one proof hook
- 2 descriptions (under 90 characters each)
- 1 long headline (under 90 characters)
- Landscape image (1200x628): bold text overlay on brand-colored background with the key stat or question
- Square image (1200x1200): same concept adapted for square format
- Logo image (1200x1200)

**Example for a DevOps tool targeting deployment pain:**
- Headline A: "73% of Deploys Fail Manually"
- Headline B: "Still Debugging on Fridays?"
- Headline C: "500+ Teams Fixed This"
- Description A: "Free guide: the 5-step checklist top engineering teams use."
- Description B: "Stop losing weekends. Get the deployment playbook."
- Long headline: "The Engineering Team's Guide to Zero-Downtime Deploys"

Do NOT mention your product name in the headlines. Problem-aware prospects respond to pain agitation and educational offers, not product pitches.

### 4. Create the Test Campaign

Run the `ad-campaign-setup` drill adapted for display:

**Human action required:** In Google Ads:

1. Create a new campaign:
   - Type: **Display**
   - Goal: **Leads** or **Website traffic**
   - Name: "Display Smoke Test - Industry Sites - [Date]"

2. Configure targeting:
   - Add managed placements: enter each of the 15-20 domains from your research
   - Set geographic targeting: countries/regions where your ICP is concentrated
   - Exclude mobile app placements (Settings > Additional settings > Content exclusions)

3. Configure budget and bidding:
   - Daily budget: $45-70/day for 7 days ($315-490 total)
   - Bidding: **Maximize Clicks** for the Smoke test (you need traffic data first; switch to conversion-based bidding at Baseline when you have conversion data)

4. Create 1 ad group per pain point (3 ad groups total):
   - Upload responsive display ads using the creative from Step 3
   - Set frequency cap: 5 impressions per user per week

5. Configure exclusions:
   - Exclude below-the-fold placements
   - Exclude parked domains
   - Exclude sexually suggestive and sensitive content categories

6. Set up UTM parameters on all destination URLs:
   `?utm_source=google&utm_medium=display&utm_campaign=display-smoke-{pain-point}&utm_content={variant}`

7. Launch the campaign

### 5. Monitor for 7 Days

Check Google Ads and PostHog daily for 7 days. Track:

- **Per-placement metrics:** impressions, clicks, CTR, CPC per domain. Identify which industry sites produce the best engagement.
- **Per-creative metrics:** which pain point and hook type gets the best CTR.
- **Landing page behavior (PostHog):** bounce rate, scroll depth, form engagement, conversion rate from display traffic.
- **Lead quality:** check form submissions against ICP criteria (job title, company size, industry).

Log all metrics in a spreadsheet or Attio note. After 3 days:
- If any placement has 1,000+ impressions and zero clicks, consider excluding it (irrelevant audience)
- If any creative has CTR below 0.05%, review the copy and image -- it may not resonate with the placement audience
- If landing page bounce rate exceeds 80% from display traffic, the page may not match the ad promise -- review message match

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 7 days, pull final campaign metrics from Google Ads and PostHog
2. Calculate:
   - Total impressions (threshold: >=20,000)
   - Average CTR across all placements (threshold: >=0.15%)
   - Average CPC (benchmark: below $3)
   - Qualified leads: form submissions from people matching ICP criteria (threshold: >=5)
   - Landing page conversion rate from display traffic (benchmark: >=2%)
   - Top 5 placements by CTR (these become your Baseline placement priority list)
3. Pass threshold: >=20,000 impressions AND CTR >=0.15% AND >=5 qualified leads

**If PASS:** Display advertising works for your ICP on these industry sites. Proceed to Baseline with increased budget, multi-platform expansion, and automated lead routing.

**If FAIL:** Diagnose:
- Low impressions: placements are too small or budget too low. Add more placements or broaden to topic targeting.
- Low CTR: creative is not resonating with the audience on these sites. Test different pain points, stronger hooks, or more specific offers (calculator, checklist, benchmark report vs. generic "learn more").
- Low lead quality: the sites attract the wrong audience. Replace low-quality placements with more niche, ICP-specific publications.
- Low landing page conversion: message mismatch between ad and page. Ensure the landing page headline directly reflects the ad promise.

## Time Estimate

- 1.5 hours: Research industry placements (compile 15-20 sites)
- 1 hour: Create banner creative (3 variants with images)
- 1 hour: Set up campaign in Google Ads (targeting, budget, creative upload, exclusions)
- 1.5 hours: Daily monitoring over 7 days (~15 min/day)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (GDN) | Display campaign on industry sites | No platform fee; ad spend only ($300-500 test) |
| PostHog | Landing page analytics and conversion tracking | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — log campaign results and leads | Free (up to 3 users) or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Canva (optional) | Banner creative design | Free plan or $15/mo (Pro) — [canva.com/pricing](https://www.canva.com/pricing) |

**Estimated play-specific cost this level:** $300-500 ad spend. Tools: $0 incremental if using PostHog free tier and Attio free plan.

## Drills Referenced

- `ad-campaign-setup` — platform selection, campaign structure, targeting configuration, creative setup, conversion tracking, and launch sequence for paid advertising campaigns
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action (advance, iterate, or pivot)
