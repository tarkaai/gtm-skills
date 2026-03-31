---
name: industry-reports-research-smoke
description: >
  Industry Reports & Research — Smoke Test. Produce one original data-driven report
  on an ICP-relevant topic and distribute it via the founder's LinkedIn and email list
  to validate that research content generates social shares and inbound leads.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Social, Email"
level: "Smoke Test"
time: "12 hours over 2 weeks"
outcome: ">=50 social shares or >=3 inbound leads within 2 weeks of publication"
kpis: ["Report downloads", "Social shares", "Inbound leads from report", "Landing page conversion rate"]
slug: "industry-reports-research"
install: "npx gtm-skills add marketing/problem-aware/industry-reports-research"
drills:
  - icp-definition
  - industry-research-production
  - threshold-engine
---

# Industry Reports & Research — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** FounderSocialContent | **Channels:** Content, Social, Email

## Outcomes

Prove that your ICP values original research from your founder enough to share it and reach out. You are not testing automation, distribution scale, or long-tail SEO. You are testing one question: does a data-driven report on this topic generate signal from problem-aware prospects?

**Pass threshold:** >=50 social shares (LinkedIn reactions + reposts + comments) or >=3 inbound leads (DMs, emails, or form submissions from ICP-matching contacts referencing the report) within 2 weeks of publication.

## Leading Indicators

- Report landing page gets 100+ unique visitors in the first week
- Landing page conversion rate (visitor to download) is above 30% for ungated or above 15% for gated
- At least 5 LinkedIn comments on the launch post that reference a specific finding from the report
- At least 1 DM or email arrives within 3 days of publication from someone who matches ICP
- At least 2 people share the report on their own LinkedIn with their own commentary

## Instructions

### 1. Define your ICP and select the report topic

Run the `icp-definition` drill to document your target audience: job titles, company sizes, industries, and the specific pain points they search for. From the ICP pain points, identify one topic that meets three criteria:
- Your ICP actively discusses this topic on LinkedIn and in industry forums
- No authoritative, recent data-driven report exists on this topic (Google "{topic} report {current year}" -- if the top results are >12 months old or anecdotal, there is a gap)
- You have a credible angle: proprietary product data, domain expertise, or access to survey respondents

Document the topic, the angle, and why it matters to the ICP.

### 2. Produce the report

Run the `industry-research-production` drill. At Smoke level, use the simplest viable data collection method:

**Fastest option (2-3 hours):** Use Clay enrichment to research 50-100 ICP companies and aggregate patterns. Example: "We analyzed the job postings, tech stacks, and public statements of 75 B2B SaaS companies to understand how they approach {topic}."

**Higher-credibility option (5-6 hours):** Run a short survey (10 questions, 30+ responses) using Typeform or Tally distributed to your existing network. Even 30-50 responses produce credible data when the respondent profile is well-defined.

Aim for a 2,000-3,000 word report with 3-5 key findings and 3-4 embedded charts. Publish as a PDF hosted on your site and a companion blog post with an executive summary.

**Human action required:** The founder must review every data point for accuracy, add personal interpretation of the findings, and ensure the report reads as founder-authored. Replace any generic analysis with specific opinions: "This surprised us because..." or "Based on our conversations with 50+ teams, this finding means..."

### 3. Distribute manually via founder channels

At Smoke level, distribution is manual and founder-led. No automation.

**LinkedIn (Day 1):** Write a LinkedIn post leading with the most surprising finding. Use a hook that creates tension: "We analyzed 75 companies and the data contradicts what most founders believe about {topic}." Attach the report chart as an image. Link to the full report in the first comment. Post at 8am in your ICP's primary timezone.

**Email (Day 1):** Send a personal email (not a mass broadcast) to 10-20 contacts who would find the report valuable. Subject: "Original data on {topic} -- thought you'd find this useful." Keep the email to 3 sentences + the report link. Send from the founder's personal email.

**LinkedIn (Day 3):** Write a second post featuring a different finding. Use a different format (carousel, numbered list, or personal story about why you ran this research).

**LinkedIn (Day 7):** Write a third post with a contrarian take or myth-busting angle from the data.

**Human action required:** Engage with every comment on your posts within 2 hours of posting. Reply substantively -- reference the data, ask follow-up questions, thank people who share. DM anyone who comments with a buying signal (mentions their company faces this problem, asks how you collected the data, or shares it with their own commentary).

### 4. Track results and evaluate

Log all activity in a spreadsheet or Attio:
- Report page views (check PostHog or site analytics daily)
- Downloads (if gated)
- LinkedIn: impressions, reactions, comments, shares for each post
- Emails sent and replies received
- DMs received (tag: ICP match yes/no, referenced report yes/no)
- Inbound leads (anyone who reaches out and matches ICP)

After 2 weeks, run the `threshold-engine` drill to evaluate: >=50 social shares or >=3 inbound leads.

**If PASS:** The topic and format resonate. Proceed to Baseline to add proper tracking, expand distribution, and produce a second report.

**If FAIL:** Diagnose:
- Low page views (<100): Distribution failed. The LinkedIn hooks were not compelling, or your network is too small. Try a different hook angle or cross-post in 2-3 relevant communities.
- Page views but low downloads/engagement: The topic is interesting but the report does not deliver enough value. Strengthen the data, add more actionable recommendations, or remove the gate.
- Downloads but no shares or leads: The report was consumed but did not prompt action. Add more surprising/contrarian findings. Make the data more shareable (quotable stats, clear charts).
- Shares but no leads: The content is shareable but does not attract buyers. The topic may be too broad -- narrow to a specific ICP pain point that connects to your product.

## Time Estimate

- ICP definition and topic selection: 2 hours
- Data collection (Clay enrichment or quick survey): 3 hours
- Analysis and report writing: 4 hours
- Founder review and editing: 1.5 hours
- Distribution (3 LinkedIn posts + 10-20 emails): 1 hour
- Tracking and evaluation: 0.5 hours
- **Total: ~12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Company research and data enrichment | Free tier: 100 credits ([clay.com/pricing](https://www.clay.com/pricing)) |
| Typeform / Tally | Survey for primary research | Typeform Free: 10 questions, 10 responses/mo ([typeform.com/pricing](https://www.typeform.com/pricing)); Tally Free: unlimited forms ([tally.so/pricing](https://tally.so/pricing)) |
| Ghost | Report landing page and blog post | Starter: $9/mo ([ghost.org/pricing](https://ghost.org/pricing/)) |
| Anthropic API | Report draft generation and analysis | ~$0.10-0.50 per report draft ([anthropic.com](https://www.anthropic.com)) |
| Attio | Lead tracking and logging | Free: up to 3 users ([attio.com](https://attio.com)) |

**Estimated monthly cost: $0-9** (free tiers sufficient at Smoke volume; Ghost Starter if no existing blog)

## Drills Referenced

- `icp-definition` — define the target audience and identify the pain point that determines the report topic
- `industry-research-production` — produce the report from data collection through publication
- `threshold-engine` — evaluate results against the pass threshold
