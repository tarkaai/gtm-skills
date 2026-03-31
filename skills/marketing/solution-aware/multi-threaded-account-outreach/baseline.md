---
name: multi-threaded-account-outreach-baseline
description: >
  Multi-threaded Outreach — Baseline Run. First always-on multi-threaded sequences across
  50 accounts using Instantly for email and LinkedIn for social, with role-specific copy
  variants and PostHog tracking per stakeholder thread.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Baseline Run"
time: "18 hours over 3 weeks"
outcome: "≥3% account-to-meeting rate from 50 accounts over 3 weeks"
kpis: ["Account-to-meeting rate", "Multi-thread engagement rate", "Cost per meeting", "Response rate by stakeholder role"]
slug: "multi-threaded-account-outreach"
install: "npx gtm-skills add marketing/solution-aware/multi-threaded-account-outreach"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - multi-channel-cadence
  - posthog-gtm-events
---

# Multi-threaded Outreach — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Prove that multi-threaded outreach converts at ≥3% account-to-meeting rate when run as always-on sequences across 50 accounts. At Smoke you validated the approach manually; now you automate the email and LinkedIn sequences while maintaining role-specific messaging and coordinated cross-stakeholder timing.

**Pass threshold:** ≥3% of 50 accounts (≥2 accounts) convert to meetings within 3 weeks, with measurable multi-stakeholder engagement (2+ contacts engaged) in at least 20% of responding accounts.

## Leading Indicators

- Email open rate ≥40% across all role-specific variants (validates subject lines land)
- LinkedIn connection acceptance ≥25% on Champion and Influencer contacts
- Reply rate ≥4% on Champion-targeted emails (this role should respond highest)
- At least 5 accounts where 2+ stakeholders open or click within the same week
- Positive reply sentiment ≥60% of all replies (not just "remove me" responses)

## Instructions

### 1. Build the 50-account target list with stakeholder depth

Using the validated ICP from Smoke, source 50 accounts. For each account, identify 3 contacts across at least 2 different stakeholder roles. Use Clay for company search and people search, then run enrichment waterfall for verified emails and LinkedIn URLs.

Target stakeholder composition per account:
- 1 Champion (Director/Manager in the buying department)
- 1 Economic Buyer (VP+ or founder at companies <100 people)
- 1 Influencer or End User (senior IC or architect)

Total: ~150 contacts across 50 accounts. Push all contacts to Attio linked to deal records. Tag each contact with `stakeholder_role` and the account-level campaign tag `multi-thread-baseline`.

### 2. Create role-specific email sequences in Instantly

Run the `cold-email-sequence` drill three times — once per stakeholder role — to create three separate Instantly campaigns:

**Campaign: Champion Sequence (4 steps)**
- Email 1 (Day 0): Problem-aware opener targeting their operational pain. Under 80 words. First line personalized from Clay data.
- Email 2 (Day 3): Short case study from a similar role at a similar company. Specific result (e.g., "cut evaluation time from 6 weeks to 10 days").
- Email 3 (Day 7): Soft ask — "Would it make sense to show you how [Company] handled this? 15 minutes."
- Email 4 (Day 12): Breakup with value — share a useful resource and leave the door open.

**Campaign: Economic Buyer Sequence (3 steps)**
- Email 1 (Day 7): Business outcome lead. Reference the company's likely strategic priority (growth, efficiency, risk). Under 60 words.
- Email 2 (Day 11): ROI angle — "Companies your size typically see [X] within [timeframe]." Offer a 15-minute ROI walkthrough.
- Email 3 (Day 15): Breakup — "If timing's off, no worries. When [trigger event], I'd be a good call."

**Campaign: Influencer Sequence (3 steps)**
- Email 1 (Day 4): Technical insight. Share something they would find genuinely useful even if they never buy. Link to docs or benchmark data.
- Email 2 (Day 9): Integration angle — "Here's how we work with [tool in their stack]." Offer a technical deep-dive.
- Email 3 (Day 14): Breakup with peer positioning — "Happy to be a sounding board on [topic] regardless."

Note the staggered Day 0 offsets: Champions start first, Influencers on Day 4, Economic Buyers on Day 7. This mirrors the Smoke timing that validated cross-thread momentum.

### 3. Launch LinkedIn outreach in parallel

Run the `linkedin-outreach` drill for Champion and Influencer contacts (skip Economic Buyers on LinkedIn — email is more appropriate for executives unless LinkedIn data shows them active).

Connection request timing per account:
- Champion: Day 0 (same day as first email — different channel reinforces presence)
- Influencer: Day 3 (before their first email on Day 4, so your name is familiar)

