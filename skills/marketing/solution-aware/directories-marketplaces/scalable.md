---
name: directories-marketplaces-scalable
description: >
  Directory & Marketplace Listings — Scalable Automation. Expand to 10+ directories, launch PPC
  campaigns, A/B test listing copy, automate review/lead sync, and drive 10x the Baseline volume.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">= 500 views and >= 15 inquiries over 2 months"
kpis: ["Listing views", "Inquiry count", "Cost per inquiry", "Review count", "Average rating", "Category rank position"]
slug: "directories-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/directories-marketplaces"
drills:
  - directory-listing-setup
  - ab-test-orchestrator
  - tool-sync-workflow
  - directory-review-generation
---

# Directory & Marketplace Listings — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Find the 10x multiplier. Expand from 3-5 directories to 10+, launch paid placements where ROI supports it, systematically A/B test listing copy, and automate the full review-to-CRM-to-response pipeline. The question this level answers: can directory presence scale without proportional manual effort?

**Pass threshold:** >= 500 views and >= 15 inquiries over 2 months.

## Leading Indicators

- Active listings on 10+ directories within 2 weeks
- PPC campaigns live on Capterra and/or G2 within 1 week (if budget permits)
- At least 1 A/B test completed per month on listing copy
- Automated review-to-CRM sync processing new reviews within 1 hour
- Cost per inquiry from PPC directories staying below 2x organic inquiry cost
- Review velocity sustained at 3+ reviews/week across all directories

## Instructions

### 1. Expand directory coverage

Run the `directory-listing-setup` drill again to add Tier 2 and Tier 3 directories. Target 10-15 total active listings:

**Tier 2 expansion:**
- TrustRadius -- strong in enterprise; reviews carry weight with procurement teams
- GetApp -- shares Gartner Digital Markets backend with Capterra, incremental reach
- SourceForge -- high domain authority, good for SEO backlinks
- AlternativeTo -- popular for users actively seeking alternatives to competitors

**Tier 3 (niche, pick 2-4 relevant to your category):**
- StackShare (developer tools)
- SaaSWorthy (SaaS discovery)
- Crozdesk (curated SaaS)
- Slant (comparison-focused)
- BuiltWith (technology profiling)
- Industry-specific directories identified during ICP research

For each new listing, follow the same optimization checklist: keywords, screenshots, video, UTM tracking, comparison fields.

### 2. Launch paid directory placements

Where Baseline proved organic traffic converts, add paid amplification:

**Capterra PPC:**
- Set up a campaign via the `directory-listing-setup` drill (PPC section)
- Start with $500/month budget, $3-5 max CPC
- Target your top 2 categories
- Landing page: the directory-specific page from Baseline (not homepage)
- Track cost per inquiry closely -- if CPI exceeds $100 in the first 2 weeks, reduce bids or pause

**G2 Sponsored Profiles:**
- Apply for sponsored placement on your primary category page
- Typically $1,000-3,000/quarter depending on category competitiveness
- Evaluate ROI after first quarter: sponsored views -> clicks -> inquiries pipeline

**Product Hunt advertising (optional):**
- Minimum $1,000/mo spend
- Only if your Product Hunt launch performed well and your audience is active there

### 3. A/B test listing elements

Run the `ab-test-orchestrator` drill to systematically test directory listing copy:

**Test 1 (Month 1): Headline/tagline.**
Create two listing descriptions. Variant A: lead with the problem ("Tired of X? Y solves it in Z minutes"). Variant B: lead with the outcome ("Teams using Y see X% improvement in Z"). Where directories support A/B testing natively, use it. Where they do not, rotate copy monthly and compare views/clicks for each period.

**Test 2 (Month 2): Screenshot set.**
Test different screenshot orders and caption copy. Hypothesis: screenshots showing results/ROI in position 1 outperform screenshots showing the UI dashboard in position 1.

**Test 3 (ongoing): Landing page elements.**
Use PostHog feature flags to test different landing page variants for directory traffic: headline, social proof placement, CTA copy, form length.

