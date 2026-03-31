---
name: partner-newsletter-swaps-baseline
description: >
  Partner Newsletter Swaps — Baseline Run. Run always-on swap operations across 5-8 partners
  with structured tracking, proving repeatable subscriber growth and lead generation from
  list swaps over a 6-week period.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Email"
level: "Baseline Run"
time: "20 hours over 6 weeks"
outcome: ">=6 completed swaps across >=3 partners, >=300 new subscribers, >=10 leads in 6 weeks"
kpis: ["Swaps completed per week", "Subscribers per swap", "Click-to-lead conversion rate", "Reciprocal balance ratio", "Partner retention rate"]
slug: "partner-newsletter-swaps"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/partner-newsletter-swaps"
drills:
  - posthog-gtm-events
  - warm-intro-request
---
# Partner Newsletter Swaps — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Email

## Outcomes
- Complete >=6 list swaps across >=3 distinct partners in 6 weeks
- Acquire >=300 new subscribers from swap traffic
- Generate >=10 leads (meetings or signups) from swap-sourced visitors
- Prove that swap results hold across multiple partners and over time (not a one-off spike)

## Leading Indicators
- >=5 active partners in the Attio partnership pipeline with confirmed swap dates
- Average subscriber gain per swap trending >=50
- Click-to-lead conversion rate stable at >=1.5% across swaps
- No partner drops out after first swap (retention signal)
- Reciprocal balance ratio within 2:1 (clicks received vs. clicks given per partner)

## Instructions

### 1. Configure swap event tracking

Run the `posthog-gtm-events` drill to set up structured event tracking for the swap program. Define and verify these events fire correctly in PostHog:

- `list_swap_email_sent` — fires when you confirm a swap email was sent (properties: `partner_slug`, `direction` [inbound/outbound], `variant_id`, `send_date`)
- `list_swap_page_visit` — fires on `pageview` where `utm_medium = list-swap` (properties: `partner_slug`, `variant_id`)
- `list_swap_cta_click` — fires when a swap visitor takes the primary CTA (properties: `partner_slug`, `cta_type`)
- `list_swap_lead_created` — fires when a swap visitor books a meeting or signs up (properties: `partner_slug`, `lead_type`)
- `list_swap_subscriber_added` — fires when a new subscriber is attributed to a swap source (properties: `partner_slug`)

Verify each event fires with a test UTM URL before running live swaps.

### 2. Expand the partner portfolio using warm intros

Run the `warm-intro-request` drill to reach 5-8 active swap partners. For each target partner from your Smoke-level research:
1. Identify mutual connections in your Attio network who know the partner contact
2. Draft a warm intro request explaining the swap opportunity and your Smoke results (share actual numbers: "Our first swap with [Partner X] generated 65 subscribers and 3 leads")
3. Track intro requests in Attio: request sent, intro made, conversation started, swap agreed
4. For partners with no warm path, fall back to cold outreach referencing your Smoke results as proof

Target: >=5 partners with confirmed first-swap dates within 3 weeks.

### 3. Build the swap scheduling system

Run the the list swap scheduling workflow (see instructions below) drill to automate coordination across your portfolio. This drill builds n8n workflows that:
1. **Swap calendar workflow** (weekly cron, Monday 9am): queries Attio for partners with swaps due in the next 14 days, checks email copy status ("Our Email Status": draft/approved/sent-to-partner/confirmed-sent), alerts you when copy is needed
2. **Reciprocal send automation**: when you approve a partner's email, n8n auto-creates a Loops broadcast with their content targeted to the agreed segment, schedules it for the swap date
3. **Confirmation workflow** (daily cron on swap days): verifies both sides sent, marks completed swaps in Attio, sets the next swap date per cadence agreement, flags delinquent partners
4. **Cadence management**: assigns each partner a tier (monthly, bimonthly, quarterly), enforces max 3 inbound swaps to your list per week to protect engagement

**Human action required:** Approve each swap email before it goes to the partner. Approve each partner's email before it goes to your list. The automation handles scheduling and tracking; you own quality control.

### 4. Execute swaps on a rolling basis

With the scheduling system running, execute 1-2 swaps per week over 6 weeks:
- Run `list-swap-email-copy` drill for each new swap (reuse proven variants where partner audience is similar)
- Alternate email variants across partners to build performance data on which angles work
- Log every swap outcome in Attio: clicks received, clicks given, leads generated, subscriber adds
- After each swap, update the partner's performance metrics: total swaps, total clicks, click-to-lead rate, reciprocal balance

### 5. Analyze per-partner performance

After 6 weeks, pull swap data from PostHog and Attio to identify:
- **Top partners:** Highest click-to-lead conversion rate. These become monthly-cadence partners.
- **Volume partners:** High clicks but low conversion. Test different email variants or landing pages.
- **Low performers:** <20 clicks per swap. Investigate audience fit. Deprioritize or pause.
- **Reciprocity imbalance:** Partners where net value is >3:1 in either direction. Renegotiate terms or adjust send segments.

### 6. Evaluate against threshold

Measure against pass criteria:
- **>=6 completed swaps:** Both emails sent, results tracked, across the 6-week period
- **>=3 distinct partners:** Not just repeat swaps with one partner
- **>=300 new subscribers:** Attributed to `list_swap_subscriber_added` events
- **>=10 leads:** Attributed to `list_swap_lead_created` events

If PASS: The swap program generates repeatable results across multiple partners. Proceed to Scalable to automate the partner pipeline and scale to 20+ partners.

If FAIL: Analyze which partners and variants drove the most value. Consolidate to the top 3 partners, test new email angles, and re-run for another 4 weeks before deciding.

---

## Time Estimate
- Event tracking setup: 3 hours
- Partner outreach via warm intros: 4 hours
- Swap scheduling system build: 4 hours
- Email writing and coordination (6+ swaps): 6 hours
- Monitoring and analysis: 3 hours

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking and swap attribution | Free tier: 1M events/mo (https://posthog.com/pricing) |
| n8n | Swap scheduling and coordination automation | Free self-hosted. Cloud: $24/mo (https://n8n.io/pricing) |
| Attio | Partner CRM and swap tracking | Free tier: 3 users. Plus: $34/user/mo (https://attio.com/pricing) |
| Loops | Reciprocal email sends to your list | Starter: $49/mo for 5K contacts (https://loops.so/pricing) |
| Clay | Partner enrichment for new prospects | Pro: $149/mo (https://www.clay.com/pricing) |

**Estimated play-specific cost:** ~$50-100/mo (n8n cloud + Loops if beyond free tier)

## Drills Referenced
- the list swap scheduling workflow (see instructions below) — automate swap coordination, reciprocal sends, confirmation, and cadence management
- `posthog-gtm-events` — define and verify all swap tracking events in PostHog
- `warm-intro-request` — leverage mutual connections to reach partner contacts
