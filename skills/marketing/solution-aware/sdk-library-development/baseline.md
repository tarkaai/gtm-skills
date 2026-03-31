---
name: sdk-library-development-baseline
description: >
  SDK & Library Development — Baseline Run. Establish always-on download tracking, conversion
  funnels, and automated release cadence across 1-2 SDKs. Prove sustained developer
  signups from registry presence.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Product"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=500 downloads/month and >=10 developer signups/month from SDK registries sustained over 8 weeks"
kpis: ["Downloads per month (per registry)", "README CTA click-through rate", "Signup conversion rate (CTA click to signup)", "Developer activation rate (signup to first API call)", "SDK-sourced leads in CRM"]
slug: "sdk-library-development"
install: "npx gtm-skills add marketing/solution-aware/sdk-library-development"
drills:
  - sdk-registry-distribution
  - posthog-gtm-events
---
# SDK & Library Development — Baseline Run

> **Stage:** Marketing -> Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Product

## Outcomes
Always-on download tracking across all published SDKs, a fully instrumented conversion funnel from registry download to product activation, automated release cadence, and SDK-sourced leads flowing into the CRM. The system runs continuously without manual intervention and delivers >=500 downloads/month and >=10 developer signups/month over 8 weeks.

## Leading Indicators
- Weekly download report is generated and posted automatically
- CTA click-through rate on README is >=0.5% of downloads
- At least 1 SDK-sourced signup per week within the first 4 weeks
- SDK-sourced developers have a higher activation rate (signup to first API call) than the product average
- Release cadence: at least 1 release per month per SDK

## Instructions

### 1. Set up the event taxonomy for SDK tracking
Run the `posthog-gtm-events` drill to define SDK-specific events in your PostHog taxonomy:
- `sdk_weekly_downloads` -- weekly download counts per registry, collected by n8n
- `sdk_docs_visit` -- visit to SDK documentation pages
- `sdk_readme_cta_clicked` -- arrival at your site via registry README UTM link
- `sdk_signup_completed` -- signup by a developer arriving from an SDK source
- `sdk_api_key_created` -- first API key creation by SDK-sourced developer
- `sdk_first_api_call` -- first successful API call attributed to an SDK user-agent

Add person properties: `sdk_source_registry`, `sdk_source_language`, `first_touch_channel = sdk`.

### 2. Build the distribution tracking pipeline
Run the `sdk-registry-distribution` drill to:
- Configure n8n to collect download counts from all registries weekly
- Build PostHog funnels: downloads -> CTA clicks -> signups -> activation
- Set up automated release cadence with conversion-tracked release notes
- Route SDK-sourced signups to Attio with registry/language attribution
- Generate weekly SDK distribution reports posted to Slack

### 3. Publish a second SDK (if not already done)
If you only have one SDK, use the `sdk-package-scaffold` drill (from Smoke) to publish for the second-most-requested language. Two SDKs provide enough data to compare performance across registries and validate that the pattern works for more than one ecosystem.

**Human action required:** Review the second SDK for code quality. Test the install and quick start flow.

### 4. Optimize README CTAs based on data
After 4 weeks of tracking data, analyze:
- Which registry generates the most CTA clicks relative to downloads?
- What is the click-to-signup conversion rate per registry?
- Are developers who arrive via one registry more likely to activate?

Update README CTA copy and positioning on the lower-performing SDKs to match the patterns of the higher-performing ones.

### 5. Evaluate against threshold
Measure against: >=500 downloads/month and >=10 developer signups/month from SDK registries sustained over 8 weeks.

If PASS: The SDK channel is a repeatable source of developer leads. Proceed to Scalable.
If FAIL: Diagnose the funnel stage where drop-off occurs. Low downloads = discoverability problem (improve metadata, keywords, add more community seeding). High downloads but low CTA clicks = README problem. High CTA clicks but low signups = landing page or onboarding problem.

## Time Estimate
- PostHog event taxonomy setup: 3 hours
- n8n download tracking pipeline: 4 hours
- Conversion funnel instrumentation: 3 hours
- Second SDK scaffold and publish: 6 hours (if needed)
- CRM integration and reporting: 2 hours
- Analysis and optimization: 2 hours

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host SDK repos and CI/CD | Free for public repos |
| npm / PyPI / registries | Package distribution | Free to publish |
| PostHog | Event tracking, funnels, dashboards | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Scheduled download collection, reporting | Free self-hosted or from EUR 20/mo cloud (https://n8n.io/pricing) |
| Attio | SDK-sourced lead tracking | Free for small teams (https://attio.com/pricing) |

## Drills Referenced
- `sdk-registry-distribution` -- builds the always-on tracking pipeline across registries with download collection, conversion funnels, release automation, and CRM attribution
- `posthog-gtm-events` -- defines the event taxonomy and person properties for SDK-specific tracking
