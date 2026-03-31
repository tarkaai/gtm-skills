---
name: instantly-reply-detection
description: Classify and route replies from cold email campaigns
tool: Instantly
difficulty: Intermediate
---

# Handle Replies in Instantly

## Prerequisites
- Active campaign with incoming replies
- CRM configured for deal creation (see `fundamentals/crm/attio-deals`)

## Steps

1. **Check the Unibox.** Instantly's Unibox aggregates replies across all sending accounts into one inbox. Check it at least twice daily during active campaigns (morning and afternoon). Reply speed matters -- responding within 1 hour doubles your meeting booking rate.

2. **Classify replies.** Tag each reply with a category: Interested (wants to learn more or book a call), Not Now (timing is wrong but not negative), Not Interested (polite decline), Out of Office (auto-reply), Unsubscribe (remove request), Wrong Person (referred elsewhere). Instantly's AI can auto-classify but always verify.

3. **Handle interested replies.** Respond within 1 hour with a short message proposing 2-3 specific meeting times (or a Cal.com link). Create a deal in your CRM immediately with stage "Meeting Requested" (see `fundamentals/crm/attio-deals`). Remove the contact from all other active sequences.

4. **Handle "Not Now" replies.** Reply acknowledging their timing and ask permission to follow up in a specific timeframe (e.g., "Mind if I check back in Q2?"). Add a reminder in your CRM for the follow-up date. Remove from current sequence.

5. **Handle unsubscribe requests.** Remove the contact immediately from all campaigns. Add them to your global suppression list in Instantly. This is both a legal requirement (CAN-SPAM) and protects your sender reputation.

6. **Automate reply routing with n8n.** At Scalable level, connect Instantly's webhook to an n8n workflow (see `fundamentals/automation/n8n-email-integration`) that auto-classifies replies using AI and creates CRM records for positive responses.
