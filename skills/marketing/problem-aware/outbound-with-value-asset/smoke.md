---
name: outbound-with-value-asset-smoke
description: >
  Outbound With Value Asset — Smoke Test. Create one value asset and send it to 50-100
  problem-aware prospects via cold email to validate that asset-led outbound generates
  replies referencing the asset content.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=2 positive replies that reference the asset content in 1 week"
kpis: ["Asset link click rate", "Reply rate", "Asset-referencing reply count"]
slug: "outbound-with-value-asset"
install: "npx gtm-skills add marketing/problem-aware/outbound-with-value-asset"
drills:
  - icp-definition
  - build-prospect-list
  - value-asset-creation
  - threshold-engine
---

# Outbound With Value Asset — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Success at Smoke means proving that leading with a value asset changes the quality of outbound replies. You are not testing volume or automation — you are testing whether prospects engage with the asset itself and respond differently than to a standard cold email.

**Pass threshold:** >=2 positive replies that specifically reference the asset content within 1 week of sending to 50-100 prospects.

A "referencing" reply means the prospect mentions something from the asset: a data point, a recommendation, a section. Generic "thanks" replies do not count.

## Leading Indicators

- Asset link click rate above 15% (prospects are curious enough to open it)
- At least 5 recipients click the asset link within 48 hours of sending
- At least 1 reply arrives within the first 3 days
- No negative replies citing the asset as irrelevant or spammy

## Instructions

### 1. Define your ICP and identify the pain point

Run the `icp-definition` drill to document your Ideal Customer Profile. Focus on:
- Which specific operational pain point your prospects face that your product addresses
- What company size, industry, and job titles map to this pain
- What triggers make this pain acute right now (hiring, funding, scaling)

The pain point you identify here determines the asset topic. Choose a pain that is widespread enough to be relevant to 80%+ of your list but specific enough that a generic report would not cover it.

### 2. Build a prospect list of 50-100 contacts

Run the `build-prospect-list` drill to source and enrich 50-100 contacts matching your ICP from Clay and Apollo. Push them to Attio. For Smoke, keep the list tight — quality over quantity. Every prospect should be someone the founder would genuinely want to help.

### 3. Create the value asset

Run the `value-asset-creation` drill. This is the core of the play. Produce a 1-5 page asset (checklist, benchmark, scorecard, or short report) that:
- Addresses the ICP pain point identified in step 1
- Delivers standalone value without pitching your product
- Contains at least one proprietary insight, data point, or framework
- Ends with a single soft CTA connecting the asset's topic to your product

Host the asset at a clean URL. At Smoke level, a Google Doc exported as PDF and hosted on your site is sufficient. No landing page gate — direct link, no form.

**Human action required:** The founder must review the asset draft, verify all data, and add personal anecdotes or opinions. The asset should read as "the founder wrote this" not "AI generated this."

### 4. Send the outreach manually

At Smoke level, the founder sends the emails personally. No automation tool required. Write a short email for each prospect:

- Line 1: One specific observation about their company or role
- Line 2: "I put together a [asset type] on [topic] for [ICP description]."
- Line 3: "Here it is: [direct link to asset]"
- Line 4: "No ask — thought it would be useful."

Send 10-20 per day over 3-5 days. Log each send in Attio with the date and prospect name.

**Human action required:** Send each email from the founder's personal email. Personalize line 1 for each prospect — do not batch-send identical messages at this level.

### 5. Track responses and evaluate

For each reply, log in Attio:
- Did the prospect reference something specific from the asset? (Tag: `asset-referenced`)
- Was the reply positive, neutral, or negative?
- Did the prospect ask a follow-up question or request a meeting?

After 1 week, run the `threshold-engine` drill to evaluate: >=2 positive replies that reference the asset content.

**If PASS:** The asset resonates. Proceed to Baseline to automate the sequence and scale volume.

**If FAIL:** Diagnose:
- If click rate was low (<10%): the email copy or subject line is not compelling enough. Rewrite.
- If clicks were high but no replies: the asset is interesting but does not prompt action. Add a stronger insight or make the CTA more specific.
- If replies are positive but do not reference the asset: the email is working but the asset is forgettable. Strengthen the asset content.

## Time Estimate

- ICP definition and prospect list: 2 hours
- Value asset creation and review: 2.5 hours
- Manual email sending (50-100 emails over 5 days): 1 hour
- Response tracking and evaluation: 0.5 hours
- **Total: ~6 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Prospect enrichment and research | Free tier: 100 credits, 500 actions/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Apollo | Initial prospect sourcing | Free: 5 mobile + 10 export credits/mo ([apollo.io/pricing](https://www.apollo.io/pricing)) |
| Attio | CRM logging and tracking | Free: up to 3 users ([attio.com](https://attio.com)) |
| Google Docs | Asset creation | Free |
| Anthropic API | Asset draft generation | ~$0.05 for one asset draft ([anthropic.com](https://www.anthropic.com)) |

**Estimated monthly cost: $0** (all free tiers sufficient at Smoke volume)

## Drills Referenced

- `icp-definition` — define the target audience and pain point that drives the asset topic
- `build-prospect-list` — source and enrich 50-100 prospects matching ICP
- `value-asset-creation` — research, draft, and produce the value asset
- `threshold-engine` — evaluate results against the pass threshold
