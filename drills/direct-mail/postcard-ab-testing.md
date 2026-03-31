---
name: postcard-ab-testing
description: Run controlled A/B tests on postcard design, copy, and targeting to find the highest-performing variant
category: DirectMail
tools:
  - Lob
  - PostHog
  - Attio
  - n8n
fundamentals:
  - lob-template-create
  - lob-postcard-send
  - posthog-custom-events
  - posthog-experiments
  - attio-contacts
  - n8n-workflow-basics
---

# Postcard A/B Testing

This drill structures rigorous A/B tests for your direct mail postcards. Unlike digital A/B tests where you can get results in hours, postcard tests require careful planning because each variant costs real money to print and mail, and results take 2-4 weeks to materialize.

## Input

- An existing postcard campaign with baseline metrics (from a prior `postcard-campaign-send` run)
- A hypothesis about what to test (copy, design, CTA, targeting, send timing)
- Sufficient budget for at least 100 postcards per variant (200+ preferred)
- Lob API key and PostHog tracking configured

## Steps

### 1. Form a testable hypothesis

Structure every test as:

"If we [change X], then [metric Y] will [increase/decrease] by [estimated amount], because [reasoning]."

**Good direct mail test hypotheses:**
- "If we personalize the headline with the prospect's specific pain point instead of a generic value prop, response rate will increase by 2 percentage points, because personalization increases perceived relevance."
- "If we send a 6x9 jumbo postcard instead of 4x6, response rate will increase by 1.5 percentage points, because larger mail stands out in the mailbox."
- "If we include a QR code instead of a typed URL, URL visit rate will increase by 3 percentage points, because QR codes reduce friction."
- "If we time the postcard to arrive Monday (start of work week), response rate will increase vs. Friday delivery, because decision-makers process mail at the start of the week."

**Testable variables for postcards:**
- Headline copy (pain point framing)
- Body copy length (short vs. detailed)
- CTA type (URL, QR code, phone number, "reply to this address")
- Postcard size (4x6, 6x9, 6x11)
- Design style (minimalist vs. bold/colorful)
- Personalization level (name only vs. name + company + pain point)
- Send timing (day of week for delivery)
- ICP segment (different job titles or company sizes)

### 2. Create variant templates

Using `lob-template-create`, create separate templates for control and treatment:

- **Control:** The current best-performing postcard (or your initial design if this is the first test)
- **Treatment:** Identical to control except for the ONE variable being tested

Store template IDs for each variant. Label them clearly: `front_control`, `front_treatment_headline_v2`, etc.

### 3. Randomly assign prospects to variants

Pull the campaign's prospect list from Attio using `attio-contacts`. Split the list randomly:

Using n8n or a script:
1. Shuffle the list randomly
2. Assign first half to Control (variant A), second half to Treatment (variant B)
3. Update each contact in Attio: `direct_mail_test_variant = A` or `B`
4. Ensure the split is balanced on key dimensions: company size, industry, job title. If the list is small (<200), verify balance manually.

Register the experiment in PostHog using `posthog-experiments` so you can analyze results in PostHog's experiment UI.

### 4. Send both variants

Run the `postcard-campaign-send` drill separately for each variant:
- Variant A contacts get the control template
- Variant B contacts get the treatment template
- Include the variant identifier in the tracking URL: `?v=A` or `?v=B`
- Include the variant in Lob metadata: `metadata[variant]=A`

Send both variants on the same day so delivery timing is not a confounding variable (unless send timing is the variable being tested).

### 5. Wait for results

Direct mail A/B tests require patience:
- **Minimum wait:** 14 days after all postcards are confirmed delivered
- **Recommended wait:** 21 days for fuller response capture
- Do NOT check results daily or call a winner early — the same statistical rigor that applies to digital A/B tests applies here

During the wait, track delivery confirmation via the `postcard-response-tracking` drill to ensure both variants have comparable delivery rates. If one variant has significantly more returns-to-sender, the address lists may not have been balanced.

### 6. Analyze results

After the attribution window closes:

Using PostHog experiment analysis or manual calculation:
1. Pull response data per variant from PostHog: URL visits, meeting bookings, total responses
2. Calculate response rate per variant: responses / postcards_delivered
3. Check for statistical significance — with direct mail's small sample sizes, you need a larger effect size to be confident:
   - At 100 per variant with 5% baseline response rate, you need a ~5 percentage point lift to reach 95% confidence
   - At 250 per variant, a ~3 percentage point lift is detectable
4. Check secondary metrics: cost per response, cost per meeting, pipeline generated per variant

Log the experiment results using `posthog-custom-events`:
- Event: `direct_mail_experiment_completed`
- Properties: hypothesis, variant_a_response_rate, variant_b_response_rate, winner, confidence_level, sample_size_per_variant

### 7. Implement the winner

If the treatment wins with statistical significance:
- Update your default postcard template to use the winning variant
- Document the result in Attio as a campaign note: what changed, how much it improved, and the confidence level
- Archive the losing variant

If no significant difference:
- Keep whichever variant is simpler or cheaper
- The test still produced value — you now know this variable does not meaningfully affect response rate. Test a different variable.

If the control wins:
- Revert to the control
- Investigate why the hypothesis was wrong — the learning matters more than the result

## Output

- A completed A/B test with statistically analyzed results
- A winning (or inconclusive) verdict with confidence level
- Updated default templates reflecting the winner
- Documentation of the experiment for the team's learning library

## Triggers

- Run at Scalable level: one test per campaign cycle (every 2-4 weeks)
- At Durable level: tests are proposed and executed by the `autonomous-optimization` drill
