---
name: developer-advocacy-program-baseline
description: >
  Developer Advocacy Program — Baseline Run. First always-on automation for technical content
  publishing, conference speaking pipeline, and community engagement. Automated content distribution,
  CFP tracking, and analytics prove the program sustains results over 8 weeks.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Events, Communities"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥10 content pieces, ≥2 conference talks submitted, and ≥20 qualified leads in 8 weeks"
kpis: ["Content-to-lead conversion rate", "Cost per developer lead", "CFP submission rate", "Community engagement growth rate", "Content distribution cycle time"]
slug: "developer-advocacy-program"
install: "npx gtm-skills add marketing/problem-aware/developer-advocacy-program"
drills:
  - technical-content-creation
  - content-repurposing
  - conference-cfp-pipeline
  - posthog-gtm-events
  - threshold-engine
---

# Developer Advocacy Program — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Events, Communities

## Outcomes

Prove the developer advocacy program sustains results with always-on automation. Content distribution, analytics tracking, and CFP pipeline run continuously. The advocate produces content; the system handles distribution, tracking, and speaking opportunity discovery.

Success: ≥10 technical content pieces published, ≥2 conference talk proposals submitted, and ≥20 qualified developer leads captured in 8 weeks.

## Leading Indicators

- Weekly tutorial publishing cadence maintained (≥2/week)
- Automated social distribution delivers 3-5 derivative posts per tutorial
- GitHub sample repos receive ≥10 clones/week (aggregate)
- CFP pipeline has ≥5 scored opportunities at any given time
- PostHog funnel shows content → lead conversion rate ≥2%
- Community engagement produces ≥3 referral visits/week

## Instructions

### 1. Set up content distribution automation

Using the `content-repurposing` drill, build the automated pipeline:

1. **Content intake:** Each tutorial published triggers automatic derivative creation — the agent generates a LinkedIn post, a Twitter/X post, a code snippet graphic, and a newsletter mention from each tutorial
2. **Scheduling:** Connect to a scheduling tool (Buffer, Typefully, or n8n direct posting) to distribute derivatives over 5-7 days following the tutorial publish date
3. **Cross-platform adaptation:** LinkedIn derivatives should be 200-300 words with a hook and tutorial link. Twitter/X derivatives should be ≤280 chars or a 3-5 tweet thread. Newsletter snippets should be 300-500 words with expanded context

The goal: each tutorial generates 4-6 distribution touchpoints without manual effort beyond writing the original.

### 2. Configure analytics tracking

Run the `posthog-gtm-events` drill to track developer advocacy events:

- `devrel_tutorial_published` — properties: title, pillar, url, github_repo_url
- `devrel_tutorial_read` — properties: url, read_time_seconds, scroll_depth, referrer
- `devrel_github_clone` — properties: repo_name, referrer_source
- `devrel_social_post_published` — properties: platform, derivative_type, source_tutorial_url
- `devrel_social_engagement` — properties: platform, post_url, likes, comments, shares, impressions
- `devrel_community_post` — properties: platform, thread_url, topic, engagement_score
- `devrel_lead_captured` — properties: source_type (content, community, speaking), source_detail, lead_title, lead_company
- `devrel_cfp_submitted` — properties: conference_name, talk_title, conference_date, audience_size
- `devrel_cfp_accepted` — properties: conference_name, talk_title

Connect blog analytics, GitHub traffic API, and social platform analytics to PostHog via n8n webhooks.

### 3. Launch the conference CFP pipeline

Run the `conference-cfp-pipeline` drill to systematically find and apply to speaking opportunities:

1. **Discover CFPs:** Run the CFP search every 2 weeks to find open call-for-papers at developer conferences matching your content pillars
2. **Score and prioritize:** Rank CFPs by ICP audience density, topic fit, audience size, and logistics. Focus on conferences where your target developers attend
3. **Draft proposals:** For each CFP scoring 60+, generate a talk proposal using AI. The talk should teach a concept from your tutorials — NOT pitch your product. Include concrete takeaways and code examples
4. **Submit and track:** Submit proposals and log each in Attio with: conference name, talk title, submission date, expected notification date. Track in PostHog: `devrel_cfp_submitted`
5. **Target:** ≥2 proposals submitted per month. Track acceptance rate to calibrate proposal quality

### 4. Establish community engagement cadence

Formalize the community engagement from Smoke into a repeatable cadence:

1. **Monitor:** Set up keyword alerts in your target communities (from Smoke) for pain points your tutorials address
2. **Respond:** When a relevant question appears, craft a helpful answer that references your tutorial (link to blog, not product). Target: 3-5 community responses per week
3. **Post:** Publish 1 original community post per week (a how-to, benchmark, or lessons-learned post). Adapt from your tutorials using the `content-repurposing` drill
4. **Track:** Log all community activity in PostHog: `devrel_community_post` with engagement scores

### 5. Execute an 8-week content calendar

Publish 2 tutorials per week for 8 weeks with automated distribution:

- Week 1-2: Continue the content pillars that worked in Smoke. Publish and let automation distribute.
- Week 3-4: Introduce 1 new content format (video tutorial, benchmark, or architecture deep-dive). Compare engagement against written tutorials.
- Week 5-6: Double down on the best-performing pillar and format combination. Start the content recycling system: refresh top-performing Smoke content with updated examples.
- Week 7-8: Review all data. Identify which content → community → lead paths produce the most qualified leads.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure results against: ≥10 content pieces, ≥2 conference talks submitted, and ≥20 qualified leads in 8 weeks.

- If PASS: proceed to Scalable. Document: best content pillars by lead generation, best communities by referral quality, CFP pipeline health, and automation reliability.
- If FAIL: diagnose which pillar is underperforming (content, speaking, or community). If content reach is low, test different distribution channels. If leads are low despite reach, adjust the CTA placement and tutorial-to-product bridge. Re-run for 4 more weeks.

## Time Estimate

- Content distribution automation setup: 3 hours
- Analytics tracking configuration: 2 hours
- CFP pipeline setup and first batch of proposals: 4 hours
- Community engagement cadence setup: 2 hours
- Ongoing content creation (2 tutorials/week x 8 weeks): ~6 hours (AI-assisted)
- Ongoing review and optimization: 1 hour/week
- Total: ~18 hours over the first 2 weeks of setup, then ~1.5 hours/week maintenance

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ghost / blog platform | Publish tutorials | Ghost Pro: $9/mo |
| GitHub | Sample repos + traffic API | Free |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo |
| n8n | Automation workflows | Self-hosted free / Cloud: $20/mo |
| Attio | CRM + CFP tracking | Free tier available |
| Clay | CFP discovery + enrichment | Starter: $149/mo |
| Claude API | Content drafting | Pay-per-use (~$5-15/mo at this volume) |
| Buffer or Typefully | Social scheduling | Buffer: $6/mo / Typefully: $12/mo |

**Total play-specific cost:** ~$50-200/mo depending on tool choices

## Drills Referenced

- `technical-content-creation` — produce tutorials, GitHub repos, and social derivatives at weekly cadence
- `content-repurposing` — automate cross-platform content distribution from each tutorial
- `conference-cfp-pipeline` — discover, score, and submit to conference speaking opportunities
- `posthog-gtm-events` — configure event tracking for all devrel activities
- `threshold-engine` — evaluate results against the pass threshold
