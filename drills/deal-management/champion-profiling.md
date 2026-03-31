---
name: champion-profiling
description: Identify and profile potential internal champions at target accounts using enrichment signals and AI scoring
category: Deal Management
tools:
  - Clay
  - Attio
  - Anthropic
fundamentals:
  - clay-champion-signal-search
  - clay-people-search
  - clay-scoring
  - attio-champion-tracking
  - attio-contacts
---

# Champion Profiling

This drill identifies the best potential champion candidates at each target account by combining firmographic data, behavioral signals, and AI-powered scoring. The output is a ranked list of champion candidates in Attio, ready for recruitment outreach.

## Input

- Target account list in Attio (companies already in pipeline, stage = Connected or later)
- Defined champion persona: titles, departments, seniority levels where champions typically sit
- Clay account with enrichment credits

## Steps

### 1. Export Target Accounts to Clay

Pull active deals from Attio where stage >= Connected:

```
POST https://api.attio.com/v2/objects/deals/records/query
{
  "filter": {
    "stage": {"in": ["Connected", "Qualified", "Proposed"]}
  }
}
```

For each deal, extract the linked company domain. Push the company list to a Clay table using the `clay-table-setup` fundamental. Include columns: `company_name`, `company_domain`, `deal_id`, `deal_stage`.

### 2. Find Champion Candidates

Run the `clay-champion-signal-search` fundamental against the company list. For each company, search for 3-5 contacts matching the champion profile:

- **Title patterns:** "Head of {department}", "Senior Manager", "Lead {role}", "Director of {function}" — one level below the economic buyer
- **Department match:** Must be in the department that uses your product
- **Seniority:** Manager to Director level
- **Tenure:** 6 months to 3 years at current company

### 3. Enrich with Behavioral Signals

For each candidate, run the Claygent behavioral enrichment from `clay-champion-signal-search`:
- Frustration signals (public posts about pain points)
- Competitor engagement (interacting with competitor content)
- Learning signals (attending webinars, sharing industry content)
- Job change signals (recently promoted or hired)

### 4. Score and Rank

Apply the champion scoring formula from `clay-scoring`:
- Job change signal: +25 points
- Frustration signals: +20 per signal (max 40)
- Competitor engagement: +15
- Learning signals: +10 per signal (max 20)
- Title match: +10
- Tenure in range: +5

Filter to Hot (75+) and Warm (50-74) candidates only.

### 5. Push to Attio

For each qualified candidate:
1. Create or update the Person record in Attio using `attio-contacts`
2. Set `champion_status` = "Candidate" using `attio-champion-tracking`
3. Set `champion_score` to the computed score
4. Store `champion_signals` as JSON in the signals field
5. Link the Person to the relevant Deal record

### 6. Create Champion Briefings

For each Hot candidate (75+), generate a one-paragraph champion briefing using Claude:

```
"Based on these signals: {signals_json}, write a 3-sentence briefing for a sales rep about why this person ({name}, {title} at {company}) is a strong champion candidate. Include: what pain they likely feel, why they'd advocate for change, and the best conversation opener."
```

Store the briefing as an Attio note on the Person record using `attio-notes`.

## Output

- Attio "Champion Candidates" list populated with scored, enriched contacts
- Each candidate has: champion_score, champion_signals, champion_status = "Candidate"
- Hot candidates have AI-generated briefings attached as notes
- All candidates are linked to their respective Deal records

## Triggers

Run this drill:
- When a new deal enters the "Connected" stage
- Weekly refresh for all active deals without an active champion
- On demand when a champion is lost (status changed to "Disengaged" or "Lost")
