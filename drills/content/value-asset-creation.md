---
name: value-asset-creation
description: Research, outline, and produce a free value asset (report, benchmark, checklist, or tool) tailored to an ICP pain point
category: Content
tools:
  - Anthropic
  - Clay
  - Google Docs
fundamentals:
  - ai-content-ghostwriting
  - anthropic-api-patterns
  - clay-claygent
  - clay-enrichment-waterfall
---

# Value Asset Creation

This drill produces a single free value asset — a 1-5 page report, benchmark, checklist, scorecard, or micro-tool — designed to be the lead magnet in an outbound-with-value-asset play. The asset must deliver standalone value so the recipient shares it internally even if they never reply.

## Input

- ICP definition (from `icp-definition` drill): target titles, company sizes, pain points
- Competitive landscape: what assets competitors already give away
- Founder's domain expertise and proprietary data/insights (if any)

## Steps

### 1. Research the pain point landscape

Use the `clay-claygent` fundamental to research 20-30 companies matching your ICP. For each, ask Claygent: "What is {Company Name}'s biggest operational challenge related to {your domain}? Reference their job postings, blog, or recent news." Aggregate the answers into a frequency table of pain points. Pick the pain point that appears in 40%+ of results — that is your asset topic.

### 2. Audit competing assets

Search Google for "{pain point} + report/checklist/benchmark + {industry}" to find existing free assets in your space. Document:
- What format each uses (PDF report, interactive tool, spreadsheet)
- What data or insight each contains
- What is missing or outdated

Your asset must fill a gap. If everyone publishes benchmarks, publish a diagnostic checklist. If everyone has checklists, publish original benchmark data.

### 3. Choose the asset format

Select the format that matches your data and audience:

- **Benchmark report** (best if you have proprietary data): "State of X" with 5-10 data points comparing industry performance. 3-5 pages. Works when your ICP cares about how they compare to peers.
- **Diagnostic checklist** (best for operational pain): 15-25 yes/no items that reveal gaps. 1-2 pages. Works when your ICP suspects they have a problem but cannot quantify it.
- **Scorecard/calculator** (best for quantifiable pain): A spreadsheet or simple web tool that takes 5-10 inputs and outputs a score or cost estimate. Works when your ICP needs to justify budget.
- **Playbook/how-to** (best for emerging categories): 3-5 pages of step-by-step instructions for a process the ICP does poorly. Works when your ICP is still learning.

### 4. Generate the asset draft

Using the `ai-content-ghostwriting` fundamental (adapted for long-form), generate the asset content via the Anthropic API:

```
POST https://api.anthropic.com/v1/messages

System prompt: "You are writing a free value asset for {ICP_DESCRIPTION}. Topic: {PAIN_POINT}. Format: {FORMAT}. The asset is authored by {FOUNDER_NAME}, founder of {COMPANY}. It must:
- Deliver standalone value without mentioning {PRODUCT} until the final paragraph
- Include specific numbers, frameworks, or actionable steps — not generic advice
- Be written in the founder's voice: {VOICE_PROFILE_SUMMARY}
- Include a single soft CTA at the end: 'If you want help implementing this, I built {PRODUCT} to do exactly that. Reply to this email or book 15 minutes: {CAL_LINK}'
- Be {PAGE_COUNT} pages when formatted"

User prompt: "Write the full asset. Use these research findings as source material: {PAIN_POINT_RESEARCH_FROM_STEP_1}. Differentiate from these competing assets: {COMPETITOR_ASSET_SUMMARIES_FROM_STEP_2}."
```

### 5. Add proprietary data (if available)

If you have customer data, usage metrics, or survey results: replace generic industry claims with your actual numbers. An asset that says "we analyzed 200 companies and found X" outperforms one that says "industry experts agree that X." Even small datasets (20-50 data points) create credibility if the methodology is transparent.

**Human action required:** Review the draft for accuracy. Verify all data points. Remove anything that sounds generic or AI-generated. Add 1-2 personal anecdotes or opinions from the founder's experience.

### 6. Format and host the asset

- **PDF**: Export from Google Docs or Notion with your brand header/footer. Keep it clean — no heavy design. A well-formatted Google Doc exported as PDF reads as "founder made this" rather than "marketing made this."
- **Spreadsheet**: Build in Google Sheets with clear instructions in the first tab. Share as "make a copy" link.
- **Web page**: If the asset is a calculator or scorecard, build a simple page and track visits with PostHog.

Host the asset at a short, memorable URL: `{yourdomain}.com/{asset-slug}`

### 7. Create the asset tracking plan

Define how you will measure asset engagement:
- **Email engagement**: Track opens, link clicks to asset URL, and replies that reference the asset
- **Asset engagement**: If hosted on web, track page views, time on page, and scroll depth via PostHog
- **Downstream**: Track which asset recipients eventually book meetings and enter pipeline

## Output

- One polished value asset ready to attach or link in outbound emails
- A hosted URL for the asset with tracking configured
- A clear understanding of which ICP pain point the asset addresses

## Triggers

Run this drill once at the start of the outbound-with-value-asset play (Smoke level). Refresh or create new assets quarterly at Scalable/Durable levels using the `value-asset-refresh-pipeline` drill.
