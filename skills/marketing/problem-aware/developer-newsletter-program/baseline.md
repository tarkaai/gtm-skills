---
name: developer-newsletter-program-baseline
description: >
  Developer Newsletter — Baseline Run. Run the newsletter as an always-on weekly cadence with
  automated tracking, content repurposing, and subscriber segmentation. Validate that results
  hold over 8 consecutive issues.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Email, Content"
level: "Baseline Run"
time: "18 hours over 8 weeks"
outcome: ">=500 subscribers and >=12 qualified leads from first 8 issues over 8 weeks"
kpis: ["Open rate", "Click rate", "Reply rate", "Subscriber growth rate", "Leads per issue", "Unsubscribe rate"]
slug: "developer-newsletter-program"
install: "npx gtm-skills add marketing/problem-aware/developer-newsletter-program"
drills:
  - newsletter-pipeline
  - posthog-gtm-events
  - content-repurposing
---

# Developer Newsletter — Baseline Run

> **Stage:** Marketing > Problem Aware | **Motion:** Founder Social Content | **Channels:** Email, Content

## Outcomes

Run 8 consecutive weekly newsletter issues with full analytics tracking. Grow to >=500 subscribers via cross-channel promotion and content repurposing. Generate >=12 qualified leads (1-2 per issue average). Prove the cadence is sustainable and results are repeatable, not a Smoke Test fluke.

## Leading Indicators

- Subscriber growth rate >=10% week-over-week for the first 4 weeks
- Open rate stabilizes at >=30% (does not decay as the list grows)
- At least 2 replies per issue on average (consistent engagement, not one-off)
- Content repurposing drives >=20% of new subscribers from social channels
- Click rate >=5% on in-issue links consistently

## Instructions

### 1. Set up the analytics tracking layer

Run the `posthog-gtm-events` drill to implement the newsletter event taxonomy in PostHog:

**Events to implement:**
- `newsletter_issue_sent` — properties: issue_number, subject_line, subject_style (question/data/contrarian/how-to), content_pillar, word_count, link_count, send_time
- `newsletter_issue_opened` — properties: subscriber_id, issue_number, device_type, open_delay_hours
- `newsletter_link_clicked` — properties: subscriber_id, issue_number, link_url, link_position (1st/2nd/3rd), content_type (tutorial/tool/repo/blog)
- `newsletter_reply_received` — properties: subscriber_id, issue_number, sentiment (positive/negative/question), buying_signal (true/false)
- `newsletter_subscriber_added` — properties: source (website/social/referral/product), acquisition_date
- `newsletter_subscriber_churned` — properties: issues_received, last_opened_issue, churn_type (unsubscribe/bounce)

Connect Loops webhooks to n8n to fire these events into PostHog automatically. Every newsletter action should be tracked without manual logging.

**Build the attribution funnel in PostHog:**
newsletter_issue_sent -> newsletter_issue_opened -> newsletter_link_clicked -> page_visited -> lead_captured -> meeting_booked

Break down by content_pillar and subject_style to identify which combinations drive leads.

### 2. Build the content repurposing engine

Run the `content-repurposing` drill to multiply each newsletter issue into 3-5 additional content pieces:

**Per-issue repurposing workflow:**
1. After writing each newsletter issue, extract 2-3 standalone insights or code snippets
2. Transform each into a LinkedIn post using the social content format: hook line referencing a specific problem, 150-250 word body expanding on the insight, CTA = "I covered this in depth in this week's newsletter — subscribe link"
3. Transform the tutorial/code section into a standalone blog post or GitHub gist for SEO
4. If the issue references a framework or decision matrix, create a visual (diagram, flowchart) for social sharing
5. Schedule the social derivatives across the week: newsletter sends Tuesday, LinkedIn derivatives post Wednesday, Thursday, and Friday

**Attribution requirement:** Every social post promoting the newsletter must use UTM parameters: `?utm_source=linkedin&utm_medium=social&utm_campaign=dev-newsletter&utm_content=issue-{N}`

### 3. Implement subscriber segmentation

Using the `newsletter-pipeline` drill, enhance Loops segmentation beyond Smoke level:

