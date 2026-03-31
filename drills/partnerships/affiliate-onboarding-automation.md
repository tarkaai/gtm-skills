---
name: affiliate-onboarding-automation
description: Automate affiliate onboarding, asset delivery, enablement, and activation tracking
category: Partnerships
tools:
  - n8n
  - Attio
  - Loops
  - Rewardful
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-crm-integration
  - n8n-email-integration
  - attio-automation
  - attio-contacts
  - loops-sequences
  - affiliate-link-generation
  - posthog-custom-events
---

# Affiliate Onboarding Automation

This drill builds the n8n automation layer that takes a new affiliate from "interested" to "generating referrals" without manual work. It handles account creation, asset delivery, enablement drip, and activation tracking. Without this automation, onboarding becomes the bottleneck once you recruit more than 10 partners.

## Input

- Affiliate program configured (from `affiliate-program-design`)
- Onboarding kit assets stored in an accessible location (Google Drive, Notion, or hosted URLs)
- n8n instance configured with Attio, Loops, Rewardful/FirstPromoter, and PostHog integrations

## Steps

### 1. Build the new-affiliate onboarding workflow

Using the `n8n-workflow-basics` and `n8n-triggers` fundamentals, create an n8n workflow:

- **Trigger**: Attio webhook fires when a partner record's status changes to "Onboarding"
- **Action 1**: Create affiliate account in Rewardful/FirstPromoter using `affiliate-link-generation` API call. Store the returned affiliate ID and tracking link back in Attio.
- **Action 2**: Send welcome email via Loops with:
  - Their unique affiliate link
  - Link to the partner portal
  - Partner agreement (accept by clicking link)
  - Quick-start guide: "3 steps to your first referral"
- **Action 3**: Fire PostHog event `affiliate_onboarded` with properties: `affiliate_id`, `partner_type` (reseller/affiliate/customer), `source` (cold_outreach/warm_intro/inbound)
- **Action 4**: Update Attio status to "Onboarded — Awaiting Activation"

### 2. Build the enablement drip sequence

Using the `loops-sequences` fundamental, create a Loops sequence triggered by the `affiliate_onboarded` event:

- **Day 0**: Welcome + affiliate link + quick-start guide
- **Day 2**: "Your marketing toolkit" — attach approved copy (email blurbs, social posts, blog snippets). Explain how to use each format.
- **Day 5**: "How our top partners promote" — share 2-3 examples of successful affiliate promotions (anonymized or with permission). Include screenshot of a partner portal showing earnings.
- **Day 10**: "Have you shared your link yet?" — gentle nudge. If they haven't generated any clicks, offer a 15-minute strategy call. If they have clicks but no conversions, share tips for converting traffic.
- **Day 21**: "How's it going?" — check in. If they've generated a referral, celebrate. If not, ask what's blocking them and offer help.

### 3. Build the activation tracking workflow

Using the `n8n-triggers` and `posthog-custom-events` fundamentals, create workflows that track partner activation milestones:

**First click detection:**
- **Trigger**: Rewardful/FirstPromoter webhook fires when an affiliate link is clicked for the first time
- **Action**: Fire PostHog event `affiliate_first_click`. Update Attio: "First Click Date" = today. If within 7 days of onboarding, mark partner as "Fast Activator."

**First referral detection:**
- **Trigger**: Rewardful/FirstPromoter webhook fires when a referral converts (signup or purchase)
- **Action**: Fire PostHog event `affiliate_first_referral`. Update Attio status to "Active." Send congratulations email via Loops with their earnings update. Post notification to Slack.

**Stale partner detection:**
- **Trigger**: n8n cron, weekly
- **Action 1**: Query Attio for partners with status "Onboarded — Awaiting Activation" where onboard date > 30 days ago
- **Action 2**: For partners with zero clicks after 30 days: send a re-engagement email ("Need help getting started? Here are 3 easy ways to share your link.")
- **Action 3**: For partners with zero clicks after 60 days: update status to "Dormant." Remove from enablement sequences. Add to quarterly re-engagement list.

### 4. Build the partner asset delivery workflow

Using the `n8n-crm-integration` fundamental, create a workflow that auto-delivers assets when Attio fields change:

- **Trigger**: Attio webhook on partner "Commission Tier" field change
- **Action**: If tier upgraded (Standard → Silver or Gold), send tier-specific perks email:
  - Silver: higher commission rate, early access to new features, dedicated Slack channel
  - Gold: custom landing page, co-branded content, quarterly strategy call

### 5. Build the onboarding health dashboard

Track onboarding funnel in PostHog:

- `affiliate_onboarded` → `affiliate_first_click` → `affiliate_first_referral`
- Measure: median time from onboarding to first click, first click to first referral
- Alert if onboarding-to-first-click median exceeds 14 days (onboarding kit may need improvement)
- Alert if activation rate (onboarded → active within 30 days) drops below 40%

## Output

- Zero-touch affiliate onboarding (account creation → welcome email → asset delivery)
- 21-day enablement drip sequence
- Activation milestone tracking with automated celebrations
- Stale partner detection and re-engagement
- Onboarding health metrics in PostHog

## Triggers

Build these workflows once at the start of Baseline level. They run continuously for every new affiliate. Review onboarding metrics monthly and update the enablement sequence based on what activated partners say helped most.
