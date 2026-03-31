---
name: tally-form-setup
description: Create interactive forms, calculators, and assessments in Tally with conditional logic and result screens
tool: Tally
product: Tally
difficulty: Setup
---

# Create Tally Interactive Forms

Tally is a free form builder with conditional logic, calculations, and hidden fields — ideal for building interactive tools (ROI calculators, maturity assessments, scoring quizzes) that gate results behind email capture.

### Authentication

Tally does not require API auth for form creation — use the web builder at tally.so. For programmatic access (reading responses, embedding), use the Tally API:

```
Base URL: https://api.tally.so
Auth: Bearer token from Tally dashboard > Settings > API
```

### Step-by-step

1. Create a new form at `https://tally.so/forms/new`. Choose "Start from scratch."

2. Add input fields for the interactive tool. Use field types:
   - **Number** for financial inputs (revenue, team size, hours spent)
   - **Multiple Choice** for categorical inputs (industry, company stage, current tools)
   - **Linear Scale** for self-assessment ratings (1-5 maturity scores)
   - **Hidden Fields** to pass UTM parameters, referral source, or pre-populated data via URL params

3. Configure **Calculated Fields** for tool output:
   - Add a calculated field using Tally's formula builder
   - Reference input fields by their variable names: `{field_name} * {multiplier}`
   - Chain calculations: use one calculated field as input to another
   - Example ROI formula: `({hours_per_week} * {hourly_rate} * 52) * {automation_rate}` = annual savings

4. Add **Conditional Logic** to branch the assessment:
   - In form settings, add logic rules: "If [field] equals [value], show [section]"
   - Use this to create different result paths: high-maturity vs low-maturity recommendations
   - Skip irrelevant questions based on prior answers (e.g., skip "team size" questions for solo founders)

5. Add an **Email Capture** gate before showing results:
   - Insert an Email field after the input section but before the results/calculation section
   - Make it required
   - Add helper text: "We'll send your full results report to this email"
   - Add a hidden field for consent tracking

6. Build the **Results Screen**:
   - Add a Thank You page (or conditional Thank You pages for different score ranges)
   - Display calculated fields in the results: "Your estimated annual savings: ${calculated_savings}"
   - Include a CTA: "Book a call to discuss your results" with a Cal.com link
   - For multi-tier results, use conditional logic to show different recommendation blocks

7. Configure **Webhooks** for downstream processing:
   - In form settings > Integrations > Webhooks
   - Add webhook URL pointing to your n8n instance
   - Payload includes all field values, calculated values, and metadata
   - Webhook fires on each form submission

8. **Embed** the form on your website:
   - Use Tally's embed code: `<iframe data-tally-src="https://tally.so/r/{form_id}" ...>`
   - Or use the JavaScript embed for better styling: `Tally.loadEmbeds()`
   - Pass URL parameters for pre-population: `https://tally.so/r/{form_id}?utm_source=linkedin&company=Acme`

9. Enable **Partial Submissions** in form settings to capture abandonment data — see which questions cause drop-off.

10. Test the full flow: fill out the form, verify calculations display correctly, verify webhook fires to n8n, verify email field captures, verify result screens show the right conditional content.

### Tally API — Reading Responses

```
GET https://api.tally.so/forms/{form_id}/responses
Authorization: Bearer {TALLY_API_KEY}

Response:
{
  "data": [
    {
      "responseId": "...",
      "submittedAt": "2026-03-30T...",
      "fields": [
        { "key": "question_abc123", "label": "Annual Revenue", "value": 500000 },
        { "key": "question_def456", "label": "Email", "value": "user@example.com" }
      ]
    }
  ],
  "page": 1,
  "totalPages": 5
}
```

### Pricing

Tally free tier: unlimited forms, unlimited submissions, conditional logic, calculated fields, webhooks. Paid plan ($29/mo) adds: custom domains, file uploads, payment collection, remove Tally branding.

### Alternative Tools

- **Typeform** — similar UX but paid for conditional logic ($29/mo+). Use `typeform-survey-setup` fundamental.
- **OutGrow** — purpose-built for calculators/assessments but expensive ($22-600/mo). Better for complex multi-page tools.
- **Formbricks** — open-source, self-hosted. Good for privacy-sensitive use cases.
- **Jotform** — wide integration ecosystem, generous free tier (100 submissions/mo).
- **Google Forms** — completely free, no conditional result screens. Best for simple surveys only.
