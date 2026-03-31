---
name: guest-posting-scale-scalable
description: >
  Guest Posting at Scale — Scalable Automation. n8n workflows automate blog discovery, AI pitch
  generation, Instantly sending, reply routing, and competitor monitoring to 10x guest post
  output while maintaining quality.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: "≥20 published articles and ≥1,500 referral visits/month with automated pipeline"
kpis: ["Pitch acceptance rate (≥15%)", "Articles published per month", "Referral traffic per month", "Backlinks acquired (dofollow)", "Conversion rate from referrals", "Cost per published article"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - guest-post-outreach-automation
  - guest-post-article-pipeline
  - guest-post-performance-monitor
  - content-repurposing
---

# Guest Posting at Scale — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Outcomes

Automate the discovery-to-publication pipeline so guest posting runs at 10x the Baseline volume without proportional time investment. n8n workflows handle blog discovery, pitch generation, sending, and reply routing. The agent writes articles. Human involvement reduces to quality review of Tier 1 pitches and final article approval.

## Leading Indicators

- Automated blog discovery surfaces ≥15 new qualified targets per week
- Pitch sending volume reaches 50-60/week with acceptance rate holding ≥15%
- Article pipeline processes ≥5 accepted pitches per week
- Per-article time investment drops below 2 hours (vs. 3-4 hours at Baseline)

## Instructions

### 1. Deploy the automated outreach pipeline

Run the `guest-post-outreach-automation` drill to build four n8n workflows:

**Workflow 1 — Weekly Blog Discovery:**
- n8n cron triggers every Monday at 6am UTC
- Loops through 15-20 niche keywords in Ahrefs Content Explorer with guest post query variants
- Deduplicates against existing Attio targets
- Pushes new blogs to Clay for enrichment
- Scores and tiers enriched results
- Pushes to Attio with tier assignment
- Posts Slack summary: "Found {{count}} new targets. {{tier_1}} Tier 1, {{tier_2}} Tier 2."

**Workflow 2 — Pitch Generation and Sending:**
- Triggered by new "ready_to_pitch" records in Attio
- Pulls blog context from Clay (recent articles, audience, guidelines)
- Generates pitch angles via Anthropic API
- Selects best angle and populates pitch email template
- Tier 1 blogs: sends to Slack for human approval before sending
- Tier 2/3 blogs: queues in Instantly automatically
- Updates Attio: status = "pitched"

**Workflow 3 — Reply Routing:**
- Triggered by Instantly reply webhook
- Classifies reply via Anthropic API: accepted, interested, redirected, declined, paused, auto_reply
- Routes each classification to the appropriate follow-up action
- Accepted pitches trigger Slack alert and queue for article writing
- Updates Attio pipeline status for every reply

**Workflow 4 — Competitor Monitoring:**
- Weekly cron checks competitor backlinks via Ahrefs
- Identifies new competitor guest posts on DA 30+ blogs
- Cross-references against your target list
- Generates differentiated pitch angles for blogs where competitors published
- Queues counter-pitches into the pitch generation workflow

### 2. Scale article production

Run the `guest-post-article-pipeline` drill at scale (target: 5+ articles/week):

1. For each accepted pitch, the agent generates a full draft via Anthropic API within 4 hours of acceptance
2. AI editorial review runs automatically: style match, backlink naturalness, content quality
3. **Human action required:** Author reviews batches of 3-5 drafts in a single session (30 min/batch). Adds personal insights, approves or requests revision.
4. Approved articles are submitted to editors via email with article body + Google Doc link + author bio
5. Editorial feedback is handled within 24 hours

Build efficiency over time: save blog-specific style profiles so the AI generates closer-to-final drafts for repeat publications.

### 3. Maximize published content with repurposing

Run the `content-repurposing` drill for every published guest post that drives ≥100 referral visits:

1. Extract 3-4 key insights from the guest article
2. Transform each insight into a LinkedIn post via `linkedin-organic-formats`
3. Adapt the core argument into a newsletter section via `loops-broadcasts`
4. Share the publication link on social channels within 24 hours of going live
5. Thank the editor publicly on social media (builds the relationship for future pitches)

This extends the content lifecycle and drives additional traffic to the guest post, improving its SEO value.

### 4. Deploy performance monitoring

Run the `guest-post-performance-monitor` drill to create always-on tracking:

- Daily n8n workflow checks Ahrefs for new and lost backlinks from guest posts
- Weekly referral traffic analysis in PostHog with anomaly alerts
- PostHog dashboard showing: referral visits by source blog, conversion rate, backlink portfolio health, domain rating trend
- Per-article ROI tracking in Attio
- Weekly automated report: articles published, backlinks acquired, referral traffic, conversions, pipeline status

### 5. Set guardrails and quality gates

Configure these in the n8n workflows:

- **Pitch volume**: Maximum 15 new pitches/day across all sending accounts
- **Quality gate**: All Tier 1 pitches require human approval via Slack
- **Acceptance rate floor**: If acceptance rate drops below 12% for 2 consecutive weeks, pause automated pitching. Alert team. Diagnose: pitch quality, targeting, or topic fatigue?
- **Per-blog cooldown**: Minimum 90 days between pitches to the same blog
- **Article turnaround SLA**: Accepted pitches must have a draft submitted within 72 hours
- **Backlink health**: If ≥3 backlinks are lost in a week, investigate and alert team

### 6. Evaluate at month 2

Measure against:
- ≥20 published articles over 2 months
- ≥1,500 referral visits/month from guest posts
- Acceptance rate holding ≥15%
- Positive ROI: total time + tool costs vs. estimated SEO value of backlinks + conversion value

If PASS: Document the automated pipeline configuration, pitch template library, and style profiles. Calculate cost per published article. Proceed to Durable.

If FAIL: Identify the bottleneck. If discovery is fine but acceptance is low, refine pitch templates. If acceptance is fine but traffic is low, target higher-traffic blogs. If automation is breaking, fix workflow reliability before scaling further.

## Time Estimate

- n8n workflow setup (4 workflows): 12 hours
- Pipeline monitoring and maintenance (8 weeks): 16 hours
- Article review and approval (20+ articles): 10 hours
- Content repurposing: 8 hours
- Performance analysis and optimization: 9 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Workflow automation (4 workflows) | Self-hosted free, Cloud $20/mo (https://n8n.io/pricing) |
| Ahrefs | Blog discovery, backlink monitoring, competitor tracking | Standard $199/mo (https://ahrefs.com/pricing) |
| Clay | Editor enrichment, merge field population | Explorer $349/mo at scale (https://clay.com/pricing) |
| Instantly | Pitch email sending with inbox rotation | Hypergrowth $77.6/mo (https://instantly.ai/pricing) |
| PostHog | Referral tracking, conversion funnels, dashboards | Free up to 1M events (https://posthog.com/pricing) |
| Attio | Pitch pipeline CRM, blog relationship tracking | Plus $34/seat/mo (https://attio.com/pricing) |
| Anthropic API | Pitch generation, article drafting, reply classification | ~$5-10/mo at scale (https://anthropic.com/pricing) |

## Drills Referenced

- `guest-post-outreach-automation` — four n8n workflows automating discovery, pitching, reply routing, and competitor monitoring
- `guest-post-article-pipeline` — AI-assisted article writing and submission at 5+/week velocity
- `guest-post-performance-monitor` — always-on backlink, referral traffic, and conversion monitoring
- `content-repurposing` — turn high-performing guest posts into LinkedIn, newsletter, and social content
