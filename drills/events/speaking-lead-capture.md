---
name: speaking-lead-capture
description: Capture and attribute leads from conference talks via QR codes, companion content, and post-talk follow-up sequences
category: Events
tools:
  - Attio
  - Cal.com
  - Loops
  - PostHog
  - Descript
fundamentals:
  - calcom-booking-links
  - attio-contacts
  - attio-lists
  - attio-notes
  - loops-sequences
  - posthog-custom-events
  - talk-content-repurposing
  - linkedin-organic-posting
---

# Speaking Lead Capture

This drill converts a delivered conference talk into attributed pipeline. It covers everything from pre-talk asset preparation through post-talk follow-up, ensuring every lead from the talk is captured, enriched, and entered into a nurture sequence.

## Input

- Talk title, conference name, conference date
- Talk recording (video or audio) -- may not be available until 1-4 weeks after the event
- Companion resource URL (blog post, GitHub repo, or landing page)
- Speaker's Cal.com scheduling link
- Attio configured with a "Speaking Leads" list

## Steps

### 1. Prepare lead capture assets (before the talk)

Set up the infrastructure that converts audience attention into trackable leads:

1. Create a Cal.com booking link using `calcom-booking-links` with event type "Post-Talk Chat" (15 min). Add UTM parameters: `utm_source=conference&utm_medium=talk&utm_campaign={conference_slug}`
2. Build a companion resource page (landing page or blog post) with:
   - Talk slides or key takeaways
   - Link to the Cal.com booking page
   - Email capture form (Loops embedded form or Tally form)
   - UTM-tagged links throughout: `utm_source={conference_slug}&utm_medium=talk&utm_campaign={talk_slug}`
3. Generate a QR code that points to the companion resource URL (use any QR code API: `https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={encoded_url}`)
4. Add the QR code to the final slide of the talk deck

### 2. Track talk delivery (day of talk)

Fire PostHog events using `posthog-custom-events`:

```
Event: speaking_talk_delivered
Properties:
  conference_name: "{conference}"
  talk_title: "{title}"
  estimated_audience: {number}
  talk_date: "{ISO date}"
  format: "{keynote|breakout|lightning|workshop}"
```

### 3. Capture leads (during and after talk)

Leads arrive through three channels. Track each:

**Channel A: QR code scans (companion page visits)**
- PostHog tracks page views on the companion resource page
- Filter by `utm_source={conference_slug}` to attribute to this talk
- Event: `speaking_companion_page_viewed` with `conference_name`, `talk_title`

**Channel B: Cal.com bookings**
- Cal.com fires a webhook on booking. Capture via n8n or direct integration
- Event: `speaking_meeting_booked` with `conference_name`, `talk_title`, `booker_email`, `booker_name`
- Create Attio contact using `attio-contacts` with tag `source:conference-talk`, `conference:{name}`

**Channel C: Email signups (companion page form)**
- Loops captures the signup and adds to a segment
- Event: `speaking_email_captured` with `conference_name`, `talk_title`
- Add to Attio using `attio-contacts` with same tagging

### 4. Run post-talk follow-up sequence

Using `loops-sequences`, trigger a 3-email follow-up for all captured leads:

**Email 1 (Day 0-1):** "Thanks for catching my talk at {Conference}"
- Link to companion resource (slides, code, blog post)
- Cal.com link for 1:1 follow-up

**Email 2 (Day 3):** "The key insight most people missed"
- Expand on one specific takeaway from the talk
- Soft CTA to try the product or read a related resource

**Email 3 (Day 7):** "What attendees asked after the talk"
- Answer the top 2-3 questions from the Q&A or hallway conversations
- Direct CTA to Cal.com booking or product signup

Log sequence engagement in Attio using `attio-notes`: who opened, who clicked, who booked.

### 5. Repurpose the talk recording

When the recording becomes available, run `talk-content-repurposing` to produce:

- Blog post from the transcript (publish on your blog, link back to companion page)
- 3-5 social video clips with captions
- 3-5 quote graphics

Post clips on LinkedIn using `linkedin-organic-posting` with conference hashtags and speaker tags. Each clip drives additional traffic to the companion page, extending the talk's lead generation window from days to weeks.

### 6. Log attribution and measure

After 30 days, tally all leads attributed to this talk:

1. Query PostHog for all events with `conference_name = {this conference}`
2. Count unique leads by channel: QR scans, Cal.com bookings, email signups, social clip traffic
3. Log the final tally in Attio as a note on the conference record
4. Fire `speaking_talk_roi_calculated` event with: `total_leads`, `meetings_booked`, `leads_per_channel`, `estimated_pipeline_value`

## Output

- Pre-talk lead capture infrastructure (QR code, companion page, Cal.com link)
- Real-time lead tracking across 3 channels
- Automated 3-email post-talk follow-up sequence
- Repurposed content extending the talk's lead window
- 30-day attribution report per talk

## Triggers

- Run asset preparation 7+ days before each talk
- Post-talk follow-up triggers automatically on lead capture
- Content repurposing runs when recording is available
- 30-day attribution report runs monthly for all talks delivered that month
