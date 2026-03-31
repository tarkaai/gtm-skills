---
name: clay-table-setup
description: Create and configure Clay tables for prospect enrichment workflows
tool: Clay
difficulty: Setup
---

# Set Up a Clay Table

## Prerequisites
- Clay account with API access
- Clear ICP definition (company size, industry, geography)

## Steps

1. **Create a new table.** In Clay, click "New Table" and name it descriptively (e.g., "Q1 Outbound - Series A SaaS"). Choose "Start from scratch" unless importing from a CSV or CRM.

2. **Define your columns.** Add these core columns: Company Name (text), Domain (URL), Contact Name (text), Title (text), Email (email), LinkedIn URL (URL), Enrichment Status (select: Pending, Enriched, Verified, Failed).

3. **Import your seed data.** Either paste a CSV of target companies, connect directly to your CRM via integration, or use Clay's built-in "Find Companies" source to pull prospects matching your ICP filters.

4. **Set row limits.** Configure your table's row limit to match your credit budget. For Smoke-level plays, cap at 50 rows. For Baseline, 200. This prevents runaway credit usage.

5. **Configure enrichment columns.** Add enrichment columns that will be populated by Clay's waterfall enrichment (see `fundamentals/enrichment/clay-enrichment-waterfall`). Keep enrichment columns to the right of your seed data columns for clarity.

6. **Enable deduplication.** Turn on Clay's built-in dedup using Domain + Contact Name as the composite key. This prevents duplicate enrichment charges.
