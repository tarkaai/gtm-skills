---
name: conference-sponsorship-pipeline
description: Evaluate, score, and secure conference sponsorships that maximize ICP exposure per dollar spent
category: Events
tools:
  - Clay
  - Attio
  - PostHog
fundamentals:
  - event-discovery-api
  - event-attendee-enrichment
  - clay-claygent
  - clay-scoring
  - attio-lists
  - attio-notes
  - posthog-custom-events
---

# Conference Sponsorship Pipeline

This drill builds a systematic process for evaluating which conferences are worth sponsoring, selecting the right sponsorship tier, negotiating terms, and tracking ROI. The goal is to spend sponsorship budget where your ICP density is highest and your brand gets maximum qualified exposure.

## Input

- ICP definition (from `icp-definition` drill): target industries, titles, company sizes, pain points
- Annual sponsorship budget or per-event budget cap
- Geographic constraints (can you travel? which regions matter?)
- Product positioning: what problem you solve and for whom

## Steps

### 1. Discover sponsorship-eligible conferences

Run the `event-discovery-api` fundamental to find conferences in your space. Extend the search to specifically target events that offer sponsorship and exhibitor packages:

1. Seed a Clay table with industry keywords, competitor names, and ICP role keywords
2. Run Claygent to find conferences with open sponsorship:
   ```
   Search the web for upcoming {Industry Keyword} conferences in {Region}
   that offer sponsorship or exhibitor booth packages. For each found, return:
   - Conference name
   - Date
   - Location (city)
   - Expected attendance
   - Website URL
   - Whether sponsorship prospectus is available online
   - Price range for booth/exhibitor packages if listed
   Format as JSON array.
   ```
3. Run a second Claygent enrichment pass on each conference URL:
   ```
   Visit {Conference URL} and find sponsorship or exhibitor information.
   Extract:
   - Sponsorship tiers and pricing (booth only, silver, gold, platinum, etc.)
   - What each tier includes (booth size, speaking slot, logo placement, lead retrieval, attendee list)
   - Whether lead retrieval / badge scanning is included
   - Sponsor contact email or form URL
   - Past sponsor companies (to gauge competitor presence)
   - Attendee profile or persona description
   ```

Aim for 15-30 candidate conferences per quarter.

### 2. Score conferences for sponsorship ROI potential

Add a scoring formula in Clay using `clay-scoring` that evaluates each conference:

- **ICP density (35%)**: How much of the attendee base matches your ICP? Use `event-attendee-enrichment` to extract and score speaker/sponsor lists as a proxy for attendee quality. If 10+ speakers are from ICP-matching companies, score 100.
- **Attendee volume (20%)**: 500-2,000 = 100, 2,000-5,000 = 80, 200-500 = 60, >5,000 = 40 (too diluted), <200 = 30 (too small for sponsorship ROI).
- **Sponsorship value (20%)**: What does the package include relative to price? Lead retrieval + speaking slot + booth = 100. Booth only = 50. Logo placement only = 20. Calculate cost per expected ICP contact: (sponsorship price) / (estimated ICP attendees). Below $20/contact = 100. $20-50 = 70. $50-100 = 40. Above $100 = 10.
- **Competitor presence (15%)**: If direct competitors sponsor, the audience is proven relevant. 2+ competitors = 90. 1 competitor = 70. No competitors but adjacent companies = 50. No relevant companies = 20.
- **Logistics (10%)**: Your team can attend in person = 100. Remote/virtual booth option = 60. Requires international travel = 40.

### 3. Select conferences and secure sponsorships

For conferences scoring 70+:

1. Download or request the sponsorship prospectus
2. Evaluate tier options against your goals:
   - **If goal is lead volume**: prioritize tiers with lead retrieval / badge scanning
   - **If goal is brand awareness**: prioritize tiers with speaking slots and logo placement
   - **If goal is both**: typically the mid-tier (Silver/Gold) offers the best value. Platinum rarely justifies the 3-5x price premium.
3. Contact the conference organizer. When negotiating:
   - Ask for historical attendee data (number of attendees, job titles, company sizes)
   - Ask about lead retrieval tool and data format (CSV export? real-time API?)
   - Negotiate add-ons: can you get a speaking slot added to a lower tier? Can you get early access to the attendee list for pre-event outreach?
   - Ask about refund or credit policies in case of cancellation
4. Log the selected conference in Attio using `attio-lists`. Create a "Conference Sponsorship Pipeline" list with fields: conference name, date, city, sponsorship tier, cost, expected attendees, ICP density score, status (evaluating, applied, confirmed, completed)
5. Track in PostHog using `posthog-custom-events`: fire `conference_sponsorship_committed` with properties: conference_name, tier, cost, expected_attendees, expected_icp_contacts

### 4. Pre-event attendee targeting

2-4 weeks before the conference:

1. If the organizer shares the attendee or registrant list, import it into Clay
2. Run `event-attendee-enrichment` to enrich and score attendees against your ICP
3. Build a target list of high-score attendees in Attio — these are the people your booth staff should prioritize
4. Send pre-event outreach to top targets: "We are exhibiting at {conference} — stop by booth #{number} to see {specific demo}. Book a time so we can prepare something tailored for you." Include a Cal.com link for scheduling booth meetings.
5. Fire `conference_preevent_outreach_sent` events in PostHog

### 5. Prepare booth operations

1 week before the conference:

1. Prepare demo environments: laptop + tablet, working offline and on mobile hotspot
2. Prepare 3 demo tracks of different lengths: 2-minute overview, 5-minute focused demo, 15-minute deep dive
3. Build or configure the lead capture system (see `badge-scan-lead-import` fundamental): ensure badge scanner app is installed or manual Tally/Typeform fallback is ready
4. Create booth staff briefing: target list with photos, key talking points per ICP segment, qualification questions (budget, timeline, current solution, pain points), and escalation criteria (when to book a meeting vs. hand off a card)
5. Print QR codes for: Cal.com booking link, product trial signup, and any gated content

**Human action required:** Confirm booth logistics with conference organizer — booth number, setup time, electrical/internet, signage dimensions.

## Output

- Scored and ranked conference sponsorship pipeline in Attio
- Sponsorship commitments with tier, cost, and expected ROI
- Pre-event target lists enriched and loaded in CRM
- Booth operations playbook for staff
- PostHog event trail for the full sponsorship pipeline

## Triggers

- Run conference discovery quarterly (90 days ahead minimum for sponsorship decisions)
- Pre-event preparation starts 4 weeks before each conference
- Booth operations prep completes 1 week before
