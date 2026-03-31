---
name: technical-tutorial-authoring
description: Draft a developer tutorial with working code samples, repo links, and structured learning flow
tool: Anthropic
difficulty: Config
---

# Technical Tutorial Authoring

Generate a developer-facing tutorial that teaches a concept or workflow using your product (or adjacent tools). The output is a complete draft ready for review and publishing via `ghost-blog-publishing` or a docs-as-code pipeline.

## Tools

| Tool | Method | Best For |
|------|--------|----------|
| **Claude API** | `POST /v1/messages` with system prompt | Long-form tutorials with code |
| **OpenAI API** | `POST /v1/chat/completions` | Alternative LLM for drafting |
| **GitHub Copilot CLI** | `gh copilot explain` / inline suggestions | Code sample generation |
| **Mintlify / readme.com** | Docs-as-code hosting | If publishing to a docs site |
| **Ghost Admin API** | `POST /ghost/api/admin/posts/` | Blog-style tutorial publishing |

## Instructions

### 1. Define the tutorial scope

Provide the AI with a structured brief:

```
System: You are a senior developer advocate writing a tutorial for {TARGET_AUDIENCE}
(e.g., "backend engineers building webhook integrations").

Write a tutorial that:
- Solves a specific problem: {PROBLEM_STATEMENT}
- Uses these tools/libraries: {TOOL_LIST}
- Targets this skill level: {beginner | intermediate | advanced}
- Should take the reader {ESTIMATED_TIME} to complete
- Must include working code samples in {LANGUAGE}

Structure:
1. One-sentence hook explaining what the reader will build
2. Prerequisites (tools, accounts, versions)
3. Step-by-step instructions (each step = one logical unit of work)
4. Working code for each step (copy-pasteable, tested)
5. "What you built" summary with a screenshot or output sample
6. Next steps: links to related tutorials or docs
7. Troubleshooting section: 3-5 common errors and fixes

Rules:
- Every code block must be runnable as-is (no placeholders like "YOUR_API_KEY" without explaining how to get it)
- Use code comments to explain non-obvious lines
- Show expected output after each code block where applicable
- Keep prose between code blocks to 2-3 sentences max
- Never use phrases like "simply" or "just" — they imply ease where there may be friction
```

### 2. Generate the code samples

Run each code sample locally or in a sandbox to verify it works. If using Claude API:

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  anthropic-version: 2023-06-01
  Content-Type: application/json
Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "system": "{SYSTEM_PROMPT_FROM_STEP_1}",
  "messages": [
    {"role": "user", "content": "Write the tutorial based on the brief."}
  ]
}
```

### 3. Validate code samples

For each code block in the tutorial:
1. Create a temporary directory: `mktemp -d`
2. Write the code to files
3. Install dependencies and run
4. Capture output and compare to the tutorial's stated expected output
5. If any code fails, fix it and regenerate that section

### 4. Add metadata for SEO and attribution

Prepend the tutorial with frontmatter:

```yaml
---
title: "{Tutorial Title — include primary keyword}"
description: "{Under 155 chars — what the reader will learn}"
author: "{Author name}"
tags: ["{topic1}", "{topic2}", "{product-name}"]
canonical_url: "{URL if cross-posting}"
---
```

### 5. Format for publishing

Output the tutorial as Markdown with:
- Fenced code blocks with language identifiers (` ```python `, ` ```bash `, etc.)
- Heading hierarchy: H1 (title), H2 (major sections), H3 (sub-steps)
- Inline code for file names, CLI commands, and variable names
- Bold for UI elements or critical warnings
- Links to official docs for every third-party tool mentioned

## Output

A complete Markdown tutorial file ready for publishing. Contains:
- Frontmatter with title, description, tags
- Working code samples validated by execution
- Structured learning flow from setup to completion
- SEO-optimized title and description

## Error Handling

- If AI generates non-working code, re-prompt with the error message and ask for a fix
- If the tutorial exceeds 3,000 words, split into a series (Part 1, Part 2)
- If a dependency version has breaking changes, pin versions explicitly in the prerequisites
