---
name: clay-table-setup
description: Create and configure Clay tables for prospect enrichment workflows
tool: Clay
product: Clay
difficulty: Setup
---

# Set Up a Clay Table

## Prerequisites
- Clay account with API access
- Clear ICP definition (company size, industry, geography)

## Steps

1. **Create a new table via API.** Use the Clay REST API to create a table:
   ```
   POST /api/v1/tables
   { "name": "Q1 Outbound - Series A SaaS", "source": "blank" }
   ```
   Name tables descriptively with date and ICP segment for easy identification.

2. **Define your columns.** Add core columns via the API: Company Name (text), Domain (URL), Contact Name (text), Title (text), Email (email), LinkedIn URL (URL), Enrichment Status (select: Pending, Enriched, Verified, Failed).

3. **Import your seed data.** Upload seed data via the API -- either a CSV of target companies, or use Clay's built-in "Find Companies" source to pull prospects matching your ICP filters programmatically.

4. **Set row limits.** Configure the table's row limit to match your credit budget. For Smoke-level plays, cap at 50 rows. For Baseline, 200. This prevents runaway credit usage.

5. **Configure enrichment columns.** Add enrichment columns that will be populated by Clay's waterfall enrichment (see `clay-enrichment-waterfall`). Keep enrichment columns to the right of your seed data columns for clarity.

6. **Enable deduplication.** Turn on Clay's built-in dedup using Domain + Contact Name as the composite key. This prevents duplicate enrichment charges.
