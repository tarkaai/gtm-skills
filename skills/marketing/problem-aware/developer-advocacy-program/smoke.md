---
name: developer-advocacy-program-smoke
description: >
  Developer Advocacy Program — Smoke Test. Produce 3 pieces of technical content (tutorials with
  working code samples) and engage 2 developer communities to generate ≥5 qualified developer leads
  in 3 weeks. Validates that your technical expertise resonates with your target developer audience
  before investing in always-on automation.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Events, Communities"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥3 pieces of technical content published and ≥5 qualified dev leads captured in 3 weeks"
kpis: ["Tutorial views", "GitHub repo clones", "Community engagement score", "Developer leads captured", "Time to first lead"]
slug: "developer-advocacy-program"
install: "npx gtm-skills add marketing/problem-aware/developer-advocacy-program"
drills:
  - icp-definition
  - technical-content-creation
  - social-content-pipeline
  - threshold-engine
---

# Developer Advocacy Program — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Events, Communities

## Outcomes

Prove that technical content (tutorials, code samples, architecture posts) attracts your target developer audience and converts interest into leads. This is a local, manual test — no automation, no budget. The agent helps research, draft, and prepare; a human publishes and engages.

Success: ≥3 technical content pieces published across blog and GitHub, ≥5 qualified developer leads captured within 3 weeks.

## Leading Indicators

- Tutorial page views > 100 per post within 7 days
- GitHub sample repo receives ≥5 clones within 7 days of creation
- LinkedIn/Twitter posts derived from tutorials get ≥3% engagement rate
- At least 2 inbound DMs or comments asking about your product/approach
- Community posts receive ≥5 upvotes or meaningful replies

## Instructions

### 1. Define your developer ICP

Run the `icp-definition` drill focused on developers. Document:
- Target developer roles (e.g., backend engineers, DevOps, data engineers)
- Programming languages and frameworks they use
- Specific technical pain points they search for solutions to
- Where they spend time online: which subreddits, Discord servers, Slack communities, Stack Overflow tags
- Content formats they engage with: tutorials, benchmarks, code samples, architecture deep-dives

### 2. Map 3 content topics to developer pain points

From your ICP research, select 3 topics where:
- Your target developers actively search for solutions (validate by checking subreddit questions, Stack Overflow frequency, Google Trends)
- You have genuine technical expertise or unique data
- Your product relates to the solution (but the content teaches the concept, not the product)

Topic formula: **[Developer Pain Point] + [Technical Approach] + [Concrete Outcome]**

Examples:
- "How to handle webhook delivery failures with exponential backoff and dead-letter queues"
- "Building a real-time data pipeline with 99.9% uptime — our architecture breakdown"
- "We load-tested 4 message queues — here is what happened at 50k msg/sec"

### 3. Create 3 technical content pieces

Run the `technical-content-creation` drill for each topic:

1. **Draft the tutorial** with working code samples. Every code block must be copy-pasteable and tested.
2. **Create a companion GitHub repo** with the complete working code, a README with quick start instructions and a CTA linking to your product.
3. **Publish the tutorial** on your blog.
4. **Create 2-3 social derivatives** per tutorial using the `social-content-pipeline` drill: an insight post, a code snippet post, and a discussion-starter post.

**Human action required:** Post the social content manually on LinkedIn and Twitter/X over 1-2 weeks. Engage with every comment and reply personally within 2 hours of posting.

### 4. Engage 2 developer communities

Choose 2 communities from your ICP research (subreddits, Discord servers, or Slack workspaces). For each:

1. Read 50+ recent posts to understand the community's tone and norms
2. Find 3-5 existing threads where your tutorial content directly answers a question or adds value
3. Write genuine, helpful replies that reference your tutorial (link to blog post, not product page)
4. Post 1 original value-first contribution per community (a how-to, a benchmark, or a lessons-learned post)

Do NOT automate community engagement at this level. Build authentic reputation first.

### 5. Track results manually

For each content piece, log:
- Blog post views (from your analytics)
- GitHub repo clones and stars (from GitHub traffic insights)
- Social post impressions, engagement rate, comments, DMs
- Community post upvotes, replies, and referral traffic
- Leads captured: anyone who books a demo, signs up, or requests more info — tag them `source: devrel-smoke` in your CRM

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure results against: ≥3 pieces of technical content published and ≥5 qualified dev leads captured in 3 weeks.

- If PASS: proceed to Baseline. Document which topics, formats, and communities produced the best results.
- If FAIL: adjust your topics (pick different pain points), try different communities, or change your content format (e.g., switch from long tutorial to short benchmark post). Re-run.

## Time Estimate

- ICP definition and topic mapping: 1.5 hours
- Content creation (3 tutorials + GitHub repos): 3 hours (AI drafts, human reviews and tests code)
- Social content derivatives: 0.5 hours
- Community engagement: 1 hour
- Total: ~6 hours over 1 week, with results measured over 3 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ghost / blog platform | Publish technical tutorials | Ghost Pro: $9/mo (or self-hosted free) |
| GitHub | Host sample code repos | Free |
| Claude API (Anthropic) | Draft tutorials and social content | Pay-per-use (~$0.50-2 per tutorial draft) |
| LinkedIn | Social distribution | Free |
| PostHog | Track content events | Free tier: 1M events/mo |
| Attio | CRM for lead tracking | Free tier available |

**Total play-specific cost:** Free (using free tiers)

## Drills Referenced

- `icp-definition` — define the target developer audience and their pain points
- `technical-content-creation` — produce tutorials with code samples, GitHub repos, and social derivatives
- `social-content-pipeline` — create social media posts derived from tutorials
- `threshold-engine` — evaluate results against the pass threshold
