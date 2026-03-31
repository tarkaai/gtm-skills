---
name: value-asset-outreach-sequence
description: Build and launch a cold email sequence that leads with a free value asset instead of a pitch
category: Outreach
tools:
  - Instantly
  - Clay
  - Attio
  - PostHog
fundamentals:
  - instantly-campaign
  - instantly-warmup
  - instantly-reply-detection
  - clay-enrichment-waterfall
  - clay-claygent
  - attio-contacts
  - posthog-custom-events
---

# Value Asset Outreach Sequence

This drill produces a 3-step cold email sequence where the value asset is the centerpiece. Unlike standard cold email that pitches a product, this sequence gives first and asks second. The asset earns the reply.

## Input

- Completed value asset (from `value-asset-creation` drill) with a hosted URL
- Enriched prospect list in Clay with ICP scoring (from `build-prospect-list` drill)
- Founder's name and email address for sending
- Cal.com booking link

## Steps

### 1. Build personalization variables in Clay

Using the `clay-enrichment-waterfall` fundamental, create these template columns:

- `personalization_line`: One sentence referencing something specific about the prospect's company or role. Use the `clay-claygent` fundamental to generate from their LinkedIn profile, company blog, or recent news. Never use "I noticed that..." — state the observation directly.
- `pain_category`: Which specific sub-problem from your ICP the prospect likely faces. Derived from their company size, industry, and role. This determines which angle of the asset to highlight in the email.
- `asset_hook`: A one-sentence description of the most relevant section of your asset for this prospect. Example: "the section on reducing onboarding time for teams under 50 people."

### 2. Write the 3-step sequence

**Email 1 — The Gift (Day 0)**

Job: Deliver the asset with zero pitch. The email earns permission to follow up by providing value first.

Structure:
- Line 1: Personalization referencing their specific situation. `{{personalization_line}}`
- Line 2: "I put together a [asset type] on [topic] — specifically for [ICP description]."
- Line 3: One sentence on what the asset covers that is relevant to their `{{pain_category}}`.
- Line 4: "Here it is: [asset URL]" — direct link, no landing page gate, no form.
- Line 5: "No ask from me — just thought it would be useful."
- Sign off: First name only.

Constraints: Under 80 words. No pitch. No CTA for a meeting. No "I'd love to" or "Would you be open to." The asset IS the message.

**Email 2 — The Follow-Up Insight (Day 4-5)**

Job: Add a specific insight FROM the asset that is relevant to the prospect's situation. Demonstrate you understand their world.

Structure:
- Line 1: "Quick follow-up on the [asset type] I shared —"
- Line 2-3: Call out one specific finding or recommendation from the asset that applies to their company. Reference `{{asset_hook}}`. Example: "Given that [company] is scaling past [X employees/stage], the section on [specific topic] might save your team [specific outcome]."
- Line 4: "Curious if that matches what you are seeing?" — genuine question, not a disguised pitch.

Constraints: Under 70 words. Still no pitch. The goal is a reply, not a meeting.

**Email 3 — The Offer (Day 9-10)**

Job: Now that you have given value twice, make a specific offer tied to the asset's content.

Structure:
- Line 1: "Last note on this —"
- Line 2: Connect the asset's core problem to your product's solution. One sentence. Example: "We built [product] to automate exactly what the [asset type] walks through manually."
- Line 3: Social proof if available — one customer result in one sentence.
- Line 4: "Worth 15 minutes to see if it fits [company]? Here's my calendar: [Cal.com link]"
- Line 5: "Either way, hope the [asset type] was useful."

Constraints: Under 75 words. The tone stays helpful, not salesy. The pitch is earned by the prior two emails.

### 3. Verify sending infrastructure

Use the `instantly-warmup` fundamental to confirm all sending accounts have:
- SPF, DKIM, and DMARC records configured
- At least 2 weeks of warmup completed
- Inbox placement rate above 90%
- Daily send limit set to 20-30 per account (founder emails must not look mass-produced)

### 4. Configure the campaign in Instantly

Using the `instantly-campaign` fundamental:

1. Create a campaign named `[Date]-value-asset-[ICP-segment]`
2. Upload leads from Clay with all personalization variables mapped
3. Load the 3-step sequence with merge fields
4. Set sending schedule: weekdays, 7:00am-9:30am in prospect's timezone
5. Disable open tracking (reduces spam risk; replies are the metric, not opens)
6. Enable link tracking only for the asset URL (to measure who clicks)

### 5. Set up reply detection and routing

Using the `instantly-reply-detection` fundamental:

- **Positive reply** (interested, asked a question, thanked for the asset): Route to Attio as a warm lead with tag `asset-reply-positive`. Notify the founder immediately via Slack.
- **Negative reply** (not interested, wrong person): Mark in Attio as `opted-out`. Remove from future sequences.
- **Asset-referencing reply** (mentions specific content from the asset): Tag in Attio as `asset-engaged` — these are the highest-quality leads. They read it.
- **Out of office**: Pause the sequence and resume when the OOO period ends.

### 6. Log events to PostHog

Using the `posthog-custom-events` fundamental, fire these events:

- `value_asset_email_sent` — properties: step (1/2/3), prospect_id, campaign_id
- `value_asset_link_clicked` — properties: asset_url, prospect_id
- `value_asset_reply_received` — properties: sentiment (positive/negative/neutral), references_asset (boolean)
- `value_asset_meeting_booked` — properties: prospect_id, source_step

### 7. Quality check before launch

Preview the first 10 rendered emails (with variables filled). Check:
- Does the personalization feel specific and real?
- Does the asset link work and load quickly?
- Is each email under its word limit?
- Does the tone feel like a founder sharing something useful, not an SDR running a sequence?

If any email feels templated, rewrite the personalization for that prospect or remove them from the batch.

## Output

- A 3-step email sequence loaded in Instantly, ready to send
- Clay table with personalization variables mapped to Instantly merge fields
- Reply detection routing configured to Attio with proper tags
- PostHog event tracking for the full funnel

## Triggers

Run once per prospect batch at Smoke/Baseline. At Scalable, new batches launch weekly via automation.
