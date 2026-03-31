---
name: marketplace-portfolio-scaling
description: Scale from 1 template to a portfolio of 5-10+ templates across multiple marketplaces with systematic topic selection and cross-promotion
category: Marketplaces
tools:
  - Clay
  - n8n
  - PostHog
  - Attio
  - Loops
fundamentals:
  - clay-claygent
  - clay-company-search
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-custom-events
  - posthog-cohorts
  - attio-contacts
  - attio-lists
  - loops-sequences
  - loops-audience
---

# Marketplace Portfolio Scaling

This drill scales your template marketplace presence from 1-2 templates to a portfolio of 5-10+ templates across multiple marketplaces. The 10x multiplier: each new template is a new discovery surface, and cross-promotion between templates compounds downloads and lead capture.

## Input

- At least 1 template with proven signal (Smoke test passed: downloads > 0, leads > 0)
- Performance data from `marketplace-listing-optimization` drill showing which marketplaces and topics convert best
- Product feature set mapped to potential template topics

## Steps

### 1. Identify the next 5-10 template topics

Use Clay with the `clay-claygent` fundamental to systematically discover template opportunities:

**Claygent prompt:**
```
Given that our product {product_name} solves {problem_description} for {ICP_description}, and our first template "{first_template_name}" on {marketplace} achieved {download_count} downloads:

1. List 10 adjacent workflow problems our ICP faces that could be solved with a template
2. For each, check the top 3 template marketplaces (Notion, Figma, Gumroad) for existing competition
3. Score each opportunity: demand (search volume signals), competition (number of existing quality templates), product fit (how naturally does this lead to our product)
4. Rank by composite score: high demand + low competition + high product fit = top priority
```

Use `clay-company-search` to validate demand: search for companies in your ICP that publicly share their workflows using these types of templates.

**Prioritize templates that:**
- Cover different stages of the same workflow (e.g., planning template, execution tracker, retrospective template)
- Target different roles within the same buying organization (e.g., IC version, manager version, executive version)
- Serve different use cases that all lead to your product's core value

### 2. Build the template creation pipeline

Using `n8n-workflow-basics` and `n8n-scheduling`, create a production cadence:

**Weekly cadence (n8n cron, Monday 9am):**
1. Check the template backlog in Attio (prioritized list from step 1)
2. Assign the next template for creation
3. Set a deadline: template should be published within 5 business days
4. Send a Slack notification with the template spec

**Template spec (stored in Attio):**
- Template name and target marketplace(s)
- Target keyword(s)
- Template type (Notion, Figma, Airtable, or multi-format)
- Target ICP segment
- CTA strategy (what the user should do after using the template)
- Cross-promotion links to include (links to other templates in the portfolio)

### 3. Implement cross-promotion between templates

Each template in the portfolio should link to other templates. This creates a discovery network:

**Inside each template:**
- Add a "More Templates" section listing 2-3 related templates with direct marketplace links
- Example: "Like this OKR tracker? Try our [Sprint Planning Template]({marketplace_url}) and [Retrospective Board]({marketplace_url})"
- UTM tag all cross-promotion links: `utm_source={source_marketplace}&utm_medium=cross-promo&utm_campaign=template-{source_slug}`

**On marketplace listings:**
- In the description of each template, mention related templates: "Part of our {ProductName} Template Collection -- see also: [Template B], [Template C]"

### 4. Automate lead capture across the portfolio

Using `loops-sequences` and `loops-audience`, set up a nurture sequence for template downloaders:

**Capture:** Gumroad automatically captures emails on download. For Notion/Figma/Airtable, the CTA in the template drives users to a landing page with email capture.

**Nurture sequence (Loops):**
1. Day 0: "Thanks for downloading {Template Name}. Here's a quick-start guide." (Include link to a 2-minute video walkthrough)
2. Day 3: "Here are 2 more free templates you might find useful: {Template B}, {Template C}" (cross-promote the portfolio)
3. Day 7: "See how {ProductName} automates what {Template Name} does manually" (soft product pitch with a specific use case)
4. Day 14: "Join {X} teams who upgraded from templates to the full platform" (social proof + CTA)

Tag each lead in Loops with: `source_marketplace`, `source_template`, `download_date`.

### 5. Track portfolio performance

Using `posthog-custom-events` and `posthog-cohorts`:

**Create cohorts per template:**
- Cohort: "Template: {slug} downloaders" -- people who arrived via UTM matching that template
- Compare cohorts: which template produces the highest lead conversion rate?

**Portfolio dashboard (PostHog):**
- Total downloads across all templates (trend)
- Downloads per template (bar chart)
- Lead conversion rate per template
- Cross-promotion click-through rate
- Active templates (count published and live)

**Update Attio** using `attio-lists`: maintain a "Template Portfolio" list with per-template performance metrics.

### 6. Scale to new marketplaces

Once a template performs well on its primary marketplace, adapt and publish to additional marketplaces:

**Marketplace expansion priority:**
1. Gumroad (accepts any file type, captures email)
2. Notion Marketplace (high traffic for productivity/ops templates)
3. Figma Community (high traffic for design/UI templates)
4. Airtable Universe (good for data/workflow templates)
5. Canva (good for marketing/social media templates)
6. Product Hunt (launch each template as a "product" for one-time visibility spike)

Adapt the template format to each marketplace's native format. Do not just upload the same file everywhere -- optimize for each platform's strengths.

## Output

- Portfolio of 5-10+ templates across multiple marketplaces
- Cross-promotion network between all templates
- Automated email nurture sequence for template downloaders
- Portfolio-level analytics dashboard
- Systematic creation pipeline with weekly cadence

## Triggers

- Run at Scalable level to expand from 1-2 templates to a full portfolio
- Template creation pipeline runs weekly on autopilot
- Re-evaluate portfolio strategy quarterly based on performance data
