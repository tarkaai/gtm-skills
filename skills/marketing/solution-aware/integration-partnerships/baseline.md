---
name: integration-partnerships-baseline
description: >
  Integration Partnerships — Baseline Run. Formalize partner outreach, build 3+ integrations with
  co-marketing launches, and establish PostHog tracking to attribute leads to specific partners.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Product, Content, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥3 integration partnerships and ≥20 qualified leads in 8 weeks"
kpis: ["Integration activation rate", "Partner-sourced lead conversion", "Cost per lead by partner", "Partner response-to-signed rate"]
slug: "integration-partnerships"
install: "npx gtm-skills add marketing/solution-aware/integration-partnerships"
drills:
  - posthog-gtm-events
  - integration-launch-campaign
  - warm-intro-request
---

# Integration Partnerships — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Product, Content, Email

## Outcomes

Three or more signed integration partnerships, each with a co-marketing launch campaign, generating a combined 20+ qualified leads attributed to partner audiences within 8 weeks. This proves the integration partnership motion is repeatable across multiple partners.

## Leading Indicators

- 5+ partner exploratory calls completed in the first 2 weeks
- Integration activation rate ≥ 15% (visitors to the integration page who activate)
- At least 2 partners agree to distribute a co-marketing announcement to their audience
- Partner-sourced leads show up in PostHog within 48 hours of each partner's distribution

## Instructions

### 1. Configure integration partnership tracking

Run the `posthog-gtm-events` drill to define the event taxonomy for integration partnerships. Implement these events:

- `integration_landing_page_viewed` — user visits an integration landing page (properties: `partner_slug`, `utm_source`, `utm_medium`)
- `integration_activated` — user enables or installs an integration (properties: `partner_slug`, `integration_type`)
- `integration_first_sync` — first successful data transfer through the integration (properties: `partner_slug`, `sync_type`)
- `integration_lead_captured` — a new lead arrives from partner distribution (properties: `partner_slug`, `channel`, `utm_campaign`)

Build the integration funnel: `integration_landing_page_viewed` -> `integration_activated` -> `integration_first_sync`. Filter by `partner_slug` to measure per-partner conversion.

### 2. Expand partner outreach

Using the partner list from Smoke level (or re-running the integration partner discovery workflow (see instructions below) for fresh candidates), run the `warm-intro-request` drill for the next batch of 10-15 partners. Target partners where:
- Smoke level showed the integration type works (similar product category, similar integration complexity)
- The partner has a distribution channel with ≥1,000 reach (email list, active blog, social following)

**Human action required:** Conduct exploratory calls with interested partners. During each call:
- Confirm audience overlap (their users match your ICP)
- Agree on integration scope (which data flows, which use cases)
- Agree on co-marketing scope (which channels each side will distribute through)
- Set a launch date

Log all partner conversations in Attio. Move partners through statuses: Prospect -> In Conversation -> Integration Agreed -> Building -> Launched.

### 3. Build and launch integrations

For each signed partner, run the `integration-launch-campaign` drill. This generates co-marketing assets (landing page copy, blog post, email announcements), configures PostHog tracking, sends your audience announcement, and provides the partner with their distribution package.

Execute 3-5 integration launches over 4-6 weeks. Stagger launches by at least 1 week to avoid audience fatigue and to allow time for per-launch analysis.

### 4. Measure per-partner performance

After each launch, track for 14 days:
- Landing page views by UTM source (your channels vs partner channels)
- Integration activations by partner
- Leads captured by partner
- Activation-to-first-sync rate (integration quality signal)

Compare partners against each other. Identify which partner characteristics predict success: partner audience size, distribution channel type (email vs blog vs social), integration complexity, or co-marketing effort level.

### 5. Evaluate against threshold

Measure against: ≥3 integration partnerships signed AND ≥20 qualified leads from partner audiences in 8 weeks. If PASS, proceed to Scalable. If FAIL, analyze:
- If <3 partnerships signed: improve outreach messaging, offer to build integrations at zero cost to partner
- If partnerships signed but <20 leads: partner distribution was weak — negotiate stronger co-marketing commitments or target partners with larger audiences

## Time Estimate

- PostHog event configuration: 2 hours
- Partner outreach (10-15 contacts): 3 hours
- Partner calls and negotiation: 4 hours
- Integration builds (3 lightweight integrations): 6 hours
- Co-marketing launch execution (per partner): 1 hour each (3 hours total)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Free tier: 100 credits/mo; Pro: $149/mo (https://www.clay.com/pricing) |
| Attio | CRM for partner pipeline tracking | Free tier: 3 users; Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Integration event tracking and funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Loops | Email announcements to your audience | Free tier: 1,000 contacts; Starter: $49/mo (https://loops.so/pricing) |

## Drills Referenced

- `posthog-gtm-events` — define and implement the integration partnership event taxonomy in PostHog
- `integration-launch-campaign` — execute co-marketing launch for each new integration (assets, tracking, distribution)
- `warm-intro-request` — find mutual connections and request introductions to partner contacts
