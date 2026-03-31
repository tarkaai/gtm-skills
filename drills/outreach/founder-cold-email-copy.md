---
name: founder-cold-email-copy
description: Write cold email sequences where the founder sends to solution-aware prospects comparing alternatives
category: Outreach
tools:
  - Instantly
  - Clay
fundamentals:
  - instantly-campaign
  - clay-enrichment-waterfall
  - clay-claygent
---

# Founder Cold Email Copywriting for Solution-Aware Prospects

This drill produces a 3-step cold email sequence written from the founder's voice to prospects who already know the solution category exists and are evaluating options. The copy must position against alternatives without sounding defensive, and leverage the founder's credibility (not an SDR's).

## Prerequisites

- ICP definition complete (run `icp-definition` drill)
- Clay table with enriched prospect data including: company name, first name, role, technology stack, and at least one competitor or alternative they may be using
- Understanding of 2-3 alternatives your prospects are likely comparing (competitors, DIY, status quo)

## Why Founder-Sent Matters

Solution-aware prospects are comparing options. An email from a founder carries signals an SDR email does not: the sender built the product, has direct authority to negotiate, and implicitly signals the company values the recipient enough for the CEO to reach out. This changes what you can say and how you say it.

## Steps

### 1. Build the competitive context brief

Before writing a single email, document the alternatives your prospects are evaluating. For each alternative, write one sentence on what it does well and one sentence on the specific gap your product fills. Do NOT write generic competitive claims. Use real specifics.

Example for a hypothetical analytics tool:
- **Competitor A**: Great dashboards but requires a data engineer to set up. Gap: your product is self-serve.
- **DIY/spreadsheets**: Free but breaks above 10 users. Gap: your product scales without manual work.
- **Status quo (doing nothing)**: No cost but the team wastes 5 hours/week on manual reporting. Gap: your product automates the reporting.

Use the `clay-claygent` fundamental to research each prospect's current stack and identify which alternative they are most likely using. Add a "likely_alternative" column to your Clay table.

### 2. Write the 3-step sequence

Each email has a specific job. Write all three before sending any.

**Email 1 — The Founder Intro (Day 0)**

Job: Establish that the founder is writing personally, acknowledge the prospect is evaluating solutions, and plant one specific differentiation seed.

Structure:
- Line 1: One-line personalization referencing something specific about the prospect (their company's recent milestone, a job posting, a blog post, their tech stack). Use Clay `{{personalization_line}}` variable. Never use "I saw that..." — state the observation directly.
- Line 2-3: "I'm [first name], founder of [company]. We built [product] specifically for [ICP description] who [specific pain point]."
- Line 4: One sentence positioning against the likely alternative WITHOUT naming the competitor. Example: "Most teams in your space end up stitching together spreadsheets and BI tools — we replace that entire workflow."
- Line 5: Soft CTA. "Would it be useful to see how [specific customer similar to prospect] handles this? Happy to share the 2-minute version."

Constraints: Under 90 words total. No links. No attachments. No HTML. Plain text only.

**Email 2 — The Proof Point (Day 3-4)**

Job: Deliver one concrete data point or customer outcome that makes the prospect think "that could be us."

Structure:
- Line 1: "Quick follow-up — thought this might be relevant."
- Line 2-3: One specific result from a customer similar to the prospect. Include the number, the timeframe, and the context. Example: "[Customer] cut their pipeline review from 3 hours to 20 minutes after switching from [category of alternative]. Their team of [size similar to prospect] was fully running within a week."
- Line 4: "Worth a 15-minute conversation to see if the same applies for [prospect company]?"

Constraints: Under 70 words. One data point only — do not stack multiple proof points.

**Email 3 — The Direct Ask (Day 7-8)**

Job: Give a clear reason to respond NOW and make the CTA frictionless.

Structure:
- Line 1: "Last note from me on this —"
- Line 2: Acknowledge you might be wrong about fit. "If [product] isn't the right fit for [company], no worries at all."
- Line 3: Restate the single strongest reason to talk. Tie it to a time-sensitive element if genuine (upcoming quarter, hiring plan, product launch).
- Line 4: Direct CTA with booking link. "Here's my calendar if it's easier: [Cal.com link]"
- Line 5: Sign off with first name only (not "Best regards, [Full Name], CEO").

Constraints: Under 60 words. Include the Cal.com booking link here and only here.

### 3. Build personalization variables in Clay

Using the `clay-enrichment-waterfall` fundamental, create these template columns in your Clay table:

- `personalization_line`: A one-sentence observation about the prospect. Use Clay's AI column to generate this from their LinkedIn headline, company description, or recent news. Review the first 10 manually to calibrate quality.
- `likely_alternative`: What the prospect is probably using today (competitor name, "spreadsheets", "manual process", etc.). Derived from technographic data or company size inference.
- `similar_customer`: The name of your customer most similar to this prospect (by size, industry, or use case). If you have fewer than 5 customers, use a composite: "teams like yours."
- `proof_metric`: The specific number result from your similar customer story.

### 4. Load the sequence into Instantly

Using the `instantly-campaign` fundamental:

1. Create a campaign named `[Date]-[ICP segment]-founder-email`
2. Upload leads from Clay with all personalization variables mapped
3. Set the sequence steps with the copy from Step 2, using `{{variable}}` merge fields
4. Set sending schedule: weekdays, 7:30am-9:30am in the prospect's timezone (founder emails sent early signal "I'm thinking about you before my day starts")
5. Set daily limit to 15-20 per sending account (lower than typical SDR volume — founder emails should not look mass-produced)
6. Disable open tracking (reduces spam filter risk and founders do not need to obsess over opens — replies are the metric)

### 5. Quality-check before sending

Review the first 5 rendered emails (with variables filled in) before activating the campaign. Check:
- Does the personalization line feel real and specific, not generic?
- Is the tone conversational, not corporate? A founder email should read like a human wrote it over coffee, not like marketing reviewed it.
- Is each email under the word limit?
- Is the Cal.com link correct and working?

If any rendered email feels templated, rewrite the personalization variable for that prospect or exclude them from this batch.

## Output

- A 3-step email sequence loaded in Instantly, ready to send
- Clay table with personalization variables mapped to Instantly merge fields
- Campaign configured with founder-appropriate sending limits and schedule

## Reusability

This drill is used by any play that requires founder-sent cold email to solution-aware prospects. The competitive context and proof points change per product, but the structure and tone remain constant.
