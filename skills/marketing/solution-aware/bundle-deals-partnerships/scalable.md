---
name: bundle-deals-partnerships-scalable
description: >
  Bundle Deal Partnerships — Scalable Automation. Automate bundle partner
  onboarding, landing page generation, deal routing, and performance tracking
  so the bundle portfolio scales to 10+ active partners without proportional
  manual effort.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: "≥8 active bundles and ≥50 bundle deals/quarter over 6 months"
kpis: ["Bundle deals per quarter", "Revenue per bundle", "Time to launch new bundle", "Partner promotional effort score", "Bundle customer retention rate"]
slug: "bundle-deals-partnerships"
install: "npx gtm-skills add marketing/solution-aware/bundle-deals-partnerships"
drills:
  - partner-pipeline-automation
  - tool-sync-workflow
---

# Bundle Deal Partnerships — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

A systematized bundle deal machine: new bundles launch in under 1 week from partner agreement (down from 2-3 weeks at Baseline), landing page generation is templatized, deal routing flows automatically from PostHog to Attio, partner performance reports generate without manual work, and the portfolio scales to 8+ active bundles producing 50+ deals per quarter. The 10x multiplier comes from automation — each new bundle requires minimal marginal effort because the infrastructure (templates, tracking, workflows, reporting) is built once and reused.

## Leading Indicators

- New bundle launches in <5 business days from partner pricing agreement (signal: the template and workflow system works)
- 80%+ of bundle deals auto-create in Attio within 1 hour of checkout completion (signal: the deal routing automation is reliable)
- Monthly partner performance reports send on time without manual intervention (signal: reporting automation is stable)
- At least 6 of 8+ bundles generate ≥1 deal per month (signal: the portfolio is not dependent on 1-2 star partners)
- Bundle customer 90-day retention rate ≥70% (signal: bundles attract real users, not just discount hunters)
- Partner promotional effort score averages ≥6/10 across the portfolio (signal: partners are actively co-marketing, not just passive)

## Instructions

### 1. Automate the partner onboarding and deal pipeline

Run the `partner-pipeline-automation` drill adapted for bundle partnerships. Build n8n workflows that handle:

**Bundle partner onboarding workflow (triggered when Attio partner status changes to "Bundle Approved"):**
1. Clone the bundle landing page template in Webflow, pre-filling partner name, logo URL, and bundle ID from Attio
2. Generate UTM-tracked distribution URLs for both partners
3. Create a new deal in the Attio Bundles pipeline with pre-populated fields: partner name, tier structure, revenue split, launch date
4. Send the partner a Loops email with: their distribution URL, co-branded assets, promotion calendar, and first month's recommended promotion cadence
5. Schedule the first performance review (4 weeks out) as an Attio task

**Bundle deal routing workflow (triggered by PostHog webhook on `bundle_deal_completed`):**
1. Parse the event: `partner_slug`, `tier_name`, `deal_value`, `attribution_source`
2. Look up the partner in Attio
3. Create or update the bundle deal record: increment deal count, add revenue, log the attribution source
4. If this is the partner's first deal, send a Slack notification celebrating the milestone
5. If deal value exceeds $500, flag for sales follow-up (bundle customer may be an expansion opportunity)

**Monthly partner report workflow (n8n cron, 1st of each month):**
1. For each active bundle partner, pull from PostHog: page views, tier selections, deals completed, revenue, traffic attribution split
2. Calculate per-partner metrics: CVR, average deal value, promotional effort score (based on traffic from their channels), month-over-month trend
3. Generate a partner-facing performance report and email it via Loops
4. Generate an internal portfolio summary and post to Slack
5. Flag underperforming bundles (0 deals in 30 days) and over-performing bundles (>10 deals in 30 days) for human review

### 2. Templatize bundle creation

Run the the bundle deal structuring workflow (see instructions below) drill one final time to build the reusable template system:

- **Landing page template**: A Webflow page template with dynamic fields for partner branding, pricing tiers, and CTAs. New bundles should require only: partner logo, partner product description, finalized pricing, and checkout link. Everything else (layout, tracking, UTM structure) is standardized.
- **Pricing model template**: A Claude prompt template that takes partner pricing as input and outputs a 3-tier bundle model in <30 seconds. The agent can run this for new partners without custom prompt engineering.
- **Pitch deck template**: A standard bundle proposal document with placeholders for partner-specific details. Include results from existing bundles as social proof.

### 3. Scale the partner portfolio

With automation in place, expand to 8-12 active bundles:

