---
name: linkedin-founder-threads-durable
description: >
  Founder LinkedIn content — Durable Intelligence. AI agent autonomously monitors
  content performance, recommends content strategy changes, runs continuous experiments,
  and sustains or improves lead volume over 6 months with weekly founder review.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving lead volume (>= 10 leads/month) over 6 months with autonomous agent optimization; founder spends < 20 min/week"
kpis: ["Monthly leads from LinkedIn", "Lead-to-meeting conversion rate", "Content-attributed pipeline value", "Engagement rate trend (3-month rolling)", "Founder time per week"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
drills:
  - founder-linkedin-content-batch
  - linkedin-lead-capture
  - dashboard-builder
  - threshold-engine
---

# Founder LinkedIn Content — Durable Intelligence

> **Stage:** Marketing > Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

The content system runs autonomously with an AI agent managing content strategy, performance monitoring, and experimentation. The founder's involvement is reduced to <20 minutes/week (reviewing AI-generated batches and approving strategy changes). Lead volume from LinkedIn content is sustained at or above the Scalable baseline (10+ leads/month) for 6 consecutive months. The agent detects performance declines before they become problems and adapts content strategy based on data.

## Leading Indicators

- Agent successfully generates weekly content batches that require <5 edits from the founder
- Performance dashboard shows no 2-week declining trend in leads or engagement
- Agent experiments produce at least 1 measurable improvement per month
- Content-attributed pipeline value is growing month-over-month
- Founder reports spending <20 minutes/week on LinkedIn content (down from 3+ hours at Smoke)

## Instructions

### 1. Build the performance monitoring dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard:

**Weekly overview panel:**
- Total impressions this week vs. last week vs. 4-week average
- Average engagement rate this week vs. Scalable baseline
- Leads captured this week vs. target (10/month = ~2.5/week)
- Follower growth this week

**Content pillar performance panel:**
- Leads per post by content pillar (bar chart, last 30 days)
- Engagement rate by content pillar (bar chart, last 30 days)
- Best-performing post this month with metrics

**Attribution panel:**
- Leads by signal type (DM, comment, connection, profile view)
- Average days from first engagement to meeting booked
- Pipeline value attributed to LinkedIn content (if deals in CRM have source tracking)
- Monthly lead trend (line chart, last 6 months)

**Experiment panel:**
- Active experiments and their current results
- Completed experiments and decisions made
- Next experiment recommendation

### 2. Configure the autonomous threshold engine

Run the `threshold-engine` drill with these LinkedIn-specific thresholds:

**Performance thresholds:**
- Leads per month: minimum 10 (Scalable baseline)
- Average engagement rate: minimum 2%
- Impressions per post: minimum 500 (or 2x account baseline)
- Profile views per week: minimum 50

**Guardrails:**
- If engagement rate drops below 1.5% for 2 consecutive weeks: ALERT - content quality declining
- If leads drop below 5/month: ALERT - content is not converting
- If follower growth goes negative for 2 consecutive weeks: ALERT - audience is disengaging
- If founder editing time exceeds 45 minutes/week for 2 consecutive weeks: ALERT - AI voice quality declining

**Automated actions via n8n:**
- Daily: pull Taplio analytics, update PostHog events, check thresholds
- Weekly (Monday AM): generate performance summary and send to founder via Slack/email
- When threshold breached: send immediate alert with diagnosis and recommended action

### 3. Set up AI agent for content strategy

Configure an AI agent (Claude Code, Letta, or n8n AI node) that runs weekly:

**Monday morning agent routine:**

1. **Pull last week's data:** Query Taplio API for all post analytics from the past 7 days. Query Attio API for leads captured with `lead_source` = "linkedin-content" in the past 7 days.

2. **Analyze performance:** Compare each post's metrics against the 4-week rolling average. Identify:
   - Which content pillar produced the most leads this week
   - Which hook style had the highest engagement rate
   - Which CTA drove the most DMs/leads
   - Whether any format (text, carousel, video) significantly outperformed

3. **Generate a strategy brief:** Output a 1-page summary:
   ```
   ## Last Week Performance
   - Posts published: {N}
   - Total impressions: {N} ({+/-X%} vs. 4-week avg)
   - Engagement rate: {X%} ({+/-X%} vs. 4-week avg)
   - Leads captured: {N} ({+/-X%} vs. 4-week avg)
   - Top post: {URL} — {impressions} impressions, {engagement_rate}% engagement

   ## Recommendations for This Week
   - Primary pillar: {pillar} (produced {X} leads last week)
   - Hook style: {style} (highest engagement rate at {X%})
   - CTA: {cta_type} (produced {X} leads last week)
   - Format mix: {X} text, {Y} carousel, {Z} video
   - Test this week: {specific experiment recommendation}

   ## Content Briefs
   1. {Topic + angle + suggested hook}
   2. {Topic + angle + suggested hook}
   3. {Topic + angle + suggested hook}
   4. {Topic + angle + suggested hook}
   5. {Topic + angle + suggested hook}
   ```

4. **Generate the content batch:** Using the `founder-linkedin-content-batch` drill, produce 5-7 post drafts aligned with the strategy brief.

5. **Send to founder for review.** The founder receives the strategy brief + drafts. They approve/edit the batch in <20 minutes.

### 4. Run continuous experiments

The agent proposes and runs one experiment per month:

**Experiment framework:**
1. Agent identifies the biggest opportunity (e.g., "Carousel posts get 2x engagement but we only do 1/week")
2. Agent proposes a hypothesis: "If we increase carousels to 3/week, leads will increase by 30%"
3. Agent designs the test: 4 weeks of increased carousels with lead tracking
4. Agent monitors results weekly and reports progress
5. At 4 weeks, agent evaluates: significant improvement? -> make permanent. No change? -> revert.

**Types of experiments the agent should run:**
- Content pillar rotation (add a new pillar, retire the weakest)
- Posting time optimization (shift by 1-2 hours, measure impressions)
- Format mix changes (more carousels, more video, more polls)
- Hook pattern evolution (new hook formulas based on trending patterns)
- CTA experiments (DM triggers, link-in-comments, question prompts)
- Cross-posting to Twitter/X (test if the same content generates leads on a second platform)

### 5. Monthly content strategy review

**Human action required:** Once per month, the founder reviews a comprehensive report:

1. **Performance summary:** Monthly leads, pipeline attributed, engagement trends
2. **Content audit:** Which pillars are thriving vs. declining
3. **Audience evolution:** Are followers and leads still matching ICP? Check Taplio audience demographics.
4. **Experiment results:** What was tested, what won, what changed
5. **Next month's strategy:** Agent's recommended focus areas and experiments

The founder approves the next month's direction or overrides with their own priorities. This is the founder's main involvement -- everything else is automated.

### 6. Adapt to platform and market changes

The agent monitors for external changes:

- **LinkedIn algorithm changes:** If overall impression volume shifts suddenly (>30% change across all posts with no content change), flag it. Research via web search what changed. Adapt strategy (e.g., LinkedIn deprioritized text posts? Shift to video).
- **Market shifts:** If a new competitor, industry event, or trend emerges that your ICP cares about, the agent proposes reactive content to capitalize on the moment.
- **Content fatigue:** If the same pillar's engagement is declining month-over-month, propose retiring it and testing a replacement.

### 7. Evaluate sustainability

**Pass threshold: Sustained >= 10 leads/month from LinkedIn content for 6 consecutive months, with founder spending < 20 minutes/week.**

Additional success criteria:
- At least 3 experiments completed with documented results
- Content-attributed pipeline value is positive and growing
- The system can survive the founder being unavailable for 2 weeks (content is pre-batched, automation captures leads, agent adjusts as needed)

If lead volume declines below threshold for 2 consecutive months despite agent optimization, diagnose: is the audience saturated? Is the market shifting? Consider adding a new platform (Twitter/X, YouTube Shorts) or evolving the content strategy fundamentally.

## Time Estimate

- Dashboard + threshold setup: 6 hours (one-time)
- AI agent configuration: 8 hours (one-time)
- Weekly founder review (24 weeks x 20 min): 8 hours
- Monthly strategy review (6 x 1 hour): 6 hours
- Experiment design and monitoring: 12 hours total
- Ongoing automation maintenance: 4 hours total
- **Total: ~44 hours active work over 6 months** (remainder is agent-automated: content generation, lead capture, performance monitoring, strategy adaptation)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free) | Publishing, engaging, DMs | Free |
| Taplio Standard | Scheduling + analytics + AI | [$65/mo](https://taplio.com/pricing) |
| Claude API | Content generation + agent analysis | ~$2-5/mo at weekly batch cadence |
| PostHog | Dashboards + event tracking | [Free tier: 1M events/mo](https://posthog.com/pricing) |
| Attio | CRM for lead tracking + attribution | Free tier or existing plan |
| Clay | Lead enrichment (automated) | [$149/mo Explorer](https://www.clay.com/pricing) or existing plan |
| n8n | Automation: lead capture, alerts, agent orchestration | [$20/mo Starter](https://n8n.io/pricing/) or self-hosted free |
| Shield (optional) | Deeper LinkedIn analytics | [$16/mo Creator](https://www.shieldapp.ai/personal-pricing) |

**Durable total cost: ~$85-255/mo** depending on Clay usage and tool choices

## Drills Referenced

- `founder-linkedin-content-batch` -- AI-generated weekly batch with agent strategy input
- `linkedin-lead-capture` -- fully automated lead capture and enrichment pipeline
- `dashboard-builder` -- comprehensive performance dashboard in PostHog
- `threshold-engine` -- automated pass/fail checks and guardrail alerts
