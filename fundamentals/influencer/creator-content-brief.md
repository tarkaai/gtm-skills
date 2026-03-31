---
name: creator-content-brief
description: Generate and send a structured content brief to a creator for a sponsored post
tool: Notion
difficulty: Config
---

# Creator Content Brief

After a creator agrees to a sponsored post, send them a structured brief. The brief tells them what to create without micromanaging their voice. Good briefs produce better content and fewer revision cycles.

## Brief Structure

Every creator brief contains these sections:

### 1. Campaign Overview
- **Brand:** Your company name and one-line description
- **Product/Service:** What you want them to mention
- **Goal:** What you want the audience to do (visit a URL, sign up, book a demo)
- **Target audience:** Who in their audience you are trying to reach (job titles, pain points)

### 2. Key Messages (Pick 1-2, Never 5+)
- **Primary message:** The ONE thing the audience should take away
- **Supporting point:** One proof point, stat, or example that supports the primary message
- **Tone guidance:** Match their voice. Do NOT ask them to sound like your marketing copy.

### 3. Requirements
- **Format:** LinkedIn post, newsletter mention, YouTube mention, tweet thread, Instagram story
- **Length:** Approximate (e.g., "300-500 words for a LinkedIn post" or "60-second mention in video")
- **Tracking link:** Provide a UTM-tagged URL for the creator to include. Format: `https://yoursite.com/landing?utm_source={{creator_handle}}&utm_medium=influencer&utm_campaign={{campaign_slug}}`
- **Disclosure:** FTC requires clear disclosure of paid partnerships. Include "#ad" or "#sponsored" or "Paid partnership with [Brand]". Non-negotiable.
- **Posting window:** Date range when the post should go live
- **Approval process:** Whether you want to review a draft before publishing (recommended for Smoke test, optional at scale)

### 4. What NOT to Do
- Do NOT provide a script. Creators know their audience better than you do.
- Do NOT ask for more than 2 key messages. Overloaded briefs produce generic content.
- Do NOT require specific phrasing or taglines. Let the creator translate your message into their voice.
- Do NOT restrict the creator's format choices beyond the agreed type.

## Generating the Brief

Use Claude to draft the brief from your campaign parameters:

```
Prompt: Generate a creator sponsorship brief.

Brand: {{company_name}}
Product: {{product_description}}
Creator: {{creator_name}} ({{platform}}, {{follower_count}} followers, topic: {{creator_topic}})
Goal: {{campaign_goal}}
Format: {{post_format}}
Tracking URL: {{utm_url}}
Post window: {{date_range}}
Budget: {{agreed_price}}

Write a brief that:
1. Gives the creator clear direction without micromanaging
2. Includes exactly 1 primary message and 1 supporting point
3. Specifies the tracking link and disclosure requirement
4. Fits on one page
```

## Sending the Brief

### Option 1: Email via Instantly or Loops

Send the brief as a formatted email. Include the tracking link as a clickable URL. Attach any brand assets (logo, screenshots) if the creator needs them.

### Option 2: Attio Note

Store the brief as an Attio note on the creator's contact record. Use the `attio-notes` fundamental to create the note. This keeps all creator communications in CRM.

```
POST https://api.attio.com/v2/notes
Authorization: Bearer {ATTIO_API_KEY}
Content-Type: application/json

{
  "parent_object": "people",
  "parent_record_id": "{{creator_attio_record_id}}",
  "title": "Sponsorship Brief — {{campaign_slug}}",
  "content": "{{brief_content_markdown}}"
}
```

### Option 3: Passionfroot Brief Field

If using Passionfroot, paste the brief into the booking's brief field when purchasing the slot.

## Error Handling

- **Creator asks for changes to the brief:** Accommodate reasonable requests. The creator knows what works with their audience.
- **Creator misses the posting window:** Send a reminder 2 days before the deadline. If they still miss it, negotiate a new date. Do not demand refunds for minor delays.
- **Creator deviates from the brief:** If the core message and tracking link are present, accept it. If the tracking link is missing, ask them to edit the post to add it — you cannot measure ROI without it.
