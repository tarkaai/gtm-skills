---
name: list-swaps-adjacent-startups-smoke
description: >
  List Swap With Partner — Smoke Test. Execute one email list swap with one
  adjacent, non-competing startup to validate that cross-audience email sends
  generate clicks and at least one meeting before investing in a multi-partner
  swap program.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 30 clicks and ≥ 1 meeting in 1 week"
kpis: ["Click-through rate", "Email open rate"]
slug: "list-swaps-adjacent-startups"
install: "npx gtm-skills add marketing/solution-aware/list-swaps-adjacent-startups"
drills:
  - partner-prospect-research
  - list-swap-email-copy
  - threshold-engine
---

# List Swap With Partner — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

One complete email list swap executed with one adjacent startup. You send a dedicated email about the partner to your list; they send a dedicated email about you to theirs. At least 30 clicks to your landing page and at least 1 meeting booked within 7 days of the swap send. This proves that a partner's subscriber list responds to your value proposition and that the swap model (mutual, free, email-for-email) is viable before investing in scaling the channel.

## Leading Indicators

- Partner responds to swap pitch within 3 days (signal: the swap concept resonates with adjacent startups)
- Partner agrees without requiring payment (signal: mutual value is obvious)
- Swap email open rate exceeds 25% on the partner's list (signal: the subject line works for an unfamiliar audience)
- Clicks arrive within 24 hours of the partner's send (signal: the audience is engaged and active)
- At least 1 click converts to a meeting booking or demo request (signal: traffic quality is real, not just curiosity)
- Your list's response to the partner's email does not spike unsubscribes above 0.3% (signal: your audience tolerates swap content)

## Instructions

### 1. Research and select one partner

Run the `partner-prospect-research` drill with a reduced scope: identify 5-10 candidate companies that meet these criteria:

- **Adjacent, not competing**: They serve the same buyer persona but solve a different problem. Example: if you sell analytics, partner with a feature flagging tool, not another analytics platform.
- **Similar audience size**: Their email list should be within 0.5x-2x of yours. A 500-subscriber list swapping with a 50,000-subscriber list creates an unfair exchange.
- **Active email program**: They send at least biweekly. A dormant list produces stale clicks.
- **Solution-aware audience**: Their subscribers already know the problem category you solve (they are solution-aware, matching this play's stage).

Score each candidate on audience overlap, list size, email engagement signals, and co-marketing friendliness. Select the single highest-scoring partner. Prioritize partners where you have an existing relationship (shared investor, met at an event, mutual connection on LinkedIn) because cold swap pitches add latency to a smoke test.

### 2. Pitch the swap

**Human action required:** Reach out to your selected partner. Send a short email or LinkedIn DM to the founder, marketing lead, or newsletter owner:

- Explain the proposal: a one-time, free email swap. You each send one dedicated email to the other's list.
- Explain the mutual value: you both get exposure to a relevant, non-competing audience at zero cost.
- Specify the format: a standalone email (not a blurb inside a newsletter), 200-400 words, with one CTA.
- Propose a specific swap date (aim for Tuesday-Thursday of the following week).
- Offer to share your email draft first so they can assess quality before committing.

Log the outreach in Attio. Update the partner status from "Prospect" to "In Conversation."

### 3. Prepare your landing page and tracking

Ensure the landing page receiving swap traffic is ready:

- One clear CTA: demo request, free trial signup, or resource download
- Page loads in under 3 seconds
- Mobile-optimized (most email readers open on phones)
- PostHog tracking installed to capture:
  - `pageview` events with UTM parameters
  - `list_swap_click` event when a visitor takes the CTA
  - `list_swap_meeting_booked` event when a meeting is booked

Build the UTM-tagged URL:
`{your_landing_page}?utm_source={partner_slug}&utm_medium=list-swap&utm_campaign=list-swaps-adjacent-startups&utm_content=smoke-v1`

### 4. Write and deliver the swap email

Run the `list-swap-email-copy` drill. Generate 3 email variants (curiosity, data-driven, story-driven), select the best fit for the partner's audience tone, and send it to the partner for approval. Include:

- Subject line and preview text
- Plain-text email body (200-400 words)
- The UTM-tracked CTA link
- A note: "Adjust the wording for your voice — the CTA link needs to stay as-is"

Simultaneously, receive the partner's swap email for your list. Review it for quality and relevance to your audience. Reject if it is off-topic or low-quality — protect your list.

### 5. Execute the swap

On the agreed date:
- The partner sends your email to their list
- You send the partner's email to your list (via Loops broadcast or your email tool)
- Both parties confirm "sent" after dispatch

Log both send timestamps in Attio on the partner record.

### 6. Monitor results in real-time

On send day and for 7 days after:
- Watch PostHog for `pageview` events with `utm_source` matching the partner and `utm_medium=list-swap`
- Note click velocity: burst arrival (engaged list) vs. trickle (low engagement)
- Monitor `list_swap_click` events for CTA conversions
- Monitor `list_swap_meeting_booked` events
- Also track how the partner's email performed with YOUR list (opens, clicks, unsubscribes)

### 7. Evaluate against threshold

Run the `threshold-engine` drill 7 days after the swap send. Measure:

- Total clicks from the partner's list to your landing page
- Meetings booked from swap-sourced traffic
- Your list's response to the partner's email (open rate, click rate, unsubscribe rate)

**Pass threshold: >= 30 clicks AND >= 1 meeting**

- **Pass**: Document what worked (partner type, email angle, landing page, audience fit). Note the reciprocity balance (did you give as much value as you received?). Proceed to Baseline.
- **Marginal**: 15-29 clicks or 0 meetings but strong click engagement. Try one more partner before deciding. The audience may be right but the email copy or landing page needs iteration.
- **Fail**: <15 clicks. Diagnose: Was the partner's audience actually solution-aware? Was the email too generic? Was the subject line weak? Was the partner's list too small or disengaged? Iterate the variable most likely to be the bottleneck and re-test with a different partner.

## Time Estimate

- Partner research and selection: 1 hour
- Partner outreach and negotiation: 30 minutes (human action)
- Landing page prep and tracking setup: 30 minutes
- Swap email writing and partner approval: 30 minutes
- Reciprocal email review and scheduling: 15 minutes
- Monitoring and evaluation: 15 minutes

Total: ~3 hours of active work over 1 week (waiting for partner response and swap date)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Partner CRM tracking | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Click, lead, and meeting tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Swap email copywriting | Sonnet 4.6: $3/$15 per MTok; ~$0.10-0.50 per email ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Loops | Send partner's email to your list | Free up to 1K contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated cost for this level: Free** (all tools within free tiers for a single swap)

## Drills Referenced

- `partner-prospect-research` — find and score adjacent startups whose audiences overlap your ICP
- `list-swap-email-copy` — write, track, and deliver the standalone swap email
- `threshold-engine` — evaluate clicks and meetings against the pass threshold
