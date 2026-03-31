---
name: infographics-visual-content-baseline
description: >
  Infographics & Visual Content — Baseline Run. First always-on infographic production cadence
  with analytics tracking and backlink outreach to prove repeatable engagement and link acquisition.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥500 total impressions and ≥5 backlinks across series in 6 weeks"
kpis: ["Total impressions", "Backlinks acquired", "Shares per infographic", "Engagement rate"]
slug: "infographics-visual-content"
install: "npx gtm-skills add marketing/problem-aware/infographics-visual-content"
drills:
  - posthog-gtm-events
  - infographic-distribution
---
# Infographics & Visual Content — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social, Content

## Overview
Scale from 1-2 test infographics to a repeatable weekly cadence. Add analytics tracking, blog hosting with embed codes, and backlink outreach. Prove that infographic content can consistently drive engagement and earn backlinks over 6 weeks.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥500 total impressions and ≥5 backlinks across series in 6 weeks

---

## Budget

**Play-specific tools & costs**
- **Ahrefs Lite** (backlink tracking): ~$99/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure analytics tracking
Run the `posthog-gtm-events` drill to set up infographic-specific event tracking. Implement these events:
- `infographic_published` — properties: topic, data_source, platform, format (single image vs carousel)
- `infographic_engagement` — properties: platform, impressions, shares, comments, saves (collected 48h after publish)
- `infographic_blog_view` — properties: infographic_slug, referrer, time_on_page
- `infographic_embed_used` — properties: embedding_domain (fires when someone uses your embed code)
- `infographic_lead_captured` — properties: source_infographic, lead_company, lead_title

Connect LinkedIn analytics to PostHog via n8n webhook so social engagement data flows automatically.

### 2. Establish a weekly production cadence
Commit to publishing 1 infographic per week for 6 weeks. Build a topic calendar:
- Week 1: Industry benchmark data (comparison chart)
- Week 2: Trend data (line chart showing change over time)
- Week 3: Survey or poll results (donut chart of responses)
- Week 4: Cost/ROI comparison (horizontal bar chart)
- Week 5: Process or workflow visualization (step diagram)
- Week 6: Best-of compilation from your top 5 data points

Run the `infographic-creation-pipeline` drill each week. Batch the LLM spec generation and review at the start of each week, then render and export mid-week for Thursday posting.

### 3. Host infographics on your blog
For each infographic, create a blog post that:
- Embeds the full-resolution image
- Provides 500-1000 words of context, analysis, and methodology
- Includes the embed code snippet for easy sharing
- Has OG meta tags so the infographic appears as the social preview card
- Is indexed and sitemap-included for SEO benefit

### 4. Run backlink outreach
Run the `infographic-distribution` drill for each published infographic. For Baseline:
- Build a list of 20-30 outreach targets per infographic (bloggers, newsletter authors, resource page owners)
- Send personalized outreach emails offering the infographic as a resource
- Track outreach: emails sent, replies, links earned
- Follow up once after 4 days if no reply

### 5. Track and iterate weekly
After each infographic, review:
- Social engagement (impressions, shares, comments) within 72 hours
- Blog traffic to the infographic post
- Outreach response rate and backlinks earned

Identify patterns: which topics get the most shares? Which visual formats drive engagement? Which outreach angle works best? Apply learnings to the next week's infographic.

### 6. Evaluate against threshold
After 6 weeks, measure against: ≥500 total impressions and ≥5 backlinks. If PASS, proceed to Scalable. If FAIL, diagnose: are the topics too niche, the data not compelling, the outreach poorly targeted, or the visual quality insufficient? Iterate for another 3-week cycle before pivoting.

---

## KPIs to track
- Total impressions
- Backlinks acquired
- Shares per infographic
- Engagement rate

---

## Pass threshold
**≥500 total impressions and ≥5 backlinks across series in 6 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## Time Estimate
- 3 hours: analytics setup and blog template creation (one-time)
- 2 hours/week: data sourcing + infographic creation + blog post
- 1 hour/week: social posting + backlink outreach
- 1 hour/week: tracking and analysis
- Total: ~18 hours over the 6-week evaluation period

---

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Anthropic Claude API | Infographic spec + companion copy | ~$0.05/week (https://www.anthropic.com/pricing) |
| Plotly + Kaleido | Data visualization rendering | Free (open source) |
| Satori + resvg | Infographic layout rendering | Free (open source) |
| Sharp / Pillow | Multi-platform image export | Free (open source) |
| Ahrefs Lite | Backlink tracking and competitor research | $99/mo (https://ahrefs.com/pricing) |
| Instantly | Backlink outreach emails | $30/mo Growth plan (https://instantly.ai/pricing) |
| PostHog | Analytics and event tracking | Free tier up to 1M events/mo (https://posthog.com/pricing) |

---

## Drills Referenced
- `posthog-gtm-events` — set up infographic-specific event tracking in PostHog
- `infographic-distribution` — distribute across social platforms and run backlink outreach

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/infographics-visual-content`_
