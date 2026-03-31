---
name: media-relationship-automation
description: Automate journalist opportunity detection, relationship nurture, and reactive PR responses at scale
category: Media
tools:
  - n8n
  - Mention
  - Qwoted
  - Featured.com
  - Attio
  - Clay
  - Anthropic Claude API
fundamentals:
  - media-monitoring-api
  - media-database-search
  - media-pitch-email
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - attio-contacts
  - attio-notes
---

# Media Relationship Automation

This drill builds always-on automation that detects PR opportunities, nurtures journalist relationships, and enables reactive pitching at scale. Instead of batched manual outreach, this creates a continuous pipeline of earned media opportunities that the agent monitors, evaluates, and acts on.

## Input

- Active media target list in Attio (from `media-target-research` drill)
- Brand monitoring configured (from `media-monitoring-api` fundamental)
- Pitch angles and press kit (from `media-pitch-outreach` drill)
- n8n instance for automation workflows
- Anthropic API key for Claude (pitch drafting and opportunity evaluation)

## Steps

### 1. Build the opportunity detection pipeline

Create an n8n workflow that aggregates PR opportunities from multiple sources:

**Source 1 -- Journalist source requests (Qwoted + Featured.com):**
1. Forward Qwoted and Featured.com email alerts to a monitored inbox
2. n8n Email Trigger node: parse each alert for topic, journalist name, outlet, deadline, and requirements
3. Claude API node: evaluate if the request matches your expertise areas (relevance score 1-5)
4. If relevance >= 3: draft a response using Claude with your founder's voice, expertise, and relevant data points
5. Route draft to Slack #pr-opportunities channel with the original request, drafted response, and deadline
6. **Human action required:** Review and approve the response before submitting

**Source 2 -- Brand and competitor mentions (Mention API):**
1. n8n webhook receiving Mention API alerts
2. Classify each mention: positive / neutral / negative / competitor_coverage
3. For positive mentions: log in Attio, share on social, thank the journalist
4. For competitor mentions: flag the outlet as a pitch target. If the journalist covered a competitor, draft a pitch offering your perspective as an alternative
5. For negative mentions: alert team immediately in Slack for response

**Source 3 -- Trending topic detection:**
1. n8n cron job (daily, 8am): query Mention API for your industry keywords, sorted by velocity (mentions/hour)
2. Claude API: evaluate if any trending topic intersects with your pitch angles
3. If match found: draft a reactive pitch tied to the trend. Include: the trend, your unique angle, and specific data/insight you can offer
4. Route to Slack #pr-opportunities with urgency flag (trending topics have a 24-48 hour window)

### 2. Automate journalist relationship tracking

Build an Attio-based relationship management system:

**Contact enrichment on a schedule:**
1. n8n cron (monthly): for each journalist in your media target list, check if they have changed outlets (Clay enrichment refresh)
2. If outlet change detected: update Attio record and evaluate if they are still a relevant target at their new outlet
3. If journalist published about your topic recently: flag for fresh pitch

**Engagement tracking:**
Track every interaction with each journalist in Attio notes:
- Pitches sent (date, angle, outcome)
- Placements earned (date, URL, traffic impact)
- Responses to their source requests (date, whether selected)
- Social interactions (when you engaged with their content)

Use Attio's timeline to see full relationship history before pitching.

**Relationship health scoring:**
Assign each journalist a relationship score in Attio:
- 0: No prior interaction
- 1: Pitched, no response
- 2: Pitched, received positive response but no placement
- 3: One placement secured
- 4: Multiple placements, journalist reaches out proactively
- 5: Ongoing relationship, mutual value exchange

Focus outreach effort on scoring 0-2 contacts up to 3+.

### 3. Build the reactive pitch workflow

When a PR opportunity is detected (trending topic, journalist request, competitor coverage), execute:

1. **Evaluate fit** (automated): Claude API scores the opportunity on relevance (1-5), urgency (hours until window closes), and effort (low/medium/high)
2. **Draft pitch** (automated): Claude generates a personalized pitch using the `media-pitch-email` template, populated with the specific opportunity context and the journalist's history from Attio
3. **Route for approval** (to Slack): post the draft with context: opportunity type, target journalist, deadline, relevance score, and the drafted pitch
4. **Human action required:** Founder reviews, edits, and approves. For high-urgency opportunities (deadline < 24 hours), the Slack message includes a one-click "Approve and Send" button connected to n8n
5. **Send and log** (automated on approval): send via Instantly or Gmail API, log in Attio with full context

### 4. Automate post-placement amplification

When a placement is logged in Attio (status = "published"):

1. n8n detects the status change
2. Automatically generate social media posts for LinkedIn and Twitter/X promoting the coverage
3. Route social posts to Slack for approval
4. On approval: schedule posts via Buffer/Typefully
5. Add the placement to your website press page (via CMS API)
6. Include in next email newsletter draft (log for newsletter-pipeline drill)
7. Send a thank-you message to the journalist (drafted by Claude, reviewed by human)
8. Add referral tracking UTMs to monitor traffic from the placement

### 5. Build the monthly media report

n8n cron workflow (first Monday of month):

1. Pull all media activity from Attio: pitches sent, replies received, placements published, relationship scores
2. Pull referral traffic data from PostHog for all placement URLs
3. Claude API generates a monthly PR report:

```
Report structure:
- Executive summary: placements this month, referral traffic, leads from PR
- Placement log: each placement with outlet, date, URL, traffic, and leads
- Pipeline: pitches outstanding, opportunities in review
- Relationship health: journalists by score tier, who to nurture next
- Opportunity log: source requests answered, win rate
- Recommendations: which angles are working, which outlets to prioritize, new targets to add
```

4. Post to Slack and store in Attio

## Output

- Always-on PR opportunity detection across 3 sources (journalist requests, brand mentions, trending topics)
- Automated pitch drafting for reactive PR opportunities
- Journalist relationship tracking with health scores in Attio
- Post-placement amplification workflow
- Monthly PR performance reports

## Triggers

- Opportunity detection: continuous (real-time webhooks + daily cron)
- Relationship enrichment refresh: monthly
- Monthly report: first Monday of each month
- Reactive pitch workflow: triggered by opportunity detection