- **Inbound pipeline**: Add a "Bundle with us" page to your website and integration directory. Partners who discover your product through your docs, marketplace listings, or integration pages can self-express interest.
- **Outbound pipeline**: Continue sourcing partners via `partner-prospect-research`. Prioritize partners whose products complement your most popular plans (where the highest volume of users would benefit from the bundle).
- **Integration-first bundles**: For partners where your products integrate, the bundle is especially compelling because customers get "better together" value, not just a discount. Prioritize building or highlighting integrations alongside bundle launches.

### 4. Connect the full tool stack

Run the `tool-sync-workflow` drill to wire together:

- **PostHog → Attio**: Bundle events auto-update deal records and partner metrics
- **Attio → n8n**: Partner status changes trigger landing page creation, email sends, and task scheduling
- **PostHog → Loops**: Bundle page visitors who do not complete checkout enter a retargeting email sequence (2 emails over 7 days, referencing the specific bundle and tier they viewed)
- **Stripe → Attio**: Payment confirmations update deal records with exact revenue, enabling accurate revenue split calculations
- **Attio → Slack**: Alerts for deal milestones, underperforming bundles, and portfolio summaries

### 5. Build the promotional amplification system

At scale, the bottleneck shifts from building bundles to ensuring partners promote them. Create systems to maximize partner promotional effort:

- **Promotion scorecard**: Score each partner monthly on: number of times they shared the bundle (tracked via UTM), traffic they drove, social mentions, in-product visibility. Share the scorecard with partners to create healthy competition.
- **Co-marketing asset library**: For each bundle, pre-create: email copy (3 variants), social media posts (LinkedIn, Twitter), in-product banner copy, and a 1-page PDF one-pager. Give partners everything they need to promote — zero effort required from them beyond pressing "send."
- **Quarterly bundle refresh**: Every quarter, update bundle pricing or add a limited-time bonus (extra month free, additional feature unlock) to give partners a reason to re-promote. Stale bundles decay; fresh angles keep partner attention.

### 6. Evaluate against threshold

Measure at month 3 and month 6:

- Active bundles generating ≥1 deal/month (target: ≥8)
- Total bundle deals per quarter (target: ≥50)
- Average time from partner agreement to live bundle (target: <5 business days)
- Bundle customer 90-day retention rate (target: ≥70%)
- Automation reliability: % of deals auto-routed, % of reports auto-generated

**Pass threshold: ≥8 active bundles AND ≥50 bundle deals/quarter over 6 months**

- **Pass**: The bundle machine works. Document the portfolio: which partner categories perform best, which tier is most popular, which promotion channels drive the most deals. Proceed to Durable.
- **Marginal**: 5-7 active bundles or 30-49 deals/quarter. Investigate: is the bottleneck partner recruitment (not enough bundles), partner promotion (bundles exist but partners do not push them), or conversion (traffic arrives but does not convert)? Fix the bottleneck and extend by 1 quarter.
- **Fail**: <30 deals/quarter despite 5+ active bundles. The bundle model may have a ceiling for your market. Consider whether integration partnerships, referral programs, or reseller agreements would generate more pipeline than discount bundles.

## Time Estimate

- Partner pipeline automation setup: 15 hours
- Landing page and pricing template creation: 8 hours
- Tool stack integration: 10 hours
- Scaling to 8+ partners (research, pitch, launch): 15 hours
- Promotional system setup: 5 hours
- Ongoing management and evaluation (3 months): 7 hours

Total: ~60 hours over 3 months (front-loaded; automation handles most ongoing work by month 2)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Partner onboarding, deal routing, reporting automation | Cloud Pro: ~EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Bundle deal pipeline, partner CRM, automation triggers | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Bundle funnel tracking, attribution, retargeting cohorts | Free up to 1M events; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Webflow | Templatized co-branded landing pages | CMS plan: $29/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Loops | Partner emails, bundle customer retargeting sequences | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Stripe | Bundle checkout and revenue tracking | 2.9% + $0.30 per transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| Anthropic Claude | Pricing model generation for new bundles | Sonnet 4: ~$5-15/mo at this volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Crossbeam | Account overlap analysis for partner prioritization | Free tier for basic; Connector from ~$400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |

**Estimated cost for this level: ~$200-500/mo** (n8n Pro + Attio Plus + Webflow CMS + Loops required; Crossbeam optional)

## Drills Referenced

- `partner-pipeline-automation` — automate partner onboarding, deal routing, performance reporting, and nurture sequences across the bundle portfolio
- the bundle deal structuring workflow (see instructions below) — build the reusable template system for landing pages, pricing models, and partner pitches
- `tool-sync-workflow` — wire PostHog, Attio, n8n, Loops, and Stripe into a unified bundle operations stack
