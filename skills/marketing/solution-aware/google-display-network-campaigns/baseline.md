---
name: google-display-network-campaigns-baseline
description: >
  Google Display Network — Baseline Run. Scale the proven Smoke campaign to always-on
  automation with retargeting, lead enrichment, CRM routing, and systematic budget
  allocation across managed placements, custom intent, and remarketing audiences.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=15 qualified leads from $2,000-3,000 GDN spend over 4 weeks with CPA <=$200"
kpis: ["Qualified leads (target >=15 over 4 weeks)", "CPA (target <=$200)", "CTR by audience segment", "Landing page conversion rate (target >=3%)", "Lead quality rate (% of leads that are ICP matches, target >=50%)"]
slug: "google-display-network-campaigns"
install: "npx gtm-skills add marketing/solution-aware/google-display-network-campaigns"
drills:
  - budget-allocation
  - retargeting-setup
  - posthog-gtm-events
  - tool-sync-workflow
---

# Google Display Network — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Move from one-shot Smoke test to always-on display advertising. At this level, you expand from a single campaign to a multi-campaign structure (managed placements, custom intent, and retargeting), add lead enrichment and CRM routing, configure end-to-end PostHog tracking, and run for 4 weeks with systematic budget allocation. The goal is to prove GDN produces qualified leads repeatedly at a sustainable CPA -- not just once. You also build the retargeting layer: visitors who clicked a display ad but did not convert get followed up with a dedicated retargeting campaign, which typically converts at 3-5x the rate of cold display.

**Pass threshold:** >=15 qualified leads from $2,000-3,000 GDN spend over 4 weeks with CPA <=$200.

## Leading Indicators

- Retargeting audience building (site visitors from display ads) reaches 500+ within 2 weeks
- At least 3 leads per week by week 2 (run rate toward 15 over 4 weeks)
- CPA trending downward week-over-week as retargeting ramps up
- Lead quality rate (ICP match) >=50% (if lower, targeting needs refinement)
- Managed placement campaigns have CTR >=0.40% (better than broad display average)
- Custom intent campaigns are producing clicks from new audience segments not reached in Smoke

## Instructions

### 1. Analyze Smoke test data and plan campaign structure

Before building, analyze the Smoke results:

1. Pull the final placement report from Google Ads. Identify the top 10 placements by CTR and conversion. These become your managed placement list for Baseline.
2. Pull custom intent audience performance. Which keywords and URLs drove the most conversions? Expand those.
3. Review the landing page funnel in PostHog: where did visitors drop off? (page_view > scroll_50 > form_view > form_submit). Address the biggest drop-off before scaling spend.
4. Document the winning creative elements from Smoke: which headlines, images, and CTAs performed best.

Plan 3 campaign types for Baseline:
- **Campaign A: Managed Placements** -- Ads on the top-performing industry sites from Smoke, plus 10-15 new sites researched from your ICP's reading habits
- **Campaign B: Custom Intent** -- Expanded custom audience with 20+ keywords and 10+ URLs
- **Campaign C: Retargeting** -- Re-engage display visitors who did not convert (requires remarketing audience built during Smoke)

### 2. Allocate budget across campaigns

Run the `budget-allocation` drill with this display-specific allocation:

- **Managed placements (Campaign A): 40% of budget** -- Highest quality traffic, lower volume. These are known-good sites from Smoke.
- **Custom intent (Campaign B): 35% of budget** -- Broader reach to new prospects. Higher volume, needs more monitoring.
- **Retargeting (Campaign C): 25% of budget** -- Highest conversion rate, smallest audience. Budget may underdeliver as the remarketing audience builds.

Set daily budgets: for $2,500 monthly total, that is approximately $33/day split across campaigns ($13 managed, $12 custom intent, $8 retargeting).

Define rebalancing triggers:
- If retargeting CPA is 50%+ below cold campaign CPA, increase retargeting budget by 20%
- If managed placements CPA exceeds $250 after 2 weeks, reduce to 30% and shift to custom intent
- If custom intent CPA exceeds $300 after 2 weeks, tighten the custom audience (remove low-performing keywords)

### 3. Set up retargeting

Run the `retargeting-setup` drill to configure GDN remarketing:

1. Create remarketing lists via `google-ads-display-audiences`:
   - **High intent (7-day window):** Visited landing page, scrolled past 50%, or viewed the form but did not submit
   - **Medium intent (30-day window):** Clicked a display ad and viewed the landing page
   - **Exclusion list:** Anyone who already submitted the form (converted)

2. Create a separate retargeting campaign (Campaign C) with:
   - Different ad creative than cold campaigns: retargeting ads should acknowledge the visitor's previous interest. Headlines like "Ready to See [Product] in Action?" or "The Report You Started Reading" (for content offers).
   - Stronger CTA: since these visitors already know your brand, use "Book a Demo" or "Start Free Trial" instead of "Learn More"
   - Frequency cap: 3 impressions per user per week (tighter than cold campaigns to avoid annoyance)
   - Bid higher than cold campaigns (these visitors are more likely to convert)

### 4. Configure end-to-end tracking

Run the `posthog-gtm-events` drill to set up the display ads event taxonomy:

1. **Events to track:**
   - `display_click` -- triggered when a display ad click lands on your page (detected via UTM parameters)
   - `display_page_view` -- page view with `utm_medium=display`
   - `display_scroll_50` -- scrolled past 50% of landing page
   - `display_form_view` -- form element entered viewport
   - `display_form_submit` -- form submission completed
   - `display_lead_qualified` -- lead scored as ICP match after enrichment

