---
name: podcast-pitch-email
description: Send personalized podcast guest pitch emails to hosts via Instantly or manual send
tool: Instantly / Gmail
difficulty: Config
---

# Podcast Pitch Email

Craft and send personalized pitch emails to podcast hosts requesting a guest appearance for your founder.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| Instantly | Automated sequence with merge fields | Pitching 10+ hosts at Baseline/Scalable |
| Gmail / Workspace | Manual send from founder's address | Smoke test (5-10 pitches), high-priority targets |
| Smartlead | Automated with inbox rotation | High-volume outreach at Scalable |
| Mailshake | Email + social touchpoints | Multi-channel sequences |

## Pitch Email Copy Framework

### Email 1 — The Pitch (Day 0)

```
Subject: Guest idea for {{podcast_name}}: {{pitch_angle_short}}

Hi {{host_first_name}},

I listened to your episode with {{recent_guest_name}} on {{recent_episode_topic}} — {{specific_observation_about_episode}}.

I'm {{founder_name}}, founder of {{company}}. We {{one_line_what_company_does}}.

I'd love to come on {{podcast_name}} to talk about {{pitch_topic}}. Specifically:

- {{talking_point_1}}
- {{talking_point_2}}
- {{talking_point_3}}

{{social_proof_line — e.g., "I've spoken at X, been on Y podcast, wrote about Z"}}

Happy to send over a one-sheet with my bio and episode angle if helpful.

{{founder_name}}
```

Rules:
- Under 150 words
- Reference a specific episode to show you actually listen
- 3 concrete talking points (not vague "I can talk about growth")
- One line of social proof
- No attachments in first email

### Email 2 — Follow-up (Day 5)

```
Subject: Re: Guest idea for {{podcast_name}}: {{pitch_angle_short}}

Hi {{host_first_name}},

Following up on my note about coming on {{podcast_name}}. I thought of another angle that might fit: {{alternative_angle}}.

If the timing isn't right, no worries at all — I know you're busy. Would love to connect for a future season too.

{{founder_name}}
```

Rules:
- Offer a different angle (shows flexibility)
- Give an easy out (reduces pressure, increases reply rate)
- Maximum 2 follow-ups total (podcast hosts get pitched constantly; 3+ emails = spam)

### Email 3 — Final bump (Day 12)

```
Subject: Re: Guest idea for {{podcast_name}}: {{pitch_angle_short}}

{{host_first_name}}, last note from me on this. If any of these topics fit a future episode, I'm easy to book: {{calendar_link}}.

Happy to be a resource even without a guest spot — feel free to reach out if you need a quote or perspective on {{topic_area}}.

{{founder_name}}
```

## Instantly Setup

### Create the campaign

Using the `instantly-campaign` fundamental:

1. Create a new campaign named `podcast-guesting-{date}`
2. Upload the enriched host list from Clay
3. Map merge fields: `host_first_name`, `podcast_name`, `recent_guest_name`, `recent_episode_topic`, `specific_observation_about_episode`, `pitch_topic`, `talking_point_1-3`
4. Set sending schedule: Tue-Thu, 9am-11am in host's timezone (podcast hosts often record mid-week)
5. Daily send limit: 10 per account (low volume, high personalization)
6. Enable reply detection

### Reply handling

- **Positive** (interested, send more info, let's schedule): Move to Attio, tag "podcast-booked", send one-sheet
- **Soft positive** (not now, maybe next quarter): Tag "podcast-nurture", add to quarterly re-pitch list
- **Negative** (not interested, not booking guests): Tag "podcast-declined", do not re-pitch
- **Booking form redirect** (they ask you to fill out their form): Flag for manual form submission

## Manual Send (Smoke Test)

For the first 5-10 pitches, send from the founder's personal Gmail or Workspace account. This is higher-trust (personal domain, not a sales tool) and appropriate for Smoke test volume. Copy the pitch framework above, personalize each one by hand, and track in a spreadsheet or Attio.

## Error Handling

- **Bounce**: Remove from list, try alternate contact method (Twitter DM, LinkedIn)
- **No reply after 3 emails**: Mark as "no response" — do not re-pitch for 6 months
- **Out of office**: Pause the sequence and restart when they return
- **"We don't take pitches"**: Respect it. Remove permanently.
