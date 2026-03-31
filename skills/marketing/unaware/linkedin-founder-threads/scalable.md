---
name: linkedin-founder-threads-scalable
description: >
  Founder LinkedIn content — Scalable Automation. Scale to daily posting with automated
  lead capture, content repurposing, A/B testing of hooks and formats, and n8n workflows
  that route leads to CRM without manual effort.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 20 inbound leads over 2 months with automated lead capture and content system producing 5+ posts/week"
kpis: ["Weekly impressions total", "Engagement rate by pillar", "Leads captured per week", "Lead-to-meeting conversion rate", "Follower growth rate"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
drills:
  - founder-linkedin-content-batch
  - linkedin-lead-capture
  - ab-test-orchestrator
  - content-repurposing
---

# Founder LinkedIn Content — Scalable Automation

> **Stage:** Marketing > Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

The content system produces 5-7 posts per week with minimal founder editing time (under 30 minutes/week). Lead capture is automated via n8n + Taplio + Attio. A/B testing on hooks, formats, and CTAs has identified the highest-performing patterns. Content repurposing extends each original post into 2-3 derivative pieces. At least 20 inbound leads over 2 months, with clear attribution showing which content pillars drive pipeline.

## Leading Indicators

- Content batch creation takes under 30 minutes of founder time per week
- Automated lead capture catches 90%+ of engagement signals without manual review
- A/B test on hook style or CTA produces a statistically significant winner within 4 weeks
- Weekly lead volume is stable or increasing (not declining as volume scales up)
- Engagement rate holds above 2% even as posting frequency increases

## Instructions

### 1. Scale posting frequency to daily

Using the `founder-linkedin-content-batch` drill, increase the weekly batch to 5-7 posts:

1. Expand from 3 content pillars to 4-5 pillars. Add pillars based on Baseline data -- which topics got the most leads?
2. Generate 7 drafts per week via LLM API. The voice profile should be mature enough from Baseline that drafts need minimal editing.
3. **Human action required:** Founder spends 20-30 minutes reviewing the weekly batch. At this level, most edits should be minor -- adding a specific detail, sharpening a hook, adjusting a CTA.
4. Schedule in Taplio with 1-2 open slots for timely/reactive posts.
5. Include at least 1 carousel/document post per week (these get higher save rates and extended reach -- see `linkedin-organic-formats`).

### 2. Automate lead capture via n8n

Build the automated lead capture workflow from the `linkedin-lead-capture` drill:

1. **Create an n8n workflow** triggered on a daily schedule (9am):
   - Fetch yesterday's post engagement from Taplio API (`GET /api/v1/analytics/posts`)
   - For each engager, check if their job title matches ICP criteria (title contains keywords like VP, Head, Director, CEO, CTO, Founder + relevant function keywords)
   - Send matching profiles to Clay for enrichment (`POST /api/clay.com/v1/tables/{TABLE_ID}/rows` with LinkedIn URL)
   - Wait for Clay enrichment to complete, then create/update contact in Attio (`POST /api/attio.com/v2/objects/people/records`)
   - Log `linkedin_lead_captured` event in PostHog
   - Send Slack notification to founder with lead details and recommended action

2. **Create a DM alert workflow** in n8n:
   - Trigger: Taplio webhook or manual trigger when a DM is received
   - Classify DM intent: buying signal, question, partnership, spam
   - If buying signal: fast-track to CRM, set status "high-intent", notify founder immediately
   - If question: log as lead if ICP match, notify founder within 4 hours

3. **Set guardrails:**
   - Maximum 10 leads/day into CRM (if more, something is misconfigured or catching false positives)
   - Do not auto-DM anyone -- DMs must be human-written by the founder
   - Dedup check: do not create duplicate contacts in Attio

### 3. Launch A/B testing on content variables

Run the `ab-test-orchestrator` drill to systematically test content variables:

**Test 1 (Weeks 1-4): Hook styles**
- Variant A: Contrarian hooks ("Most founders get X wrong. Here's why.")
- Variant B: Story hooks ("Last Tuesday, something happened that changed how we think about X.")
- Sample: 10+ posts per variant. Measure: engagement rate and leads generated per post.
- Decision: adopt the winning hook style as your default; use the other for variety.

**Test 2 (Weeks 3-6): CTA types**
- Variant A: Comment-based CTA ("Drop your biggest challenge with X in the comments")
- Variant B: DM-based CTA ("DM me 'guide' and I'll send you our framework")
- Variant C: Link CTA ("Full breakdown in the comments -- link to [resource]")
- Sample: 8+ posts per variant. Measure: leads generated per post (not just engagement).
- Decision: adopt the CTA that produces the most leads, not the most comments.

**Test 3 (Weeks 5-8): Format**
- Variant A: Text-only posts (150-300 words)
- Variant B: Carousel/document posts (7-12 slides)
- Variant C: Short video (60-90 seconds, founder talking to camera)
- Sample: 6+ posts per variant. Measure: impressions, engagement rate, and leads.
- Decision: allocate posting frequency proportional to lead production by format.

Track all test results in PostHog. Log each post with properties: `hook_style`, `cta_type`, `format` so you can filter and compare.

### 4. Build content repurposing pipeline

Run the `content-repurposing` drill to multiply output from each original post:

1. **Weekly top performer -> long-form blog post:** Take the week's highest-engagement post. Expand it into a 1,000-word blog post with more depth, examples, and data. Publish on your company blog with SEO optimization.

2. **Carousel adaptation:** Take 2 list/framework posts and convert them into carousels (PDF uploaded as LinkedIn document posts). These get a second life and often outperform the original text version.

3. **Video derivative:** The founder records a 60-90 second video expanding on one post per week. Post as native LinkedIn video. Video gets prioritized in the algorithm and reaches a different audience segment.

4. **Newsletter integration:** If you run a newsletter (via Loops or similar), include the week's best-performing post insight in the next send. Reference the LinkedIn discussion to drive subscribers to follow the founder.

### 5. Build a content performance dashboard

Create a PostHog dashboard tracking:
- Weekly impressions total (trend line)
- Average engagement rate by content pillar (bar chart)
- Leads captured per week (trend line)
- Lead source breakdown: DM vs comment vs connection vs profile view (pie chart)
- Follower growth rate (trend line)
- A/B test results: performance by hook style, CTA type, and format (table)

Set alerts:
- Engagement rate drops below 1.5% for 2 consecutive weeks
- Lead volume drops below 2/week for 2 consecutive weeks

### 6. Evaluate against threshold

At the end of 2 months:
- Total leads captured in Attio with `lead_source` = "linkedin-content" over 60 days.
- **Pass threshold: >= 20 inbound leads over 2 months**
- Also verify: lead quality (are these ICP-matching contacts who could become pipeline?) and process efficiency (is the founder spending <30 min/week on content?).
- If PASS: document the content system, A/B test winners, and automation workflows. Proceed to Durable.
- If FAIL: check funnel. High impressions but low leads = wrong audience or weak CTAs. Low impressions = hooks are weak or posting times are off. Fix the bottleneck and re-run for another month.

## Time Estimate

- n8n automation setup: 4 hours (one-time)
- Weekly content batch + founder review (8 weeks x 45 min): 6 hours
- Daily engagement (40 days x 20 min): 13 hours
- A/B test setup and monitoring: 3 hours
- Content repurposing (8 weeks x 1 hour): 8 hours
- Weekly performance reviews (8 weeks x 30 min): 4 hours
- Dashboard setup: 2 hours
- Evaluation: 1 hour
- **Total: ~41 hours active work over 2 months** (remaining time is passive -- automation running, posts publishing on schedule)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free) | Publishing, engaging, DMs | Free |
| Taplio Standard | Scheduling + analytics + AI | [$65/mo](https://taplio.com/pricing) |
| Claude or GPT API | Generating post drafts | ~$0.20/month for 28-30 posts |
| PostHog | Event tracking + dashboards | [Free tier: 1M events/mo](https://posthog.com/pricing) |
| Attio | CRM for lead tracking | Free tier or existing plan |
| Clay | Lead enrichment | [$149/mo Explorer](https://www.clay.com/pricing) or existing plan |
| n8n | Automation workflows | [$20/mo Starter](https://n8n.io/pricing/) or self-hosted free |
| Loom or Descript (optional) | Video derivatives | [Loom Free](https://www.loom.com/pricing) / [$24/mo Descript](https://www.descript.com/pricing) |

**Scalable total cost: ~$85-235/mo** depending on Clay and video tool choices

## Drills Referenced

- `founder-linkedin-content-batch` -- weekly batch generation scaled to 5-7 posts
- `linkedin-lead-capture` -- automated lead capture via n8n + Clay + Attio
- `ab-test-orchestrator` -- systematic testing of hooks, CTAs, and formats
- `content-repurposing` -- multiplying content output across formats and channels
