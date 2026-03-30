---
name: ai-content-generation-scale-baseline
description: >
  AI Content Generation — Baseline Run. Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content"
level: "Baseline Run"
time: "18 hours over 6 weeks"
outcome: "≥2,000 page views and ≥20 conversions over 6 weeks"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity", "Social shares"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
---
# AI Content Generation — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content

## Overview
Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.

**Time commitment:** 18 hours over 6 weeks
**Pass threshold:** ≥2,000 page views and ≥20 conversions over 6 weeks

---

## Budget

**Play-specific tools & costs**
- **Taplio (LinkedIn analytics + scheduling):** ~$50/mo

_Total play-specific: ~$50/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Anthropic** (AI/LLM)
- **Ghost** (Content)
- **Ahrefs** (Analytics)

---

## Instructions

1. Expand content calendar to 15-20 posts over 6 weeks; map topics to customer journey stages (problem-aware, solution-aware, product-aware).

2. Create 3-5 prompt templates for different content types: how-to guides, comparison articles, thought leadership, case studies; include SEO guidelines in each template.

3. Use Claude or GPT-4 to generate drafts for all 15-20 posts; establish editing workflow with quality checklist (accuracy, brand voice, SEO, value to reader).

4. For each post, conduct competitor content analysis: identify content gaps and unique angles; instruct AI to incorporate these insights in the draft.

5. Publish 3-4 posts per week; implement content distribution strategy across LinkedIn, Twitter, relevant communities, and email newsletter.

6. Set up PostHog cohorts to segment readers by content topic and stage; track progression from first post view to signup or demo request.

7. Set pass threshold: ≥2,000 total page views and ≥20 conversions over 6 weeks, with average time on page ≥2 minutes.

8. Use PostHog session recordings to understand how readers engage with AI-generated content; identify sections where readers drop off and refine AI prompts accordingly.

9. After 6 weeks, compute conversion rate by content type and topic; identify the 3 highest-performing content formats.

10. If you hit the threshold, document content calendar process, prompt library, and distribution strategy and proceed to Scalable; if not, adjust content topics or improve AI prompt quality.

---

## KPIs to track
- Page views
- Time on page
- Conversion rate
- Content production velocity
- Social shares

---

## Pass threshold
**≥2,000 page views and ≥20 conversions over 6 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/ai-content-generation-scale`_
