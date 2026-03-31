---
name: apollo-sequences
description: Set up multi-step outreach sequences in Apollo
tool: Apollo
difficulty: Intermediate
---

# Create Outreach Sequences in Apollo

## Prerequisites
- Apollo account with sequence access (paid plan)
- Verified sending email connected to Apollo
- Contact list ready for outreach

## Steps

1. **Create a new sequence via API.** Use the Apollo API to create a sequence. Name it with campaign context (e.g., "Q1 DevTools VP Eng - Pain Point"). Select your sending mailbox and set the sequence to run on weekdays only, between 8am-11am in the recipient's timezone.

2. **Build your email steps.** Add 3-4 email steps for a standard outbound sequence. Step 1: personalized cold email (day 0). Step 2: value-add follow-up (day 3). Step 3: social proof or case study (day 7). Step 4: breakup email (day 14). Keep each email under 150 words.

3. **Add manual tasks.** Between email steps, add manual LinkedIn tasks: "View profile" (day 1), "Connect with note" (day 4), "Comment on recent post" (day 8). This multi-channel approach increases reply rates by 2-3x over email-only.

4. **Configure sequence settings.** Set daily send limits per mailbox (30-50 for warmed accounts). Enable "Stop on reply" so prospects who respond are automatically removed. Set "Stop on bounce" to protect sender reputation.

5. **Add contacts to the sequence.** Import contacts from your Apollo saved search or upload a CSV. Apollo will deduplicate against contacts already in active sequences to prevent double-messaging.

6. **Monitor performance.** After the first 50 sends, check open rate (target >50%), reply rate (target >5%), and bounce rate (keep under 3%). If bounce rate exceeds 3%, pause and re-verify your list.
