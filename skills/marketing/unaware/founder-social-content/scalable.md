---
name: founder-social-content-scalable
description: >
  Founder Social & Content — Scalable Automation. AI-assisted batch generation scales output to daily
  multi-platform publishing. Automated distribution, content A/B testing, and lead routing
  find the 10x multiplier while reducing founder time to 30 minutes per week.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 30 leads or ≥ 16 meetings over 2 months"
kpis: ["Impressions per post", "Engagement rate", "Leads per week", "Meetings per week", "Founder time per week", "AI draft approval rate"]
slug: "founder-social-content"
install: "npx gtm-skills add marketing/unaware/founder-social-content"
drills:
  - founder-content-scaling
  - ab-test-orchestrator
  - linkedin-lead-capture
---

# Founder Social & Content — Scalable Automation

> **Stage:** Marketing → Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

Find the 10x multiplier for founder content without proportional increase in founder effort. AI-assisted batch generation scales from 3-5 posts/week to daily multi-platform publishing (14-21 posts/week across LinkedIn and Twitter/X). Automated n8n workflows handle scheduling, distribution, engagement collection, and lead routing. Content A/B testing identifies the highest-performing hooks, formats, pillars, and posting times. Founder's time drops from 3+ hours/week to under 45 minutes while output and results increase 5-10x.

Success = at least 30 leads or 16 meetings over 2 months from content-attributed inbound.

## Leading Indicators

- Publishing cadence: 7+ posts/week across platforms (daily LinkedIn + daily Twitter/X)
- AI draft approval rate: ≥ 80% first pass (voice profile is well-calibrated)
- Engagement rate stable: within 80% of Baseline average despite higher volume
- Lead capture automated: n8n workflow routing leads from engagement to Attio without manual entry
- A/B tests running: at least 1 active experiment on hooks, formats, posting times, or CTAs
- Founder time: ≤ 45 minutes/week on content (batch review + high-value engagement)
- Leads per week trending up over the 8-week period

## Instructions

### 1. Scale content production with AI batch generation

Run the `founder-content-scaling` drill to build the 10x content engine:

1. **Analyze performance patterns**: Query PostHog for the last 30 days of content performance. Rank all posts by engagement rate and lead generation. Extract: which pillars produce leads, which formats get engagement, which hooks drive impressions, which posting times work best.

2. **Build the weekly batch pipeline**: Generate 14-21 post drafts per week using the `ai-content-ghostwriting` fundamental with:
   - Founder voice profile (refined over 4+ weeks of Baseline data)
   - Content performance profile (top patterns from PostHog data)
   - 7 LinkedIn posts (1/day, rotating across top pillars)
   - 7 Twitter/X adaptations (shorter, punchier versions)
   - 2-3 cross-platform variations for high-confidence topics

3. **Streamline founder review**: Present all drafts for a single 30-minute review session. Founder marks each as approve, edit, or reject. Target: 80%+ approval on first pass.

4. **Automate distribution**: Build 4 n8n workflows:
   - Daily LinkedIn Publisher: posts at optimal time from content queue
   - Daily Twitter/X Publisher: posts 2 hours offset from LinkedIn
   - Engagement Collector: pulls metrics for all posts published in last 48 hours
   - Lead Alert: notifies founder when a post exceeds 2x average engagement

### 2. Launch content A/B testing

Run the `ab-test-orchestrator` drill to systematically optimize content:

**Test 1 (weeks 1-2): Hook styles**
- Control: story-opening hooks ("Last week I made a $40K mistake...")
- Variant: statistic-opening hooks ("73% of founders get this wrong...")
- Metric: engagement rate per post
- Minimum: 10 posts per variant before declaring winner

**Test 2 (weeks 3-4): Content format**
- Control: best-performing format from Baseline
- Variant: alternate format (if text posts won Baseline, test list posts or carousels)
- Metric: leads generated per post (not just engagement)

**Test 3 (weeks 5-6): Posting cadence**
- Control: 5 posts/week (Baseline cadence)
- Variant: 7 posts/week (daily)
- Metric: total leads per week (does daily posting produce proportionally more leads, or does quality drop?)

**Test 4 (weeks 7-8): CTA optimization**
- Control: question CTA ("What's your take?")
- Variant: action CTA ("DM me 'playbook' for the template")
- Metric: DM conversion rate

Run one test at a time. Each test needs 10+ posts per variant minimum. Use PostHog experiments with content pillar and format as segment properties.

