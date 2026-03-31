---
name: q-a-sites-stackoverflow-etc-scalable
description: >
  Q&A Site Authority -- Scalable Automation. 10x output by automating question discovery,
  answer drafting, multi-platform expansion, and A/B testing answer formats.
stage: "Marketing > Problem Aware"
motion: "CommunitiesForums"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">= 300 profile clicks and >= 15 leads over 2 months"
kpis: ["Profile views", "Profile click rate"]
slug: "q-a-sites-stackoverflow-etc"
install: "npx gtm-skills add marketing/problem-aware/q-a-sites-stackoverflow-etc"
drills:
  - qa-question-discovery
  - dashboard-builder
  - qa-answer-crafting
  - qa-authority-performance-monitor
  - ab-test-orchestrator
---

# Q&A Site Authority -- Scalable Automation

> **Stage:** Marketing > Problem Aware | **Motion:** CommunitiesForums | **Channels:** Other

## Outcomes

Pass threshold: >= 300 profile clicks and >= 15 leads over 2 months.

This level finds the 10x multiplier. Instead of manually triaging alerts and writing each answer from scratch, the agent automates question scoring, drafts answers in batch, expands to additional Stack Exchange sites and platforms, and A/B tests answer formats to maximize upvotes and profile clicks per answer. Human effort shifts from writing answers to reviewing and approving agent-drafted content.

## Leading Indicators

- Answer output: 5-10 answers posted per day across all platforms (up from 3-5)
- Average upvotes per answer >= 8 (quality maintained at higher volume)
- Stack Overflow reputation crossing 200+ (established user status)
- Referral sessions from Q&A growing week-over-week in PostHog
- At least 2 answers appearing in Google search results for target keywords ("long-tail SEO from Q&A")
- Answer acceptance rate >= 20%

## Instructions

### 1. Expand platform coverage

Run `qa-question-discovery` with expanded scope:

1. **Add Stack Exchange sites** beyond Stack Overflow: identify 3-5 additional SE sites relevant to your domain (Server Fault, Software Engineering, Data Science, DevOps, etc.). Run `GET /sites?filter=default` on the Stack Exchange API to list all 170+ sites. For each candidate, check question volume in your tags.

2. **Add niche Q&A platforms**: Depending on your domain, expand to:
   - Hashnode (developer Q&A and blogging)
   - Stack Overflow for Teams alternatives if your ICP uses them
   - Industry-specific forums with Q&A sections (e.g., Spiceworks for IT, Biostars for bioinformatics)
   - Reddit Q&A threads (r/learnprogramming, r/webdev, etc. where questions are common)

3. **Increase Quora keyword coverage**: Expand from 5-10 keywords to 20-30. Add long-tail variants and competitor comparison queries.

Update the `dashboard-builder` workflows to include new platforms and keywords.

### 2. Automate answer drafting at scale

Enhance the `qa-answer-crafting` drill for batch operation:

1. The agent processes the daily answer queue (10-20 questions) and drafts all answers in a single batch using `ai-content-ghostwriting`.
2. Each draft includes: the specific answer format selected, working code examples (Stack Overflow), and UTM-tagged links where appropriate.
3. Drafts are queued for human review. The human reviews, makes minor edits, and approves for posting.
4. Approved answers are posted via API (Stack Overflow, Dev.to) or manually (Quora).

**Human action required:** Review and approve batched answer drafts daily. Target: 15-minute daily review session for 5-10 drafts. Reject answers that do not meet the quality bar -- better to post 5 excellent answers than 10 mediocre ones.

### 3. A/B test answer formats

Run the `ab-test-orchestrator` drill to optimize answer performance:

**Test 1: Answer length**
- Variant A: Concise answers (150-250 words, code-first)
- Variant B: Detailed answers (400-700 words, explanation-first)
- Metric: upvotes at 72h per answer
- Duration: 2 weeks (20+ answers per variant)

