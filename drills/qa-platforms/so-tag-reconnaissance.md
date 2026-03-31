---
name: so-tag-reconnaissance
description: Discover, evaluate, and rank Stack Overflow tags where your product expertise can answer questions for solution-aware developers
category: QA Platforms
tools:
  - Stack Exchange API
  - Attio
fundamentals:
  - qa-platform-api-read
  - attio-lists
---

# Stack Overflow Tag Reconnaissance

This drill identifies the Stack Overflow tags where your expertise is relevant, evaluates each tag for opportunity (question volume, competition, answer gaps), and produces a ranked target list. Run once at play start; refresh quarterly.

## Input

- ICP definition: what technologies, languages, frameworks, and problem domains your customers use
- Your product's core capabilities and technical differentiation
- Competitor product names and categories

## Steps

### 1. Generate candidate tag lists

From your ICP definition and product capabilities, produce three keyword groups:

**Technology tags** — the stack your ICP uses:
- Languages: `python`, `javascript`, `go`, `rust`, etc.
- Frameworks: `react`, `django`, `fastapi`, `nextjs`, etc.
- Infrastructure: `docker`, `kubernetes`, `aws`, `terraform`, etc.

**Problem-domain tags** — the categories of problems you solve:
- `api-design`, `rate-limiting`, `authentication`, `webhooks`, `etl`, `data-pipeline`, etc.
- Include compound tags: `python-requests`, `node.js-http`, etc.

**Adjacent tags** — where your ICP asks about problems your product addresses indirectly:
- Competitor names as tags (if they exist): check `GET /tags/{competitor}/info`
- Related categories: `monitoring`, `logging`, `testing`, `deployment`, etc.

### 2. Evaluate each candidate tag

For each candidate tag, use the `qa-platform-api-read` fundamental:

```bash
# Get tag info (question count, description)
GET /tags/{TAG}/info?site=stackoverflow&key=YOUR_API_KEY

# Get recent unanswered questions (opportunity signal)
GET /questions/unanswered?tagged={TAG}&order=desc&sort=creation&site=stackoverflow&key=YOUR_API_KEY&pagesize=50

# Get recent questions with no accepted answer
GET /search/advanced?tagged={TAG}&accepted=false&sort=creation&order=desc&site=stackoverflow&key=YOUR_API_KEY&pagesize=50

# Get related tags (find adjacent opportunities)
GET /tags/{TAG}/related?site=stackoverflow&key=YOUR_API_KEY
```

For each tag, record:
- **Total questions**: from tag info
- **Questions per day**: estimate from recent question creation dates
- **Unanswered ratio**: unanswered questions / total recent questions
- **Low-answer ratio**: questions with 0-1 answers / total recent questions
- **Avg views on unanswered**: mean `view_count` on unanswered questions (demand signal)
- **Related tags**: tags frequently co-occurring (expand your target list)

### 3. Score and rank tags

Score each tag (0-50):

| Signal | Weight | Calculation |
|--------|--------|-------------|
| Question volume | 10 | `min(questions_per_day / 5 * 10, 10)` — at least 5/day is ideal |
| Unanswered ratio | 15 | `unanswered_ratio * 15` — higher = more opportunity |
| View demand | 10 | `min(avg_views_unanswered / 500 * 10, 10)` — views signal demand |
| Expertise fit | 10 | Manual: 0=tangential, 5=moderate, 10=core expertise |
| Competition | 5 | `(1 - pct_questions_with_accepted_answer) * 5` — less competition = higher score |

### 4. Select target tags

Sort by total score. Select:
- **Primary (3-5 tags, score 35+)**: Monitor and answer daily
- **Secondary (5-10 tags, score 25-34)**: Answer when high-opportunity questions appear
- **Watch list (remaining)**: Review monthly for promotion

### 5. Build tag engagement profiles

For each selected tag, produce:

```markdown
## [TAG] Engagement Profile

- **Total questions**: X | **Questions/day**: Y | **Unanswered ratio**: Z%
- **Score**: XX/50
- **Avg views on unanswered**: N
- **Related tags**: [list]
- **Typical question patterns**: [what people ask about]
- **Your unique angle**: [what you can answer that others cannot]
- **Common pitfalls in existing answers**: [where current answers are wrong or outdated]
- **Best answer format**: [code-heavy, explanation-heavy, or both]
- **Competing answerers**: [prolific users in this tag — their strengths and gaps]
```

### 6. Store in CRM

Using the `attio-lists` fundamental, create an Attio list called "SO Tag Targets" with entries for each tag. Include the engagement profile data as structured fields. Track answer count, upvotes earned, and referral visits per tag over time.

## Output

- Ranked list of 10-15 target Stack Overflow tags with engagement profiles
- Attio list with tag targets and metadata
- Three keyword groups (technology, problem-domain, adjacent) for use in question monitoring

## Triggers

- Run once at play start
- Re-run quarterly or when product capabilities change
- Ad-hoc when a new relevant tag is discovered
