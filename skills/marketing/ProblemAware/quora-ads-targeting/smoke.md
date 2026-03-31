---
name: quora-ads-targeting-smoke
description: >
  Quora Ads — Smoke Test. Run answer-based ads on Quora targeting specific questions and topics
  where problem-aware prospects are actively researching solutions. Validate that Quora delivers
  qualified traffic at a competitive CPC with a $200-500 test budget.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Communities"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=5,000 impressions, >=50 clicks, >=3 qualified leads from $200-500 Quora test budget within 1 week"
kpis: ["Impressions", "Clicks", "CTR", "CPC", "Landing page conversion rate", "Qualified leads"]
slug: "quora-ads-targeting"
install: "npx gtm-skills add Marketing/ProblemAware/quora-ads-targeting"
drills:
  - threshold-engine
---

# Quora Ads — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Communities

## Outcomes

Prove that Quora Ads can reach problem-aware prospects at a cost-effective CPC by placing ads on question pages where your ICP is actively researching problems your product solves. At this level, the agent assists with question/topic research, creative generation, and landing page setup. Campaign creation in Quora Ads Manager is manual. No automation, no always-on spend. This is a single-flight test to validate the channel.

**Pass threshold:** >=5,000 impressions, >=50 clicks, >=3 qualified leads from $200-500 Quora test budget within 1 week.

## Leading Indicators

- CTR exceeds 0.8% (vs 0.5% benchmark for Quora B2B ads)
- CPC is below $3.00 (vs $1.50-4.00 typical range for B2B on Quora)
- Landing page conversion rate exceeds 3% (form submits / page views)
- At least 1 lead matches ICP criteria (right job title, company size, industry) when enriched via Clay
- Comments or upvotes on Quora questions in your target topics indicate active community engagement
- Quora Pixel fires correctly and CAPI events match PostHog events

## Instructions

### 1. Research Target Questions and Topics

Run the the quora ads campaign build workflow (see instructions below) drill, starting with the research phase:

1. List 5 pain points your ICP has that your product addresses
2. Search Quora for each pain point. Identify:
   - 10-15 Tier 1 topics (directly related to the problem)
   - 30-50 high-traffic questions (500+ monthly views each)
3. Group findings into 2 targeting clusters:
   - **Cluster A — Topic targeting**: 10-15 core problem topics
   - **Cluster B — Question targeting**: 30-50 specific high-intent questions
4. Document the research in a structured targeting spec

For the Smoke test, the agent performs the Quora search and question scoring. Manual browsing of Quora Ads Manager topic suggestions is acceptable — you do not need a third-party research tool.

### 2. Build the Landing Page

Continue the the quora ads campaign build workflow (see instructions below) drill — landing page phase:

1. Create a dedicated landing page for this Quora campaign
2. Headline matches the ad promise (e.g., "The 5-Step Framework for [Solving ICP Problem]")
3. Offer delivers immediate value: free guide, checklist, template, or tool (no demo-gate for Smoke)
4. Form: email only (minimize friction for first test)
5. Install Quora Pixel base code and `ViewContent` event on page load
6. Install qclid capture script (stores Quora click ID for CAPI matching)
7. Install PostHog tracking: page view, scroll depth, form submit events
8. No navigation links — single CTA

**Human action required:** Review the landing page for messaging accuracy and brand consistency.

### 3. Create Campaign and Ads

Continue the the quora ads campaign build workflow (see instructions below) drill — campaign creation phase:

1. The agent generates a campaign brief with:
   - Campaign: objective `Conversions`, daily budget $30-75/day, 7-day run
   - Ad Set 1 — Topic Targeting: 10-15 core topics, CPC bid $1.50
   - Ad Set 2 — Question Targeting: 30-50 questions, CPC bid $1.00
   - 3 ad variants per ad set (data hook, question hook, outcome hook)
   - Both Image Ad and Text Ad formats for each variant
   - All destination URLs with UTM parameters
2. The agent outputs image assets (1200x628px) for Image Ad variants

