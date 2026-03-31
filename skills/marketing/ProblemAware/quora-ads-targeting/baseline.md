---
name: quora-ads-targeting-baseline
description: >
  Quora Ads — Baseline Run. First always-on Quora Ads campaigns with multi-targeting (topics,
  questions, keywords), retargeting audiences, automated lead routing through enrichment and scoring
  into CRM and nurture sequences. Validate repeatable qualified lead generation at sustainable CPA.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Communities"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=50,000 impressions and >=15 qualified leads from $1,500-2,500 budget over 4 weeks, with cost per qualified lead below $175"
kpis: ["Impressions", "CTR", "CPC", "Conversions", "Cost per qualified lead", "Lead quality (% scoring 70+)", "Targeting type CPA comparison"]
slug: "quora-ads-targeting"
install: "npx gtm-skills add Marketing/ProblemAware/quora-ads-targeting"
drills:
  - quora-ads-campaign-build
  - paid-social-lead-routing
  - posthog-gtm-events
---

# Quora Ads — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Communities

## Outcomes

First always-on Quora Ads campaigns. The agent builds multi-targeting campaigns (topics, questions, and keywords), configures retargeting audiences, and deploys automated lead routing. Leads flow from Quora click through landing page conversion, Clay enrichment, ICP scoring, Attio CRM, and Loops nurture sequences without manual intervention. The goal is to prove Quora Ads generate repeatable, qualified leads at a sustainable cost per qualified lead.

**Pass threshold:** >=50,000 impressions and >=15 qualified leads from $1,500-2,500 budget over 4 weeks, with cost per qualified lead below $175.

## Leading Indicators

- CTR sustains above 0.8% across all ad sets
- CPC remains below $3.00 (target: $1.00-2.50)
- At least 2 of 3 targeting types (topic, question, keyword) produce qualified leads
- Lead quality: >=50% of leads score 70+ on ICP scoring via Clay
- Landing page conversion rate sustains above 3%
- Retargeting audience builds to 300+ users within 2 weeks (minimum for Quora audience targeting)
- CAPI match rate exceeds 60% (conversion events sent server-side match Quora click data)

## Instructions

### 1. Expand Campaign Structure

Run the `quora-ads-campaign-build` drill with expanded scope:

1. Create a new campaign: `quora-ads-targeting-baseline-{date}`, objective `Conversions`, daily budget $55-90/day
2. Build 3 ad sets using all three contextual targeting types:
   - **Ad Set 1 — Topic Targeting**: Expand from Smoke. Use 15-20 topics across Tier 1 (core problem) and Tier 2 (adjacent problem). Budget share: 40%
   - **Ad Set 2 — Question Targeting**: Expand from Smoke. Target 50-100 questions grouped by theme. Include new questions discovered from Smoke click data (which topics drove traffic? Find more questions in those topics). Budget share: 30%
   - **Ad Set 3 — Keyword Targeting**: New for Baseline. 20-30 keywords based on ICP pain points and Smoke learnings. Include both broad terms ("deployment automation") and specific terms ("kubernetes CI/CD pipeline"). Budget share: 30%
3. Carry forward winning ad variants from Smoke. Add 2-3 new variants incorporating Smoke creative learnings (which hook type won? create more in that style)
4. Add Text Ad variants for every Image Ad — test format preference at scale
5. All ad sets: CPC bidding, starting bids based on Smoke CPC data (set bid at Smoke CPC + 20% for competitive delivery)

**Human action required:** Create the expanded campaign in Quora Ads Manager following the agent's brief. Launch after tracking verification.

### 2. Configure Retargeting Audiences

Using the Quora Ads Manager audience tools:

1. **Website Traffic Audience**: Create a retargeting audience from Quora Pixel data:
   - All landing page visitors from Smoke who did not convert
   - All website visitors from the last 30 days
   - Minimum 300 users required before Quora will serve ads to this audience
2. **List Match Audience**: Upload email addresses from Attio:
   - Exclusion list: existing customers (do not spend ad budget on people who already pay you)
   - Target list (optional): high-value prospects from other channels who have not yet converted
3. Once the website traffic audience reaches 300+ users (typically week 2-3 of Baseline):
   - Create **Ad Set 4 — Retargeting**: Website visitors who did not convert, CPC bid $1.00 (retargeting converts at lower cost), budget share: reallocate 15% from the other 3 ad sets

**Human action required:** Create audiences and retargeting ad set in Ads Manager.

### 3. Deploy Automated Lead Routing

Run the `paid-social-lead-routing` drill adapted for Quora:

Build an n8n workflow triggered by PostHog `quora_ads_lead_captured` webhook:

1. **Capture**: Receive lead data (email, UTM parameters, qclid, form fields)
2. **Enrich**: Send to Clay for company data, LinkedIn profile, ICP scoring
3. **Score**: Clay returns lead_score (0-100 based on ICP match: job title, company size, industry, technology stack)
4. **Route to CRM**: Create or update contact in Attio with properties:
   - `source`: quora-ads
   - `campaign`: from utm_campaign
   - `ad_set`: from utm_content (includes targeting type)
   - `lead_score`: from Clay
   - `qclid`: for Quora attribution
