---
name: trade-show-lead-nurture
description: Segment trade show leads by interest tier and route into automated follow-up sequences calibrated to booth interaction depth
category: Events
tools:
  - Loops
  - Attio
  - Loom
  - n8n
  - PostHog
fundamentals:
  - loops-sequences
  - attio-contacts
  - attio-deals
  - loom-personalized-outreach
  - loom-embed-in-email
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# Trade Show Lead Nurture

This drill converts raw trade show leads into pipeline through segmented, automated follow-up. The key insight: trade show leads have a 72-hour half-life. Every day you delay follow-up, response rates drop by roughly 50%. This drill ensures Tier 1 leads hear from you within 12 hours and all tiers are in a nurture sequence within 48 hours.

## Input

- Attio list from `trade-show-booth-operations` drill: contacts with interest level, demo path, agreed next step, and booth notes
- Loom account for personalized video follow-ups (Tier 1)
- Loops sequences configured for each tier
- n8n instance for routing and trigger logic

## Steps

### 1. Segment leads by tier (within 4 hours of show close)

Build an n8n workflow using `n8n-triggers` that reads the Attio trade show list and segments:

- **Tier 1 — Hot (interest 5, agreed to meeting or deep demo):** These prospects expressed clear buying intent. They either booked a meeting at the booth or asked detailed product questions that indicate active evaluation. Expected: 5-10% of total booth leads.
- **Tier 2 — Warm (interest 3-4, saw a guided demo):** Interested and engaged, but did not commit to a next step. They may be evaluating multiple solutions or need internal buy-in. Expected: 20-30% of total.
- **Tier 3 — Curious (interest 2-3, elevator pitch only):** Stopped by the booth, had a brief conversation, but did not see a full demo. May become relevant later. Expected: 30-40% of total.
- **Tier 4 — Badge scan only (interest 1, no meaningful conversation):** Badge was scanned but no substantive interaction. These go into long-term nurture only. Expected: 20-30% of total.

Using `attio-contacts`, tag each contact with their tier. This tag drives all downstream routing.

### 2. Tier 1 follow-up (within 12 hours)

For each Tier 1 lead, the agent prepares a personalized follow-up:

1. Use `loom-personalized-outreach` to record a 60-90 second personalized Loom video per lead. Reference: their name, their company, the specific pain point they mentioned at the booth, and the part of the demo that addressed it. End with a clear ask: "I've booked our follow-up for [date] — looking forward to it" or "Let's find a time this week — here's my calendar."
2. Use `loom-embed-in-email` to create the follow-up email. Structure:
   - Subject: "{First name} — following up from {show name}"
   - Body: 2-3 sentences referencing the booth conversation. Embedded Loom thumbnail. Cal.com link if no meeting booked yet.
3. Send via the booth staff member's email (not a marketing tool) to keep it personal.
4. Log the follow-up in Attio. Update the deal record with follow-up timestamp and Loom link.
5. Fire PostHog event: `trade_show_followup_sent` (properties: show_name, tier, followup_type: "personalized_loom", days_since_show)

**Human action required:** The booth staff member who had the conversation should record the Loom. The agent can draft the talking points and prepare the email template, but a human face on the video is critical for Tier 1.

### 3. Tier 2 follow-up (within 24 hours)

Enroll Tier 2 leads in a 3-touch Loops sequence using `loops-sequences`:

**Email 1 (day 1):** Reference the show and their interest area. Share a relevant resource — case study, one-pager, or blog post that addresses the pain point noted in their booth interaction. Include a Cal.com link.

**Email 2 (day 4):** Share a second resource from a different angle (e.g., if email 1 was a case study, email 2 is a product deep-dive or webinar recording). Ask: "Would it be helpful to walk through how this applies to {their company}?"

**Email 3 (day 8):** Lightweight check-in: "I know trade shows produce a flood of follow-ups. If {pain point} is still a priority for your team, I'd love 15 minutes to show you something specific. If now isn't the right time, no worries at all."

For each Tier 2 contact, pull the booth notes from Attio and use them to personalize the pain point and resource references in the sequence. This is the difference between "here's our product" and "at the booth you mentioned [specific problem] — here's how we solve it."

Track: `trade_show_nurture_email_sent`, `trade_show_nurture_email_opened`, `trade_show_nurture_reply_received` via PostHog.

### 4. Tier 3 follow-up (within 48 hours)

Enroll Tier 3 leads in a lighter 2-touch Loops sequence:

**Email 1 (day 2):** "Great meeting you at {show name}. We help companies like {their company type} solve {ICP pain point}. Here's a quick overview: {link to product page or one-pager}."

**Email 2 (day 7):** "If {pain point} comes up for your team, we'd love to help. Here's a 2-minute video overview: {product video link}. Feel free to book time if you'd like to explore: {Cal.com link}."

No further outreach unless they engage (open 3+ times or click).

### 5. Tier 4 long-term nurture

Add Tier 4 to your general marketing nurture list in Loops. No trade-show-specific follow-up beyond a single "Thanks for visiting our booth" email. These contacts may convert through other channels later.

### 6. Escalation triggers

Build n8n workflows using `n8n-triggers` that watch for engagement signals and escalate:

- **Tier 2 reply received**: Auto-create an Attio deal, notify the booth staff member via Slack, and fast-track to personal follow-up.
- **Tier 3 opens email 3+ times**: Promote to Tier 2 and enroll in the Tier 2 sequence.
- **Any tier visits pricing page** (detected via PostHog): Alert the assigned sales rep immediately. This is a buying signal.
- **Tier 1 no-show on booked meeting**: Trigger a reschedule sequence — 2 hours after the missed meeting, send a friendly "let's find another time" with 3 suggested slots.

### 7. Track nurture funnel

Fire PostHog events at every step using `posthog-custom-events`:

- `trade_show_followup_sent` (tier, followup_type, days_since_show)
- `trade_show_followup_opened` (tier, sequence_step)
- `trade_show_followup_clicked` (tier, link_type)
- `trade_show_followup_replied` (tier, sentiment)
- `trade_show_meeting_booked_from_nurture` (tier, days_since_show, source_email_step)
- `trade_show_deal_created_from_nurture` (tier, days_since_show, deal_value_estimate)

Build a PostHog funnel: `trade_show_followup_sent` -> `trade_show_followup_opened` -> `trade_show_followup_replied` -> `trade_show_meeting_booked_from_nurture` -> `trade_show_deal_created_from_nurture`. Group by tier to compare conversion rates.

## Output

- All trade show leads segmented by tier in Attio
- Tier 1: personalized Loom follow-ups sent within 12 hours
- Tier 2: 3-touch automated nurture sequence running
- Tier 3: 2-touch lightweight nurture running
- Tier 4: added to general marketing nurture
- Escalation triggers active for engagement signals
- Full PostHog event trail from follow-up through deal creation

## Triggers

- Run once per trade show, starting the evening of the first show day
- Tier 1 follow-up: within 12 hours of lead capture
- Tier 2-3 sequences: enrolled within 24-48 hours
- Escalation triggers: always-on during the 30-day nurture window
