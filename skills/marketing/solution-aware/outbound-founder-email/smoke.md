---
name: outbound-founder-email-smoke
description: >
  Outbound founder-led email — Smoke Test. The founder personally sends cold emails
  to 20-50 solution-aware prospects to validate whether founder-sent email produces
  meetings. No tooling budget. Manual send from the founder's real inbox.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 2 positive replies (meeting booked or interest expressed) from ≤ 50 sends in 7 days"
kpis: ["Positive reply rate (target ≥ 4%)", "Time to first reply (target < 48 hours)", "Meetings booked"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
---

# Outbound Founder-Led Email — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Prove that cold email sent from the founder to solution-aware prospects produces positive replies and meetings. This is a manual test — the founder writes and sends emails from their real inbox. No cold email tooling. No automation. If this works at 20-50 sends, it is worth automating at Baseline.

Pass: 2 or more positive replies (meeting booked or explicit interest) from up to 50 emails within 7 days.
Fail: Fewer than 2 positive replies after 50 sends and 7 days.

## Leading Indicators

- First reply arrives within 48 hours of first send (signals the message resonates)
- At least 1 reply in the first 20 sends (signals the list quality is adequate)
- Replies reference the competitive positioning or proof point, not just politeness (signals the solution-aware angle is landing)

## Instructions

### 1. Define ICP and competitive positioning

Run the `icp-definition` drill to document your Ideal Customer Profile. For this play, add one extra step: list the 2-3 alternatives your prospects are most likely evaluating (competitors, DIY/spreadsheets, status quo/doing nothing). For each alternative, write one sentence on what it does well and one sentence on the gap your product fills. This competitive context drives the email copy.

**Human action required:** The founder must validate the competitive context from their own customer conversations. The agent can draft it, but the founder knows which competitors actually come up in sales calls.

### 2. Build a prospect list of 20-50 contacts

Manually search LinkedIn, your network, and your CRM (Attio) for 20-50 people matching your ICP. For each prospect, record in a spreadsheet or Attio:
- Name, email, company, role
- One specific thing you noticed about them (recent post, company news, job posting, tech stack detail)
- Which alternative they are most likely using today

Do NOT use enrichment tools yet. The point of Smoke is to validate the channel with zero spend. If you cannot find 20 prospects manually, the ICP may be too narrow — revisit step 1.

Use the `attio-contacts` fundamental to log each prospect in Attio with status "Prospected" and tag "outbound-founder-email-smoke".

### 3. Write the 3-step email sequence

Run the the founder cold email copy workflow (see instructions below) drill to write a 3-step sequence. At Smoke level, you are sending manually, so the output is a Google Doc or text file with:
- Email 1 template (the founder intro — under 90 words)
- Email 2 template (the proof point — under 70 words)
- Email 3 template (the direct ask — under 60 words)

Personalize Email 1's first line for each prospect individually. Emails 2 and 3 can use the same template across all prospects with only the company name and similar-customer reference swapped.

**Human action required:** The founder must review all email copy before sending. The agent drafts, the founder edits for voice. If the emails do not sound like the founder wrote them, they will not perform.

### 4. Send manually over 5 days

**Human action required:** The founder sends emails from their primary email account (not a secondary domain). Send Email 1 to all prospects on Day 1 (limit: 10 per day to avoid triggering spam filters from a personal inbox). Send Email 2 on Day 4 to anyone who did not reply. Send Email 3 on Day 7 to anyone who still did not reply.

Log each send in Attio: update the contact's "Last Contacted" date and add a note with the email step number.

### 5. Handle replies within 1 hour

**Human action required:** When a positive reply arrives, the founder responds within 1 hour with 2-3 specific meeting times or a Cal.com booking link. Speed matters — the prospect is comparing solutions, and the first vendor to get a meeting wins mindshare.

For each reply, update Attio: change status to "Replied - Interested", "Replied - Not Now", or "Replied - Not Interested". For meetings booked, create a deal in Attio at stage "Meeting Booked".

### 6. Evaluate results after 7 days

Count: total emails sent, positive replies, meetings booked. Compute positive reply rate (positive replies / emails sent).

- **PASS (≥ 2 positive replies):** The channel works. Document which message angles and personalization lines got the best responses. Proceed to Baseline.
- **MARGINAL (1 positive reply):** Promising but not proven. Review which emails were opened but not replied to (ask non-responders if you know them). Adjust the competitive positioning or proof point and re-run with 30 fresh prospects.
- **FAIL (0 positive replies):** Diagnose: Was the list quality poor (wrong ICP)? Was the messaging wrong (not addressing the right alternative)? Was the proof point weak? Fix the weakest link and re-run once. If the second run also fails, this motion may not work for your market — try a different play.

## Time Estimate

- ICP definition and competitive context: 1 hour
- Prospect list building (manual): 1 hour
- Email copywriting with the founder cold email copy workflow (see instructions below) drill: 1 hour
- Sending, monitoring, and replying over 7 days: 1 hour total
- Total: ~4 hours of active work spread over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Log prospects and track replies | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | Booking link in Email 3 | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Founder's primary email | Sending | $0 (existing inbox) |

**Estimated monthly cost for Smoke:** $0

## Drills Referenced

- `icp-definition` — define the target audience and competitive context for solution-aware messaging
- the founder cold email copy workflow (see instructions below) — write the 3-step sequence in the founder's voice with solution-aware positioning
