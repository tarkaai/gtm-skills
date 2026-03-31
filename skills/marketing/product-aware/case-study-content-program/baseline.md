---
name: case-study-content-program-baseline
description: >
  Case Study Content Program — Baseline Run. Scale to 10-12 case studies with an
  always-on candidate recruitment pipeline. Establish systematic production with
  PostHog event tracking, gated/ungated formats, and a case study hub. First
  always-on automation for identifying and recruiting case study candidates.
stage: "Marketing > ProductAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Baseline Run"
time: "35 hours over 8 weeks"
outcome: "≥ 2,000 total page views and ≥ 30 conversions across all case studies over 8 weeks"
kpis: ["Total page views across all case studies (target ≥ 2,000)", "Conversions from case study pages (target ≥ 30)", "Average time on page (target ≥ 3 min)", "Customer participation rate (target ≥ 30% of outreach)", "Case studies published (target 10-12)"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
drills:
  - case-study-creation
  - case-study-candidate-pipeline
  - posthog-gtm-events
---

# Case Study Content Program — Baseline Run

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Scale from 3 case studies to 10-12 covering different ICPs, industries, and use cases. Deploy an always-on candidate recruitment pipeline that identifies high-fit customers and runs automated outreach sequences. Establish detailed PostHog event tracking so every case study interaction is measured, and build a case study hub for discovery.

Pass: ≥ 2,000 total page views and ≥ 30 conversions across all case studies over 8 weeks, with average time on page ≥ 3 minutes.
Fail: < 2,000 page views or < 30 conversions after 8 weeks, or fewer than 8 case studies published.

## Leading Indicators

- The candidate pipeline surfaces 5+ qualified candidates with case_study_fit_score >= 70 in the first 2 weeks (the scoring model works and your user base has recruitable customers)
- At least 3 of the first 10 outreach sequences result in a scheduled interview (the recruitment messaging resonates)
- Gated PDF downloads convert at ≥ 15% of case study page visitors (the content is valuable enough to trade an email for)
- Case study hub filter usage exceeds 20% of visitors (visitors are looking for specific stories, not just browsing)
- At least 1 sales rep includes a case study in their outreach within the first 3 weeks (sales enablement value is evident)

## Instructions

### 1. Configure detailed event tracking

Run the `posthog-gtm-events` drill to set up a complete case study event taxonomy in PostHog. Define these events:

```
case_study_hub_viewed — visitor lands on the case study hub page
case_study_hub_filtered — visitor applies a filter (industry, use case, company size)
case_study_page_viewed — visitor opens a specific case study
case_study_scroll_depth — visitor scrolls to 25%, 50%, 75%, 100% of the page
case_study_cta_clicked — visitor clicks a CTA (demo, signup, contact)
case_study_pdf_downloaded — visitor downloads the gated PDF version
case_study_email_captured — visitor provides email to access gated content
case_study_converted — visitor completes a conversion action (demo booked, signup, contact form)
case_study_shared — visitor uses a share button (LinkedIn, Twitter, email)
```

Each event carries standard properties: `case_study_id`, `company_name`, `industry`, `use_case`, `traffic_source`, `device_type`. Build PostHog funnels: hub_viewed -> page_viewed -> cta_clicked -> converted, and hub_viewed -> page_viewed -> pdf_downloaded -> email_captured.

Create PostHog cohorts for visitors who engaged with case studies (viewed 2+ pages or downloaded a PDF) to use for retargeting and nurture sequences.

### 2. Deploy the candidate recruitment pipeline

Run the `case-study-candidate-pipeline` drill to build the always-on recruitment system. This drill:

1. **Scores all active accounts** weekly on four dimensions: results strength (product usage, retention, feature adoption), story potential (industry relevance, brand recognition, role seniority), relationship health (NPS, support sentiment, email engagement), and timing signal (recent milestones, not in active sales cycle).

2. **Maintains a ranked candidate list** in Attio with composite `case_study_fit_score`. Only candidates scoring >= 70 enter the active pipeline, limited to 10 at a time.

3. **Runs a 4-touch recruitment sequence** via Loops: personalized ask email (Day 0), social proof email showing an existing case study (Day 4), in-app nudge via Intercom for opened-but-not-booked candidates (Day 9), and a final low-pressure follow-up offering alternatives like written Q&A or async video (Day 14).

4. **Handles responses** via n8n webhooks: interview bookings route to Cal.com, declines set a 6-month cooldown, alternative format requests trigger a separate workflow.

5. **Tracks the full recruitment funnel** in PostHog: scored -> entered_pipeline -> outreach_sent -> outreach_opened -> interview_scheduled -> interview_completed -> case_study_published.

**Human action required:** Review the candidate pipeline's first 10 selections. Verify the scoring model is surfacing customers you would actually want to feature. Adjust dimension weights if the model is over-indexing on brand recognition at the expense of story quality, or vice versa.

### 3. Produce 10-12 case studies

Run the `case-study-creation` drill for each recruited customer. At Baseline level, accelerate production by:

- Using AI (via the `ai-content-ghostwriting` fundamental) to generate first drafts from interview transcripts. The agent extracts the Challenge-Solution-Results arc, selects the strongest quotes, and structures the narrative. A human editor then polishes for accuracy, storytelling, and voice.
- Creating both gated and ungated versions of each case study: an ungated HTML page for SEO and organic discovery, and a gated PDF download that captures email for sales follow-up.
- Building a consistent visual template: summary box (company, industry, size, key metric, pull quote), challenge section, solution section, results section, and CTA block.

Aim for 3-4 new case studies per week during weeks 2-5, with customer review and publication in weeks 3-7.

### 4. Build the case study hub

Create a dedicated hub page on your website with all published case studies. Include filters for:

- Industry (SaaS, Healthcare, Fintech, etc.)
- Use case (the primary workflow or problem each case study addresses)
- Company size (SMB, Mid-market, Enterprise)
- Results type (Revenue, Efficiency, Retention, Growth)

Each card shows: company logo, company name, industry tag, one-line result, and a "Read story" CTA. Track filter usage with `case_study_hub_filtered` events in PostHog to understand what prospects are looking for.

**Human action required:** Design review of the hub page layout before launch. Ensure the filtering works correctly and the page loads fast.

### 5. Integrate with sales

Using the `attio-notes` and `attio-deals` fundamentals (referenced in the `case-study-creation` drill), arm the sales team:

- For each active deal in Attio, attach the most relevant case study as a note (same industry or use case)
- Notify deal owners when a new case study is published that matches their open deals
- Create an Attio view: "Case Studies by Industry" so sales reps can quickly find the right story for any prospect

Track sales usage: fire `case_study_sent_by_sales` in PostHog when a rep forwards a case study to a prospect. This measures adoption of case studies in the sales process.

### 6. Evaluate after 8 weeks

Run the `threshold-engine` drill. Aggregate across all case study pages:

- Total page views, total conversions, conversion rate
- Average time on page (target ≥ 3 minutes)
- PDF download count and email capture rate
- Recruitment pipeline metrics: outreach acceptance rate, interviews completed, case studies published
- Sales usage: how many deals received case study assets

- **PASS (≥ 2,000 views and ≥ 30 conversions, ≥ 3 min avg time on page):** Document the production workflow, the candidate scoring model's performance, and which case studies drive the most conversions. Identify the top-performing case study and analyze why. Proceed to Scalable.
- **MARGINAL (1,500-1,999 views or 20-29 conversions):** Check distribution: are all case studies being promoted equally? Check the hub: are filters driving discovery or are visitors only finding case studies through direct links? Check PDF gating: is the gate helping or hurting (compare gated vs ungated conversion rates)?
- **FAIL (< 1,500 views or < 20 conversions):** Diagnose: Is the recruitment pipeline producing enough candidates? Are the case studies compelling (check time on page -- < 2 min suggests weak stories)? Are the CTAs specific and visible? Is the hub discoverable from your main site navigation?

## Time Estimate

- PostHog event taxonomy setup: 3 hours
- Candidate pipeline deployment and scoring model: 6 hours
- 10-12 interviews (30 min each + prep): 10 hours
- Writing and editing (with AI first drafts): 8 hours
- Customer review coordination: 2 hours
- Hub page creation: 3 hours
- Sales integration setup: 2 hours
- Monitoring and evaluation: 1 hour
- Total: ~35 hours over 8 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies.ai | Interview transcription | Free: 800 min/mo; Pro ~$10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Ghost | Case study publishing and CMS | Free self-hosted; Pro $9/mo ([ghost.org/pricing](https://ghost.org/pricing)) |
| PostHog | Event tracking, funnels, cohorts | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Candidate pipeline, deal matching, sales enablement | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Recruitment pipeline automation, webhooks | Free self-hosted; Starter ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Recruitment outreach sequences | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app nudge for recruitment | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Cal.com | Interview scheduling | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Anthropic API | AI first-draft generation from transcripts | Usage-based ~$3/1M input tokens for Sonnet ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Baseline:** $50-120/mo (Attio + n8n + Loops on starter plans; other tools on free tiers; Anthropic API negligible at this volume)

## Drills Referenced

- `case-study-creation` — end-to-end process for interviewing customers, writing the case study, creating derivative assets, and distributing strategically
- `case-study-candidate-pipeline` — always-on pipeline that scores active accounts for case study fit, maintains a ranked candidate list, and runs a 4-touch automated recruitment sequence
- `posthog-gtm-events` — define and implement the case study event taxonomy in PostHog for funnels, cohorts, and conversion tracking
