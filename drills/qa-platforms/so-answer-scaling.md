---
name: so-answer-scaling
description: Batch answer generation pipeline with AI drafting, quality gates, and multi-tag coverage to scale SO presence 5-10x
category: QA Platforms
tools:
  - Stack Exchange API
  - n8n
  - Anthropic
  - PostHog
fundamentals:
  - qa-platform-api-read
  - qa-platform-api-write
  - qa-question-monitoring
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-dashboards
---

# Stack Overflow Answer Scaling

This drill scales Stack Overflow answering from 2-5 manual answers/day to 10-25 answers/day using AI-assisted drafting, batch processing, and quality gates. The goal is to increase volume without degrading answer quality or triggering SO's quality filters.

## Input

- Active question monitoring pipeline (from `so-question-monitoring-automation`)
- Established answer patterns from Baseline (what formats, lengths, and styles earn upvotes in each tag)
- Stack Overflow account with 200+ reputation (enables comment privileges and removes some rate limits)

## Steps

### 1. Build the answer generation pipeline in n8n

```
Webhook Node (receives question from monitoring pipeline)
  -> HTTP Request Node (Stack Exchange API):
     Fetch full question with body and existing answers
  -> Function Node (assess):
     Determine if this question is answerable:
       - Is the question clear enough to produce a definitive answer?
       - Do existing answers already fully cover the solution?
       - Is this within our expertise domain?
     Output: {answerable: boolean, reason: string, answer_type: string}
  -> IF Node: Only continue if answerable == true
  -> HTTP Request Node (Anthropic API):
     System prompt: "You are a senior software engineer answering a Stack Overflow question.
       Rules:
       - Provide a complete, runnable code solution
       - Explain WHY the solution works, not just WHAT to change
       - Include imports and setup code
       - Format with fenced code blocks using the correct language identifier
       - Keep total length 150-600 words
       - Never mention any product by name unless the question is specifically about that product
       - Never include links to external sites
       - Be precise and factual; no opinions or hedging"
     User prompt: "Question title: {title}\nQuestion body: {body}\nTags: {tags}\nExisting answers summary: {existing_answer_summary}\nAnswer type to write: {answer_type}"
  -> Function Node (quality gate):
     Verify the draft answer:
       - Contains at least one code block
       - Code block has a language identifier
       - Word count between 100 and 800
       - Does not contain product names or external URLs
       - Does not contain phrases: "I think", "In my experience", "Great question"
       - Does not repeat content from existing answers
     Output: {passes: boolean, issues: string[]}
  -> IF Node: Only continue if passes == true; else log rejection reason
  -> SET Node: Queue the answer for human review
```

### 2. Implement the review queue

Answers that pass the quality gate enter a review queue. The queue is stored in n8n static data or an external store:

```json
{
  "question_id": 12345,
  "question_url": "https://stackoverflow.com/q/12345",
  "question_title": "How to...",
  "tags": ["python", "api"],
  "draft_answer": "...",
  "answer_type": "complete_solution",
  "quality_score": 4,
  "generated_at": "2026-03-30T10:00:00Z",
  "status": "pending_review"
}
```

**Human action required:** Review each draft answer before posting. For the first 2 weeks, review every answer. After establishing trust in the pipeline's quality, shift to spot-checking (review 1 in 5, auto-post the rest through the `qa-platform-api-write` fundamental).

### 3. Implement rate limiting

Stack Overflow enforces rate limits and quality bans for rapid posting:

- **Maximum 40 write operations/day** (API limit for non-trusted apps)
- **Post no more than 1 answer every 3 minutes** (built-in cooldown)
- **Answer quality ban threshold**: If 3+ answers are downvoted or deleted in a short period, the account is answer-banned

Build rate limiting into the n8n pipeline:
- Queue answers and post them on a staggered schedule (every 15-30 minutes)
- Track answer outcomes (upvotes, downvotes, deletions) and pause posting if downvote rate exceeds 10%
- Maintain a daily budget: post max 15 answers/day initially, scale up as quality metrics confirm

### 4. Scale across tag groups

Once the pipeline is running reliably for primary tags:
- Add secondary tags to the question monitoring pipeline
- Create tag-specific system prompts for the AI drafting (different tags need different answer styles)
- Track quality metrics per tag: upvote rate, acceptance rate, average score
- Allocate answer budget proportionally to tags with highest ROI (upvotes per answer)

### 5. Build the performance dashboard

Using the `posthog-dashboards` fundamental, create a dashboard tracking:

- **Answers posted per day**: target 10-25
- **Average upvote score per answer**: target 2+
- **Acceptance rate**: target 15%+
- **Quality gate pass rate**: target 70%+ (if lower, system prompts need tuning)
- **Downvote rate**: must stay under 10% (if higher, pause and investigate)
- **Referral sessions from SO**: PostHog tracking of `utm_source=stackoverflow` visits
- **Time from question posted to answer posted**: target under 2 hours for high-priority

### 6. Implement feedback loops

After 2 weeks of scaled operation, analyze:
- Which answer types earn the most upvotes? Weight the AI toward those formats.
- Which tags have the highest acceptance rate? Allocate more budget there.
- Which questions does the AI struggle with? Add those patterns to a skip list.
- What word count performs best? Adjust the prompt's length target.

Feed these learnings back into the system prompt and quality gate rules.

## Output

- AI-assisted answer generation pipeline processing 10-25 questions/day
- Review queue with quality gate (auto-post after confidence established)
- Rate-limited posting schedule respecting SO's limits
- Performance dashboard with quality and volume metrics
- Tag-specific optimization data

## Triggers

- Activated when the play reaches Scalable level
- Runs continuously via n8n workflow
- Weekly: review pipeline quality metrics and adjust
- Monthly: tune system prompts based on performance data
