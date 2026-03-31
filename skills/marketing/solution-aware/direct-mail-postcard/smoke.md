---
name: direct-mail-postcard-smoke
description: >
  Direct Mail Postcards — Smoke Test. Send 20-50 personalized postcards to named accounts
  via the Lob API to test whether physical mail cuts through digital noise and generates
  inbound interest or meetings.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Other"
level: "Smoke Test"
time: "4 hours over 2 weeks"
outcome: "≥ 1 response (URL visit, email reply, or meeting booked) from 20-50 postcards within 14 days of delivery"
kpis: ["Postcards delivered", "Response rate", "Meetings booked"]
slug: "direct-mail-postcard"
install: "npx gtm-skills add marketing/solution-aware/direct-mail-postcard"
drills:
  - icp-definition
  - build-prospect-list
  - postcard-campaign-send
  - threshold-engine
---

# Direct Mail Postcards — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Other

## Outcomes

Prove that sending physical postcards to named accounts generates ANY signal — a tracking URL visit, an inbound email, or a meeting booking. This is a one-shot manual test, not an always-on campaign. The goal is to validate the channel before investing in automation.

## Leading Indicators

- Postcards successfully delivered (Lob tracking shows `Processed for Delivery` or `In Local Area`)
- Personalized tracking URL gets at least 1 visit within 14 days of delivery
- Any inbound email or LinkedIn message that references the postcard

## Instructions

### 1. Define your ICP for direct mail

Run the `icp-definition` drill. For direct mail, your ICP must include contacts for whom you can obtain a verified physical mailing address (typically office addresses). Focus on:
- Decision makers at companies with physical offices (not fully remote)
- Job titles that receive and process their own mail (founders, VPs at small companies)
- Industries where physical mail is uncommon in sales (SaaS, tech) — this is where postcards stand out most

### 2. Build and enrich a prospect list with mailing addresses

Run the `build-prospect-list` drill with a focus on enriching mailing addresses. Target 20-50 contacts for this Smoke test. In Clay, use the `clay-enrichment-waterfall` to source business mailing addresses. If Clay cannot find a physical address for a contact, check LinkedIn for company headquarters and use that address. Remove any contact without a verifiable physical address.

Export the list to Attio with fields: first_name, last_name, company, title, address_line1, address_line2, city, state, zip, pain_point (a one-line description of their primary challenge that your product addresses).

### 3. Write postcard copy

Create one postcard variant. This is a Smoke test — you are testing the CHANNEL, not optimizing copy.

**Front copy template:**
- Headline: Personalized to the recipient's pain point (e.g., "{{first_name}}, still spending 10 hours/week on {{pain_point}}?")
- One sentence of value proposition
- Keep it scannable — recipients decide in 2 seconds whether to flip the card

**Back copy template:**
- 2-3 sentences expanding on how you solve their problem
- A clear CTA: "Scan the QR code for a 15-minute demo" or "Visit {{tracking_url}} to see how we helped {{similar_company}}"
- Include a personalized tracking URL: `https://yoursite.com/dm?ref={{contact_id}}&c=smoke-1`
- Your name, title, and company (this is founder-led outreach, make it personal)

### 4. Send the postcards

Run the `postcard-campaign-send` drill:
1. Verify all addresses via Lob's address verification API
2. Create front and back templates in Lob with your copy
3. Send postcards to all verified addresses
4. Log send data in Attio (postcard ID, send date, expected delivery)

**Human action required:** Review the Lob PDF preview of your postcard before confirming the live send. Check that merge variables rendered correctly, the layout is readable, and the tracking URL is correct.

**Cost estimate:** 20-50 postcards x $0.77/piece (Lob Developer plan) = $15-$39 total.

### 5. Wait for delivery and responses

Monitor Lob tracking events for delivery confirmation. Postcards typically deliver in 3-7 business days.

After delivery confirmation, watch for responses over 14 days:
- Check PostHog for `direct_mail_url_visited` events from the tracking URLs
- Check email inbox for replies mentioning the postcard
- Check Attio for any new meetings booked by contacts who received postcards

Log every response manually in Attio: response type, date, and the contact's reaction.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pass threshold: at least 1 response (URL visit, email reply, or meeting booked) from 20-50 postcards within 14 days of delivery.

If PASS: Direct mail works for your audience. Proceed to Baseline to automate and scale.
If FAIL: Diagnose whether the issue was addressing (postcards returned?), relevance (wrong ICP or messaging), or timing. Iterate and re-run Smoke with adjusted targeting or copy.

Record qualitative notes: Who responded? What did they say? Did anyone mention the postcard was surprising or memorable? This qualitative signal is as valuable as the numbers at Smoke stage.

## Time Estimate

- 1 hour: ICP definition and prospect list building (with Clay enrichment)
- 1 hour: Copy writing and template creation in Lob
- 30 minutes: Address verification and send execution
- 30 minutes: Response monitoring and evaluation (spread over 2 weeks)
- Total: ~4 hours of active work over a 2-week window (including delivery and response time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Lob | Print and mail postcards via API | $0/mo + $0.77/postcard (Developer plan). https://www.lob.com/pricing |
| Clay | Enrich prospects with mailing addresses | From $149/mo. https://www.clay.com/pricing |
| Attio | Store contacts, log send data and responses | Free for small teams. https://attio.com/pricing |
| PostHog | Track URL visits from postcards | Free up to 1M events/mo. https://posthog.com/pricing |

**Estimated total cost for Smoke:** $15-$39 (postcard printing and mailing only)

## Drills Referenced

- `icp-definition` — Define the ideal customer profile for direct mail targeting
- `build-prospect-list` — Source and enrich 20-50 prospects with mailing addresses
- `postcard-campaign-send` — Verify addresses, create templates, and send postcards via Lob API
- `threshold-engine` — Evaluate results against the pass threshold
