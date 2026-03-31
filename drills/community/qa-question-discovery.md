---
name: qa-question-discovery
description: Identify and rank unanswered or poorly answered questions across Q&A platforms where your expertise can build authority
category: QA Platforms
tools:
  - Stack Exchange API
  - SerpAPI
  - Dev.to API
  - Attio
fundamentals:
  - qa-platform-api-read
  - attio-lists
  - attio-notes
---

# Q&A Question Discovery

This drill finds high-opportunity questions across Stack Overflow, Quora, Dev.to, and other Q&A platforms where your expertise can produce standout answers. It produces a ranked queue of questions to answer, prioritized by visibility, relevance, and competition.

## Input

- ICP definition: what problems your product solves, for whom, in what context
- Product expertise areas: specific topics, technologies, or domains you can speak on authoritatively
- Competitor names: so you can find "vs" or "alternative to" questions
- Target platforms and tags (e.g., Stack Overflow tags: `python`, `api`, `rate-limiting`)

## Steps

### 1. Define your tag and keyword maps

Build three keyword maps:

**Tag map (Stack Overflow / Dev.to):**
- Primary tags: 3-5 tags directly in your product domain (e.g., `javascript`, `react`, `testing`)
- Adjacent tags: 5-10 tags where your ICP hangs out but your product is not the direct topic (e.g., `node.js`, `typescript`, `ci-cd`)
- Use the `qa-platform-api-read` fundamental to pull related tags:
  ```
  GET /tags/PRIMARY_TAG/related?site=stackoverflow
  ```

**Keyword map (Quora / general search):**
- Pain-point queries: "how to solve X", "why does X happen", "best way to handle X"
- Comparison queries: "X vs Y", "alternative to X", "should I use X or Y"
- Recommendation queries: "best tool for X", "what do you use for X"

**Competitor map:**
- "[competitor] problems", "[competitor] not working", "switch from [competitor]"

### 2. Pull candidate questions from Stack Overflow

Using the `qa-platform-api-read` fundamental, run these queries for each primary and adjacent tag:

```bash
# Unanswered questions (highest priority)
GET /questions/unanswered?tagged=TAG&sort=creation&site=stackoverflow&pagesize=50

# Questions with no accepted answer
GET /search/advanced?tagged=TAG&accepted=false&sort=creation&site=stackoverflow&pagesize=50

# Questions with low answer counts
GET /search/advanced?tagged=TAG&answers=1&accepted=false&sort=votes&site=stackoverflow&pagesize=50
```

Also search for keyword-based matches:
```bash
GET /search/advanced?q=KEYWORD&sort=creation&site=stackoverflow&pagesize=50
```

Collect all unique question IDs. Target: 50-100 candidate questions per discovery run.

### 3. Pull candidate questions from Quora

Using the `qa-platform-api-read` fundamental's SerpAPI approach:

```bash
# For each keyword in your keyword map
curl "https://serpapi.com/search.json?engine=google&q=site:quora.com+KEYWORD&tbs=qdr:w&api_key=KEY&num=20"
```

The `tbs=qdr:w` restricts to the last week. Parse Quora question URLs and titles from results.

### 4. Pull candidate questions from Dev.to

```bash
# Recent help/discuss posts
curl "https://dev.to/api/articles?tag=help&top=7&per_page=30"
curl "https://dev.to/api/articles?tag=discuss&top=7&per_page=30"
```

Filter by titles that contain your keywords.

### 5. Score and rank all candidates

For each candidate question, compute a priority score (0-100):

| Signal | Weight | Scoring |
|--------|--------|---------|
| **No accepted answer** | 25% | 100 if no accepted answer, 20 if accepted but stale |
| **View count** | 20% | Normalize: top 10% of views = 100, bottom 10% = 10 |
| **Recency** | 20% | Posted < 6h = 100, < 24h = 80, < 72h = 50, < 1w = 20, older = 5 |
| **Low competition** | 15% | 0 answers = 100, 1 answer = 70, 2 = 40, 3+ = 10 |
| **Tag relevance** | 10% | Primary tag match = 100, adjacent = 50, keyword-only = 30 |
| **Asker reputation** | 10% | High-rep asker = more visible question. > 1000 rep = 100, > 100 = 60, < 100 = 30 |

Sort by total score descending. Take the top 10-20 for the answer queue.

### 6. Build the answer queue

For each selected question, create a queue entry:

```json
{
  "platform": "stackoverflow",
  "question_id": "12345",
  "url": "https://stackoverflow.com/questions/12345/...",
  "title": "How to handle rate limiting in Node.js?",
  "tags": ["node.js", "api", "rate-limiting"],
  "score": 87,
  "priority": "high",
  "answer_count": 0,
  "view_count": 1500,
  "created_at": "2026-03-30T10:00:00Z",
  "your_angle": "We built a rate limiter; can share the pattern without promoting product",
  "estimated_effort": "15 minutes",
  "status": "pending"
}
```

Store the queue in Attio using the `attio-lists` fundamental: create a list named "Q&A Answer Queue" with structured fields for each property above.

### 7. Log discovery run metadata

Using `attio-notes`, log each discovery run:
- Date, platforms searched, tags and keywords used
- Total candidates found, total after scoring
- Top 10 selected questions with scores
- Any new tags or keywords discovered during the search

## Output

- Ranked queue of 10-20 questions to answer across all platforms
- Attio list with queue entries and metadata
- Discovery run log for tracking coverage over time

## Triggers

- Run daily during Smoke and Baseline levels
- Run every 4 hours during Scalable level (automated via n8n)
- Feed into `qa-answer-crafting` drill for response generation
