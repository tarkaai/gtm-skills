---
name: attio-contacts
description: Create and manage contact records in Attio with proper data hygiene
tool: Attio
product: Attio
difficulty: Beginner
---

# Manage Contacts in Attio

## Prerequisites
- Attio workspace configured
- Attio MCP server connected

## Steps

1. **Create contacts.** Use the Attio MCP to create Person records. Required fields: full name, email address, company (linked to Company object), job title, and source (how you found them). Always check for duplicates before creating — search by email first.

2. **Link contacts to companies.** Every contact must be associated with a Company record. If the company doesn't exist, create it first with at minimum: name, domain, and industry.

3. **Enrich contact data.** After creation, add LinkedIn URL, phone number, and any relevant tags. If using Clay for enrichment, the enriched data should flow into these fields automatically via your n8n sync workflow.

4. **Tag contacts by role.** Use a "Role Type" select field: Decision Maker, Champion, Influencer, End User, Blocker. This drives your outreach sequencing — Champions get different messaging than Decision Makers.

5. **Track engagement.** Add a "Last Contacted" date field and update it after every outreach touch. Create a "Contact Status" field: Active, Nurture, Do Not Contact, Bounced.

6. **Merge duplicates.** Periodically query for contacts sharing the same email domain and similar names. Use the Attio MCP to merge duplicates, keeping the record with more complete data as primary.
