---
name: paid-social-ads-baseline
description: >
  Paid Social Ads — Baseline Run. Scale the winning smoke test to always-on with $1,000-3,000/mo
  budget, add lead routing automation, and run retargeting. Prove repeatable lead generation
  with ≥ 8 leads or ≥ 4 meetings over 2 weeks.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 8 leads or ≥ 4 meetings over 2 weeks"
kpis: ["Cost per lead (CPL)", "Cost per meeting (CPM)", "Lead-to-meeting conversion rate", "Lead-to-ICP match rate", "Ad platform ROAS"]
slug: "paid-social-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-social-ads"
drills:
  - paid-social-lead-routing
  - retargeting-setup
  - budget-allocation
  - posthog-gtm-events
  - threshold-engine
---

# Paid Social Ads — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Generate at least 8 leads or 4 meetings over 2 weeks with $1,000-3,000/mo ad spend. This proves paid social is a repeatable lead channel, not a one-time fluke. You also prove that automated lead routing works: every lead that fills out a form lands in your CRM, gets enriched, scored, and receives a nurture email within 5 minutes.

## Leading Indicators

- CPL trending stable or declining week-over-week (campaign is optimizing, not degrading)
- Lead-to-ICP match rate stays above 50% at higher volume (targeting holds quality at scale)
- Nurture email open rate above 40% (leads are real and engaged)
- At least 1 lead replies to a nurture email or books via the Cal.com link (downstream signal)
- Retargeting audience growing (website visitors are being captured for re-engagement)

## Instructions

### 1. Set up end-to-end tracking

Run the `posthog-gtm-events` drill to establish event tracking for the full paid social funnel:
- `paid_social_ad_impression` — ad served (pulled from ad platform API via n8n)
- `paid_social_ad_click` — ad clicked
- `paid_social_landing_page_view` — landing page loaded (PostHog pageview with UTM params)
- `paid_social_form_submit` — lead gen form or landing page form completed
- `paid_social_lead_enriched` — Clay enrichment completed
- `paid_social_lead_scored` — ICP score assigned
- `paid_social_meeting_booked` — meeting booked via Cal.com or manual logging

Tag every event with properties: `platform` (linkedin/meta), `campaign_id`, `ad_variant_id`, `audience_segment`, `pain_point`.

### 2. Build lead routing automation

Run the `paid-social-lead-routing` drill to set up:
- n8n workflow polling LinkedIn Lead Gen API every 15 minutes for new submissions
- n8n workflow listening for Meta leadgen webhooks (with 15-minute polling fallback)
- For each new lead: deduplicate against Attio, enrich via Clay, score against ICP, create contact in Attio, trigger Loops nurture sequence
- High-value lead alert (score >= 80) sends Slack notification to the team with name, company, title, and which ad they responded to
- Target: lead form submission to CRM entry in under 5 minutes

### 3. Expand creative from smoke test winners

Run the the paid social creative pipeline workflow (see instructions below) drill to create additional variants:
- Take the winning variant type from smoke (stat/question/proof hook) and write 3 new versions with different pain points
- Add a second pain point from your ICP — create 3 variants for it
- Total: 6-9 active variants across 2 pain points
- Use the same ad format that won in smoke (lead gen form vs. landing page)

### 4. Add a second audience segment

Expand from 1 to 2 audience segments. If your smoke test ran on LinkedIn Core ICP, add:
- LinkedIn Adjacent ICP (broader industry/company size)
- OR Meta 1% lookalike from your customer list (if not tested in smoke)

Run each audience as a separate campaign to isolate performance data. Do NOT mix audiences in the same campaign.

### 5. Set up retargeting

Run the `retargeting-setup` drill to capture and re-engage visitors who clicked but did not convert:
- Install LinkedIn Insight Tag and Meta Pixel on all landing pages (if not done in smoke)
- Create retargeting audiences: landing page visitors last 14 days who did NOT submit a form
- Create retargeting ads with stronger CTAs: "Still dealing with [problem]? Here's the checklist 200+ teams use." or offer a different resource than the original ad
- Set retargeting budget to 15-20% of total ad spend
- Set frequency cap: max 3 impressions per person per week

