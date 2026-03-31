---
name: twitter-x-ads-baseline
description: >
  Twitter/X Ads — Baseline Run. Scale the proven X Ads campaign to $1,500 over 2 weeks
  with retargeting, structured A/B testing, and end-to-end conversion tracking
  from ad click to qualified lead in CRM.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=150,000 impressions and >=20 qualified leads from $1,500 budget over 2 weeks"
kpis: ["Impressions", "CTR by ad group", "Cost per lead (CPL)", "Landing page conversion rate", "Lead-to-qualified rate", "ROAS"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - budget-allocation
  - retargeting-setup
  - posthog-gtm-events
  - threshold-engine
---

# Twitter/X Ads — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Outcomes

Scale the proven X Ads campaign from $200 to $1,500 over 2 weeks. Add retargeting, structured event tracking, and budget optimization across ad groups. Prove the campaign is repeatable: >=150,000 impressions AND >=20 qualified leads.

## Leading Indicators

- Week 1 CPL within 2x of Smoke CPL (cost hasn't blown up with scale)
- Retargeting audience building (>=500 website visitors in the pixel pool by day 7)
- Conversion rate holding steady or improving vs. Smoke (landing page is not degrading)
- At least 3 ad groups actively delivering with measurable CPL differences (data to optimize with)

## Instructions

### 1. Analyze Smoke data and allocate budget

Run the `budget-allocation` drill using your Smoke test results:
- Which ad group (keyword vs. follower-lookalike) delivered lower CPL?
- Which creative variants had the highest CTR?
- Allocate 60% of budget to the winning ad group, 30% to the runner-up, 10% to a new experimental audience.
- Set daily budgets: $100-150/day for 2 weeks = $1,400-2,100 total.

### 2. Set up retargeting

Run the `retargeting-setup` drill to create retargeting audiences on X:
- **Website visitors who didn't convert**: Upload via X website tag pixel (already installed from Smoke). Create a custom audience of visitors from the last 30 days who did NOT submit the form.
- **Engaged social users**: Create an audience of users who engaged with your promoted tweets (liked, retweeted, replied, clicked) but did not visit the landing page.
- Create a dedicated ad group for each retargeting audience with tailored creative: "Still considering [solution category]? Here's what 200+ teams do differently."
- Set retargeting bid 20-30% higher than prospecting bids (these users are warmer).

### 3. Configure end-to-end tracking

Run the `posthog-gtm-events` drill to set up a complete event pipeline:
- `twitter_ads_ad_click` — captured via UTM parameters on landing page load
- `twitter_ads_page_view` — PostHog pageview with source attribution
- `twitter_ads_scroll_50` — visitor scrolled past halfway (engagement signal)
- `twitter_ads_form_view` — form entered viewport
- `twitter_ads_form_submit` — form submitted
- `twitter_ads_lead_created` — lead created in Attio (via n8n webhook)
- `twitter_ads_lead_qualified` — lead marked as ICP-qualified in Attio

Build a PostHog funnel: ad click > page view > form submit > lead qualified. This gives you true conversion rate and CPL at every stage.

### 4. Expand creative testing

Using the Smoke test creative winners as a starting point, create 3 new variants per ad group:
- **Winner riff**: Same hook type as the Smoke winner, different specific angle
- **New format**: If text-only won in Smoke, test Website Cards with images. If cards won, test text-only.
- **Stronger CTA**: Test "Get the [specific asset]" vs. "See how [result] works" vs. "Join [N] teams"

Run all variants simultaneously. After 500 impressions each, pause variants with CTR below 0.3%.

### 5. Run for 2 weeks with weekly check-ins

**Week 1 check-in (day 7):**
- Are all ad groups delivering? If any has <1,000 impressions, broaden targeting.
- Is CPL tracking? Calculate CPL per ad group. Shift budget from high-CPL to low-CPL groups.
- Is retargeting pool growing? Need >=500 visitors for retargeting to deliver.

**Week 2 check-in (day 14):**
- Final CPL and ROAS calculation
- Lead quality review: Of all leads generated, what % are ICP matches?

### 6. Evaluate against threshold

Run the `threshold-engine` drill:
- **Impressions >= 150,000**: Did the campaign scale delivery 10x from Smoke?
- **Qualified leads >= 20**: Did quality hold as volume increased?

Decision tree:
- **PASS**: Campaign scales profitably. Proceed to Scalable to automate and find 10x.
- **PARTIAL (volume met, quality missed)**: Traffic scaled but leads aren't qualifying. Tighten audience targeting or improve lead qualification criteria.
- **FAIL (neither met)**: Budget allocation issue or audience saturation. Test new audiences or platforms before re-running.

## Time Estimate

- 2 hours: Smoke data analysis and budget allocation
- 3 hours: Retargeting setup and audience creation
- 3 hours: Event tracking pipeline configuration
- 2 hours: New creative production
- 1 hour: Campaign launch and verification
- 4 hours: Weekly monitoring (2 hours per check-in)
- 3 hours: Final evaluation, documentation, and decision

**Total: ~18 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| X Ads | Promoted tweets, retargeting | $1,500 ad spend |
| PostHog | Full-funnel event tracking and funnels | Free tier (1M events/mo) |
| Webflow | Landing page hosting | ~$15/mo Starter |
| n8n | Lead routing webhook (landing page to Attio) | Free self-hosted or $20/mo cloud |

## Drills Referenced

- `budget-allocation` — Analyzes Smoke test data and allocates budget across ad groups based on performance
- `retargeting-setup` — Creates website visitor and engaged-user retargeting audiences on X
- `posthog-gtm-events` — Configures the full event tracking pipeline from ad click through lead qualification
- `threshold-engine` — Evaluates final results against the >=150,000 impressions and >=20 qualified leads threshold
