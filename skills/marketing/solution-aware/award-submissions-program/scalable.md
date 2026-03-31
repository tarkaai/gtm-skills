---
name: award-submissions-program-scalable
description: >
  Industry Award Submissions — Scalable. Automate award discovery, deadline tracking, and
  submission preparation via n8n. Scale to 30+ submissions per year with systematic PR
  amplification and full award-to-pipeline attribution.
stage: "Marketing > SolutionAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Scalable"
time: "70 hours over 6 months"
outcome: ">=30 submissions, >=10 wins or finalist placements, and >=35 qualified leads from award visibility over 6 months"
kpis: ["Submissions per quarter", "Win rate by category", "PR placements from awards", "Award-influenced pipeline value", "Social proof coverage score", "Cost per award-attributed lead"]
slug: "award-submissions-program"
install: "npx gtm-skills add marketing/solution-aware/award-submissions-program"
drills:
  - award-submission-pipeline
  - media-pitch-outreach
  - award-performance-monitor
---

# Industry Award Submissions — Scalable

> **Stage:** Marketing > SolutionAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

Scale the award program to a continuously operating engine: awards are discovered automatically, deadlines are tracked in a rolling calendar, submissions are prepared using optimized content blocks, and wins are amplified through automated PR workflows. Award credibility becomes a systematic sales enablement asset.

**Pass threshold:** >=30 submissions, >=10 wins or finalist placements, and >=35 qualified leads from award visibility over 6 months.

## Leading Indicators

- Award pipeline has 40+ awards tracked with rolling deadline management
- Win rate exceeds 30% (improving from Baseline through better targeting and submission quality)
- Each award win generates at least 1 media mention or social amplification within 48 hours
- Award badges are displayed on 5+ surfaces and consistently referenced by sales team
- Award-influenced deals represent 5%+ of total pipeline
- Content blocks are refreshed quarterly with new metrics

## Instructions

### 1. Automate Award Discovery

Build an n8n workflow for continuous award discovery:

**Trigger:** Monthly cron (first Monday)

**Workflow steps:**
1. Run Claygent queries via Clay API for new awards: search for "{industry} awards" + "{category} best" + competitor award mentions
2. For each new award found, check if it already exists in the Clay table (deduplicate)
3. Auto-populate the award tracking table with: name, organizer, deadline, entry fee, estimated audience
4. Use Claude API to score ICP overlap based on the organizer's audience description
5. Route new high-score awards to Slack #awards channel for review
6. Update the Attio submission calendar with new deadlines

### 2. Scale Submission Volume

Run the `award-submission-pipeline` drill at Scalable volume (30+ submissions over 6 months):

1. Maintain a rolling pipeline of 40+ awards across all categories
2. Batch submission preparation: each month, identify all awards with deadlines in the next 30-60 days
3. Use Claude API to generate submission drafts in batch, referencing the specific judging criteria for each award
4. **Human action required:** Founder reviews submissions in weekly batches (target: 30-45 min/week). Focus review time on Priority 1 awards.
5. For Priority 2-3 awards: template-based submissions with metric merge fields require minimal customization

### 3. Build the Award Amplification Engine

Automate post-win amplification via n8n:

**Trigger:** When an award submission status changes to "winner" or "finalist" in Attio

**Workflow steps:**
1. Generate social media posts (LinkedIn, Twitter) using Claude API: announcement, thank you, behind-the-scenes angle
2. Generate a brief press announcement paragraph
3. Route all content to Slack for human approval
4. On approval:
   - Schedule social posts via Buffer/Typefully
   - Send to media targets using the `media-pitch-outreach` drill (5-10 relevant journalists)
   - Update website press page (via CMS API or manual task)
   - Queue customer announcement email (via Loops)
   - Add badge to email signatures (manual task, logged)
5. Track all amplification activity in PostHog: `award_social_post`, `award_press_mention`

### 4. Deploy Award Performance Monitoring

Run the `award-performance-monitor` drill:

1. Build the PostHog award dashboard (4 panels: submission pipeline, win tracking, social proof distribution, pipeline attribution)
2. Implement the award event taxonomy in PostHog
3. Configure anomaly detection: win rate decline, submission drought, influence decline
4. Deploy quarterly automated reports via n8n

### 5. Integrate Awards into Sales Process

Systematize how awards are used in the sales cycle:

1. Create an "Awards & Recognition" one-pager (PDF) for the sales team with all current wins, organized by category
2. Add award badges to the sales deck cover slide and trust/proof slide
3. Build an Attio automation: when a deal reaches "Evaluation" stage, auto-include the awards one-pager in the deal materials
4. Track: which awards do prospects mention? Which badge placements (website, email, sales deck) do they notice?
5. Monthly: share with the sales team which awards are resonating most with prospects

### 6. Monthly Optimization

Monthly review cycle:

1. Pull the quarterly report from the `award-performance-monitor` drill
2. Analyze:
   - Which award categories have the highest win rate?
   - Which wins generate the most PR amplification?
   - Which wins influence the most deals?
   - Are paid awards (entry fee > $0) producing more value per dollar than free awards?
   - Which submission content blocks need refreshing with new data?
3. Adjust:
   - Shift submission effort toward highest-win-rate categories
   - Drop categories with zero wins after 3+ submissions
   - Update content blocks with fresh metrics quarterly
   - Expand to new award types if current pipeline is saturated

## Time Estimate

- 3 hours: Award discovery automation setup (n8n + Clay)
- 6 hours/quarter: Batch submission preparation and review (x2 = 12 hours)
- 4 hours: Amplification engine setup (n8n workflow)
- 4 hours: Award monitoring setup (dashboard, events, reports)
- 3 hours: Sales integration (one-pager, deck updates, Attio automation)
- 20 hours: Ongoing submission writing and submission over 6 months
- 12 hours: Win amplification and PR outreach over 6 months
- 8 hours: Monthly optimization reviews (1.5 hours/month x 6 months)
- 3 hours: Quarterly content block refresh

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — submission pipeline, deal attribution, sales integration | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — award discovery, past winner research | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Automation — discovery, amplification, monitoring | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — award dashboards and attribution | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Email — customer announcement emails | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Instantly | Media outreach for win amplification | $30/mo (Growth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Claude API | Submission drafting, amplification content, past winner analysis | ~$30-50/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Entry fees ~$500-1,500/quarter. Loops ~$49/mo + Instantly ~$30/mo = ~$79/mo play-specific tools. n8n, PostHog, Attio, Clay are standard stack.

## Drills Referenced

- `award-submission-pipeline` — automated award discovery, batch submission preparation, and rolling pipeline management
- `media-pitch-outreach` — amplify award wins through targeted media outreach to journalists and newsletter editors
- `award-performance-monitor` — continuous monitoring of submission pipeline, win rates, social proof impact, and award-to-pipeline attribution
