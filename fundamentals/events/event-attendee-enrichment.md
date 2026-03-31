---
name: event-attendee-enrichment
description: Extract and enrich attendee/speaker lists from event websites and platforms
tool: Clay
difficulty: Config
---

# Event Attendee Enrichment

Extract publicly available speaker lists, sponsor lists, and attendee directories from event websites, then enrich those contacts with Clay for pre-event targeting.

## Authentication

- Clay account with enrichment credits
- Claygent enabled for web scraping

## Step 1: Extract Speaker and Sponsor Lists

Add a Claygent column to your events table:

```
Visit {Event URL} and find all speakers listed on the website.
For each speaker return:
- Full name
- Job title
- Company name
- LinkedIn URL (if linked on the page)
Format as JSON array.
```

Run a second Claygent column for sponsors:

```
Visit {Event URL} and find all sponsor companies listed on the website.
For each sponsor return:
- Company name
- Sponsorship tier (if shown: Platinum, Gold, etc.)
- Company website URL
Format as JSON array.
```

## Step 2: Expand to Individual Rows

Use Clay's "Expand rows" feature to convert multi-person JSON arrays into one row per contact. Each row gets the parent event name and date as inherited columns.

## Step 3: Enrich Contacts

For each person row, run the standard enrichment waterfall (see `clay-enrichment-waterfall`):

1. **LinkedIn URL**: If not scraped from the event page, use Clay's LinkedIn lookup by name + company.
2. **Email**: Clearbit > Hunter > People Data Labs waterfall.
3. **Company firmographics**: Company size, funding stage, industry via Clearbit or Crunchbase.
4. **Role verification**: Confirm the person's current title matches what was listed (people change jobs).

## Step 4: Score for Hallway Demo Relevance

Add a formula column that scores each contact:

- **Title match to ICP buyer persona** (40%): Exact title match = 100, adjacent title = 60, non-buyer = 0
- **Company fit** (30%): Company size, industry, funding stage match to ICP
- **Accessibility** (20%): Speaker = 80 (they'll be in hallways between sessions), Sponsor rep = 60 (at booth but takes breaks), Attendee = 40 (less predictable location)
- **Recency** (10%): Event in next 7 days = 100, 8-14 days = 80, 15-30 days = 50

## Step 5: Push to CRM

Export scored contacts to Attio using `attio-lists`. Tag each contact with:
- `source: hallway-demo-prospect`
- `event: {event_name}`
- `event_date: {date}`
- `priority: {score tier: hot/warm/cold}`

## Error Handling

- Many event websites use JavaScript rendering; if Claygent returns empty results, try with explicit instructions: "This page may use JavaScript. Look for speaker sections, about pages, or agenda pages."
- If no public attendee list exists, focus on speakers and sponsors only -- these are higher-value targets anyway.
- Deduplicate contacts who appear at multiple events before pushing to CRM.
