---
name: chrome-web-store-teaser-smoke
description: >
  Chrome Extension Teaser — Smoke Test. Build and publish a minimal teaser Chrome extension
  with a lead-capture popup to validate whether developers and power users discover and install
  extensions in your problem space.
stage: "Marketing > Unaware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">=20 installs and >=1 lead in 1 week"
kpis: ["Store listing views", "Install rate", "Popup open rate", "Waitlist signups"]
slug: "chrome-web-store-teaser"
install: "npx gtm-skills add marketing/unaware/chrome-web-store-teaser"
drills:
  - chrome-extension-listing-setup
  - landing-page-pipeline
  - threshold-engine
---

# Chrome Extension Teaser — Smoke Test

> **Stage:** Marketing > Unaware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Prove that your ICP discovers browser extensions when searching for solutions to the problem you solve. A passing Smoke Test means at least 20 people installed the extension and at least 1 submitted their email through the popup waitlist form. This confirms the Chrome Web Store is a viable discovery channel before you invest in always-on automation.

## Leading Indicators

- Store listing impressions > 0 within 48 hours of publish (confirms CWS indexes your listing)
- At least 5 installs in the first 3 days (confirms search intent exists)
- At least 1 popup open per 3 installs (confirms users engage with the extension after installing)

## Instructions

### 1. Define extension scope and keywords

Run the `chrome-extension-listing-setup` drill, Step 1. Before scaffolding, research the Chrome Web Store:
- Search 10 terms your ICP would use to find a tool like yours
- Record how many competing extensions appear for each term
- Identify 3 underserved keywords (meaningful intent, fewer than 30 competitors)
- Define the extension's name using the highest-value keyword: `[Primary Keyword] - [Brand]` (max 45 characters)
- Write a 132-character short description: pain point first, then what the extension does

### 2. Build the teaser extension

Run the `chrome-extension-listing-setup` drill, Steps 1-4. Build a minimal Manifest V3 extension with:
- A popup (350px wide) containing: headline, 2-sentence value prop, 3 "coming soon" feature bullets, email capture form, link to your website
- Background script that fires `extension_installed` event to PostHog on install
- Popup script that fires `popup_opened` on load and `waitlist_form_submitted` on form submit
- Form submission sends email to Loops API, tagging the contact with `source: chrome-web-store-teaser`
- Uninstall URL set to a short survey page on your website

**Human action required:** Create 4 icon sizes (16, 32, 48, 128px PNG). Pay the $5 Chrome Web Store developer registration fee (one-time). Provide or create a privacy policy URL.

### 3. Build a landing page for extension traffic

Run the `landing-page-pipeline` drill to create a landing page at `yoursite.com/extension` or similar. This page:
- Matches the extension's messaging and keywords
- Provides more detail than the popup can hold
- Includes a demo video or product screenshots
- Has its own email capture form (tagged `source: chrome-extension-landing-page`)
- Link to this page from the extension's store listing and popup

### 4. Publish and submit for review

Run the `chrome-extension-listing-setup` drill, Step 6:
- Package the extension as a zip
- Upload via Chrome Web Store API
- Complete the store listing: detailed description (keyword-optimized), 3 screenshots (1280x800), category selection
- Submit for review (typically 1-3 business days)

**Human action required:** Approve the final listing before clicking publish. Review the permissions prompt to ensure it matches what users expect.

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 1 week:
- Query PostHog for `extension_installed` count (target: >= 20)
- Query Loops for contacts with tag `source: chrome-web-store-teaser` (target: >= 1)
- If PASS: proceed to Baseline Run
- If FAIL with > 10 installs but 0 leads: the extension popup is not compelling enough — rewrite copy, simplify form
- If FAIL with < 10 installs: keywords or listing copy are not reaching your ICP — research new keywords, rewrite title and description

## Time Estimate

- 1 hour: keyword research + listing copy + icon creation
- 1 hour: extension scaffolding + analytics instrumentation + landing page
- 30 minutes: packaging, upload, store listing completion
- 30 minutes: threshold evaluation after 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Chrome Web Store | Extension hosting and distribution | $5 one-time registration fee |
| PostHog | Extension event tracking (installs, popup opens, form submissions) | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Email capture and waitlist management | Free tier: 1,000 contacts, 4,000 emails/month ([loops.so/pricing](https://loops.so/pricing)) |
| Webflow | Landing page for extension traffic | Free tier available ([webflow.com/pricing](https://webflow.com/pricing)) |

**Estimated monthly cost at Smoke level: $0** (all tools within free tiers, plus $5 one-time CWS fee)

## Drills Referenced

- `chrome-extension-listing-setup` — scaffolds, instruments, and publishes the teaser extension
- `landing-page-pipeline` — builds the landing page that extension traffic lands on
- `threshold-engine` — evaluates install count and lead count against pass threshold
