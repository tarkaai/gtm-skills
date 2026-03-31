---
name: creator-campaign-execution
description: Brief creators, manage the posting timeline, and capture results from each sponsored post
category: Influencer
tools:
  - Attio
  - PostHog
  - n8n
fundamentals:
  - creator-content-brief
  - creator-campaign-tracking
  - posthog-custom-events
  - posthog-funnels
  - attio-notes
  - n8n-triggers
---

# Creator Campaign Execution

This drill manages the lifecycle of a creator sponsorship from brief delivery through post publication to results capture. It ensures every post is tracked, every lead is captured, and every creator is managed through the process.

## Input

- Booked creator deals from `creator-outreach-pipeline` drill (creator, format, date, price, tracking link)
- Landing page URL (from `landing-page-pipeline` drill if applicable)
- PostHog project with tracking configured

## Steps

### 1. Generate and send the brief

For each booked creator, use `creator-content-brief` to generate a structured brief:

1. Draft the brief using Claude with campaign parameters: brand info, primary message, supporting point, tracking URL, posting window, disclosure requirement
2. Send the brief to the creator via email, Attio note, or Passionfroot brief field
3. Log the brief in Attio using `attio-notes` on the creator's record
4. Update creator status to "briefed"

**Timeline:** Send the brief at least 5 business days before the requested posting date. Creators need time to draft, and you may want to review before publishing.

### 2. Set up tracking infrastructure

For each creator post, use `creator-campaign-tracking`:

1. Generate a unique UTM-tagged URL for this specific creator and post
2. Verify the UTM link resolves correctly and PostHog captures the page view with UTM properties
3. If using a landing page, confirm the form submission fires `influencer_lead_captured` with the creator handle
4. Test the full flow: click link, land on page, submit form, verify event in PostHog and lead in Attio

### 3. Review draft (optional but recommended at Smoke level)

If you requested draft approval:
1. Creator sends draft content for review
2. Check: Is the tracking link present and correct? Is the disclosure included (#ad, #sponsored)? Is the primary message present?
3. Do NOT rewrite their content. Only flag if the tracking link is missing, disclosure is absent, or factual claims about your product are wrong.
4. Approve and confirm the posting date

### 4. Monitor posting

Use `n8n-triggers` to set up reminders:
1. 2 days before posting window: send creator a reminder email ("Looking forward to the post going live on {{date}}!")
2. On posting day: check the creator's profile or channel for the post
3. When post is confirmed live:
   - Capture the post URL
   - Log it in Attio on the creator record
   - Update status to "posted"
   - Start the measurement clock

### 5. Capture and log results

Starting from post publication, track for 7 days:

**Day 0-1 (first 24 hours):**
- Pull post engagement metrics: impressions, likes, comments, shares (manually from the platform or via API if available)
- Check PostHog for UTM-tagged traffic hitting the landing page
- Log early metrics in Attio

**Day 3:**
- Pull updated engagement metrics
- Count leads captured via PostHog: `influencer_lead_captured` events where `creator_handle = {{handle}}`
- Check lead quality: are the leads ICP matches? (verify in Attio)

**Day 7:**
- Pull final engagement metrics
- Calculate: total clicks, total leads, conversion rate, CPL, engagement rate
- Log final metrics in Attio
- Update creator status to "completed"

### 6. Process payment

After confirming the post went live and tracking link was used:
1. Trigger payment per agreed terms (typically net-15 or net-30)
2. For Passionfroot bookings: payment is handled by the platform
3. For direct deals: send payment via your accounts payable process
4. Log payment in Attio

## Output

- Each creator post tracked with full metrics (engagement, clicks, leads, CPL)
- All leads captured in PostHog and synced to Attio
- Creator records in Attio updated with performance data
- Payment processed and logged

## Triggers

Run once per booked creator post. At Smoke, you may execute 1-2 posts manually. At Baseline and beyond, use n8n workflows to automate reminders and metric collection.
