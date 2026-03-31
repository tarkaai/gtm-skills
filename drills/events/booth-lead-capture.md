---
name: booth-lead-capture
description: Execute booth operations at conferences with structured lead capture, real-time qualification, and same-day CRM enrichment
category: Events
tools:
  - Attio
  - Cal.com
  - PostHog
  - Clay
fundamentals:
  - badge-scan-lead-import
  - attio-contacts
  - attio-deals
  - calcom-booking-links
  - posthog-custom-events
  - clay-enrichment-waterfall
---

# Booth Lead Capture

This drill covers execution-day booth operations: how to capture, qualify, and route leads during a conference. It turns badge scans and booth conversations into structured pipeline data the same day.

## Input

- Conference sponsorship details (from `conference-sponsorship-pipeline` drill): booth number, tier, lead retrieval access
- Pre-event target list in Attio (high-priority attendees to seek out)
- Demo environments loaded on laptop + tablet
- Badge scanner or manual lead capture form ready
- Cal.com booking link with QR code printed

## Steps

### 1. Booth setup and systems check (morning of event)

Before the conference floor opens:

1. Test the lead retrieval system — scan a test badge (your own) and verify data appears in the app or exports correctly
2. Confirm demo environments load and work on venue WiFi. Have mobile hotspot as backup.
3. Position QR codes visibly: Cal.com booking link on the table, product trial link on the banner or screen
4. Open the pre-event target list on a tablet so booth staff can reference it throughout the day
5. Brief all booth staff on the qualification framework:

**Qualification tiers (assign during or immediately after each conversation):**

- **Tier 1 (Hot)**: Has budget, active project, timeline within 3 months, decision maker or strong champion. Agreed to a demo or follow-up meeting.
- **Tier 2 (Warm)**: Relevant pain point, interested but no active project or timeline. Wants to learn more. Open to follow-up.
- **Tier 3 (Curious)**: Browsing the booth, asked general questions, no clear pain point or project. Took collateral.
- **Tier 4 (Not ICP)**: Student, job seeker, vendor, or company outside your ICP. Polite interaction, no follow-up needed.

### 2. Booth conversation execution

**Opening framework** (do not lead with a pitch):

1. **Observe and open**: Watch what catches the visitor's eye on your booth display. "What caught your attention?" or "What are you working on that brought you to {conference}?"
2. **Listen for pain signals**: Let them describe their situation. If they mention anything your product addresses, that is your opening.
3. **Qualify quickly**: Ask 2-3 questions to place them in a tier: "Are you currently using anything for {problem area}?" / "What does your team look like for this?" / "Is this something you are actively solving or exploring?"
4. **Demo if appropriate**: For Tier 1-2, offer a demo matched to their interest: "Let me show you exactly how we handle that — 2 minutes." Do not demo for Tier 3-4.
5. **Close with a specific next step**:
   - Tier 1: Book a meeting on the spot via Cal.com QR code. "Let's get 30 minutes on the calendar while we are both here."
   - Tier 2: Agree on a follow-up method: "I'll send you {specific resource} tomorrow — what email should I use?"
   - Tier 3: "Here is our site — check out {specific page} when you get a chance."
   - Tier 4: Thank them, move on.

### 3. Real-time lead logging

After each meaningful conversation, immediately log it. Do not batch — memory degrades after 3+ conversations.

Using the `badge-scan-lead-import` fundamental:

- If using conference badge scanner: scan the badge, then add notes in the lead retrieval app (interest level, key pain point mentioned, agreed next step, demo given yes/no)
- If using manual form (Tally/Typeform): log name, email, company, title, interest tier, notes, next step agreed

**Minimum fields per lead:**
- Name and email (or LinkedIn if email not captured)
- Company and title
- Interest tier (1-4)
- Key pain point mentioned (1-2 sentences)
- Next step agreed (meeting booked, follow-up email, trial signup, none)
- Demo given (yes/no, which track)

### 4. Same-day CRM enrichment (evening after each day)

Within 4 hours of the conference floor closing:

1. Export all badge scan data from the lead retrieval platform (CSV or API)
2. Run the `badge-scan-lead-import` fundamental to import into Attio:
   - Create or update a contact record for every person scanned
   - Attach: conversation notes, interest tier, demo given, agreed next step
   - Tag with conference name and date as source
3. For Tier 1 and 2 leads, run `clay-enrichment-waterfall` to fill in missing data: LinkedIn URL, company size, funding stage, tech stack
4. Using `attio-deals`, create deals for Tier 1 contacts:
   - Deal name: "{Company} — {Conference Name}"
   - Stage: "Meeting Requested" (if booked) or "Qualified Lead" (if follow-up agreed)
   - Source: conference-booth-sponsorship
   - Attach booth conversation notes
5. Using `attio-contacts`, update all Tier 2 contacts with a next-step task for follow-up

### 5. Track booth performance metrics

Using `posthog-custom-events`, fire events for the full booth funnel:

- `booth_badge_scanned` — properties: conference_name, day, interest_tier
- `booth_demo_given` — properties: conference_name, demo_track, duration_minutes, interest_tier
- `booth_meeting_booked` — properties: conference_name, days_to_meeting, interest_tier
- `booth_deal_created` — properties: conference_name, deal_value_estimate, interest_tier
- `booth_day_summary` — properties: conference_name, day, total_scans, tier1_count, tier2_count, demos_given, meetings_booked

Fire `booth_day_summary` at the end of each conference day for daily performance tracking.

### 6. End-of-conference debrief

After the last day of the conference:

1. Compile total lead counts by tier
2. Calculate: total badge scans, % qualified (Tier 1+2), demos given, meetings booked, deals created
3. Identify: which demo track resonated most, which pain points came up repeatedly, any competitive intelligence gathered (what competitors were showing, what attendees said about them)
4. Log the debrief in Attio as a note on the conference record
5. Fire `booth_conference_completed` event in PostHog with all summary metrics

## Output

- All booth leads imported to Attio with tier, notes, and next steps
- Deals created for Tier 1 contacts
- Enrichment completed for Tier 1-2 contacts
- PostHog event trail for the full booth funnel
- Conference debrief with competitive intelligence and pain point patterns

## Triggers

- Run once per conference attended
- Same-day CRM enrichment must execute within 4 hours of booth closing each day
- End-of-conference debrief within 24 hours of last day
