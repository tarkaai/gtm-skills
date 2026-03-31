---
name: outbound-email-li-calls-smoke
description: >
  Outbound Email/LI/Calls — Smoke Test. Manually run a founder-sent multi-channel
  outreach sequence (email + LinkedIn + phone) to 50-100 ICP contacts to validate
  whether this channel combination produces meetings within 7-10 days.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 2 meetings booked in 1 week"
kpis: ["Reply rate", "Time to first reply", "Meetings booked"]
slug: "outbound-email-li-calls"
install: "npx gtm-skills add marketing/solution-aware/outbound-email-li-calls"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# Outbound Email/LI/Calls — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

The Smoke Test proves that multi-channel outbound (email + LinkedIn + calls) can book meetings with solution-aware prospects. Success means at least 2 meetings booked from a manually executed sequence of 50-100 contacts within 1 week. No automation, no budget — just the founder reaching out with prepared messaging across three channels.

## Leading Indicators

- Positive email replies within 48 hours of first send
- LinkedIn connection acceptance rate above 30%
- At least 1 phone conversation lasting over 2 minutes
- Prospects referencing your email or LinkedIn message during calls

## Instructions

### 1. Define your ICP for outbound

Run the `icp-definition` drill. Document the firmographic criteria (company size, industry, funding stage), buyer persona (title, seniority, department), top 3 pain points, and 3 triggering events that make outbound timely. Write disqualification criteria so you do not waste outreach on poor fits.

Output: a one-page ICP document saved to your project's `docs/` directory and scoring criteria loaded into Clay.

### 2. Build a prospect list of 50-100 contacts

Run the `build-prospect-list` drill. Source contacts from Apollo matching your ICP. Import into Clay, run the enrichment waterfall to fill email addresses, LinkedIn URLs, and phone numbers. Score each contact. Filter to the top 50-100 by score. Push to Attio with tags `play:outbound-email-li-calls` and `level:smoke`.

Requirements per contact: verified email, LinkedIn profile URL, and phone number (at least 70% phone coverage — exclude the rest from call steps).

### 3. Write outreach copy for each channel

Prepare messaging for the 3-channel sequence. Write it yourself — this is a Smoke Test, not a template library exercise. The copy must be:

**Email (3-step sequence):**
- Email 1 (Day 1): Problem-aware opener from the founder. Under 80 words. Reference a specific pain point. No pitch. Soft question as CTA.
- Email 2 (Day 4): One proof point or data point from a similar customer. Under 70 words. Ask for 15 minutes.
- Email 3 (Day 7): Direct breakup email. Acknowledge you might be wrong. Include Cal.com booking link.

**LinkedIn (2-step):**
- Connection request (Day 2): Under 200 characters. Reference something specific about the prospect. No pitch.
- Follow-up message (Day 5, if connected): Share something useful. Ask a question about their current setup.

**Phone (1-2 attempts):**
- Call script: Opener referencing your email. One question about their current approach. Bridge to a 15-minute follow-up if interested.

### 4. Execute the multi-channel sequence manually

**Human action required:** Send all emails from your personal email client (Gmail, Outlook). Send LinkedIn connection requests and messages manually from your LinkedIn account. Make phone calls from your phone or Google Voice. This is NOT automated — you are proving the channel combination works before investing in tools.

Follow this timing across 7 days:
- Day 1: Send Email 1 to all prospects
- Day 2: Send LinkedIn connection requests to all prospects
- Day 3: Make phone calls to top 20 prospects
- Day 4: Send Email 2 to prospects who did not reply to Email 1
- Day 5: Send LinkedIn follow-up to those who accepted connections
- Day 6: Make phone calls to remaining top prospects
- Day 7: Send Email 3 (breakup) to all remaining non-responders

Log every touchpoint in Attio immediately: channel, step, response, and sentiment.

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Pull logged data from Attio. Count meetings booked. Compare against the pass threshold: **≥ 2 meetings booked in 1 week**.

- **PASS**: Proceed to Baseline. Document which channel drove each meeting (first touch and last touch), which messaging resonated, and which ICP segments responded.
- **FAIL**: Diagnose — was it targeting (wrong ICP), messaging (no replies), or channel (replies but no meetings)? Adjust and re-run Smoke.

Also record: reply rate by channel, time to first reply, and qualitative notes on objections heard.

## Time Estimate

- ICP definition and list building: 1 hour
- Copy writing: 30 minutes
- Manual outreach execution across 7 days: 1 hour total (10-15 min/day)
- Logging and evaluation: 30 minutes

Total: ~3 hours of active work spread over 1 week.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Prospect enrichment and list building | Free tier: 100 credits/mo; Pro: $149/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing | Free tier: 50 emails/mo; Basic: $49/mo (https://www.apollo.io/pricing) |
| Attio | CRM for logging outreach | Free tier: 3 users; Plus: $29/user/mo (https://attio.com/pricing) |
| Cal.com | Booking link in breakup email | Free tier available (https://cal.com/pricing) |
| PostHog | Event tracking | Free tier: 1M events/mo (https://posthog.com/pricing) |

**Estimated play-specific cost: $0 (free tiers sufficient for Smoke)**

## Drills Referenced

- `icp-definition` — define ideal customer profile with scoring criteria
- `build-prospect-list` — source, enrich, and qualify 50-100 contacts in Clay
- `threshold-engine` — evaluate pass/fail against ≥ 2 meetings threshold
