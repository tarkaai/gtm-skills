---
name: expansion-outreach-sequence
description: Multi-touch sales outreach sequence for usage-limit expansion opportunities, personalized with specific usage data and value framing
category: Deal Management
tools:
  - Loops
  - Intercom
  - Attio
  - Cal.com
  - n8n
fundamentals:
  - loops-transactional
  - loops-sequences
  - intercom-in-app-messages
  - attio-deals
  - attio-notes
  - calcom-booking-links
  - n8n-workflow-basics
  - n8n-scheduling
---

# Expansion Outreach Sequence

This drill builds a multi-touch outreach cadence for expansion opportunities identified by usage-limit signals. Unlike automated upgrade prompts, this sequence is sales-led — each touch references the customer's specific usage data, frames the upsell around business value, and drives toward a conversation with a decision-maker.

## Input

- Qualified expansion opportunities from `expansion-signal-qualification` (account context, usage data, decision-maker info, expansion deal in Attio)
- Loops configured for personalized triggered emails
- Intercom configured for in-app messages
- Cal.com for booking expansion calls

## Steps

### 1. Build the expansion email templates

Using the `loops-transactional` fundamental, create personalized email templates for each touch in the sequence. Every email must include the customer's actual numbers.

**Touch 1: Usage insight (Day 0)**
Subject: "Your {{resource_name}} usage this month"
From: Account owner name (personal, not marketing@)
Body:
- Open with a specific observation: "I noticed your team has used {{current_count}} of {{plan_limit}} {{resource_name}} this billing period — that's {{pct_used}}% of your current plan."
- Frame as a growth signal, not a problem: "This tells me your team is getting real value from {{product_name}}, especially around {{top_use_case}}."
- Introduce the next tier naturally: "Most teams at your usage level move to {{next_tier}} because [specific benefit: unlimited API calls, more seats for growing teams, higher storage for production workloads]."
- CTA: "Want me to walk you through what {{next_tier}} looks like for your team? Here's my calendar: [Cal.com link]"
- No pricing in the first touch. The goal is to start a conversation, not close a deal.

**Touch 2: Value proof (Day 3)**
Subject: "Re: Your {{resource_name}} usage this month"
Body:
- Reference the first email without repeating it.
- Add a proof point: "Teams that upgrade at this stage typically see [concrete outcome — e.g., 40% faster project delivery, 3x API throughput, no more workaround exports]."
- If possible, reference a similar customer: "{{similar_company}} was in the same position — they upgraded to {{next_tier}} and [specific result]."
- Same CTA: Cal.com booking link.

**Touch 3: Urgency + options (Day 7)**
Subject: "Quick question about your {{product_name}} limits"
Body:
- Acknowledge they are busy: "I know you're heads-down — just wanted to flag that at your current rate, you'll hit your {{resource_name}} limit around {{projected_hit_date}}."
- Explain the consequence: "When that happens, [what breaks — API calls rejected, new seats blocked, storage writes fail]."
- Offer options, not just one path: "A few ways to handle this: (1) Upgrade to {{next_tier}} for {{next_tier_limit}} {{resource_name}}, (2) I can extend your current limit temporarily while you evaluate, (3) We can look at annual pricing that saves {{discount_pct}}%."
- CTA: "Which option sounds right? Happy to set up a quick call: [Cal.com link]"

**Touch 4: Final — in-app + email (Day 14)**
Send only if no response to touches 1-3 and the account is still at 85%+ usage.
Email subject: "Last note on your {{resource_name}} limit"
Body: Brief. "Wanted to make sure this does not catch your team off guard. Your {{resource_name}} is at {{pct_used}}%. I have set up a temporary safety net so you will not lose access, but it expires in 7 days. Let me know if you want to discuss — [Cal.com link]."

### 2. Build the in-app message for touch 4

Using the `intercom-in-app-messages` fundamental, create a targeted in-app message that fires alongside the final email:

Type: Banner (persistent)
Audience: Admins and billing contacts on the flagged account
Copy: "Your account owner {{account_owner_name}} has been in touch about your {{resource_name}} limit. Need help? [Reply here] or [Schedule a call]."
CTA primary: Opens an Intercom conversation with the account owner name pre-filled
CTA secondary: Links to the Cal.com booking page

This creates a warm handoff between the email channel and the in-product experience.

### 3. Configure the sequence in n8n

Using `n8n-workflow-basics` and `n8n-scheduling`, build the sequence orchestration:

1. Trigger: Webhook from `expansion-signal-qualification` when a deal moves to "Expansion Qualified" stage
2. Day 0: Send Touch 1 via Loops
3. Day 1-3: Check Attio deal stage — if moved to "Expansion Meeting Booked" or "Expansion Closed," stop the sequence
4. Day 3: Send Touch 2 via Loops (skip if reply detected)
5. Day 4-7: Check for replies via Loops webhook. If reply detected, stop sequence and alert account owner
6. Day 7: Send Touch 3 via Loops (skip if reply or meeting booked)
7. Day 8-14: Monitor for response. If the account upgrades via self-serve during this window, stop sequence and log as "Self-serve conversion during outreach"
8. Day 14: If still no response and usage >= 85%, send Touch 4 email + fire Intercom in-app message
9. Day 21: If no response after 4 touches, move Attio deal to "Expansion Stalled" and add a task for the account owner to attempt a different channel (phone, LinkedIn, etc.)

### 4. Log every touch in the CRM

Using `attio-notes`, log each outreach touch on the expansion deal:

```
Touch {{touchNumber}} sent — {{channel}}
Subject: {{subject}}
Usage at time of send: {{current_count}}/{{plan_limit}} ({{pct_used}}%)
Status: Sent / Opened / Replied / No response
```

This creates a full timeline the account owner can reference before any live conversation.

### 5. Build the booking-to-deal workflow

Using `calcom-booking-links`, create an expansion-specific event type:

- Title: "Usage Expansion Discussion — {{companyName}}"
- Duration: 25 minutes
- Pre-fill: Link the booking to the Attio deal so the account owner has full context
- Post-booking: Automatically move the Attio deal to "Expansion Meeting Booked" and stop the outreach sequence

### 6. Track sequence performance

Using `attio-deals` and `attio-notes`, track per-sequence metrics:

- Touch 1 open rate and reply rate
- Touch 2 reply rate
- Touch 3 reply rate
- Touch 4 reply rate
- Meeting booking rate (bookings / sequences started)
- Expansion close rate (closed deals / sequences started)
- Median days from sequence start to meeting booked
- Median days from sequence start to deal closed
- Self-serve conversion during sequence rate

Feed these metrics to the health monitor drill for reporting.

## Output

- 4-touch email sequence templates in Loops, personalized with usage data
- 1 in-app message template in Intercom for the final touch
- n8n orchestration workflow managing sequence timing and stop conditions
- Cal.com expansion event type with CRM integration
- Full touch logging in Attio per expansion deal

## Triggers

Fires when an expansion deal moves to "Expansion Qualified" in Attio. Runs the 4-touch sequence over 14-21 days. Stops automatically on reply, meeting booking, self-serve upgrade, or deal stage change.
