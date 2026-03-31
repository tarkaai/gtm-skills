---
name: display-advertising-industry-baseline
description: >
  Display Advertising — Baseline Run. First always-on display campaigns across Google Display
  Network and Meta Audience Network with managed placements, custom intent audiences, automated
  lead routing, and proper conversion tracking. Validate that display ads produce repeatable
  qualified leads at a sustainable cost.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Baseline Run"
time: "18 hours over 4 weeks"
outcome: ">=200,000 impressions and >=20 qualified leads from $2,000-3,000 budget over 4 weeks, with cost per qualified lead below $150"
kpis: ["Impressions", "CTR by placement", "CPC", "Cost per qualified lead", "Lead quality score", "Landing page conversion rate", "Placement quality distribution"]
slug: "display-advertising-industry"
install: "npx gtm-skills add Marketing/ProblemAware/display-advertising-industry"
drills:
  - display-campaign-build
  - landing-page-pipeline
  - paid-social-lead-routing
---

# Display Advertising — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

First always-on display advertising campaigns. The agent builds multi-platform campaigns across Google Display Network and Meta Audience Network with proper placement targeting, custom intent audiences, conversion tracking, and automated lead routing. Leads flow automatically from display click through enrichment and scoring into CRM and email nurture. The goal is to prove that display ads on industry sites produce repeatable, qualified leads at a sustainable cost.

**Pass threshold:** >=200,000 impressions and >=20 qualified leads from $2,000-3,000 budget over 4 weeks, with cost per qualified lead below $150.

## Leading Indicators

- Display CTR sustains above 0.15% across managed placement campaigns
- At least 5 managed placements produce CTR above 0.20% (validated placement list)
- CPC remains below $2 on GDN, below $1.50 on Meta Audience Network
- Lead quality: >=50% of display leads score 70+ on ICP scoring (via Clay enrichment)
- Landing page conversion rate from display traffic exceeds 2%
- Custom intent audiences on GDN produce comparable or better CPA than managed placements
- Meta retargeting campaign produces the lowest CPA of all audience segments

## Instructions

### 1. Build Multi-Platform Display Campaigns

Run the `display-campaign-build` drill:

**Google Display Network (60% of budget — $1,200-1,800):**

1. **Campaign A — Managed Placements:**
   - Carry over the top 10 placements from the Smoke test (highest CTR and conversion rate)
   - Add 10-15 new placements based on Smoke learnings (similar sites, same content categories)
   - Total: 20-25 managed placements
   - Budget share: 60% of GDN allocation
   - Bidding: Maximize Conversions (you now have conversion data from the Smoke test)

2. **Campaign B — Custom Intent Audiences:**
   - Build 2 custom intent audiences:
     - Audience 1 (pain-point keywords): 10-15 keywords the ICP searches when experiencing the problem
     - Audience 2 (competitor + industry): competitor URLs and industry resource URLs
   - Budget share: 40% of GDN allocation
   - Bidding: Maximize Conversions

3. **Create 3 ad groups per campaign** (one per top pain point from Smoke results):
   - Each ad group gets 4-5 responsive display ad variants
   - Carry over Smoke test winning creatives and add 2-3 new variants

4. **Configure exclusions:**
   - Exclude all placements that produced clicks but zero conversions in the Smoke test
   - Exclude mobile app inventory
   - Exclude below-the-fold placements
   - Set frequency cap: 5 impressions per user per week

**Meta Audience Network (40% of budget — $800-1,200):**

5. **Campaign C — Retargeting:**
   - Audience: website visitors from last 30 days who did not convert (from Meta Pixel)
   - Budget share: 50% of Meta allocation
   - This is your highest-conversion audience; retarget aggressively

6. **Campaign D — Lookalike:**
   - Export top customers from Attio, hash emails, upload to Meta
   - Create 1% lookalike audience
   - Budget share: 30% of Meta allocation

7. **Campaign E — Interest-based:**
   - Target interests matching the problem space (not solution category)
   - Budget share: 20% of Meta allocation
   - This is experimental; evaluate after 2 weeks

Set daily budgets across all campaigns: $70-100/day total ($2,100-3,000 for 4 weeks).

### 2. Build Landing Pages for Display Traffic

Run the `landing-page-pipeline` drill:

1. Create dedicated landing pages for display traffic — one per pain point (3 total)
2. Each page must:
   - Match the ad creative exactly (same headline, same pain point, same offer)
   - Include a clear form above the fold (name, email, company for a content download; add role for demo requests)
   - Remove navigation (no exits except the CTA)
   - Load fast (display traffic has lower intent; slow pages kill conversion)
3. Install PostHog tracking on each page: page_view, scroll_depth, form_focus, form_submit
4. Configure UTM parameter capture so every conversion carries its source campaign and placement

### 3. Deploy Automated Lead Routing

Run the `paid-social-lead-routing` drill adapted for display:

Since display ads drive to landing pages (not platform-native lead forms), leads come through website form submissions:

1. Build an n8n workflow triggered by PostHog `display_conversion` webhook:
   - Extract lead data from form submission event
   - Enrich via Clay: company data, LinkedIn profile, ICP scoring
   - Create or update contact in Attio with: `source: display-ads`, `platform` (google/meta), `campaign`, `placement_domain`, `pain_point`, `lead_score`
   - If lead_score >= 70: create deal in Attio, add to Loops high-intent nurture, send Slack alert
   - If lead_score < 70: add to Loops educational nurture

