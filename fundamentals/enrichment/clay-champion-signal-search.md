---
name: clay-champion-signal-search
description: Search Clay for behavioral and firmographic signals that identify potential internal champions at target accounts
tool: Clay
product: Clay
difficulty: Config
---

# Clay Champion Signal Search

Find contacts at target accounts who exhibit champion behavioral patterns — people who are likely to advocate internally for a new solution based on their role, activity, and context.

## Prerequisites

- Clay account with enrichment credits (Launch plan minimum)
- Target account list already loaded in a Clay table (see `clay-company-search`)
- Defined champion persona: the job titles, seniority levels, and departments where champions typically sit

## Champion Signal Taxonomy

Champions are not the same as decision-makers. Champions are mid-level operators who feel the pain daily, have influence but not final authority, and are motivated to push for change. The key signals:

| Signal | Source | Weight |
|--------|--------|--------|
| Recently promoted (last 6 months) | LinkedIn via Clay | High — new role, eager to make impact |
| Posted about industry pain points | LinkedIn content via Claygent | High — publicly frustrated with status quo |
| Engaged with competitor content | LinkedIn activity via Claygent | Medium — actively evaluating alternatives |
| Attended relevant webinars/events | Event platform enrichment | Medium — investing time in learning |
| Job title contains "Head of", "Lead", "Senior Manager" | Clay people search | Medium — influence without final authority |
| Company is hiring in relevant department | Job board enrichment | Low — growth signal, not individual |

## Steps

### 1. Create a Champion Signal Table

Using the `clay-table-setup` fundamental, create a new Clay table named `{play-slug}-champion-signals`. Add columns:

- `company_name` (text)
- `company_domain` (text)
- `contact_name` (text)
- `contact_title` (text)
- `contact_linkedin` (URL)
- `contact_email` (email)
- `champion_signal_score` (number)
- `signal_details` (text)

### 2. Find People with Champion Profiles

Using the `clay-people-search` fundamental, search for contacts at each target company matching your champion persona. Configure:

- **Title keywords:** "Head of", "Lead", "Senior Manager", "Director" (one level below VP/C-suite)
- **Departments:** Map to your product's primary user department (e.g., Engineering, Marketing, Operations, Sales)
- **Seniority:** Manager to Director level (not C-suite — they are economic buyers, not champions)
- **Tenure at company:** 6 months to 3 years (long enough to have influence, not so long they are change-resistant)

### 3. Enrich with Behavioral Signals

Add a Claygent enrichment column (see `clay-claygent` fundamental) with the prompt:

```
Research this person's LinkedIn activity over the last 90 days. Look for:
1. Posts or comments about problems in their domain (frustration signals)
2. Engagement with content from our competitors or similar tools
3. Shares of industry reports or thought leadership (learning signals)
4. Recent job change or promotion (new mandate signals)

Return a JSON object:
{
  "frustration_signals": ["signal 1", "signal 2"],
  "competitor_engagement": ["competitor 1", "competitor 2"],
  "learning_signals": ["topic 1", "topic 2"],
  "job_change": true/false,
  "champion_likelihood": "high" | "medium" | "low",
  "reasoning": "one sentence explanation"
}
```

### 4. Score Champion Likelihood

Using the `clay-scoring` fundamental, create a formula column that computes a champion score (0-100):

- Job change in last 6 months: +25 points
- Frustration signals found: +20 points per signal (max 40)
- Competitor engagement: +15 points
- Learning signals: +10 points per signal (max 20)
- Title seniority match (Manager-Director): +10 points
- Tenure 6mo-3yr: +5 points

Set thresholds: Hot Champion (75+), Warm Champion (50-74), Unlikely (<50).

### 5. Filter and Export

Filter the table to Hot and Warm champions only. Verify email addresses using the `clay-email-verification` fundamental. Export the scored list to Attio using Clay's CRM push integration, tagged with `champion-candidate` status.

## Error Handling

- **Claygent returns empty results:** The contact may have a private LinkedIn profile. Fall back to title-based scoring only. Deduct 30 points from the maximum possible score.
- **Email not found:** Do not discard the contact. They can still be reached via LinkedIn DM. Flag as `linkedin-only` in the export.
- **Rate limit on enrichment:** Process in batches of 25-50. Wait 60 seconds between batches.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay | Claygent + enrichment waterfall | Best for multi-signal scoring |
| Apollo | People search + signals API | Good for basic title/role matching |
| LinkedIn Sales Navigator | Lead filters + alerts | Manual but precise for behavioral signals |
| ZoomInfo | Intent data + org charts | Enterprise-grade, expensive |
| Clearbit | Reveal + enrichment | Good firmographic data, weaker on behavioral |
