---
name: newsletter-subscriber-growth
description: Automated workflows to grow newsletter subscriber base through cross-channel promotion, lead magnets, and referral mechanics
category: Content
tools:
  - Loops
  - n8n
  - PostHog
  - Clay
  - LinkedIn
fundamentals:
  - loops-audience
  - loops-broadcasts
  - loops-sequences
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
  - posthog-funnels
  - clay-people-search
  - linkedin-organic-posting
---

# Newsletter Subscriber Growth

This drill builds automated systems that continuously acquire new newsletter subscribers from multiple channels. It connects social content, website traffic, product signups, and referral mechanics into n8n workflows that route subscribers into Loops with proper segmentation and attribution.

## Input

- Loops account with newsletter configured and sending domain authenticated
- n8n instance for automation workflows
- PostHog tracking on your website and newsletter signup forms
- At least one active social media channel producing content (LinkedIn, Twitter/X)
- Clay account for enrichment of new subscribers

## Steps

### 1. Build the subscriber acquisition funnel in PostHog

Using the `posthog-custom-events` fundamental, implement these events on your signup forms and landing pages:

- `newsletter_signup_form_viewed` — properties: source_page, utm_source, utm_medium, utm_campaign
- `newsletter_signup_submitted` — properties: email_domain, source_page, utm_source, referrer_url
- `newsletter_signup_confirmed` — properties: email, subscriber_source, enrichment_complete

Using `posthog-funnels`, create a funnel: form_viewed -> submitted -> confirmed. Break down by utm_source to identify which channels produce subscribers and at what conversion rate.

### 2. Configure multi-channel signup capture in n8n

Using `n8n-workflow-basics` and `n8n-triggers`, build these acquisition workflows:

**Workflow A — Website signup:**
1. Webhook trigger from website signup form submission
2. Validate email format and reject disposable domains
3. Enrich the subscriber via Clay using `clay-people-search` (company, title, industry)
4. Create contact in Loops via `loops-audience` with properties: source=website, signup_date, company, title, industry
5. Fire `newsletter_signup_confirmed` event to PostHog
6. If enrichment reveals ICP match (title + company size match target), tag as "high-value-subscriber" in Loops

**Workflow B — Social-to-newsletter:**
1. Trigger: new LinkedIn/Twitter connection or DM that mentions the newsletter
2. Extract email from DM or profile
3. Add to Loops with source=social, platform=linkedin|twitter
4. Send welcome email via `loops-sequences` with social-specific onboarding (reference the content they engaged with)

**Workflow C — Product signup cross-sell:**
1. Trigger: new user signup in your product (webhook from product backend)
2. Check if user is already a newsletter subscriber in Loops
3. If not subscribed, add with source=product, plan_type, signup_date
4. Tag with product usage properties for personalized newsletter content

### 3. Build a lead magnet delivery system

Create high-value gated content that requires email signup:

1. Identify your top 3 newsletter issues by engagement rate (from PostHog data)
2. Package each into a downloadable resource: a cheat sheet, checklist, or template derived from the newsletter content
3. Build n8n workflows that: accept form submission, deliver the resource via email (using `loops-sequences`), and add the subscriber to the newsletter list with source=lead-magnet, resource_name

### 4. Implement a referral program

Build a subscriber-brings-subscriber mechanism:

1. Generate unique referral links for each subscriber. Store the referral code in Loops contact properties.
2. Using `n8n-triggers`, create a webhook that fires when a new subscriber signs up with a referral parameter.
3. Credit the referring subscriber by updating their Loops contact: referral_count += 1.
4. At referral milestones (3, 10, 25 referrals), trigger a reward email via `loops-sequences`: exclusive content, early access to issues, or a direct call with the founder.
5. Track referral-sourced subscribers separately in PostHog to measure viral coefficient.

### 5. Automate social promotion of each issue

Using `linkedin-organic-posting` and `n8n-workflow-basics`:

1. After each newsletter issue is sent (triggered by Loops webhook), extract the top insight or stat from the issue.
2. Generate a LinkedIn post teasing that insight with a CTA to subscribe for the full content.
3. Queue the post for publishing 2-4 hours after the newsletter sends (so existing subscribers see it first, then social followers feel FOMO).
4. Track clicks from the promotional post to the signup page via UTM parameters.

### 6. Monitor growth metrics

Track these subscriber growth KPIs weekly in PostHog:

- Net new subscribers per week (gross signups minus unsubscribes)
- Subscriber growth rate (% week over week)
- Acquisition cost per subscriber by channel (factor in any paid promotion)
- Subscriber-to-lead conversion rate (how many subscribers become qualified leads)
- Referral coefficient: referral-sourced subscribers / total new subscribers

Set alerts: if net new subscribers drops below 50% of 4-week average, trigger an investigation workflow.

## Output

- Multi-channel subscriber acquisition funnels automated in n8n
- Lead magnet delivery system for gated content conversion
- Referral program tracking and reward automation
- Social cross-promotion of each newsletter issue
- Weekly subscriber growth metrics in PostHog

## Triggers

Acquisition workflows run continuously via webhooks. Social promotion triggers after each newsletter send. Growth metrics are computed weekly via n8n cron job.
