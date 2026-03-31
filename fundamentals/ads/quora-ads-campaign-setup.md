---
name: quora-ads-campaign-setup
description: Create and configure Quora Ads campaigns, ad sets, and ads via Quora Ads Manager and Conversion API
tool: Quora
product: Quora Ads
difficulty: Setup
---

# Quora Ads — Campaign Setup

Create and manage Quora advertising campaigns. Quora does not expose a full public campaign-management API (unlike Google/Meta/Reddit). Campaign creation and configuration happen through the Quora Ads Manager UI or via API partners (AdStage, Supermetrics, Improvado). The Conversion API (CAPI) handles server-side conversion tracking.

## Authentication

### Ads Manager (UI-based campaign management)

1. Create a Quora for Business account at https://www.quora.com/business
2. Access Ads Manager at https://www.quora.com/ads/
3. Configure billing (credit card required)

### Conversion API (server-side tracking)

1. In Ads Manager, navigate to the **Pixel & Events** tab
2. Click **Generate Token** under the Conversion API section
3. Store the API access token securely — each token is scoped to one ad account

## Campaign Hierarchy

Quora Ads follows: **Campaign -> Ad Set -> Ad**

- **Campaign**: Objective, budget (daily or lifetime), schedule
- **Ad Set**: Targeting (topic, question, keyword, audience), bid type, bid amount, placement
- **Ad**: Creative (headline, body, image, CTA, destination URL)

## Campaign Objectives

Select one objective per campaign:

| Objective | Use Case | Bidding |
|-----------|----------|---------|
| Conversions | Drive form submissions, signups, demos | CPC or Conversion Optimized |
| Traffic | Drive website visits | CPC |
| Awareness | Maximize impressions | CPM |
| Video Views | Promote video content | CPV |
| Lead Generation | Collect leads via Quora Lead Gen Forms | CPC or Conversion Optimized |
| App Installs | Drive mobile app downloads | CPC |

For B2B SaaS problem-aware targeting, use **Conversions** with CPC bidding.

## Create a Campaign (Ads Manager)

**Human action required:** In Quora Ads Manager:

1. Click **Create Campaign**
2. Select campaign objective: **Conversions**
3. Name the campaign: `quora-ads-targeting-{level}-{date}` (e.g., `quora-ads-targeting-smoke-2026-04`)
4. Set budget:
   - Daily budget: set in dollars (minimum $5/day; recommended $30-50/day for Smoke)
   - Lifetime budget: alternative to daily; total spend capped
5. Set schedule: start and end dates
6. Save and proceed to Ad Set configuration

## Create an Ad Set

Within the campaign:

1. Name the ad set: `adset-{targeting-type}-{descriptor}` (e.g., `adset-topic-devops-tools`)
2. Select targeting type (see `quora-ads-question-targeting` fundamental for details):
   - **Topic Targeting**: select from Quora's topic taxonomy
   - **Question Targeting**: target specific question pages
   - **Keyword Targeting**: target questions containing keywords
   - **Audience Targeting**: website visitors, list match, or lookalike
3. Set geographic targeting (default: US, UK, CA, AU for B2B SaaS)
4. Set device targeting (All Devices recommended)
5. Set bid:
   - CPC bidding: start at $1.00-2.00 for B2B topics (adjust after 3 days of data)
   - CPM bidding: start at $3.00-5.00
   - Conversion Optimized: let Quora optimize for conversions (requires pixel + conversion data)
6. Disable **Audience Expansion** to maintain targeting precision
7. Save ad set

## Create an Ad

Within the ad set:

1. Ad format: **Image Ad** (most common) or **Text Ad**
2. Business name: your company name
3. Headline: max 65 characters (benefit-driven, question-aware framing)
4. Body text: max 105 characters (supporting value proposition)
5. CTA button: `Learn More`, `Sign Up`, `Download`, `Get Quote`, `Contact Us`
6. Destination URL: landing page with UTM parameters:
   ```
   https://yoursite.com/quora-lp?utm_source=quora&utm_medium=paid&utm_campaign=quora-ads-targeting&utm_content={ad-variant-id}
   ```
7. Image: 600x315px minimum (recommended 1200x628px), PNG or JPG, max 2MB
8. Save ad in **Paused** status for review before launch

## Bulk Campaign Management via n8n

For agents without direct UI access, use n8n HTTP Request nodes to interact with Quora via:

1. **Supermetrics** or **Improvado** connectors for pulling reporting data
2. **Quora Conversion API** for sending conversion events server-side (see `quora-ads-conversion-tracking`)
3. **Zapier/n8n Quora triggers** (limited to conversion event forwarding)

Campaign creation itself requires Ads Manager UI. The agent should prepare campaign specifications (targeting, budget, creative, UTMs) and present them for human execution.

## Error Handling

- **Ad rejected**: Quora reviews all ads (24-48 hour turnaround). Common rejections: misleading claims, landing page mismatch, prohibited content. Check the Ads Manager dashboard for rejection reasons.
- **Low delivery**: If an ad set spends less than 50% of daily budget, broaden targeting or increase bid.
- **Pixel not firing**: Verify pixel installation using the Quora Pixel Helper browser extension.

## n8n Workflow Template

```
Trigger: Manual or scheduled
Step 1: Generate campaign spec (name, objective, budget, schedule)
Step 2: Generate ad set specs (targeting, bid, geo)
Step 3: Generate ad creative specs (headline, body, CTA, image URL, destination URL with UTMs)
Step 4: Output a structured JSON campaign brief for human execution in Ads Manager
Step 5: After human launches, receive webhook from PostHog confirming pixel fires on landing page
```
