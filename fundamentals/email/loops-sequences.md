---
name: loops-sequences
description: Build automated email sequences triggered by user actions in Loops
tool: Loops
difficulty: Intermediate
---

# Create Automated Sequences in Loops

## Prerequisites
- Loops audience with contact properties and events configured (see `fundamentals/email/loops-audience`)
- Email templates designed for your brand

## Steps

1. **Plan your sequence map.** Before building, map out which sequences each user type receives. Core sequences: Welcome/Onboarding (all signups), Trial-to-Paid (trial users), Feature Adoption (new users), Re-engagement (inactive users), Upgrade Prompt (free users hitting limits). No user should receive more than one sequence at a time.

2. **Create a welcome sequence.** Go to Loops > Loops (sequences) > New Loop. Trigger: "Contact created" event. Build 4-5 emails over 14 days. Email 1 (day 0): Welcome + quickstart. Email 2 (day 1): Key feature highlight. Email 3 (day 3): Use case example. Email 4 (day 7): Social proof. Email 5 (day 14): Check-in + help offer.

3. **Add conditional branches.** Use Loops' branching logic to personalize sequences. After Email 2, check if "onboarding_complete" is true. If yes, skip to feature adoption content. If no, send a help email with setup guide. This prevents sending irrelevant emails.

4. **Set timing and delays.** Use relative delays (days since previous email), not fixed dates. Space emails 2-3 days apart to avoid overwhelming users. Avoid sending on weekends for B2B audiences.

5. **Configure exit conditions.** Set rules for when contacts leave a sequence: "user upgraded plan" exits the trial sequence, "onboarding_complete becomes true" exits onboarding sequence. This prevents mismatched messaging.

6. **Test before launching.** Send yourself through each sequence using a test contact. Verify timing, personalization variables, and branch logic. Check that exit conditions fire correctly by updating the test contact's properties mid-sequence.
