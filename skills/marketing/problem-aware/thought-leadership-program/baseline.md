---
name: thought-leadership-program-baseline
description: >
  Thought Leadership Program — Baseline Run. Scale to 3-4 posts/week with scheduling tools,
  add speaking slot submissions, and validate repeatable content-to-lead generation over 8 weeks.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Social, Content, Events"
level: "Baseline Run"
time: "24 hours over 8 weeks"
outcome: ">=15 posts published, >=2.5% average engagement rate, >=2 speaking slots secured, and >=20 qualified leads attributed to content within 8 weeks"
kpis: ["Posts per week", "Engagement rate by pillar", "Follower growth rate", "Content-attributed leads", "Speaking submissions and acceptances"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - founder-linkedin-content-batch
  - conference-cfp-pipeline
  - threshold-engine
---

# Thought Leadership Program — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Social, Content, Events

## Outcomes

The first always-on thought leadership cadence. The agent generates weekly content batches using proven pillars, the founder reviews and approves, and a scheduling tool handles distribution. Speaking slot submissions begin. The goal is repeatability: can this program produce consistent engagement and leads week after week for 8 weeks?

**Pass threshold:** >=15 posts published, >=2.5% average engagement rate, >=2 speaking slots secured, and >=20 qualified leads attributed to content within 8 weeks.

## Leading Indicators

- Engagement rate per pillar remains stable or improves over 8 weeks (no decay)
- Follower growth rate exceeds 2% per week
- At least 1 content-attributed lead per week by week 4
- CFP acceptance rate >= 25% (at least 2 of 8 submissions)
- Content repurposing produces at least 2 derivative pieces per source post

## Instructions

### 1. Set Up Scheduling Infrastructure

Configure a LinkedIn scheduling tool:
- **Taplio** ($49/mo): AI-assisted scheduling with analytics — [taplio.com/pricing](https://taplio.com/pricing)
- **Buffer** ($10-15/mo): Simple cross-platform scheduling — [buffer.com/pricing](https://buffer.com/pricing)
- **Typefully** ($12/mo): LinkedIn and Twitter scheduling with thread support — [typefully.com](https://typefully.com)

Connect the founder's LinkedIn account. Verify scheduling works with a test post.

### 2. Run Weekly Content Batches

Run the `founder-linkedin-content-batch` drill every Friday or Monday:

1. Select 3-4 topics from the content pillars defined in Smoke, rotating across pillars
2. For each topic, define the specific angle, format (expand beyond text: add carousels, document posts), and hook type
3. Generate drafts using Claude API with the founder's voice profile
4. **Human action required:** Founder reviews all drafts (target: 30-45 min/week). Edits for authenticity. Approves or rejects.
5. Schedule approved posts via Taplio/Buffer/Typefully: Tuesday, Wednesday, Thursday at 8:00am ICP timezone
6. Leave 1 slot open for reactive/timely posts

Repeat weekly for 8 weeks. Track every post's performance in Attio.

### 3. Add Content Repurposing

For each week's top-performing post (highest engagement rate after 48 hours):

1. Repurpose into 2 additional formats:
   - Twitter/X thread (break the LinkedIn post into 5-7 tweets)
   - Blog post or newsletter section (expand with additional detail)
2. If the post includes data or a framework, create a simple visual (infographic or screenshot) for a second LinkedIn post
3. Log all derivative content with a reference back to the source post for attribution

### 4. Launch the Speaking Pipeline

Run the `conference-cfp-pipeline` drill:

1. Use the `conference-cfp-search` fundamental to find 8-10 conferences with open CFPs where your ICP attends
2. For each conference, use `clay-scoring` to rank by: ICP audience match (40%), conference size (25%), CFP deadline proximity (20%), cost to attend (15%)
3. Select the top 8 conferences to submit to
4. Generate talk proposals using Claude API: tie each proposal to a content pillar that has proven engagement
5. **Human action required:** Founder reviews and customizes each proposal. Submit.
6. Track all submissions in Attio: conference name, CFP deadline, submission date, topic, status (submitted / accepted / rejected / waitlisted)

Target: submit to 8 CFPs over 8 weeks. Accept rate benchmark: 25%+ (>=2 acceptances).

### 5. Track Attribution

Set up basic content-to-lead attribution:

1. Add UTM parameters to all CTA links in posts: `?utm_source=linkedin&utm_medium=organic&utm_campaign=thought-leadership&utm_content={post_id}`
2. Add the same UTM to the founder's LinkedIn profile link
3. In Attio, tag every new lead with their source: `content`, `speaking`, `referral`, or `other`
4. In PostHog, set up a funnel: `content_cta_click` -> `page_view` -> `lead_captured`
5. Log weekly: leads attributed to content, leads attributed to speaking, total pipeline value

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill after 8 weeks:

1. Compile metrics:
   - Total posts published (threshold: >=15)
   - Average engagement rate (threshold: >=2.5%)
   - Speaking slots secured (threshold: >=2)
   - Qualified leads attributed to content (threshold: >=20)
2. Pillar analysis: which pillars drove the most leads (not just engagement)?
3. Format analysis: which post formats produced the highest engagement and leads?
4. Time analysis: is engagement stable, growing, or declining over the 8 weeks?

**If PASS:** The content engine is repeatable. Proceed to Scalable with automation, multi-platform distribution, and content repurposing at scale.

**If FAIL:** Diagnose:
- Low engagement: test new hook styles or post formats. Consider video or carousel.
- Low leads: CTAs are weak or misaligned. Test direct vs indirect CTAs. Ensure the landing page converts.
- Low speaking acceptances: refine talk proposals. Target smaller, more niche events first.
- Declining engagement: content fatigue on one pillar. Rotate topics more aggressively or add a new pillar.

## Time Estimate

- 1 hour/week: Content batch generation + scheduling (8 weeks = 8 hours)
- 1 hour/week: Founder review and editing (8 weeks = 8 hours)
- 4 hours: CFP research, proposal writing, and submissions
- 2 hours: Attribution setup (UTMs, PostHog funnels, Attio tagging)
- 2 hours: Threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Taplio | LinkedIn scheduling + analytics | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |
| LinkedIn | Content publishing and engagement | Free — [linkedin.com](https://linkedin.com) |
| Attio | CRM — lead attribution and content tracking | Free or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Analytics — content funnel tracking | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Clay | Enrichment — CFP research and scoring | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Claude API | Content drafting and talk proposals | ~$20-30/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Taplio ~$49/mo. Other tools are standard stack or minimal incremental cost.

## Drills Referenced

- `founder-linkedin-content-batch` — generate, review, and schedule a week's worth of LinkedIn posts in the founder's voice using content pillars and voice profile
- `conference-cfp-pipeline` — discover open CFPs, craft talk proposals, submit, and track acceptance rates
- `threshold-engine` — evaluate Baseline results against the pass threshold and recommend next action
