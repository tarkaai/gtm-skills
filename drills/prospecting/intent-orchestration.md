---
name: intent-orchestration
description: Build a real-time signal-to-outreach pipeline that automatically triggers personalized multi-channel sequences when intent scores cross thresholds
category: Prospecting
tools:
  - n8n
  - Clay
  - Attio
  - Instantly
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - clay-intent-scoring
  - clay-enrichment-waterfall
  - clay-claygent
  - attio-deals
  - attio-lists
  - instantly-campaign
  - instantly-reply-detection
  - posthog-custom-events
  - posthog-feature-flags
---

# Intent Orchestration

This drill builds the 10x multiplier: instead of agents monitoring dashboards and manually prioritizing accounts, intent orchestration automatically triggers the right outreach to the right account at the right time based on their intent score. When a company crosses into Hot tier, outreach fires within minutes — not days.

## Input

- Working intent signal automation (from `intent-signal-automation` drill)
- Calibrated intent score model with proven Hot/Warm/Cool/Cold thresholds
- Instantly account with warmed-up sending domains and proven email templates
- At least 4 weeks of Baseline-level data showing intent-based outreach outperforms cold outreach

## Steps

### 1. Build the Hot-tier instant outreach workflow

Create an n8n workflow that fires when any account crosses into Hot tier:

**Trigger:** Attio webhook — fires when `intent_tier` changes to "Hot"

**Flow:**
1. **Attio GET** — pull the full account record: company domain, contacts, signals that fired, previous interactions
2. **Dedup gate** — check if this account received outreach in the last 14 days. If yes, skip (prevent over-contacting). If no, proceed.
3. **Clay Claygent node** — using `clay-claygent`, generate a one-line personalization for the top contact based on their specific intent signals. Example prompt: "This company visited our pricing page 3 times and compared us on G2. Their VP Engineering just posted about scaling their dev team. Write a one-line opener that connects their situation to our product without mentioning we know they visited our site."
4. **Instantly campaign node** — using `instantly-campaign`, add the contact to a Hot-tier email sequence. The sequence uses the AI-generated personalization in the first line, followed by your proven email template.
5. **PostHog log** — fire `intent_outreach_triggered` with properties: company_domain, intent_score, tier, signals, outreach_channel, personalization_used
6. **Attio update** — set `last_outreach_date` and `outreach_status` = "sequence_active" on the contact record

### 2. Build the Warm-tier batch outreach workflow

Create an n8n workflow that runs daily at 9am:

**Trigger:** n8n cron, daily 9:00 AM

**Flow:**
1. **Attio query** — pull all accounts with `intent_tier` = "Warm" AND `outreach_status` != "sequence_active" AND `last_outreach_date` is null or older than 30 days
2. **Batch limit** — process a maximum of 20 accounts per day to stay within sending limits
3. **Clay enrichment** — using `clay-enrichment-waterfall`, verify email addresses and fill any missing contact data
4. **Clay Claygent** — generate batch personalizations for all 20 accounts
5. **Instantly campaign** — add contacts to a Warm-tier email sequence (less aggressive cadence: 4-day gaps instead of 2-day)
6. **PostHog + Attio logging** — same as Hot-tier workflow

### 3. Build the score-change outreach modifier

Create an n8n workflow that adjusts active sequences when intent scores change:

**Trigger:** Attio webhook — fires when `intent_score` changes

**Flow:**
1. **Score direction check** — compare new score to previous score
2. **Upgrade path** — if score increased and crossed a tier boundary (e.g., Warm -> Hot):
   - Move the contact from Warm-tier sequence to Hot-tier sequence in Instantly
   - Add a contextual follow-up referencing the new signal: "I noticed your team has been looking into [topic]..."
   - Send Slack alert to founder
3. **Downgrade path** — if score decreased below Cool threshold while in active sequence:
   - Pause the Instantly sequence for this contact
   - Log as `intent_score_decay_pause` in PostHog
   - Move account back to monitoring-only in Attio

### 4. Build the reply-to-action routing

Create an n8n workflow that handles responses:

**Trigger:** Instantly webhook — reply detected

**Flow:**
1. **Sentiment classification** — using `instantly-reply-detection`, classify: positive (interested/meeting), neutral (question/more info), negative (not interested/unsubscribe)
2. **Positive route** — create Attio deal at "Meeting Requested" stage. Send Slack notification with reply text. Pause the sequence for this contact.
3. **Neutral route** — flag for manual follow-up within 4 hours. Pause sequence. Create Attio task assigned to founder.
4. **Negative route** — remove from all sequences. Update Attio with opt-out flag. Log `intent_outreach_rejected` in PostHog.

### 5. Set up A/B testing on personalization

Using `posthog-feature-flags`, create an experiment:
- **Control:** Static email templates (proven copy from Baseline)
- **Variant:** AI-personalized first lines generated by Clay Claygent

Route 50% of Hot-tier outreach to each variant. After 100 sends per variant, compare reply rates. If AI personalization wins by 2+ percentage points with statistical significance, make it the default.

### 6. Scale volume controls

Configure rate limits across the orchestration:
- Maximum 50 Hot-tier outreach emails per day
- Maximum 20 Warm-tier outreach emails per day
- Maximum 1 email per contact per 48 hours across all sequences
- Maximum 3 total touches per contact per 14-day period (across email + LinkedIn)
- If daily Hot-tier volume exceeds 50, queue overflow for next business day (do not increase sending limits)

## Output

- Real-time Hot-tier outreach pipeline (signal to email in under 30 minutes)
- Daily Warm-tier batch outreach
- Dynamic sequence adjustment based on score changes
- Reply routing with sentiment classification
- A/B testing on personalization strategy
- Full PostHog event trail for every orchestration action

## Triggers

- Hot-tier: real-time (webhook from Attio tier change)
- Warm-tier: daily batch (9am cron)
- Score changes: real-time (webhook from Attio score update)
- Replies: real-time (webhook from Instantly)
