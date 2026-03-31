---
name: conference-cfp-pipeline
description: Discover open CFPs, craft talk proposals, submit to conferences, and track acceptance rates
category: Events
tools:
  - Clay
  - Attio
  - AI (Claude / GPT)
  - PostHog
fundamentals:
  - conference-cfp-search
  - event-discovery-api
  - clay-claygent
  - clay-scoring
  - attio-lists
  - attio-notes
  - posthog-custom-events
---

# Conference CFP Pipeline

This drill builds a systematic pipeline for finding open call-for-papers, crafting talk proposals, submitting to conferences, and tracking acceptance rates. The goal is to land speaking slots at events where your ICP attends, converting talks into brand awareness and qualified developer leads.

## Input

- ICP definition: target developer roles, industries, and the problems they care about (from `icp-definition` drill)
- 3-5 talk topics aligned with your content pillars and product expertise
- Speaker bio and photo (standardized across platforms)
- Target: number of talks per quarter and geographic preferences

## Steps

### 1. Discover open CFPs

Run the `conference-cfp-search` fundamental to find open CFPs matching your topics:

1. Seed a Clay table with your talk topic keywords and target regions
2. Run Claygent to scrape CFP aggregators (Papercall, Sessionize, confs.tech, cfpland.com, dev.events)
3. Parse results into individual CFP rows with: conference name, date, CFP deadline, location, audience size, submission URL, topics accepted
4. Filter: remove CFPs with deadlines < 7 days out (not enough time to craft a quality proposal)
5. Filter: remove conferences with estimated audience < 50 (too small for ROI)

### 2. Score and prioritize CFPs

Add a scoring formula in Clay using `clay-scoring`:

- **ICP audience density (40%)**: Does the conference attract your target developer personas? Check past speaker companies, sponsor list, and topic tracks. Use `clay-claygent` to research: "What types of developers attend {Conference Name}? What companies sponsor it?"
- **Topic fit (25%)**: How closely do the accepted tracks match your prepared talks? Exact match = 100. Adjacent topic = 60. Tangential = 20.
- **Audience size (15%)**: 200-500 = 90, 500-2000 = 100, 50-200 = 50, 2000+ = 70 (larger events are harder to land)
- **Travel logistics (10%)**: Local/remote = 100. Same continent = 70. International = 40. Covers travel = add 20 bonus.
- **Conference reputation (10%)**: First-year conference = 30. Established (3+ years) = 70. Flagship events = 100.

Push scored CFPs to Attio using `attio-lists`. Create a "CFP Pipeline" list with fields: conference name, score, deadline, status (discovered, drafting, submitted, accepted, rejected).

### 3. Craft talk proposals

For each CFP scoring 60+, draft a talk proposal using Claude:

```
System: You are a developer advocate submitting a talk proposal to {Conference Name}.
The conference audience is: {Audience Description}.
The accepted topics are: {Topics/Tracks}.

Write a talk proposal with:
1. Title (under 80 characters, specific and benefit-driven — avoid buzzwords)
2. Abstract (200-300 words):
   - Open with a problem the audience faces
   - Describe what they will learn
   - Promise concrete takeaways (code, framework, checklist)
   - End with why this talk matters NOW
3. Outline (5-7 bullet points, one per section of the talk)
4. Key takeaways (3 bullet points the audience will leave with)
5. Target audience description (who should attend, prerequisites)

Rules:
- No product pitches in the abstract. The talk teaches a concept; the product is mentioned only as one tool among several.
- Use specific numbers: "reduced latency from 2s to 200ms" not "significantly improved performance"
- Reference the conference's specific audience and topics — generic proposals get rejected
- Include a "Why me" section: what unique experience qualifies you to give this talk
```

### 4. Submit proposals

For each scored CFP:

1. Submit the proposal via the CFP platform (Papercall, Sessionize, Google Form, etc.)
2. Log the submission in Attio using `attio-notes`: conference name, talk title, submission date, CFP deadline, expected notification date
3. Track in PostHog using `posthog-custom-events`: fire `devrel_cfp_submitted` with properties: conference_name, talk_title, conference_date, audience_size, score

### 5. Prepare accepted talks

When a talk is accepted:

1. Update the Attio record status to "accepted"
2. Fire `devrel_cfp_accepted` event in PostHog
3. Build the talk deck (use your slide template — keep slides minimal, code-heavy)
4. Prepare a companion blog post or GitHub repo that attendees can reference after the talk
5. Create a scheduling link (Cal.com) for post-talk follow-up conversations
6. Design a QR code slide for the end of the talk linking to: your blog post, GitHub repo, and scheduling link

### 6. Post-talk lead capture

After delivering the talk:

1. Fire `devrel_talk_delivered` event in PostHog with: conference_name, audience_size, talk_title
2. Share the talk recording (when available) on social channels
3. Publish the companion blog post
4. Track leads from the talk: anyone who books via the Cal.com link or visits the companion content gets tagged `source: conference-talk` in Attio
5. Fire `devrel_talk_lead_captured` for each lead with: conference_name, talk_title, lead_source (qr_code, direct, social_share)

### 7. Analyze and iterate

After each quarter:

1. Calculate acceptance rate: submitted / accepted
2. Calculate lead yield per talk: leads captured / talks delivered
3. Identify which conference types (size, region, topic) produced the most leads
4. Update your talk topics based on which proposals got accepted and which talks generated the most engagement
5. Retire talks that have been given 3+ times; develop new material

## Output

- Scored and prioritized CFP pipeline in Attio
- Talk proposals ready for submission
- Submission tracking with acceptance rates
- Post-talk lead capture and attribution
- Quarterly analysis of speaking program ROI

## Triggers

- Run CFP discovery every 2 weeks to catch new openings
- Submit proposals as CFPs are discovered (do not batch — deadlines vary)
- Post-talk lead capture within 48 hours of each talk
- Quarterly ROI review