2. **Event properties on every display event:**
   - `platform`: google
   - `campaign_type`: managed_placements | custom_intent | retargeting
   - `campaign_id`: Google Ads campaign ID
   - `ad_group`: ad group name
   - `placement_url`: the site where the ad appeared (from Google Ads)
   - `creative_variant`: which headline/image combo was shown
   - `pain_point`: which ICP pain point this ad group targets

3. **Build the PostHog funnel:**
   `display_click > display_page_view > display_scroll_50 > display_form_view > display_form_submit > display_lead_qualified`
   Segment by `campaign_type` to compare managed placements vs custom intent vs retargeting.

### 5. Build lead routing and CRM sync

Run the `tool-sync-workflow` drill to connect display ads to your CRM:

1. Build an n8n workflow triggered by the `display_form_submit` PostHog webhook:
   - Extract lead data from the form submission
   - Enrich via Clay: company size, industry, LinkedIn profile, ICP score
   - Create or update contact in Attio with properties: `source: display-ads`, `campaign_type`, `placement_url`, `lead_score`
   - If lead_score >= ICP threshold: create deal in Attio, add to Loops high-intent nurture sequence, send Slack alert
   - If lead_score < threshold: add to Loops educational nurture sequence
   - Log the enrichment and routing decision as a PostHog event for attribution

2. Build a weekly n8n report workflow:
   - Query Attio for all leads sourced from display-ads in the last 7 days
   - Include: lead count, ICP match rate, deals created, average lead score
   - Post to Slack and store in Attio

### 6. Launch and run for 4 weeks

**Week 1:** Launch Campaign A (managed placements) and Campaign B (custom intent). Monitor daily: impressions, CTR, placement quality, and click-to-page-view match rate. Exclude junk placements aggressively.

**Week 2:** Launch Campaign C (retargeting) once the remarketing audience reaches 500+ users. Review the first week's creative performance: pause underperforming ads (CTR below campaign average), promote winning headlines. Make first budget reallocation if any rebalancing triggers are hit.

**Week 3:** Evaluate lead quality. Pull the ICP match rate from Attio. If <50% of leads are ICP matches, diagnose: is the audience targeting too broad (tighten custom intent), or is the landing page attracting the wrong people (adjust messaging)? Refresh any creative with CTR declining >25%.

**Week 4:** Final measurement week. Do not make major changes. Let data accumulate for threshold evaluation.

### 7. Evaluate against threshold

Run the `threshold-engine` drill. Pull from PostHog, Google Ads, and Attio:
- Total qualified leads (ICP match confirmed via enrichment)
- CPA (total spend / qualified leads)
- Lead quality rate (qualified leads / total form submissions)
- Performance by campaign type: which produced the best CPA? Which the most volume?
- Retargeting conversion rate vs cold campaign conversion rate
- Top 10 placements by conversion

**Pass:** >=15 qualified leads with CPA <=$200. Proceed to Scalable.

**Fail -- sufficient leads but CPA too high:** Shift budget toward the lowest-CPA campaign type. Tighten custom intent audiences. Increase retargeting allocation.

**Fail -- low lead volume:** Display reach may not be sufficient for your market. Expand to Meta Audience Network as a second platform. Add more managed placements. Broaden custom intent with adjacent keywords.

**Fail -- low lead quality (ICP match <40%):** The targeting is reaching the wrong people. Tighten in-market audiences to more specific subcategories. Review the custom intent keywords -- remove broad terms, add more specific solution-comparison terms. Test managed placements only (highest quality, lowest waste).

## Time Estimate

- 3 hours: Analyze Smoke data, plan campaign structure, research new managed placements
- 4 hours: Build 3 campaigns, create audiences, write new creative, set up retargeting
- 3 hours: Configure PostHog event taxonomy, build funnel, set up n8n lead routing
- 2 hours: Set up budget allocation, rebalancing triggers, weekly reporting
- 4 hours: Weekly monitoring and optimization (1 hr/week for 4 weeks)
- 4 hours: Weekly lead quality review, creative refresh, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Display campaigns (managed placements, custom intent, retargeting) | $2,000-3,000/mo ad spend -- [ads.google.com](https://ads.google.com) |
| Webflow | Landing pages | CMS $23/mo -- [webflow.com/pricing](https://webflow.com/pricing) |
| PostHog | Analytics, funnels, event tracking | Free tier or Growth ~$50/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Clay | Lead enrichment | Explorer $149/mo (2,500 credits) -- [clay.com/pricing](https://clay.com/pricing) |
| n8n | Workflow automation (lead routing, reporting) | Pro EUR 60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM for lead tracking | Plus $29/user/mo -- [attio.com/pricing](https://attio.com/pricing) |
| Loops | Email nurture sequences | Starter $49/mo -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** $2,000-3,000/mo ad spend + ~$200-350/mo tooling (Clay + Loops; Webflow, n8n, PostHog, and Attio are standard stack)

## Drills Referenced

- `budget-allocation` -- Allocate and rebalance budget across managed placements, custom intent, and retargeting campaigns based on CPA performance
- `retargeting-setup` -- Configure GDN remarketing audiences by intent level, create retargeting campaign with different creative and tighter frequency caps
- `posthog-gtm-events` -- Define and implement the display ads event taxonomy in PostHog for full-funnel attribution
- `tool-sync-workflow` -- Build n8n workflows connecting display ad conversions to Clay enrichment, Attio CRM, and Loops nurture sequences
