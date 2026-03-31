---
name: postcard-campaign-send
description: Prepare, verify, and send a batch of personalized postcards to a prospect list via Lob or PostGrid
category: DirectMail
tools:
  - Lob
  - PostGrid
  - Attio
  - Clay
fundamentals:
  - lob-address-verify
  - lob-template-create
  - lob-postcard-send
  - postgrid-postcard-send
  - attio-contacts
  - clay-enrichment-waterfall
---

# Postcard Campaign Send

This drill takes a prospect list from your CRM, verifies mailing addresses, creates personalized postcard templates, and sends a batch of physical postcards via the Lob or PostGrid API. It handles the full send workflow from list to mailbox.

## Input

- A prospect list in Attio (or exported from Clay) with: name, company, address, and at least one personalization field (pain point, trigger event, etc.)
- Postcard copy variants (headline, body, CTA) — at minimum 1 variant, ideally 2-3 for testing
- Sender return address
- Lob API key (or PostGrid API key)

## Steps

### 1. Export the prospect list from CRM

Pull the target contact list from Attio using the `attio-contacts` fundamental. Query contacts tagged for this direct mail campaign. Required fields per contact: first_name, last_name, company, address_line1, city, state, zip, and the personalization field (e.g., pain_point, trigger_event).

If addresses are missing, use the `clay-enrichment-waterfall` fundamental to enrich contacts with physical mailing addresses. Clay can source business addresses from firmographic data providers.

### 2. Verify all mailing addresses

For each contact, run the `lob-address-verify` fundamental against their address. Process the results:

- `deliverable` or `deliverable_unnecessary_unit` — Keep. Use the standardized address from the response (Lob corrects typos and formatting).
- `deliverable_missing_unit` — Flag for manual review. The address may be a multi-unit building.
- `undeliverable` or `deliverable_incorrect_unit` — Remove from the send list. Update the contact in Attio with `address_status = undeliverable`.

Log verification results: total contacts, deliverable count, undeliverable count.

### 3. Create postcard templates

Using the `lob-template-create` fundamental, create front and back templates for each variant.

**Front template** should include:
- A personalized headline using `{{first_name}}` and/or `{{company}}`
- A compelling visual or product screenshot
- One clear value proposition tied to `{{pain_point_headline}}`

**Back template** should include:
- 2-3 sentences of body copy addressing the specific pain point
- A clear CTA (e.g., "Scan the QR code to book a 15-minute call")
- A personalized tracking URL: `https://yoursite.com/dm?ref={{contact_id}}`
- Your company logo and return address

Store the template IDs for each variant.

### 4. Generate personalized tracking URLs

For each contact, construct a unique tracking URL:
```
https://yoursite.com/dm?ref={{contact_id}}&v={{variant_id}}&c={{campaign_id}}
```

This URL should redirect to your booking page or landing page while logging a PostHog event (`direct_mail_url_visited`) with the contact ID, variant, and campaign as properties.

### 5. Send postcards

For each verified contact, call the `lob-postcard-send` fundamental (or `postgrid-postcard-send` if using PostGrid):

- Pass the verified, standardized address
- Pass the template IDs for the assigned variant
- Include merge variables: first_name, company, pain_point_headline, body_copy, cta_text, qr_or_url
- Include metadata for filtering: `metadata[campaign_id]`, `metadata[variant]`, `metadata[contact_id]`

Process in batches of 50 to monitor for errors. After each batch, check for 422 errors (address issues that passed verification but failed at send time) and log them.

### 6. Log send data in CRM

For each successfully sent postcard:
- Update the contact in Attio with: `direct_mail_sent = true`, `direct_mail_sent_date`, `direct_mail_postcard_id` (the Lob/PostGrid ID), `direct_mail_variant`, `direct_mail_expected_delivery`
- Create a note on the contact record: "Postcard sent: [variant name], expected delivery: [date]"

### 7. Post-send summary

Generate a campaign summary:
- Total contacts in list
- Addresses verified as deliverable
- Addresses undeliverable (removed)
- Postcards successfully sent
- Postcards failed at send time
- Estimated delivery window
- Cost: [count] x [per-piece cost] = [total spend]

Log this summary as a PostHog event: `direct_mail_campaign_sent` with properties for all counts.

## Output

- A batch of personalized postcards in the Lob/PostGrid print queue
- Each contact in Attio updated with send status, postcard ID, and expected delivery date
- A campaign summary with counts and cost
- Personalized tracking URLs ready to attribute responses

## Triggers

- Run manually per campaign at Smoke and Baseline levels
- At Scalable level, trigger via n8n when a batch of prospects is ready (e.g., weekly list refresh from Clay)
