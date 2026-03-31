---
name: account-research-enrichment
description: Batch-enrich target accounts with firmographics, news, tech stack, and contacts via Clay automation
category: Research
tools:
  - Clay
  - Attio
  - Apollo
fundamentals:
  - clay-table-setup
  - clay-enrichment-waterfall
  - clay-claygent
  - clay-intent-signals
  - news-signal-search
  - tech-stack-detection
  - account-intelligence-assembly
  - attio-lists
---

# Account Research Enrichment

This drill automates the account research process for batches of 30-50+ accounts. Instead of manually researching each account, you configure Clay tables with enrichment columns that run automatically across all rows. The output is a fully enriched account list with research briefs pushed to your CRM.

## Input

- A qualified prospect list in Attio (from `build-prospect-list` drill)
- Clay account with sufficient credits (budget ~15-20 credits per account)
- Your ICP document with pain points, buyer personas, and relevant technologies

## Steps

### 1. Create the research table in Clay

Run the `clay-table-setup` fundamental. Create a new Clay table named "{date}-account-research-{campaign}". Import your prospect list from Attio — pull company name, domain, and primary contact for each account.

### 2. Configure firmographic enrichment

Using `clay-enrichment-waterfall`, add enrichment columns in waterfall order:
- **Company data**: Clearbit > Apollo > LinkedIn. Populate: employee count, revenue estimate, industry, founding year, headquarters.
- **Funding data**: Crunchbase > PitchBook. Populate: last funding round, amount, date, lead investor, total raised.

### 3. Configure tech stack enrichment

Add a BuiltWith or Wappalyzer enrichment column per the `tech-stack-detection` fundamental. Input: company domain. Output: full technology list.

Add a formula column that classifies each detected technology:
```
IF tech IN {your_complementary_tools} THEN "complementary"
ELSE IF tech IN {your_competitor_tools} THEN "competing"
ELSE "neutral"
```

### 4. Configure news signal enrichment

Add a Claygent column per the `news-signal-search` fundamental. Prompt each row to search for the last 90 days of news. Parse the output into structured fields: `top_signal_type`, `top_signal_date`, `top_signal_summary`.

### 5. Configure contact enrichment

Add a "Find People at Company" column using `clay-enrichment-waterfall`. Filter for titles matching your buyer personas. Limit to 3 contacts per company. For each contact, enrich: full name, title, LinkedIn URL, email (verified).

### 6. Generate account scores

Add a formula column that computes a research-based account priority score:

```
score = 0
IF funding_last_90_days THEN score += 25
IF hiring_relevant_roles >= 3 THEN score += 20
IF uses_complementary_tech THEN score += 15
IF uses_competitor_tech THEN score += 15
IF recent_news_signal THEN score += 15
IF contact_found_with_email THEN score += 10
RETURN min(score, 100)
```

### 7. Generate personalization hooks at scale

Add a Claygent column that takes all enrichment data for each row and generates 2 personalization hooks:

```
Given this account data for {Company Name}:
- Funding: {funding_data}
- News: {news_signal}
- Tech stack: {relevant_tech}
- Key contact: {contact_name}, {contact_title}

Generate 2 personalization hooks for cold outreach. Each hook must reference a specific fact from the data above and include a suggested email first line. Return as JSON:
[
  {"hook": "...", "first_line": "..."},
  {"hook": "...", "first_line": "..."}
]
```

### 8. Push enriched data to Attio

Use Clay's Attio integration to push enriched data back to CRM:
- Company record: update firmographics, tech stack, funding data, account priority score
- Contact records: create or update with verified emails, titles, LinkedIn URLs
- Create a note on each company record with the generated personalization hooks

Use the `attio-lists` fundamental to create a dynamic list of high-priority accounts (score >= 50) for immediate outreach.

### 9. Track enrichment metrics

Log to PostHog for each batch:
- `account_batch_enriched` event with properties: `batch_size`, `enrichment_hit_rate`, `avg_score`, `credits_consumed`, `time_elapsed`
- Per-account: `account_researched` with `research_depth: "automated"`, `signal_count`, `hook_count`

## Output

- Fully enriched account list with firmographics, tech stack, news signals, contacts, and personalization hooks
- Priority-scored accounts pushed to Attio with ready-to-use outreach data
- Research metrics logged for ROI comparison against manual research
- Estimated 2-3 minutes per account (vs 15-20 minutes manual)

## Triggers

- Run when a new prospect list is built (after `build-prospect-list` drill)
- Re-run monthly to refresh enrichment data on active target accounts
- At Baseline level, process 30-50 accounts per batch
