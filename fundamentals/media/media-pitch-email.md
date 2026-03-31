---
name: media-pitch-email
description: Craft and send personalized pitch emails to journalists and newsletter editors for earned coverage
tool: Instantly / Gmail / Smartlead
difficulty: Config
---

# Media Pitch Email

Craft and send personalized pitch emails to journalists and newsletter editors requesting coverage, a guest article slot, or a mention. Media pitches differ from sales emails -- they must lead with the story, not the product.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| Gmail / Workspace | Manual send from founder's address | Smoke test (5-10 pitches), top-tier journalists |
| Instantly | Automated sequence with merge fields | Pitching 15+ contacts at Baseline/Scalable |
| Smartlead | Automated with inbox rotation | High-volume outreach at Scalable |
| Mailshake | Email + social touchpoints | Multi-channel press outreach |

## Pitch Email Copy Framework

### Email 1 -- The Pitch (Day 0)

```
Subject: {{pitch_angle_short}} -- data for your {{beat}} coverage

Hi {{journalist_first_name}},

I read your piece on {{recent_article_topic}} in {{outlet_name}} -- {{specific_observation}}.

I have a story that fits your beat: {{pitch_angle_one_sentence}}.

The hook: {{compelling_data_point_or_stat}}.

I can provide:
- {{asset_1}} (e.g., "exclusive data from our analysis of 500 companies")
- {{asset_2}} (e.g., "a customer willing to go on record about results")
- {{asset_3}} (e.g., "a contrarian take on why the conventional approach fails")

Happy to share more detail or jump on a 10-minute call.

{{founder_name}}
{{company}} -- {{one_liner}}
```

Rules:
- Under 150 words
- Reference a specific recent article they wrote (proves you read their work)
- Lead with the story angle, not your product
- Offer concrete assets (data, sources, exclusive access)
- No attachments in first email
- Do NOT use "I'd love to introduce you to..." or "Have you heard of..."

### Email 2 -- Follow-up with new angle (Day 5)

```
Subject: Re: {{pitch_angle_short}} -- data for your {{beat}} coverage

Hi {{journalist_first_name}},

Quick follow-up. I noticed {{recent_industry_news_or_trend}} this week -- our data shows {{relevant_insight_tied_to_news}}.

If you're covering this, I can provide {{specific_asset_or_quote}}.

No worries if it doesn't fit right now.

{{founder_name}}
```

Rules:
- Tie follow-up to a current news event (makes the pitch timely)
- Offer something concrete they can use immediately
- One follow-up maximum for journalists. They get 100+ pitches/day.

### Newsletter-Specific Pitch Variant

For newsletter editors, adapt the pitch:

```
Subject: Story idea for {{newsletter_name}}: {{angle}}

Hi {{editor_first_name}},

I'm a subscriber -- I especially liked your recent issue on {{recent_topic}}.

I have a piece that could work for {{newsletter_name}}: {{pitch_angle}}.

Key points:
- {{point_1}}
- {{point_2}}
- {{point_3}}

I can write a full draft ({{word_count}} words) or just share the data for you to write up.

{{founder_name}}
```

Newsletter editors prefer pre-written content or rich data they can repurpose. Offer both options.

## Instantly Setup

Using the `instantly-campaign` fundamental:

1. Create campaign: `media-outreach-{date}`
2. Upload enriched media list from Clay
3. Map merge fields: `journalist_first_name`, `outlet_name`, `recent_article_topic`, `specific_observation`, `pitch_angle_short`, `pitch_angle_one_sentence`, `compelling_data_point_or_stat`
4. Sending schedule: Tue-Thu, 7am-9am in journalist's timezone (journalists check email early)
5. Daily send limit: 15 per account (media outreach = low volume, high personalization)
6. Enable reply detection
7. Set 1 follow-up maximum (not 3 like sales sequences)

## Reply Handling

- **"Send me more info"**: Reply with a press kit link, key data points, and offer a brief call. Update Attio: status = "interested"
- **"I'll cover this"**: Provide everything they need immediately: quotes, data, images, customer contacts. Update Attio: status = "covering"
- **"Not for me, try [colleague]"**: Thank them, pitch the referred journalist. Update Attio: status = "referred"
- **"Not right now"**: Ask if you can re-pitch when you have new data/news. Update Attio: status = "nurture"
- **"Unsubscribe / stop"**: Remove permanently. Never re-pitch.
- **No reply after 2 emails**: Mark "no response". Re-pitch in 3 months with a completely different angle.

## Personalization Requirements by Volume

| Level | Volume | Personalization |
|-------|--------|----------------|
| Smoke | 5-10 | Hand-written, reference specific article, unique per journalist |
| Baseline | 15-30 | Template with 3+ merge fields per email, each reviewed before send |
| Scalable | 50+ | Template with merge fields from Clay enrichment, tier-based personalization depth |

## Error Handling

- **Bounce**: Journalist may have changed outlets. Check LinkedIn for current role, find new email.
- **Auto-reply "on assignment"**: Pause sequence, re-send when they return.
- **"I already covered this"**: Thank them, ask if they'd be interested in a follow-up angle when you have new data.
- **Spam filter**: Media pitches from new domains often land in spam. At Smoke, always send from founder's established personal email domain.
