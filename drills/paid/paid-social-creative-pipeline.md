---
name: paid-social-creative-pipeline
description: Create, test, and iterate paid social ad creative targeting problem-aware prospects on LinkedIn and Meta
category: Paid
tools:
  - LinkedIn Ads
  - Meta Ads
  - Anthropic API
fundamentals:
  - linkedin-ads-creative
  - meta-ads-creative-optimization
  - linkedin-ads-campaign-setup
  - meta-ads-campaign-setup
---

# Paid Social Creative Pipeline

This drill produces ad creative (copy, images, CTAs) specifically designed for problem-aware audiences on LinkedIn and Meta. Problem-aware prospects know they have a pain point but are NOT yet comparing solutions. Your ads must agitate the problem and offer educational value — NOT pitch your product features.

## Prerequisites

- ICP with documented pain points and triggering events (from `icp-definition` drill)
- Active LinkedIn and/or Meta campaigns with audiences configured (from `paid-social-audience-builder` drill)
- Brand guidelines (logo, colors, tone) if available
- At least 3 customer stories or data points to use as proof

## Input

- ICP pain points (top 3)
- Triggering events that make the problem acute
- Customer quotes or results data
- Product positioning (how you frame the solution)

## Steps

### 1. Map the problem-aware messaging framework

Problem-aware prospects respond to messaging that validates their pain, NOT messaging that pitches a solution. Build a messaging matrix:

| Pain Point | Agitation (why it's urgent) | Value Offer (educational, not product) | Proof Point |
|---|---|---|---|
| "Deployments break on Friday afternoons" | "Teams that deploy manually have 3x more incidents" | "Free guide: 5-step deploy checklist used by 200+ teams" | "Acme Corp cut incidents by 73%" |
| "We spend 10 hours/week on manual QA" | "That's 520 hours/year a senior engineer isn't building features" | "Calculator: What's your manual testing actually costing?" | "Beta Corp automated QA in 2 weeks" |
| "Our onboarding takes 3+ months" | "67% of new hires consider leaving if onboarding is poor" | "Webinar: How high-growth teams onboard in 30 days" | "Gamma Inc reduced onboarding from 90 to 21 days" |

Fill in 3 rows minimum. Each row becomes the basis for an ad variant.

### 2. Write LinkedIn ad variants

For each pain point, create 3 variants using the `linkedin-ads-creative` fundamental. Follow this structure:

**Variant A — Statistic hook:**
- Headline (under 70 chars): Lead with a surprising statistic. "73% of deploy failures are preventable"
- Body (under 150 chars): Connect the stat to the reader's reality. "If your team deploys manually, you're in the majority — and the risk zone."
- CTA: "Download the Guide" or "Get the Checklist"

**Variant B — Question hook:**
- Headline: Ask a question they'll answer "yes" to. "Still debugging deploys on Friday nights?"
- Body: Validate and offer a way out. "200+ engineering teams use this 5-step checklist to deploy without the drama."
- CTA: "Get the Checklist"

**Variant C — Social proof hook:**
- Headline: Lead with a customer result. "How Acme Corp cut deploy incidents by 73%"
- Body: Tease the method. "They changed 3 things in their deploy process. We documented all of them."
- CTA: "Read the Case Study"

Produce 3 variants per pain point = 9 total ads minimum.

### 3. Write Meta ad variants

Meta creative differs from LinkedIn: shorter attention span, more visual, UGC-style performs better.

For each pain point, create 2 variants using the `meta-ads-creative-optimization` fundamental:

**Variant A — Problem-agitation (static image):**
- Primary text (under 125 chars): State the problem bluntly. "Manual deploys cost engineering teams 10+ hours/week."
- Image: Bold text on contrasting background with one key statistic. No stock photos. Use brand colors.
- Headline: Offer the resource. "Free 5-Step Deploy Checklist"
- CTA: DOWNLOAD or LEARN_MORE

**Variant B — Story-style (carousel or video):**
- Card 1: "Meet [persona]. VP Engineering at a 50-person SaaS company."
- Card 2: "Every Friday, the deploy breaks. Again."
- Card 3: "They tried [common failed approach]. Didn't work."
- Card 4: "Then they changed 3 things." (tease)
- Card 5: "Get the exact playbook. Free." + CTA
- For video: 15-second version of the same narrative. Hook in first 3 seconds. Captions mandatory.

Produce 2 variants per pain point = 6 Meta ads minimum.

### 4. Generate creative assets with AI

Use the Anthropic API (via `anthropic-api-patterns` fundamental or Claude Code directly) to:

- Generate 10 headline variations per pain point, then human-select the top 3
- Write 5 body copy variations per headline
- Draft carousel card sequences
- Create ad image text overlays (the text content; design in Figma/Canva or use your brand template)

Prompt structure for Claude:
```
You are writing LinkedIn ads for {product} targeting {persona} who {pain point}.
They know they have this problem but have NOT started looking for solutions.
Write 10 headline options (under 70 characters each) that:
- Agitate the problem with a specific stat, question, or customer result
- Do NOT mention {product name} or any product features
- Make the reader think "that's me" within 2 seconds
```

### 5. Set up creative testing framework

Do not guess which ad works. Test systematically:

- Run all variants simultaneously within each audience segment
- Set minimum 500 impressions per variant before making decisions
- After 500 impressions: pause any variant with CTR below 0.3% (LinkedIn) or 0.8% (Meta)
- After 1,000 impressions: identify the top 2 performers per platform
- After 2,000 impressions: declare a winner and create 3 new variants inspired by the winning angle

Track in PostHog: `ad_variant_id`, `pain_point`, `hook_type` (stat/question/proof), `platform`. This lets you analyze which hook types work best across pain points.

### 6. Refresh creative on a 2-week cycle

Ad fatigue is the top killer of paid social performance. Build a refresh cadence:

- **Week 1-2**: Launch initial 9 LinkedIn + 6 Meta variants
- **Week 3-4**: Pause bottom 50%. Write 5 new variants inspired by winners. Launch.
- **Week 5-6**: Repeat. By now you know which pain points and hook types resonate.
- **Ongoing**: Produce 3-5 new variants every 2 weeks. Never let a single ad run more than 4 weeks.

Use n8n to automate fatigue detection: if a variant's CTR drops 30% from its first-week average, flag it for replacement.

## Output

- 9+ LinkedIn ad variants (3 per pain point, 3 hook types)
- 6+ Meta ad variants (2 per pain point)
- Messaging matrix document linking pain points to ads
- Creative testing framework with decision thresholds
- 2-week refresh schedule
