---
name: slack-discord-reconnaissance
description: Discover, evaluate, and rank Slack workspaces and Discord servers where your ICP is active
category: Community
tools:
  - Clay
  - Web Search
  - Slack API
  - Discord API
  - Attio
fundamentals:
  - community-directory-search
  - slack-api-read
  - discord-api-read
  - attio-lists
---

# Slack/Discord Reconnaissance

Discover and rank Slack workspaces and Discord servers where your ICP participates. Produces a prioritized engagement target list with detailed profiles for each community. Runs once at play start and is refreshed quarterly.

## Input

- ICP definition (firmographics, job titles, pain points, triggering events) from the `icp-definition` drill
- Your product category and the problems you solve
- Competitor names

## Steps

### 1. Generate discovery keyword lists

From your ICP definition, produce three keyword lists:

**Pain-point keywords** — problems your ICP discusses in communities:
- Extract the top 3 pain points from your ICP doc
- For each, generate 3-5 natural-language phrases: "how do I handle X", "anyone solved Y", "struggling with Z"
- Include tool-seeking variants: "what tool do you use for X", "is there a way to automate Y"

**Category keywords** — your product category and adjacent spaces:
- Product category and synonyms
- "best [category] tool", "[category] recommendations", "[category] for [ICP role]"
- Competitor names and comparison queries

**ICP identity keywords** — terms that describe your target person:
- Job titles: "startup founder", "head of growth", "devtools"
- Industries: "B2B SaaS", "fintech", "developer tools"
- Community archetypes: "indie hackers", "SaaS operators", "growth marketers"

### 2. Discover candidate communities

Using the `community-directory-search` fundamental, run the following discovery methods:

**Slack community directories:**
- Search https://slofile.com for each keyword
- Search https://standuply.com/slack-chat-groups for industry terms
- Search "site:slack.com {keyword}" via web search
- Search "{keyword} slack community join {current_year}" via web search
- Check https://www.saastr.com/saastr-slack/ and similar curated lists for your industry

**Discord server directories:**
- Search https://disboard.org for each keyword
- Search https://discordservers.com for each keyword
- Use Discord's discovery API: `GET https://discord.com/api/v10/discovery/search?query={keyword}&limit=25`
- Search "discord server {keyword} {industry}" via web search

**Cross-platform:**
- Use Clay's Claygent to ask: "What are the most active Slack communities for {ICP role} in {industry}?"
- Use Clay's Claygent to ask: "What are the largest Discord servers for {topic}?"
- Check competitor websites and docs for community links (many SaaS companies have public Slack or Discord communities)
- Search Product Hunt and Indie Hackers for community mentions

Target: 20-40 candidate communities before filtering.

### 3. Evaluate each candidate

For each Slack workspace you can access, using the `slack-api-read` fundamental:

1. **Get workspace info**: `team.info` API call. Note member count, workspace name, icon.
2. **List channels**: `conversations.list` API call. Count total channels, identify the most relevant channels by name and topic.
3. **Sample activity**: For the 3-5 most relevant channels, pull the last 100 messages. Calculate messages per day, unique posters per day, and average thread reply count.
4. **Check ICP density**: Read 50 recent messages. Count how many are from people matching your ICP (by job title in profile or content of messages).
5. **Check rules**: Look for #rules, #guidelines, or pinned messages in #general. Note any restrictions on self-promotion, link sharing, or vendor participation.

For each Discord server, using the `discord-api-read` fundamental (where bot access is available):

1. **Get server info**: Note member count, verification level, and server description.
2. **List channels**: Identify text channels and forum channels relevant to your expertise.
3. **Sample activity**: Pull the last 100 messages from the 3-5 most relevant channels. Calculate activity metrics.
4. **Check ICP density**: Read member roles and recent message content to assess ICP fit.
5. **Check rules**: Read #rules or #welcome channel for community guidelines.

For communities where API access is not possible, manually evaluate by joining and observing for 48 hours.

### 4. Score and rank

Score each community (0-50) on five dimensions:

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| ICP fit | 30% | 0=no ICP presence, 5=majority matches ICP, 15=dedicated ICP community |
| Activity level | 25% | 0=dead, 5=weekly activity, 12.5=daily active discussions |
| Engagement quality | 20% | 0=announcements only, 5=shallow chat, 10=deep technical discussions |
| Accessibility | 15% | 0=invite-only/paid, 3=application, 7.5=open join |
| Competition saturation | 10% | 5=no vendors, 3=some vendors, 0=saturated with vendor spam |

Sort by total score. Select:
- **Primary (3-5 communities, score 35+):** Daily engagement
- **Secondary (5-8 communities, score 25-34):** 2-3x per week, test for promotion
- **Watch list (remaining):** Monitor only via keyword alerts

### 5. Build engagement profiles

For each selected community, produce:

```markdown
## {Community Name} Engagement Profile

- **Platform**: Slack / Discord
- **Members**: X | **Daily active**: ~Y
- **Score**: XX/50
- **Join URL**: {url}
- **Cost**: Free / $X per month
- **Key channels**: #{channel1} (topic), #{channel2} (topic), #{channel3} (topic)
- **Rules summary**: [no self-promo / links OK in #showcase / vendor intros in #introductions]
- **Peak activity hours (UTC)**: [when messages get the most engagement]
- **Recurring events**: [weekly AMAs, monthly demos, daily standups]
- **Top contributors**: [3-5 regulars who set the tone — note their roles and topics]
- **Competitor presence**: [none / low / moderate / saturated]
- **Your angle**: [specific expertise gap you can fill]
- **First 5 interactions plan**: [specific messages/threads you would engage with]
```

### 6. Store in CRM

Using the `attio-lists` fundamental, create an Attio list called "Slack/Discord Community Targets" with entries for each community. Include score, platform, tier (primary/secondary/watch), key channels, and the engagement profile as structured fields.

## Output

- Ranked list of 10-15 target Slack/Discord communities with engagement profiles
- Attio list with community targets and metadata
- Three keyword lists (pain-point, category, ICP identity) for use in monitoring
- Join URLs and access instructions for each community

## Triggers

- Run once at play start
- Re-run quarterly or when ICP changes
- Ad-hoc when a new relevant community is discovered
