---
name: award-submissions-program-baseline
description: >
  Industry Award Submissions — Baseline Run. Scale to 10+ submissions per quarter with a
  systematic pipeline, add paid awards with high ICP visibility, track award-to-pipeline
  attribution, and validate repeatable wins over 10 weeks.
stage: "Marketing > SolutionAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Baseline Run"
time: "25 hours over 10 weeks"
outcome: ">=10 submissions, >=3 wins or finalist placements, and >=10 qualified leads influenced by award credibility within 10 weeks"
kpis: ["Submissions per quarter", "Win rate", "Award categories won", "Social proof impressions", "Award-influenced leads"]
slug: "award-submissions-program"
install: "npx gtm-skills add marketing/solution-aware/award-submissions-program"
drills:
  - award-submission-pipeline
  - media-pitch-outreach
  - threshold-engine
---

# Industry Award Submissions — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

The first systematic award submissions program. A rolling pipeline of awards is maintained, submissions are prepared using proven content blocks, and wins are amplified through PR outreach. The goal is proving that awards reliably produce social proof and pipeline influence at repeatable volume.

**Pass threshold:** >=10 submissions, >=3 wins or finalist placements, and >=10 qualified leads influenced by award credibility within 10 weeks.

## Leading Indicators

- Award pipeline has 15+ awards tracked with deadlines and status
- Win rate exceeds 25% (at least 3 wins from 10 submissions)
- Award wins are displayed on at least 3 surfaces (website, social, email signature, sales deck)
- Sales team reports at least 2 prospects mentioning award credibility during evaluation
- At least 1 award win generates a media mention or backlink

## Instructions

### 1. Build the Full Award Pipeline

Run the `award-submission-pipeline` drill at Baseline scale (20-30 awards tracked):

1. Expand beyond Smoke: include paid awards (entry fees $100-500) with high ICP visibility
2. Add categories you did not target at Smoke: workplace awards, regional awards, founder awards
3. Build the complete Clay table with scoring for all awards
4. Select 10-15 for submission this quarter based on score and deadline alignment
5. Create a submission calendar in Attio: map all deadlines over the next 10 weeks

### 2. Prepare High-Quality Submissions

Using the content blocks from Smoke (updated with new data):

1. For each submission, read the specific judging criteria and past winner profiles
2. Use Claude API to research past winners (search "{award name} winners {previous year}"). Identify patterns in what judges reward.
3. Customize each submission to match the judging emphasis:
   - **Growth awards:** Lead with revenue metrics, customer growth rate, market expansion
   - **Innovation awards:** Lead with technical differentiation, product uniqueness, patent/IP
   - **Customer impact awards:** Lead with customer stories, specific outcome metrics, testimonials
   - **People/culture awards:** Lead with team growth, retention, culture initiatives, diversity stats
4. For awards requiring references: maintain a roster of 5 willing customers, pre-briefed on what to say
5. **Human action required:** Founder reviews each submission before sending. Verify all metrics are current and approved for external sharing.

### 3. Amplify Wins with PR Outreach

When wins are announced, use the `media-pitch-outreach` drill to amplify:

1. Draft a press announcement for each significant win
2. Pitch to 5-10 media targets who cover your space: "We were named [award] by [organizer]. Here is what it means for [industry trend]."
3. Create social content for LinkedIn and Twitter: announcement post, thank you to the organizer, behind-the-scenes of the team's reaction
4. Email your customer base about the win (via Loops or newsletter)
5. Update all social proof surfaces: website badges, email signatures, sales deck

### 4. Track Award-to-Pipeline Attribution

Build basic attribution tracking:

1. Add an "Award Influence" tag in Attio for deals where the prospect mentions awards
2. In the sales process, add a discovery question: "Have you seen any of the awards or recognitions we have received?"
3. Track in PostHog: `award_won` event (properties: award name, category, audience size), `deal_award_influenced` event (properties: deal name, award referenced, deal value)
4. When a prospect visits your pricing page with award badges, PostHog tracks the `award_badge_viewed` event
5. Weekly: review Attio for new award-influenced deals

### 5. Optimize Submission Quality

After each batch of results comes in:

1. Analyze win rate by award category: which categories have the highest success rate?
2. Review feedback from awards that provide it (some share judges' scores or comments)
3. Compare winning submissions to non-winning ones: what did the winners emphasize differently?
4. Update content blocks with new data and improved framing
5. For awards you were shortlisted but did not win: identify the gap and re-submit next cycle with stronger evidence

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill after 10 weeks:

1. Compile:
   - Total submissions (threshold: >=10)
   - Wins or finalist placements (threshold: >=3)
   - Award-influenced leads (threshold: >=10 qualified leads where award credibility was a factor)
2. Calculate: win rate, cost per win (entry fees / wins), award-influenced pipeline value
3. Analyze: which award categories produce the most wins? Which produce the most pipeline influence?

**If PASS:** Awards are a repeatable credibility engine. Proceed to Scalable with automated pipeline management and PR amplification.

**If FAIL:** Diagnose:
- Low win rate: submissions are not competitive. Study past winners more carefully. Invest in stronger customer references.
- Wins but no pipeline influence: wrong awards for your ICP. Shift to awards that appear in publications your buyers read.
- Not enough submissions: pipeline management is the bottleneck. Dedicate recurring time to submission prep.

## Time Estimate

- 4 hours: Award pipeline expansion and scoring (20-30 awards)
- 8 hours: 10-15 submission preparation and customization
- 4 hours: PR amplification for wins (social posts, media outreach, website updates)
- 4 hours: Attribution tracking setup and sales team training
- 3 hours: Submission quality analysis and content block updates
- 2 hours: Threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — submission tracking and pipeline attribution | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — award research and past winner analysis | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Analytics — award event tracking and attribution | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Email — award announcement emails to customers | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Claude API | Submission drafting and past winner research | ~$15-25/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Entry fees ~$200-500/quarter for paid awards. Loops ~$49/mo for announcements. Other tools are standard stack.

## Drills Referenced

- `award-submission-pipeline` — systematic discovery, scoring, content preparation, and submission of industry awards
- `media-pitch-outreach` — amplify award wins through targeted media outreach for press coverage
- `threshold-engine` — evaluate Baseline results against the pass threshold and recommend next action
