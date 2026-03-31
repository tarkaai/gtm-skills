---
name: qa-platform-api-write
description: Post answers on Q&A platforms (Stack Overflow, Dev.to) via their APIs
tool: Stack Exchange API / Dev.to API
difficulty: Config
---

# Q&A Platform API -- Write Operations

Post answers, comments, and articles on Q&A platforms. Stack Overflow requires OAuth2 for write operations. Dev.to supports API-key-based publishing. Quora requires browser automation for posting.

## Stack Overflow -- Post an Answer

### Prerequisites

Write operations require a full OAuth2 access token (not just an API key):

1. Register an app at https://stackapps.com/apps/oauth/register
2. Set `OAuth Domain` to your domain and `Application Website` to your URL
3. Initiate OAuth2 flow: redirect user to:

```
https://stackoverflow.com/oauth?client_id=YOUR_CLIENT_ID&scope=write_access&redirect_uri=YOUR_REDIRECT_URI
```

4. Exchange the authorization code for an access token:

```bash
curl -X POST "https://stackoverflow.com/oauth/access_token" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=AUTH_CODE&redirect_uri=YOUR_REDIRECT_URI"
```

5. Response: `access_token=TOKEN&expires=86400`

### Post an answer

```bash
curl -X POST "https://api.stackexchange.com/2.3/questions/QUESTION_ID/answers/add" \
  -d "key=YOUR_API_KEY&access_token=YOUR_ACCESS_TOKEN&site=stackoverflow&body=YOUR_ANSWER_BODY_HTML&filter=default"
```

The `body` field accepts HTML (not Markdown). Convert Markdown to HTML before sending. The body must meet Stack Overflow quality standards:
- Minimum 30 characters
- Should include code blocks where relevant
- Should directly address the question asked

### Post a comment

```bash
curl -X POST "https://api.stackexchange.com/2.3/posts/POST_ID/comments/add" \
  -d "key=YOUR_API_KEY&access_token=YOUR_ACCESS_TOKEN&site=stackoverflow&body=YOUR_COMMENT"
```

Comments require 50+ reputation. Maximum 600 characters.

### Edit an answer

```bash
curl -X POST "https://api.stackexchange.com/2.3/answers/ANSWER_ID/edit" \
  -d "key=YOUR_API_KEY&access_token=YOUR_ACCESS_TOKEN&site=stackoverflow&body=UPDATED_BODY_HTML"
```

Edits require the same access token used to post the original answer or 2000+ reputation.

### Reputation requirements

Stack Overflow enforces minimum reputation for actions:
- Post answer: 1 (new accounts can answer immediately)
- Post comment: 50
- Upvote: 15
- Create tag: 1500
- Edit others' posts: 2000

**Human action required:** If the account is new (low reputation), the agent should draft the answer and the human posts it until enough reputation is earned.

## Dev.to -- Post an Article

### Post a response article

Dev.to does not have a comment API for programmatic posting, but you can publish articles that respond to other articles (common pattern on Dev.to).

```bash
curl -X POST "https://dev.to/api/articles" \
  -H "api-key: YOUR_DEV_TO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "article": {
      "title": "Re: How to handle API rate limiting in Node.js",
      "body_markdown": "Your Markdown content here...",
      "published": true,
      "tags": ["node", "api", "ratelimiting", "discuss"],
      "series": null
    }
  }'
```

### Update an article

```bash
curl -X PUT "https://dev.to/api/articles/ARTICLE_ID" \
  -H "api-key: YOUR_DEV_TO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "article": {
      "body_markdown": "Updated Markdown content..."
    }
  }'
```

## Quora -- Browser Automation

Quora has no write API. Post answers via Playwright:

```python
from playwright.async_api import async_playwright

async def post_quora_answer(question_url: str, answer_text: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="quora_auth.json")
        page = await context.new_page()
        await page.goto(question_url)
        # Click the "Answer" button
        await page.click('button:has-text("Answer")')
        # Wait for the editor
        await page.wait_for_selector('[contenteditable="true"]')
        # Type the answer
        await page.fill('[contenteditable="true"]', answer_text)
        # Submit
        await page.click('button:has-text("Post")')
        await page.wait_for_timeout(3000)
        await browser.close()
```

**Important:** Quora requires an authenticated session. Export cookies after manual login using `context.storage_state()`. Session tokens expire; refresh them weekly.

**Human action required:** Quora's terms of service restrict automated posting. Agent should draft answers; human reviews and posts manually until you confirm compliance with platform terms.

## Quality Guardrails (All Platforms)

Before posting any answer, verify:

1. **Relevance check**: The answer directly addresses the specific question asked.
2. **Uniqueness check**: The answer adds value not present in existing answers. If existing answers fully cover the question, skip it.
3. **Code quality**: All code examples must be syntactically valid, tested, and use current library versions.
4. **Self-promotion limits**: Maximum 1 in 10 answers includes a link to your own content. Link must be genuinely the best resource for the question.
5. **Length minimum**: Answers under 100 words rarely provide enough value. Target 150-500 words.
6. **Platform rules**: Check each platform's self-promotion policy before including any links.

## Error Handling

- **400 Bad Request**: Body too short, missing required fields, or malformed HTML.
- **401/403**: Token expired or insufficient reputation. Re-authenticate or escalate to human.
- **409 Conflict**: Duplicate answer detected. Skip this question.
- **429 Rate Limit**: Stack Exchange allows 40 write operations per day for non-trusted apps. Queue answers and spread across the day.
- **Captcha**: Stack Overflow may present a captcha for new or low-rep accounts. Flag for human intervention.
