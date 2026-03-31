---
name: podcast-host-enrichment
description: Enrich podcast host contact information using Clay waterfall enrichment
tool: Clay
difficulty: Config
---

# Podcast Host Enrichment

Given a list of podcast hosts, find their verified email addresses, LinkedIn profiles, and Twitter handles so you can pitch them directly.

## Tool Options

| Tool | Method | Best For |
|------|--------|----------|
| Clay | Waterfall enrichment (multiple providers) | Highest find rate, automated |
| Apollo | People search API | Direct email lookup by name + company |
| Hunter.io | Domain search API | Email by domain |
| Clearbit | Enrichment API | Company + person data |
| Manual LinkedIn | LinkedIn Sales Navigator search | When automated methods fail |

## Clay Enrichment (Primary)

### Step 1: Set up the Clay table

Create a Clay table with columns:
- `podcast_name` (text)
- `host_name` (text)
- `podcast_website` (URL)
- `host_linkedin` (URL — if found from Podchaser or manual search)
- `host_twitter` (URL — from podcast RSS or show notes)

Import your qualified podcast list from the `podcast-directory-search` step.

### Step 2: Run enrichment waterfall

Add enrichment columns in this priority order:

1. **Find email from LinkedIn URL** (if available): Use Clay's LinkedIn enrichment to pull the associated email
2. **Find email from name + domain**: Use Clay's email finder (stacks Hunter.io, Clearbit, Apollo) with `host_name` + `podcast_website` domain
3. **Find email from podcast RSS**: Parse the RSS `<itunes:owner><itunes:email>` field — many podcasts publish the host's email in their feed metadata
4. **Apollo fallback**: Search Apollo for the host by name + company/podcast name

### Step 3: Verify emails

Add a Clay email verification column. This checks deliverability before you send any pitch. Skip hosts with catch-all or unverifiable emails — prioritize verified addresses.

### Step 4: Enrich with context

Add columns that help personalize your pitch:
- **Recent episode title**: Pull from RSS or ListenNotes. Reference their latest episode in your pitch.
- **Host LinkedIn headline**: Shows their focus area — match your pitch angle to it.
- **Podcast guest history**: Search ListenNotes for `type=episode` on this podcast to see what kind of guests they book.

## Apollo People Search API

```http
POST https://api.apollo.io/v1/people/match
Header: Content-Type: application/json
Header: X-Api-Key: {APOLLO_API_KEY}

{
  "first_name": "Jane",
  "last_name": "Smith",
  "organization_name": "The SaaS Podcast",
  "domain": "thesaaspodcast.com"
}
```

Response includes: `email`, `linkedin_url`, `title`, `organization`.

## RSS Feed Email Extraction

Many podcast hosts publish their email in the RSS feed. Parse the XML:

```python
import feedparser
feed = feedparser.parse("https://podcast-rss-url.com/feed.xml")
owner_email = feed.feed.get("publisher_detail", {}).get("email")
# Also check: feed.feed.get("author_detail", {}).get("email")
```

This is the highest-signal email — it is the address the host chose to publish publicly for their podcast.

## Output

A Clay table or Attio list with verified contact info for each podcast host:
- Host name
- Verified email
- LinkedIn URL
- Twitter handle
- Podcast name
- Recent episode reference
- Contact method preference (email > Twitter DM > LinkedIn InMail)

## Error Handling

- **No email found**: Fall back to Twitter DM or LinkedIn connection request with pitch note
- **Catch-all domain**: Send but monitor bounce rate. If bounce > 5%, pause and switch to social outreach
- **Host uses booking form**: Some podcasts have a "Be a Guest" page. Flag these for manual or form-fill approach instead of email
