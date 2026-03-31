---
name: breakup-email-copy
description: Write breakup email sequences that re-engage silent prospects by leveraging loss aversion and low-commitment CTAs
category: Outreach
tools:
  - Instantly
  - Clay
  - Attio
fundamentals:
  - instantly-campaign
  - clay-claygent
  - clay-enrichment-waterfall
  - attio-contacts
  - attio-notes
---

# Breakup Email Copywriting

This drill produces a 2-3 step breakup email sequence designed for prospects who went silent during a prior outbound sequence. Breakup emails are NOT cold emails — the prospect already received your initial outreach and ignored it. The psychology is different: you are triggering loss aversion ("we're closing your file") rather than sparking curiosity. The tone must be respectful, direct, and final — not desperate or guilt-tripping.

## Prerequisites

- A list of prospects who completed a prior outbound sequence (3+ touches) without replying
- Prior sequence details: which emails they received, what angles were used, how long ago the sequence ended
- Clay table with prospect data and enrichment from the original sequence
- At least 30 days since the last touch in the prior sequence (sending a breakup 3 days after the last email feels like spam, not a breakup)

## Why Breakup Emails Work

Silent prospects are not always uninterested — many are busy, distracted, or waiting for a reason to prioritize your message. A breakup email works because it:

1. **Triggers loss aversion:** "We're moving on" implies they are losing access to something. Behavioral economics shows people weigh losses 2x more than equivalent gains.
2. **Removes pressure:** "No hard feelings" signals you are not going to keep hammering them. Paradoxically, reducing pressure increases responses.
3. **Creates a natural reply moment:** The prospect can respond to a farewell more easily than to a pitch. "Actually, now is a good time" is a low-effort reply.
4. **Filters genuine interest:** Anyone who replies to a breakup email is genuinely interested — these are high-quality responses.

## Steps

### 1. Segment your silent prospect list

Pull all prospects from Attio who completed a prior outbound sequence without responding. Use the `attio-contacts` fundamental to filter by:

- Status: "Sequence Completed" or "No Reply"
- Last contacted: 30-90 days ago (too recent = annoying; too old = forgotten)
- Original sequence source: tag with the prior play slug for attribution

Use the `clay-claygent` fundamental to check for any new signals since the prospect went silent: job change, funding event, company news, new LinkedIn post. These signals feed personalization in the breakup email — "I noticed [company] just [signal]" gives a fresh reason to re-engage.

Segment into two groups:
- **Signal-detected:** Prospect has a new signal since going silent. These get a signal-referenced breakup (higher priority).
- **No new signal:** No change detected. These get a standard breakup.

### 2. Write the breakup sequence

A breakup sequence is 2 steps for no-signal prospects and 3 steps for signal-detected prospects. Each email has a specific psychological job.

**Email 1 — The Honest Close (Day 0)**

Job: Signal that this is the last outreach, trigger loss aversion, and give one final reason to engage.

Structure for **no-signal** prospects:
- Line 1: "I sent a few notes over the past [timeframe] about [one-line problem your product solves]."
- Line 2: "I haven't heard back, so I'll assume the timing isn't right — closing your file on our end."
- Line 3: "If anything changes, you have my email. No hard feelings either way."
- Sign off: First name only.

Structure for **signal-detected** prospects:
- Line 1: "I reached out a couple months ago about [problem]. I see [company] just [specific signal — funding, hire, news]."
- Line 2: "That changes the math on [how your product helps in light of the signal]. Worth a quick look?"
- Line 3: "If not, I'll close your file — no worries."
- Sign off: First name only.

Constraints: Under 60 words for no-signal, under 75 words for signal-detected. No links. No attachments. No images. Plain text. No subject line tricks — use simple subjects like "closing your file" or "quick note."

**Email 2 — The Door Ajar (Day 4-5)**

Job: For prospects who opened Email 1 but did not reply, give one ultra-low-friction CTA.

Structure:
- Line 1: "One more thing before I close this out —"
- Line 2: One sentence offering the single lowest-friction next step you have. Not a meeting. Not a demo. Something they can consume in 2 minutes: a case study PDF, a 90-second video, a benchmark data point relevant to their company.
- Line 3: "Reply 'send it' if you want it. If not, all good."
- Sign off: First name only.

Constraints: Under 40 words. The "reply 'send it'" format gets replies because it takes 2 seconds. Only send this to prospects who opened Email 1 (use Instantly open tracking for this step only).

**Email 3 — Signal Follow-Through (Day 7, signal-detected only)**

Job: For signal-detected prospects who opened but did not reply to Emails 1 or 2, deliver the signal-specific value upfront without asking for anything.

Structure:
- Line 1: "Last note — saw [signal detail]. Thought this might be useful:"
- Line 2-3: One specific, relevant insight or data point about how companies in a similar situation benefited from addressing [problem]. Not a pitch — an observation they can use whether or not they buy your product.
- Line 4: "Worth a conversation if this resonates. Either way, good luck with [signal context]."

Constraints: Under 70 words. This email gives value first, creating reciprocity. Only use for signal-detected prospects who showed open engagement.

### 3. Build personalization variables in Clay

Using the `clay-enrichment-waterfall` fundamental, create these template columns:

- `prior_sequence_topic`: One-line summary of what the original outreach was about. Pull from Attio notes on the contact record.
- `days_since_last_touch`: Calculated field. Used to set the "I sent a few notes over the past [X weeks/months]" line.
- `recent_signal`: The new buying signal detected since they went silent. Null for no-signal prospects.
- `signal_relevance`: One sentence explaining why the signal makes your product more relevant now. Generated by Clay AI column.
- `low_friction_asset`: The specific resource to offer in Email 2. Match to the prospect's industry or role from your content library.

### 4. Load the sequence into Instantly

Using the `instantly-campaign` fundamental:

1. Create two campaigns: `[Date]-breakup-signal` and `[Date]-breakup-standard`
2. Upload leads from Clay with personalization variables mapped
3. Set the sequence steps with the copy from Step 2
4. Set sending schedule: Tuesday-Thursday, 8-10am in the prospect's timezone (avoid Mondays and Fridays for breakup emails — Tuesdays have the highest breakup reply rates historically)
5. Set daily limit to 20-30 per sending account (higher than initial outreach is fine — these are known contacts, not cold)
6. Enable open tracking on Email 1 only (needed to gate Email 2 delivery)
7. Set Email 2 as conditional: only sends if Email 1 was opened
8. Set Email 3 as conditional: only sends to signal-detected prospects who opened Email 1 or 2

### 5. Quality-check before sending

Review the first 5 rendered emails from each campaign. Check:
- Does the "closing your file" tone feel genuine and not passive-aggressive?
- Is the signal reference specific and current (not stale news)?
- Is the low-friction asset in Email 2 actually low-friction (not a 30-page whitepaper)?
- Does each email feel like a human closing a loop, not a robot running a sequence?

Use the `attio-notes` fundamental to log the breakup campaign launch on each contact record so future outreach knows this prospect received a breakup.

## Output

- A 2-3 step breakup email sequence loaded in Instantly, segmented by signal vs. no-signal
- Clay table with breakup-specific personalization variables mapped to Instantly merge fields
- Attio contact records updated with breakup sequence log
- Campaign configured with conditional step delivery based on opens

## Reusability

This drill is used by any play that needs to re-engage silent prospects from a completed outbound sequence. The breakup copy structure stays the same; the signal types and low-friction assets change per product and ICP.
