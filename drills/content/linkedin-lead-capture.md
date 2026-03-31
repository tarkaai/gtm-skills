---
name: linkedin-lead-capture
description: Systematically convert LinkedIn content engagement into CRM leads and pipeline
category: Content
tools:
  - LinkedIn
  - Attio
  - Clay
  - n8n
  - PostHog
fundamentals:
  - linkedin-organic-dms
  - linkedin-organic-analytics
  - attio-contacts
  - clay-people-search
  - clay-enrichment-waterfall
  - posthog-custom-events
  - n8n-workflow-basics
---

# LinkedIn Lead Capture

This drill builds the system that turns LinkedIn content engagement into tracked, enriched leads in your CRM. It covers identifying lead signals, enriching contacts, routing them into your pipeline, and measuring content-to-pipeline attribution.

## Input

- Active LinkedIn posting cadence (from `founder-linkedin-content-batch` drill)
- Engagement data from LinkedIn (from `linkedin-engagement-workflow` drill)
- CRM configured with lead stages (Attio or equivalent)
- Clay table for enrichment

## Steps

### 1. Define lead signals from LinkedIn engagement

Not every like or comment is a lead. Define your signal hierarchy:

| Signal | Intent Level | Action |
|--------|-------------|--------|
| DM asking about your product | Very High | Respond immediately, offer call |
| Comment describing a problem you solve | High | DM them, log as lead |
| Connection request with relevant note | High | Accept, send welcome DM, log |
| Multiple post engagements from same person | Medium | Research them, DM if ICP match |
| Profile view from ICP-matching title | Medium | Send connection request with note |
| Single like from ICP match | Low | Add to watch list, engage with their content |

### 2. Set up daily lead capture workflow

**Manual process (Smoke/Baseline levels):**

Each day after engagement workflow, review:
1. New DMs received (check LinkedIn inbox)
2. Comments on today's post with buying signals
3. Connection requests with notes
4. Profile viewers matching ICP (LinkedIn shows last 90 days of viewers in Creator Mode)

For each lead, record in a spreadsheet or directly in Attio:
- Name, title, company, LinkedIn URL
- Signal type (DM, comment, connection, profile view)
- Which post triggered the engagement
- Next action (DM sent, call scheduled, nurture)

**Automated process (Scalable/Durable levels):**

Using the `n8n-workflow-basics` fundamental, build a workflow:

1. **Trigger**: Daily schedule (9am) or webhook from Taplio when new engagement is detected
2. **Fetch engagement data**: Using `linkedin-organic-analytics` fundamental, pull yesterday's post engagement via Taplio/Shield API
3. **Filter for lead signals**: Check each engager against ICP criteria (title contains VP/Head/Director/CEO/CTO/Founder + company size > 10 employees)
4. **Enrich via Clay**: Using `clay-people-search` and `clay-enrichment-waterfall` fundamentals, send matching profiles to Clay for enrichment (email, company data, tech stack)
5. **Create CRM record**: Using `attio-contacts` fundamental, create lead in Attio with all enriched data + source attribution
6. **Log event in PostHog**: Using `posthog-custom-events` fundamental:
   ```
   posthog.capture('linkedin_lead_captured', {
     source: 'linkedin-content',
     signal_type: 'comment|dm|connection|profile_view',
     post_url: '{URL of triggering post}',
     lead_title: '{their job title}',
     lead_company: '{their company}'
   })
   ```
7. **Notify founder**: Send Slack message or email with the lead's details and recommended next action

### 3. Build content-to-pipeline attribution

Track the full journey from post to pipeline:

1. **Post published** -> `linkedin_post_published` event in PostHog (track: post URL, topic pillar, format)
2. **Engagement received** -> `linkedin_engagement_received` event (track: post URL, engagement type, engager title)
3. **Lead captured** -> `linkedin_lead_captured` event (track: post URL, signal type, lead details)
4. **Meeting booked** -> `linkedin_meeting_booked` event (track: lead name, source post, days from first engagement to meeting)
5. **Deal created** -> `linkedin_deal_created` event (track: lead name, deal value, source post)

This chain lets you answer: "Which content pillars produce the most pipeline?" and "What's the average time from first post engagement to meeting booked?"

### 4. Weekly lead review

Every Friday, review the week's LinkedIn leads:
- Total leads captured this week
- Leads by signal type (DM vs comment vs connection vs profile view)
- Leads by content pillar (which topics produce the most leads)
- Conversion: leads -> meetings booked -> deals created
- Compare to threshold (Smoke: 3/week, Baseline: 2-3/week, Scalable: 2-3/week sustained)

Update content strategy based on findings: double down on pillars that produce leads, retire topics that get engagement but no leads.

## Output

- All LinkedIn engagement signals captured and categorized daily
- High-intent leads enriched and added to CRM with source attribution
- PostHog events flowing for content-to-pipeline attribution
- Weekly lead review with content performance insights
- n8n automation routing leads (at Scalable+ levels)

## Triggers

Run daily (manual at Smoke/Baseline, automated at Scalable/Durable). Weekly review every Friday. Time investment: 15-20 minutes daily manual, <5 minutes daily automated.
