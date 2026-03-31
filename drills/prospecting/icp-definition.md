---
name: icp-definition
description: Define and validate your Ideal Customer Profile using data from closed deals and market research
category: Strategy
tools:
  - Attio
  - Clay
  - PostHog
fundamentals:
  - attio-list-management
  - attio-pipeline-management
  - posthog-cohort-analysis
---

# ICP Definition

This drill walks you through defining a rigorous Ideal Customer Profile based on actual data, not assumptions. Your ICP drives every other GTM drill — list building, scoring, messaging, and channel selection all depend on it.

## Prerequisites

- Access to your CRM (Attio) with historical deal data
- PostHog with product usage data (if available)
- At least 10 closed-won deals to analyze (fewer is fine, but patterns are weaker)

## Steps

### 1. Analyze your best customers

Pull your closed-won deals from Attio using the `attio-pipeline-management` fundamental. Sort by deal value, time-to-close, expansion revenue, and retention. Identify the top 20% — these are your model customers.

### 2. Extract firmographic patterns

For your best customers, document: company size (employees and revenue), industry vertical, funding stage, geography, technology stack, and business model (B2B, B2C, marketplace, SaaS). Look for clusters. If 80% of your best deals are Series A-B SaaS companies with 20-100 employees, that is your firmographic ICP.

### 3. Extract buyer persona patterns

Document who signed the deal: their title, department, seniority level, reporting structure, and whether they were the champion, decision maker, or both. Identify common titles and the typical buying committee structure.

### 4. Identify pain points and triggers

Review deal notes and call recordings. What problem drove each customer to seek a solution? What event triggered the search? Map common pain points and triggering events. These feed your messaging and signal detection.

### 5. Validate with usage data

If you have PostHog data, use the `posthog-cohort-analysis` fundamental to compare your best customers' product usage against churned accounts. Which features do high-value customers adopt? This refines your ICP beyond firmographics into behavioral fit.

### 6. Write your ICP document

Create a concise ICP document with these sections: firmographic criteria (must-have and nice-to-have), buyer persona (primary and secondary), pain points (top 3), triggering events (top 3), and disqualification criteria (who is NOT your ICP). Keep it to one page.

### 7. Score and test

Apply your ICP criteria as a scoring model in Clay. Run it against your existing pipeline. Do your current open deals score well? Do lost deals score poorly? If the model matches reality, ship it. If not, adjust the weights.

### 8. Distribute and enforce

Share the ICP document with everyone doing outreach. Load the scoring criteria into Clay so every new prospect gets automatically scored against it. Review quarterly as your product and market evolve.
