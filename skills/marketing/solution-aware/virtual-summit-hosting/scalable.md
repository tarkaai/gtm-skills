---
name: virtual-summit-hosting-scalable
description: >
  Virtual Summit Hosting — Scalable Automation. Automate the quarterly summit
  cadence with agent-managed speaker pipelines, cascading promotion workflows,
  and cross-summit A/B testing. Find the 10x multiplier without proportional effort.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Scalable Automation"
time: "100 hours over 6 months"
outcome: "≥1,500 total registrations and ≥100 qualified leads from 3-4 quarterly summits over 6 months with <30% increase in per-summit effort"
kpis: ["Registration count per summit", "Qualified leads per summit", "Per-summit operational hours", "A/B test experiment count", "Promotion channel ROI", "Speaker pipeline fill rate", "Cost per qualified lead"]
slug: "virtual-summit-hosting"
install: "npx gtm-skills add marketing/solution-aware/virtual-summit-hosting"
drills:
  - ab-test-orchestrator
---

# Virtual Summit Hosting — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Automate the quarterly summit cadence so the agent manages speaker pipelines, promotion workflows, and cross-summit analytics with minimal human intervention. Find the 10x multiplier: more registrations, more pipeline, and more summits without proportional effort. Pass threshold: ≥1,500 total registrations AND ≥100 qualified leads from 3-4 quarterly summits over 6 months, with per-summit operational hours growing <30% despite growing summit scale.

## Leading Indicators

- Speaker pipeline auto-generates ≥15 qualified speaker prospects per summit with <2 hours manual effort
- Promotion engine runs the full 8-week cadence via n8n with <1 hour manual intervention per summit
- Net-new prospect sourcing via Clay adds ≥500 theme-relevant registrants per summit
- A/B tests produce at least 1 statistically significant winner per summit (improving registration, show rate, or conversion)
- Per-summit operational hours decrease or stay flat while registration counts grow

## Instructions

### 1. Deploy the summit series automation

Run the the summit series automation workflow (see instructions below) drill. This builds the automated infrastructure that transforms manual summit operations into a repeatable quarterly cadence:

**Series calendar and theme planning:**
- Create the 12-month summit calendar in Attio with themes scored by ICP pain alignment, speaker availability, competitive differentiation, and timeliness.
- The agent proposes themes based on: ICP pain point research, topic performance data from previous summits, trending industry topics (from LinkedIn and conference CFP analysis), and product roadmap milestones.

**Human action required:** Approve the theme selection and final speaker lineup for each summit. The agent proposes; the human decides.

**Automated speaker pipeline:**
- 12 weeks before each summit, the agent auto-sources 20-30 speaker prospects via Clay matching the theme: recent LinkedIn content on the topic, conference speaking history, customer status, and audience reach.
- Auto-sends personalized speaker invitations from Attio.
- Tracks the speaker pipeline: invited → accepted → confirmed → prepped → delivered.
- If a speaker declines, auto-triggers the next prospect on the ranked list.
- Schedules prep calls via Cal.com and sends logistics emails automatically.

**Cascading promotion engine:**
- The full 8-week promotion cadence runs via n8n with no manual triggers:
  - T-8: Save-the-date email + LinkedIn announcement
  - T-6: Full invitation email + net-new prospect sourcing via Clay + speaker promotion activation
  - T-4: Non-opener resend + speaker-specific emails + sponsor/partner cross-promotion
  - T-2: Final push email + reminder sequence activation + production prep
  - T+1: Post-summit nurture trigger (hands off to `summit-attendee-nurture` drill)
- Each promotion step fires PostHog events for attribution tracking.

**Sponsor coordination automation:**
- For summits with sponsors, the agent manages the sponsor pipeline: proposal sends, logistics coordination, material collection, and post-event data delivery.

### 2. Test summit variations with A/B testing

Run the `ab-test-orchestrator` drill to systematically test variables across summits. Because summits are quarterly, each summit is an opportunity to test one variable against the baseline:

**Variables to test (one per summit):**

- **Theme framing**: Same core topic positioned differently. "The Future of [X]" vs "Why [X] Is Broken" vs "How Top Teams Do [X]." Measure registration rate difference.
- **Summit length**: Half-day (4 sessions) vs full-day (6-8 sessions). Measure show rate, multi-session rate, and qualified lead count.
- **Promotion timing**: Start promotion 8 weeks out vs 6 weeks out vs 4 weeks out. Measure total registrations and registration velocity.
- **Speaker lineup composition**: Customer-heavy (4 customers + 2 experts) vs expert-heavy (2 customers + 4 experts). Measure registration pull and post-summit conversion.
- **Registration page design**: Long-form (full agenda + all speaker bios) vs short-form (theme + 3 bullet points + date). Measure page-to-registration conversion.
- **Nurture approach**: Standard tier-based sequence vs personalized video response for all Tier 1-2 attendees. Measure reply rate and meeting booking rate.

