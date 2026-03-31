---
name: user-generated-content-baseline
description: >
  UGC Campaign — Baseline Run. Automate the full collection pipeline: webhook-based
  submission processing, AI moderation, CRM cataloging, and creator engagement sequences.
  Launch external content detection. Begin amplifying approved UGC across social, email,
  and in-product channels. Target >=15 approved pieces from >=8 unique creators in 4 weeks.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Referrals"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=15 approved UGC pieces from >=8 unique creators in 4 weeks with automated collection and moderation"
kpis: ["Approved UGC pieces (target >=15)", "Unique creators (target >=8)", "Prompt-to-submission conversion rate (target >=4%)", "Approval rate (target >=60%)", "Amplified pieces (target >=10)", "Referral visits from UGC (target >=20)"]
slug: "user-generated-content"
install: "npx gtm-skills add product/referrals/user-generated-content"
drills:
  - posthog-gtm-events
  - ugc-amplification-pipeline
---

# UGC Campaign — Baseline Run

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Referrals

## Outcomes

Move from manual Smoke-level review to an always-on UGC pipeline. The submission webhook processes incoming content automatically. AI moderation scores and routes each piece (approve, review, reject). Approved content enters the UGC Library in Attio. External content detection finds UGC posted on social media, review sites, and community channels. The amplification pipeline distributes approved UGC across LinkedIn, email newsletters, and in-product showcases. The system runs continuously without manual intervention for collection and moderation.

Pass: >=15 approved UGC pieces from >=8 unique creators in 4 weeks, with automated collection, moderation, and at least 10 pieces amplified across channels.
Fail: <15 pieces or <8 unique creators after 4 weeks, or the automation pipeline requires daily manual intervention.

## Leading Indicators

- The submission webhook processes its first automated submission within 24 hours of deployment (the pipeline works end-to-end)
- AI moderation agrees with human judgment on >=80% of pieces from the Smoke level (the moderation model is calibrated)
- External detection discovers at least 2 UGC pieces the team did not know about (users are creating content without being asked)
- At least 1 amplified UGC piece generates a referral visit within 7 days (UGC drives traffic)
- Creator thank-you emails achieve >=50% open rate (creators care about the relationship)
- At least 1 creator submits a second piece within the 4-week period (repeat behavior is possible)

## Instructions

### 1. Set up the event taxonomy

Run the `posthog-gtm-events` drill to establish UGC-specific tracking. Configure these events:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `ugc_submitted` | Content enters the webhook | `content_type`, `platform`, `submitter_tier`, `trigger_type` |
| `ugc_moderated` | AI moderation completes | `verdict`, `composite_score`, `quality_score`, `relevance_score`, `processing_time_ms` |
| `ugc_approved` | Content passes moderation | `content_type`, `platform`, `amplification_score`, `suggested_channels` |
| `ugc_rejected` | Content fails moderation | `content_type`, `rejection_reason` |
| `ugc_amplified` | Content published to a channel | `content_id`, `channel`, `content_type`, `creator_tier` |
| `ugc_amplified_clicked` | Someone clicks through UGC to your site | `content_id`, `channel`, `referral_source` |
| `ugc_creator_thanked` | Thank-you sent to creator | `template_type`, `channel` |

Build PostHog funnels:
- **Collection funnel:** `ugc_submitted` -> `ugc_moderated` -> `ugc_approved`
- **Amplification funnel:** `ugc_approved` -> `ugc_amplified` -> `ugc_amplified_clicked`
- **Prompt funnel:** `ugc_prompt_shown` -> `ugc_prompt_clicked` -> `ugc_form_completed` -> `ugc_submitted`

### 2. Deploy the automated collection pipeline

Run the the ugc collection automation workflow (see instructions below) drill. This deploys:

**Submission webhook:** An n8n workflow that receives content submissions, validates fields, deduplicates, enriches the submitter from Attio CRM, and routes to AI moderation. Replace the manual review from Smoke with this automated pipeline.

**AI moderation:** Each submission runs through the `ugc-moderation-api` fundamental. The API scores content on quality, relevance, brand safety, amplification potential, and authenticity. Content scoring >=3.5 composite is auto-approved. Content scoring 2.5-3.5 enters a human review queue in Attio. Content below 2.5 is auto-rejected with a gracious email.

**External content detection:** A daily n8n workflow searches Twitter/X, LinkedIn, YouTube, GitHub, community channels, and review sites for mentions of your product. Discovered content is POSTed to the submission webhook with the source platform noted. The deduplication check prevents reprocessing known content.

