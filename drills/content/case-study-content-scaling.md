---
name: case-study-content-scaling
description: Repurpose each completed case study into multiple derivative assets and distribute them across channels with automated routing
category: Content
tools:
  - PostHog
  - Attio
  - n8n
  - Loops
  - Intercom
  - Ghost
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - attio-lists
  - attio-contacts
  - attio-deals
  - attio-notes
  - n8n-triggers
  - n8n-workflow-basics
  - loops-sequences
  - loops-transactional
  - intercom-in-app-messages
  - ghost-blog-publishing
---

# Case Study Content Scaling

This drill takes each completed case study and systematically produces 8-12 derivative assets, then distributes them to the right audience at the right time. The goal is to extract maximum pipeline influence from every case study investment.

## Prerequisites

- At least 3 completed case studies (need a library to match prospects against)
- Ghost or CMS configured for publishing
- Attio with active deal pipeline
- Loops configured for email
- Intercom configured for in-app messaging
- n8n instance for automation

## Steps

### 1. Define the derivative asset framework

For each completed case study, produce these assets in order of effort:

**Tier 1 — Automated (agent-produced, no human review needed)**
1. **Pull quote cards** (3-4 per case study): extract the strongest customer quotes with the metric they reference. Format as text blocks for social or email insertion.
2. **Metric highlight**: single-stat callout (e.g., "2x retention rate in 90 days") with company name and logo permission.
3. **Email snippet**: 2-3 sentence summary with a link to the full case study, formatted for insertion into sales email templates.
4. **In-app social proof banner**: short message for Intercom: "[Company] achieved [metric] with [Product]. Read their story."

**Tier 2 — Semi-automated (agent-produced, human reviews before publish)**
5. **One-page PDF**: structured summary with challenge, solution, results, and pull quote. Formatted for sales to attach to proposals.
6. **Blog post**: expanded narrative version with SEO optimization for "[industry] + [use case] case study" keywords. Published via Ghost.
7. **LinkedIn post**: story-format post written in the founder's voice, highlighting the customer's transformation, not the product's features.
8. **Newsletter feature**: 150-word segment for the next product newsletter via Loops.

**Tier 3 — Human-required**
9. **Video testimonial clip**: if the interview was recorded, extract a 60-90 second highlight clip. **Human action required:** review and approve the clip.
10. **Conference slide**: a single slide summarizing the case study for use in pitch decks and conference talks. **Human action required:** design review.

### 2. Automate asset production

Using `n8n-triggers`, create a workflow triggered by the `case_study_completed` event in PostHog:

1. Pull the case study content from Ghost using `ghost-blog-publishing` (read the published post)
2. Extract: company name, industry, company size, primary metric, secondary metrics, top 3 quotes, challenge summary, solution summary, results summary
3. Generate Tier 1 assets automatically:
   - Pull quote cards: select quotes with specific numbers or outcomes, format with attribution
   - Metric highlight: identify the single most impressive stat
   - Email snippet: write a 2-3 sentence version using the challenge-result arc
   - In-app banner: write a one-line version with the primary metric
4. Generate Tier 2 drafts:
   - One-page PDF: structured markdown ready for PDF conversion
   - Blog post: expand the case study with SEO structure (H2s for each section, meta description, target keyword)
   - LinkedIn post: rewrite in conversational founder voice, open with the result, tell the story, close with a takeaway
   - Newsletter feature: compress to 150 words with a CTA to read the full story
5. Store all assets as notes on the case study record in Attio using `attio-notes`
6. Flag Tier 2 assets for human review in Attio

### 3. Build the distribution engine

Using `n8n-triggers`, automate distribution after assets are approved:

**Sales enablement routing:**
Using `attio-deals`, identify all active deals in the same industry or use case as the case study subject. For each matching deal:
- Using `attio-notes`, attach the email snippet and one-page PDF to the deal record
- Notify the deal owner: "New case study matches your deal [Deal Name]. [Company] achieved [metric]. Assets attached."
- Fire `case_study_routed_to_deal` in PostHog with deal_id and case_study_id

**In-app distribution:**
Using `intercom-in-app-messages`, show the social proof banner to users in the same industry cohort as the case study subject. Use `posthog-cohorts` to target: users whose company industry matches the case study company's industry, who are in their first 90 days (when social proof has the most influence on retention).

**Email distribution:**
Using `loops-sequences`, add the newsletter feature to the next scheduled product newsletter. For prospects in the matching industry segment, trigger a dedicated "customer story" email via `loops-transactional` with the email snippet and a link to the full case study.

**Content distribution:**
Publish the blog post via `ghost-blog-publishing`. Schedule the LinkedIn post (store in Attio for the human to post, or use a scheduling tool if available).

### 4. Track asset performance

Using `posthog-custom-events`, instrument every derivative:
- `case_study_asset_viewed` with properties: asset_type (pdf, blog, email, banner), case_study_id, viewer_segment
- `case_study_asset_clicked` with properties: asset_type, case_study_id, destination
- `case_study_influenced_deal` with properties: case_study_id, deal_id, deal_stage_when_shared

Build a PostHog dashboard: asset views by type, click-through rates by type, deals influenced per case study, time from case study publish to first deal influence.

### 5. Build the matching engine for ongoing routing

Using `n8n-scheduling`, create a weekly workflow:
1. Pull all case studies from Attio with their industry and use case tags
2. Pull all new deals created this week from Attio
3. Match: for each new deal, find the best-fit case study (same industry, similar company size, similar use case)
4. If a match exists: auto-attach the email snippet and one-page PDF, notify the deal owner
5. If no match: flag the gap. This industry/use case needs a case study. Feed this back into the `case-study-candidate-pipeline` as a priority filter.

## Output

- 8-12 derivative assets from each completed case study
- Automated production pipeline triggered by case study completion
- Sales enablement routing: matching case studies to active deals
- In-app social proof distribution targeted by industry cohort
- Email distribution via newsletter and targeted sends
- Performance tracking dashboard for all assets
- Weekly deal-to-case-study matching engine

## Triggers

Asset production fires on `case_study_completed`. Distribution fires after human approval of Tier 2 assets. Deal matching runs weekly. All workflows are always-on after initial setup.