**Test 2: Self-link placement**
- Variant A: Link in a "Further reading" section at the end
- Variant B: Link inline mid-answer ("I wrote about this pattern in detail here")
- Variant C: No link (pure authority play, rely on profile clicks)
- Metric: profile clicks per answer, referral sessions
- Duration: 3 weeks

**Test 3: Response speed**
- Track correlation between time-to-answer (from question posting to your answer) and upvote count
- Hypothesis: answers posted within 2 hours of the question get 3x more upvotes than answers posted after 6 hours
- Use monitoring data to validate

Log all test results in PostHog via `posthog-experiments`.

### 4. Build the authority flywheel

Stack Overflow reputation is a compounding asset. At Scalable level, actively pursue reputation milestones:

1. **50 rep (comment privilege)**: Engage on others' questions by asking clarifying questions. This builds visibility without writing full answers.
2. **200 rep (reduced ads)**: Start editing and improving others' answers (suggested edits earn +2 rep each). Edits show your username on the post.
3. **1000 rep (established user)**: You appear in tag leaderboards. Create a tag wiki excerpt for a tag you use frequently (earns visibility + rep).
4. **Bounty strategy**: Place bounties (50-500 rep) on questions relevant to your domain to attract attention to topics where you can write the definitive answer. This costs reputation but builds massive visibility.

Track milestone progress in the weekly report.

### 5. Deploy comprehensive performance monitoring

Run the `qa-authority-performance-monitor` drill:

1. Daily tracking: answer upvotes, acceptance rate, reputation delta, new comments requiring follow-up.
2. PostHog dashboard: Q&A referral traffic trend, conversion funnel (visit -> signup), platform breakdown, top-performing answers by referral sessions.
3. Anomaly detection: alert if referral traffic drops >40% vs 4-week average, or if answer quality drops (average upvotes declining).
4. Weekly report to Slack: answers posted, upvotes earned, reputation change, referral sessions, signups, and leads.

### 6. Evaluate against threshold

At the end of 2 months, measure:
- Profile clicks: >= 300 total across all platforms.
- Leads: >= 15 signups, demo requests, or inbound emails with Q&A attribution.

**PASS**: Proceed to Durable.
**FAIL**: Diagnose by platform. Which platforms drive clicks but not leads? (Landing page issue.) Which platforms drive neither? (Drop them.) Is answer volume high but upvotes low? (Quality issue.) Adjust and re-run Scalable.

## Time Estimate

- Platform expansion and workflow updates: 4 hours
- Daily answer review and approval (15 min/day x 60 days): 15 hours
- A/B test setup and analysis: 4 hours
- Reputation-building activities: 5 hours
- Performance monitoring and weekly reviews: 4 hours
- Ongoing answer drafting (agent-automated, human reviews): 25 hours
- Total: ~57 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stack Exchange API | Read/write across 170+ SE sites | Free (10,000 req/day with key) |
| Dev.to API | Read and publish articles | Free |
| SerpAPI | Monitor Quora and niche platforms | ~$50-75/mo for 5,000-10,000 searches ([serpapi.com/pricing](https://serpapi.com/pricing)) |
| Syften | Real-time keyword monitoring (optional upgrade from polling) | $40/mo Standard plan ([syften.com](https://syften.com)) |
| PostHog | Attribution tracking, experiments, anomaly detection | Free tier or ~$0 at this volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Monitoring + automation workflows | Free self-hosted or from $20/mo cloud ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM, answer tracking, lead attribution | Included in standard stack |
| Anthropic API | Answer draft generation via Claude | ~$10-30/mo at this volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |

Estimated play-specific cost: $50-165/mo

## Drills Referenced

- `qa-question-discovery` -- expanded search across additional platforms and tags
- `dashboard-builder` -- always-on monitoring with expanded platform coverage
- `qa-answer-crafting` -- batch answer drafting with human review workflow
- `qa-authority-performance-monitor` -- full-funnel tracking from answers to pipeline
- `ab-test-orchestrator` -- test answer formats, link placement, and response timing
