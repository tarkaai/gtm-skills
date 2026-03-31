---
name: conference-booth-sponsorship-scalable
description: >
  Conference Booth & Sponsorship — Scalable Automation. Build a quarterly
  conference program with agent-managed sponsorship selection, automated
  pre-event targeting, A/B tested follow-up sequences, and cross-conference
  optimization. Multiply meetings and pipeline without proportional effort
  per event.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Scalable Automation"
time: "60 hours over 6 months"
outcome: ">=300 badge scans, >=60 qualified leads, >=20 meetings booked across 4-6 conferences over 6 months. Cost per meeting trending down quarter over quarter."
kpis: ["Qualified leads per conference", "Meetings booked per conference", "Cost per meeting (trend)", "Follow-up conversion rate", "Pre-event outreach response rate", "Pipeline generated per conference"]
slug: "conference-booth-sponsorship"
install: "npx gtm-skills add marketing/solution-aware/conference-booth-sponsorship"
drills:
  - conference-sponsorship-pipeline
  - booth-lead-capture
  - booth-follow-up-nurture
  - ab-test-orchestrator
---

# Conference Booth & Sponsorship — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Scale from ad-hoc conference sponsorships to a structured quarterly program with 4-6 conferences over 6 months
- Automate the repeatable parts: conference evaluation, pre-event targeting, follow-up nurture, ROI reporting
- Systematically A/B test booth tactics, follow-up sequences, and conference selection criteria to find the winning formula
- Reduce cost per meeting quarter over quarter through data-driven conference selection and follow-up optimization
- Build a reusable conference operations playbook that any team member can execute without starting from scratch

## Leading Indicators

- Conference scoring model accurately predicts which events will produce the best ROI (top-scored conferences outperform bottom-scored by 2x+)
- Pre-event outreach response rate exceeds 25% (targeting is precise)
- Automated Tier 2 follow-up sequence generates at least 1 meeting per conference without manual intervention
- Cost per meeting decreases by at least 15% from the first 2 conferences to the last 2
- Pipeline generated per dollar of sponsorship spend increases quarter over quarter

## Instructions

### 1. Build the quarterly conference program

Run the `conference-sponsorship-pipeline` drill to evaluate 10-15 conferences for the next 6 months. Apply Baseline learnings to refine the scoring model:

- Increase weight on factors that predicted Baseline success (e.g., if ICP density was the strongest predictor, weight it 45% instead of 35%)
- Decrease weight on factors that did not correlate with results
- Add new scoring criteria based on Baseline data: conferences similar to your highest-ROI Baseline event should score higher

Select 4-6 conferences (roughly 1 per month). Build the annual conference calendar in Attio with: conference name, date, city, tier, cost, expected qualified leads, and expected meetings (based on Baseline conversion rates).

Plan budget allocation across conferences. Invest more in conferences that score highest. Consider upgrading sponsorship tier for top-scoring events (e.g., if a speaking slot is available at Gold tier and your Baseline data shows that speaking at a conference doubles your qualified lead rate, the upgrade is worth it).

### 2. Automate pre-event targeting at scale

For each conference, automate the pre-event sequence using the `conference-sponsorship-pipeline` drill's pre-event steps, now running as n8n workflows:

- **T-30 days**: n8n workflow triggers Clay to search for conference attendees, speakers, and sponsor employees. Enrichment waterfall runs automatically. Scored contacts land in Attio with a "Pre-Event Target" tag.
- **T-21 days**: n8n triggers a Loops email sequence to top-scored targets: pre-event outreach offering booth meetings. Track open and reply rates in PostHog.
- **T-14 days**: For targets who opened but did not reply, trigger a second touch via Loops or LinkedIn (if LinkedIn automation is set up).
- **T-7 days**: Send a final reminder to confirmed booth meetings. Send a new outreach to any recently published attendee lists.
- **T-1 day**: Generate booth staff briefing: target list with photos, meeting schedule, key talking points per visitor.

Track pre-event outreach performance by conference in PostHog: `preevent_outreach_sent`, `preevent_outreach_opened`, `preevent_outreach_replied`, `preevent_meeting_prebooked`.

### 3. Systematically test booth and follow-up variables

Run the `ab-test-orchestrator` drill to test one variable at a time across consecutive conferences:

**Variables to test (in priority order):**