**Human action required:** Create the campaign in Quora Ads Manager following the agent's brief. Set all ads to Paused. Review, then activate. Note: Quora manually reviews ads (24-48 hour approval).

### 4. Configure Conversion Tracking

Complete the the quora ads campaign build workflow (see instructions below) drill — tracking phase:

1. Verify Quora Pixel fires on landing page (use Quora Pixel Helper extension)
2. Verify qclid capture stores the click ID on landing page load
3. Set up CAPI via n8n: on PostHog `quora_ads_lead_captured` webhook, forward the event to Quora's Conversion API with the stored qclid and hashed email
4. Verify PostHog receives `quora_ads_page_view` and `quora_ads_lead_captured` events
5. Send a test CAPI event and confirm it appears in Ads Manager Event Testing

### 5. Monitor for 7 Days

Check Quora Ads Manager and PostHog daily for 7 days. Track:

- Per-ad-set metrics: impressions, clicks, CTR, CPC, spend
- Per-variant metrics: CTR and click volume (which hook type performs best)
- Landing page metrics in PostHog: page views, scroll depth, form submits, conversion rate
- Quora Pixel event count vs PostHog event count (should match within 5%)

After 3 days: if any ad set has spent less than 20% of its budget, the targeting may be too narrow. Broaden topics or add more questions. If any ad variant has CTR below 0.3%, pause it and note the hook type that underperformed.

Do not optimize aggressively mid-flight. The purpose of Smoke is to collect data, not to optimize. Make only critical fixes (broken tracking, rejected ads, zero delivery).

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 7 days, pull final metrics from Quora Ads Manager and PostHog
2. Calculate:
   - Total impressions (threshold: >=5,000)
   - Total clicks (threshold: >=50)
   - Average CTR (benchmark: >=0.8%)
   - Average CPC (benchmark: <=$3.00)
   - Total qualified leads (threshold: >=3, where qualified = ICP match confirmed by Clay enrichment)
   - Landing page conversion rate (benchmark: >=3%)
   - Cost per qualified lead
3. Compare topic targeting ad set vs question targeting ad set: which delivered better CPA?
4. Compare hook types across variants: which generated highest CTR?

**If PASS:** Quora delivers qualified traffic at a viable cost. Proceed to Baseline with increased budget, retargeting, and proper lead routing.

**If FAIL:** Diagnose:
- Low impressions (<5,000): targeting too narrow. Broaden topics, add more questions, or increase bid.
- Low CTR (<0.5%): creative not resonating with Quora audience. Test different pain points or switch from Image Ads to Text Ads (which blend better on Quora).
- Low conversion rate (<2%): landing page is the bottleneck. Check message match between ad and page. Simplify the form. Test a different offer.
- Low lead quality: targeting is reaching the wrong audience. Review which topics/questions drove clicks and refine toward higher-intent contexts.

## Time Estimate

- 2 hours: Question and topic research
- 1.5 hours: Landing page build and tracking installation
- 1.5 hours: Campaign brief generation and creative production
- 1 hour: Campaign creation in Ads Manager (human) + tracking verification
- 1.5 hours: Daily monitoring over 7 days (~15 min/day)
- 0.5 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Quora Ads | Campaign management and ad delivery | No platform fee; ad spend only ($200-500 for Smoke) |
| PostHog | Analytics — funnel tracking, conversion attribution | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — log leads and campaign results | Free (up to 3 users) or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Webflow | Landing page builder | Free (1 site) or $18/mo (Basic) — [webflow.com/pricing](https://webflow.com/pricing) |
| Clay | Lead enrichment and ICP scoring | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Automation — CAPI integration | Free (self-hosted) or $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost this level:** $200-500 ad spend + $0 incremental tools (using free tiers). Total: $200-500.

## Drills Referenced

- the quora ads campaign build workflow (see instructions below) — complete campaign construction from question/topic research through targeting, creative, landing page, conversion tracking, and launch spec for Quora Ads Manager
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action (advance, iterate, or pivot)
