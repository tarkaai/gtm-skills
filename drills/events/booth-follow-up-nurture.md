---
name: booth-follow-up-nurture
description: Execute segmented post-conference follow-up sequences based on booth lead tier to maximize meeting conversion
category: Events
tools:
  - Loops
  - Attio
  - n8n
  - Loom
  - PostHog
fundamentals:
  - loops-sequences
  - attio-deals
  - attio-contacts
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# Booth Follow-Up Nurture

This drill builds the post-conference follow-up system that converts booth leads into meetings and pipeline. The key insight: conference leads decay fast. A lead that was excited at your booth on Tuesday has forgotten you by the following Monday. Speed and personalization by tier are everything.

## Input

- Booth lead data in Attio (from `booth-lead-capture` drill): contacts with tier, notes, and agreed next steps
- Conference debrief notes
- Demo recording or product screenshots for email attachments
- Cal.com booking link

## Steps

### 1. Segment leads for follow-up routing

Within 12 hours of the conference ending, build follow-up segments in Attio using `attio-contacts`:

- **Tier 1 (Hot)**: Meeting already booked OR agreed to follow-up demo. Expected: 5-15% of total scans.
- **Tier 2 (Warm)**: Relevant pain point, interested, agreed to receive follow-up material. Expected: 15-25% of total scans.
- **Tier 3 (Curious)**: Stopped by the booth, general interest, no specific pain point. Expected: 30-40% of total scans.
- **Tier 4 (Not ICP)**: No follow-up. Do not email. Expected: 20-30% of total scans.

Using `n8n-triggers`, create a webhook that fires when a new conference lead is tagged in Attio with an interest tier, routing them into the correct Loops sequence.

### 2. Build Tier 1 (Hot) follow-up — personal, same-day

Timing: within 12 hours of the booth conversation.

This is NOT an automated sequence — it is a personal email that the agent drafts and the rep sends.

For each Tier 1 contact:

1. Draft a personal email referencing the specific conversation at the booth:
   ```
   Subject: Following up from {Conference} — {specific topic discussed}

   {First name}, great meeting you at the {Conference} booth {today/yesterday}.

   You mentioned {specific pain point from booth notes}. Here is {specific
   resource: case study, demo recording clip, or documentation link} that
   addresses exactly that.

   {If meeting already booked}: Looking forward to our call on {date}. I will
   prepare a demo focused on {their use case}.

   {If meeting not yet booked}: Want to pick up where we left off? Here is my
   calendar: {Cal.com link}
   ```
2. If the agent has Loom access, record a 60-second personalized video recap: "Hey {name}, this is {rep} from the {conference} booth. You asked about {pain point} — here is the quick walkthrough I promised." Attach via `loom-embed-in-email`.
3. Log the follow-up in Attio. Update the contact's last-touch date.
4. Fire `booth_followup_sent` in PostHog with properties: conference_name, tier: 1, has_loom: true/false

### 3. Build Tier 2 (Warm) follow-up — semi-personal, within 48 hours

Using `loops-sequences`, create a 3-email sequence triggered by the n8n webhook when a lead is tagged Tier 2:

**Email 1 (Day 1 post-conference):**
```
Subject: {Conference} recap + the {topic} resource you asked about

{First name}, good to connect at {Conference}.

You mentioned interest in {topic from booth notes}. Here is {specific resource:
case study, blog post, demo video} that goes deeper.

If you want to see how this applies to {their company}, I can do a quick
15-minute walkthrough: {Cal.com link}
```

**Email 2 (Day 4):**
```
Subject: Quick question from {Conference}

{First name}, one thing I did not get to show you at the booth: {specific
feature or capability relevant to their pain point}.

Here is a 2-minute overview: {product page or Loom link}

Worth a quick call? {Cal.com link}
```

**Email 3 (Day 8):**
```
Subject: Last note from {Conference}

{First name}, wrapping up my {Conference} follow-ups. If {pain point} is still
on your radar, happy to jump on a quick call anytime.

{Cal.com link}

Either way, was great meeting you.
```

4. Fire PostHog events at each step: `booth_nurture_email_sent` with properties: conference_name, tier: 2, sequence_step, contact_email

### 4. Build Tier 3 (Curious) follow-up — automated, lightweight

Using `loops-sequences`, create a single-email follow-up:

**Email 1 (Day 2 post-conference):**
```
Subject: Thanks for stopping by at {Conference}

{First name}, thanks for visiting our booth at {Conference}.

Here is a quick overview of what we do: {product landing page URL}

If {general problem area} is something your team is tackling, we would love to
show you more: {Cal.com link}
```

No multi-email sequence for Tier 3. One touch is enough. If they do not engage, add them to your general marketing nurture list in Loops.

### 5. Monitor follow-up performance

Using `posthog-custom-events`, track the full follow-up funnel:

- `booth_followup_sent` — properties: conference_name, tier, sequence_step
- `booth_followup_opened` — properties: conference_name, tier, sequence_step
- `booth_followup_replied` — properties: conference_name, tier, reply_sentiment
- `booth_followup_meeting_booked` — properties: conference_name, tier, days_since_conference
- `booth_followup_deal_advanced` — properties: conference_name, tier, new_stage

Build an n8n workflow using `n8n-triggers` that watches for replies:
- Positive reply from Tier 2 → auto-create Attio deal using `attio-deals`, notify rep via Slack
- Meeting booked → update Attio contact and deal, fire PostHog event
- Negative reply or unsubscribe → remove from sequence, update Attio status

### 6. Post-conference ROI calculation (14 days after event)

14 days after the conference, compile:

| Metric | Value |
|--------|-------|
| Total badge scans | ? |
| Tier 1 leads | ? |
| Tier 2 leads | ? |
| Meetings booked (total) | ? |
| Deals created | ? |
| Pipeline value generated | ? |
| Sponsorship cost | ? |
| Cost per qualified lead (Tier 1+2) | ? |
| Cost per meeting | ? |

Log the ROI calculation in Attio as a note on the conference record. Fire `booth_conference_roi_calculated` in PostHog with all metrics.

## Output

- Tier-segmented follow-up sequences launched within 48 hours of conference end
- Personal follow-ups drafted and sent for Tier 1 contacts
- Automated sequences running for Tier 2-3 contacts
- Deals created from positive replies
- 14-day post-conference ROI report

## Triggers

- Tier 1 follow-up: within 12 hours of conference end
- Tier 2 sequence: starts Day 1 post-conference, runs 8 days
- Tier 3 email: Day 2 post-conference
- ROI calculation: 14 days post-conference
