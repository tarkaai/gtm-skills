---
name: case-study-content-program-scalable
description: >
  Case Study Content Program — Scalable Automation. Scale to 30+ case studies with
  automated multi-format content derivation from each interview, an intelligent
  deal-matching engine that routes the right case study to the right deal at the
  right sales stage, and a production cadence of 3-4 new case studies per month.
stage: "Marketing > ProductAware"
motion: "LeadCaptureSurface"
channels: "Content, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 4,000 page views/month and deal close rate +15% when case studies are used in the sales process"
kpis: ["Monthly page views across all case studies (target ≥ 4,000)", "Monthly conversions (target ≥ 60)", "Deal close rate lift when case study used vs not used (target +15%)", "Production velocity (target ≥ 3 new case studies/month)", "Sales usage rate (target ≥ 50% of active deals receive a matched case study)", "Multi-format engagement (target: PDF + social + email each receive > 100 interactions/month)"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
drills:
  - case-study-content-scaling
  - case-study-deal-matching
---

# Case Study Content Program — Scalable Automation

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Find the 10x multiplier for the case study program. Instead of manually distributing each case study, build automated systems that derive 8-12 assets from each interview, route the right case study to the right deal at the right sales stage, and track the direct influence of case studies on deal outcomes. The production cadence reaches 3-4 new case studies per month without proportional effort increase.

Pass: ≥ 4,000 page views/month across all case studies AND deal close rate improves by ≥ 15% when case studies are used in the sales process (compared to deals where no case study was shared).
Fail: < 4,000 views/month after 2 months, or case studies have no measurable effect on deal close rate, or production velocity drops below 2 per month for 2+ consecutive months.

## Leading Indicators

- The content scaling pipeline produces 8+ derivative assets from the first case study it processes (automation works end-to-end)
- At least 60% of Tier 1 assets (pull quotes, email snippets, metric highlights) require zero human editing (AI generation quality is sufficient)
- The deal matching engine routes case studies to ≥ 50% of new deals within 24 hours of deal creation (matching algorithm has sufficient coverage)
- Sales reps forward matched case studies to prospects within 48 hours of receiving the notification (the matching is relevant enough to use)
- Prospects who view a case study page via deal routing (tracked by UTM) spend ≥ 3 minutes on page (the matched content is relevant to them)
- At least 1 deal owner reports that a case study directly helped close a deal within the first month

## Instructions

### 1. Deploy the multi-format content scaling pipeline

Run the `case-study-content-scaling` drill. This builds the automated system that takes each completed case study and produces derivative assets across three tiers:

**Tier 1 — Fully automated (no human review):**
- 3-4 pull quote cards with the strongest customer quotes and metrics
- Metric highlight: single-stat callout (e.g., "2x retention rate in 90 days") for social and email
- Email snippet: 2-3 sentence summary with link for sales insertion
- In-app social proof banner via Intercom for users in the same industry cohort

**Tier 2 — Semi-automated (agent produces, human reviews):**
- One-page PDF for sales proposals
- SEO-optimized blog post via Ghost
- LinkedIn post in the founder's voice (leads with the result, tells the story, closes with a takeaway)
- Newsletter feature (150 words) for the next Loops broadcast

**Tier 3 — Human-required:**
- Video testimonial clip (if interview was recorded) -- **Human action required:** review and approve the clip
- Conference slide summarizing the case study for pitch decks -- **Human action required:** design review

The drill creates an n8n workflow triggered by the `case_study_completed` PostHog event. It extracts content from the published case study, generates all Tier 1 and Tier 2 assets, stores them in Attio, and flags Tier 2 for human review.

**Human action required:** Review Tier 2 assets before publication. The LinkedIn post should sound like the founder, not like a marketing template. The blog post should add value beyond the case study page (deeper analysis, broader industry context). Approve or edit each within 48 hours to maintain production velocity.

### 2. Deploy the deal matching engine

Run the `case-study-deal-matching` drill. This builds the always-on system that connects case studies to active deals:

**New-deal matching:** When a deal is created in Attio, the engine computes a match score for every published case study using four dimensions: industry match (40% weight), company size match (25%), use case match (25%), and metric relevance (10%). The top 2-3 matches (score ≥ 50) are attached to the deal as Attio notes, and the deal owner receives a Loops email with the case study summary, one-page PDF, and email snippet to forward.

**Stage-triggered routing:** The engine delivers the right case study at the right moment:
- Discovery -> Evaluation: route the top industry-match case study with email snippet and one-pager (credibility moment)
- Evaluation -> Decision: route a second case study with the full story and pull quotes (validation moment)
- Decision -> Negotiation: route the case study with the strongest ROI metric regardless of industry (budget justification moment)

**Weekly gap analysis:** Every Monday, the engine checks all active deals against the case study library. Deals with no relevant match (no case study scoring ≥ 50) are flagged as coverage gaps. The gap report groups missing coverage by industry and use case and feeds back into the `case-study-candidate-pipeline` (still running from Baseline) to prioritize recruiting customers in gap segments.

Configure PostHog events: `case_study_routed_to_deal`, `case_study_forwarded_to_prospect`, `case_study_prospect_viewed`, `case_study_influenced_deal_won`. Build the routing-to-influence funnel to measure the actual impact of case study distribution on deal outcomes.

### 3. Activate triggered prospect follow-ups

Using n8n, create a workflow that fires when a prospect views a case study page (tracked via UTM from deal routing):

1. Query PostHog for the `case_study_prospect_viewed` event with the `deal_id` and `case_study_id`
2. Wait 24 hours (allow the prospect to digest the story)
3. Trigger a personalized follow-up email via Loops to the deal owner (not the prospect directly): "Your prospect at [Company] read the [Case Study Company] case study yesterday. They spent [X] minutes on the page. Consider referencing [Primary Metric] in your next conversation, or offer to connect them directly with [Case Study Customer]."
4. Fire `case_study_follow_up_triggered` in PostHog

This closes the loop between content consumption and sales action without being intrusive to the prospect.

### 4. Implement A/B testing for case study formats

Using PostHog feature flags, test variations that affect conversion:

- **Structure test**: Challenge-first (traditional) vs. Results-first (lead with the metric, then explain how they got there). Run on new case studies, splitting traffic 50/50.
- **Length test**: Full case study (1,000-1,500 words) vs. Short format (400-600 words with a "Read full story" expansion). Test on the hub page.
- **CTA test**: "Book a demo" vs. "See how [Similar Company] did it" (link to a second case study) vs. "Talk to [Case Study Customer]" (offer a reference call). Test on the highest-traffic case study pages.

Run each test for minimum 14 days or 500 views per variant. Evaluate using the `case_study_converted` event rate. Promote winning formats and apply to new case studies.

### 5. Set guardrails

Build n8n alert workflows for:

- **Conversion rate decline**: If overall case study conversion rate drops > 20% from Baseline rate for 2 consecutive weeks, alert the team. Diagnose: traffic source change (lower quality visitors), CTA fatigue, or content quality decline.
- **Production velocity**: If fewer than 2 case studies are published in any 4-week period, alert the team. Diagnose: candidate pipeline stall (check `case-study-candidate-pipeline` metrics), writing bottleneck (check time-to-publish), or customer review delays.
- **Deal routing coverage**: If the weekly gap analysis shows > 40% of active deals have no matching case study, prioritize filling the top gap industry/use case.
- **Sales adoption**: If deal owner forward rate drops below 30% (they receive the match but do not forward to the prospect), survey the sales team. The matches may not be relevant enough, or the assets may not be in a usable format.

### 6. Evaluate after 2 months

Compute:

- Monthly page views across all case studies (month 1 and month 2 separately)
- Monthly conversions and conversion rate
- Deal close rate for deals where case studies were used vs. deals where they were not. Use the `case_study_routed_to_deal` and deal outcome data in Attio to compute: `close_rate_with_case_study / close_rate_without_case_study`
- Production velocity: how many case studies published per month
- Multi-format engagement: views/clicks across PDFs, social posts, email snippets
- Deal routing coverage: % of active deals with a matching case study
- Sales rep forward rate: % of routed case studies that were forwarded to prospects

- **PASS (≥ 4,000 views/mo and +15% close rate lift):** The case study program is a measurable sales multiplier. Document the close rate lift as the program's ROI metric. Proceed to Durable.
- **MARGINAL (3,000-3,999 views/mo or +8-14% close rate lift):** The program is working but not at full potential. Check: Are the strongest case studies being routed to the most important deals? Is the content quality consistent across all 30+ case studies? Is the PDF/email format optimized for how prospects actually consume social proof?
- **FAIL (< 3,000 views/mo or < +8% close rate lift):** Diagnose the funnel: Is traffic the problem (distribution not working at scale) or conversion (stories are not compelling to product-aware visitors)? Is deal routing happening but having no effect (case studies are not influencing decisions)? If close rate lift is near zero, the case studies may be targeting the wrong stage of the buying process.

## Time Estimate

- Content scaling pipeline setup: 10 hours
- Deal matching engine setup: 8 hours
- Triggered follow-up workflow: 3 hours
- A/B test configuration: 4 hours
- Guardrail and alert setup: 3 hours
- Ongoing case study production (3-4/month for 2 months): 20 hours
- Human review of Tier 2 assets: 6 hours
- Monitoring, evaluation, and iteration: 6 hours
- Total: ~60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, experiments, feature flags, cohorts | Free tier: 1M events/mo; paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Content scaling pipeline, deal matching, triggered follow-ups | Pro ~$60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Case study metadata index, deal pipeline, sales enablement | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Ghost | Blog post publishing | Free self-hosted; Pro $9/mo ([ghost.org/pricing](https://ghost.org/pricing)) |
| Loops | Transactional emails (deal owner notifications, prospect follow-ups) | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app social proof banners | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Riverside | Video interview recording (for testimonial clips) | Standard $19/mo annual ([riverside.com/pricing](https://riverside.com/pricing)) |
| Cal.com | Interview scheduling (from Baseline pipeline) | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Anthropic API | Derivative asset generation, first-draft writing | Usage-based ~$3/1M input tokens for Sonnet ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Scalable:** $150-250/mo (n8n Pro + Attio + Loops + Riverside; PostHog and Ghost on free tiers; Anthropic API ~$5-15/mo at this volume)

## Drills Referenced

- `case-study-content-scaling` — automated pipeline that produces 8-12 derivative assets from each completed case study (pull quotes, PDFs, blog posts, social posts, email snippets, in-app banners) and distributes them through sales, email, in-app, and content channels with full PostHog tracking
- `case-study-deal-matching` — always-on engine that matches published case studies to active deals by industry, company size, use case, and metric relevance, routes assets to deal owners at each sales stage, and generates weekly coverage gap reports
