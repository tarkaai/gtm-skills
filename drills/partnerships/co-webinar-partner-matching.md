---
name: co-webinar-partner-matching
description: Find, qualify, and pitch co-webinar partners whose audiences overlap your ICP but are non-competing
category: Partnerships
tools:
  - Clay
  - Attio
  - Crossbeam
  - Anthropic
fundamentals:
  - clay-company-search
  - clay-enrichment-waterfall
  - clay-people-search
  - crossbeam-account-mapping
  - attio-lists
  - attio-contacts
  - attio-notes
  - hypothesis-generation
---

# Co-Webinar Partner Matching

This drill identifies, scores, and qualifies companies to co-host webinars with. Unlike general partner prospect research, this drill specifically evaluates a partner's webinar capability: audience engagement, content fit, promotional reach, and speaker quality.

## Input

- Your ICP definition (firmographics, buyer persona, pain points)
- Your webinar topic backlog (at least 5 candidate topics)
- Minimum partner audience size threshold (default: 2,000 engaged subscribers or followers)
- Target number of qualified co-webinar partners (default: 10)

## Steps

### 1. Source co-webinar partner candidates from Clay

Use `clay-company-search` to find companies that meet these criteria:

- **Adjacent, not competing**: They serve the same buyer persona but solve a different problem. If you sell analytics, partner with a feature flagging tool, data pipeline, or monitoring tool — not another analytics platform.
- **Active content program**: They publish content regularly (blog, newsletter, podcast, YouTube). Companies with an active content engine have the infrastructure and habit to promote a co-webinar.
- **Similar or larger audience size**: Their email list, LinkedIn following, or community should be within 0.5x-3x of yours. A massive mismatch creates unequal promotional burden.
- **Solution-aware audience**: Their audience already understands the problem category you solve. They are solution-aware, matching this play's stage.
- **Webinar history**: Check if they have hosted webinars, appeared on panels, or run virtual events before. Companies with webinar experience are easier to collaborate with and bring better speaker quality.

Set Clay filters: industry overlap with your ICP, employee count 10-1000, active blog or newsletter, and exclude companies in your direct competitive set. Pull 50-100 candidates.

### 2. Enrich partner candidates

Use `clay-enrichment-waterfall` to add:
- Company domain and website
- LinkedIn company URL and follower count
- Employee count and funding stage
- Contact info for the marketing lead, head of content, or DevRel lead (name, email, LinkedIn)
- Tech stack signals (what tools they use — this helps identify integration story angles)

Use `clay-people-search` to find the specific person who owns webinar or content partnerships at each company. Titles to search: "Head of Marketing," "Content Marketing Manager," "DevRel Lead," "Partnerships Manager," "Community Manager."

### 3. Score each partner on co-webinar fit

Score each candidate on five dimensions (each 1-5, max 25):

**Audience overlap (1-5)**: How closely does their audience match your ICP?
- 5: Same buyer persona, same company size, same industry
- 3: Overlapping persona but different industry or company size
- 1: Minimal overlap

**Promotional reach (1-5)**: Can they drive registrations?
- 5: 10,000+ email list or 5,000+ LinkedIn following, active newsletter
- 3: 2,000-10,000 email list or 1,000-5,000 LinkedIn following
- 1: <2,000 email and <1,000 LinkedIn following

**Content fit (1-5)**: Can you co-create a compelling topic at the intersection of both products?
- 5: Natural integration story ("Using X + Y together to solve Z")
- 3: Related but requires creative framing
- 1: No obvious content intersection

**Webinar capability (1-5)**: Can they execute a professional co-webinar?
- 5: Have hosted 3+ webinars, have a speaker/subject-matter-expert, have promotional playbook
- 3: Some event experience, willing speaker but no established process
- 1: No webinar history, would need to build from scratch

**Relationship proximity (1-5)**: How easy is it to make the ask?
- 5: Existing relationship (customer, advisor, shared investor, mutual connection)
- 3: Warm connection (commented on their content, met at an event, mutual LinkedIn connections)
- 1: Cold outreach required

Keep partners scoring 16+ out of 25.

### 4. Check account overlap with Crossbeam

If Crossbeam is configured, use `crossbeam-account-mapping` to check which partners share the most overlapping target accounts. Partners with high account overlap are the highest-value co-webinar targets because their audience members are literally your prospects.

### 5. Match partners to topics

For each qualified partner, use `hypothesis-generation` to identify the top 3 co-webinar topic ideas that sit at the intersection of both companies' expertise. Each topic should:

- Address a shared pain point of the overlapping audience
- Position both products as part of the solution (without being a product demo)
- Be specific enough that only the target audience cares about it
- Have a clear takeaway the attendee can implement immediately

Store the topic ideas as notes on each partner record in Attio using `attio-notes`.

### 6. Build the ranked partner list in Attio

Use `attio-lists` to create a list called "Co-Webinar Partners — {date}". Add qualified partners with fields:
- Company name and domain
- Partner score (out of 25) and subscores for each dimension
- Account overlap count (from Crossbeam, if available)
- Top 3 co-webinar topic ideas
- Contact name, email, and LinkedIn URL for the partnership lead
- Status: "Prospect" (initial state)
- Estimated promotional reach (email list + LinkedIn following)

Sort by partner score descending. The top 10 are your outreach targets.

## Output

- Ranked list of 10+ qualified co-webinar partners in Attio
- Each partner scored on audience overlap, promotional reach, content fit, webinar capability, and relationship proximity
- Topic ideas matched to each partner
- Contact info for the right person at each partner company
- Ready for outreach via personalized co-webinar pitch

## Triggers

Run this drill once at Smoke level (reduced scope: 5 candidates), then quarterly at Baseline+ to refresh the partner pipeline and identify new co-webinar opportunities.
