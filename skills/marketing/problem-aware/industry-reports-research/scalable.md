---
name: industry-reports-research-scalable
description: >
  Industry Reports & Research — Scalable Automation. Establish a quarterly report
  cadence with automated distribution, SEO-optimized landing pages, A/B tested
  promotion, and multi-format repurposing to 10x reach without proportional effort.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Social, Email"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: ">=500 downloads and >=40 qualified leads per report; >=2 reports published in 3 months"
kpis: ["Downloads per report", "Qualified leads per report", "Cost per lead", "Backlinks per report", "Organic search traffic to report pages", "Social amplification ratio"]
slug: "industry-reports-research"
install: "npx gtm-skills add marketing/problem-aware/industry-reports-research"
drills:
  - industry-research-production
  - report-distribution-pipeline
  - ab-test-orchestrator
  - blog-seo-pipeline
  - content-repurposing
  - follow-up-automation
---

# Industry Reports & Research — Scalable Automation

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Content, Social, Email

## Outcomes

Scalable finds the 10x multiplier. You move from ad hoc report production to a systematic quarterly cadence with: automated distribution workflows, A/B tested landing pages and promotion, SEO-optimized report pages that generate organic downloads for months, multi-format repurposing that turns each report into 20+ content pieces, and automated lead follow-up sequences. Each report becomes a lead generation engine, not a one-time event.

**Pass threshold:** >=500 downloads and >=40 qualified leads per report, with >=2 reports published in 3 months. Organic search drives >=10% of downloads for reports older than 30 days.

## Leading Indicators

- Each report hits 200+ downloads in its first 2 weeks (strong launch distribution)
- Landing page conversion rate stays above 20% for gated reports across all traffic sources
- A/B tests produce at least 2 winning variants that improve conversion by 10%+
- Backlinks per report reach 10+ within 60 days of publication
- Organic search traffic to report pages begins within 4 weeks and grows monthly
- Content repurposing produces 15+ derivative pieces per report with measurable engagement
- Cost per qualified lead from reports stays below $30
- Report-attributed pipeline value grows quarter-over-quarter

## Instructions

### 1. Establish the quarterly report production cadence

Plan 4 reports per year (1 per quarter), each targeting a different ICP pain point. Using the `industry-research-production` drill, create a production calendar:

- **Weeks 1-2:** Topic selection and data collection design. Validate the topic against search volume (use `blog-seo-pipeline` keyword research step), competitor gaps, and ICP pain point frequency.
- **Weeks 3-5:** Data collection (survey distribution, enrichment runs, or product data aggregation)
- **Weeks 6-7:** Analysis, writing, founder review, and design
- **Week 8:** Publication and distribution launch

Start each quarter's report production 8 weeks before the target launch date. While one report is in distribution (Weeks 1-4 post-launch), the next report enters production (Weeks 1-4 of the cycle).

For data collection at scale, increase sample sizes:
- Surveys: target 100-200 responses. Use Clay to build a targeted distribution list of ICP contacts to invite. Offer early access to findings as incentive.
- Enrichment: research 200-500 companies per report for statistically meaningful patterns.

### 2. Optimize report landing pages for SEO and conversion

Run the `blog-seo-pipeline` drill for each report's landing page:

- Research the primary keyword for each report topic (e.g., "{industry} benchmark report {year}", "state of {topic} {year}")
- Optimize the landing page title, meta description, H1, and content for the target keyword
- Publish an ungated executive summary (800-1,200 words) on the landing page for search indexing. The full report remains gated below the summary.
- Add FAQ schema markup answering 3-5 questions the report addresses
- Internal link from 3-5 existing blog posts to each report page
- Ensure page load time is under 2 seconds

This creates a compounding asset: each report page accrues organic traffic over time, generating downloads months after the social distribution campaign ends.

### 3. A/B test distribution and conversion elements

Run the `ab-test-orchestrator` drill to systematically test:

**Priority 1 — Landing page conversion:**
- Gate type: 2-field form (email + company) vs email-only vs fully ungated with optional email capture
- Form placement: above the fold vs below the executive summary
- Social proof: with testimonials/download count vs without

**Priority 2 — LinkedIn post performance:**
- Hook style: data-point lead ("72% of teams still do X manually") vs question lead ("How does your team handle X?") vs story lead ("We analyzed 200 companies and found something we didn't expect")
- Post format: text-only vs image with chart vs carousel
- Posting time: 8am vs 10am vs 12pm in ICP timezone

**Priority 3 — Email broadcast performance:**
- Subject line: direct stat vs curiosity gap vs question
- Send time: Tuesday 8am vs Thursday 10am
- Content: executive summary vs single finding deep-dive

Use PostHog feature flags for landing page tests. For social and email tests, split audiences manually across batches. Minimum 200 visitors per landing page variant, 50 sends per email variant, before declaring winners.

### 4. Build multi-format repurposing workflows

Run the `content-repurposing` drill to turn each report into 20+ content pieces:

