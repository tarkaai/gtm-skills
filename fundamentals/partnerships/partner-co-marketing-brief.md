---
name: partner-co-marketing-brief
description: Generate a joint landing page, blog post, and email announcement for an integration launch with a partner
tool: Anthropic
product: Claude API
difficulty: Setup
---

# Partner Co-Marketing Brief

## Prerequisites
- Integration built and tested (or at least scoped with clear value proposition)
- Partner company name, domain, and product description
- Agreed co-marketing scope with partner (which assets, launch date, distribution channels)
- Anthropic API key for Claude (content generation)

## Steps

1. **Assemble integration context.** Collect the raw materials Claude needs to generate launch assets:

   ```json
   {
     "your_product": "{your_product_name}",
     "partner_product": "{partner_product_name}",
     "integration_description": "What the integration does in one sentence",
     "use_cases": ["Use case 1", "Use case 2", "Use case 3"],
     "target_persona": "Who benefits most (title, role, pain point)",
     "value_proposition": "Why this integration matters to the target persona",
     "setup_steps": ["Step 1", "Step 2", "Step 3"],
     "cta_url": "URL where users activate the integration",
     "launch_date": "YYYY-MM-DD",
     "partner_audience_size": "Estimated reach via partner channels"
   }
   ```

2. **Generate the joint landing page copy.** Call the Anthropic API:

   ```
   POST https://api.anthropic.com/v1/messages
   Authorization: Bearer {ANTHROPIC_API_KEY}
   Content-Type: application/json

   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 2000,
     "messages": [{
       "role": "user",
       "content": "Write landing page copy for a product integration launch. Hero headline (max 10 words), subheadline (max 25 words), 3 benefit blocks (headline + 2-sentence description each), setup section (3-step numbered list), and CTA button text. Integration context: {integration_context_json}. Write for {target_persona}. Tone: clear, specific, no hype. Every claim must be verifiable."
     }]
   }
   ```

3. **Generate the co-marketing blog post.** Call the Anthropic API:

   ```
   POST https://api.anthropic.com/v1/messages
   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 3000,
     "messages": [{
       "role": "user",
       "content": "Write an 800-word blog post announcing a product integration. Structure: problem statement (what workflow is broken without this integration), solution (what the integration does), 3 specific use cases with concrete examples, setup instructions, and CTA. Integration context: {integration_context_json}. Write for a technical audience. No filler paragraphs. Every sentence must add information."
     }]
   }
   ```

4. **Generate partner email announcement.** Call the Anthropic API:

   ```
   POST https://api.anthropic.com/v1/messages
   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 1000,
     "messages": [{
       "role": "user",
       "content": "Write two email announcements for a product integration launch. Email A: for YOUR audience (people who use your product but may not use the partner's). Email B: for the PARTNER's audience (people who use the partner's product but may not use yours). Each email: subject line, preview text, 150-word body, CTA button text. Integration context: {integration_context_json}. Tone: helpful, not salesy. Focus on the workflow improvement, not the feature."
     }]
   }
   ```

5. **Generate UTM parameters for tracking.** Create tracked URLs for each asset:
   - Landing page: `?utm_source={partner_slug}&utm_medium=integration&utm_campaign=launch-{partner_slug}`
   - Blog post: `?utm_source=blog&utm_medium=content&utm_campaign=integration-{partner_slug}`
   - Your email: `?utm_source=email&utm_medium=lifecycle&utm_campaign=integration-launch-{partner_slug}`
   - Partner email: `?utm_source={partner_slug}&utm_medium=partner-email&utm_campaign=integration-launch-{partner_slug}`

6. **Record the brief.** Store in your CRM (Attio) as a note on the partner record:
   - Landing page copy (for your web team to implement)
   - Blog post draft (for review and publication)
   - Two email drafts (one for your list, one for partner's list)
   - UTM tracking URLs for each asset
   - Launch date and distribution plan

## Error Handling
- If Claude generates generic copy, re-prompt with more specific use cases and concrete numbers
- If partner requests copy changes, regenerate the specific asset with their feedback as additional context
- If launch date shifts, update UTM campaign parameters to include the new date

## Alternative Tools
- **OpenAI GPT-4**: Alternative LLM for content generation
- **Jasper**: Marketing-focused AI writing tool
- **Copy.ai**: Marketing copy generation
- **Notion AI**: Collaborative content drafting with partner team
- **Canva**: Generate visual assets (social cards, email banners) for the integration launch
