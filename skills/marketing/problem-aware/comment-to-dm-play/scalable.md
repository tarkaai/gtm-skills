---
name: comment-to-dm-play-scalable
description: >
  Comment-to-DM Play — Scalable Automation. Scale the comment-to-DM motion with automated prospect
  discovery, AI-assisted comment drafting, multi-account monitoring, and systematic A/B testing of
  comment strategies to find the 10x multiplier.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "≥ 30 DM conversations and ≥ 12 meetings booked over 2 months with identified best-performing comment strategies"
kpis: ["Comments per week", "Author reply rate by strategy", "DM-to-meeting conversion rate", "Average days first-comment-to-meeting", "Cost per meeting"]
slug: "comment-to-dm-play"
install: "npx gtm-skills add marketing/problem-aware/comment-to-dm-play"
drills:
  - ab-test-orchestrator
---

# Comment-to-DM Play — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social

## Outcomes

Find the 10x multiplier for the comment-to-DM motion. The Baseline proved the motion works; Scalable finds out how to do 10x more with the same founder time. The levers: automated prospect discovery, AI-assisted comment drafting, expanded target lists, systematic A/B testing of strategies, and cross-platform expansion. The agent handles everything except final comment posting and DM sending.

## Leading Indicators

- Target list expanded to 80-100 active prospects across 3 tiers
- Comment volume: ≥ 40 comments per week with no quality degradation (author reply rate stable)
- Daily comment queue generated automatically with ≥ 80% acceptance rate by founder
- A/B test results: identified the 2-3 comment strategies that produce the highest author reply rate
- DM pipeline depth: ≥ 15 prospects in warming/warm/dm-ready stages at any time
- Average time from first comment to meeting decreasing month over month

## Instructions

### 1. Automate prospect discovery at scale

Run the the prospect content discovery workflow (see instructions below) drill (Option C -- Automated):

1. Build the n8n workflow that aggregates posts from Taplio CRM (now tracking 80-100 profiles) and Shield (tracking 10+ peer/competitor accounts)
2. Implement relevance scoring: topic match (pain points from ICP) x author tier x post freshness x engagement level (sweet spot: 5-50 comments)
3. Deliver a ranked daily comment queue of 15-20 posts to Slack each morning at 8am
4. The founder selects 8-12 to comment on (the rest are auto-archived)
5. Track acceptance rate: how often does the founder select a post from the auto-generated queue vs finding their own? Target: ≥ 80% queue acceptance means the discovery algorithm is working

### 2. Scale comment production with AI assistance

Extend the the comment crafting workflow (see instructions below) drill with batch AI drafting:

1. For each post in the daily queue, the agent reads the post and top comments
2. The agent generates 2 comment draft options per post using the Claude prompt template from the comment-crafting drill
3. The founder reviews drafts, picks one, edits for voice, and posts
4. Track: which drafts get posted as-is vs edited heavily? If >50% need heavy edits, refine the voice prompt

This reduces the founder's daily time from 30 minutes of writing to 15 minutes of review-and-edit.

### 3. Expand the target list to 80-100 profiles

Grow beyond the initial 30-40 prospects:

1. Use Clay to find new ICP-matching LinkedIn profiles. Run the `clay-people-search` fundamental against your target company list and filter for profiles with ≥ 1 post in the last 30 days (active posters)
2. Categorize new prospects into tiers
3. Add all to Taplio CRM for monitoring
4. Set up auto-discovery: the n8n workflow checks for new ICP-matching profiles posting about your topics weekly and suggests additions

### 4. Run A/B tests on comment strategies

Run the `ab-test-orchestrator` drill to systematically test what works:

**Test 1: Comment strategy type**
- Control: "Add Value" comments (share experience/data that extends the author's point)
- Variant: "Sharp Question" comments (ask a deep question that shows expertise)
- Metric: Author reply rate
- Duration: 2 weeks, minimum 50 comments per variant

**Test 2: Comment length**
- Control: 2-3 sentences
- Variant: 4-5 sentences with more depth
- Metric: Author reply rate + subsequent DM acceptance rate
- Duration: 2 weeks

**Test 3: Comment timing**
- Control: Comment within 1-2 hours of post
- Variant: Comment within 4-8 hours of post
- Metric: Comment likes + author reply rate
- Duration: 2 weeks

**Test 4: DM timing after reaching DM-ready**
- Control: DM within 24 hours of hitting DM-ready
- Variant: Wait 3-5 days after DM-ready (continue commenting, build more familiarity)
- Metric: DM reply rate + meeting conversion rate
- Duration: 4 weeks

Log all test results in PostHog. After each test, implement the winner and move to the next test.

### 5. Build the comment-to-DM pipeline dashboard

Expand the PostHog tracking from Baseline with Scalable-specific metrics:

- **Funnel by prospect tier**: Which tier converts best from comment to meeting?
- **Strategy effectiveness**: Which comment strategies produce the most author replies and eventual meetings?
- **Time-to-convert**: How many days and touches does each tier need on average?
- **Volume vs quality**: As comment volume increases, does reply rate hold steady?
- **Cost analysis**: Track founder time per meeting booked (the key efficiency metric at Scalable)

### 6. Evaluate against threshold

After 2 months, measure: ≥ 30 DM conversations AND ≥ 12 meetings booked. Also evaluate: has the founder's time per meeting decreased (efficiency gain)? Are the A/B tests producing actionable winners?

If PASS, proceed to Durable. If FAIL, the most common issue at Scalable is quality degradation at higher volume. Reduce volume, refine AI drafts, and focus on the highest-converting prospect tier and comment strategy.

## Time Estimate

- Automation setup (n8n discovery workflow, AI drafting pipeline): 4 hours
- Target list expansion and Clay enrichment: 2 hours
- Daily commenting (40 days x 15 min review + 5 min logging): 13 hours
- A/B test design and monitoring (4 tests): 4 hours
- Weekly pipeline reviews (8 x 30 min): 4 hours
- DM conversations and meeting booking: 5 hours
- Dashboard and reporting setup: 2 hours
- Monthly deep analysis (2 x 2 hours): 4 hours
- **Total: ~38 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Premium or Sales Navigator | Feed search, prospect discovery | $29.99-99/mo (https://www.linkedin.com/premium/) |
| Taplio | Track 80-100 prospect feeds, post monitoring | $49/mo (https://taplio.com/pricing) |
| Shield | Peer/competitor post monitoring | $25/mo (https://shieldapp.ai/pricing) |
| PostHog | Funnel analytics, A/B test tracking | Free up to 1M events (https://posthog.com/pricing) |
| Attio | CRM, cadence tracking | Free up to 3 users (https://attio.com/pricing) |
| Clay | Prospect enrichment, new prospect discovery | $149/mo Explorer plan (https://clay.com/pricing) |
| n8n | Automated discovery, event routing | Free self-hosted or $20/mo cloud (https://n8n.io/pricing) |
| Anthropic API | AI comment drafting | ~$10-30/mo at this volume (https://www.anthropic.com/pricing) |

## Drills Referenced

- the prospect content discovery workflow (see instructions below) — automated daily comment queue generation via n8n
- the comment to dm cadence workflow (see instructions below) — cadence management at scale with 80-100 tracked prospects
- `ab-test-orchestrator` — systematic testing of comment strategies, timing, and DM approaches
