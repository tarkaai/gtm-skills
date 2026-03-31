---
name: infographics-visual-content-scalable
description: >
  Infographics & Visual Content — Scalable Automation. Automate infographic production, distribution,
  and backlink outreach to 2-3 infographics per week with A/B testing on topics and visual formats.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social, Content"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥5,000 impressions and ≥15 backlinks per month over 4 months"
kpis: ["Monthly impressions", "Backlinks per month", "Shares per infographic", "Outreach conversion rate", "Cost per backlink"]
slug: "infographics-visual-content"
install: "npx gtm-skills add marketing/problem-aware/infographics-visual-content"
drills:
  - ab-test-orchestrator
---
# Infographics & Visual Content — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social, Content

## Overview
Automate the infographic production pipeline to produce 2-3 infographics per week with minimal manual effort. Implement A/B testing on topics, visual formats, and outreach templates. Scale backlink outreach volume while maintaining personalization quality.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥5,000 impressions and ≥15 backlinks per month over 4 months

---

## Budget

**Play-specific tools & costs**
- **Ahrefs Standard** (full backlink API access): ~$199/mo
- **Canva for Teams** (template-based design acceleration): ~$10/user/mo
- **Instantly Growth** (outreach at scale): ~$30/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate the creation pipeline
Build an n8n workflow that automates the the infographic creation pipeline workflow (see instructions below) drill:

**Trigger:** Weekly cron (Monday 9am) or on-demand via webhook.

**Workflow steps:**
1. Pull trending topics and data from configured sources (API feeds, RSS, scheduled data queries)
2. Send each topic + data to Claude API for infographic spec generation
3. Render visualizations via Plotly (called as a Python subprocess or microservice)
4. Compose final infographic via Satori
5. Export platform-specific sizes via Sharp
6. Create blog post draft with embed code and OG tags
7. Queue social posts for scheduled publishing
8. Notify for human review before final publish

**Human action required:** Review the batch of generated infographics before they are published. Check data accuracy and visual quality. Approve, request revisions, or reject. Target: 15 minutes per infographic at this stage (the LLM + rendering handles 90% of the work).

### 2. Scale to 2-3 infographics per week
Increase volume by diversifying data sources:
- Set up automated data ingestion from 3-5 recurring sources (industry report RSS feeds, public API scheduled pulls, your own product analytics weekly export)
- Build a topic backlog that the creation pipeline draws from
- Alternate between format types: stat cards (quick to produce, high share rate), full infographics (slower, higher backlink potential), carousels (highest save rate on LinkedIn)

### 3. A/B test topics and formats
Run the `ab-test-orchestrator` drill to systematically test:
- **Topics:** Compare engagement across content pillars (e.g., industry benchmarks vs how-to data vs cost comparisons)
- **Visual formats:** Single image vs carousel vs animated GIF
- **Color schemes:** Dark background vs light background vs brand-accent heavy
- **Posting times:** Morning vs afternoon vs evening
- **CTA styles:** Question CTA vs share CTA vs link CTA

Run each test over 6+ infographics (3 per variant) before declaring a winner. Track shares as the primary metric (shares drive both reach and backlinks).

### 4. Scale backlink outreach
Expand the the infographic distribution workflow (see instructions below) drill's outreach:
- Increase target list to 50-100 per infographic using Clay enrichment
- Build outreach templates that A/B test subject lines and value propositions
- Segment outreach targets: tier 1 (DR 50+, highly personalized), tier 2 (DR 30-50, semi-personalized), tier 3 (DR 15-30, templated with name personalization)
- Set up automated follow-up sequences in Instantly (day 0, day 4, day 10)

**Guardrails:**
- Max 100 outreach emails per day across all infographics
- Personalization required for tier 1 and tier 2 targets
- Monitor bounce rate: pause if >5% bounces (list quality issue)
- Monitor reply sentiment: pause if negative replies exceed 3% (messaging issue)

### 5. Build the content flywheel
As you accumulate infographics:
- Create a "data hub" or "research" section on your site listing all infographics
- Build internal linking between related infographic posts
- Republish top performers as LinkedIn carousels 4-6 weeks after initial post (new audience sees them)
- Offer a monthly "data digest" email via Loops featuring that month's best infographics

### 6. Monitor efficiency at scale
Track weekly in PostHog:
- Impressions per infographic (should maintain or grow as you scale)
- Shares per infographic (should maintain or grow)
- Backlinks per infographic (should maintain)
- Time per infographic (should decrease as automation improves)
- Cost per backlink (should decrease with volume)

If quality metrics (shares, backlinks per infographic) drop as volume increases, reduce volume and focus on higher-quality pieces.

### 7. Evaluate against threshold
Measure monthly against: ≥5,000 impressions and ≥15 backlinks per month. Must sustain over 4 consecutive months. If PASS, proceed to Durable. If FAIL, identify the bottleneck (production quality, topic selection, outreach effectiveness, or distribution) and optimize before re-evaluating.

---

## KPIs to track
- Monthly impressions
- Backlinks per month
- Shares per infographic
- Outreach conversion rate
- Cost per backlink

---

## Pass threshold
**≥5,000 impressions and ≥15 backlinks per month over 4 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## Time Estimate
- 10 hours: automation pipeline build (one-time setup)
- 3 hours/week: data review + infographic approval + outreach management
- 2 hours/week: A/B test analysis and optimization
- Total: ~75 hours over 3 months

---

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Anthropic Claude API | Infographic spec + copy generation at scale | ~$1-2/mo (https://www.anthropic.com/pricing) |
| Plotly + Kaleido | Data visualization rendering | Free (open source) |
| Satori + resvg | Infographic layout rendering | Free (open source) |
| Sharp | Multi-platform image export | Free (open source) |
| Canva for Teams | Template-based design for complex layouts | $10/user/mo (https://www.canva.com/pricing/) |
| Ahrefs Standard | Backlink tracking + competitor research | $199/mo (https://ahrefs.com/pricing) |
| Instantly Growth | Scaled backlink outreach | $30/mo (https://instantly.ai/pricing) |
| Clay | Outreach target enrichment | $149/mo Explorer plan (https://www.clay.com/pricing) |
| n8n | Production pipeline automation | Self-hosted free or $20/mo cloud (https://n8n.io/pricing) |
| PostHog | Analytics + A/B testing | Free tier or Growth $0+ (https://posthog.com/pricing) |

---

## Drills Referenced
- the infographic creation pipeline workflow (see instructions below) — automated infographic production from data to export
- the infographic distribution workflow (see instructions below) — social distribution and scaled backlink outreach
- `ab-test-orchestrator` — systematic testing of topics, formats, and outreach templates

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/infographics-visual-content`_
