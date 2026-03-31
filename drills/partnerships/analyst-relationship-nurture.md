---
name: analyst-relationship-nurture
description: Maintain ongoing analyst and consultant relationships through automated update cadences, content sharing, and re-briefing triggers
category: Outreach
tools:
  - n8n
  - Attio
  - Loops
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - attio-contacts
  - attio-lists
  - attio-automation
  - loops-sequences
  - posthog-custom-events
---

# Analyst Relationship Nurture

This drill builds the always-on system for maintaining analyst and consultant relationships after the initial briefing. Analysts forget vendors who go silent. This nurture cadence keeps you top-of-mind without being annoying.

## Input

- Analyst contact records in Attio with completed briefings (Briefing Status: "Briefed")
- Company news, product updates, and milestone announcements
- PostHog tracking configured for analyst interactions

## Steps

### 1. Define the nurture cadence

Analysts and consultants need a different cadence than sales prospects. Too frequent is worse than too infrequent. Standard cadence:

- **Quarterly update email:** Share 2-3 bullet points of significant news (new customers, product launches, funding, metrics milestones). No fluff. Analysts value signal over volume.
- **Ad-hoc update on major milestones:** Funding round, major customer win, product pivot, market expansion. Send within 48 hours of the event.
- **Annual re-briefing request:** Offer a 30-minute update meeting once per year. Tie it to something new worth discussing.
- **Content sharing (opportunistic):** When you publish research, data, or thought leadership relevant to their coverage, share it directly. Not every blog post — only substantive content.

### 2. Build the quarterly update automation in n8n

Use the `n8n-workflow-basics` fundamental to create a workflow:

**Trigger:** Cron schedule — first Monday of each quarter (January, April, July, October) at 9am.

**Steps:**
1. Query Attio (via `attio-lists`) for all contacts in the "Analyst Briefing Targets" list with Briefing Status = "Briefed"
2. For each analyst, pull the latest company metrics and news from a designated Attio note (or a Google Sheet maintained by the team)
3. Generate a personalized quarterly update email using Claude API:
   - Reference the analyst by name
   - Mention their coverage area
   - Share 2-3 updates relevant to their focus
   - Close with: "Happy to schedule a follow-up briefing if any of this is worth discussing."
4. Send via Loops using the `loops-sequences` fundamental (create a "Analyst Quarterly Update" sequence)
5. Log the send as a PostHog event: `analyst_update_sent` with properties: analyst_name, analyst_tier, quarter

**Human action required:** Before each quarterly send, review the update content. Ensure metrics are current and approved for external sharing.

### 3. Build milestone notification triggers in n8n

Use the `n8n-triggers` fundamental to create event-driven workflows:

**Trigger A — Funding announcement:**
When a "funding_announced" event is logged in PostHog, trigger: generate a tailored announcement email for each briefed analyst, queue for human review, then send.

**Trigger B — Major customer win:**
When a deal in Attio is marked "Won" and tagged "Logo-worthy," trigger: draft a brief note to relevant analysts mentioning the win (with customer permission).

**Trigger C — Product launch:**
When a "product_launched" event fires in PostHog, trigger: generate a product update email with relevance to each analyst's coverage area, queue for review, send.

### 4. Track analyst engagement

Use the `posthog-custom-events` fundamental to track:
- `analyst_update_sent` — quarterly or ad-hoc update sent
- `analyst_update_opened` — email opened (via Loops tracking)
- `analyst_briefing_requested` — analyst asks for a follow-up briefing
- `analyst_referral_received` — analyst refers a prospect to you
- `analyst_mention_detected` — analyst mentions your company in published content

Create an Attio automation using the `attio-automation` fundamental: when an analyst has not engaged (no opens, no replies) for 2 consecutive quarters, change their Briefing Status to "Re-engage" and trigger a re-introduction workflow.

### 5. Build the re-briefing pipeline

For analysts with Briefing Status = "Re-engage" or those approaching the 12-month mark since last briefing:
- Generate a re-briefing request using the `briefing-deck-preparation` drill
- Position it as: "It has been [X months] since our last conversation. We have [major change]. Worth 30 minutes to update you?"
- Queue the request for human review and send

### 6. Monitor relationship health

Build an Attio list view showing analyst relationship health:
- **Healthy:** Engaged in last quarter (opened update or had interaction)
- **Cooling:** No engagement in 1-2 quarters
- **Cold:** No engagement in 3+ quarters
- **Active:** Currently in briefing or follow-up conversation

Alert the team weekly if any Priority 1 analyst moves from Healthy to Cooling.

## Output

- Automated quarterly update emails to all briefed analysts
- Event-driven milestone notifications
- Relationship health tracking in Attio
- Re-briefing pipeline for disengaged analysts
- PostHog events tracking all analyst interactions

## Triggers

- Quarterly update: automated via n8n cron
- Milestone notifications: automated via PostHog event triggers
- Re-briefing: triggered when analyst hits 12-month mark or "Re-engage" status
