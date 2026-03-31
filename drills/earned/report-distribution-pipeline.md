---
name: report-distribution-pipeline
description: Multi-channel distribution workflow for industry reports including social, email, PR, and community amplification
category: Content
tools:
  - LinkedIn
  - Loops
  - Ghost
  - n8n
  - Anthropic
fundamentals:
  - linkedin-organic-posting
  - linkedin-organic-hooks
  - linkedin-organic-formats
  - linkedin-organic-scheduling
  - loops-broadcasts
  - ghost-blog-publishing
  - ghost-newsletters
  - ai-content-ghostwriting
  - n8n-scheduling
---

# Report Distribution Pipeline

This drill takes a published industry report and distributes it across all available channels over 3-4 weeks to maximize downloads, social shares, backlinks, and inbound leads. Each channel gets a tailored version of the report's key findings, not just a link dump.

## Input

- Published report with landing page URL (from `industry-research-production` drill)
- Distribution brief: 5-8 key findings, 4-6 social graphics, quotable statistics
- ICP definition: who should see this report and where they spend time
- Email subscriber list and LinkedIn follower base size
- List of relevant communities, newsletters, and journalists (if available)

## Steps

### 1. Build the 4-week distribution calendar

Map report promotion across channels over 4 weeks. Front-load the first 10 days for maximum momentum, then sustain with repurposed angles.

**Week 1 (Launch):**
- Day 1: LinkedIn post (headline finding), email broadcast to subscriber list, blog post with executive summary
- Day 2: LinkedIn post (second finding with chart graphic), Twitter thread
- Day 3: Post in 2-3 relevant communities (Slack groups, Reddit, indie hackers)
- Day 5: LinkedIn post (contrarian take from the data)

**Week 2 (Amplification):**
- Day 8: LinkedIn carousel (top 5 findings as slides)
- Day 10: Newsletter feature with deeper analysis of one finding
- Day 12: LinkedIn post (personal story about why this research matters)

**Week 3 (Repurpose):**
- Day 15: Short-form video summarizing the report (Loom or recorded talking head)
- Day 17: LinkedIn post (myth-busting angle from the data)
- Day 19: Guest post pitch to 2-3 industry publications with exclusive finding angle

**Week 4 (Long tail):**
- Day 22: LinkedIn poll based on a finding ("Does this match your experience?")
- Day 25: Roundup post: "Here's what people said about our report" (quote commenters)
- Day 28: Email broadcast to non-openers with different subject line

### 2. Write the social content series

Using the `ai-content-ghostwriting` fundamental, generate all social posts for the 4-week calendar:

For each LinkedIn post, use the `linkedin-organic-hooks` fundamental to craft the opening line. Structure:
- **Hook** (line 1): Lead with the most surprising data point or a question the data answers
- **Body**: Provide the context and data behind the hook. Reference the chart if posting a graphic
- **CTA**: "Full report here: [link]" or "What's your experience? Drop it in the comments."

For each post, specify:
- The specific finding being promoted
- The social graphic to attach (if any)
- The posting time (using `linkedin-organic-scheduling` fundamental)
- Pre-planned engagement targets: 3-5 accounts to engage with before posting

Using `linkedin-organic-formats`, vary the formats across the 4 weeks: text-only, image + text, carousel, poll, video.

### 3. Send the email broadcasts

Using the `loops-broadcasts` fundamental, create 3 email sends:

**Email 1 (Day 1 -- Launch):**
- Subject line: Reference the headline finding as a question or surprising stat
- Body: Executive summary (3-4 sentences), 2-3 bullet-point findings, direct link to report
- CTA: "Read the full report"

**Email 2 (Day 10 -- Deep dive):**
- Subject line: Focus on the most actionable finding
- Body: 200-300 words expanding on one finding with practical takeaways
- CTA: "See how this compares to your situation -- full data here: [link]"

**Email 3 (Day 28 -- Re-send to non-openers):**
- Different subject line: curiosity-based or FOMO angle
- Same body as Email 1

Tag all email link clicks with `utm_source=email&utm_campaign=report-{slug}` for PostHog attribution.

### 4. Publish the blog companion post

Using the `ghost-blog-publishing` fundamental, publish a blog post that:
- Summarizes the report's executive findings (500-800 words)
- Embeds 2-3 key charts inline
- Links to the full report for download
- Is optimized for SEO with the report's topic as the target keyword
- Includes schema markup for "Report" type content

This blog post becomes the evergreen search-discoverable entry point for the report long after the social campaign ends.

### 5. Distribute to communities

For each relevant community (Slack groups, Discord servers, Reddit, Indie Hackers, Hacker News):
- Read the community rules on self-promotion
- Lead with the most relevant finding for that community's audience, not the report link
- Share the insight first, then mention "we put together a full report if this is useful: [link]"
- Engage with every response for 24 hours minimum
- Never post the same copy across communities -- tailor each post

### 6. Track distribution performance

Log every distribution action in a tracking sheet or n8n workflow:
- Channel, date, post URL, content angle used
- Engagement metrics (24h and 7d after posting)
- Link clicks to report page (via PostHog UTM tracking)
- Downloads or email captures (from report landing page)
- Leads generated (contacts who downloaded and match ICP)

After 4 weeks, aggregate: total downloads, total social shares, total leads captured, total meetings booked attributable to the report. This data informs topic selection for the next report.

## Output

- 10-15 social posts published across 4 weeks
- 3 email broadcasts sent to subscriber list
- 1 blog companion post published
- 3-5 community posts distributed
- Complete tracking log with per-channel attribution
- Post-campaign performance summary

## Triggers

Run this drill immediately after each report is published. The 4-week calendar begins on report launch day. At Scalable/Durable levels, this drill runs quarterly aligned with the `industry-research-production` drill cadence. Time investment: 6-10 hours per report distribution cycle.
