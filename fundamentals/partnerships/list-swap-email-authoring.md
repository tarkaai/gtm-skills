---
name: list-swap-email-authoring
description: Generate a full standalone email to send to a partner's email list as part of a list swap
tool: Anthropic
product: Claude API
difficulty: Setup
---

# List Swap Email Authoring

Write a complete, standalone email designed to be sent directly to a partner's subscriber list. Unlike a newsletter blurb (which is embedded inside the partner's own email), a list swap email is its own message — sent by the partner on your behalf or co-branded. The email must feel native to the partner's audience while driving clicks to your landing page.

## Prerequisites

- Partner newsletter audit completed (tone, audience persona, format)
- Partner agreement on swap terms: you send to their list, they send to yours
- Landing page URL with PostHog tracking installed
- Anthropic API key for Claude-powered copywriting

## Steps

1. **Gather context.** Collect before writing:
   - Partner company name and newsletter name
   - Partner audience persona: job titles, industries, pain points, sophistication level
   - Partner newsletter tone: casual, formal, technical, conversational
   - 2-3 recent partner newsletter emails (for voice matching)
   - Your value proposition tailored to their audience
   - Landing page URL for this swap
   - Any partner constraints: max word count, required disclaimers, image guidelines, from-name/from-address rules

2. **Build UTM-tracked links.** Every link in the swap email must include UTM parameters:

   ```
   {base_url}?utm_source={partner_slug}&utm_medium=list-swap&utm_campaign=list-swaps-adjacent-startups&utm_content={variant_id}
   ```

   Example: `https://yourproduct.com/demo?utm_source=acme-tools&utm_medium=list-swap&utm_campaign=list-swaps-adjacent-startups&utm_content=curiosity-v1`

3. **Generate the email using Claude.** Call the Anthropic API:

   ```
   POST https://api.anthropic.com/v1/messages
   Authorization: Bearer {ANTHROPIC_API_KEY}
   Content-Type: application/json

   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 2048,
     "messages": [{
       "role": "user",
       "content": "Write a standalone email (200-400 words) to be sent to {partner_newsletter_name}'s subscriber list as part of an email list swap.\n\nPartner audience: {audience_description}\nPartner tone: {tone}\nOur product: {product_description}\nValue prop for their audience: {value_prop}\nCTA URL: {landing_page_url}\n\nRules:\n- Subject line: specific and curiosity-driven, under 60 characters\n- Preview text: complement (don't repeat) the subject line, under 90 characters\n- Open with a pain point or question the reader recognizes immediately\n- Body: 2-3 short paragraphs, scannable, mobile-friendly\n- Include one specific data point or proof point (stat, customer result, benchmark)\n- One primary CTA button/link — do not dilute with multiple CTAs\n- Close with a low-commitment ask (e.g., 'See how it works in 2 minutes' not 'Book a 30-minute demo')\n- Tone must match the partner's voice, not yours\n- No hype words: revolutionary, game-changing, cutting-edge, etc.\n- Include a brief 'Who is {your_company}?' line (1 sentence max) at the bottom\n\nGenerate 3 variants:\n- Variant A: curiosity-driven (open loop)\n- Variant B: data-driven (lead with a stat)\n- Variant C: story-driven (mini scenario)\n\nFor each variant, output: subject_line, preview_text, body_html, body_plain_text."
     }]
   }
   ```

4. **Validate the email.** Before sending to partner for approval, verify:
   - Subject line is under 60 characters
   - Preview text is under 90 characters
   - Total word count is within partner constraints
   - CTA link works and UTM parameters fire in PostHog
   - No jargon the partner's audience would not understand
   - The email reads as a recommendation, not a cold ad
   - Unsubscribe link handling is clarified with the partner (their unsubscribe, not yours)
   - CAN-SPAM / GDPR compliance: the partner is the sender of record

5. **Send to partner for approval.** Email the top variant to the partner contact. Include:
   - Subject line and preview text
   - Plain-text version (for copy-pasting)
   - HTML version (if they want formatted layout)
   - The tracked CTA link — ask them not to modify it
   - Any image/logo assets (2x resolution PNG)
   - A note: "Adjust wording for your voice — the CTA link is the only thing that needs to stay as-is"

6. **Archive the approved version.** Store in your CRM (Attio) linked to the partner record: subject line, body, variant used, swap date, and CTA URL. This builds a library for reuse and A/B testing.

## Error Handling

- If Claude produces generic copy, add 2-3 paragraphs from the partner's recent newsletters as few-shot examples in the prompt
- If the partner rejects all variants, request a past sponsored/partner email they liked and use it as a structural template
- If UTM parameters break the URL, URL-encode all parameter values
- If the partner requires HTML email format, use a clean single-column layout with inline CSS (no external stylesheets)

## Alternative Tools

- **OpenAI GPT-4o**: Alternative LLM for email generation
- **Jasper**: Marketing-focused AI copywriter with email templates
- **Copy.ai**: Short-form marketing copy specialist
- **Beehiiv**: If the partner uses Beehiiv, they may have a built-in swap/recommendation feature
- **SparkLoop**: Newsletter recommendation platform that automates swap logistics
