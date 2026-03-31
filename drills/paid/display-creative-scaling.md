---
name: display-creative-scaling
description: Scale display ad creative production with AI-assisted generation, systematic A/B testing, fatigue detection, and cross-platform creative rotation
category: Paid
tools:
  - Google Ads
  - Meta Ads
  - Anthropic
  - PostHog
  - n8n
fundamentals:
  - google-ads-display-campaign
  - meta-ads-creative-optimization
  - posthog-custom-events
  - posthog-experiments
  - hypothesis-generation
  - n8n-workflow-basics
  - n8n-scheduling
---

# Display Creative Scaling

This drill automates display ad creative production to sustain high-volume campaigns without proportional human effort. It combines AI-assisted creative generation, systematic testing frameworks, automated fatigue detection, and cross-platform creative rotation. Creative fatigue is the primary killer of display campaign performance -- this drill prevents it.

## Prerequisites

- Active display campaigns on GDN and/or Meta Audience Network (run `display-campaign-build` first)
- At least 4 weeks of performance data establishing creative baselines
- Anthropic API key for Claude (creative generation)
- n8n instance for automation workflows
- PostHog tracking display events with `creative_id` property
- Brand guidelines: colors, fonts, tone of voice, logo assets

## Input

- Winning creative from Baseline: top 3 performing ads by CTR and conversion rate
- ICP pain points (expanded to 5-7 from initial 3)
- 10+ customer proof points (stats, quotes, case studies)
- Creative performance data from PostHog (4+ weeks)

## Steps

### 1. Analyze winning patterns from Baseline

Query PostHog for creative performance data:

1. Pull CTR, conversion rate, and CPA for every `creative_id` across the last 4 weeks
2. Segment by: hook type (stat/question/proof), pain point, image style, CTA type
3. Identify the top 3 performing combinations
4. Document winning patterns:
   - Which hook type produces the best CTR?
   - Which pain point drives the most conversions?
   - Does image style (bold text overlay vs. product screenshot vs. illustration) affect performance?
   - Which CTA drives the most form submissions?

This analysis becomes the creative playbook that guides all future creative production.

### 2. Build the AI creative generation pipeline

Create an n8n workflow that generates creative batches:

**Input to Claude via Anthropic API:**
```
You are generating display ad creative for {product} targeting {persona} who {pain point}.
These prospects are problem-aware: they know they have this issue but are NOT comparing solutions.

Winning patterns from past campaigns:
- Best hook type: {stat/question/proof}
- Best pain point: {pain_point}
- Best CTA: {cta_type}
- Average CTR of winners: {ctr}%

Generate 5 display ad variants. For each variant provide:
1. Headline (under 30 characters)
2. Long headline (under 90 characters)
3. Description (under 90 characters)
4. Image concept (describe what the image should show -- bold text overlay on brand color, or product context)
5. CTA type (LEARN_MORE, GET_QUOTE, SIGN_UP, DOWNLOAD)

Rules:
- Agitate the problem, do NOT pitch the product
- Each variant uses a different hook: 1 stat, 1 question, 1 customer proof, 1 fear of missing out, 1 curiosity gap
- Numbers and specific data outperform vague claims
- No superlatives (best, #1, leading)
```

**Output processing:**
1. Parse Claude's response into structured ad components
2. Store in a staging queue (Airtable, Google Sheet, or Attio note)
3. Send to Slack for human approval of copy
4. On approval, upload to platforms via API

Run this workflow bi-weekly to maintain a creative pipeline of 10+ ready-to-deploy variants.

### 3. Deploy systematic A/B testing

Using `posthog-experiments`:

1. **Test one variable at a time across campaigns:**
   - Week 1-2: Test hook types (stat vs. question vs. proof) -- hold image and CTA constant
   - Week 3-4: Test image styles (text overlay vs. screenshot vs. illustration) -- hold copy constant
   - Week 5-6: Test CTAs (Learn More vs. Download vs. Get Demo) -- hold copy and image constant

2. **Minimum sample per variant:** 500 impressions and 20 clicks before declaring a winner
3. **Statistical rigor:** Use PostHog's built-in Bayesian analysis. Require 95% confidence before adopting.
4. **Log every test** in Attio with: hypothesis, variants, start/end date, result, confidence level

### 4. Automate creative fatigue detection

Build an n8n workflow on a daily cron schedule:

1. Query PostHog for CTR by `creative_id` over the last 7 days
2. Compare each creative's current CTR to its first-week CTR
3. Flag creatives where CTR has declined 30%+ from baseline
4. Cross-reference with frequency data: if the creative is flagged AND frequency > 4, it is fatigued
5. Action:
   - If fatigued creative count > 2 in a campaign: trigger the AI creative generation pipeline
   - Pause fatigued creatives and replace with the next variant from the staging queue
   - Log the rotation in Attio: which creative was retired, why, and what replaced it

6. Alert via Slack if:
   - More than 50% of active creatives are fatigued (systemic issue)
   - No creatives are in the staging queue (pipeline is dry)
   - A campaign has fewer than 3 active creatives

### 5. Scale to 5-7 pain points

Expand from the initial 3 pain points to 5-7 by:

1. Mining search query reports from GDN for new pain-point language the ICP uses
2. Analyzing which landing page sections get the most scroll depth (PostHog data)
3. Reviewing customer interview transcripts or support tickets for undiscovered pain points
4. For each new pain point: generate 5 creative variants via the AI pipeline, create a new ad group, and launch with 10% of campaign budget as a test allocation

### 6. Cross-platform creative synchronization

Maintain consistent messaging across GDN and Meta while respecting platform differences:

1. **Shared elements:** Pain point messaging, proof points, and value proposition are identical
2. **Platform-specific adaptation:**
   - GDN: responsive display ads with multiple headlines/descriptions (Google mixes and matches)
   - Meta Audience Network: single image with bold text overlay (more visual, shorter copy)
3. **Sync schedule:** When a creative wins on one platform, adapt and deploy on the other within 48 hours
4. **Cross-platform reporting:** Track `creative_concept_id` (maps to the underlying message) across both platforms in PostHog so you can compare the same concept's performance across GDN and Meta

## Output

- AI creative generation pipeline producing 10+ variants bi-weekly
- Systematic A/B testing framework with logged results
- Automated fatigue detection and creative rotation
- Expanded pain point coverage (5-7 pain points)
- Cross-platform creative synchronization
- Creative performance database for pattern analysis

## Triggers

- AI creative generation: bi-weekly on Monday
- Fatigue detection: daily at 07:00 UTC
- A/B test evaluation: when sample size thresholds are met (checked daily)
- Cross-platform sync: within 48 hours of declaring a winning creative
