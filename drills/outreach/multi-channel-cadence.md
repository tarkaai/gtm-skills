---
name: multi-channel-cadence
description: Orchestrate a synchronized outreach cadence across email, LinkedIn, phone, and direct mail
category: Outreach
tools:
  - Instantly
  - LinkedIn
  - Attio
  - n8n
  - PostHog
fundamentals:
  - instantly-campaign-setup
  - linkedin-messaging-sequence
  - n8n-workflow-patterns
  - attio-deal-tracking
  - posthog-event-tracking
---

# Multi-Channel Cadence

This drill builds a coordinated outreach sequence that uses email, LinkedIn, phone, and optionally direct mail in a single cadence. Multi-channel outreach consistently outperforms single-channel because prospects see you in multiple contexts, building familiarity and credibility.

## Prerequisites

- Completed `cold-email-sequence`, `linkedin-outreach`, and `cold-call-framework` drills
- Prospect list enriched with email, LinkedIn URL, and phone number
- n8n instance connected to Attio and Instantly
- 14-day window dedicated to running the cadence

## Steps

### 1. Design the cadence timeline

Map out 14 days of coordinated touches across channels. A proven pattern:

- **Day 1**: LinkedIn connection request (warm the name)
- **Day 2**: Cold email #1 (problem-aware opener)
- **Day 4**: Engage with their LinkedIn content (like/comment)
- **Day 5**: Cold email #2 (value angle)
- **Day 7**: Phone call attempt #1
- **Day 8**: LinkedIn message #1 (if connected)
- **Day 10**: Cold email #3 (soft CTA)
- **Day 12**: Phone call attempt #2
- **Day 14**: Breakup email + LinkedIn message #2

Each touch references or builds on the previous one without being repetitive.

### 2. Build the orchestration workflow

Using the `n8n-workflow-patterns` fundamental, create a master workflow that coordinates timing across channels. The workflow should: trigger each step on schedule, check Attio for replies or status changes before proceeding (do not call someone who already replied to email), and pause the cadence instantly when a prospect engages positively on any channel.

### 3. Set up channel-specific sequences

Configure each channel using its respective fundamental:

- Email: Use `instantly-campaign-setup` to build the email steps
- LinkedIn: Follow the `linkedin-messaging-sequence` fundamental for connection and message steps
- Phone: Use your call block schedule from `cold-call-framework`

Ensure messaging is consistent across channels but not identical. Same core value proposition, different angles.

### 4. Configure cross-channel triggers

Using the `attio-deal-tracking` fundamental, set up status updates that flow across channels. If a prospect opens email 3 times, bump up the phone call priority. If they accept a LinkedIn connection, adjust the email tone to be warmer. If they reply negatively on any channel, stop all channels immediately.

### 5. Add personalization layers

Each channel should reference the others subtly. Email: "I also sent you a connection request on LinkedIn — would love to connect." Phone: "I sent you a note last week about [topic] — wanted to put a voice to it." LinkedIn: "Following up on my email — thought this was easier." This shows persistence without being robotic.

### 6. Measure channel attribution

Track which channel drives the conversion using `posthog-event-tracking`. Log every touch with channel, step number, and timestamp. When a meeting books, attribute it to the last touch and the first touch. Review weekly: which channel combination produces the highest meeting rate? Adjust cadence timing and channel mix based on data.
