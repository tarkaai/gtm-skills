---
name: workshop-series-educational-scalable
description: >
  Workshop Series — Scalable Automation. Transform one-off workshops into an
  automated monthly series with agent-managed promotion, Clay-powered prospect
  sourcing, content repurposing from each session, and A/B testing across topics,
  difficulty levels, exercise formats, and promotion channels. Multiply
  registrations and pipeline without proportional manual effort.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=160 total registrations, >=40% average show rate, >=50 qualified leads from monthly workshops over 3 months"
kpis: ["Registrations per workshop", "Show rate", "Exercise completion rate", "Qualified leads", "Cost per qualified lead", "Repeat attendance rate"]
slug: "workshop-series-educational"
install: "npx gtm-skills add marketing/solution-aware/workshop-series-educational"
drills:
  - workshop-series-automation
  - ab-test-orchestrator
  - content-repurposing
---

# Workshop Series — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content

## Outcomes

- Scale from ad-hoc workshops to a consistent monthly series with automated operations
- Reach 160+ total registrations across events with agent-managed promotion and prospect sourcing
- Generate 50+ qualified leads over 3 months through automated nurture and scaled promotion
- Identify the winning combination of topic, difficulty level, exercise format, timing, and promotion channel via A/B testing
- Build a content flywheel: each workshop produces derivative content (clips, blog posts, exercise templates) that drives future registrations
- Reduce per-workshop human effort to content delivery only (75 minutes) while automation handles everything else

## Leading Indicators

- Net-new registrations per workshop increasing (list growth, not just re-engaging existing contacts)
- At least 20% of registrations come from Clay-sourced net-new prospects
- Repeat attendance rate >15% (community building signal -- attendees returning for more advanced sessions)
- Content derivatives (clips, posts, exercise templates) drive >10% of next workshop's registrations
- Cost per qualified lead trending down as automation efficiency improves
- Exercise completion rate stable or improving as curriculum quality improves

## Instructions

### 1. Launch the automated workshop series

Run the `workshop-series-automation` drill to build the full series engine:

- Create a topic backlog scored by ICP pain alignment, competitive differentiation, and funnel position. Queue at least 6 topics across multiple difficulty levels. Map each topic to prerequisites, required materials, and exercise designs.
- Build the n8n promotion engine that auto-triggers 21 days before each workshop: registration page generation, email invite waves (day -14 and day -7), LinkedIn post scheduling, personal invite lists from Attio, prep sequence activation, and day-of reminders.
- Configure Clay to find 200-500 net-new, topic-relevant prospects per workshop using `clay-people-search` and `clay-enrichment-waterfall`. Filter by skill level when possible (e.g., target engineering managers for intermediate sessions, individual contributors for beginner sessions). Import into Loops for targeted invitation.
- Set up facilitator coordination workflows if workshops include guest experts or co-facilitators: prep call scheduling, technical check reminders, and post-event thank-you.
- Build the attendee preparation pipeline: automated prerequisite verification, environment setup instructions, and pre-workshop skill assessment to match attendees to the right difficulty level.

Target cadence: bi-weekly for the first month (2 workshops), then monthly. Evaluate cadence based on registration velocity, audience capacity, and content preparation bandwidth.

### 2. A/B test workshop variables

Run the `ab-test-orchestrator` drill to systematically test one variable at a time across successive workshops:

**Variables to test (in priority order):**

1. **Topic category**: Which pain point area drives the most registrations and pipeline? Test at least 3 distinct topic categories over the first 4 workshops.
2. **Difficulty level**: Beginner vs intermediate vs advanced. Track not just registrations but exercise completion and pipeline conversion by level.
3. **Exercise format**: Guided step-by-step vs open-ended challenge vs pair programming vs individual. Which produces the highest engagement and follow-up conversion?
4. **Day and time**: Tuesday 11am vs Wednesday 2pm vs Thursday 10am. Workshops may perform differently from webinars due to the time commitment.
5. **Workshop length**: 60 minutes vs 90 minutes vs 2 hours. Longer workshops may have lower show rates but higher conversion.
6. **Promotion channel mix**: Measure registration source by channel. Shift budget toward highest-converting channels.
7. **Email subject line**: A/B test invite email subject lines within the same send using Loops.

For each test, define the hypothesis, success metric, and minimum sample size before running. After each workshop, log the result and the learning in Attio. After 4 workshops, compile a "winning formula" document: best topic category, difficulty level, exercise format, time slot, and promotion channel.

### 3. Build the content repurposing flywheel

Run the `content-repurposing` drill after each workshop to multiply content output:

- **Recording -> clips**: Extract 3-5 highlight clips (60-90 seconds each) from each recording using Descript. Focus on: the clearest explanation of a concept, the most common mistake during exercises, the best audience question + answer, and a "before and after" showing what attendees built.
- **Recording -> tutorial blog post**: Transcribe the workshop and transform it into a step-by-step tutorial (1,500-2,500 words) that someone can follow asynchronously. Include screenshots from the exercises.
- **Exercise -> standalone template**: Package the exercise materials as a downloadable template or starter kit. Gate it behind email capture to drive future workshop registrations.
- **Clips -> LinkedIn posts**: Each clip becomes a LinkedIn post with a text hook showing the skill being taught, the video clip, and a CTA to register for the next workshop.
- **Q&A -> newsletter content**: The best audience questions become a "workshop Q&A" section in your newsletter via Loops.
- **Exercise outputs -> case studies**: If attendees produce impressive exercise outputs, request permission to use them as case studies or testimonials.

