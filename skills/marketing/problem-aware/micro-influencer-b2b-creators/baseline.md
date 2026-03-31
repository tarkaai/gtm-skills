---
name: micro-influencer-b2b-creators-baseline
description: >
  Micro-Influencer B2B Post — Baseline Run. Run 3-5 creator sponsorships in parallel over
  2 weeks with always-on tracking. Prove that the creator channel produces leads consistently
  across multiple creators, not just one lucky post.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 3 leads from creator posts over 2 weeks"
kpis: ["Leads per creator post", "Average CPL across creators", "Creator booking rate", "Lead-to-ICP match rate"]
slug: "micro-influencer-b2b-creators"
install: "npx gtm-skills add marketing/problem-aware/micro-influencer-b2b-creators"
drills:
  - creator-outreach-pipeline
  - creator-campaign-execution
  - posthog-gtm-events
  - threshold-engine
---

# Micro-Influencer B2B Post — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Get at least 3 leads from creator posts over 2 weeks by running 3-5 creator sponsorships in parallel. This proves the micro-influencer channel works across multiple creators — not just a single lucky post. You are establishing that creator-led content is a repeatable lead source with a measurable CPL.

## Leading Indicators

- 3+ creators booked and briefed within the first 3 days (confirms the outreach pipeline scales)
- Each creator post generates 10+ UTM-tagged clicks (confirms audience engagement is not creator-specific)
- At least 2 different creators produce leads (confirms the channel works, not just one person)
- CPL stays below $300 per creator post (confirms unit economics are viable for scale)
- PostHog tracking captures complete funnel data for every creator (confirms measurement infrastructure works)

## Instructions

### 1. Expand the creator pipeline

Using the scored creator list from your Smoke test, run `creator-outreach-pipeline` at Baseline volume:
- Outreach to 10-15 creators to book 3-5 posts
- Diversify: book creators on at least 2 different platforms or formats (e.g., 2 LinkedIn posts + 1 newsletter mention + 1 Twitter thread)
- Reuse the same landing page from Smoke if it converted well; build a variant if conversion was below 3%
- Stagger posting dates across the 2 weeks so you can react to early results

**Budget allocation:** $1,000-2,500 total across 3-5 creators. Average $200-500 per post.

### 2. Set up end-to-end tracking

Run the `posthog-gtm-events` drill to configure a complete tracking pipeline:
- Event: `influencer_page_view` — fires on landing page load with UTM params
- Event: `influencer_lead_captured` — fires on form submission with `creator_handle`, `campaign`, `post_format`
- Event: `influencer_meeting_booked` — fires when a lead from creator traffic books a meeting (connect Cal.com webhook to PostHog via n8n)
- Funnel: `influencer_page_view` → `influencer_lead_captured` → `influencer_meeting_booked`, broken down by `creator_handle`

This gives you per-creator attribution at every stage of the funnel.

### 3. Execute campaigns in parallel

Run `creator-campaign-execution` for each booked creator:
- Generate a unique UTM link per creator (same landing page, different `utm_source`)
- Send briefs to all creators with their specific tracking links
- Review drafts from each creator (recommended at Baseline to calibrate quality)
- Track posting dates and confirm each post goes live on schedule

### 4. Monitor weekly

**Week 1 checkpoint:**
- How many creators have posted? If fewer than 2, follow up with late creators.
- Pull interim results: clicks and leads per creator from PostHog
- Are any creators driving significantly more traffic? Note which formats and messaging angles are performing.
- If a creator's post got zero clicks after 48 hours, investigate: wrong link? Post not actually published? Low engagement?

**Week 2:**
- Remaining creators post
- Pull cumulative metrics
- Start building the performance comparison across creators

### 5. Build the creator performance report

Run the `creator-performance-reporting` drill:
- Create the PostHog dashboard: campaign overview, creator comparison, format analysis
- Build Attio scorecard views: creator performance, active campaigns, pipeline
- Calculate per-creator CPL, CPC, conversion rate, and engagement quality score
- Rank creators by CPL — this ranking informs which creators to rebook at Scalable

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Compare results to: **3 or more leads from creator posts over 2 weeks**.

Deep analysis:
- **Per-creator performance:** Which creators drove leads? Which drove clicks but no conversions? Which drove nothing?
- **Format comparison:** Did LinkedIn posts outperform newsletters? Did any format surprise you?
- **Audience quality:** What percentage of leads are ICP matches? If less than 50%, tighten creator selection criteria.
- **CPL benchmark:** At Baseline, target CPL under $300. Compare to your other channels — is creator-led content competitive?

**PASS (3+ leads, at least 2 creators producing results):** Proceed to Scalable. Document: which creators and formats to scale, which to drop.
**MARGINAL (3+ leads but all from 1 creator):** You found a good creator, not a good channel. Try different creators to confirm it is not creator-dependent. Re-run Baseline with fresh creators.
**FAIL (<3 leads across all creators):** Diagnose: if clicks are high but conversions are low, the landing page or offer needs work. If clicks are low, the creators are not the right fit or the content angle is wrong. Iterate and re-run.

## Time Estimate

- 2 hours: Expand outreach, negotiate and book 3-5 creators
- 1 hour: Set up PostHog tracking pipeline
- 1 hour: Generate briefs and send to all creators
- 2 weeks: Posts go live on staggered schedule (minimal active time between posts)
- 3 hours: Monitor weekly, collect metrics, review drafts
- 2 hours: Build performance report and run threshold evaluation
- 1 hour: Analysis, documentation, and Scalable planning

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| SparkToro | Audience research for creator discovery | Standard: $50/mo. [Pricing](https://sparktoro.com/pricing) |
| Passionfroot | Book creators with transparent pricing | 2% transaction fee. [Pricing](https://www.passionfroot.me/creator-pricing) |
| Clay | Creator enrichment and scoring | Launch: $185/mo. [Pricing](https://www.clay.com/pricing) |
| Instantly | Cold outreach to creators without Passionfroot | Growth: $30/mo. [Pricing](https://instantly.ai/pricing) |
| PostHog | Full-funnel creator attribution tracking | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| Attio | Creator CRM and lead management | Free for up to 3 users. Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |
| Webflow | Landing page | Basic: $14/mo. [Pricing](https://webflow.com/pricing) |
| n8n | Webhook routing for Cal.com to PostHog | Community (self-hosted): free. Cloud Starter: $24/mo. [Pricing](https://n8n.io/pricing) |

**Estimated Baseline cost:** $1,000-2,500 creator fees + ~$100-300 tooling/mo = $1,100-2,800 total

## Drills Referenced

- `creator-outreach-pipeline` — outreach to 10-15 creators, book 3-5 deals
- `creator-campaign-execution` — brief, manage, and track each creator post
- `posthog-gtm-events` — configure end-to-end tracking with per-creator attribution
- `threshold-engine` — evaluate Baseline results against pass threshold