Follow-up DM sequence after acceptance: 2 messages over 10 days. Message 1 is value-first (share something useful). Message 2 is a soft meeting ask.

### 4. Set up cross-channel coordination

Run the `multi-channel-cadence` drill to build the orchestration layer. Configure the n8n workflow to:

- **Pause rule**: If any contact at an account replies positively on any channel, pause all other sequences for that account for 48 hours. Check Attio deal status before each Instantly send.
- **Escalation rule**: If a Champion responds positively, trigger the Economic Buyer sequence immediately (skip the Day 7 delay) with an updated message: "Your team at [Company] has been exploring [topic]..."
- **Suppression rule**: If any contact replies negatively or opts out, suppress all outreach to that account for 30 days.
- **No-overlap rule**: Never send email and LinkedIn message to the same person on the same day.

### 5. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up tracking specific to multi-threaded outreach:

**Required events:**
- `mto_email_sent` — properties: account_id, stakeholder_role, sequence_step, subject_variant
- `mto_email_replied` — properties: account_id, stakeholder_role, sentiment, sequence_step
- `mto_linkedin_sent` — properties: account_id, stakeholder_role, message_type (connection/dm)
- `mto_linkedin_replied` — properties: account_id, stakeholder_role, sentiment
- `mto_meeting_booked` — properties: account_id, stakeholder_role, source_channel, threads_engaged (count of stakeholders who responded at this account)
- `mto_cross_thread_signal` — properties: account_id, signal_type (internal_referral, multi_stakeholder_response, escalation_triggered)

Connect Instantly webhooks to PostHog via n8n. Connect Attio deal stage changes to PostHog via webhook.

### 6. Run for 3 weeks and monitor daily

Let the sequences execute. Daily monitoring checklist:
- Check Instantly deliverability: bounce rate must stay below 2%. If it spikes, pause sends and check domain health.
- Check reply sentiment: if negative replies exceed 10%, review messaging for that role.
- Check cross-account coordination: ensure the pause rules are firing correctly (no one should receive email after a colleague already booked a meeting).

Weekly: review which stakeholder role generates the most replies, which message step converts best, and whether the staggered timing is producing cross-thread signals.

### 7. Evaluate against pass threshold

After 3 weeks:

1. Count accounts that converted to meetings: target ≥2 of 50 (3%)
2. Count accounts with multi-stakeholder engagement: target ≥10 of 50 (20%)
3. Review cost per meeting: add Instantly + Clay + LinkedIn costs and divide by meetings

**PASS (≥3% account-to-meeting rate + multi-stakeholder engagement in ≥20% of responding accounts):** The multi-threaded approach works at automation scale. Document which role-specific sequences performed best. Proceed to Scalable.

**FAIL — low reply rates across all roles (<2%):** Messaging problem. Review subject lines and openers. Check that the solution-aware framing is correct — are these buyers actually in evaluation mode?

**FAIL — replies but no meetings:** Conversion problem. Review the meeting ask in step 3 of each sequence. Consider whether the Influencer/End User thread is creating enough internal pressure to make the Economic Buyer receptive.

**FAIL — good single-thread results but no cross-thread signals:** The staggered timing or role-specific angles may not be creating internal conversation. Compress the timing (all threads within 3 days instead of 7) or add explicit cross-references in the messaging.

## Time Estimate

- Account sourcing and enrichment (50 accounts, 150 contacts): 4 hours
- Role-specific sequence copywriting (3 sequences): 4 hours
- Instantly and LinkedIn campaign setup: 3 hours
- PostHog event tracking and n8n coordination workflows: 4 hours
- Daily monitoring over 3 weeks: 3 hours
- Total: 18 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email sequences (3 role-specific campaigns) | Growth plan: $30/mo for 5,000 emails (https://instantly.ai/pricing) |
| Clay | Contact enrichment + email verification for 150 contacts | Explorer: $149/mo (https://www.clay.com/pricing) |
| LinkedIn | Connection requests and DM sequences (manual or basic) | Free tier sufficient at 50 accounts |
| PostHog | Event tracking and funnel analysis | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Attio | CRM deal and stakeholder tracking | Free tier: up to 3 users (https://attio.com/pricing) |

**Estimated monthly cost:** $179/mo (Instantly $30 + Clay $149)

## Drills Referenced

- `cold-email-sequence` — build and launch the 3 role-specific email sequences in Instantly
- `linkedin-outreach` — run LinkedIn connection + DM sequences for Champion and Influencer contacts
- `multi-channel-cadence` — orchestrate cross-channel timing and coordination rules in n8n
- `posthog-gtm-events` — set up event tracking for multi-threaded outreach metrics