### 6. Allocate and pace budget

Run the `budget-allocation` drill with baseline-specific settings:
- Total budget: $1,000-3,000 for the 2-week period
- Split: 70% to the audience segment that performed best in smoke, 20% to the new segment, 10% to retargeting
- Set daily budget caps to prevent front-loading spend
- If one audience has CPL 50%+ higher than the other after 5 days, shift 20% of its budget to the winner

### 7. Monitor weekly and adjust once

At the end of week 1, review:
- CPL by audience segment and variant
- Lead quality: what % of leads match ICP? Are enriched leads converting to meetings?
- Creative performance: which variants have the highest CTR and lowest CPL?
- Retargeting performance: any conversions from retargeting?

Make ONE set of adjustments:
- Pause variants with CTR below 0.3% (LinkedIn) or 0.8% (Meta) after 500+ impressions
- Shift budget toward the better-performing audience segment
- Refresh any creative that has been running for 10+ days with declining CTR

Do NOT make daily changes. Let the data accumulate.

### 8. Evaluate against threshold

Run the `threshold-engine` drill at the end of week 2. Compare to: **≥ 8 leads or ≥ 4 meetings over 2 weeks**.

Check quality metrics alongside volume:
- Lead-to-ICP match rate: target ≥ 50%
- Lead-to-meeting conversion rate: target ≥ 15% of ICP-matching leads
- CPL: benchmark against your target CPA (usually CPL should be under 30% of expected deal value)

Decision:
- **PASS:** 8+ leads with ≥50% ICP match, or 4+ meetings. Lead routing automation is working. Proceed to Scalable.
- **MARGINAL:** 5-7 leads or 2-3 meetings. Stay at Baseline. Test new pain points, audiences, or offers for 2 more weeks.
- **FAIL:** <5 leads and <2 meetings. Diagnose: Is it targeting (low ICP match)? Creative (low CTR)? Offer (low conversion)? Budget (insufficient spend)? Fix the weakest link and re-run.

## Time Estimate

- 3 hours: Lead routing automation setup (n8n workflows, Loops sequences)
- 2 hours: Tracking setup (PostHog events, UTM parameters)
- 2 hours: Creative expansion (6-9 new variants)
- 1 hour: Retargeting setup
- 1 hour: Budget allocation and campaign configuration
- 1 hour: Week 1 review and adjustment
- 2 hours: Final evaluation, documentation, and reporting

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | B2B paid social advertising | $1,000-3,000/mo ad spend. CPC $4-12. [Pricing](https://business.linkedin.com/marketing-solutions/ads/pricing) |
| Meta Ads | Retargeting and lookalike campaigns | Included in above budget. CPC $0.50-3.00. [Pricing](https://www.facebook.com/business/ads/pricing) |
| Clay | Lead enrichment and ICP scoring | $185/mo Launch plan (2,500 credits). [Pricing](https://clay.com/pricing) |
| Loops | Nurture email sequences | Free up to 1,000 contacts. [Pricing](https://loops.so/pricing) |
| Webflow | Landing pages | $14/mo Basic. [Pricing](https://webflow.com/pricing) |
| PostHog | Funnel tracking and analytics | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| n8n | Lead routing automation | Free self-hosted or $20/mo cloud. [Pricing](https://n8n.io/pricing) |

**Estimated baseline monthly cost:** $1,000-3,000 ad spend + ~$235 tooling = $1,235-3,235/mo

## Drills Referenced

- the paid social creative pipeline workflow (see instructions below) — expand winning smoke test creative to 6-9 variants across 2 pain points
- `paid-social-lead-routing` — automate lead flow from ad forms to CRM with enrichment and nurture
- `retargeting-setup` — capture non-converters and re-engage with stronger CTAs
- `budget-allocation` — distribute budget across audience segments and retargeting
- `posthog-gtm-events` — set up end-to-end event tracking for the paid social funnel
- `threshold-engine` — evaluate baseline results against the pass threshold