**UGC Library in Attio:** Create the "UGC Library" list with attributes: title, content type, platform, URL, submitter link, moderation scores, status (approved/amplified/featured/archived), and amplification metrics.

**Creator engagement:** Configure Loops transactional emails: thank-you on approval, notification when content is featured, and a follow-up 14 days after first submission encouraging a second piece.

Test end-to-end: submit a test piece through the form, verify the webhook processes it, verify AI moderation runs, verify the Attio record is created, verify the thank-you email sends.

### 3. Launch the amplification pipeline

Run the `ugc-amplification-pipeline` drill. This deploys:

**Weekly content selection:** An n8n workflow that runs every Monday, queries the UGC Library for approved-but-not-amplified content, ranks by amplification score, and queues the top 3-5 pieces for the week.

**Channel formatting:** For each piece, the workflow creates channel-specific versions:
- LinkedIn post: user quote or paraphrase + attribution + CTA to submit
- Email newsletter section: "From our community" feature with creator name, summary, and link
- In-product showcase: Intercom in-app message showing relevant UGC to non-creators in the same role/industry

**Creator notification:** When content is amplified, the creator receives an email with the link and an encouragement to reshare.

**Performance tracking:** PostHog events (`ugc_amplified`, `ugc_amplified_clicked`) with per-channel and per-piece metrics stored in the Attio UGC Library.

For Baseline, amplify at a modest cadence: 1 LinkedIn UGC post per week, 1 newsletter feature per edition, 1-2 in-product showcases per week. Prioritize quality over volume.

### 4. Evaluate after 4 weeks

Review the PostHog funnels and Attio UGC Library:

- Total submitted, moderated, approved, amplified
- Unique creators (from Attio Contributors list)
- Prompt-to-submission conversion rate by trigger type
- Approval rate (approved / total submitted)
- AI moderation accuracy: manually review 10 random decisions. Does the AI agree with your judgment?
- Amplification metrics: impressions, clicks, and referral visits from UGC
- Creator engagement: thank-you email open rates, second-submission rate

- **PASS (>=15 approved pieces from >=8 unique creators, >=10 amplified, automated pipeline):** The UGC pipeline works as an always-on system. Document: best-performing trigger types, content types that get highest approval rates, channels that drive the most referral traffic, and the AI moderation accuracy rate. Proceed to Scalable.
- **MARGINAL (10-14 pieces or 5-7 creators):** Check: Are prompts reaching enough users? Is the submission form too complex? Is the external detection finding content? Is AI moderation rejecting good content (tighten the prompt)? Stay at Baseline and optimize the weakest link.
- **FAIL (<10 pieces or <5 creators after 4 weeks):** The automated pipeline is not producing sufficient volume. Diagnose: Are enough users hitting trigger events? Is the user base large enough for UGC? Are external platforms producing any organic mentions? If the product lacks the user base for UGC at scale, consider pivoting to a more targeted play like case-study-recruitment or testimonial-collection.

## Time Estimate

- Event taxonomy and funnel setup: 2 hours
- Collection pipeline deployment (webhook + moderation + CRM): 6 hours
- External detection workflow setup: 3 hours
- Amplification pipeline setup: 4 hours
- Monitoring over 4 weeks: 3 hours total
- Evaluation and documentation: 2 hours
- Total: ~20 hours of active work spread over 4 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | All automation: webhook, moderation routing, external detection, amplification scheduling | Starter EUR24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM: UGC Library, Contributors list, creator records | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Intercom | In-app UGC prompts, in-product UGC showcase | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Creator engagement emails, newsletter UGC features | Free up to 1,000 contacts; Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | AI content moderation | Usage-based ~$3/1M input tokens for Sonnet ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Baseline:** $55-105/mo (n8n Starter + Intercom Essential + Loops if >1K contacts; Anthropic usage minimal at this volume)

## Drills Referenced

- `posthog-gtm-events` — establish the UGC event taxonomy with standard event names and properties for submission, moderation, amplification, and referral tracking
- the ugc collection automation workflow (see instructions below) — deploy the always-on pipeline: submission webhook, AI moderation, CRM cataloging, external content detection, and creator engagement sequences
- `ugc-amplification-pipeline` — format approved UGC for LinkedIn, email, and in-product channels; schedule weekly amplification; track per-piece and per-channel performance
