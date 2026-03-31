---
name: award-submission-pipeline
description: Discover relevant industry awards, score and prioritize by ICP impact, prepare submissions, and track the full lifecycle from submission to announcement
category: Awards
tools:
  - Clay
  - Attio
  - Anthropic Claude API
fundamentals:
  - clay-claygent
  - clay-table-setup
  - clay-scoring
  - attio-lists
  - attio-notes
---

# Award Submission Pipeline

This drill builds a systematic pipeline for discovering industry awards, evaluating their value, preparing compelling submissions, and tracking outcomes. It replaces ad-hoc "someone saw an award deadline on Twitter" with a data-driven process that maximizes win rate and ICP visibility.

## Input

- Company description: what you do, key differentiators, and target market
- ICP definition: who your buyers are and what publications/events they follow
- Customer proof points: 3-5 customer success stories with specific metrics
- Company milestones: funding, revenue milestones, product launches, team growth
- Competitor names (to check which awards they have won)

## Steps

### 1. Discover relevant awards

Use the `clay-claygent` fundamental to search for industry awards:

**Search queries:**
1. "{your industry} awards {current year}" (e.g., "B2B SaaS awards 2026")
2. "{your category} best product award" (e.g., "best sales automation tool award")
3. "startup awards {your stage}" (e.g., "startup awards Series A")
4. Awards your competitors have won: search "{competitor name} award winner"
5. Awards your ICP would see: search for awards featured in publications your ICP reads

**Award categories to include:**
- **Industry-specific:** Awards from trade publications (SaaS Awards, DevOps awards, MarTech Breakthrough)
- **Business stage:** Growth/startup awards (Inc. 5000, Deloitte Fast 500, Forbes Cloud 100)
- **Regional:** Local/regional business awards (Best Places to Work, local chamber awards)
- **Product-focused:** Product Hunt Golden Kitty, G2 Best Software, Capterra Shortlist
- **People-focused:** Founder awards (Forbes 30 Under 30, EY Entrepreneur of the Year)
- **Workplace:** Best Places to Work, Glassdoor Best, BuiltIn Best

### 2. Build the award tracking table

Use `clay-table-setup` to create a table called "Award Pipeline - {year}" with columns:

| Column | Type | Notes |
|--------|------|-------|
| award_name | Text | Full name of the award |
| organizer | Text | Who runs the award (publication, association, etc.) |
| category | Select | industry / growth / regional / product / people / workplace |
| submission_deadline | Date | When the submission is due |
| announcement_date | Date | When winners are announced |
| entry_fee | Number | Cost to submit (0 if free) |
| estimated_audience | Number | How many people see the winners (organizer's reach) |
| icp_overlap | Number 1-5 | How much the award's audience overlaps with your ICP |
| competitor_won | Boolean | Has a direct competitor won this award before? |
| submission_complexity | Select | simple (form) / moderate (essay) / complex (multi-part, references required) |
| status | Select | researching / preparing / submitted / shortlisted / finalist / winner / not selected |
| submission_url | URL | Where to submit |
| notes | Text | Special requirements, judging criteria, tips |

### 3. Score and prioritize

Use the `clay-scoring` fundamental to rank awards:

- **ICP visibility (40%):** Will your ICP see the winner announcement? Awards featured in publications your buyers read score highest.
- **Win probability (25%):** Smaller, niche awards have higher win rates than major publications. Free awards get more submissions (lower odds). Consider: do you meet all eligibility criteria?
- **PR amplification (20%):** Does winning create press coverage opportunities? Some awards (Inc. 5000, Forbes lists) generate significant media buzz. Others are badge-only.
- **Competitive value (15%):** If a competitor has won this award, winning it yourself neutralizes their advantage. If no competitor has won, you get first-mover credibility.

Set thresholds: Priority 1 (score >= 8), Priority 2 (score 6-7), Priority 3 (score 4-5). Discard below 4.

### 4. Prepare submission content blocks

Before writing individual submissions, prepare reusable content blocks:

1. **Company overview block (150 words):** What you do, who you serve, key differentiator
2. **Growth metrics block:** Revenue growth rate, user growth, customer count, retention rate
3. **Customer impact stories (3-5):** Each story: customer name, problem, solution, specific metric improvement
4. **Product innovation block:** What you built that is technically novel or differentiated
5. **Team/culture block:** Team size, growth rate, diversity stats, culture initiatives
6. **Founder story block:** Founder background, motivation, journey

Use Claude API to generate drafts of each block. **Human action required:** Founder reviews and approves all metrics and claims.

### 5. Write submissions

For each Priority 1 and Priority 2 award:

1. Read the award's judging criteria carefully. Map your content blocks to their criteria.
2. Use Claude API to generate a submission draft that:
   - Addresses every judging criterion explicitly
   - Leads with the strongest relevant metric
   - Includes specific numbers (not "significant growth" but "340% revenue growth")
   - Tells a story, not just lists achievements
   - Stays within word limits
3. **Human action required:** Founder reviews each submission for accuracy and approves before sending.
4. If the award requires references: identify 2-3 customers willing to be contacted and brief them on what the award is about.

### 6. Submit and track

1. Submit each award before the deadline (set reminders 7 days and 1 day before)
2. Log in Attio using `attio-lists`: create "Award Submissions - {year}" list
3. Update status as results come in: submitted -> shortlisted -> finalist -> winner / not selected
4. For wins: immediately trigger the amplification workflow (social posts, press page update, email to customers)

## Output

- Scored, prioritized list of 15-30 relevant awards in Clay
- Reusable content blocks for rapid submission writing
- Completed submissions tracked in Attio with status pipeline
- Deadline reminders set for all active submissions

## Triggers

- Run once at play start to build the initial pipeline
- Run monthly at Scalable+ to discover new awards and maintain the pipeline
- Run immediately when a major milestone occurs (creates new submission material)
