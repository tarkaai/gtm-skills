---
name: case-study-recruitment-scalable
description: >
  Customer Story Pipeline — Scalable. Multiply case study output by repurposing each
  story into 8-12 derivative assets, routing them to matching deals automatically, and
  segmenting recruitment by industry vertical. Target 6+ case studies per month covering
  all major ICPs.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Scalable"
time: "60 hours over 2 months"
outcome: ">=6 case studies/month with automated distribution to matching deals"
kpis: ["Recruitment acceptance rate", "Case study completion rate", "Pipeline velocity", "Content coverage by ICP", "Deal influence rate", "Asset engagement rate"]
slug: "case-study-recruitment"
install: "npx gtm-skills add product/referrals/case-study-recruitment"
drills:
  - case-study-candidate-pipeline
  - dashboard-builder
---

# Customer Story Pipeline — Scalable

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Multiply the pipeline's output and influence. Each case study produces 8-12 derivative assets automatically distributed to matching prospects and deals. Recruitment is segmented by industry vertical to ensure coverage across all major ICPs. The pipeline produces 6+ case studies per month without proportional effort increase.

## Leading Indicators

- Candidate pipeline segmented by at least 3 industry verticals with active candidates in each
- Derivative asset production automated: 8+ assets created per completed case study
- Case study assets routed to matching deals within 24 hours of publish
- At least 1 case study available for each of the top 5 industry verticals in the deal pipeline
- Deal owners using case study assets in at least 30% of active proposals

## Instructions

### 1. Segment the candidate pipeline by vertical

Enhance the `case-study-candidate-pipeline` drill with vertical segmentation:

1. Define 3-5 priority industry verticals based on your deal pipeline (query Attio for the industries with the most active deals)
2. Add `target_vertical` as a scoring dimension boost: candidates in underrepresented verticals get a +15 score bonus to prioritize coverage gaps
3. Create separate Attio lists per vertical: "Case Study Candidates — [Vertical]"
4. Customize the outreach sequence per vertical: reference industry-specific outcomes and link to existing case studies in their industry (if available)
5. Set per-vertical targets: at least 1 new case study per vertical per quarter

Configure the scoring pipeline to report the coverage gap: which verticals have zero or one case study but significant deal pipeline volume? Feed these gaps back as priority weights.

### 2. Deploy content scaling automation

Run the the case study content scaling workflow (see instructions below) drill to build the derivative asset engine:

1. Configure the n8n workflow triggered by `case_study_completed` event
2. Automate Tier 1 asset production (pull quotes, metric highlights, email snippets, in-app banners)
3. Set up Tier 2 asset drafting (one-page PDF, blog post, LinkedIn post, newsletter feature) with human review queue
4. Build the deal-matching distribution engine: when a case study publishes, find all active deals in Attio in the same industry and attach the email snippet + one-page PDF
5. Configure in-app social proof: Intercom banners targeted to users in the matching industry cohort during their first 90 days
6. Build the weekly deal-to-case-study matching workflow: every new deal gets the best-matching case study assets attached automatically

Validate: after the first 2 case studies flow through the scaling pipeline, audit the derivative assets. Are the pull quotes compelling? Is the email snippet concise enough for sales to use without editing? Is the LinkedIn post in the right voice? Adjust the generation prompts if needed.

### 3. Monitor pipeline health

Run the `dashboard-builder` drill:

1. Configure the 7 health metrics with Scalable-level targets (pipeline velocity target: 6/month)
2. Deploy the daily health check workflow
3. Configure diagnostic triggers for each metric
4. Deploy automated interventions: stale subject line rotation, no-show prevention reminders, draft approval nudges, pipeline stall alerts
5. Build the weekly health report with content gap analysis

The health monitor surfaces problems before they compound. Key signals to watch at Scalable:
- Candidate pool depletion: as you publish more case studies, the eligible pool shrinks. Monitor pool replenishment rate (new customers reaching score 70) vs. consumption rate.
- Vertical concentration: if one vertical produces all the case studies while others stall, the outreach for underperforming verticals needs different messaging or incentives.
- Asset fatigue: if the same case studies are being routed to deals repeatedly, the library needs refresh. Track unique case studies used per quarter.

### 4. Scale interview capacity

At 6+ interviews per month, the bottleneck shifts from candidate supply to production capacity:

1. Create an interview playbook: standardized question framework with vertical-specific modules, so any team member can conduct an interview (not just the founder)
2. Train 2-3 team members on the interview process using the recorded interviews from Smoke and Baseline as examples
3. Build a scheduling round-robin in Cal.com: interviews auto-distribute across interviewers based on availability
4. Standardize post-interview handoff: transcription auto-uploaded, brief auto-generated, writing assignment auto-created in Attio

**Human action required:** Train additional interviewers. Conduct the first 2-3 interviews as a pair (experienced + new interviewer) before the new interviewer goes solo.

### 5. Build the content library dashboard

Extend the PostHog dashboard with Scalable metrics:

- **Library coverage**: case studies by vertical, by company size, by use case. Heatmap of gaps.
- **Asset performance**: views, clicks, and deal influence by asset type. Which derivative format drives the most deal engagement?
- **Deal influence**: case studies attached to deals -> deals progressed -> deals won. Attribution from case study touchpoint to close.
- **Production efficiency**: average hours from interview to all assets published. Trend over time (should decrease as the process matures).
- **Content freshness**: age distribution of the case study library. Flag any case study older than 12 months for potential refresh.

## Time Estimate

- 12 hours: vertical segmentation, outreach customization, pipeline enhancement
- 10 hours: content scaling automation setup (asset generation, distribution engine, deal matching)
- 8 hours: health monitor setup (metrics, diagnostics, interventions, reporting)
- 4 hours: interview playbook creation and interviewer training
- 6 hours/month: conducting 6+ interviews
- 8 hours/month: case study writing and asset review
- 4 hours/month: pipeline health review and optimization
- 8 hours: dashboard expansion and library tracking

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring, funnels, dashboards, experiments | Free tier (1M events/mo) |
| Attio | Pipeline CRM, deal matching, candidate tracking | Free tier available |
| n8n | Scoring, asset production, distribution, health monitoring | Self-hosted free; Cloud from $24/mo |
| Loops | Outreach sequences, newsletter distribution | From $49/mo (1,000 contacts) |
| Intercom | In-app recruitment nudges, social proof banners | From $29/seat/mo; ~$85/seat for Advanced |
| Fireflies | Interview transcription | Pro $10/user/mo annual (multiple interviewers) |
| Cal.com | Round-robin interview scheduling | Teams $15/user/mo |
| Ghost | Case study and blog publishing | From $9/mo (starter) |

**Play-specific cost:** Loops ~$49/mo + Intercom ~$85/mo + Fireflies ~$30/mo (3 users) + Cal.com ~$45/mo (3 users) = ~$209/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `case-study-candidate-pipeline` — segmented scoring and vertical-specific outreach
- the case study content scaling workflow (see instructions below) — derivative asset production and automated deal-matched distribution
- `dashboard-builder` — daily health checks, diagnostics, interventions, and weekly reporting
