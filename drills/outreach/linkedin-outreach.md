---
name: linkedin-outreach
description: Run a structured LinkedIn connection and messaging sequence to book meetings with target prospects
category: Outreach
tools:
  - LinkedIn
  - Attio
  - Clay
fundamentals:
  - linkedin-organic-engagement
  - linkedin-organic-engagement
  - attio-deals
---

# LinkedIn Outreach

This drill sets up a repeatable LinkedIn outreach workflow: connect, engage, message, and convert. It works best paired with the `cold-email-sequence` drill as a parallel channel.

## Prerequisites

- LinkedIn profile optimized for your buyer persona (headline speaks to their pain, not your title)
- Clay table with LinkedIn URLs for target prospects
- Attio workspace for tracking conversations

## Steps

### 1. Segment your prospect list

Pull your scored prospect list from Clay and filter to LinkedIn-ready contacts (those with valid LinkedIn URLs). Segment into tiers: Tier 1 (highest-fit, personalize heavily), Tier 2 (good fit, use templates with light customization), Tier 3 (warm the connection, engage later).

### 2. Pre-engagement warm-up

Before sending connection requests, engage with your Tier 1 prospects organically. Like 2-3 of their recent posts. Leave a thoughtful comment on something they shared. Follow their company page. This makes your name familiar before the connection request arrives. Spend 15 minutes daily on this for one week before outreach begins.

### 3. Send connection requests

Using the `linkedin-organic-engagement` fundamental, send personalized connection requests. Keep the note under 200 characters. Reference something specific: a post they wrote, a mutual connection, a shared interest, or a signal (new role, funding). Never pitch in the connection request. Send 15-20 per day maximum to avoid LinkedIn restrictions.

### 4. Build the messaging sequence

Once connected, use the `linkedin-organic-engagement` fundamental to run a 3-message sequence over 10-14 days:

- **Message 1 (Day 1 after accept)**: Thank them for connecting. Ask a genuine question about their work or a topic they post about. No pitch.
- **Message 2 (Day 5)**: Share something useful: a relevant article, a data point, or an observation about their industry. Tie it loosely to the problem your product solves.
- **Message 3 (Day 10)**: Direct but low-pressure CTA. Suggest a 15-minute conversation about the topic you have been discussing. Offer specific times.

### 5. Handle responses

Positive responses: move to scheduling in Attio using the `attio-deals` fundamental. Create a deal at the "Meeting Booked" stage. Negative or no response: tag in Attio and add to a long-term nurture list. Never send more than 3 unreplied messages.

### 6. Track and optimize

Log connection acceptance rate, response rate per message, and meeting conversion rate. Benchmark: 30%+ acceptance, 15%+ response, 5%+ meeting rate. If below benchmarks, revisit your profile, connection note, or messaging copy.
