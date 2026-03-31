---
name: comment-to-dm-cadence
description: Execute the full comment-to-DM conversion sequence from first comment through meeting booked
category: Content
tools:
  - LinkedIn
  - Attio
  - n8n
  - Cal.com
fundamentals:
  - linkedin-organic-engagement
  - linkedin-organic-dms
  - attio-contacts
  - attio-deals
  - calcom-booking-links
  - n8n-workflow-basics
---

# Comment-to-DM Cadence

This drill defines the complete conversion sequence: from your first comment on a prospect's post through to a booked meeting via DM. The key principle is EARNING the right to DM by building visible familiarity through 3-5 touchpoints before the DM ever goes out.

## Input

- Comment tracking log from `comment-crafting` drill (which prospects you have commented on, how many times, and whether they replied)
- ICP definition for qualifying DM targets
- CRM records in Attio for prospect status tracking
- Cal.com booking link for meeting scheduling

## Steps

### 1. Define the cadence stages

Every prospect moves through these stages before receiving a DM:

| Stage | Touches | Duration | Signal to Advance |
|-------|---------|----------|-------------------|
| Cold | 0 comments | - | Prospect identified, added to comment target list |
| Warming | 1-2 comments on their posts | 3-7 days | They liked your comment or you got 5+ likes on the comment |
| Warm | 3-4 comments, at least one author reply | 7-14 days | Author replied to at least one of your comments |
| DM-Ready | 4-5 comments, mutual recognition | 10-21 days | Author replied 2+ times, or sent you a connection request, or commented on YOUR post |
| DM Sent | - | Day of DM | Natural opening exists (author reply, shared context) |
| Conversation | DM exchange active | 1-7 days | They respond to your DM |
| Meeting Booked | - | When ready | They accept a call |

Track each prospect's current stage in Attio using the `attio-contacts` fundamental. Add a custom field `comment_dm_stage` with values matching these stages.

### 2. Execute the warming phase (touches 1-3)

For each prospect in Cold or Warming stage:

1. Comment on their next post using the `comment-crafting` drill
2. Like 1-2 of their other recent posts (puts your name in their notifications)
3. If they have a LinkedIn newsletter, subscribe to it
4. After each comment, update their Attio record: increment touch count, note date, record whether they engaged

Do NOT rush this phase. The temptation is to DM after one good comment exchange. Resist it. Premature DMs feel cold and waste the familiarity you are building.

### 3. Identify DM-ready prospects

A prospect is DM-ready when ANY of these signals appear:

- **They replied to your comments 2+ times** (they recognize your name)
- **They sent you a connection request** (they want to know you)
- **They commented on YOUR post** (they are now in your world)
- **They liked 3+ of your comments** (they notice you consistently)
- **They referenced you or your company in a post** (rare but strongest signal)
- **Mutual connection introduced you** (bypasses the warming phase)

When a prospect becomes DM-ready, update their Attio stage to `dm-ready` and move to Step 4.

### 4. Craft the DM

The DM must reference the shared context from your comment engagement. Never send a generic DM to a warmed prospect -- it wastes all the familiarity you built.

**DM templates (adapt to specific context):**

**After author replied to your comment:**
"Hey {first_name}, really enjoyed our exchange on your post about {topic}. Your point about {specific thing they said} stuck with me -- we have been grappling with exactly that. Curious how you are approaching {related challenge}? Would love to hear more."

**After they commented on YOUR post:**
"Hey {first_name}, thanks for your comment on my post about {topic}. You clearly know this space well. I had a follow-up thought about {point they raised} -- mind if I share?"

**After they sent a connection request:**
"Hey {first_name}, great to connect! I have been enjoying your posts on {their topic}. Your take on {specific post} was especially sharp. What prompted your interest in connecting?"

**Rules for the first DM:**
- Reference a SPECIFIC shared interaction (post, comment, topic)
- Ask a genuine question about THEIR situation
- Do NOT pitch your product
- Do NOT mention what your company does
- Do NOT include a CTA for a meeting
- Keep it to 3-4 sentences
- Send during business hours (9am-5pm in their timezone)

### 5. Run the DM conversation

After the first DM, follow this progression:

**Message 1 (opening DM):** Reference shared context, ask about their situation. See templates above.

**Message 2 (after they reply):** Respond to what they said. Share a relevant insight, experience, or resource. Deepen the conversation. Still no pitch.

**Message 3 (when they describe a problem you solve):** Acknowledge the problem, briefly mention you have seen others solve it (or that your company works in this area), and offer a short call: "We have been working on exactly this. Would a 15-min call make sense? I can share what we have seen work. Here is my calendar if easier: {Cal.com link}"

**If they don't describe a problem:** Continue the conversation. Some prospects take 4-5 DM exchanges before the right moment arises. Do not force a meeting ask. If after 5 exchanges there is no natural opening, the prospect may not have the problem right now -- add them to a nurture list and continue commenting on their posts.

Using the `calcom-booking-links` fundamental, send a direct scheduling link when they agree to a call.

### 6. Log everything in CRM

Using the `attio-contacts` and `attio-deals` fundamentals:

For every DM conversation:
1. Update `comment_dm_stage` to current stage
2. Set `lead_source` = "comment-to-dm"
3. Add a note with: first comment date, total comments before DM, which comment/interaction triggered the DM, DM conversation summary
4. When meeting books, create a Deal record at "Meeting Booked" stage with source attribution

This data feeds the optimization loop: which comment strategies produce the most DM replies? How many touches before a DM? Which prospect tiers convert best?

### 7. Handle common scenarios

**Prospect never replies to comments:** After 5 comments across 3+ weeks with zero engagement, move to the bottom of your target list. They may not be active on LinkedIn or may not engage with comments. Try engaging with their company's posts instead, or find a different contact at the same company.

**Prospect replies to DM but goes cold:** Send one follow-up after 5-7 days: "Hey {name}, just circling back -- no pressure at all. If the timing is not right, I'll keep an eye on your posts. Your content on {topic} is genuinely helpful." Then move them back to a comment-nurture stage.

**Prospect asks what you do in the DM:** Answer honestly and concisely. Do not pivot to a full pitch. "We build {one-line description}. It helps teams like yours {outcome}. But I am more curious about your situation -- what is the biggest challenge you are facing with {area}?"

## Output

- A tracked cadence for each prospect: stage, touch count, dates, and DM status
- DM conversations logged in Attio with full attribution chain
- Meetings booked via Cal.com with source tracking
- Conversion data: comments-to-DM-ready rate, DM-to-reply rate, reply-to-meeting rate

## Triggers

Review prospect stages daily. Send DMs to DM-ready prospects as signals appear (do not batch -- timeliness matters). Log updates in Attio after each interaction. Weekly review of full pipeline: how many prospects at each stage, and what is the average time to progress.
