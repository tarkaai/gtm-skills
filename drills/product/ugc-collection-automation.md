---
name: ugc-collection-automation
description: Automate collection, moderation, and cataloging of user-generated content from in-product submissions and external platforms
category: Product
tools:
  - n8n
  - PostHog
  - Attio
  - Anthropic
  - Intercom
  - Loops
fundamentals:
  - ugc-submission-webhook
  - ugc-moderation-api
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - posthog-custom-events
  - attio-contacts
  - attio-notes
  - attio-lists
  - loops-transactional
---

# UGC Collection Automation

This drill builds the always-on pipeline that collects user-generated content from all sources (in-product forms, social mentions, community posts, review sites), moderates it via AI, catalogs it in the CRM, and triggers the appropriate follow-up with the creator. The output is a continuously growing library of approved UGC ready for amplification.

## Prerequisites

- UGC submission webhook deployed (run `ugc-submission-webhook` fundamental)
- UGC prompts designed and active (run `ugc-prompt-design` drill)
- Attio CRM with contact records
- n8n instance for automation
- Anthropic API key for AI moderation

## Steps

### 1. Build the core collection workflow in n8n

Create the master UGC processing workflow:

**Trigger:** `ugc-submission-webhook` receives a submission (in-product form, email, or external detection)

**Step 1 — Enrich the submitter:**
Using `attio-contacts`, look up the submitter by email. Pull:
- Account name, plan tier, account age
- Power user score (if `power-user-scoring` drill is active)
- Advocacy tier (if `advocacy-program-design` drill is active)
- Previous UGC submissions (count and types)

**Step 2 — AI moderation:**
Using `ugc-moderation-api`, send the submission content for scoring. Receive quality, relevance, brand safety, amplification potential, and authenticity scores plus a verdict (approve/review/reject).

**Step 3 — Route based on verdict:**

- **Approve (composite >= 3.5):**
  1. Create an Attio note on the submitter's contact: "UGC Approved: [title] ([content_type]). Composite score: [X]. Suggested channels: [channels]."
  2. Add submitter to the "UGC Contributors" Attio list
  3. Fire PostHog event `ugc_approved` with all moderation scores
  4. Send a thank-you email via `loops-transactional`: "Thanks for sharing [title]! We love it and may feature it on our channels. We'll let you know."
  5. Queue the content for the amplification pipeline

- **Review (composite 2.5-3.5):**
  1. Create an Attio task: "Review UGC submission: [title] from [submitter_name]. AI scores: quality=[X], relevance=[X], brand_safety=[X]. Reason: [verdict_reason]."
  2. Fire PostHog event `ugc_review_queued`
  3. **Human action required:** Team member reviews within 48 hours and manually approves or rejects in Attio

- **Reject (composite < 2.5):**
  1. Fire PostHog event `ugc_rejected` with rejection reason
  2. Send a gracious email via `loops-transactional`: "Thanks for submitting [title]! We appreciate you thinking of us. Right now it's not quite the right fit for our content channels, but we'd love to see more from you in the future."
  3. Log the rejection in Attio notes (for pattern analysis)

### 2. Build the external content detection workflow

Using `n8n-scheduling`, create a daily workflow that discovers UGC posted on external platforms without using the submission form:

**Social monitoring (daily):**
1. Search Twitter/X for mentions of your product name, branded hashtags, or product URL
2. Search LinkedIn for posts mentioning your product (via `linkedin-organic-feed-search` if available, or Clay social search)
3. Search YouTube for new videos mentioning your product name
4. Search GitHub for new repositories or READMEs mentioning your product

**Community monitoring (daily):**
1. Check Slack/Discord community channels for tutorial-style messages, workflow shares, or "how I use [Product]" posts
2. Check Reddit for posts in relevant subreddits mentioning your product

**Review site monitoring (weekly):**
1. Check G2, Capterra, Product Hunt, and TrustRadius for new reviews
2. Check industry-specific review platforms relevant to your market

For each discovered piece of content:
1. POST to the `ugc-submission-webhook` with `platform` set to the source and `content_url` set to the permalink
2. The webhook deduplication check prevents reprocessing known content
3. The AI moderation evaluates the content
4. If approved, send a thank-you DM or reply to the creator: "We saw your [post/review/video] about [Product] -- thank you! Would you be okay with us sharing it?"

### 3. Build the UGC catalog in Attio

Create a structured UGC tracking system:

**Attio list: "UGC Library"**
Using `attio-lists`, create a list with these attributes:
- Title, content type, platform, URL
- Submitter (linked to contact record)
- Moderation scores (quality, relevance, amplification)
- Status: approved, amplified, featured, archived
- Channels used (social, blog, email, case study)
- Amplification date, impressions, clicks (populated later by amplification pipeline)

**Attio list: "UGC Contributors"**
Track all users who have contributed content:
- Contact link, total submissions, approved submissions
- Content types contributed
- Last submission date
- Contributor tier: first-timer, repeat (2-4), prolific (5+)

### 4. Build the creator engagement sequence

Using `loops-transactional`, create templates for each stage of the creator relationship:

**First submission thank-you:**
- Send immediately after approval
- Include: what you plan to do with their content, a link to view other UGC, an invitation to submit more

**Content featured notification:**
- Send when their content is amplified on your channels
- Include: where it was shared, any metrics (views, engagement), a social share link so they can amplify it too

**Repeat contributor recognition:**
- Send after 3rd approved submission
- Include: recognition ("You're one of our top contributors"), exclusive perk (early access, branded swag, or feature credit), invitation to a deeper collaboration (case study, webinar guest)

### 5. Track collection metrics

Fire PostHog events for the full collection pipeline:

| Event | Properties |
|-------|-----------|
| `ugc_submitted` | content_type, platform, submitter_tier |
| `ugc_moderated` | verdict, composite_score, processing_time_ms |
| `ugc_approved` | content_type, platform, amplification_score, suggested_channels |
| `ugc_review_queued` | content_type, verdict_reason |
| `ugc_rejected` | content_type, rejection_reason |
| `ugc_external_detected` | platform, content_type |
| `ugc_creator_thanked` | template_type, channel |

Build a PostHog funnel: `ugc_submitted` -> `ugc_moderated` -> `ugc_approved` -> (later) `ugc_amplified`

## Output

- Always-on UGC collection pipeline processing in-product and external submissions
- AI moderation with approve/review/reject routing
- UGC Library and Contributors lists in Attio
- External content detection workflow (social, community, review sites)
- Creator engagement email templates
- Full PostHog event tracking for the collection pipeline

## Triggers

The core collection workflow runs on every webhook submission (event-driven). External detection runs daily via n8n cron. Review site monitoring runs weekly. All workflows are always-on after initial setup.