2. Build a weekly lead quality report (n8n workflow, Monday mornings):
   - Pull all display leads from Attio created in the last 7 days
   - Calculate: leads submitted, leads enriched, leads scored >= 70, leads that booked meetings
   - Compare lead quality by platform and campaign type
   - Log as PostHog event: `display_lead_quality_weekly`

### 4. Install Full Conversion Tracking

As part of the `display-campaign-build` drill:

1. **Google Ads:** Create conversion actions for form_submit, demo_booked. Import PostHog events as Google Ads offline conversions via the API.
2. **Meta:** Verify Pixel fires on all landing pages. Configure Conversions API (CAPI) for server-side event deduplication.
3. **PostHog events:**
   - `display_click` (UTM parameter capture on landing page load)
   - `display_page_view` (page view with display source)
   - `display_scroll_50` (scroll depth trigger)
   - `display_form_focus` (user interacts with form)
   - `display_conversion` (form submission)
   - Properties on each: `platform`, `campaign_id`, `ad_group`, `placement_domain`, `pain_point`, `creative_variant`
4. **Build the PostHog funnel:**
   `display_click > display_page_view > display_scroll_50 > display_form_focus > display_conversion`

### 5. Weekly Performance Review

Every Monday, review campaign performance manually:

1. **Google Ads placement report:** Pull per-domain performance. Identify:
   - Top 5 placements by CTR and conversion rate (increase bids or budget share)
   - Bottom 5 placements by CTR or with clicks but zero conversions (exclude)
   - New placements discovered by custom intent targeting (evaluate and add to managed placements if quality is high)

2. **Cross-platform comparison:**
   - GDN managed placements vs. custom intent: which produces lower CPA?
   - Meta retargeting vs. lookalike vs. interest: which produces the most qualified leads?
   - Which pain point produces the best conversion rate across platforms?

3. **Creative performance:**
   - Pause any creative with CTR below 0.05% after 2,000+ impressions
   - Identify the top-performing hook type and pain point
   - Queue 2-3 new creatives inspired by winners for the next rotation

4. **Budget reallocation:**
   - Shift budget from underperforming campaigns/segments to winners
   - If Meta retargeting CPA is 50%+ lower than cold campaigns, increase its share
   - If a custom intent audience outperforms managed placements, consider increasing its allocation

### 6. Evaluate at 4 Weeks

Run the `threshold-engine` drill:

1. Total impressions (threshold: >=200,000)
2. Total qualified leads (threshold: >=20, where qualified = lead_score >= 70 in Attio)
3. Cost per qualified lead (threshold: below $150)
4. Best-performing placement domains (these become your Scalable priority list)
5. Best-performing audience type (managed placements vs. custom intent vs. retargeting vs. lookalike)
6. Landing page conversion rate trend: stable, improving, or declining?

**If PASS:** Display ads produce repeatable qualified leads across platforms. Proceed to Scalable with expanded budget, automated creative rotation, and data-driven budget allocation.

**If FAIL:** Diagnose:
- Low impressions but good CTR: placements are too small. Expand the placement list or add topic targeting alongside managed placements.
- Low CTR across all placements: creative is not resonating. Test more aggressive pain agitation, specific offers (calculator, benchmark), or different image styles.
- High click volume but low conversions: landing page is the bottleneck. Improve message match between ads and pages, simplify the form, or test a different offer.
- Low lead quality: audience targeting is too broad. Focus on managed placements over broad targeting. Tighten custom intent keywords.

## Time Estimate

- 5 hours: Campaign build across GDN and Meta (structure, targeting, creative, tracking, lead routing)
- 2 hours: Landing page creation and tracking setup
- 8 hours: Weekly reviews and optimization over 4 weeks (~2 hours/week)
- 1 hour: Lead routing workflow setup and testing
- 2 hours: Final threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (GDN) | Display campaigns on industry sites | Ad spend ($1,200-1,800/mo) |
| Meta Ads (Audience Network) | Display retargeting and lookalike campaigns | Ad spend ($800-1,200/mo) |
| PostHog | Analytics — funnel tracking, conversion attribution | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead management, deal tracking | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring and company data | $149/mo (Starter) or $349/mo (Explorer) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences for display leads | $49/mo (Starter) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — lead routing workflows | $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |
| Webflow | Landing pages for display traffic | $14/mo (Basic) or $29/mo (CMS) — [webflow.com/pricing](https://webflow.com/pricing) |

**Estimated play-specific cost this level:** $2,000-3,000/mo ad spend + ~$265-480/mo tools (Clay, Loops, n8n, Webflow). Total: $2,265-3,480/mo.

## Drills Referenced

- `display-campaign-build` — build and launch display campaigns on GDN and Meta Audience Network with managed placements, custom intent audiences, creative, tracking, and CRM integration
- `landing-page-pipeline` — build high-converting landing pages for display traffic with PostHog tracking and form optimization
- `paid-social-lead-routing` — route display-sourced leads through Clay enrichment, Attio CRM, and Loops email nurture automatically within 5 minutes of form submission