**Segments to create:**
- "highly-engaged" — opened last 3 issues AND clicked at least 1 link. These subscribers get earlier access to content or bonus material.
- "warm-leads" — clicked a product-related link or replied with a buying signal. These get tracked in Attio as marketing qualified leads.
- "at-risk" — did not open the last 2 issues. These get a re-engagement email after Issue 4: "Still interested? Here's what you missed" with links to top-performing issues.
- "by-source" — segment by acquisition source (website, social, referral) to analyze which sources produce the most engaged subscribers.

### 4. Execute the 8-issue content calendar

Plan all 8 issues in advance. Rotate through content pillars systematically:

**Issue planning template (per issue):**
- Content pillar (rotate: tutorial -> industry -> behind-the-scenes -> curated)
- Subject line style (rotate through styles tested in Smoke, plus new variants)
- Main topic (selected from ICP pain points and topics that performed well in Smoke)
- CTA type (reply-ask, resource-link, meeting-book — rotate based on what converted in Smoke)
- Code example or technical artifact included (yes/no — track in PostHog to measure impact)

**Writing cadence:**
- Friday: research and outline next issue
- Monday: agent drafts the issue based on outline, pillar, and subject line style
- Tuesday morning: founder reviews, adds personal anecdotes, approves
- Tuesday 9-10am: send via Loops
- Tuesday-Wednesday: agent repurposes into social content
- Wednesday-Friday: publish social derivatives

**Human action required:** Founder reviews and edits each draft before send. Founder responds personally to replies with buying signals.

### 5. Track and analyze weekly

After each issue (48 hours post-send), pull metrics from Loops and PostHog:

| Metric | Target | Action if below target |
|--------|--------|----------------------|
| Open rate | >=30% | Test different subject line styles next issue |
| Click rate | >=5% | Improve link placement, add more code/actionable links |
| Reply rate | >=1% | Add a specific question at the end of each issue |
| Unsubscribe rate | <0.5% | Content-audience mismatch — survey unsubscribers |
| New subscribers this week | >=50 | Increase social promotion, add more CTAs to blog posts |
| Qualified leads this issue | >=1 | Strengthen product-adjacent CTAs |

Log each issue's metrics in Attio on the newsletter campaign record. After Issue 4, identify the top-performing content pillar and subject line style — lean into winners for Issues 5-8.

### 6. Evaluate against threshold

Run the `threshold-engine` drill after Issue 8:
- Check: total subscriber count >= 500
- Check: total qualified leads >= 12 across 8 issues
- Check: average open rate >= 28% (slight decay from Smoke is acceptable as list grows)
- Check: subscriber growth rate still positive (not plateauing)
- Check: at least 2 content pillars consistently produce engagement (not over-reliant on one topic)

**PASS:** All criteria met. The newsletter is a sustainable, repeatable channel. Proceed to Scalable.
**FAIL:** Diagnose: if subscriber growth stalled, social promotion or referral mechanics need work. If leads are low but engagement is high, CTAs need sharpening. If open rates decayed significantly, list hygiene or subject line strategy needs attention. Iterate and run 4 more issues.

## Time Estimate

- Analytics setup and tracking implementation: 2 hours
- Content repurposing system setup: 2 hours
- Subscriber segmentation configuration: 1 hour
- Writing and editing 8 issues (1.5 hours each): 12 hours
- Weekly analysis and threshold evaluation: 1 hour
- **Total: 18 hours over 8 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Newsletter sending, segmentation, subscriber management | Free up to 1,000 contacts; Starter $49/mo for 5,000 — https://loops.so/pricing |
| PostHog | Event tracking, funnels, attribution analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Attio | CRM for lead tracking and campaign logging | Free tier or $29/user/mo — https://attio.com/pricing |
| Clay | Subscriber enrichment for lead qualification | Free tier for 100 credits/mo; Pro $149/mo — https://clay.com/pricing |

**Play-specific cost: ~$50-100/mo** (Loops Starter plan if list exceeds 1,000 subscribers)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `newsletter-pipeline` — manage the Loops configuration, segments, and sending cadence
- `posthog-gtm-events` — implement the full newsletter event taxonomy for attribution
- `content-repurposing` — multiply each issue into social and blog derivatives
