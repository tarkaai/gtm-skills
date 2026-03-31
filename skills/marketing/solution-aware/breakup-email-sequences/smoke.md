---
name: breakup-email-sequences-smoke
description: >
  Breakup Email Sequences — Smoke Test. The founder manually sends "we're closing
  your file" emails to 30-50 silent prospects who completed a prior outbound sequence
  without replying. Validates whether breakup emails produce re-engagement from
  solution-aware leads who went dark. No tooling budget. Manual send from existing inbox.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 3 positive replies from ≤ 50 breakup emails in 7 days"
kpis: ["Re-engagement rate (target ≥ 6%)", "Time to first reply (target < 48 hours)", "Latent interest ratio (replies from prospects who never replied to the original sequence)"]
slug: "breakup-email-sequences"
install: "npx gtm-skills add marketing/solution-aware/breakup-email-sequences"
drills:
  - icp-definition
---

# Breakup Email Sequences — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Prove that sending a "we're closing your file" email to prospects who went silent during a prior outbound sequence produces positive re-engagement. This is a manual test — the founder writes and sends from their real inbox to 30-50 prospects who received a prior outbound sequence and did not reply. The breakup email is psychologically different from cold email: it triggers loss aversion rather than curiosity. If 3+ prospects re-engage out of 50 sends, the tactic is worth automating.

Pass: 3 or more positive replies (meeting interest, question asked, or asset requested) from up to 50 breakup emails within 7 days.
Fail: Fewer than 3 positive replies after 50 sends and 7 days.

## Leading Indicators

- First reply arrives within 48 hours of first send (the loss-aversion trigger is resonating)
- At least 1 reply comes from a prospect who never opened any email in the original sequence (the breakup format is cutting through where the initial sequence could not)
- Replies include phrases like "actually, now is a good time" or "sorry I missed your earlier emails" (confirms the breakup frame is working, not just general outreach volume)

## Instructions

### 1. Identify the silent prospect pool

Check your CRM (Attio) for prospects who meet ALL of these criteria:

- Completed a prior outbound email sequence (3+ touches sent)
- Did not reply to any email in that sequence
- Last email in the prior sequence was sent 30-90 days ago (too recent feels like spam; too old and they have forgotten you)
- Still at the same company and role (check LinkedIn — do not send a breakup email to someone who left the company)

Use the `attio-contacts` fundamental to filter contacts by status "Sequence Completed" or "No Reply" and last contacted date within the 30-90 day window. You need 30-50 prospects. If you have fewer than 30, your prior outbound volume was too low — wait until you have enough, or expand the window to 120 days.

Run the `icp-definition` drill to confirm these prospects still match your ICP. If your ICP has shifted since the original outreach, filter out prospects who no longer fit.

### 2. Check for new signals on each prospect

Before sending a generic breakup, manually check each prospect for any change since they went silent:

- Did they change roles or get promoted? (LinkedIn profile check)
- Did their company raise funding? (Crunchbase or Google search)
- Did they post or engage with content related to your problem space? (LinkedIn activity)
- Did their company post job openings in your product's domain? (LinkedIn jobs)

For each prospect, note: `has_signal: yes/no` and `signal_detail: [what changed]`. Split your list into signal-detected (roughly 20-30% of prospects will have a signal) and no-signal groups. This segmentation matters — signal-detected breakups should reference the signal.

### 3. Write the breakup emails

Run the the breakup email copy workflow (see instructions below) drill to write the sequence. At Smoke level, you are sending manually, so the output is a text file or Google Doc with:

**For no-signal prospects (Email 1 only — the Honest Close):**

Subject: closing your file
Body (under 60 words):
- Line 1: "I sent a few notes over the past [X weeks] about [one-line problem]."
- Line 2: "I haven't heard back, so I'll assume the timing isn't right — closing your file on our end."
- Line 3: "If anything changes, you have my email. No hard feelings either way."
- Sign off: First name only.

**For signal-detected prospects (Email 1 — Signal-Referenced Close):**

Subject: closing your file
Body (under 75 words):
- Line 1: "I reached out a couple months ago about [problem]. I see [company] just [specific signal]."
- Line 2: "That changes the math on [how your product helps given the signal]. Worth a quick look?"
- Line 3: "If not, I'll close your file — no worries."
- Sign off: First name only.

