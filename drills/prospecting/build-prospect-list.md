---
name: build-prospect-list
description: Source, enrich, and qualify prospects matching your ICP using Clay and your CRM
category: ListBuilding
tools:
  - Clay
  - Attio
  - Apollo
fundamentals:
  - clay-table-setup
  - clay-enrichment-waterfall
  - attio-lists
---

# Build a Prospect List

This drill walks you through sourcing, enriching, and qualifying a prospect list that feeds directly into your outreach plays.

## Prerequisites

- ICP defined (run `icp-definition` drill first if you haven't)
- Clay account with API credits
- Attio workspace with a People and Companies collection
- Apollo account for initial sourcing

## Steps

### 1. Source initial contacts from Apollo

Open Apollo and run a search using your ICP filters: job titles, company size, industry, location, and technology stack. Export up to 500 contacts per batch to CSV. Keep the export focused — broad lists waste enrichment credits.

### 2. Import into Clay

Create a new Clay table using the `clay-table-setup` fundamental. Upload your Apollo CSV. Name the table with the date and ICP segment (e.g., "2024-03-Series-A-DevTools-CTOs"). Set up columns for: name, email, company, title, LinkedIn URL, company size, and funding stage.

### 3. Run enrichment waterfall

Apply the `clay-enrichment-waterfall` fundamental. Stack enrichment providers in priority order: first Clearbit for firmographics, then People Data Labs for contact details, then LinkedIn for role verification. Clay's waterfall logic tries each provider in sequence and stops when data is found, saving credits.

### 4. Score and filter

Add a scoring formula column in Clay. Weight factors based on your ICP: company size match (30%), title seniority match (25%), technology stack overlap (20%), recent funding (15%), hiring signals (10%). Filter to keep only prospects scoring above 70.

### 5. Push qualified prospects to Attio

Use Clay's Attio integration to push qualified rows. Map Clay columns to Attio fields. Use the `attio-lists` fundamental to create a named list for this batch. Tag each contact with the campaign name and source date.

### 6. Verify and deduplicate

In Attio, run a duplicate check against existing contacts. Remove any prospects already in active deals or who have opted out. Verify email addresses using Clay's built-in email verification column before any outreach begins.

### 7. Handoff

Your qualified, enriched list is now in Attio and ready for outreach drills like `cold-email-sequence` or `linkedin-outreach`. Log the list size and qualification rate in PostHog for tracking.
