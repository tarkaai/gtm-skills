---
name: guest-post-outreach-automation
description: Automate guest post blog discovery, pitch generation, sending, and follow-up via n8n workflows
category: GuestPosting
tools:
  - n8n
  - Ahrefs
  - Clay
  - Instantly
  - Anthropic
  - Attio
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - n8n-error-handling
  - ahrefs-content-explorer
  - ahrefs-backlink-analysis
  - clay-table-setup
  - clay-enrichment-waterfall
  - instantly-campaign
  - ai-guest-post-drafting
  - attio-lists
  - attio-contacts
---

# Guest Post Outreach Automation

This drill builds n8n workflows that automate the guest post discovery-to-pitch pipeline. It handles continuous blog discovery, automatic pitch generation, personalized email sending, follow-up sequences, and reply routing. This is the 10x multiplier that takes guest posting from 10-15 pitches/week (manual) to 50-100 pitches/week (automated with human quality gates).

## Input

- Working `guest-post-blog-discovery` and `guest-post-pitch-outreach` drills completed manually at least once (you need baseline data on what works)
- n8n instance running and connected to: Ahrefs API, Clay API, Instantly API, Anthropic API, Attio API
- Niche keyword list (10-20 terms)
- Pitch template library: 5-7 proven pitch templates from Baseline level results
- Author credentials and content pillars

## Steps

### 1. Build the blog discovery workflow (n8n)

Create an n8n workflow triggered by weekly cron (every Monday, 6am UTC):

**Nodes:**

1. **Cron Trigger**: Weekly schedule
2. **Ahrefs Content Explorer**: Loop through niche keywords with guest post search queries from `guest-post-blog-discovery`. Use `ahrefs-content-explorer` for each query variant. Filter: DR >= 30, organic_traffic >= 500.
3. **Deduplicate**: Compare results against existing Attio blog targets. Remove domains already in the pipeline.
4. **Clay Push**: Push new blog domains to Clay using `clay-table-setup`. Trigger enrichment waterfall for editor contacts.
5. **Enrichment Wait**: Pause workflow for 2 hours (Clay enrichment processing time).
6. **Clay Pull**: Retrieve enriched data including editor email, LinkedIn, blog topics.
7. **Score and Tier**: Apply scoring formula (DR 30%, relevance 30%, traffic 20%, accessibility 10%, competitor 10%). Assign tier_1 / tier_2 / tier_3.
8. **Attio Push**: Push scored, enriched blogs to Attio list using `attio-lists`.
9. **Slack Notification**: Post summary to Slack: "Found {{count}} new guest post targets this week. {{tier_1_count}} Tier 1, {{tier_2_count}} Tier 2."

**Error handling** via `n8n-error-handling`:
- Ahrefs rate limit (429): retry after 60s, max 3 retries
- Clay enrichment failure: skip row, log to error table, continue
- Attio push failure: retry once, then log error

### 2. Build the pitch generation workflow (n8n)

Create an n8n workflow triggered by new Attio records (when blogs move to "ready_to_pitch" status):

**Nodes:**

1. **Attio Webhook**: Triggered when a blog record enters "ready_to_pitch" status
2. **Pull Blog Context**: Fetch from Clay: recent articles, topics, editor name, editorial guidelines URL
3. **Scrape Guidelines**: HTTP Request node to fetch the blog's "write for us" page. Extract: preferred topics, word count requirements, submission process.
4. **Generate Pitch Angles**: Call Anthropic API using `ai-guest-post-drafting` (pitch angle generation mode). Input: blog audience, recent topics, content gaps, author expertise. Output: 3 ranked pitch ideas.
5. **Select Best Pitch**: Pick the top-ranked pitch angle. If the blog has published a competitor guest post, select the angle most differentiated from that competitor's content.
6. **Generate Pitch Email**: Use the pitch email template from `guest-post-pitch-outreach`, populate merge fields from Clay data and generated pitch angle.
7. **Human Review Gate (Tier 1 only)**: If blog is tier_1, send the draft pitch to Slack for human approval before sending. Wait for approval webhook. If tier_2 or tier_3, proceed automatically.
8. **Queue in Instantly**: Push the personalized pitch to Instantly campaign queue using `instantly-campaign`. Set follow-up after 7 days.
9. **Update Attio**: Set blog status to "pitched" with pitch date and angle used.

### 3. Build the reply routing workflow (n8n)

Create an n8n workflow triggered by Instantly reply webhook:

**Nodes:**

1. **Instantly Webhook**: Fires when a reply is detected
2. **Classify Reply**: Call Anthropic API to classify the reply into categories: `accepted` (send draft/outline), `interested` (wants more info), `redirected` (different topic), `declined`, `paused` (not now), `auto_reply`
3. **Route by classification**:
   - `accepted`: Update Attio status. Send Slack alert: "Guest post accepted at {{blog_name}}! Topic: {{topic}}". Trigger `guest-post-article-pipeline` drill.
   - `interested`: Generate a response with the requested information (outline, samples, credentials). Send via Instantly reply.
   - `redirected`: Generate a new pitch for the suggested topic. Queue for human review.
   - `declined`: Update Attio status to "declined". Set 6-month re-approach reminder.
   - `paused`: Update Attio with re-approach date. Set reminder.
   - `auto_reply`: Ignore. Wait for real reply.
4. **Update Attio**: Log classification, reply content, and next action for every reply.

### 4. Build the competitor monitoring workflow (n8n)

Create an n8n workflow triggered by weekly cron:

**Nodes:**

1. **Cron Trigger**: Weekly (Friday, 6am UTC)
2. **Ahrefs Backlink Check**: For each competitor, use `ahrefs-backlink-analysis` to pull new backlinks from the last 7 days. Filter to editorial/blog domains (exclude forums, directories, social media).
3. **Identify New Guest Posts**: Filter backlinks where: source domain DR >= 30, anchor text contains competitor brand or author name, URL path contains "/blog/" or "/articles/".
4. **Cross-Reference**: Check if the source blog is already in your target list. If not, add it.
5. **Generate Pitch**: For new blogs with competitor guest posts, generate a differentiated pitch angle via Anthropic API. Feed context: what the competitor wrote about + a unique angle you can offer.
6. **Queue for Outreach**: Push to the pitch generation workflow (step 2) with a "competitor_response" tag.
7. **Slack Summary**: Post weekly competitor guest posting activity summary.

### 5. Configure guardrails

Set these guardrails in n8n:

- **Daily send limit**: Maximum 15 new pitches per day across all sending accounts
- **Per-blog cooldown**: Minimum 90 days between pitches to the same blog
- **Quality gate**: Tier 1 blogs always require human approval before pitch sends
- **Reply SLA**: Accepted pitches trigger a Slack alert within 5 minutes. Draft must be submitted within 72 hours.
- **Error budget**: If pitch-to-reply rate drops below 10% for 2 consecutive weeks, pause all automated pitching and alert team for pitch quality review
- **Deduplication**: Never pitch the same topic to the same blog. n8n checks Attio history before queuing.

## Output

- Weekly automated blog discovery adding new targets to the pipeline
- Automated pitch generation and sending with tier-based quality gates
- Reply classification and routing with appropriate follow-up actions
- Competitor guest post monitoring with counter-pitch generation
- Guardrails preventing over-pitching and quality degradation

## Triggers

- Blog discovery: weekly cron
- Pitch generation: event-driven (new "ready_to_pitch" records)
- Reply routing: event-driven (Instantly reply webhook)
- Competitor monitoring: weekly cron