Do NOT add a calendar link. Do NOT pitch. The entire point is to create a low-pressure reply moment. The prospect should feel like they are choosing to re-engage, not being sold to.

**Human action required:** The founder must review every email before sending. The tone must be genuinely casual — not passive-aggressive, not guilt-tripping, not "just checking in." If it reads like a marketing email, rewrite it.

### 4. Send manually over 3 days

**Human action required:** The founder sends breakup emails from their primary inbox (the same address used for the original outreach — continuity matters).

- Day 1: Send to all signal-detected prospects first (10-15 emails). These have the highest expected reply rate.
- Day 2: Send to the first half of no-signal prospects (10-15 emails).
- Day 3: Send to the remaining no-signal prospects (10-15 emails).

Space sends throughout the morning. Do not send more than 15 from a personal inbox in one day.

Log each send in Attio: update the contact's "Last Contacted" date, add a note "Breakup email sent — [signal/no-signal]", and change status to "Breakup Sent".

### 5. Handle replies within 2 hours

**Human action required:** When a reply arrives, respond within 2 hours. Breakup replies are psychologically fragile — the prospect just overcame their inertia to respond. A slow response kills the momentum.

For each reply, categorize and respond:

- **"Actually, let's talk":** Send 2-3 specific meeting times or a Cal.com link. Create a deal in Attio at "Meeting Booked" stage. Tag the deal `source: breakup-email-sequences`.
- **"Send me that resource":** If they are responding to a signal or showing curiosity, send the most relevant asset you have (case study, data point, 2-minute demo video). Follow up 3 days later to ask if it was useful and offer a call.
- **"Not now but maybe later":** Respond warmly, set a 90-day follow-up reminder in Attio. Do not send another breakup to this person — they responded, so they are now in a different nurture cadence.
- **"Remove me":** Update Attio status to "Do Not Contact." Respect immediately.

### 6. Evaluate results after 7 days

Count: total breakup emails sent, positive replies (categories 1-3 above), meetings booked. Compute re-engagement rate (positive replies / emails sent). Also compute:

- Signal-detected re-engagement rate vs. no-signal rate (does signal-based personalization lift performance?)
- Latent interest ratio (how many replies came from prospects who never opened the original sequence?)

- **PASS (3+ positive replies from 50 sends, ≥ 6% re-engagement rate):** Breakup emails recover silent prospects. Document: which signal types produced replies, whether the "closing your file" framing or the signal reference was cited in replies, and what the re-engaged prospects said about why they went silent originally. Proceed to Baseline.
- **MARGINAL (1-2 positive replies):** The tactic has potential but the sample is thin. Analyze: Did signal-detected prospects reply at a higher rate? If yes, the play works but needs better signal coverage. If no, the breakup framing may need adjustment. Re-run with 30 fresh silent prospects using a different subject line (try "last note from me" instead of "closing your file").
- **FAIL (0 positive replies):** Diagnose: Were the prospects too old (>90 days since last touch)? Was the original sequence already perceived as spam (negative brand association)? Did the breakup emails land in spam (check deliverability)? Try once more with a fresher pool (30-45 day window). If the second run also fails, these prospects may be genuinely uninterested and the play does not work for your market.

## Time Estimate

- Prospect identification and signal checking: 1.5 hours
- Breakup email writing with the breakup email copy workflow (see instructions below) drill: 30 minutes
- Sending over 3 days: 45 minutes total
- Reply handling over 7 days: 45 minutes total
- Results evaluation: 30 minutes
- Total: ~4 hours of active work spread over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Filter silent prospects, log sends, track replies | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | Booking link for re-engaged prospects | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Founder's primary email | Sending breakup emails | $0 (existing inbox) |
| LinkedIn | Manual signal checking | Free (basic profile views) |

**Estimated monthly cost for Smoke:** $0

## Drills Referenced

- `icp-definition` — confirm the silent prospect pool still matches your current ICP before sending breakups
- the breakup email copy workflow (see instructions below) — write the "closing your file" sequence with loss-aversion framing and signal-based personalization
