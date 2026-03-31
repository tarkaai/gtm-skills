---
name: so-answer-crafting
description: Craft high-quality Stack Overflow answers that solve the specific problem, earn upvotes, and build reputation
category: QA Platforms
tools:
  - Stack Exchange API
  - AI (Claude / GPT)
fundamentals:
  - qa-platform-api-read
  - qa-platform-api-write
  - community-engagement-tracking
---

# Stack Overflow Answer Crafting

This drill produces technically rigorous, community-appropriate Stack Overflow answers. Stack Overflow is not Reddit — it demands precise, reproducible solutions with working code. Every answer must pass the "would a senior engineer upvote this?" test.

## Input

- A question URL or question ID to answer
- Your product's technical capabilities and relevant documentation
- The tag engagement profile (from `so-tag-reconnaissance`)

## Steps

### 1. Analyze the question

Using the `qa-platform-api-read` fundamental, fetch the question and existing answers:

```bash
GET /questions/{QUESTION_ID}?site=stackoverflow&key=YOUR_API_KEY&filter=withbody
GET /questions/{QUESTION_ID}/answers?order=desc&sort=votes&site=stackoverflow&key=YOUR_API_KEY&filter=withbody
```

Analyze:
- **What is the exact problem?** Parse the error message, code snippet, and expected vs actual behavior.
- **What has already been answered?** Read every existing answer. Identify gaps, outdated approaches, or errors.
- **What's the asker's skill level?** Infer from their code, question phrasing, and reputation. Match your explanation depth.
- **Is the question still active?** Questions older than 30 days are lower priority unless they have high views and no accepted answer.
- **Is there a canonical duplicate?** If so, vote to close rather than answering.

### 2. Determine answer strategy

Based on the analysis, choose one approach:

**The Complete Solution** — When you can solve the exact problem with working code:
- Provide the fix with a complete, runnable code snippet
- Explain WHY the fix works (not just what to change)
- Include error handling and edge cases
- Show before/after if modifying the asker's code

**The Root Cause Explanation** — When the asker has an XY problem (asking about their attempted solution, not their actual problem):
- Identify the real problem first
- Explain why their approach won't work
- Provide the correct approach with code
- Be respectful — "The issue is actually..." not "You're doing it wrong"

**The Comparison Answer** — When multiple valid approaches exist:
- Present 2-3 approaches with code for each
- Compare tradeoffs: performance, readability, compatibility
- Recommend one with clear reasoning
- Use headings to make the answer scannable

**The Update Answer** — When existing answers are outdated (deprecated APIs, old library versions):
- State which existing answer you're updating and why
- Provide the current/modern approach
- Reference the documentation for the current version
- Note when the change occurred (version number)

### 3. Write the answer

**Structure rules:**
- First line: directly state the solution or key insight (no preamble)
- Code blocks: use triple-backtick fenced blocks with language identifier (```python, ```javascript, etc.)
- Every code snippet must be syntactically valid and tested
- Maximum one link to external documentation per answer. Link to official docs, not your marketing site.
- If your product is genuinely the best solution, mention it as ONE option among alternatives. Frame: "Another approach is using [tool], which handles this via [specific mechanism]." Never frame it as a recommendation.

**Content rules:**
- All code must be copy-paste-runnable. Include imports, variable declarations, and setup.
- Include expected output as a comment in the code block.
- If the solution has prerequisites (install a package, configure something), list them explicitly.
- Use inline code formatting for function names, variables, and short expressions (`len(arr)`, `response.json()`).
- No opinions. No "I think..." or "In my experience..." on Stack Overflow. State facts and back them with documentation links.

**Self-promotion guardrails:**
- Maximum 1 in 15 answers references your product.
- When you do reference it, the answer must ALSO provide a solution that does not require your product.
- Never link to your landing page, pricing page, or signup page. Only link to technical documentation or open-source repos.
- If the question is specifically about your product, you may answer fully — but disclose your affiliation: "Disclosure: I work on [product]."

### 4. Validate before posting

Before submitting, verify:
- [ ] Code compiles/runs without errors (mentally or actually execute it)
- [ ] The answer addresses the EXACT question asked, not a related question
- [ ] If code modifies the asker's snippet, the diff is clear
- [ ] Formatting: code blocks are fenced with language IDs, no raw URLs
- [ ] No markdown rendering issues (preview if possible)
- [ ] If an accepted answer already exists and is correct, adding another answer only makes sense if yours adds significant new value
- [ ] Answer length: 100-800 words. Under 100 is too terse for SO. Over 800 test reader patience.

### 5. Post and track

Using the `qa-platform-api-write` fundamental, submit the answer:

```bash
POST /questions/{QUESTION_ID}/answers/add
body: YOUR_ANSWER_HTML
key: YOUR_API_KEY
access_token: YOUR_ACCESS_TOKEN
site: stackoverflow
```

**Human action required:** If the Stack Overflow account has fewer than 50 reputation points, the agent drafts the answer and a human posts it. Once reputation exceeds 50, the agent can post via API.

Track the interaction using the `community-engagement-tracking` fundamental:
- Date, question ID, tags, answer type, link included (y/n), word count

### 6. Monitor answer performance

Check the answer 48 hours later using `qa-platform-api-read`:

```bash
GET /answers/{ANSWER_ID}?site=stackoverflow&key=YOUR_API_KEY&filter=withbody
```

Record:
- Upvote score
- Was it accepted?
- Any comments (respond to follow-ups within 24 hours)
- Question view count (correlates with long-term visibility)

If the answer receives a comment requesting clarification, edit the answer to address it — don't just reply in comments. Stack Overflow rewards self-contained answers.

## Output

- A posted answer on Stack Overflow (or draft for human posting if low reputation)
- Activity log entry with engagement metrics
- Follow-up edits and comment responses within 48 hours

## Triggers

- Triggered by question monitoring alerts (from `so-question-monitoring-automation` drill)
- Daily: answer 2-5 questions across target tags
- Prioritize: unanswered questions > questions with low-quality answers > questions with many views and no accepted answer
