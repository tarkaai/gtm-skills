---
name: joint-content-campaigns-scalable
description: >
  Joint Content Campaigns -- Scalable Automation. Automate partner pipeline management,
  content production scheduling, lead attribution, and partner nurture sequences to
  sustain 10+ co-created assets with 10+ partners over 6 months without proportional
  effort increase.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Content, Email"
level: "Scalable Automation"
time: "75 hours over 6 months"
outcome: ">=10 co-created assets published and >=80 qualified leads over 6 months"
kpis: ["Assets published per month", "Active partner count", "Qualified leads per month", "Cost per qualified lead", "Partner retention rate", "Production cycle time (days from agreement to publication)"]
slug: "joint-content-campaigns"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/joint-content-campaigns"
drills:
  - partner-pipeline-automation
  - dashboard-builder
  - threshold-engine
---
# Joint Content Campaigns -- Scalable Automation

> **Stage:** Marketing -> ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Content, Email

## Outcomes
Ten or more co-created content assets published across 10+ partner relationships. At least 80 qualified leads from joint content over 6 months. Production cycle time decreases as automation handles scheduling, attribution, and partner nurture. The system runs with decreasing manual effort per asset.

## Leading Indicators
- Partner pipeline maintains 15+ prospects at any time (replacing partners that churn)
- Production cycle time decreases from Baseline levels (target: <14 days from agreement to publication)
- Automation handles >80% of lead attribution and partner performance reporting
- Repeat collaborations: at least 3 partners produce 2+ assets each
- Monthly lead volume grows or holds steady across months 3-6

## Instructions

### 1. Automate the partner pipeline
Run the `partner-pipeline-automation` drill to build n8n workflows that manage the partner portfolio at scale:

**Partner outreach automation:**
- Trigger: new partner added to "Content Partners" list in Attio with status "Prospect"
- Auto-send personalized outreach via email referencing account overlap data and your existing co-created assets as proof
- If no reply in 5 days, send one follow-up
- If positive reply, create an Attio deal in the "Content Partnerships" pipeline and update status to "In Conversation"

**Production scheduling automation:**
- Trigger: weekly cron (Monday 9am)
- Query Attio for active partners where "Next Asset Due" is within 14 days
- Check asset production status: topic selected, outline approved, sections in progress, sections received, assembly, published
- If any asset is behind schedule, send alerts to Slack with the specific blocker
- If partner sections are >3 days late, auto-send a nudge email to the partner contact

**Lead attribution automation:**
- Trigger: PostHog webhook fires when `content_download` event occurs with `utm_source` matching a partner slug
- Look up the partner in Attio, increment their "Total Leads" counter
- Create a lead record linked to the partner and asset
- If this is the partner's first lead from a new asset, send a performance update to the partner contact

**Partner nurture sequence:**
- Day 0 after asset publication: send the partner a performance summary (downloads, lead count)
- Day 7: share full first-week performance report
- Day 14: propose the next collaboration with a suggested topic based on what converted best
- Day 30: monthly partnership summary (total leads, pipeline value generated for both sides)

### 2. Scale content production
Run the the joint content production workflow (see instructions below) drill continuously, targeting 2 new assets per month. Use templates and processes proven at Baseline:

**Standardize the production process:**
- Create an n8n workflow that auto-generates the content outline from Crossbeam overlap data + Clay ICP research when a new partner deal reaches "Topic Selection" stage
- Template the section assignment structure (your 3 sections + partner 3 sections + joint intro/conclusion)
- Use the best-performing format from Baseline as the default; experiment with alternatives quarterly

**Scale the content variety:**
- Ebooks/guides for broad topics (highest download volume)
- Benchmark reports for data-heavy topics (highest conversion rate, typically)
- Checklists/scorecards for actionable topics (fastest to produce, good for new partners)
- Webinar recordings converted to written guides (leverage live events with partners)

### 3. Build the performance dashboard
Run the `dashboard-builder` drill to create a PostHog dashboard for the joint content program:
- Total downloads and leads this month vs. last month
- Per-partner performance ranking (leads, conversion rate, production velocity)
- Per-format performance (which content types convert best)
- Per-topic performance (which pain points generate the most leads)
- Partner pipeline health: prospects, in-conversation, active, churned
- Production pipeline: assets in progress by stage

Set guardrails: if conversion rate drops >20% below Baseline average for 2 consecutive weeks, trigger an investigation. If a specific format consistently underperforms, deprioritize it.

### 4. Optimize partner selection
Using data from 6+ months of partnerships:
- Identify the partner profile that converts best (company size, audience overlap %, content quality score)
- Prioritize outreach to partners matching the high-performing profile
- Retire underperforming partnerships (partners whose assets generate <5 leads after 4 weeks)
- Double down on top partners: propose quarterly collaboration schedules

### 5. Evaluate against threshold
Run the `threshold-engine` drill to measure against: >=10 co-created assets published and >=80 qualified leads over 6 months.

If PASS: proceed to Durable. The automation sustains output and quality at scale.
If FAIL: analyze:
- If 10+ assets but <80 leads -> content quality or distribution is the issue. Focus on the top-converting topics and formats.
- If <10 assets -> production bottleneck. Reduce asset scope (shorter pieces) or add a content coordinator role.
- If leads are high but quality is low -> tighten qualification criteria and partner selection.

## Time Estimate
- 15 hours: partner pipeline automation setup (n8n workflows, Attio configuration)
- 5 hours: dashboard and alert setup
- 40 hours: content co-production (20 assets x 2 hours each, efficiency gains from templates)
- 10 hours: partner relationship management and optimization
- 5 hours: threshold evaluation and strategic review

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for partner pipeline and lead attribution | Plus plan ~$34/user/mo; https://attio.com/pricing |
| n8n | Automation for partner workflows, scheduling, attribution | Self-hosted free, Cloud from EUR20/mo; https://n8n.io/pricing |
| PostHog | Analytics dashboard and event tracking | Free up to 1M events/mo; https://posthog.com/pricing |
| Clay | Partner research and enrichment | From $149/mo; https://clay.com/pricing |
| Crossbeam | Account overlap mapping at scale | Free tier; paid from ~$0-200/mo; https://www.crossbeam.com/pricing |
| Anthropic Claude | Content drafting at volume | Pay-per-use ~$20-60/mo at this scale; https://www.anthropic.com/pricing |
| Ghost | Asset hosting | Free self-hosted; https://ghost.org/pricing |
| Loops | Email distribution | From $49/mo for larger lists; https://loops.so/pricing |

## Drills Referenced
- `partner-pipeline-automation` -- n8n workflows for partner outreach, scheduling, attribution, and nurture
- the joint content production workflow (see instructions below) -- per-asset co-creation workflow, now templatized
- `dashboard-builder` -- PostHog dashboard for program-level visibility
- `threshold-engine` -- evaluate pass/fail against the 80-lead threshold
