---
name: linkedin-organic-dms
description: Monitor LinkedIn DMs and connection requests to capture inbound leads from content
tool: LinkedIn
difficulty: Config
---

# Capture LinkedIn DM Leads

## Prerequisites
- LinkedIn account with active posting cadence
- CRM (Attio, HubSpot, etc.) to log captured leads
- Optional: n8n for automation, Clay for enrichment

## Why This Matters

When a founder posts thought leadership content on LinkedIn, the highest-intent signal is a DM or connection request with a message. These are warm leads who self-selected based on your content. Capturing and routing them quickly is the difference between converting interest and losing it.

## Steps

### 1. Set up DM monitoring via LinkedIn Messaging API

LinkedIn's Messaging API is restricted to approved apps (LinkedIn partners). For most founders, manual DM checking or Taplio's DM management feature is the practical path.

**If you have LinkedIn API messaging access:**
```
GET https://api.linkedin.com/rest/conversations?q=participant&participant=urn:li:person:{MEMBER_ID}
Authorization: Bearer {ACCESS_TOKEN}
LinkedIn-Version: 202401
```
Returns recent conversations. Filter for new/unread messages.

**If you do not have API access (most cases):**
Use one of these approaches:

### 2. Option A: Taplio DM monitoring

Taplio surfaces DMs from people who engaged with your content. Check the Taplio inbox daily. When a new DM arrives from someone who commented on or liked a recent post:
1. Categorize the DM: question, compliment, partnership inquiry, or buying signal
2. Respond within 4 hours (same business day)
3. If buying signal, move to step 4

### 3. Option B: n8n webhook + manual trigger

Create an n8n workflow triggered by a manual webhook. When you receive a DM that is a lead:
1. Trigger the webhook with the person's LinkedIn profile URL, message text, and your classification (lead/not-lead)
2. n8n enriches the person via Clay (see `clay-people-search` fundamental):
   ```
   POST https://api.clay.com/v1/tables/{TABLE_ID}/rows
   {
     "linkedin_url": "https://www.linkedin.com/in/{handle}",
     "source": "linkedin-dm",
     "original_message": "Their DM text"
   }
   ```
3. n8n creates or updates the contact in Attio (see `attio-contacts` fundamental):
   ```
   POST https://api.attio.com/v2/objects/people/records
   {
     "data": {
       "values": {
         "name": [{"first_name": "...", "last_name": "..."}],
         "linkedin_url": [{"value": "..."}],
         "lead_source": [{"value": "linkedin-content"}]
       }
     }
   }
   ```

### 4. Qualify and respond to DM leads

When a DM contains a buying signal (asks about pricing, describes a problem you solve, requests a demo):

1. **Reply within 4 hours.** Acknowledge their message, reference the post they engaged with, and ask one qualifying question: "Happy to chat more -- what's your current setup for [problem area]?"

2. **Do not pitch in the DM.** The goal is to move to a call. After 1-2 message exchanges, offer: "Would it be helpful to jump on a 15-min call? Here's my calendar: [Cal.com link]"

3. **Log in CRM.** Create a lead record with:
   - Source: `linkedin-content`
   - First touch: the post they engaged with
   - DM text: their original message
   - Status: `responded` or `meeting-booked`

### 5. Monitor connection requests with messages

LinkedIn connection requests with a note are another lead signal. Check pending invitations daily. Accept requests from people who match your ICP. If their note references your content or describes a problem you solve, send a welcome DM:

"Thanks for connecting, [name]! Glad that post on [topic] resonated. What are you working on?"

This opens a conversation without being pushy.

### 6. Track DM-to-meeting conversion

In PostHog or your CRM, track:
- `linkedin_dm_received` (all inbound DMs from content)
- `linkedin_dm_qualified` (DMs with buying signals)
- `linkedin_dm_meeting_booked` (DMs that became calls)
- `linkedin_dm_deal_created` (calls that became pipeline)

This attribution chain proves the ROI of founder LinkedIn content.

## Error Handling

- **LinkedIn message limits**: LinkedIn limits messaging for free accounts. With Sales Navigator or Premium, limits are higher. If you hit limits, prioritize responding to highest-intent DMs first.
- **Spam DMs**: Not every DM is a lead. Ignore recruiters, salespeople pitching you, and generic "great post!" messages with no substance. Only log DMs where the person has a problem you can solve.
