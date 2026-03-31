---
name: story-library-curation
description: Build and maintain a structured library of customer stories indexed by industry, use case, pain point, and outcome for demo narrative selection
category: Value Engineering
tools:
  - Attio
  - Fireflies
  - Anthropic
  - Clay
fundamentals:
  - attio-lists
  - attio-notes
  - attio-custom-attributes
  - fireflies-transcription
  - story-matching-scoring
---

# Story Library Curation

This drill builds and maintains a structured customer story library optimized for demo narrative selection. Each story is a self-contained record with the challenge, solution approach, results, key quotes, and metadata tags that enable AI-powered story matching to prospects.

## Input

- Access to existing customers in Attio
- Fireflies transcripts from customer calls, QBRs, or case study interviews
- Optional: existing case studies, testimonials, or success metrics

## Steps

### 1. Identify story candidates

Query Attio for customers who meet story criteria using `attio-lists`:
- Active customer for 3+ months
- Has measurable results (usage metrics, reported outcomes, NPS 8+)
- Willing to be referenced (check `reference_status` attribute)
- Represents a distinct segment (industry, use case, or pain point not already covered in the library)

For each candidate, check if a Fireflies transcript exists from any recent call (QBR, check-in, onboarding wrap-up). If yes, the story can be extracted without scheduling a new interview.

### 2. Extract story elements from transcripts

For each candidate with a Fireflies transcript, use `fireflies-transcription` to retrieve the full transcript. Send to Claude for structured extraction:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Extract a customer story from this call transcript. Find the moments where the customer describes their situation before using the product, how they adopted it, and what changed.

Transcript:
{transcript_text}

Return JSON:
{
  "company": "...",
  "industry": "...",
  "headcount": 0,
  "story_title": "One-line story title (e.g., 'How Acme cut onboarding time by 80%')",
  "challenge": {
    "summary": "2-3 sentences describing the problem in the customer's language",
    "pain_categories": ["onboarding", "churn", "manual-processes"],
    "quantified_pain": "Specific numbers if mentioned (e.g., '3 weeks per customer')",
    "emotional_context": "How the team felt about the problem"
  },
  "solution_approach": {
    "summary": "2-3 sentences on what they did with your product",
    "features_used": ["feature-1", "feature-2"],
    "implementation_time": "How long to set up"
  },
  "results": {
    "primary_metric": "Single most impressive result with number",
    "secondary_metrics": ["Other measurable outcomes"],
    "timeframe": "How long to achieve results",
    "emotional_outcome": "How the team feels now"
  },
  "key_quotes": [
    {"quote": "Exact customer words", "context": "What they were describing", "emotional_tone": "relief|excitement|pride|surprise"}
  ],
  "story_tags": {
    "industry": "...",
    "company_size_bucket": "1-50|51-200|201-1000|1000+",
    "pain_themes": ["theme1", "theme2"],
    "use_case": "...",
    "stakeholder_persona": "VP CS|CTO|CEO|..."
  }
}"
```

### 3. Create story records in Attio

Set up custom attributes on a "Stories" object or use tagged notes on Company records with `attio-custom-attributes`:

Required fields per story:
- `story_id`: unique slug (e.g., `acme-onboarding-speed`)
- `story_title`: one-line title
- `company_name`: customer company
- `industry`: industry tag
- `headcount_bucket`: size category
- `pain_themes`: array of pain categories
- `use_case`: primary use case
- `primary_metric`: headline result
- `story_status`: `draft|reviewed|approved|retired`
- `last_refreshed`: date of last update

Store the full structured story as an Attio note using `attio-notes`.

### 4. Assess library coverage

Map stories against your ICP segments:

| Segment | Stories Available | Coverage |
|---------|------------------|----------|
| B2B SaaS, 50-200 employees | 3 | Strong |
| Fintech, 200-1000 employees | 1 | Weak |
| Healthcare, any size | 0 | Gap |

Flag gaps where you have active pipeline but no matching story. Feed gaps into the `case-study-creation` drill as priority candidates.

### 5. Schedule story refreshes

Stories decay in relevance. Set up a quarterly review:
- Stories older than 6 months: check if the customer still has strong results. Update metrics if improved.
- Stories where the customer has churned or downgraded: retire immediately. Set `story_status: retired`.
- Stories with outdated product references: update the solution approach to reflect current product capabilities.

### 6. Validate story library for matching

Run `story-matching-scoring` against 5 recent deals to test that the library returns good matches. If the top score is below 50 for any deal, the library has a coverage gap for that segment.

## Output

- Structured story library in Attio with 5+ stories covering major ICP segments
- Each story has: challenge, solution, results, key quotes, metadata tags
- Coverage map showing strong segments and gaps
- Quarterly refresh schedule
- Story matching validated against recent deals

## Triggers

- Run on initial setup to build the first library
- Run when a new case study is completed (add to library)
- Run quarterly to refresh and validate coverage
- Run when story matching returns low scores (coverage gap detected)