### 3. Automate lead capture and routing

Run the `linkedin-lead-capture` drill at Scalable configuration:

Build the automated n8n lead capture workflow:
1. **Daily trigger** (9am): Pull yesterday's engagement data from Taplio/Shield API.
2. **Filter for ICP**: Check each engager against ICP criteria (title matches target titles, company size > threshold).
3. **Enrich via Clay**: Send matching profiles for enrichment (email, company data, tech stack).
4. **Create CRM record**: Create or update lead in Attio with: name, title, company, LinkedIn URL, source_post_url, signal_type, enrichment data.
5. **Log to PostHog**: `social_lead_captured` event with all properties.
6. **Route**: High-intent leads (DMs, product questions) get an immediate Slack alert to the founder. Medium-intent leads (multiple engagements, ICP match) go into a nurture queue.

### 4. Implement content recycling

Identify the top 10% of posts by engagement from 60+ days ago. Generate refreshed versions with the same core insight but new hooks and updated examples. Add refreshed posts to the content queue. This extends the life of proven content indefinitely.

Schedule a monthly recycling review via n8n: query PostHog for top performers from 60+ days ago, generate refreshed versions, add to next week's batch.

### 5. Monitor scaling health

Track weekly in PostHog:
- Total posts published per platform
- Average engagement rate per post (must stay within 80% of Baseline)
- Leads generated per week (should increase with volume)
- Leads per post (should stay stable or improve)
- Founder time per week (target: ≤ 45 minutes)
- AI draft approval rate (target: ≥ 80%)

**Guardrail**: If engagement rate drops below 60% of Baseline for 2 consecutive weeks, reduce posting frequency immediately. Volume without engagement is noise, not scale.

### 6. Evaluate against threshold

At the end of 2 months, measure:

**Pass threshold:** ≥ 30 leads or ≥ 16 meetings over 2 months

All leads and meetings must be content-attributed in PostHog (prospect engaged with content before converting).

If PASS: document the complete system — content generation pipeline, n8n workflows, A/B test winners, lead routing automation. Proceed to Durable.

If FAIL: diagnose —
- Volume but low leads? Content is reaching people but not attracting buyers. Review content pillars — shift toward more specific ICP problems.
- Good leads but low meetings? Lead follow-up is too slow or DM quality is poor. Tighten the alert-to-DM response time to <4 hours.
- Engagement rate crashed? Scaled too fast. Reduce to 5 posts/week and rebuild quality.
- A/B tests inconclusive? Not enough volume per variant. Run each test for longer or reduce the number of simultaneous tests.

Re-run the final 4 weeks with adjustments.

## Time Estimate

- Content scaling setup (n8n workflows, scheduling tools): 6 hours (one-time)
- Weekly batch generation and founder review (8 weeks x 45 min): 6 hours
- A/B test setup and analysis (4 tests): 4 hours
- Lead capture automation setup: 4 hours (one-time)
- Daily monitoring and high-value engagement (40 days x 15 min): 10 hours
- Weekly reviews and optimization (8 x 30 min): 4 hours
- Content recycling setup: 2 hours (one-time)
- Evaluation and documentation: 2 hours
- **Total: ~38 hours active work over 2 months** (budget allows 60 hours including iteration)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free account) | Publishing, engagement, DMs | Free |
| Taplio | LinkedIn analytics + scheduling + AI assist | ~$49/mo (https://taplio.com/pricing) |
| Typefully or Buffer | Cross-platform scheduling (Twitter/X) | ~$12-25/mo (https://typefully.com/pricing / https://buffer.com/pricing) |
| PostHog | Event tracking, experiments, dashboards | Free up to 1M events/mo (https://posthog.com/pricing) |
| Clay | Lead enrichment | From $149/mo (https://www.clay.com/pricing) |
| Anthropic Claude API | Content generation and adaptation | ~$2-5/mo at scale (https://www.anthropic.com/pricing) |
| n8n (self-hosted) | Workflow automation | Free self-hosted (https://n8n.io/pricing) |
| Attio | CRM for lead management | Free up to 3 users (https://attio.com/pricing) |

## Drills Referenced

- `founder-content-scaling` — AI batch generation, n8n distribution, content recycling, and cross-platform adaptation
- `ab-test-orchestrator` — systematic A/B testing of hooks, formats, cadence, and CTAs
- `linkedin-lead-capture` — automated lead capture, enrichment, and CRM routing from engagement
