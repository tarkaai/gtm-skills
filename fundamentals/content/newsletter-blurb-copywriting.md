---
name: newsletter-blurb-copywriting
description: Write a short co-marketing blurb optimized for placement in a partner's newsletter
tool: Anthropic
product: Claude API
difficulty: Setup
---

# Newsletter Blurb Copywriting

## Prerequisites
- Partner newsletter audit completed (know their tone, audience, format)
- Clear value proposition for the partner's audience
- Landing page URL with UTM parameters ready
- Anthropic API key for Claude-powered copywriting

## Steps

1. **Gather context for the blurb.** Before writing, collect:
   - Partner newsletter name and typical tone (formal/casual/technical)
   - Their audience persona (title, industry, pain points)
   - 2-3 example blurbs or ads from their previous newsletters (if available)
   - Your value proposition tailored to their audience
   - The landing page URL you want to drive traffic to
   - Any format constraints from the partner (word count, image allowed, CTA style)

2. **Generate the blurb using Claude.** Call the Anthropic API with a structured prompt:

   ```
   POST https://api.anthropic.com/v1/messages
   Authorization: Bearer {ANTHROPIC_API_KEY}
   Content-Type: application/json

   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 1024,
     "messages": [{
       "role": "user",
       "content": "Write a co-marketing newsletter blurb (60-100 words) for placement in {partner_newsletter_name}.\n\nPartner audience: {audience_description}\nPartner tone: {tone}\nOur product: {product_description}\nValue prop for their audience: {value_prop}\nCTA URL: {landing_page_url}\n\nRules:\n- Match the partner's voice and tone\n- Lead with the reader's pain point, not our product\n- One clear CTA (not multiple)\n- No superlatives or hype words\n- Include a specific, concrete benefit\n- Keep under 100 words\n\nGenerate 3 variants: one curiosity-driven, one data-driven, one story-driven."
     }]
   }
   ```

3. **Add UTM tracking to the CTA link.** Every blurb link must include UTM parameters for attribution:

   ```
   {base_url}?utm_source={partner_slug}&utm_medium=newsletter&utm_campaign=co-marketing-shoutouts&utm_content={variant_id}
   ```

   Example: `https://yourproduct.com/demo?utm_source=acme-weekly&utm_medium=newsletter&utm_campaign=co-marketing-shoutouts&utm_content=curiosity-v1`

4. **Validate the blurb.** Before sending to the partner, check:
   - Word count within partner's constraints
   - CTA link works and UTM parameters fire in PostHog
   - No jargon the partner's audience wouldn't understand
   - The blurb reads as native content, not an ad
   - Spelling and grammar are correct

5. **Send to partner for approval.** Email the blurb variants to your partner contact. Include:
   - The blurb text (plain text, not HTML)
   - Any image/logo assets if the format allows
   - Suggested placement (top, middle, or end of newsletter)
   - The tracked CTA link
   - A note that they can edit for tone — the CTA link is the only non-negotiable

6. **Archive the final version.** Store the approved blurb in your CRM (Attio) linked to the partner record. Include: blurb text, variant used, partner newsletter issue date, and CTA URL. This creates a library of proven blurbs for reuse and optimization.

## Error Handling
- If Claude generates off-brand copy, add 2-3 example paragraphs from the partner's newsletter to the prompt as few-shot examples
- If the partner rejects all variants, ask for a past sponsor blurb they liked and use it as a template
- If UTM parameters break the URL, URL-encode all parameter values

## Alternative Tools
- **OpenAI GPT-4**: Alternative LLM for copywriting
- **Jasper**: Marketing-focused AI copywriter
- **Copy.ai**: Specialized in short-form marketing copy
- **Manual writing**: For high-stakes partnerships, human-written blurbs may outperform
