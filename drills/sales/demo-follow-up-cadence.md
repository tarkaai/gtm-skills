---
name: demo-follow-up-cadence
description: Execute a structured multi-touch follow-up cadence after demo recap, delivering value assets timed to deal context
category: Sales
tools:
  - Attio
  - Instantly
  - Loops
  - Loom
  - PostHog
  - Cal.com
fundamentals:
  - attio-deals
  - attio-notes
  - attio-contacts
  - instantly-campaign
  - instantly-tracking
  - instantly-reply-detection
  - loops-sequences
  - loom-analytics
  - posthog-custom-events
  - calcom-booking-links
---

# Demo Follow-Up Cadence

This drill executes a structured post-demo follow-up sequence. Unlike cold outreach cadences, these touches are warm — the prospect has seen the product. Each touch delivers specific value tied to what happened in the demo, not generic nurture content.

## Input

- Demo recap assembled (from `demo-recap-assembly` drill): deal_id, features_covered, questions_addressed, concerns, suggested_next_step, urgency_level
- Deal record in Attio with demo signals populated
- Prospect contact in Attio with email verified
- Product resource library accessible as URLs

## Steps

### 1. Send the recap email (Hour 0 — within 2 hours of demo)

Retrieve the recap email from the Attio note created by `demo-recap-assembly`.

**Human action required:** Review the AI-generated recap for accuracy. Check that feature descriptions match what was actually shown and that question answers are correct. Edit if needed. Send from the founder's personal email (not a sequence tool) for authenticity.

After sending, update Attio using `attio-deals`:
- `demo_recap_sent`: true
- `demo_recap_sent_at`: timestamp
- `follow_up_sequence_status`: "active"

Fire a PostHog event:
```json
{
  "event": "demo_follow_up_sent",
  "properties": {
    "deal_id": "...",
    "touch_number": 0,
    "touch_type": "recap",
    "channel": "email",
    "personalized": true
  }
}
```

### 2. Check-in email (Day 1)

Send a brief check-in 24 hours after the recap:

```
Subject: Re: {original recap subject}

{first_name}, just checking if the recap and resources were helpful.

Any questions come up since our call? Happy to dig into anything that wasn't clear.

{if unanswered_questions > 0: "I also looked into {unanswered_question} — here's what I found: {answer}"}

{sender_name}
```

If the prospect opened the recap email but didn't reply (check via `instantly-tracking` or email open data), this touch is especially important. If they haven't opened it at all, change the subject line to stand out:

```
Subject: Quick follow-up on our {product_name} conversation
```

Log in Attio and fire PostHog event with `touch_number: 1`, `touch_type: check_in`.

### 3. Value asset delivery (Day 3)

Select a resource matched to the demo context. Use the `attio-notes` data from the recap to pick the right asset:

| Demo Context | Asset to Send |
|-------------|---------------|
| Asked technical integration questions | Integration guide or API docs |
| Mentioned other stakeholders need to see it | One-page executive summary or shareable Loom video |
| Showed interest in a specific use case | Case study from similar company/industry |
| Raised security or compliance concerns | Security whitepaper or compliance documentation |
| Discussed pricing or ROI | ROI calculator pre-filled with their numbers |
| Mentioned a competitor | Comparison page or migration guide |

Draft the email:
```
Subject: {asset_title} — thought this would be helpful

{first_name}, based on {specific_demo_moment}, I thought you'd find this useful:

{asset_link_with_description}

{if stakeholders_mentioned: "If you're sharing with {stakeholder_name}, there's a section on {relevant_topic} that covers their likely questions."}

Let me know what you think.

{sender_name}
```

Use `instantly-tracking` to add tracking to asset links. Log as `touch_number: 2`, `touch_type: value_asset`.

### 4. Engagement-based touch (Day 5-7)

Before sending this touch, check engagement signals:

Using `loom-analytics`, check if the prospect watched the recap video (if one was sent). Using `instantly-tracking`, check if they clicked the asset link from Day 3.

**If high engagement (video watched >50% OR asset clicked):**
Accelerate — propose the next step directly:
```
Subject: Next step: {suggested_next_step}

{first_name}, I noticed you've been reviewing the materials.

Based on our demo conversation, the natural next step would be {suggested_next_step_description}. I've blocked a few times next week: {calcom_link}

{sender_name}
```

**If low engagement (no opens, no clicks):**
Try a different angle. Reference something from the demo that was NOT in previous follow-ups:
```
Subject: One thing I forgot to mention

{first_name}, I realized I didn't cover {overlooked_feature_or_benefit} during our demo. It's actually one of the things {similar_company} found most valuable.

Worth a quick follow-up? {calcom_link}

{sender_name}
```

Log as `touch_number: 3`, `touch_type: engagement_based`.

### 5. Momentum check (Day 10)

If no response to any previous touch:
```
Subject: Still relevant, {first_name}?

{first_name}, I know things get busy. Quick question — is {solving_their_primary_pain} still a priority this quarter?

If so, I'd love to pick up where we left off. If timing has shifted, no worries at all — just let me know and I'll follow up when it makes sense.

{calcom_link}

{sender_name}
```

If they responded positively to any previous touch but haven't booked a next step:
```
Subject: Locking in next steps

{first_name}, glad the {asset/recap/video} was helpful. To keep momentum going, want to get {suggested_next_step} on the calendar?

Here are a few openings: {calcom_link}

{sender_name}
```

Log as `touch_number: 4`, `touch_type: momentum_check`.

### 6. Handle sequence exits

Using `instantly-reply-detection`, monitor for replies at every stage:

- **Positive reply (books meeting, asks question, requests proposal):** Pause the sequence. Update Attio deal stage. Log `follow_up_sequence_completed` with `outcome: next_step_booked`.
- **Neutral reply (acknowledged but no commitment):** Continue the sequence but adjust timing — add 2 extra days between remaining touches.
- **Negative reply (not interested, bad timing, chose competitor):** Stop the sequence. Update Attio deal to appropriate status. Log `follow_up_sequence_completed` with `outcome: {reason}`.
- **No response after all touches:** Mark the sequence as complete. Set a 30-day re-engagement reminder in Attio. Log `follow_up_sequence_completed` with `outcome: no_response`.

### 7. Track cadence performance

Using `posthog-custom-events`, fire events at every touch point. After completing sequences on 8+ demos, analyze:

- Which touch number generates the most replies (identify the "magic touch")
- Which value asset types drive the most engagement
- Average touches to next-step booking
- Sequence completion rate vs early exit rate
- Response rate by urgency level

Store the analysis as an Attio campaign note.

## Output

- 5-touch post-demo follow-up sequence executed per deal
- Engagement-reactive touch selection (not just time-based)
- Attio deal records updated at every touch
- PostHog events for full sequence analytics
- Cadence performance data for optimization

## Triggers

Starts immediately after `demo-recap-assembly` completes. Each subsequent touch fires on schedule (Day 1, 3, 5-7, 10) unless a response triggers an early exit.
