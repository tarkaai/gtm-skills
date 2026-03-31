---
name: ai-content-generation-scale-smoke
description: >
  AI Content Generation — Smoke Test. Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content"
level: "Smoke Test"
time: "6 hours over 3 weeks"
outcome: "≥300 page views and ≥3 conversions in 3 weeks"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - social-content-pipeline
  - threshold-engine
---
# AI Content Generation — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content

## Overview
Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.

**Time commitment:** 6 hours over 3 weeks
**Pass threshold:** ≥300 page views and ≥3 conversions in 3 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Anthropic** (AI/LLM)
- **Ghost** (Content)

---

## Instructions

1. Define 5 content topics aligned with your ICP's problems; research top-performing articles on each topic using Ahrefs or BuzzSumo to understand what resonates.

2. Create a prompt template for Claude or GPT-4 that includes: target audience, topic, key points to cover, desired tone, word count (800-1,200 words); test the prompt with 3 variations to find the best structure.

3. Generate 5 blog posts using your refined prompt; for each post, review and edit for accuracy, brand voice, and SEO optimization (include target keyword in title, H1, and body).

4. Publish the 5 posts on your blog or Ghost; add relevant images, internal links, and clear CTAs; ensure each post is optimized for Core Web Vitals.

5. Set up PostHog to track page views, time on page, scroll depth, and conversions (signup, download) for each AI-generated post.

6. Set pass threshold: ≥300 total page views and ≥3 conversions from the 5 posts within 3 weeks.

7. Share each post on LinkedIn and Twitter; track social referral traffic in PostHog to measure distribution effectiveness.

8. After 3 weeks, analyze performance in PostHog: identify top-performing post by traffic and conversions; note what made it successful (topic, format, CTA placement).

9. Compare AI editing time vs. writing from scratch; document time savings and quality trade-offs.

10. If you hit the threshold, document the prompt template and editing process and proceed to Baseline; if not, refine prompts or topic selection and retest.

---

## KPIs to track
- Page views
- Time on page
- Conversion rate
- Content production velocity

---

## Pass threshold
**≥300 page views and ≥3 conversions in 3 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/ai-content-generation-scale`_
