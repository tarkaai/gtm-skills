---
name: outgrow-interactive-content
description: Build calculators, assessments, quizzes, and recommendation engines in OutGrow with lead capture and analytics
tool: OutGrow
product: OutGrow
difficulty: Config
---

# Create OutGrow Interactive Content

OutGrow is a purpose-built platform for interactive content — ROI calculators, maturity assessments, product recommendation quizzes, and graders. It handles complex calculation logic, conditional branching, and result personalization without code.

### Authentication

OutGrow API access for programmatic operations:

```
Base URL: https://api.outgrow.co/api/v1
Auth: API key from OutGrow dashboard > Settings > API & Webhooks
Header: api_key: {OUTGROW_API_KEY}
```

### Step-by-step

1. Create a new content piece at `https://app.outgrow.co`. Choose the content type:
   - **Numerical Calculator** — for ROI calculators, cost estimators, savings calculators. User inputs numbers, gets a computed result.
   - **Graded Quiz/Assessment** — for maturity assessments, readiness scores. User answers questions, gets a score and tier (Beginner/Intermediate/Advanced).
   - **Outcome Quiz** — for product recommendations, plan selectors. User answers questions, gets matched to a specific outcome.
   - **Poll** — for surveys with real-time results display.

2. Configure input questions:
   - Add questions using OutGrow's drag-and-drop builder
   - Use question types: Numeric Slider, Dropdown, Single Select, Multi-Select, Text Input, Rating
   - Set default values and ranges for numeric inputs (min/max/step)
   - Add helper text explaining what each input means and why it matters

3. Build the calculation/scoring logic:
   - For **Calculators**: use OutGrow's formula builder. Reference inputs by variable names. Support operators: +, -, *, /, ^, MIN, MAX, IF/ELSE, AND, OR.
   - Example: `IF({team_size} > 10, {hours_saved} * {hourly_rate} * 1.5, {hours_saved} * {hourly_rate})` — different multiplier for larger teams
   - For **Assessments**: assign point values to each answer option. Define score ranges for each tier (0-30 = Beginner, 31-60 = Intermediate, 61-100 = Advanced).
   - For **Outcome Quizzes**: map answer combinations to outcomes using OutGrow's outcome mapping grid.

4. Add the **Lead Capture Gate**:
   - In OutGrow settings, enable "Lead Generation Form"
   - Place it BEFORE results (users must enter email to see their score/calculation)
   - Fields: Name, Work Email, Company (keep minimal — each extra field reduces completion by ~10%)
   - Add a checkbox for marketing consent
   - Configure the skip option: decide whether to allow skipping (lowers capture rate but increases completion rate)

5. Design the **Results Page**:
   - Display the primary result prominently: "Your estimated annual savings: $X" or "Your maturity score: X/100"
   - Add contextual interpretation: "This puts you in the top 30% of companies we've assessed"
   - Include personalized recommendations based on score ranges
   - Add a primary CTA: "Book a consultation to improve your score" with Cal.com/Calendly link
   - Add a secondary CTA: "Download your full report" (PDF generation via OutGrow)
   - Add social sharing buttons (OutGrow tracks viral coefficient)

6. Configure **Integrations**:
   - Webhook: Settings > Integrations > Webhook. Fires on completion with all inputs, calculated results, and lead data.
   - n8n: Use webhook URL from n8n to receive submissions
   - CRM: OutGrow has native Attio/HubSpot/Salesforce integrations, or use webhook + n8n for custom routing
   - Email: Connect to Loops/Mailchimp for automated follow-up sequences

7. Set up **Analytics Tracking**:
   - OutGrow provides built-in analytics: views, starts, completions, lead captures, shares
   - Add PostHog tracking via custom JavaScript in OutGrow's HTML injection:
   ```javascript
   // Add to OutGrow custom JS settings
   window.addEventListener('message', function(event) {
     if (event.data && event.data.type === 'outgrow') {
       if (event.data.action === 'started') posthog.capture('tool_started', { tool_type: 'calculator', tool_id: '{outgrow_id}' });
       if (event.data.action === 'completed') posthog.capture('tool_completed', { tool_type: 'calculator', tool_id: '{outgrow_id}', result: event.data.result });
       if (event.data.action === 'lead_captured') posthog.capture('lead_captured', { tool_type: 'calculator', tool_id: '{outgrow_id}', surface_type: 'interactive_tool' });
     }
   });
   ```

8. **Embed** the OutGrow content:
   - Inline embed: `<div class="op-interactive" id="{outgrow_content_id}"></div><script src="https://outgrow.co/lib/calc.js" ...></script>`
   - Popup embed: trigger on button click or exit intent
   - Full-page: host at a custom URL via OutGrow's hosting or redirect

9. Enable **A/B Testing** (OutGrow Pro plan):
   - Create variants of questions, result copy, or CTA placement
   - OutGrow splits traffic and reports conversion rates per variant
   - Run tests for minimum 200 completions per variant before calling a winner

10. Test the full flow: complete the tool, verify result calculation is correct, verify lead capture fires webhook, verify CRM record creation, verify email sequence enrollment.

### OutGrow API — Reading Responses

```
GET https://api.outgrow.co/api/v1/content/{content_id}/leads
Headers: api_key: {OUTGROW_API_KEY}

Response:
{
  "data": [
    {
      "id": "...",
      "email": "user@example.com",
      "name": "Jane Doe",
      "result": "85",
      "answers": { "q1": "50000", "q2": "SaaS", "q3": "4" },
      "createdAt": "2026-03-30T..."
    }
  ]
}
```

### Pricing

- **Freelancer**: $22/mo — 1 content piece, 1,000 leads/mo
- **Essentials**: $115/mo — 5 content pieces, 5,000 leads/mo, custom branding
- **Business**: $600/mo — unlimited content, 50,000 leads/mo, A/B testing, API access
- Free trial: 7 days on Business plan

### Alternative Tools

- **Tally** — free, good for simpler calculators. Use `tally-form-setup` fundamental.
- **Typeform** — good UX, limited calculation. Use `typeform-survey-setup` fundamental.
- **Involve.me** — similar to OutGrow, $29/mo+. Strong on quizzes and payment forms.
- **Calconic** — calculator-only, embeddable, $19/mo+. Lighter than OutGrow.
- **ConvertCalculator** — focused on price/ROI calculators, $19/mo+.
