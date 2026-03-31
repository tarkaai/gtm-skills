---
name: qa-answer-crafting
description: Draft and post authoritative answers on Q&A platforms that build expertise reputation and drive profile clicks
category: QA Platforms
tools:
  - Stack Exchange API
  - Dev.to API
  - Anthropic
fundamentals:
  - qa-platform-api-read
  - qa-platform-api-write
  - community-engagement-tracking
  - ai-content-ghostwriting
---

# Q&A Answer Crafting

This drill produces high-quality answers for Q&A platforms (Stack Overflow, Quora, Dev.to) that establish technical authority and drive profile visits. Every answer must be genuinely the best answer to the question -- not a vehicle for marketing.

## Input

- A question from the answer queue (from `qa-question-discovery` drill)
- Your product's expertise areas, code examples, and relevant content
- Platform-specific profile and reputation data

## Steps

### 1. Deep-read the question

Using `qa-platform-api-read`, fetch the full question with all existing answers:

**Stack Overflow:**
```
GET /questions/QUESTION_ID?site=stackoverflow&filter=withbody
GET /questions/QUESTION_ID/answers?site=stackoverflow&filter=withbody&sort=votes
```

**Dev.to:**
```
GET /api/articles/ARTICLE_ID
GET /api/comments?a_id=ARTICLE_ID
```

Analyze:
- **What is the actual problem?** Strip away the poster's framing and identify the root technical issue.
- **What have existing answers covered?** Map each answer's approach and identify gaps.
- **What is wrong with existing answers?** Outdated library versions, deprecated APIs, security issues, incomplete solutions.
- **What is your unique angle?** A better approach, a simpler solution, a production-tested pattern, a common gotcha.

If existing answers fully and correctly solve the problem and you have nothing to add, **skip the question**. Move to the next item in the queue.

### 2. Select answer format

Choose based on the question type:

**The Direct Solution** -- for specific "how do I X?" questions:
- Lead with working code
- Explain what the code does and why
- Note edge cases and error handling
- Include library versions tested against

**The Architecture Answer** -- for design/approach questions:
- Present 2-3 approaches with tradeoffs
- Recommend one with clear reasoning
- Include a minimal code example for the recommended approach
- Link to further reading for each approach

**The Debugging Walkthrough** -- for "why is X happening?" questions:
- Explain the root cause first
- Show the fix
- Explain why the original code failed
- Suggest how to prevent this class of bug

**The Comparison Answer** -- for "X vs Y" questions:
- Structured comparison table
- Specific use-case recommendations
- Personal experience with each option (if genuine)
- Benchmarks or data if available

### 3. Draft the answer

Use `ai-content-ghostwriting` to generate a draft, then refine. The draft prompt should include:
- The full question text
- Existing answers (so the draft avoids repetition)
- Your specific expertise and examples
- The selected answer format

**Formatting rules by platform:**

**Stack Overflow:**
- Use Markdown: headers, code blocks with language hints, bullet points
- Code blocks must be syntactically valid and tested
- Lead with the solution, then explain. Stack Overflow readers scan for code first.
- Include version numbers: "Tested with Node.js 20.x and Express 4.x"
- Keep under 800 words for answers, 300 words for comments
- Never use emoji. Tone: direct, technical, precise.

**Quora:**
- Use Quora's rich text: bold key points, numbered lists
- More conversational tone than Stack Overflow
- Can include personal experience and opinion
- Lead with a direct 1-2 sentence answer, then elaborate
- 200-600 words is the sweet spot
- Include relevant images or diagrams if they clarify the answer

**Dev.to:**
- Full Markdown with code blocks, headers, images
- More narrative style -- Dev.to readers expect blog-post quality
- Include "TL;DR" at the top for long answers
- Can be 500-1500 words
- End with a discussion prompt ("What approach do you use?")

### 4. Code validation (Stack Overflow only)

Before posting any answer with code:

1. **Syntax check**: Run the code through a linter for the relevant language
2. **Execution check**: If possible, execute the code and verify it produces the claimed output
3. **Version check**: Verify library versions mentioned are current (not deprecated)
4. **Security check**: Ensure code does not demonstrate insecure patterns (SQL injection, eval(), hardcoded secrets)

If the code cannot be validated, add a caveat: "Note: this approach requires [specific version]. Check [docs link] for your version."

### 5. Apply self-promotion guardrails

Before posting, run this checklist:

- [ ] Does this answer stand on its own without any link to your product? **It must.**
- [ ] If including a link to your content, is it the single best resource for this specific question?
- [ ] Is the link to educational content (blog post, open-source repo, docs) and NOT a landing page, pricing page, or signup page?
- [ ] Have you included at least 2 non-self links for every 1 self-link?
- [ ] In your last 10 answers on this platform, have you linked to yourself fewer than 2 times?

Stack Overflow explicitly bans promotional content. Quora is more lenient but communities self-police. Dev.to allows "shameless plugs" only in dedicated threads.

**Profile optimization** (do this once, not per answer):
- Stack Overflow: Set your profile bio to include your expertise area and a link to your site. Answers drive profile views; the profile drives clicks.
- Quora: Fill out credentials for your expertise areas. Quora displays credentials next to your answers.
- Dev.to: Complete your bio with your expertise and website link.

### 6. Post the answer

Using `qa-platform-api-write`:

**Stack Overflow:**
```
POST /questions/QUESTION_ID/answers/add
body=HTML_ENCODED_ANSWER&site=stackoverflow
```

**Dev.to:** Post as an article response or comment depending on length and platform norms.

**Quora:** Draft the answer. **Human action required:** Post via Quora's web interface until API access is confirmed.

### 7. Track the answer

Using `community-engagement-tracking`, log:

```json
{
  "date": "2026-03-30",
  "platform": "stackoverflow",
  "question_id": "12345",
  "question_url": "https://stackoverflow.com/questions/12345/...",
  "answer_url": "https://stackoverflow.com/a/12346/...",
  "answer_format": "direct-solution",
  "topic": "rate-limiting",
  "tags": ["node.js", "api"],
  "included_link": false,
  "word_count": 350,
  "code_included": true,
  "status": "posted"
}
```

### 8. Follow up at 24h and 72h

Using `qa-platform-api-read`, check each posted answer after 24 hours and 72 hours:

- **Upvote count**: Log it. Answers with 3+ upvotes in 24h are strong signals.
- **Accepted**: Did the OP accept your answer? Log it.
- **Comments**: Did anyone ask follow-up questions? Respond promptly -- engaged follow-ups build more reputation than the original answer.
- **Competing answers**: Did a better answer appear? If so, note what they did differently.

Update the activity log with performance data.

## Output

- Posted answer on the Q&A platform
- Activity log entry with performance metrics (updated at 24h and 72h)
- Follow-up responses to comments

## Triggers

- Triggered by `qa-question-discovery` drill output (answer queue)
- Target: 2-3 answers per day during active levels
- Skip days when no high-quality opportunities exist -- no filler answers
