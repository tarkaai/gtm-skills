---
name: crm-duplicate-prevention
description: Real-time duplicate detection and prevention at point of record creation, with fuzzy matching and automated merge recommendations
category: Operations
tools:
  - Attio
  - n8n
  - Clay
fundamentals:
  - attio-contacts
  - attio-lists
  - attio-notes
  - clay-deduplication
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-crm-integration
---

# CRM Duplicate Prevention

Intercept record creation in real time to detect and prevent duplicates before they enter the CRM. Uses exact matching (email, domain) and fuzzy matching (name similarity, company variations) to catch duplicates that simple rules miss.

## Input

- Attio workspace with existing records
- n8n instance with Attio webhook or polling integration
- Clay workspace (for fuzzy matching on bulk operations)

## Steps

### 1. Set up real-time creation interceptor

Use `n8n-triggers` to watch for new record creation in Attio:
- Listen for `record.created` events on the People and Companies objects
- Debounce: wait 5 seconds after creation to allow any concurrent field updates to settle

### 2. Run exact match check

When a new record is created, immediately check for exact matches using `attio-contacts`:

**For contacts:**
- Query Attio for existing contacts with the same email address
- If match found: this is a confirmed duplicate

**For companies:**
- Query Attio for existing companies with the same domain
- If match found: this is a confirmed duplicate

### 3. Run fuzzy match check

If no exact match, run fuzzy checks using `n8n-workflow-basics` code node:

**For contacts:**
- Query Attio for contacts at the same company domain
- Compare names using normalized string comparison: lowercase, strip whitespace, remove common prefixes/suffixes (Mr., Dr., Jr., III)
- Flag as potential duplicate if normalized name similarity > 80%

**For companies:**
- Query Attio for companies with similar names
- Normalize: lowercase, remove legal suffixes (Inc., LLC, Ltd., Corp., GmbH), remove punctuation
- Flag as potential duplicate if normalized similarity > 85%

### 4. Handle confirmed duplicates

When a duplicate is confirmed (exact email or domain match):

1. Use `attio-notes` to create a note on BOTH records: "Potential duplicate detected. This record shares [email/domain] with [link to other record]. Review and merge."
2. Add both records to a "Pending Merge" list via `attio-lists`
3. Determine which record has more complete data (higher field count)
4. Generate a merge recommendation: "Keep [record A] (more complete: 12/15 fields) and merge [record B] (8/15 fields) into it"

### 5. Handle potential duplicates (fuzzy match)

When a fuzzy match is found:

1. Use `attio-notes` to create a note: "Possible duplicate — similar [name/company name] found. Compare with [link to other record]."
2. Add to a "Review Duplicates" list (separate from confirmed duplicates)
3. Do NOT auto-merge — fuzzy matches need human confirmation

### 6. Batch deduplication for existing records

For cleaning up historical duplicates, run a batch process:

1. Export all contacts to Clay using `n8n-crm-integration`
2. Use `clay-deduplication` with composite key (email + domain) for exact matches
3. Run a second pass with name + domain for fuzzy matches
4. Import duplicate pairs back to Attio as a "Historical Duplicates" list
5. Process the list: merge confirmed duplicates, review fuzzy matches

### 7. Track duplicate metrics

Log deduplication events:
- `duplicate_prevented`: new record creation was flagged before becoming a problem
- `duplicate_merged`: two records were merged
- `duplicate_false_positive`: a flagged pair was reviewed and determined to be distinct records

Track duplicate prevention rate: `(duplicates_prevented / new_records_created) * 100`

## Output

- Real-time duplicate detection on every new record creation
- Exact and fuzzy matching for contacts and companies
- "Pending Merge" and "Review Duplicates" lists in Attio
- Merge recommendations with data completeness comparison
- Batch deduplication process for historical cleanup
- Duplicate prevention metrics