1. **Follow-up timing**: Does sending Tier 1 follow-up within 4 hours vs 12 hours affect reply rate? Split Tier 1 leads from one conference into two groups.
2. **Follow-up format**: Does a Loom video follow-up outperform text-only email for Tier 2? Test across 2 conferences (Loom for conference A, text-only for conference B).
3. **Demo track**: Which demo approach converts best? Test: problem-focused demo vs feature-focused demo vs customer-story demo. One track per conference.
4. **Booth engagement style**: Does an interactive demo station (visitors try the product themselves) outperform guided demos? Test at consecutive conferences.
5. **Pre-event outreach copy**: A/B test subject lines and messaging within the same conference's outreach send.
6. **Sponsorship tier**: If budget allows, try upgrading to a tier with a speaking slot at one conference. Compare qualified lead rate vs booth-only conferences.

For each test, define the hypothesis, success metric, and minimum sample size before running. After 4 conferences, compile a "Conference Booth Best Practices" document: winning follow-up timing, format, demo track, and engagement style.

### 4. Optimize follow-up nurture sequences

Upgrade the `booth-follow-up-nurture` drill sequences based on Baseline data:

- **Tier 1**: If Loom videos tested well, include them by default. Personalize the video script with conference-specific content. Reduce time-to-first-email to the winning timing from your test.
- **Tier 2**: Extend or shorten the sequence based on which step produces the most replies. If Email 2 (Day 4) outperforms Email 3 (Day 8), drop Email 3 and redirect effort to a different channel (LinkedIn connection request on Day 6).
- **Tier 3**: If single-email approach yields <5% engagement, test adding them to a content nurture sequence instead. If they engage with content, promote them to Tier 2 treatment.

Build a post-conference automation in n8n that:
1. Imports badge scan data to Attio (automated via webhook or scheduled CSV import)
2. Triggers the correct follow-up sequence per tier
3. Monitors for replies and auto-creates deals
4. Generates the 14-day ROI report automatically

### 5. Evaluate against the threshold

After 6 months (4-6 conferences), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total badge scans | >=300 | Sum across all conferences in Attio |
| Qualified leads (Tier 1+2) | >=60 | Sum of Tier 1+2 contacts across conferences |
| Meetings booked (total) | >=20 | Cal.com bookings attributed to conference program |
| Cost per meeting trend | Declining | Compare Q1 vs Q2 cost per meeting |
| Pipeline generated | Tracking | Total deal value from conference-sourced leads |

**PASS**: Core metrics met and cost per meeting trending down. Proceed to Durable. You have a scaled, data-driven conference program.

**FAIL**: Diagnose by metric:
- Low badge scans: Conference selection is off. Refresh the scoring model with updated ICP data. Try different conference types or regions.
- Low qualified leads: Booth execution needs work. Review demo track, conversation framework, and booth positioning. Consider hiring professional booth staff.
- Low meetings: Follow-up is the bottleneck. Accelerate testing — try radically different approaches (phone call follow-up, same-day meeting requests, conference dinner invitations).
- Cost not declining: You are not learning from conference to conference. Review cross-conference analysis more carefully. Drop the worst-performing conference type and double down on the best.

## Time Estimate

- Quarterly conference program planning and scoring: 6 hours x 2 quarters = 12 hours
- Pre-event automation setup (one-time, then runs for each conference): 6 hours
- Per-conference pre-event targeting review: 1 hour x 6 = 6 hours
- Per-conference booth execution + enrichment: 4 hours x 6 = 24 hours
- A/B test planning and implementation: 4 hours
- Follow-up optimization: 4 hours
- Cross-conference analysis and reporting: 4 hours
- **Total: ~60 hours over 6 months** (split: ~35 hours agent, ~25 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Conference scoring + attendee enrichment | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Attio | CRM, conference pipeline, deal tracking | $29/user/mo Plus — [attio.com](https://attio.com) |
| PostHog | Event tracking, funnels, experiments | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Automated follow-up nurture | $49/mo (5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Pre-event automation, follow-up triggers, reporting | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Personalized follow-up videos | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |

**Estimated play-specific cost at Scalable: $300-500/mo + sponsorship costs** (sponsorship typically $2,000-10,000 per conference at this level)

## Drills Referenced

- `conference-sponsorship-pipeline` — quarterly conference program planning, scoring, and pre-event automation
- `booth-lead-capture` — standardized booth execution with real-time lead qualification
- `booth-follow-up-nurture` — automated tier-segmented follow-up sequences with optimization
- `ab-test-orchestrator` — systematic testing of booth tactics, follow-up format, timing, and demo approach
