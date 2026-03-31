---
name: award-submissions-program-smoke
description: >
  Industry Award Submissions — Smoke Test. Research 10-15 relevant industry awards, prepare
  and submit to 3-5 free or low-cost awards, and validate that the program produces at least
  1 win or finalist placement within 4 weeks.
stage: "Marketing > SolutionAware"
motion: "PREarnedMentions"
channels: "Other, Social"
level: "Smoke Test"
time: "10 hours over 4 weeks"
outcome: ">=3 submissions completed, >=1 win or finalist placement, and social proof assets created for at least 1 award within 4 weeks"
kpis: ["Awards researched", "Submissions completed", "Win/finalist placements", "Submission quality score", "Time per submission"]
slug: "award-submissions-program"
install: "npx gtm-skills add marketing/solution-aware/award-submissions-program"
drills:
  - award-submission-pipeline
  - threshold-engine
---

# Industry Award Submissions — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** PREarnedMentions | **Channels:** Other, Social

## Outcomes

Prove that the company can win industry awards and that the wins produce usable social proof. At this level, the agent researches awards and helps draft submissions, and the founder reviews and submits manually. Focus on free or low-cost awards with near-term deadlines. The goal is signal: can you win and does winning create credibility that solution-aware prospects notice?

**Pass threshold:** >=3 submissions completed, >=1 win or finalist placement, and social proof assets created for at least 1 award within 4 weeks.

## Leading Indicators

- At least 10 relevant awards discovered across 3+ categories
- Submission content blocks written and approved (reusable for future submissions)
- At least 2 submissions completed before the first deadline passes
- Win or finalist notification received within the evaluation period
- At least 1 prospect or customer mentions the award after it is displayed on the website

## Instructions

### 1. Research the Award Landscape

Run the `award-submission-pipeline` drill at Smoke scale (10-15 awards):

1. Use Claygent or web search to find awards in these categories:
   - **Product awards:** G2 Best Software, Product Hunt Golden Kitty, SaaS Awards, Capterra Shortlist
   - **Growth awards:** Inc. 5000, Deloitte Technology Fast 500, SaaStr Annual awards
   - **Industry-specific:** Awards from publications your ICP reads (e.g., MarTech Breakthrough, DevOps Dozen, AI Awards)
   - **People/founder awards:** Forbes 30 Under 30, EY Entrepreneur (if eligible)
2. For each award, record: name, organizer, category, submission deadline, announcement date, entry fee, eligibility requirements, judging criteria, and estimated audience
3. Check competitor award wins: search "{competitor name} award" to see which awards they target
4. Filter for Smoke: focus on awards that are free to enter (or under $100), have deadlines within the next 4 weeks, and have simple submission requirements (form-based, not multi-part essays)

### 2. Score and Select

Score each award on:
- ICP visibility (40%): will your buyers see the winner announcement?
- Win probability (25%): smaller awards, niche categories, and awards without your competitors have higher odds
- PR amplification (20%): does winning generate media coverage or just a badge?
- Competitive value (15%): does a competitor already have this award?

Select the top 3-5 awards to submit to. At Smoke, prioritize speed and ease of submission over prestige.

### 3. Prepare Submission Content Blocks

Build reusable content blocks that can be adapted for any award:

1. **Company overview (150 words):** What you do, who you serve, key differentiator. Write this once and adapt for each submission.
2. **Growth metrics:** Revenue growth %, user growth %, customer count, retention rate. Include specific numbers with timeframes.
3. **Customer impact stories (3):** For each: customer name (with permission), problem, solution, specific metric improvement (e.g., "reduced churn by 35% in 6 months").
4. **Product innovation statement (200 words):** What makes your product technically novel or differentiated from alternatives.
5. **Founder story (100 words):** Background, motivation, journey.

Use Claude API to generate first drafts. **Human action required:** Founder reviews all metrics, claims, and customer references for accuracy. Approve each block.

### 4. Write and Submit

For each selected award:

1. Read the judging criteria for this specific award
2. Map your content blocks to their criteria. If they emphasize growth, lead with metrics. If they emphasize innovation, lead with product differentiation.
3. Use Claude API to generate a tailored submission using the relevant content blocks and the award's specific format
4. **Human action required:** Founder reviews and edits the submission. Verify all numbers are current. Submit.
5. If the award requires references: prepare 2 customers and brief them on what the award is about and that they may be contacted.
6. Log the submission in Attio: award name, category, submission date, deadline, status

### 5. Deploy Social Proof from Wins

When a win or finalist placement is announced:

1. **Website:** Add the award badge to your homepage, pricing page, and about page. Most award organizers provide badge assets.
2. **Social media:** Post an announcement on LinkedIn and Twitter. Thank the organizer. Tag relevant people.
3. **Email signature:** Add the award badge to the founder's and sales team's email signatures with a link to the announcement.
4. **Sales materials:** Update the company overview slide in the sales deck with the award logo.
5. **Press page:** Add to your press or awards page.

### 6. Evaluate Against Threshold

Run the `threshold-engine` drill:

1. After 4 weeks (or when all submissions have been adjudicated), compile:
   - Submissions completed (threshold: >=3)
   - Wins or finalist placements (threshold: >=1)
   - Social proof assets created (threshold: at least 1 award displayed on website/social)
2. Assess: did the submission process produce reusable content blocks? Are the content blocks strong enough to scale?
3. Calculate: time per submission, entry cost per submission

**If PASS:** Awards are a viable credibility channel. Proceed to Baseline with a larger pipeline and systematic tracking.

**If FAIL:** Diagnose:
- No wins: submissions may be too generic. Read winning examples from the award's past years. Target less competitive categories.
- Wins but no visibility: the award may not reach your ICP. Shift to awards published in outlets your buyers read.
- Could not find relevant awards: broaden search. Include regional awards, workplace awards, and people awards.

## Time Estimate

- 3 hours: Award research and scoring (10-15 awards)
- 2 hours: Content block preparation and founder review
- 3 hours: 3-5 submission writing and customization
- 1 hour: Submission logistics and tracking setup
- 1 hour: Social proof deployment and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn | Social proof distribution | Free — [linkedin.com](https://linkedin.com) |
| Attio | CRM — submission tracking | Free plan or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — award research via Claygent | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Claude API | Submission drafting | ~$5-10 — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Free (targeting free-to-enter awards). Entry fees: $0. Clay and Claude API usage minimal.

## Drills Referenced

- `award-submission-pipeline` — discover, score, and prioritize awards; prepare reusable content blocks; write and submit tailored applications
- `threshold-engine` — evaluate Smoke test results against the pass threshold and recommend next action
