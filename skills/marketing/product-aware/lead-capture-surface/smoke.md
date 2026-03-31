---
name: lead-capture-surface-smoke
description: >
  Single CTA Lead Capture — Smoke Test. Deploy one lead capture surface (inline calendar,
  short form, or chat widget) on one high-intent page. Send 50 product-aware visitors to it.
  Validate whether the surface converts warm traffic into leads at ≥ 3% rate.
stage: "Marketing > ProductAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 3% conversion rate from ≥ 50 product-aware visitors in 1 week"
kpis: ["Conversion rate (leads / visitors, target ≥ 3%)", "CTA click-through rate (target ≥ 10%)", "Time from CTA click to lead captured (target < 3 min)"]
slug: "lead-capture-surface"
install: "npx gtm-skills add marketing/product-aware/lead-capture-surface"
drills:
  - lead-capture-surface-setup
  - threshold-engine
---

# Single CTA Lead Capture — Smoke Test

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

Prove that a single lead capture surface on a high-intent page converts product-aware visitors into leads. Product-aware visitors already know your product exists -- the bottleneck is giving them a frictionless way to take the next step. This test deploys one surface type on one page and measures whether it hits a minimum conversion threshold.

Pass: ≥ 3% conversion rate (leads captured / unique visitors) from ≥ 50 product-aware visitors within 7 days.
Fail: < 3% conversion rate after 50+ visitors, or fewer than 50 visitors reached in 7 days.

## Leading Indicators

- First lead arrives within 48 hours of deploying the surface (the page is discoverable and the CTA is compelling)
- CTA click-through rate exceeds 10% (visitors are noticing and engaging with the surface)
- At least 1 lead comes from a visitor you did not directly send to the page (organic discovery signal)
- Time from CTA click to lead captured is under 3 minutes (the surface has low friction)
- No visitors report technical issues with the form, calendar, or chat widget (the surface works reliably)

## Instructions

### 1. Deploy the lead capture surface

Run the `lead-capture-surface-setup` drill. Choose ONE surface type based on your sales motion:

- **Inline calendar** if your next step is a sales conversation. Use the `calcom-inline-embed` fundamental to embed a Cal.com scheduling widget directly on the page. Place it below the value proposition with a heading like "Pick a time -- 30-minute discovery call."
- **Short form** if your next step is a trial, resource download, or email nurture. Use the `webflow-forms` fundamental to build a 2-3 field form (name, email, one qualifying question). Button copy should match the action: "Start free trial" or "Download the guide."
- **Chat widget** if visitors need to ask questions before committing. Use the `intercom-bots` fundamental to deploy a qualification bot that captures email and routes high-intent visitors to a booking link.

The drill handles PostHog event tracking (`cta_impression`, `cta_clicked`, `lead_captured`), n8n webhook routing to Attio CRM, and Loops nurture sequence enrollment.

Test end-to-end before driving traffic: load the page, interact with the surface, verify PostHog events fire, verify the Attio record is created, verify the Loops sequence triggers.

### 2. Drive 50 product-aware visitors to the page

**Human action required:** You need to send product-aware visitors to the page. These are people who already know your product -- not cold traffic. Options:

- Email existing contacts who have visited your site or engaged with content: "We made it easier to [take next step] -- [link to page]"
- Add the page link to your email signature for 1 week
- Post the link in communities where you are already active and the audience knows your product
- If running outbound, replace your current CTA link with this page's URL
- Share the page link in relevant Slack/Discord communities where you have presence

Target: 50 unique visitors matching your ICP within 7 days.

### 3. Track results manually

For the Smoke test, track daily in a spreadsheet or Attio notes:
- Unique visitors to the page (from PostHog or server analytics)
- Leads captured (from Attio records created via n8n webhook)
- For each lead: which surface type converted them, how they found the page, time from page load to conversion

If PostHog is already installed, the events from step 1 will capture this automatically. If not, manual tracking is sufficient at Smoke level.

### 4. Evaluate after 7 days

Run the `threshold-engine` drill to measure against the pass threshold.

Count: total unique visitors, total leads captured, conversion rate (leads / visitors).

- **PASS (≥ 3% conversion rate from ≥ 50 visitors):** The surface works. Document: which surface type you used, where you placed it, the CTA copy, and the conversion rate. Proceed to Baseline.
- **MARGINAL (1-2% conversion rate):** Check: Were visitors actually product-aware, or was traffic too cold? Was the CTA visible without scrolling? Was the surface type right for your sales motion? Fix the weakest element and re-run with 50 fresh visitors.
- **FAIL (< 1% or 0 leads):** Diagnose: Did the surface render correctly (check browser console for errors)? Did visitors scroll to the CTA? Did anyone click but not complete? If the surface worked but nobody converted, try a different surface type or a different page.

## Time Estimate

- Surface deployment and n8n webhook setup: 1.5 hours
- End-to-end testing: 30 minutes
- Driving traffic over 7 days: 1 hour total (composing emails/posts)
- Monitoring and evaluation: 1 hour
- Total: ~4 hours of active work spread over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Inline scheduling embed (if calendar surface) | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Webflow | Landing page + form (if form surface) | Free starter or CMS $23/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Tally | Alternative form builder (if form surface) | Free plan — unlimited forms and submissions ([tally.so/pricing](https://tally.so/pricing)) |
| Intercom | Chat widget + qualification bot (if chat surface) | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Attio | CRM — log leads and create deals | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Webhook routing from surface to CRM | Free self-hosted or Starter €24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| PostHog | Event tracking (optional at Smoke) | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

**Estimated monthly cost for Smoke:** $0 (all tools on free tiers, except Intercom if using chat surface: $29/mo)

## Drills Referenced

- `lead-capture-surface-setup` — build and deploy the lead capture surface (form, calendar, or chat widget) with tracking, CRM routing, and nurture sequence enrollment
- `threshold-engine` — evaluate conversion rate against the pass threshold and recommend next action
