---
name: community-directory-search
description: Search community directories and aggregators to discover alumni, campus, and professional org groups
tool: Clay
difficulty: Setup
---

# Community Directory Search

Programmatically discover alumni networks, campus organizations, professional associations, and industry groups where your ICP participates. This fundamental covers the search and cataloging step -- not engagement.

## Approach

Use a combination of Clay web scraping, LinkedIn API queries, and structured web search to build a comprehensive community list. Each approach targets a different community type.

### Method 1: LinkedIn Groups Discovery (LinkedIn API)

Search LinkedIn's group directory for groups matching your ICP's industry, role, and affiliations.

**Endpoint:** `GET https://api.linkedin.com/v2/search?q=groups`

```
Headers:
  Authorization: Bearer {LINKEDIN_ACCESS_TOKEN}
  X-Restli-Protocol-Version: 2.0.0

Query parameters:
  keywords: "{industry} {role} alumni"
  start: 0
  count: 25
```

Iterate through result pages. For each group, extract:
- Group name and ID
- Member count
- Description
- Activity level (last post date)
- Admin approval required (open vs closed)

**Search queries to run (adjust per ICP):**
- `"{university name} alumni {industry}"`
- `"{professional association} members"`
- `"{city} {industry} professionals"`
- `"{role title} community"`
- `"YPO" OR "EO" OR "Vistage" OR "{industry} council"`

### Method 2: Clay Community Enrichment

Create a Clay table to enrich and expand community discovery.

1. **Seed the table** with known community names from your ICP research
2. **Use Claygent** (via `clay-claygent` fundamental) to search for:
   - "What Slack communities exist for {ICP role} in {ICP industry}?"
   - "What Discord servers are active for {topic}?"
   - "List alumni associations for {university} that have active online groups"
   - "What professional organizations exist for {role} in {geography}?"
3. **Enrich each result** with:
   - Platform (Slack, Discord, LinkedIn, Circle, Discourse, Facebook, in-person)
   - Estimated member count
   - Joining requirements (open, application, referral, paid)
   - Cost (free, membership fee amount)
   - Activity indicators (posts per week if available)

### Method 3: Structured Web Search

Run structured searches to find communities that don't appear in LinkedIn or Slack directories.

**Alumni networks:**
```
site:linkedin.com/groups "{university} alumni"
site:facebook.com/groups "{university} alumni {industry}"
"{university} alumni network" "{city}" site:alumni.{university}.edu
"{university}" "alumni chapter" "{city}" "join"
```

**Campus organizations:**
```
site:campusgroups.com "{university}"
site:engage.{university}.edu "organizations"
"{university}" "student org" "{topic}" "advisor"
"{university}" "entrepreneurship club" OR "business club" OR "tech club"
```

**Professional organizations:**
```
"{industry}" "professional association" "membership" "chapter"
"{role}" "professional organization" "join" "{geography}"
site:meetup.com "{industry}" "{city}"
"{industry} council" OR "{industry} alliance" OR "{industry} forum" members
```

**Slack/Discord communities:**
```
site:slack.com "{industry}" "join"
site:slofile.com "{topic}"
site:discordservers.com "{topic}"
site:top.gg "{industry}"
"{topic} slack community" "join" "{year}"
```

### Method 4: Aggregator APIs

Query community aggregator sites programmatically:

**Slofile (Slack directory):**
```
GET https://slofile.com/search?q={topic}
```
Parse HTML response for community names, member counts, and join links.

**Discord server search:**
```
GET https://discord.com/api/v10/discovery/search?query={topic}&limit=25
Headers: Authorization: Bot {DISCORD_BOT_TOKEN}
```

**Meetup API:**
```
GET https://api.meetup.com/find/groups?text={topic}&location={city}&radius=50
```
Returns local professional groups and their member counts.

## Output Schema

For each discovered community, produce a record:

```json
{
  "name": "SaaS Founders Network",
  "platform": "slack",
  "url": "https://saasfoundernetwork.slack.com",
  "type": "professional_org",
  "member_count": 2400,
  "activity": "high",
  "join_method": "application",
  "cost": "free",
  "geography": "global",
  "icp_relevance": "high",
  "notes": "Active #growth channel with 50+ messages/day. Many Series A-B founders."
}
```

Community types: `alumni_network`, `campus_org`, `professional_org`, `industry_slack`, `industry_discord`, `meetup_group`, `linkedin_group`, `facebook_group`, `forum`

## Error Handling

- **Rate limits:** LinkedIn API limits to 100 requests/day for most apps. Batch searches and cache results.
- **Closed communities:** Many alumni and professional groups require verification. Flag these as "requires_manual_join" and include the application URL.
- **Stale results:** Web search may return inactive communities. Always verify the last activity date before adding to your target list.
- **API authentication failures:** LinkedIn and Discord require OAuth tokens. If tokens expire, re-authenticate before retrying.
