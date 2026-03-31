---
name: field-event-content-capture
description: Capture insights, quotes, and themes from in-person field events and repurpose them into marketing content that promotes future events
category: Events
tools:
  - Fireflies
  - Descript
  - Attio
  - Loops
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - attio-notes
  - attio-lists
  - loops-broadcasts
  - posthog-custom-events
  - ai-content-ghostwriting
  - linkedin-organic-posting
---

# Field Event Content Capture

This drill extracts value from in-person field events beyond the direct pipeline. Every dinner conversation, happy hour debate, and lunch discussion contains insights that can be turned into content — content that promotes the next event, establishes thought leadership, and keeps attendees engaged between events.

The challenge with in-person events is that conversations are ephemeral. This drill creates a systematic capture-and-repurpose workflow.

## Input

- Completed field event with attendance logged in Attio
- Host's post-event debrief notes (voice memo or written, captured within 2 hours of event end)
- Any photos taken at the event (with attendee consent for sharing)
- If the event had a structured discussion portion, any recording from Fireflies

## Steps

### 1. Capture the host debrief

Within 2 hours of the event ending (while memory is fresh), the host records a 5-10 minute voice debrief covering:
- Top 3 discussion themes that got the most energy
- Any surprising insights or contrarian takes from attendees
- Specific quotes or stories that resonated (paraphrased if exact recall is imperfect)
- Pain points or challenges that multiple attendees mentioned
- Product-relevant signals (features requested, competitors mentioned, buying timeline hints)
- Overall energy level and format feedback (what worked, what to change)

If the host used Fireflies to record a structured discussion segment, pull the transcript using `fireflies-transcription` and extract key themes and action items with `fireflies-action-items`.

If no recording exists, the voice memo debrief is the primary input. Use a transcription service to convert it to text.

### 2. Extract structured insights

Process the debrief into structured data and log in Attio using `attio-notes`:

**Per-event insights record:**
- Event slug, city, date, format, attendee count
- Top 3 themes discussed (tagged by category: industry trend, pain point, competitive landscape, technology shift, market dynamics)
- Notable quotes (anonymized unless the speaker consented to attribution): "A VP of Engineering at a Series B company said..."
- Product signals: feature requests, competitor mentions, pricing sensitivity indicators
- Market intelligence: hiring trends, budget changes, technology adoption patterns mentioned by attendees

**Per-attendee intelligence updates:**
For each Tier 1 and Tier 2 attendee, update their Attio contact record with:
- Topics they were most engaged on
- Pain points they mentioned
- Competitive products they referenced
- Timeline or budget signals

### 3. Produce derivative content

Using `ai-content-ghostwriting`, transform event insights into 3-4 content pieces per event:

**Content piece 1 — LinkedIn discussion post:**
Take the most energetic discussion theme and write a LinkedIn post from the host's perspective:
- Hook: "Hosted a dinner with [N] [title]s in [city] last week. One topic dominated the conversation: [theme]."
- 3-4 paragraphs sharing the key perspectives (anonymized) and the host's synthesis
- CTA: "If you're in [next event city], we're doing this again on [date]. [link]"
- Post using `linkedin-organic-posting`

**Content piece 2 — Event recap email:**
Using `loops-broadcasts`, send a recap to all attendees (including no-shows):
- 3 key takeaways from the discussion
- An anonymized "quote of the night" that captures the event's energy
- A link to any resources mentioned during the discussion
- Next event announcement with early-access RSVP link

**Content piece 3 — Newsletter segment:**
Write a 200-word newsletter section: "What we heard in [city]" summarizing the top theme with market context. Feed this to the company newsletter pipeline for inclusion in the next send.

**Content piece 4 (optional) — Data insight post:**
If the discussion surfaced a quantifiable trend ("7 out of 10 attendees said they're consolidating vendors this year"), write a data-driven LinkedIn post with the finding and analysis.

### 4. Feed content into promotion for next event

Store all content pieces in Attio tagged by event and city. When the next event in the same city is being promoted (via `field-event-series-automation`), the invitation sequence references insights from the previous event:
- "At our last [city] dinner, the room spent an hour debating [theme]. This time we're tackling [new topic]."
- Include a quote from the recap to signal the quality of conversation

This creates a flywheel: each event's content promotes the next event, and returning attendees see that their contributions are valued.

### 5. Track content performance

Using `posthog-custom-events`, track:
- `field_event_content_published` (properties: event_slug, city, content_type, channel)
- `field_event_content_engaged` (properties: event_slug, content_type, engagement_type)
- `field_event_content_rsvp_driven` (properties: event_slug, city, content_piece_id)

Measure: which content types drive the most engagement? Which content pieces drive RSVPs for the next event? Feed these findings into the `ab-test-orchestrator` or `autonomous-optimization` drills to improve content strategy over time.

## Output

- Structured insights record per event in Attio
- Updated attendee intelligence in Attio contact records
- 3-4 content pieces produced and published per event
- Content performance tracked in PostHog
- Content assets tagged and stored for use in future event promotion

## Triggers

- Start within 2 hours of event completion (host debrief)
- Content production: within 48 hours of event
- Content publication: spread over 1-2 weeks post-event
- Run once per event
