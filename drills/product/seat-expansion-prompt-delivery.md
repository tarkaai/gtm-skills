---
name: seat-expansion-prompt-delivery
description: Deliver contextual seat expansion prompts via in-app messages, email, and sales routing based on account tier and expansion readiness
category: Product
tools:
  - Intercom
  - Loops
  - Attio
  - PostHog
  - n8n
fundamentals:
  - intercom-in-app-messages
  - loops-transactional
  - loops-sequences
  - attio-deals
  - attio-lists
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-triggers
---

# Seat Expansion Prompt Delivery

This drill takes the output from `seat-growth-signal-detection` and delivers the right expansion prompt at the right moment through the right channel. The prompt is contextual — it references the specific signal that triggered it (e.g., "You just invited a colleague but your plan has no remaining seats") rather than showing a generic "Upgrade now" banner.

## Input

- Webhook payload from `seat-growth-signal-detection` containing: account_id, expansion_tier, score, current_seat_count, seat_limit, top_signal
- Attio account data (plan tier, MRR, account owner, lifecycle stage)
- Intercom configured for in-app messaging
- Loops configured for triggered emails

## Steps

### 1. Enrich the expansion signal with account context

When the n8n webhook receives an expansion signal, pull account context from Attio using the `attio-deals` fundamental:

- Account plan tier (free, starter, pro, enterprise)
- Monthly recurring revenue (MRR)
- Account owner (CSM or AE if assigned)
- Days since signup
- Previous expansion prompt history (have we already prompted this account recently?)
- Current seat count and limit

Apply a cooldown rule: do not send a second expansion prompt within 14 days of the last one unless the account moves from warm to hot tier. Check `last_expansion_prompt_date` in Attio before proceeding.

### 2. Route by expansion tier and account value

Build routing logic in n8n using `n8n-workflow-basics`:

**Hot tier (score >= 40) — immediate, multi-channel:**
- If self-serve eligible (MRR < $500): In-app message via Intercom + email via Loops
- If sales-assisted (MRR $500-$2000): In-app message + email + create Attio expansion deal
- If enterprise (MRR > $2000): Create urgent Attio expansion deal + Slack alert to account owner + personal email draft

**Warm tier (score 20-39) — single-channel, timed:**
- Wait for the user's next login, then show in-app message via Intercom
- If user does not log in within 48 hours, send an email via Loops
- Do not create sales deals for warm — let the prompt do the work

### 3. Build contextual in-app messages

Using the `intercom-in-app-messages` fundamental, create messages tied to the specific signal. Each message should feel like a helpful suggestion, not a sales pitch.

**For `team_invite_failed` (most urgent):**
Type: Modal (blocks the action path since they literally cannot add more users)
Copy: "Your team has reached its {{seatLimit}}-seat limit. Add more seats to bring {{inviteeName}} on board."
CTA: "Add seats now" → links directly to the seat purchase page with the invite pre-queued
Secondary CTA: "Maybe later" → dismisses but logs the event

**For `seat_limit_hit` (approaching limit):**
Type: Banner (non-blocking, persistent until dismissed)
Copy: "You are using {{currentSeats}} of {{seatLimit}} seats. Add more before your team hits the limit."
CTA: "View plans" → links to billing page

**For `team_invite_sent` with remaining seats (growth signal):**
Type: Tooltip (appears when they return to team settings)
Copy: "Your team is growing! Teams with {{currentSeats + 2}}+ members unlock collaborative features like [specific feature]."
CTA: "Explore team plans" → links to pricing comparison

**For collaboration signals (`mention_non_member`, `resource_shared_external`):**
Type: Post (subtle, in the Intercom Messenger)
Copy: "Looks like you are collaborating with people outside your {{productName}} account. Adding them as team members makes sharing easier — no more exports and email attachments."
CTA: "Invite your team" → links to the invite page

### 4. Build contextual email templates

Using the `loops-transactional` fundamental, create email templates for each signal category:

**Template: seat-expansion-limit-hit**
Subject: "{{firstName}}, your team is out of seats"
Body: Reference the specific blocked action. Show current seat usage ({{currentSeats}}/{{seatLimit}}). Explain what adding seats unlocks. Include a one-click add-seats link. Show the per-seat price clearly.

**Template: seat-expansion-growth**
Subject: "Your {{productName}} team is growing"
Body: Reference collaboration activity (e.g., "You shared 12 resources with external collaborators this week"). Suggest adding those collaborators as team members. Highlight the collaboration features they would unlock. Include a link to the invite page.

**Template: seat-expansion-personal (for high-MRR accounts)**
Subject: "Quick note about your team's growth — {{accountOwnerName}}"
Body: Written as a personal note from the CSM. Reference specific usage patterns. Offer to set up a call to discuss team expansion options. Include a Cal.com booking link.

Using `loops-sequences`, create a 2-email follow-up sequence for accounts that receive a prompt but do not act:
- Day 0: Signal-specific template (above)
- Day 5: "Still thinking about adding seats? Here's how other teams of your size use {{productName}}" — include a mini case study or social proof

### 5. Build sales routing for high-value accounts

Using `attio-deals`, create expansion opportunities for accounts that qualify for sales-assisted expansion:

1. Create an expansion deal in Attio with:
   - Deal name: "Seat Expansion — {{companyName}}"
   - Stage: "Expansion Identified"
   - Value: estimated additional MRR (additional seats x per-seat price)
   - Context note: expansion score, top signals, current seat utilization, days since last login
2. Assign to the account owner (CSM or AE)
3. Include a pre-drafted email the owner can personalize

Using `attio-lists`, maintain a list called "Seat Expansion — Sales Action" that auto-populates with all expansion deals in the "Expansion Identified" stage.

### 6. Track prompt performance

Using `posthog-custom-events`, track the full expansion prompt funnel:

```javascript
// When expansion prompt is delivered
posthog.capture('seat_expansion_prompt_shown', {
  account_id: accountId,
  expansion_tier: 'hot',
  channel: 'in_app',  // in_app | email | sales
  prompt_type: 'team_invite_failed',
  current_seats: 4,
  seat_limit: 5
});

// When user clicks the CTA
posthog.capture('seat_expansion_prompt_clicked', {
  account_id: accountId,
  channel: 'in_app',
  prompt_type: 'team_invite_failed',
  cta: 'add_seats_now'
});

// When seats are actually added
posthog.capture('seats_added', {
  account_id: accountId,
  previous_seats: 5,
  new_seats: 8,
  seats_added: 3,
  source: 'expansion_prompt',
  prompt_type: 'team_invite_failed',
  days_from_prompt: 0
});

// When prompt is dismissed without action
posthog.capture('seat_expansion_prompt_dismissed', {
  account_id: accountId,
  channel: 'in_app',
  prompt_type: 'team_invite_failed'
});
```

Calculate weekly: prompts shown by channel, click-through rate by prompt type, conversion rate (seats added / prompts shown), average seats added per conversion, revenue impact (additional MRR from seat additions). Feed this data back to optimize prompt copy, timing, and routing rules.

## Output

- n8n routing workflow that processes expansion signals and dispatches contextual prompts
- 4 Intercom in-app message templates (modal, banner, tooltip, post) tied to specific signals
- 3 Loops email templates and a 2-email follow-up sequence
- Attio expansion deal creation for high-value accounts
- Full funnel tracking from signal detection through seat addition

## Triggers

Fires automatically when `seat-growth-signal-detection` sends a webhook. Runs for each individual account flagged. Respects a 14-day cooldown per account (no duplicate prompts within 14 days unless tier escalates from warm to hot).
