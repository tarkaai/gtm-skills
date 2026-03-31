---
name: clay-deduplication
description: Prevent duplicate records and wasted enrichment credits in Clay
tool: Clay
product: Clay
difficulty: Beginner
---

# Deduplicate Records in Clay

## Prerequisites
- Clay table with imported or enriched data
- Understanding of your unique identifier fields

## Steps

1. **Choose your dedup key.** The best composite key for contact deduplication is Email + Company Domain. For company-only tables, use Domain alone. Never rely on name alone since variations ("IBM" vs "International Business Machines") cause false negatives.

2. **Enable table-level deduplication.** In Clay's table settings, turn on deduplication and select your key columns. Clay will automatically flag or skip duplicate rows when new data is added.

3. **Handle existing duplicates.** If your table already has duplicates, sort by your dedup key columns to group them together. Use Clay's "Remove Duplicates" action to keep the most recently enriched version and remove the rest.

4. **Cross-table deduplication.** If you run multiple campaigns, check new prospects against existing tables before enriching. Export your "master" contact list and use it as a suppression list when importing new seed data.

5. **CRM dedup sync.** Before pushing enriched contacts to your CRM (see `fundamentals/crm/attio-contacts`), check for existing records. Use email as the match key in Attio to update existing contacts rather than creating duplicates.

6. **Monitor credit waste.** Check your Clay credit usage weekly. If you see credits spent on rows that already exist in your CRM, your dedup process has a gap. Tighten your suppression list.
