---
name: interactive-tool-build
description: Research ICP pain, choose tool format, build a calculator/assessment/grader, deploy with email gate and tracking
category: Content
tools:
  - Tally
  - OutGrow
  - Anthropic
  - Clay
  - PostHog
  - n8n
  - Attio
fundamentals:
  - tally-form-setup
  - outgrow-interactive-content
  - typeform-survey-setup
  - ai-content-ghostwriting
  - clay-claygent
  - posthog-custom-events
  - n8n-triggers
  - n8n-workflow-basics
  - attio-contacts
  - attio-deals
  - webflow-landing-pages
---

# Interactive Tool Build

This drill produces a single interactive content tool — a calculator, assessment, grader, or recommendation engine — deployed on a landing page with email capture gating and full event tracking. The tool must deliver standalone value to the user: they input their data, the tool computes a meaningful result, and they get actionable insight whether or not they ever talk to sales.

## Input

- ICP definition (from `icp-definition` drill): target titles, company sizes, pain points
- One validated pain point or decision the ICP needs help with (e.g., "How much am I spending on manual data entry?" or "Am I ready for a CRM?")
- Product value prop: what your product solves and how the tool connects to it

## Steps

### 1. Identify the tool concept

Use `clay-claygent` to research 30+ companies matching your ICP. For each, ask: "What calculations, comparisons, or assessments does {Company Name} need to make when evaluating {your product category}? What numbers do they care about?" Aggregate responses into a frequency table.

Pick the concept that appears in 40%+ of results AND has a direct connection to your product's value prop. Common interactive tool types:

| Tool Type | Best When | Example |
|-----------|-----------|---------|
| ROI Calculator | ICP needs to justify budget | "Calculate how much you'd save by automating X" |
| Maturity Assessment | ICP unsure if they have a problem | "Score your team's data maturity (1-100)" |
| Cost Estimator | ICP compares build vs buy | "Estimate your total cost of building X in-house" |
| Readiness Grader | ICP evaluating timing | "Are you ready for a CRM? Take the 2-minute assessment" |
| Benchmarking Tool | ICP wants to compare to peers | "How does your conversion rate compare to industry benchmarks?" |

### 2. Design the input fields

Use `ai-content-ghostwriting` (via Anthropic API) to generate the tool's question set:

```
System: "You are designing an interactive {TOOL_TYPE} for {ICP_DESCRIPTION}. The tool must:
- Use 5-8 input fields maximum (each additional field reduces completion by ~10%)
- Ask for data the user already knows (no research required to answer)
- Progress from easy/obvious questions to specific/revealing questions
- Use the right input types: sliders for ranges, dropdowns for categories, number inputs for financials
- Include one 'aha moment' calculation that surprises the user with a number they didn't know"

User: "Design the input fields for a {TOOL_CONCEPT}. For each field, specify: label, input type, default value, range (if applicable), and why this field matters for the calculation."
```

Review the output. Remove any field where the user would need to look something up. The tool should be completable in under 90 seconds.

### 3. Design the calculation logic

Define the formulas that transform inputs into results. Use Anthropic API:

```
System: "You are building the calculation engine for a {TOOL_TYPE}. Given these inputs: {INPUT_FIELDS_FROM_STEP_2}, design formulas that produce:
- One primary result (the headline number: savings, score, or recommendation)
- 2-3 secondary results (supporting metrics that add context)
- For each formula, show: the math, the assumptions, and where assumptions come from
- All assumptions must be cited (industry benchmark source or your product data)"
```

Document every formula and assumption. The user should be able to verify each number.

### 4. Build the tool

Choose platform based on complexity:

**For simple tools (5-7 fields, straightforward formulas):**
Use `tally-form-setup` to build in Tally (free). Configure calculated fields, conditional logic for result tiers, and email gate before results screen.

**For complex tools (8+ fields, conditional logic, multi-outcome):**
Use `outgrow-interactive-content` to build in OutGrow. Use the formula builder for complex calculations, multiple result pages, and built-in A/B testing.

**For custom-branded tools:**
Build as a custom web page using `webflow-landing-pages`. Implement calculations in client-side JavaScript. More effort but full design control.

### 5. Gate results behind email capture

Configure the email gate:
- Place email field AFTER the user has invested effort (answered 3+ questions) but BEFORE showing results
- Copy: "Enter your email to see your results. We'll also send a detailed report."
- Make email required. Do NOT allow skipping.
- Add a hidden field for UTM source tracking
- Fire a PostHog event on email submission: `lead_captured` with `surface_type: interactive_tool`, `tool_id`, `tool_type`

### 6. Build the results display

The results screen must deliver a genuine "aha moment":
- **Primary result** in large text: "You're spending $127,000/year on manual data entry" or "Your maturity score: 42/100 (Below Average)"
- **Context**: "Companies your size typically score 65+. Here's what separates you from the leaders."
- **Breakdown**: Show how each input contributed to the result. Users trust transparent math.
- **Recommendation**: 2-3 specific actions tied to their results. The third action should naturally lead to your product.
- **CTA**: "Book a call to discuss your results" → Cal.com link. "Download full report" → triggers PDF generation via n8n.

### 7. Wire tracking and CRM routing

Using `posthog-custom-events`, instrument these events:

| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `tool_viewed` | Landing page loads | `tool_id`, `tool_type`, `utm_source` |
| `tool_started` | User fills first field | `tool_id`, `tool_type` |
| `tool_field_completed` | Each field answered | `tool_id`, `field_name`, `field_position` |
| `tool_email_captured` | Email submitted | `tool_id`, `tool_type`, `email` |
| `tool_results_viewed` | Results screen displayed | `tool_id`, `primary_result`, `result_tier` |
| `tool_cta_clicked` | User clicks CTA on results | `tool_id`, `cta_type` (book_call, download_report, share) |

Using `n8n-triggers`, build a webhook workflow:
1. Tool completion webhook fires → `attio-contacts` creates Person + Company records with tool results as custom attributes → `attio-deals` creates a deal at "Tool Lead" stage with tool type, primary result, and result tier as properties.

### 8. Build the landing page

Using `webflow-landing-pages`, create a dedicated page for the tool:
- **URL**: `{yourdomain}.com/tools/{tool-slug}` (e.g., `/tools/roi-calculator`)
- **Above fold**: Headline matching the tool's value prop + the embedded tool
- **Below fold**: Methodology explanation, example results, customer logos or testimonials
- **SEO**: Target keywords like "{product category} calculator", "{pain point} assessment", "free {industry} ROI tool"

### 9. Test end-to-end

1. Complete the tool with test data. Verify calculations are correct.
2. Submit email. Verify PostHog events fire: `tool_started`, `tool_email_captured`, `tool_results_viewed`.
3. Verify n8n webhook fires and creates Attio records with correct properties.
4. Click the CTA. Verify the booking or download flow works.
5. Test on mobile — tool must be fully functional on phone screens.
6. Test with edge case inputs (zero values, maximum values). Verify calculations handle them gracefully.

## Output

- One live interactive tool on a dedicated landing page
- Email gate capturing leads with full tool response data
- PostHog event stream tracking the complete tool funnel
- n8n webhook routing leads to Attio CRM with tool results as attributes
- SEO-optimized landing page targeting relevant search terms

## Triggers

Run once per tool at Smoke level (1 tool). Run 2-4 additional times at Baseline level. At Scalable level, use the established template to batch-produce tools faster.