For each test:
1. Form a hypothesis: "If we [change X], then [metric Y] will improve by [Z%], because [reasoning]."
2. Design the experiment using PostHog feature flags where possible (e.g., registration page A/B test).
3. For summit-level variables (theme, length, lineup), compare consecutive summits with all other variables held constant.
4. Evaluate using the `ab-test-orchestrator` drill's analysis framework.
5. Adopt winners as the new default. Document the result in Attio.

### 3. Scale registration through automated prospecting

For each summit, the agent auto-sources net-new registrants:

1. 6 weeks before the summit, use Clay to identify 500-1000 people matching the summit ICP + theme keywords.
2. Enrich with verified email via Clay enrichment waterfall.
3. Import to Loops and send a targeted summit invitation sequence (2 emails: initial invite + follow-up for non-openers).
4. Track which net-new segments convert to registrants and which convert to pipeline.
5. Feed conversion data back into Clay search criteria for the next summit: "People like the ones who converted from last summit."

Target: net-new prospect sourcing should contribute ≥30% of total registrations by the third automated summit.

### 4. Build the cross-summit intelligence layer

Using the data from the the summit series automation workflow (see instructions below) drill's cross-summit analytics, the agent generates insight reports after each summit:

- **Theme performance ranking**: Which themes generate the most registrations? The most pipeline?
- **Speaker ROI ranking**: Which speakers drove the most registrations through their promotion? Which sessions had the highest engagement?
- **Promotion channel ROI**: Cost per registrant and cost per qualified lead by channel (email list, net-new Clay prospects, LinkedIn, speaker-driven, sponsor-driven).
- **Optimal summit configuration**: Best day of week, best time slot, best session count, best format mix.

Store all insights in Attio. The agent uses this data to propose the next summit's configuration.

### 5. Evaluate against threshold

Measure across the 6-month period:

- Total registrations across all summits (target: ≥1,500)
- Total qualified leads across all summits (target: ≥100)
- Per-summit operational hours trend (target: <30% growth despite scaling)
- A/B test win count (target: ≥2 statistically significant winners in 6 months)
- Cost per qualified lead trend (target: flat or declining)

**PASS → Durable**: Hit both primary thresholds AND operational hours are scaling sub-linearly. The automated summit engine works and is ready for autonomous optimization.
**MARGINAL → Continue Scalable**: Close but operational efficiency not yet achieved. Run one more quarter to improve automation coverage.
**FAIL → Reassess**: If qualified leads per summit are declining despite growing registrations, the problem is conversion, not scale. Return to Baseline-level nurture optimization before scaling further.

## Time Estimate

- Summit series automation setup (one-time): 12 hours
- Per-summit agent management and oversight: 8 hours × 3-4 summits = 24-32 hours
- A/B test design and analysis: 4 hours per summit × 3-4 = 12-16 hours
- Human moderation per summit: 4 hours × 3-4 = 12-16 hours
- Cross-summit analysis and strategic planning: 4 hours per quarter × 2 = 8 hours
- Clay prospecting oversight and iteration: 2 hours per summit × 3-4 = 6-8 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Summit hosting and recording | $24/mo (Business) for longer sessions — https://riverside.fm/pricing |
| n8n | Automation orchestration (promotion, speaker pipeline, nurture triggers) | $20/mo (cloud Starter) or free self-hosted — https://n8n.io/pricing |
| Loops | Email sequences, broadcasts, and nurture | $49/mo (Growth) — https://loops.so/pricing |
| Attio | CRM for full pipeline and series tracking | Free up to 3 seats — https://attio.com/pricing |
| PostHog | Full funnel analytics, experiments, feature flags | Free up to 1M events; $0 for feature flags — https://posthog.com/pricing |
| Clay | Speaker sourcing and net-new prospect enrichment | $149/mo (Explorer) — https://clay.com/pricing |
| Anthropic Claude API | Theme proposal generation, insight reports | ~$10-20/mo — https://www.anthropic.com/pricing |

**Estimated play-specific cost: $252-342/mo** (Riverside + n8n + Loops + Clay + Claude API)

## Drills Referenced

- the summit series automation workflow (see instructions below) — automates the full quarterly summit cadence: theme planning, speaker pipeline, cascading promotion, sponsor coordination, and cross-summit analytics
- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on summit variables: theme framing, length, promotion timing, speaker lineup, registration page, and nurture approach