From each report, extract:
- **5-8 LinkedIn posts** (one per key finding, varying formats across the 4-week distribution calendar)
- **1 LinkedIn carousel** (top 5 findings as slides)
- **1 Twitter/X thread** (10-tweet summary of the report)
- **2-3 newsletter sections** (deep-dive on individual findings, distributed across 2-3 weekly newsletters)
- **4-6 social graphics** (quotable stats formatted for LinkedIn and Twitter)
- **1 short-form video** (founder explaining the headline finding, 60-90 seconds)
- **1 blog post** (executive summary, SEO-optimized)
- **2-3 guest post pitches** (each offering an exclusive finding to a different industry publication)
- **1 slide deck** (formatted for webinar or speaking opportunity using report data)

Set up an n8n workflow using the `report-distribution-pipeline` drill to schedule all derivative content automatically: input the report's key findings and graphics, and the workflow queues the 4-week social calendar, triggers the email broadcasts, and schedules the newsletter features.

### 5. Automate lead follow-up at scale

Run the `follow-up-automation` drill to build n8n workflows for report-sourced leads:

- **Immediate (on download):** Enrich the downloader via Clay. Score ICP fit. If ICP score >= 70, add to Attio as a qualified lead with `report-{slug}` attribution.
- **Day 3 (for ICP-matching downloaders):** Auto-send a personal email from the founder referencing the report and their company: "Saw you downloaded our {report}. Curious how {company_name} approaches {topic} — happy to share what we're seeing from the data."
- **Day 7 (if no reply):** Follow up with one exclusive insight not in the report plus a Cal.com booking link.
- **Day 14 (if no meeting booked):** Add to the general nurture sequence via Loops. Tag with `report-nurture-{slug}` for segmentation.

Guardrails: Maximum 3 touches per downloader. Suppress anyone who replies negatively or unsubscribes. Never auto-email non-ICP downloaders (they get added to the general newsletter list instead).

### 6. Monitor and optimize the report portfolio

Track weekly in PostHog:
- Downloads per report (current week vs 4-week average)
- Conversion rate by traffic source (social, email, organic, referral)
- A/B test results and winning variants
- Lead quality: what percentage of downloaders become qualified leads
- Long-tail performance: are older reports still generating downloads via organic search?

Monthly: Review the report portfolio. Which topics generated the most pipeline value? Use this to prioritize next quarter's topic. Retire or refresh reports where downloads have dropped below 10/week.

After 3 months, evaluate against threshold: >=500 downloads and >=40 qualified leads per report, with >=2 reports published.

**If PASS:** The report motion scales. Proceed to Durable to deploy autonomous optimization.

**If FAIL:** Diagnose:
- Downloads below 500 but leads quality is high: Distribution is the bottleneck. Expand to paid promotion (LinkedIn ads targeting ICP, newsletter sponsorships featuring the report).
- Downloads above 500 but leads below 40: Conversion is the bottleneck. Tighten the ICP focus, improve the follow-up sequence, or add a stronger CTA inside the report.
- First report performed well, second did not: Topic selection matters more than production quality. Invest more time in topic validation before starting production.
- Organic search not materializing: SEO optimization is weak. Strengthen the keyword targeting, build more internal links, and pursue guest post backlinks.

## Time Estimate

- Quarterly production planning: 3 hours
- Report 1 production (enhanced data collection + writing): 12 hours
- Report 2 production: 12 hours
- Landing page optimization and A/B testing: 6 hours
- Content repurposing and distribution setup: 8 hours
- Follow-up automation: 4 hours
- Weekly monitoring (1 hr/week x 12 weeks): 12 hours
- Monthly review and optimization: 3 hours
- **Total: ~60 hours over 3 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Data collection, enrichment, lead scoring | Growth: $495/mo — higher volume, CRM integrations ([clay.com/pricing](https://www.clay.com/pricing)) |
| Typeform | Surveys at scale | Business: $50/mo — 10,000 responses, logic jumps ([typeform.com/pricing](https://www.typeform.com/pricing)) |
| Ghost | Report landing pages, blog, newsletters | Creator: $25/mo — custom integrations ([ghost.org/pricing](https://ghost.org/pricing/)) |
| Loops | Email broadcasts and nurture sequences | Growth: $49/mo — 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| PostHog | Analytics, funnels, A/B testing | Free tier up to 1M events; ~$50/mo for 2M events ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation (distribution, follow-ups, monitoring) | Pro: ~$60/mo — 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM, lead tracking, report attribution | Pro: $59/user/mo — advanced reporting ([attio.com](https://attio.com)) |
| Ahrefs | SEO monitoring and backlink tracking | Lite: $99/mo — 5 projects ([ahrefs.com/pricing](https://ahrefs.com/pricing)) |
| Anthropic API | Report analysis, content generation | ~$5-10/mo for quarterly production + repurposing ([anthropic.com](https://www.anthropic.com)) |

**Estimated monthly cost: ~$850-950/mo** (Clay Growth + Typeform Business + Ghost Creator + Loops Growth + n8n Pro + Attio Pro + Ahrefs Lite)

## Drills Referenced

- `industry-research-production` — produce each report from data collection through publication
- `report-distribution-pipeline` — multi-channel 4-week distribution for each report launch
- `ab-test-orchestrator` — systematically test landing page, social, and email variants
- `blog-seo-pipeline` — SEO-optimize report landing pages for organic traffic
- `content-repurposing` — turn each report into 20+ derivative content pieces
- `follow-up-automation` — automated lead follow-up for report downloaders
