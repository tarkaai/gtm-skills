---
name: hackathon-attendee-nurture
description: Post-hackathon multi-touch nurture that segments participants by engagement depth and routes high-intent developers to pipeline
category: Events
tools:
  - Loops
  - Attio
  - n8n
  - PostHog
  - Loom
fundamentals:
  - loops-sequences
  - loops-audience
  - attio-contacts
  - attio-lists
  - attio-deals
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
  - loom-recording
---

# Hackathon Attendee Nurture

This drill builds the post-hackathon follow-up system that converts hackathon participants into active product users and pipeline. It segments participants by their engagement depth during the hackathon and runs differentiated nurture sequences for each segment.

## Prerequisites

- Completed hackathon with participant and submission data (from `hackathon-challenge-pipeline` drill)
- Loops account with sequences configured
- Attio workspace with hackathon-related lists
- n8n instance for trigger-based automation
- PostHog tracking events from the hackathon

## Steps

### 1. Segment participants by engagement tier

Within 24 hours of the hackathon closing, classify every participant into one of five tiers using `attio-lists`:

- **Tier 1 -- Winners**: Placed in the top 3. Highest product familiarity and public visibility.
- **Tier 2 -- Submitters (strong)**: Submitted a project that scored above median quality and used 3+ product features. High technical engagement.
- **Tier 3 -- Submitters (basic)**: Submitted a project but with minimal product usage or below-median quality. Showed effort but need more education.
- **Tier 4 -- Registered, no submission**: Signed up and possibly attended the kickoff but did not submit. Interest signal without follow-through.
- **Tier 5 -- Mentors and judges**: External experts who participated. Potential advocates or influencer partners, not direct leads.

Using `attio-contacts`, tag each participant with the hackathon slug, date, and their tier. Add submission URL, quality score, and API usage metrics.

### 2. Build tier-specific nurture sequences in Loops

Using `loops-sequences`, create five sequences:

**Tier 1 sequence -- Winners (4 emails over 14 days):**
- Email 1 (within 6 hours): Congratulations with prize fulfillment details. CTA: "We would love to feature your project -- reply if interested." Include a link to extended free-tier access or upgraded product credits.
- Email 2 (day 3): "Your project in the spotlight" -- offer to co-write a blog post or record a demo video of their winning project. Use `loom-recording` to send a personalized 60-second video congratulating them and previewing the collaboration opportunity.
- Email 3 (day 7): Invite to join a developer advisory board or beta program. CTA: book a call via Cal.com to discuss ongoing partnership.
- Email 4 (day 14): Share what other winners have built since their hackathon. CTA: upgrade to a paid plan with a winner-exclusive discount.

**Tier 2 sequence -- Strong submitters (3 emails over 10 days):**
- Email 1 (within 12 hours): Thank you + recording of awards ceremony. Highlight their project by name. CTA: "Keep building -- here is 3 months of free Pro access."
- Email 2 (day 4): Tutorial or documentation link for the product features they used most heavily (personalize based on API usage data). CTA: "Need help taking your project further? Book office hours."
- Email 3 (day 10): Invite to the next hackathon or developer event. CTA: book a product demo to explore features they did not use during the hackathon.

**Tier 3 sequence -- Basic submitters (3 emails over 10 days):**
- Email 1 (within 12 hours): Thank you + recording of awards ceremony. CTA: "See the winning projects for inspiration."
- Email 2 (day 4): Getting-started tutorial focused on the features they struggled with (personalize based on submission quality data). CTA: "Follow this tutorial and reply with what you build."
- Email 3 (day 10): Invite to the next hackathon with a "level up" framing. CTA: join the developer community Discord/Slack.

**Tier 4 sequence -- Registered, no submission (2 emails over 7 days):**
- Email 1 (within 24 hours): "Sorry we missed your submission" + recording of awards ceremony and winning project demos. CTA: "Check out what others built and try the quickstart yourself."
- Email 2 (day 7): Invite to the next hackathon with "start early" framing -- share starter templates and resources now. CTA: register for the next event.

**Tier 5 sequence -- Mentors and judges (2 emails over 7 days):**
- Email 1 (within 24 hours): Thank you for contributing. Share event metrics (participants, submissions, quality highlights). CTA: "Interested in mentoring again or co-hosting the next one?"
- Email 2 (day 7): Share the published blog post or recap. CTA: connect on LinkedIn and explore partnership opportunities.

### 3. Build automation triggers in n8n

Using `n8n-triggers` and `n8n-workflow-basics`, create workflows that:

- **Auto-segment on hackathon close**: Pull participant data from the hackathon platform (Devpost API, Luma export, or CSV). Match submissions against registrations. Assign tiers in Attio based on submission status and quality scores.
- **Trigger sequences**: When a participant is tagged with their tier, enroll them in the corresponding Loops sequence using `loops-audience`.
- **Escalate high-intent signals**: If a Tier 1 or Tier 2 participant replies to any nurture email, or if any participant signs up for a paid plan within 14 days, create a deal in Attio using `attio-deals` and notify the team via Slack.
- **Track product adoption**: Monitor API usage after the hackathon. If a participant who was Tier 3 or Tier 4 starts actively using the product (5+ API calls in a week), upgrade their tier and trigger a personalized outreach.

### 4. Track nurture performance

Using `posthog-custom-events`, fire events at each step:

- `hackathon_nurture_email_sent` with properties: tier, sequence_step, hackathon_slug
- `hackathon_nurture_email_opened` with properties: tier, sequence_step, hackathon_slug
- `hackathon_nurture_reply_received` with properties: tier, hackathon_slug
- `hackathon_nurture_meeting_booked` with properties: tier, hackathon_slug, source_email_step
- `hackathon_product_adoption` with properties: tier, api_calls_post_event, features_used, hackathon_slug

### 5. Measure nurture effectiveness

After each hackathon's nurture window closes (21 days), calculate:

- Reply rate by tier (target: Tier 1 >50%, Tier 2 >25%, Tier 3 >10%, Tier 4 >5%)
- Product adoption rate by tier: % who continued using the product post-hackathon (target: Tier 1 >80%, Tier 2 >40%)
- Meetings booked by tier (target: Tier 1 >40%, Tier 2 >15%)
- Paid conversion rate within 30 days (target: >5% of all submitters)
- Sequence-to-pipeline conversion rate (target: >8% of all participants enter pipeline)

Compare these rates across hackathons to identify which challenge designs, prize structures, and nurture approaches generate the most pipeline.

## Output

- Tiered nurture sequences running for all hackathon participants
- Automated tier assignment and sequence enrollment
- High-intent signal escalation to sales pipeline
- Performance metrics per hackathon for cross-event comparison