Log every test in Attio with: hypothesis, variant descriptions, start date, end date, winner, metric change.

### 4. Automate review and lead sync

Run the `tool-sync-workflow` drill to build end-to-end automation:

**Review sync (n8n workflow):**
1. Webhook trigger: new review on G2/Capterra/TrustRadius
2. Parse review: extract rating, reviewer name, company, pros, cons
3. Match reviewer to Attio contact (search by name + company)
4. Update Attio: set `reviewed_on`, `review_rating`, `review_directory`
5. If rating >= 4: tag as case study candidate
6. If rating <= 2: alert CS team in Slack immediately
7. Draft review response using Claude API (follow response guidelines from `directory-review-monitoring` fundamental)
8. Post response to the directory (or queue for human approval if rating <= 2)

**Lead sync (n8n workflow):**
1. Webhook trigger: new form submission with `utm_source` matching a directory
2. Create or update Attio contact with: name, email, company, lead_source = "directory", directory_name, inquiry_type
3. Route: if demo request -> assign to sales. If trial signup -> add to Loops onboarding sequence. If content download -> add to nurture sequence.

**Listing update sync (n8n workflow):**
1. Trigger: product feature change logged in Attio or product changelog
2. Regenerate listing description incorporating new feature
3. Queue update for human review before pushing to directories

### 5. Scale review generation

Run the `directory-review-generation` drill with expanded scope:

- Increase review ask volume: target every customer at 30, 90, and 180 days
- Rotate which directory you ask for: distribute review asks across directories to maintain balanced coverage
- Track review velocity per directory weekly
- Goal: 5+ new reviews per week across all directories

### 6. Evaluate against threshold

After 2 months, measure:

- **PASS (>= 500 views, >= 15 inquiries):** Directory channel scales. Proceed to Durable.
- **MARGINAL (>= 500 views, 10-14 inquiries):** Volume is there, conversion needs work. Double down on landing page optimization and A/B tests. Re-run for another month.
- **FAIL (< 500 views or < 10 inquiries):** Directory channel may have a ceiling in your category. Focus budget on the top 2-3 performing directories. Consider whether organic-only (no PPC) is more efficient.

## Time Estimate

- 10 hours: Expand to 10+ directories (listing creation)
- 8 hours: PPC campaign setup and initial optimization
- 12 hours: A/B test design, execution, and analysis (2 tests)
- 15 hours: n8n automation build (review sync, lead sync, listing update sync)
- 10 hours: Review generation expansion and monitoring
- 5 hours: Weekly performance reviews and optimization

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Directory listings + sponsored | Free listing; sponsored ~$1,000-3,000/quarter ([sell.g2.com/plans](https://sell.g2.com/plans)) |
| Capterra | Directory listings + PPC | Free listing; PPC min $500/mo at $2+/click ([capterra.com/vendors](https://www.capterra.com/vendors/)) |
| Product Hunt | Product directory | Free listing; ads min $1,000/mo ([producthunt.com](https://www.producthunt.com/)) |
| TrustRadius | Enterprise review directory | Free listing ([trustradius.com](https://www.trustradius.com/)) |
| PostHog | Tracking, funnels, experiments | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation | Community (self-hosted) free; Cloud Pro EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Review ask sequences | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM and pipeline tracking | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Competitive monitoring | Explorer $149/mo ([clay.com/pricing](https://clay.com/pricing)) |

**Estimated monthly cost at this level:** $500-2,000 (primarily Capterra PPC + optional G2 sponsored)

## Drills Referenced

- `directory-listing-setup` -- expand from 3-5 to 10-15 directory listings with PPC campaigns
- `ab-test-orchestrator` -- systematically test listing headlines, screenshots, and landing page elements
- `tool-sync-workflow` -- automate review-to-CRM sync, lead routing, and listing update workflows
- `directory-review-generation` -- scale review collection to 5+ reviews/week across all directories
