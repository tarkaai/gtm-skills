---
name: lead-capture-surface-baseline
description: >
  Single CTA Lead Capture — Baseline Run. Instrument the lead capture surface with full
  PostHog funnel tracking, build a dedicated landing page optimized for conversion, and
  run always-on lead routing. Validate ≥ 4% conversion rate over 2 weeks with proper
  attribution and CRM pipeline integration.
stage: "Marketing > ProductAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 4% conversion rate over 2 weeks with full funnel instrumentation and always-on lead routing"
kpis: ["Conversion rate (target ≥ 4%)", "CTA click-through rate (target ≥ 12%)", "Form/widget completion rate (target ≥ 50% of those who click)", "Lead-to-meeting rate (target ≥ 30%)", "Time from lead capture to CRM record creation (target < 60 seconds)"]
slug: "lead-capture-surface"
install: "npx gtm-skills add marketing/product-aware/lead-capture-surface"
drills:
  - posthog-gtm-events
  - landing-page-pipeline
  - lead-capture-surface-setup
---

# Single CTA Lead Capture — Baseline Run

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

Move from a manually tracked Smoke test to a fully instrumented, always-on lead capture system. Build a dedicated landing page (or optimize the existing high-intent page), install comprehensive PostHog funnel tracking, and automate the entire lead-to-CRM pipeline. The system runs continuously without manual intervention for lead routing.

Pass: ≥ 4% conversion rate over 2 weeks, with all leads automatically routed to Attio CRM within 60 seconds and PostHog funnels showing the full conversion path.
Fail: < 4% conversion rate after 2 weeks, or lead routing requires manual steps.

## Leading Indicators

- PostHog funnel shows data within 24 hours of deployment (tracking is working)
- CTA click-through rate exceeds 12% (improved from Smoke through copy and placement optimization)
- Form/widget completion rate exceeds 50% of those who click the CTA (low-friction surface)
- At least 1 lead per day on average over the 2-week period (volume is sufficient to judge)
- Lead-to-Attio record creation happens in under 60 seconds (automation is reliable)
- No manual data entry required for any lead captured

## Instructions

### 1. Set up full event tracking

Run the `posthog-gtm-events` drill to establish the event taxonomy for lead capture surfaces. Ensure these events are configured and firing:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `cta_impression` | CTA container enters viewport | `page`, `surface_type`, `cta_variant`, `utm_source`, `device_type` |
| `cta_clicked` | Visitor clicks or interacts with the CTA | `page`, `surface_type`, `cta_variant`, `utm_source`, `device_type` |
| `lead_captured` | Form submitted, meeting booked, or email collected | `page`, `surface_type`, `utm_source`, `cta_variant`, `lead_email` |

Build a PostHog funnel: `cta_impression` -> `cta_clicked` -> `lead_captured`. Break down by `page`, `utm_source`, `device_type`, and `cta_variant`. Set the conversion window to 30 minutes (lead capture should be fast).

Save as: "Lead Capture Funnel - Baseline"

Add person properties to each lead captured:
- `first_touch_channel`: the `utm_source` value from the page URL
- `capture_surface_type`: form, calendar, or chat
- `capture_page`: which page they converted on

### 2. Build or optimize the landing page

Run the `landing-page-pipeline` drill to build a dedicated landing page (or optimize the existing page from Smoke). The page structure:

- **Hero:** Headline focused on the visitor's next step (not your product features). Under 10 words. Subheadline explains what happens after they convert. Example: "See how [product] works for your team" / "Book a 30-minute walkthrough. No commitment."
- **Social proof:** Customer logos, a testimonial quote, or a specific metric ("500+ teams use [product]")
- **The CTA surface:** Place the lead capture surface (calendar, form, or chat) prominently. Above the fold on desktop. Immediately visible after one scroll on mobile.
- **Supporting content:** 3 bullet points answering "Why now?" — what the visitor gets by taking action today
- **Objection handling:** 2-3 FAQ items addressing the most common hesitations (time commitment, pricing, what to expect)
- **No navigation links.** The page has one exit: the CTA or the back button.

Use the `webflow-landing-pages` fundamental to build the page. Install the PostHog tracking events from step 1.

### 3. Deploy the always-on lead capture surface

Run the `lead-capture-surface-setup` drill to deploy (or update) the surface on the new landing page. If you used a different surface type than Smoke and it performed better in testing, switch. Otherwise, keep the surface type that passed Smoke.

Ensure the full automation pipeline is active:
- Surface interaction -> PostHog events fire
- Lead captured -> n8n webhook -> Attio Person + Company + Deal created
- Lead captured -> Loops nurture sequence enrollment
- If calendar surface: Cal.com booking -> pre-meeting prep email via Loops

Test end-to-end: submit a test conversion, verify PostHog events, verify Attio record creation time (must be < 60 seconds), verify Loops enrollment.

### 4. Drive consistent traffic over 2 weeks

**Human action required:** Maintain a steady flow of product-aware visitors to the page. Continue the traffic sources from Smoke, plus:

- Add the page URL as the primary CTA in all outbound communications
- Link to it from relevant pages on your website (pricing page footer, product page sidebar, blog post CTAs)
- If running any content marketing or social posts, point CTAs to this page

Target: enough traffic to generate at least 1 lead per day on average. If traffic is too low to measure conversion rate reliably, increase promotion effort.

### 5. Analyze the funnel after 2 weeks

Review the PostHog funnel built in step 1:
- Overall conversion rate: `lead_captured / cta_impression`
- Breakdown by device type: is mobile conversion significantly lower than desktop?
- Breakdown by traffic source: which sources produce the highest conversion rate?
- Drop-off analysis: where in the funnel do visitors leave? After impression? After click? After starting the form?

- **PASS (≥ 4% conversion rate, automation working):** The lead capture surface is a reliable, instrumented conversion channel. Document: page URL, surface type, conversion rate by source, and the full PostHog funnel. Proceed to Scalable.
- **MARGINAL (3-4% conversion rate):** Analyze the funnel for the biggest drop-off. If click-through is low, test new CTA copy or placement. If completion rate is low, simplify the form or shorten the booking flow. Stay at Baseline and re-measure after changes.
- **FAIL (< 3% conversion rate):** The improvement from Smoke did not hold with sustained traffic. Check: Is the new traffic actually product-aware? Is the landing page clear about what happens next? Is the surface type still the right choice? Fix the weakest link and re-run.

## Time Estimate

- PostHog event taxonomy and funnel setup: 2 hours
- Landing page build or optimization: 4 hours
- Lead capture surface deployment and automation testing: 2 hours
- Traffic driving over 2 weeks: 2 hours total
- Analysis and evaluation: 2 hours
- Total: ~12 hours of active work spread over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, event tracking, person properties | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Webflow | Landing page build | CMS plan $23/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Cal.com | Inline scheduling embed (if calendar surface) | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Tally | Form builder (if form surface) | Free plan ([tally.so/pricing](https://tally.so/pricing)) |
| Intercom | Chat widget (if chat surface) | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Attio | CRM — lead records and deal pipeline | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Webhook routing, lead automation | Starter €24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Nurture sequence emails | Free up to 1,000 contacts; Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Baseline:** $25-75/mo (Webflow CMS + n8n Starter; other tools on free tiers)

## Drills Referenced

- `posthog-gtm-events` — establish the event taxonomy for lead capture surfaces with standard event names, properties, and PostHog funnels
- `landing-page-pipeline` — build a high-converting landing page with proper structure, tracking, and form/CTA integration
- `lead-capture-surface-setup` — deploy or update the lead capture surface with full automation pipeline (PostHog + n8n + Attio + Loops)
