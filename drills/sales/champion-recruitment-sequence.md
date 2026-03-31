---
name: champion-recruitment-sequence
description: Multi-channel outreach sequence designed to recruit identified champion candidates into active internal advocates
category: Sales
tools:
  - Instantly
  - Loom
  - Attio
  - n8n
fundamentals:
  - instantly-campaign
  - instantly-tracking
  - loom-personalized-outreach
  - loom-analytics
  - attio-champion-tracking
  - attio-notes
  - linkedin-organic-dms
  - n8n-workflow-basics
---

# Champion Recruitment Sequence

This drill executes a structured multi-channel outreach sequence to convert champion candidates into actively recruited champions. Unlike standard cold outreach, champion recruitment focuses on empowerment — giving the candidate tools and insights that make them look good internally.

## Input

- Champion candidates list from Attio (output of `champion-profiling` drill)
- Champion briefings from the profiling step
- Value assets: ROI calculator, competitive comparison, or internal business case template
- Product demo or walkthrough video

## Steps

### 1. Segment Candidates by Signal Strength

Pull the "Champion Candidates" list from Attio. Segment into two tracks:

**Track A — High Signal (score 75+):** These candidates have strong behavioral signals. Lead with personalized, signal-specific messaging.

**Track B — Warm Signal (score 50-74):** These candidates match the profile but lack strong behavioral signals. Lead with value-first content that creates the problem awareness.

### 2. Build Track A Sequence (Signal-Led)

Using `instantly-campaign`, create a 4-touch email sequence:

**Email 1 (Day 0) — Signal Reference:**
Subject: Reference their specific signal (e.g., "Re: your post about {pain_point}")
Body: Acknowledge their public signal. Share a relevant insight or data point. Ask a low-commitment question ("Curious if you've explored X approach?"). No product pitch.

**Email 2 (Day 3) — Value Asset:**
Subject: "{First name}, thought this might help with {pain_area}"
Body: Share a genuinely useful asset (ROI calculator, industry benchmark, template). Frame it as helpful regardless of whether they buy anything. Include a soft CTA: "Happy to walk through how other {title}s at similar companies approached this."

**Email 3 (Day 7) — Loom Video:**
Create a personalized Loom video (60-90 seconds) using the `loom-personalized-outreach` fundamental. In the video: reference their specific situation, show one screen of how your product addresses their pain, and ask for 15 minutes. The Loom thumbnail should show their company logo or LinkedIn profile.

**Email 4 (Day 14) — Breakup with Bridge:**
Subject: "Last note on {pain_area}"
Body: Acknowledge they may not be the right person. Ask: "Is there someone on your team who's closer to this problem?" This either re-engages them or gets a referral to the real champion.

### 3. Build Track B Sequence (Value-Led)

Using `instantly-campaign`, create a 3-touch email sequence:

**Email 1 (Day 0) — Problem Education:**
Subject: "The hidden cost of {problem} at {company_size} companies"
Body: Share a data point about the problem your product solves. Make it about their world, not your product. Link to a blog post or case study.

**Email 2 (Day 5) — Peer Proof:**
Subject: "How {similar_company} solved {problem}"
Body: Brief case study of a peer company. Focus on the champion in that story — how they identified the problem, built the business case, and got it solved. Plant the seed that they could be that person.

**Email 3 (Day 12) — Direct Ask:**
Subject: "Quick question about {department} at {company}"
Body: Direct ask for 15 minutes. Frame it as research: "We're talking to {title}s about how they're handling {problem}. Would you be open to a 15-min conversation?"

### 4. Add LinkedIn Touch Layer

For Track A candidates, add LinkedIn touches in parallel using `linkedin-organic-dms`:

- **Day 1:** Connect request with a note referencing their signal (keep under 300 characters)
- **Day 5:** After connection accepted, send a DM with the value asset
- **Day 10:** Share a relevant post or comment on their content

For Track B: connect only, no DM unless they accept and engage with your profile.

### 5. Configure Tracking

Using `instantly-tracking`, set up tracking for:
- Email opens, clicks, and replies
- Loom view completions (via `loom-analytics`)
- LinkedIn connection acceptance and DM replies

Build an n8n workflow using `n8n-workflow-basics` that:
1. Listens for positive email replies (sentiment = positive or neutral-curious)
2. Updates Attio: set `champion_status` from "Candidate" to "Recruited"
3. Sets `champion_recruited_date` to today
4. Creates a note in Attio logging the recruitment interaction
5. Alerts the founder via Slack or email

### 6. Handle Responses

**Positive reply:** Move to champion enablement. Update status to "Recruited" in Attio.

**Referral to colleague:** Add the referred person as a new champion candidate. Run a quick `clay-people-search` to enrich them. Start a modified Track A sequence.

**Negative reply or unsubscribe:** Set status to "Lost" in Attio. Do not re-contact.

**No response after full sequence:** Set status to "Disengaged". Add to a 90-day re-engagement queue (re-run profiling at that point to check for new signals).

## Output

- Champion candidates moved to "Recruited" status in Attio
- Recruitment interaction history logged as Attio notes
- Loom video views tracked and correlated with reply rates
- Clear list of who responded, who referred, and who went silent

## Triggers

- Run immediately after `champion-profiling` drill produces new Hot candidates
- Re-run for Warm candidates 7 days after Hot sequence launches (stagger to manage volume)
- Re-run for "Disengaged" candidates after 90-day cooling period if new signals detected
