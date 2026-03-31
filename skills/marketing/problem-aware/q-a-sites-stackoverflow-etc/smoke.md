---
name: q-a-sites-stackoverflow-etc-smoke
description: >
  Q&A Site Authority -- Smoke Test. Answer 10 questions across Stack Overflow, Quora, and Dev.to
  to test whether high-quality answers drive profile clicks and generate a lead.
stage: "Marketing > Problem Aware"
motion: "CommunitiesForums"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">= 30 profile clicks and >= 1 lead in 1 week"
kpis: ["Profile views", "Profile click rate"]
slug: "q-a-sites-stackoverflow-etc"
install: "npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc"
drills:
  - qa-question-discovery
  - qa-answer-crafting
  - threshold-engine
---

# Q&A Site Authority -- Smoke Test

> **Stage:** Marketing > Problem Aware | **Motion:** CommunitiesForums | **Channels:** Other

## Outcomes

Pass threshold: >= 30 profile clicks and >= 1 lead (signup, demo request, or inbound email) within 1 week.

This proves that answering questions on Q&A platforms generates measurable interest in your product. You are testing: (a) whether your expertise maps to active questions, (b) whether answers get upvoted and seen, and (c) whether profile clicks convert to site visits.

## Leading Indicators

- Answers receiving >= 3 upvotes within 48 hours (signals the answer is valued)
- At least 1 answer accepted by the question asker
- Profile view count increasing daily on Stack Overflow user page
- Referrer traffic from stackoverflow.com or quora.com appearing in PostHog or analytics

## Instructions

### 1. Discover high-opportunity questions

Run the `qa-question-discovery` drill manually. The agent:

1. Defines your tag map (3-5 primary Stack Overflow tags matching your domain) and keyword map (5-10 pain-point and comparison queries for Quora).
2. Pulls unanswered and poorly answered questions from Stack Overflow using the Stack Exchange API: `GET /questions/unanswered?tagged=TAG&sort=creation&site=stackoverflow`.
3. Pulls recent Quora questions via SerpAPI: `site:quora.com KEYWORD`.
4. Scores each question by: no accepted answer (25%), view count (20%), recency (20%), low competition (15%), tag relevance (10%), asker reputation (10%).
5. Selects the top 10-15 questions as the answer queue.

Store the queue in Attio or a local file.

### 2. Optimize your profiles

**Human action required:** Before answering, set up profiles on each platform:

- **Stack Overflow**: Edit your profile bio to include your expertise domain and a link to your site. Add a professional avatar. Fill in the "About" section with 2-3 sentences about what you build. Stack Overflow profiles are the #1 driver of clicks from answers.
- **Quora**: Add credentials for each topic you answer (e.g., "CTO at [Company], 10 years building APIs"). Quora displays credentials next to every answer.
- **Dev.to**: Complete your profile with expertise areas and website URL.

### 3. Write and post 10 answers

Run the `qa-answer-crafting` drill for each question in the queue. For each answer:

1. The agent reads the full question and existing answers via `qa-platform-api-read`.
2. Identifies the gap -- what existing answers miss or get wrong.
3. Selects answer format: Direct Solution (code-first), Architecture Answer (tradeoffs), Debugging Walkthrough (root cause), or Comparison (structured table).
4. Drafts the answer. Stack Overflow answers lead with working code; Quora answers lead with a direct 1-2 sentence answer then elaborate.
5. Validates code examples for syntax and current library versions.
6. Applies self-promotion guardrails: no links to your product in the first 8 answers. Maximum 1-2 answers out of 10 may include a link to educational content (blog post, open-source repo) -- never a landing page.

**Human action required:** For Quora, the agent drafts answers and the human posts them via the web interface. For Stack Overflow, the agent can post via API if the account has an OAuth token. For new SO accounts, the human may need to post the first few answers manually.

Target: 10 answers across platforms over 5-7 days (not all at once).

### 4. Monitor answer performance at 24h and 72h

For each posted answer, the agent checks performance using `qa-platform-api-read`:
- Upvote count and delta
- Whether the answer was accepted
- Any comments or follow-up questions (respond to these promptly)
- Referral traffic in PostHog from the platform

Log all metrics in the activity log.

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Check:
- Profile clicks (Stack Overflow: user profile views accessible at `/users/YOUR_ID`; Quora: profile view count in settings; Dev.to: dashboard analytics) -- target >= 30 total.
- Leads: any signups, demo requests, or inbound emails attributable to Q&A activity -- target >= 1.

**PASS**: >= 30 profile clicks and >= 1 lead. Proceed to Baseline.
**FAIL**: Iterate. Try different tags, different answer formats, or different platforms. Re-run Smoke.

## Time Estimate

- Question discovery and scoring: 30 minutes
- Profile optimization: 15 minutes
- Writing 10 answers (15-25 min each): 2.5-4 hours
- Performance monitoring and follow-ups: 30 minutes
- Total: ~3.5-5 hours over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stack Exchange API | Read questions, post answers, track reputation | Free (10,000 req/day with API key) |
| Quora | Answer questions (manual posting) | Free |
| Dev.to API | Read articles, post responses | Free |
| Attio | Store answer queue and activity log | Included in standard stack |

## Drills Referenced

- `qa-question-discovery` -- find and rank high-opportunity questions across platforms
- `qa-answer-crafting` -- draft and post authoritative answers with quality guardrails
- `threshold-engine` -- evaluate pass/fail against the 30 profile clicks / 1 lead threshold
