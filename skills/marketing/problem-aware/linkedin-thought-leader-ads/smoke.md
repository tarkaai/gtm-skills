---
name: linkedin-thought-leader-ads-smoke
description: >
  Thought Leader Ads — Smoke Test. Select 3-5 high-performing organic LinkedIn posts from the
  founder's profile, promote them as Thought Leader Ads with a $300-500 test budget, and validate
  that TLAs produce measurably higher engagement and lower CPC than company-page ads.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5,000 impressions, >=1.5% engagement rate, and >=5 qualified profile visits or website clicks from $300-500 test budget"
kpis: ["Impressions", "Engagement rate", "CPC", "Profile visits from ICP titles", "Website clicks"]
slug: "linkedin-thought-leader-ads"
install: "npx gtm-skills add marketing/problem-aware/linkedin-thought-leader-ads"
drills:
  - tla-post-selection
  - threshold-engine
---

# Thought Leader Ads — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

Prove that promoting the founder's organic LinkedIn posts as Thought Leader Ads produces meaningful engagement with problem-aware prospects at a lower cost per click than standard company-page sponsored content. At this level, the agent assists with post selection and scoring, the founder publishes organically, and Campaign Manager setup is manual. No automation, no always-on spend.

**Pass threshold:** >=5,000 impressions, >=1.5% engagement rate, and >=5 qualified profile visits or website clicks from $300-500 test budget within 1 week.

## Leading Indicators

- TLA engagement rate exceeds 1.5% (vs 0.3-0.5% benchmark for company-page ads)
- CPC is below $5 (vs $8-15 benchmark for standard LinkedIn Sponsored Content)
- Comments on promoted posts include people matching ICP titles (VP, Director, Head of)
- Thought leader receives profile views or connection requests from ICP-matching prospects
- At least 1 post generates organic engagement beyond the paid reach (comments that attract non-targeted viewers)

## Instructions

### 1. Confirm Prerequisites

Verify the following before starting:

1. The founder has an active LinkedIn profile with Creator Mode enabled and at least 10 posts published in the last 90 days
2. Your company has a LinkedIn Page linked to Campaign Manager
3. Campaign Manager has billing configured
4. The LinkedIn Insight Tag is installed on your website (needed for conversion tracking)

If any prerequisite is missing, resolve it first. Do not proceed without the Insight Tag -- you will not be able to measure website conversions.

### 2. Grant TLA Permissions

**Human action required:** In Campaign Manager, navigate to Account Assets > Thought Leader Ads. Search for the founder by name. Send the permission request. The founder must accept via their LinkedIn notification or Settings > Account Preferences > Thought Leader Ads.

This is a one-time setup step. Once permission is granted, it persists for all future campaigns.

### 3. Run Post Selection

Run the `tla-post-selection` drill for the founder's profile:

1. Pull the founder's post analytics for the last 90 days (via Taplio, Shield, or LinkedIn native analytics)
2. Filter for TLA-eligible posts (remove polls, reshares, articles, celebrations)
3. Score each post on: organic engagement, ICP pain-point alignment, problem-aware framing, and comment quality
4. Select 3-5 top-scoring posts with format and topic diversity
5. Get the founder's approval on each selected post

For the Smoke test, manual analytics review is acceptable. You do not need Taplio or Shield -- LinkedIn's native Creator Analytics provides enough data to rank posts.

### 4. Create the Test Campaign

**Human action required:** In Campaign Manager:

1. Create a new campaign group: "TLA Smoke Test - [Founder Name] - [Date]"
2. Create one campaign:
   - Objective: **Engagement** (delivers lower CPC than Brand Awareness for TLAs)
   - Ad format: Single image ad
   - Placement: LinkedIn feed only
3. Add the 3-5 selected posts as separate ads within the campaign
4. Configure targeting -- keep it simple for the Smoke test:
   - Job function matching your ICP (e.g., Engineering, Product)
   - Seniority: Director and above
   - Company size: 50-1,000 employees
   - Industry: Software, Internet, Technology
   - Audience size target: 30,000-100,000
5. Exclude: your company's employees, known competitors
6. Set budget: $50-75/day for 7 days ($350-525 total)
7. Bidding: Maximum Delivery (automated)
8. Launch the campaign

### 5. Monitor for 7 Days

Check Campaign Manager daily for 7 days. Track:

- Per-post metrics: impressions, engagement rate, clicks, CPC
- Audience insights: which job titles and industries are engaging
- Social actions: count of likes, comments, and shares (these amplify organic reach)
- The founder's profile view count (check LinkedIn analytics -- TLAs drive profile visits)

Log all metrics in a spreadsheet or Attio note. After 3 days, if any post has zero engagement or CTR below 0.3%, consider replacing it with the next post from the selection list.

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 7 days, pull final campaign metrics from Campaign Manager
2. Calculate:
   - Total impressions (threshold: >=5,000)
   - Average engagement rate across all posts (threshold: >=1.5%)
   - Average CPC (benchmark reference: should be below $5)
   - Qualified interactions: count of profile visits, website clicks, or comments from people matching ICP titles (threshold: >=5)
3. Compare TLA metrics to any company-page ad benchmarks you have (if available)
4. Pass threshold: >=5,000 impressions AND >=1.5% engagement rate AND >=5 qualified interactions

**If PASS:** The TLA format works for your audience. Proceed to Baseline with increased budget and proper tracking.

**If FAIL:** Diagnose:
- Low impressions: audience too small or budget too low. Broaden targeting or increase daily budget.
- Low engagement: posts not resonating. Review which pain points the ICP cares about. Test different post styles.
- Low qualified interactions: audience targeting is off. Check if engaging users match your ICP or are outside your target.

## Time Estimate

- 0.5 hours: Confirm prerequisites and grant TLA permissions
- 2 hours: Run post selection drill (pull analytics, score, select)
- 1 hour: Create campaign in Campaign Manager (targeting, budget, launch)
- 1.5 hours: Daily monitoring over 7 days (~15 min/day)
- 1 hour: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | TLA campaign creation and management | No platform fee; ad spend only |
| LinkedIn Campaign Manager | Campaign setup and performance reporting | Included with ad account |
| Attio | CRM — log campaign results and contacts | Free plan (up to 3 users) or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Taplio (optional) | LinkedIn analytics for post selection | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |

**Estimated play-specific cost this level:** $300-500 ad spend. Tools: $0 incremental if using LinkedIn native analytics, or ~$49/mo if adding Taplio for better post analytics.

## Drills Referenced

- `tla-post-selection` — identify and score organic LinkedIn posts for TLA promotion based on engagement signals and ICP pain-point alignment
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action (advance, iterate, or pivot)
