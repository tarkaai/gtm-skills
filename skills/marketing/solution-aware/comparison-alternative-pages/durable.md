---
name: comparison-alternative-pages-durable
description: >
  Comparison and Alternative Pages — Durable Intelligence. Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "95 hours over 6 months"
outcome: "Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven competitive intelligence and comparison page optimization"
kpis: ["Organic traffic trend", "Conversion rate", "Competitor keyword coverage", "Feature comparison accuracy", "Competitive positioning effectiveness"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
---
# Comparison and Alternative Pages — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.

**Time commitment:** 95 hours over 6 months
**Pass threshold:** Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven competitive intelligence and comparison page optimization

---

## Budget

**Play-specific tools & costs**
- **Webflow:** ~$15–40/mo
- **Hotjar or FullStory:** ~$30–100/mo

_Total play-specific: ~$15–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Ahrefs** (Analytics)
- **Anthropic** (AI/LLM)
- **Google Search Console** (Analytics)

---

## Instructions

1. Deploy PostHog event streams that trigger n8n AI agents when: competitor keyword rankings shift, new competitors emerge, or comparison page performance changes.

2. Build n8n AI competitive intelligence agent that monitors competitor websites, product updates, pricing changes, and positioning shifts daily; automatically updates comparison pages with new information.

3. Implement continuous content experimentation: AI agent tests different comparison formats (tables vs. prose, feature-by-feature vs. use-case-based), CTA placements, and messaging angles; promotes winning variants.

4. Create automatic competitor discovery system: n8n monitors G2, ProductHunt, Crunchbase for new competitors in your category; AI agent generates comparison pages for emerging threats within 48 hours.

5. Build learning loop: PostHog tracks visitor journeys from comparison pages to conversion; AI agent analyzes which competitor positioning and differentiation messages drive highest conversion rates; updates pages accordingly.

6. Deploy AI content refresh agent: identifies comparison pages with declining traffic or outdated information; generates updated feature tables, pricing comparisons, and customer testimonials quarterly.

7. Implement A/B testing for comparison page elements: AI agent tests different feature table designs, pricing presentation formats, and CTA copy; automatically implements winners.

8. Create competitor content monitoring: n8n tracks when competitors publish counter-comparison pages ("[Your Product] vs [Competitor]"); AI agent analyzes their claims and suggests defensive updates to your pages.

9. Set guardrails: if organic traffic to comparison pages drops >20% for 2+ weeks or conversion rate falls below Scalable threshold, n8n alerts team and pauses automatic changes pending review.

10. Establish monthly review cycle: analyze which competitive positioning worked, which competitors to prioritize, which comparison formats to expand; refine AI agent prompts and competitive strategy based on conversion data.

---

## KPIs to track
- Organic traffic trend
- Conversion rate
- Competitor keyword coverage
- Feature comparison accuracy
- Competitive positioning effectiveness

---

## Pass threshold
**Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven competitive intelligence and comparison page optimization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/comparison-alternative-pages`_
