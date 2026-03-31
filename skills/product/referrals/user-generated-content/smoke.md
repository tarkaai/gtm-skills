---
name: user-generated-content-smoke
description: >
  UGC Campaign — Smoke Test. Deploy 2-3 in-product prompts at high-signal moments
  (post-activation, milestone, upgrade) to ask users to create content about the product.
  Collect and manually review at least 5 UGC pieces in 2 weeks. Validate that real users
  will create content when asked at the right moment.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Referrals"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: ">=5 approved UGC pieces from >=3 unique creators in 2 weeks"
kpis: ["UGC pieces submitted (target >=5)", "Unique creators (target >=3)", "Prompt-to-submission conversion rate (target >=3%)", "Approval rate on submitted content (target >=50%)"]
slug: "user-generated-content"
install: "npx gtm-skills add product/referrals/user-generated-content"
drills:
  - threshold-engine
---

# UGC Campaign — Smoke Test

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Referrals

## Outcomes

Prove that product users will create content about the product when prompted at the right moment. This is not about volume or amplification yet — it is about validating the core hypothesis: users who just experienced a success event (activation, milestone, upgrade) will take 2 minutes to share their experience when asked directly with a low-friction form.

Pass: >=5 approved UGC pieces from >=3 unique creators within 2 weeks.
Fail: <5 pieces or <3 unique creators after 2 weeks of active prompting.

## Leading Indicators

- First UGC submission arrives within 72 hours of deploying prompts (the trigger moment and messaging work)
- At least 1 submission comes from a trigger type you did not expect to perform best (multiple triggers have potential)
- Prompt click-through rate exceeds 8% (users are noticing and engaging with the ask)
- At least 1 submission requires zero editing to be shareable (proof that users can produce quality content without hand-holding)
- No users report being annoyed by the prompt or submit negative/sarcastic content (the timing and tone are appropriate)

## Instructions

### 1. Design and deploy UGC prompts

Run the the ugc prompt design workflow (see instructions below) drill. For Smoke level, deploy 2-3 trigger-based prompts:

**Post-activation prompt (highest priority):**
Deploy an Intercom in-app message triggered 24-48 hours after the user's activation event. The message asks the user to share how they set things up. Provide a lightweight form: one text field for their tip or experience (280 characters), plus an optional longer text area. Auto-populate their name, email, and account from their session.

**Milestone prompt:**
Deploy an Intercom in-app message triggered when a user crosses a usage milestone (100th action, 1000th event, or similar round number in your product). Ask them to share their best tip or use case.

**Upgrade prompt (if applicable):**
Deploy an Intercom in-app message triggered 7 days after a plan upgrade. Ask for a quick testimonial: role, what they use the product for, and why it works.

Set frequency capping: maximum 1 UGC prompt per user per 14 days. Never show to users with open support tickets.

The drill configures PostHog events for the full prompt funnel: `ugc_prompt_shown`, `ugc_prompt_clicked`, `ugc_form_started`, `ugc_form_completed`.

For Smoke level, form submissions can go to a simple destination — an email inbox, a Slack channel, or a Google Sheet. The `ugc-submission-webhook` is optional at Smoke but recommended if n8n is already running.

### 2. Manually review and approve submissions

**Human action required:** As submissions arrive, review each one manually. For each piece:

- Is it genuine? (Not sarcastic, not a support complaint disguised as feedback)
- Is it relevant? (Actually about your product or a use case)
- Is it coherent? (Could another person understand and benefit from it)
- Would you be comfortable sharing it publicly?

Track in a spreadsheet or Attio notes:
- Submitter name, email, account
- Content type (tip, testimonial, tutorial, use case)
- Trigger that prompted it (post-activation, milestone, upgrade)
- Quality rating (1-5)
- Verdict (approved, needs editing, rejected)

### 3. Thank creators and test amplification manually

For each approved piece:
- Send a personal thank-you message (email or in-app). Mention the specific content: "Your tip about [topic] is great — we'd love to share it."
- Ask for permission to share publicly if not already granted via the form
- Pick the single best piece and share it on one channel (LinkedIn post, newsletter mention, or community channel) to test whether UGC resonates with your audience

Track: did the creator respond positively to the thank-you? Did the shared piece generate any engagement or traffic?

### 4. Evaluate after 2 weeks

Run the `threshold-engine` drill to measure against the pass threshold.

Count: total pieces submitted, total approved, unique creators, prompt-to-submission conversion rate.

- **PASS (>=5 approved pieces from >=3 unique creators):** Users will create content when prompted at the right moment. Document: which triggers performed best, which content types were submitted most, what the quality range looked like, and how creators responded to the thank-you. Proceed to Baseline.
- **MARGINAL (3-4 pieces or only 1-2 unique creators):** The core hypothesis has some signal but needs refinement. Check: Are prompts being shown to enough users? Is the ask too big (reduce to a simpler form)? Is the timing right (try a different trigger moment)? Re-run with adjustments for another 2 weeks.
- **FAIL (<3 pieces or 0 unique creators):** Users are not responding to the prompts. Diagnose: Did users see the prompts (check `ugc_prompt_shown` events)? Did anyone click but not submit (check `ugc_form_started` vs `ugc_form_completed`)? Is the product generating enough success events to trigger prompts? Consider whether the user base is large enough for UGC or whether a different referral play (review-ask, testimonial collection) is more appropriate.

## Time Estimate

- UGC prompt design and deployment: 3 hours
- Monitoring submissions over 2 weeks: 2 hours total
- Manual review and creator outreach: 2 hours
- Evaluation and documentation: 1 hour
- Total: ~8 hours of active work spread over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app UGC prompts and forms | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| PostHog | Prompt funnel tracking | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Track submissions and creator records | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Smoke:** $29/mo (Intercom Essential; PostHog and Attio on free tiers)

## Drills Referenced

- the ugc prompt design workflow (see instructions below) — design and deploy in-product prompts at high-signal moments (post-activation, milestone, upgrade) with lightweight submission forms and frequency capping
- `threshold-engine` — evaluate submission count and creator diversity against the pass threshold and recommend next action
