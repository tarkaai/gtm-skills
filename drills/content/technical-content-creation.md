---
name: technical-content-creation
description: Create developer-facing technical content (tutorials, code samples, architecture posts) that demonstrates expertise and generates inbound interest
category: Content
tools:
  - Ghost
  - GitHub
  - AI (Claude / GPT)
  - PostHog
fundamentals:
  - technical-tutorial-authoring
  - ghost-blog-publishing
  - github-readme-optimization
  - github-repo-create
  - posthog-custom-events
  - linkedin-organic-formats
  - linkedin-organic-hooks
---

# Technical Content Creation

This drill produces developer-focused content that establishes authority in your domain and drives inbound developer leads. Unlike generic social content, technical content includes working code, architecture diagrams, benchmarks, and hands-on tutorials that developers trust and share.

## Input

- ICP definition: target developer roles, languages, frameworks, pain points (from `icp-definition` drill)
- Product capabilities and technical differentiators
- 3-5 content pillar topics aligned with ICP problems
- Publishing channels: blog (Ghost), GitHub, LinkedIn, dev community sites

## Steps

### 1. Map content pillars to developer pain points

For each content pillar, define 5-10 specific topics that combine:
- A pain point your ICP faces (from ICP research)
- A technical concept your product relates to
- A format that developers engage with

Topic formula: **[Pain Point] + [Technical Approach] + [Concrete Outcome]**

Examples:
- "How to process 10k webhooks/sec without dropping events" (pain + approach + outcome)
- "We benchmarked 5 vector databases — here are the results" (data-driven comparison)
- "Building an LLM-powered code review agent in 200 lines" (hands-on tutorial)

Prioritize topics where you have genuine expertise or data others do not have.

### 2. Create a technical blog tutorial

Using the `technical-tutorial-authoring` fundamental, generate a full tutorial:

1. Pick a topic from your content map that solves a real developer problem
2. Write the tutorial with working code samples — every code block must be copy-pasteable and tested
3. Include a companion GitHub repo (created via `github-repo-create`) with the complete working code
4. Optimize the repo's README using `github-readme-optimization` — include a CTA that links back to your product
5. Publish the tutorial on your blog via `ghost-blog-publishing`

### 3. Create a companion GitHub sample repo

For each tutorial, create a standalone sample repo:

1. Use `github-repo-create` to create the repo with a descriptive name (e.g., `webhook-processor-example`)
2. Push the working code from the tutorial
3. Use `github-readme-optimization` to write a README that:
   - Describes what the sample does in one sentence
   - Has a Quick Start section that works on first try
   - Links back to the full tutorial on your blog
   - Includes a CTA block linking to your product
4. Add topics/tags for GitHub discoverability (e.g., `webhooks`, `python`, `event-driven`)

### 4. Create social distribution versions

For each tutorial, produce derivative social posts using `linkedin-organic-formats` and `linkedin-organic-hooks`:

- **The Insight Post**: Extract the key takeaway and write a 200-word LinkedIn post with a hook, the insight, and a link to the full tutorial
- **The Code Snippet Post**: Share the most interesting code block with a brief explanation of what it does and why it matters
- **The Contrarian Take**: If the tutorial challenges a common approach, write a "hot take" post that links to the data/benchmarks in the tutorial
- **The Thread/Carousel**: Break the tutorial into 5-7 slides or a Twitter thread with step-by-step visuals

### 5. Track content performance

Using `posthog-custom-events`, fire events for each piece:

- `devrel_tutorial_published` — properties: title, pillar, format, url, github_repo_url
- `devrel_tutorial_read` — properties: url, read_time, scroll_depth, reader_referrer
- `devrel_github_clone` — properties: repo_name, cloner_referrer (tracked via GitHub traffic API)
- `devrel_cta_clicked` — properties: source_url, cta_type (signup, demo, docs)
- `devrel_social_post_published` — properties: platform, derivative_type, source_tutorial_url

### 6. Maintain a content backlog

After each piece, update your content backlog:
- Log what was published, when, and on which channels
- Note initial engagement signals (views, clones, social engagement)
- Queue the next 3 topics from your content map
- Flag topics where reader questions or comments suggest a follow-up tutorial

## Output

Per content cycle (weekly):
- 1 full technical tutorial (blog + GitHub repo + social derivatives)
- 3-5 social posts derived from the tutorial
- PostHog events flowing for all published content
- Updated content backlog with next topics queued

## Triggers

- Smoke: 1 tutorial per week (manual publish)
- Baseline: 2 tutorials per week (automated distribution)
- Scalable: 3-5 tutorials per week (batch production with AI assistance)
- Durable: continuous production optimized by `autonomous-optimization` drill
