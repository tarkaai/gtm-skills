---
name: micro-influencer-b2b-creators-smoke
description: >
  Micro-Influencer B2B Post — Smoke Test. Pay one B2B micro-influencer for a single sponsored
  post to test whether creator-led shoutouts produce any leads from their audience. One creator,
  one post, one week.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 1 lead from a single creator post in 1 week"
kpis: ["Clicks from creator UTM link", "Leads captured", "Cost per lead (CPL)", "Post engagement rate"]
slug: "micro-influencer-b2b-creators"
install: "npx gtm-skills add marketing/problem-aware/micro-influencer-b2b-creators"
drills:
  - creator-prospect-research
  - creator-outreach-pipeline
  - creator-campaign-execution
  - landing-page-pipeline
  - threshold-engine
---

# Micro-Influencer B2B Post — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Get at least 1 lead from a single paid creator post in 1 week. This proves that a B2B micro-influencer can drive ICP-matching traffic to your site and that their audience trusts their recommendations enough to take action. You are NOT trying to build a creator program or prove ROI at scale yet — you are testing whether creator-led content drives any signal at all.

## Leading Indicators

- Creator agrees to a deal and posts on schedule (confirms the outreach process works)
- UTM-tagged link gets 20+ clicks in the first 48 hours (confirms the creator's audience engages with sponsored content)
- Landing page conversion rate above 3% from creator traffic (confirms the traffic is relevant)
- Post engagement rate above 2% (confirms the creator's audience is active, not ghost followers)

## Instructions

### 1. Find and score 5-10 B2B creators

Run the `creator-prospect-research` drill at Smoke scale:
- Use SparkToro to find creators whose audience overlaps with your ICP
- Focus on micro-influencers: 1,000-50,000 followers
- Target one platform only (LinkedIn is typically best for B2B problem-aware content)
- Check Passionfroot for creators who already sell sponsorship slots (fastest path to a deal)
- Score and rank creators by audience fit, engagement quality, and cost

You need 5-10 prospects to book 1 post. Expect a 20-30% booking rate from outreach.

### 2. Outreach and book one creator

Run the `creator-outreach-pipeline` drill:
- Start with Passionfroot creators (book directly, no cold outreach needed)
- If no Passionfroot options, send personalized outreach to your top 3-5 prospects via email
- Negotiate a single post: LinkedIn post, newsletter mention, or tweet thread
- Budget: $200-500 for a micro-influencer post. Some creators with 5,000-15,000 followers charge $200-400.
- Close the deal with confirmed terms: format, date, price, tracking link

**Human action required:** Approve the final creator selection and budget before payment.

### 3. Build a landing page

Run the `landing-page-pipeline` drill:
- Build a dedicated page for this campaign (do NOT send creator traffic to your homepage)
- Headline should match the creator's content angle — if the creator is posting about "why manual data entry kills sales teams," the landing page should address that exact pain
- Include: problem-focused headline, 2-3 bullet points on your solution, single CTA (demo, trial, or content download), short form (name + email + company)
- Install PostHog tracking with UTM parameter capture

### 4. Brief the creator and execute

Run the `creator-campaign-execution` drill:
- Generate a structured brief: one primary message, one supporting proof point, the UTM-tagged landing page URL, and the FTC disclosure requirement
- Send the brief at least 5 days before the posting date
- Review the draft if offered (check for tracking link and disclosure)
- On posting day, confirm the post is live and the tracking link is correct

### 5. Measure for 7 days

After the post goes live:
- **Day 1:** Check PostHog for UTM-tagged page views. If zero clicks after 24 hours, verify the creator used the correct link.
- **Day 3:** Pull interim lead count. Check lead quality in Attio — are they ICP matches?
- **Day 7:** Pull final metrics. Calculate: total clicks, leads, conversion rate, CPL.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Compare results to: **1 or more leads from the creator post in 1 week**.

Also evaluate:
- **Lead quality:** Is the lead an ICP match? A non-ICP lead does not count.
- **Engagement signal:** Did the post get genuine comments or just likes? Comments indicate the audience took the content seriously.
- **CPL benchmark:** At Smoke, any CPL under $500 from a creator post is a positive signal. The goal is proof of concept, not efficiency.

**PASS (1+ ICP-matching lead):** Proceed to Baseline. Document: which creator, what format, what messaging angle worked.
**MARGINAL (clicks but no leads):** The creator drove traffic but the landing page did not convert. Test a different offer or page. Re-run smoke.
**FAIL (no clicks or no engagement):** Either the creator's audience is not a fit, or the sponsorship format did not work. Try a different creator or platform. Re-run smoke.

## Time Estimate

- 1 hour: Creator research and scoring
- 30 minutes: Outreach and booking (faster if using Passionfroot)
- 30 minutes: Landing page setup and tracking verification
- 15 minutes: Brief creation and delivery
- 5-7 days: Post goes live and runs (no active time)
- 45 minutes: Results collection, analysis, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| SparkToro | Audience research to find creators your ICP follows | Free: 5 searches/mo. Standard: $50/mo. [Pricing](https://sparktoro.com/pricing) |
| Passionfroot | B2B creator marketplace for direct booking | Free to browse. 2% fee on transactions. [Pricing](https://www.passionfroot.me/creator-pricing) |
| Clay | Creator enrichment and scoring | Launch: $185/mo (2,500 credits). [Pricing](https://www.clay.com/pricing) |
| Webflow | Landing page builder | Basic: $14/mo. [Pricing](https://webflow.com/pricing) |
| PostHog | UTM tracking, funnel analytics, lead attribution | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| Instantly | Cold outreach to creators | Growth: $30/mo. [Pricing](https://instantly.ai/pricing) |
| Attio | CRM for creator records and lead tracking | Free for up to 3 users. Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |

**Estimated smoke test cost:** $200-500 creator fee + $0-50 tooling = $200-550 total

## Drills Referenced

- `creator-prospect-research` — find, score, and shortlist B2B micro-influencers
- `creator-outreach-pipeline` — outreach to creators, negotiate, and close the sponsorship deal
- `creator-campaign-execution` — brief the creator, manage the post, capture results
- `landing-page-pipeline` — build a dedicated landing page for creator traffic
- `threshold-engine` — evaluate smoke test results against the pass threshold
