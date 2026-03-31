---
name: gift-campaign-send
description: Build a prospect list, select gifts via AI, send personalized gifts, and log all activity in CRM
category: Gifting
tools:
  - Sendoso
  - Tremendous
  - Reachdesk
  - Giftsenda
  - Clay
  - Attio
  - Anthropic
fundamentals:
  - sendoso-send-gift
  - tremendous-send-reward
  - reachdesk-send-gift
  - giftsenda-send-gift
  - gift-selection-scoring
  - clay-enrichment-waterfall
  - attio-contacts
  - attio-notes
---

# Gift Campaign Send

This drill takes a qualified prospect list, selects the optimal gift for each recipient using AI, sends gifts via the configured gifting platform, and logs all activity in the CRM. It handles the full send workflow from list to delivered gift.

## Input

- A prospect list in Attio tagged for the gift campaign, with: first_name, last_name, email, company, title, signal_type, and optionally physical address and LinkedIn interests
- Campaign ID for tracking
- Budget ceiling per gift (e.g., $50)
- Gifting platform credentials (at least one of: Sendoso, Tremendous, Reachdesk, Giftsenda)

## Steps

### 1. Export the prospect list from CRM

Pull contacts from Attio using the `attio-contacts` fundamental. Query contacts where `gift_campaign_tag = {{campaign_id}}` and `gift_sent = false`. Required fields per contact: first_name, last_name, email, company, title, signal_type.

If physical addresses are needed and missing, use the `clay-enrichment-waterfall` fundamental to source business mailing addresses. For eGift-only campaigns, addresses are not required.

### 2. Enrich prospects for gift personalization

For each contact, gather personalization data:
- Pull LinkedIn headline and recent activity from Clay enrichment
- Extract company news and funding data from Clay company enrichment
- Classify the signal type (job change, funding, hiring, competitor adoption)

Store all enrichment data on the contact record in Attio.

### 3. Run AI gift selection for each prospect

For each contact, call the `gift-selection-scoring` fundamental with the prospect's enrichment data and budget ceiling. The AI returns:
- Recommended gift category and specific item
- Gift value
- Personalized note draft
- Confidence score

If confidence < 0.5, flag the contact for human review and skip automated sending.

### 4. Map gift selections to platform catalog

For each AI recommendation, map it to an available item in your gifting platform:

**For eGift cards / digital rewards:**
Use `tremendous-send-reward` — lowest cost, no platform fee, 1000+ brands.

**For physical gifts (books, gourmet, swag):**
Use `sendoso-send-gift` or `reachdesk-send-gift` depending on your platform. For international recipients, prefer `reachdesk-send-gift` or `giftsenda-send-gift` (better international coverage).

If the AI-recommended item is not available in the catalog, select the closest match from the same category and price range.

### 5. Send gifts

For each contact, execute the send via the appropriate gifting platform fundamental:

1. Pass recipient data (name, email, address if physical)
2. Pass the gift item ID from the catalog
3. Include the AI-generated personalized note
4. Include metadata: `campaign_id`, `contact_id`, `signal_type`, `variant_id` (if A/B testing)

Process in batches of 25 to monitor for errors. After each batch, check for failures and log them.

### 6. Log send data in CRM

For each successfully sent gift, update the contact in Attio using `attio-contacts`:
- Set `gift_sent = true`
- Set `gift_sent_date = {{today}}`
- Set `gift_type = {{gift_category}}`
- Set `gift_value = {{gift_value}}`
- Set `gift_platform = {{platform}}`
- Set `gift_send_id = {{platform_send_id}}`
- Set `gift_variant = {{variant_id}}`

Create a timeline note using `attio-notes`:
"Gift sent: {{gift_description}} (${{gift_value}}) via {{platform}}. Note: '{{personalized_note_preview}}'. Campaign: {{campaign_id}}."

### 7. Post-send summary

Generate a campaign send summary:
- Total contacts in list
- Gifts successfully sent (by type: eGift, physical, book, swag)
- Gifts failed (by failure reason)
- Low-confidence contacts flagged for human review
- Total spend: sum of all gift values + platform fees
- Average gift value

Log this summary as a PostHog event: `gift_campaign_batch_sent` with all counts as properties.

## Output

- A batch of personalized gifts sent via the configured platform
- Each contact in Attio updated with send status and gift details
- A campaign summary with counts, costs, and failures
- Low-confidence contacts flagged for manual gift selection

## Triggers

- Run manually per campaign at Smoke and Baseline levels
- At Scalable level, trigger via n8n when a batch of signal-detected prospects is ready (e.g., weekly)
- At Durable level, runs as part of the autonomous optimization loop
