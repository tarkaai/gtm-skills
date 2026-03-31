---
name: chrome-web-store-teaser-baseline
description: >
  Chrome Extension Teaser — Baseline Run. First always-on automation: instrument full-funnel
  tracking, automate lead routing from extension installs, and validate that installs and leads
  sustain over 2 weeks without manual intervention.
stage: "Marketing > Unaware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=50 installs and >=3 leads over 2 weeks"
kpis: ["Store listing views", "Install rate", "Popup open rate", "Waitlist signups", "Install-to-lead conversion rate"]
slug: "chrome-web-store-teaser"
install: "npx gtm-skills add marketing/unaware/chrome-web-store-teaser"
drills:
  - posthog-gtm-events
  - chrome-extension-listing-setup
  - landing-page-pipeline
  - threshold-engine
---

# Chrome Extension Teaser — Baseline Run

> **Stage:** Marketing > Unaware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Prove that Chrome Web Store installs and leads sustain over 2 weeks with automated tracking and lead routing. The Smoke Test proved signal exists; Baseline proves the signal holds over time and that leads flow into your CRM without manual effort. Pass threshold: >= 50 installs and >= 3 leads over 2 weeks.

## Leading Indicators

- Daily install rate holds steady or grows week-over-week (no decay after initial burst)
- Popup engagement rate (popup opens / installs) stays above 15%
- At least 1 lead per week (confirms consistent conversion, not a one-time spike)
- Landing page receives traffic from the extension popup link

## Instructions

### 1. Configure full-funnel PostHog tracking

Run the `posthog-gtm-events` drill to establish the event taxonomy for this play:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `cws_listing_impression` | Daily scrape of CWS Developer Dashboard stats | `date`, `keyword_source` |
| `extension_installed` | `chrome.runtime.onInstalled` | `install_reason`, `version` |
| `popup_opened` | Popup HTML load | `page`, `session_number` |
| `feature_preview_clicked` | Click on feature bullet in popup | `feature_name` |
| `waitlist_form_submitted` | Form submission in popup | `email_domain` |
| `landing_page_viewed` | Page view on extension landing page | `utm_source`, `utm_medium`, `referrer` |
| `extension_uninstalled` | Uninstall survey page view | `days_since_install`, `reason` |

Build a PostHog funnel: `extension_installed` > `popup_opened` > `waitlist_form_submitted`. This is your core conversion funnel.

### 2. Update the extension with improved tracking

Using the `chrome-extension-listing-setup` drill, update the extension:
- Add `feature_preview_clicked` tracking for each feature bullet in the popup
- Add session counting (increment a counter in `chrome.storage.local` on each popup open)
- Improve the uninstall survey page: add 4-5 multiple-choice reasons and a free-text field
- Increment the version in `manifest.json` and publish the update via Chrome Web Store API

### 3. Automate lead routing

Build an n8n workflow that runs on a schedule (every 15 minutes):
1. Query the Loops API for new contacts tagged `source: chrome-web-store-teaser` since last check
2. For each new contact, create or update a record in Attio with:
   - Source: `chrome-web-store`
   - Channel: `extension-waitlist`
   - First seen: contact creation timestamp
3. Send a Loops transactional email: "Thanks for joining the waitlist" with a link to book a call or try the product
4. Log the lead creation as a PostHog event: `lead_created` with `source: chrome-web-store-teaser`

### 4. Optimize the landing page

Run the `landing-page-pipeline` drill to refine the extension landing page based on Smoke data:
- Add UTM parameters to all links from the extension popup: `?utm_source=chrome-extension&utm_medium=popup&utm_campaign=teaser`
- Track scroll depth and form engagement on the landing page via PostHog
- If popup-to-landing-page click rate is below 10%, add a stronger CTA in the popup linking to the page

### 5. Improve listing based on Smoke data

Using the Chrome Web Store Developer Dashboard:
- Check which search terms drove impressions and clicks
- If CTR (listing visits / impressions) is below 5%, rewrite the title and short description to better match search intent
- If install rate (installs / listing visits) is below 10%, improve screenshots and detailed description
- Respond to any user reviews (even if just one)

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 2 weeks:
- Query PostHog: `extension_installed` count in last 14 days (target: >= 50)
- Query Loops: contacts with tag `source: chrome-web-store-teaser` created in last 14 days (target: >= 3)
- Calculate conversion rates: listing-to-install, install-to-popup, popup-to-lead
- If PASS: proceed to Scalable. Document which keywords and listing elements drove the most installs.
- If FAIL with >= 30 installs but < 3 leads: popup conversion is the bottleneck — rewrite popup copy, simplify form, add stronger value prop
- If FAIL with < 30 installs: listing discovery is the bottleneck — research new keywords, update title and screenshots

## Time Estimate

- 3 hours: PostHog event taxonomy setup + funnel configuration
- 3 hours: Extension update (tracking improvements, uninstall survey, version bump)
- 2 hours: n8n lead routing workflow
- 2 hours: Landing page optimization + UTM setup
- 1 hour: Listing copy optimization based on Smoke data
- 1 hour: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Chrome Web Store | Extension hosting and distribution | $5 one-time (already paid at Smoke) |
| PostHog | Full-funnel event tracking and funnels | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Lead capture, tagging, transactional emails | Free tier: 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Lead routing automation (Loops > Attio) | Self-hosted free; Cloud Starter: $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM — store and track extension leads | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |
| Webflow | Extension landing page | Free tier available ([webflow.com/pricing](https://webflow.com/pricing)) |

**Estimated monthly cost at Baseline level: $0-24/mo** (n8n Cloud if not self-hosting; all other tools within free tiers)

## Drills Referenced

- `posthog-gtm-events` — establishes the event taxonomy and funnels for CWS tracking
- `chrome-extension-listing-setup` — updates the extension with improved tracking
- `landing-page-pipeline` — optimizes the landing page based on Smoke data
- `threshold-engine` — evaluates install and lead counts against pass threshold