5. **Route to email**:
   - If lead_score >= 70: Add to Loops high-intent nurture sequence, create a deal in Attio, send Slack alert to sales
   - If lead_score < 70: Add to Loops educational nurture sequence
6. **Confirm to Quora**: Fire CAPI event with qclid and hashed email for conversion attribution

### 4. Set Up Tracking Pipeline

Run the `posthog-gtm-events` drill to configure end-to-end tracking:

1. Standardize event taxonomy for the Quora play:
   - `quora_ads_page_view`: landing page load with UTM and qclid
   - `quora_ads_lead_captured`: form submission
   - `quora_ads_lead_qualified`: Clay enrichment scores lead 70+ (fired from n8n workflow)
   - `quora_ads_meeting_booked`: meeting scheduled by lead (fired from Cal.com webhook)
   - `quora_ads_deal_created`: deal created in Attio (fired from Attio webhook)
2. Build PostHog funnel: `quora_ads_page_view` > `quora_ads_lead_captured` > `quora_ads_lead_qualified` > `quora_ads_meeting_booked`
3. Set up UTM parameter parsing to attribute every PostHog event to a specific ad set, variant, and targeting type

### 5. Run for 4 Weeks with Weekly Reviews

Weekly review cadence (every Monday):

1. Pull Quora Ads Manager data: impressions, clicks, CTR, CPC, spend per ad set
2. Pull PostHog funnel data: conversion rates at each stage
3. Pull Attio data: leads created, lead scores, meetings booked
4. Analyze by targeting type: which type (topic, question, keyword) delivers the lowest cost per qualified lead?
5. Analyze by creative variant: which hook type and format (image vs text) drive the best CTR and conversion rate?
6. Action:
   - Pause any ad with CTR below 0.4% or CPC above $5.00
   - Shift 10-20% of budget from worst-performing ad set to best-performing ad set
   - If a targeting type has CPA >200% of average after 2 weeks, pause it and reallocate budget
   - Replace fatigued creatives (CTR declining for 5+ consecutive days) with new variants
   - If retargeting audience has reached 300+, launch the retargeting ad set

### 6. Evaluate at 4 Weeks

Run the `threshold-engine` drill:

1. Total impressions (threshold: >=50,000)
2. Total qualified leads (threshold: >=15, where qualified = lead_score >= 70 in Attio)
3. Cost per qualified lead (threshold: below $175)
4. Best-performing targeting type, creative format, and hook type
5. Retargeting audience size and retargeting CPA vs cold targeting CPA
6. Full-funnel conversion rate: Quora click > qualified lead (target: >=1.5%)

**If PASS:** Quora Ads generate repeatable qualified leads. Proceed to Scalable with automated creative rotation, budget optimization, and audience expansion.

**If FAIL:** Diagnose:
- Low lead volume but good CTR: landing page or offer is the bottleneck. Test a different offer (demo vs guide) or simplify the form.
- High CPC: competition is driving costs up in your topics. Test less competitive topics or shift to question targeting (typically lower CPC).
- Low lead quality: targeting is too broad. Tighten topics to Tier 1 only, add negative keywords, or use list-match exclusions more aggressively.
- One targeting type dominates: this is informative, not a failure. Consolidate budget to the winning type and test new audiences within it.

## Time Estimate

- 4 hours: Campaign expansion (new ad sets, targeting research, creative variants)
- 2 hours: Retargeting audience setup and lead routing automation
- 2 hours: Tracking pipeline configuration (PostHog events, CAPI, n8n workflows)
- 8 hours: Weekly reviews and optimization over 4 weeks (~2 hours/week)
- 2 hours: Creative refresh and ad rotation (ongoing)
- 2 hours: Final threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Quora Ads | Campaign management and ad delivery | Ad spend only ($1,500-2,500/mo) |
| PostHog | Analytics — funnel tracking, conversion attribution | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead management, deal tracking | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring and company data | $149/mo (Starter) or $349/mo (Explorer) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences for Quora leads | $49/mo (Starter) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — lead routing, CAPI, weekly reports | $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |
| Webflow | Landing page hosting | $18/mo (Basic) — [webflow.com/pricing](https://webflow.com/pricing) |

**Estimated play-specific cost this level:** $1,500-2,500/mo ad spend + ~$270-470/mo tools (Clay, Loops, n8n, Webflow). Total: $1,770-2,970/mo.

## Drills Referenced

- `quora-ads-campaign-build` — expanded campaign construction with 3 targeting types (topic, question, keyword), retargeting audiences, and refreshed creative
- `paid-social-lead-routing` — automated lead pipeline from Quora conversion through Clay enrichment, Attio CRM, and Loops nurture sequences
- `posthog-gtm-events` — standardized event taxonomy for Quora Ads tracking with full-funnel PostHog events and UTM attribution