Schedule derivative content to publish over the weeks between workshops. Each piece of content should link to the next workshop's registration page, creating a flywheel where this workshop's content drives next workshop's registrations.

### 4. Scale registration through multi-channel promotion

Expand beyond manual outreach and email to a multi-channel promotion system:

- **Email (owned list)**: Segmented broadcasts via Loops. Send topic-relevant invites to the right audience segments. Match difficulty level to the recipient's history -- if they attended a beginner session, invite them to intermediate.
- **Clay prospecting**: 200-500 net-new prospects per workshop enriched and imported into the invite flow. Target by role, industry, and inferred skill level.
- **LinkedIn organic**: 3 posts per workshop (announcement with skill-gap hook, exercise preview clip, countdown with social proof) using content derivatives from previous workshops.
- **LinkedIn paid (optional)**: If budget allows, promote the registration page via LinkedIn Sponsored Content. Target by title + industry matching your ICP. Start with $200/workshop and measure cost per registration.
- **Personal invites**: Use Attio to identify high-value prospects in active pipeline. A workshop invite is a low-friction way to re-engage stalled deals -- prospects get value even if they do not buy.
- **Cross-promotion**: If you have guest facilitators, they promote to their audience. Negotiate this as part of the facilitator agreement.
- **Template/resource distribution**: Gated exercise templates from previous workshops drive email captures that feed into future workshop invites.

Track registrations by source channel in PostHog. After 4 workshops, you should know your cost per registration and cost per qualified lead by channel.

### 5. Evaluate against the threshold

After 3 months (4-8 workshops), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total registrations | >=160 | Sum of all workshop registrations in Attio |
| Average show rate | >=40% | Mean show rate across all workshops |
| Average exercise completion | >=60% | Mean exercise completion rate across workshops |
| Qualified leads | >=50 | Total qualified leads from workshop funnel |
| Cost per qualified lead | Trending down | Total spend / qualified leads, workshop over workshop |
| Repeat attendance rate | >=15% | Contacts who attended 2+ workshops / total unique attendees |

**PASS**: All core metrics met (registrations, show rate, qualified leads). Proceed to Durable. You have a scalable series with working automation, proven content flywheel, and optimized variables.

**FAIL**: Diagnose by metric:
- Low registrations: Clay prospecting not producing enough net-new contacts, or topic backlog exhausted. Refresh the topic backlog based on ICP research. Expand Clay searches to adjacent roles.
- Low show rate: Prep sequence not effective, or workshops scheduled at suboptimal times. Test different time slots. Add a "what to expect" video. Consider shorter sessions if the time commitment is deterring attendance.
- Low exercise completion: Exercises not calibrated to audience skill level. Use pre-workshop skill assessments to route attendees to the right difficulty level. Provide more scaffolding.
- Low qualified leads: Workshops attract curious but not high-intent attendees. Shift topics closer to product-relevant use cases (solution-aware, not problem-aware). Improve exercise-to-CTA bridge.

## Time Estimate

- Series automation setup (n8n workflows, Clay integration, Loops sequences): 14 hours
- A/B test planning and implementation: 4 hours
- Content repurposing system setup (Descript, templates, blog pipeline): 6 hours
- Per-workshop effort (curriculum prep, content delivery, analysis): 5 hours x 6 workshops = 30 hours
- Cross-event analysis and optimization: 8 hours
- Content derivative creation: 8 hours total (spread across workshops)
- Clay prospecting management: 5 hours total
- **Total: ~75 hours over 3 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Workshop recording + production | $29/mo Pro (4K, 15hr transcription) -- [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Email invites, prep, reminders, nurture | $49/mo (up to 5,000 contacts) -- [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, workshop lists, deal tracking | Free (3 users) or $29/user/mo Plus -- [attio.com](https://attio.com) |
| n8n | Series automation workflows | Self-hosted free or Cloud Pro EUR60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing per workshop | $185/mo Launch (2,500 credits) -- [clay.com/pricing](https://www.clay.com/pricing) |
| Descript | Recording clips + transcription | $24/mo Hobbyist -- [descript.com/pricing](https://www.descript.com/pricing) |
| Loom | Personalized follow-up clips | Free (25 videos, 5 min each) or $12.50/mo Business -- [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier -- [cal.com/pricing](https://cal.com/pricing) |
| LinkedIn Ads | Paid promotion (optional) | ~$200-500/workshop budget -- [linkedin.com/ad](https://www.linkedin.com/ad) |

**Estimated play-specific cost at Scalable: $300-560/mo** (Riverside + Loops + Clay + Descript + optional paid promotion)

## Drills Referenced

- `workshop-series-automation` -- automate recurring series operations, topic scheduling, prospect sourcing, attendee preparation, and cross-event analytics
- `ab-test-orchestrator` -- systematically test topic, difficulty, exercise format, timing, and promotion variables across workshops
- `content-repurposing` -- transform each workshop recording into derivative content (clips, tutorials, templates) that drives future registrations
