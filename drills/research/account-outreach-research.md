---
name: account-outreach-research
description: Manually research a target account and produce a structured brief with personalization hooks for outreach
category: Research
tools:
  - Clay
  - Attio
  - LinkedIn
fundamentals:
  - account-intelligence-assembly
  - news-signal-search
  - tech-stack-detection
  - org-chart-research
  - attio-custom-attributes
  - attio-notes
---

# Account Research Brief

This drill walks an agent through the manual process of researching a single target account and producing a structured outreach brief. It is designed for Smoke-level testing where the agent researches each account individually, the human reviews and executes outreach, and you measure whether deep research improves reply rates.

## Input

- A target account: company name and domain
- Your ICP document (from `icp-definition` drill) with pain points and buyer personas
- Access to Clay, Attio, and LinkedIn

## Steps

### 1. Gather company overview

Run the `account-intelligence-assembly` fundamental against the target company. Pull firmographics from Clay: company name, domain, industry, employee count, revenue estimate, funding stage, last funding round, founding year, headquarters location.

Store the raw data in Attio as custom attributes on the company record using `attio-custom-attributes`.

### 2. Search for recent news and signals

Run the `news-signal-search` fundamental. Query the last 90 days for: funding announcements, product launches, executive hires, partnerships, acquisitions, layoffs, market expansion. Score each signal for outreach relevance.

Capture the top 3 signals with dates and sources.

### 3. Detect technology stack

Run the `tech-stack-detection` fundamental. Identify the company's technology stack from their website. Classify each detected technology as complementary (integration angle), competing (displacement angle), indicator (qualification signal), or neutral.

Focus on technologies in your product's category and adjacent categories.

### 4. Research key contacts

Run the `org-chart-research` fundamental to identify 3-5 key contacts at the company matching your buyer personas. For each contact, gather: full name, title, department, LinkedIn URL, tenure at company, recent LinkedIn posts or activity, and any shared connections with your team.

Classify each contact's likely role: economic buyer, champion, influencer, end user.

### 5. Identify personalization hooks

From the data gathered in steps 1-4, extract 2-3 personalization hooks. Each hook must be:
- **Specific**: references a real event, fact, or signal (not "your company is growing")
- **Recent**: from the last 90 days if possible
- **Relevant**: connects to a pain point your product solves
- **Actionable**: can be turned into a compelling email first line

Rank hooks by strength: recent funding > executive hire > product launch > tech stack overlap > hiring signals > generic industry trend.

### 6. Compile the brief

Write a structured brief using the `attio-notes` fundamental. Attach it to the company record in Attio:

```
## Account Brief: {Company Name}
**Researched:** {date} | **Time spent:** {minutes}

### Company Snapshot
- Industry: {industry} | Employees: {count} | Funding: {stage}, last round {amount} on {date}
- Tech stack (relevant): {list}

### Top Signals
1. {Signal with date and source}
2. {Signal with date and source}
3. {Signal with date and source}

### Key Contacts
| Name | Title | Role | Priority |
|------|-------|------|----------|
| {name} | {title} | {champion/buyer/influencer} | {1/2/3} |

### Personalization Hooks
1. **{Hook}**: {one-sentence rationale} → Suggested first line: "{email opener}"
2. **{Hook}**: {one-sentence rationale} → Suggested first line: "{email opener}"
3. **{Hook}**: {one-sentence rationale} → Suggested first line: "{email opener}"

### Recommended Approach
- Entry point: {Contact name and why}
- Channel: {Email / LinkedIn / both}
- Angle: {One sentence connecting their situation to your value}
```

### 7. Track research metrics

Log the following in PostHog for each account researched:
- `account_researched` event with properties: `company_domain`, `research_time_minutes`, `signal_count`, `hook_count`, `research_depth` ("manual")
- This data feeds the comparison between researched vs non-researched outreach performance

## Output

- One structured account brief per target account, stored in Attio
- 2-3 ranked personalization hooks ready for outreach
- Research time logged for ROI calculation
- Key contacts identified with suggested entry point

## Triggers

- Run before any outreach to a new target account
- Re-run when an account re-enters the pipeline after going cold for 60+ days
- At Smoke level, expect 15-20 minutes per account for thorough research
