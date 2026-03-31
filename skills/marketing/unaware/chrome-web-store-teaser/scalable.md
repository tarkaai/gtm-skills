---
name: chrome-web-store-teaser-scalable
description: >
  Chrome Extension Teaser — Scalable Automation. Find the 10x multiplier: A/B test listing
  elements, automate Chrome Web Store ASO, expand to related extension categories, and build
  automated review management to drive 200+ installs and 15+ leads in 2 months.
stage: "Marketing > Unaware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=200 installs and >=15 leads over 2 months"
kpis: ["Store listing views", "Install rate", "Popup open rate", "Waitlist signups", "Install-to-lead conversion rate", "CWS search ranking position"]
slug: "chrome-web-store-teaser"
install: "npx gtm-skills add marketing/unaware/chrome-web-store-teaser"
drills:
  - chrome-store-aso
  - ab-test-orchestrator
  - tool-sync-workflow
  - threshold-engine
---

# Chrome Extension Teaser — Scalable Automation

> **Stage:** Marketing > Unaware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Scale install volume 4x and lead volume 5x over Baseline by systematically optimizing the Chrome Web Store listing, testing popup variations, and automating review and competitor monitoring. The 10x multiplier comes from: better keywords driving more impressions, optimized listing copy converting more visitors to installs, and improved popup UX converting more installs to leads. Pass threshold: >= 200 installs and >= 15 leads over 2 months.

## Leading Indicators

- CWS listing impressions growing week-over-week (confirms keyword optimization is working)
- Install rate (installs / listing visits) improving from Baseline level
- Popup-to-lead conversion rate above 8% (up from Baseline baseline)
- At least 2 user reviews received (confirms engaged user base)
- Search ranking for primary keywords in top 10 results

## Instructions

### 1. Run Chrome Web Store ASO

Run the `chrome-store-aso` drill to systematically optimize the listing:

**Keyword optimization (Week 1-2):**
- Research 15+ candidate search terms using the CWS search and Google Trends
- Identify the 3 primary and 5 secondary keywords with the best relevance-to-competition ratio
- Rewrite the extension title, short description, and detailed description to target these keywords
- Publish the update and measure 2-week CTR and install rate change

**Screenshot optimization (Week 3-4):**
- Create 5 professional screenshots (1280x800) with annotations showing the extension in action
- Test two different hero screenshots (the first screenshot shown in search results) by swapping every 2 weeks
- Measure install rate change for each hero screenshot variant

**Review management:**
- Set up automated review monitoring via n8n (check daily for new reviews)
- Respond to every review within 24 hours
- For positive reviews, reply with thanks and a specific mention of what they liked
- For negative reviews, acknowledge the issue, state the fix timeline, and ask for updated review after resolution

### 2. A/B test popup variations

Run the `ab-test-orchestrator` drill to test extension popup elements:

**Test 1 (Week 1-2): Value proposition copy**
- Control: current popup headline and description
- Variant: rewritten copy emphasizing a different pain point or benefit
- Metric: `waitlist_form_submitted` rate per `popup_opened`
- Implement via PostHog feature flag in the popup (fetch flag on popup load, render variant)

**Test 2 (Week 3-4): Form design**
- Control: email-only form
- Variant A: email + company name (higher quality leads, potentially lower conversion)
- Variant B: email with "What problem are you trying to solve?" dropdown (qualifies leads)
- Metric: form submission rate and downstream lead quality (do they book calls?)

**Test 3 (Week 5-6): CTA copy and urgency**
- Control: "Get Early Access"
- Variant: "Join 50+ teams on the waitlist" (social proof) or "Limited beta spots" (scarcity)
- Metric: form submission rate

### 3. Automate listing and lead management

Run the `tool-sync-workflow` drill to build n8n workflows:

**Workflow 1: Competitor monitor (weekly)**
1. Scrape CWS search results for your 3 primary keywords
2. Record top 10 extensions for each keyword (name, install count, rating, last updated)
3. Compare against previous week's data
4. Alert if a new competitor appears in top 5 or an existing competitor updates their listing
5. Log competitive data in Attio

**Workflow 2: Install milestone alerts (daily)**
1. Query PostHog for cumulative `extension_installed` count
2. When milestones hit (50, 100, 200, 500), send a Slack notification
3. Log milestone events in Attio

**Workflow 3: Lead quality scoring (on each new lead)**
1. When a new contact is created in Loops with CWS source tag
2. Enrich the email domain: company size, industry, technology stack (via Clay if available)
3. Score the lead: ICP match (high/medium/low)
4. Route high-quality leads to a priority Attio list for immediate follow-up
5. Route others to the standard nurture sequence in Loops

### 4. Expand extension functionality

Based on which feature previews get the most clicks (tracked via `feature_preview_clicked` events), build 1-2 lightweight features into the extension:
- Choose the feature with the highest click rate in the popup
- Implement a minimal working version
- This converts the extension from "teaser" to "tool with a teaser" — users get immediate value, increasing retention and word-of-mouth

**Human action required:** Decide which feature to implement based on click data and engineering effort required. Build and test the feature.

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 2 months:
- Query PostHog: `extension_installed` count in last 60 days (target: >= 200)
- Query Loops: contacts with tag `source: chrome-web-store-teaser` created in last 60 days (target: >= 15)
- Review A/B test results: which variants won and their impact on conversion
- Document: best-performing keywords, optimal listing elements, popup variant winners
- If PASS: proceed to Durable. Lock in the winning listing configuration and popup variant.
- If FAIL with >= 100 installs but < 15 leads: popup conversion is the constraint — continue testing popup variations
- If FAIL with < 100 installs: listing discovery is the constraint — test new categories, expand keyword targeting, consider cross-promoting the extension from other channels (blog posts, social media)

## Time Estimate

- 15 hours: Chrome Store ASO (keyword research, listing rewrites, screenshot creation, review management setup)
- 15 hours: A/B test setup and analysis (3 tests over 6 weeks)
- 15 hours: n8n automation workflows (competitor monitor, milestone alerts, lead scoring)
- 10 hours: Extension feature development (1-2 lightweight features)
- 5 hours: Ongoing monitoring, threshold evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Chrome Web Store | Extension hosting and distribution | $5 one-time (already paid) |
| PostHog | Event tracking, funnels, feature flags, A/B tests | Free tier: 1M events + 1M feature flag requests/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Lead capture and nurture sequences | Free < 1,000 contacts; Starter $49/mo if over ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automation: competitor monitoring, lead routing, alerts | Self-hosted free; Cloud Starter $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM for lead tracking and competitive intel | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Lead enrichment and scoring | Explorer $149/mo for enrichment credits ([clay.com/pricing](https://www.clay.com/pricing)) |

**Estimated monthly cost at Scalable level: $75-225/mo** (n8n Cloud + Loops Starter if over 1K contacts + Clay Explorer if enriching leads)

## Drills Referenced

- `chrome-store-aso` — keyword research, listing copy optimization, screenshot testing, review management
- `ab-test-orchestrator` — popup A/B tests (copy, form design, CTAs)
- `tool-sync-workflow` — competitor monitoring, install milestone alerts, lead quality scoring automations
- `threshold-engine` — evaluates cumulative installs and leads against pass threshold
