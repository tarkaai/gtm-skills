---
name: interactive-content-tools-baseline
description: >
  Interactive Content Tools — Baseline Run. Expand to 3-5 interactive tools across the buyer journey.
  Deploy automated lead nurture sequences personalized by tool results. Always-on tracking, CRM routing,
  and result-based email follow-up running continuously.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Baseline Run"
time: "22 hours over 6 weeks"
outcome: "≥300 tool completions and ≥100 qualified leads over 6 weeks"
kpis: ["Tool completion rate", "Email capture rate", "SQL conversion rate", "Cost per lead", "Tool engagement time"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
drills:
  - posthog-gtm-events
  - lead-capture-surface-setup
  - threshold-engine
---

# Interactive Content Tools — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Expand from 1 tool to 3-5 tools covering different buyer journey stages. Deploy always-on lead nurture that personalizes follow-up based on each user's tool results. This is the first level where the pipeline runs continuously without manual intervention.

**Pass threshold:** ≥300 tool completions and ≥100 qualified leads over 6 weeks

## Leading Indicators

- Tool completion rate stays ≥50% across all tools — new tools maintain quality
- Email capture rate ≥30% across the portfolio — gate is working at scale
- Nurture email open rate ≥40% — result-personalized emails outperform generic nurture
- At least 5 meetings booked from tool leads — the funnel connects to pipeline
- Organic traffic to tool pages growing week-over-week — SEO is building

## Instructions

### 1. Build 2-4 additional interactive tools

Run the the interactive tool build workflow (see instructions below) drill for each new tool. Choose tools that cover different stages of the buyer journey:

- **Awareness stage tool:** A benchmarking or assessment tool that helps the prospect discover they have a problem. Example: "How does your {metric} compare to industry benchmarks?"
- **Consideration stage tool:** A cost estimator or ROI calculator that quantifies the problem. Example: "Calculate the true cost of {pain point} at your company"
- **Decision stage tool:** A readiness grader or product-fit quiz that helps the prospect decide if your solution is right. Example: "Is {your product category} right for your team? Take the 2-minute assessment"

Each tool targets a different search keyword cluster. Diversify tool types (calculator, assessment, grader) to learn which format your ICP prefers.

### 2. Standardize event tracking

Run the `posthog-gtm-events` drill to establish a consistent event taxonomy across all tools. Every tool must fire the same events with the same property schema: `tool_viewed`, `tool_started`, `tool_field_completed`, `tool_email_captured`, `tool_results_viewed`, `tool_cta_clicked`.

Add the `tool_id` and `tool_type` properties to every event so you can compare tool performance in a single PostHog dashboard.

### 3. Optimize lead capture surfaces

Run the `lead-capture-surface-setup` drill for each tool's landing page. Configure:
- Email gate placement: after 3+ questions but before results (validated at Smoke)
- Thank-you redirect: show results on the same page, not a separate URL (reduces friction)
- CRM routing: n8n webhook → Attio contact creation with all tool response data as custom attributes
- Mobile optimization: verify every tool works on phone screens (50%+ traffic is mobile)

### 4. Deploy result-based nurture automation

Run the the interactive tool nurture pipeline workflow (see instructions below) drill to build three Loops sequences (fast-track, education, long-nurture) that personalize follow-up based on each user's tool results and score tier.

This is the key Baseline upgrade: instead of manually following up with tool leads, the n8n workflow scores each lead by their result tier (high/medium/low value), routes them to the appropriate Loops sequence, and the sequence references their specific tool results in every email.

**Human action required:** Review the AI-generated email content for the first 10 leads. Verify personalization quality and accuracy. Adjust the Anthropic prompt if the content feels generic or inaccurate.

### 5. Build cross-tool discovery

Add "Related tools" CTAs to each tool's results page. When someone completes the ROI calculator, suggest the maturity assessment. When someone completes the readiness grader, suggest the ROI calculator. This increases tools-per-visitor and deepens engagement.

Track cross-tool engagement in PostHog: `tool_cross_promoted` event with `source_tool_id` and `destination_tool_id`.

### 6. Promote tools via content

For each tool, generate a supporting blog post using the Anthropic API:

```
System: "Write a 1,000-word blog post that explains a {TOOL_TYPE} tool. Structure:
(1) Why {ICP_ROLE}s need to know their {METRIC} — open with a concrete scenario
(2) How the tool works — explain the methodology and what inputs mean
(3) Example walkthrough — show anonymized results from 3 different company profiles
(4) Embed CTA — 'Try the free {TOOL_TYPE} below' with the tool embed
(5) FAQ section (3-4 questions) answering common objections about the tool's methodology
Write for SEO. Target keyword: '{KEYWORD}'. Include the keyword in H1, first paragraph, one H2, and meta description."
```

**Human action required:** Review the blog post for accuracy, add the tool embed code, and publish. Verify schema markup (FAQPage) is added for the FAQ section.

### 7. Evaluate against threshold

Run the `threshold-engine` drill to measure against: ≥300 tool completions and ≥100 qualified leads over 6 weeks.

- **PASS:** Tools are generating leads at scale. Document which tool types, promotion channels, and nurture sequences drive the best results. Proceed to Scalable.
- **FAIL:** Diagnose: Is it a traffic problem (not enough people seeing the tools) or a conversion problem (people see the tools but don't complete them)? If traffic: invest in SEO and paid promotion. If conversion: simplify tools, improve landing page copy, or test different tool concepts.

---

## Time Estimate

- Build 2-4 additional tools (2-3 hours each): 8 hours
- PostHog event taxonomy setup: 2 hours
- Lead capture surface optimization per tool: 3 hours
- Nurture pipeline setup (3 sequences + n8n routing): 4 hours
- Blog content and SEO for each tool: 3 hours
- Monitoring and optimization over 6 weeks: 2 hours

Total: ~22 hours of active work over 6 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Tally | Build interactive tools (forms, calculations, logic) | Free tier; $29/mo for custom branding |
| PostHog | Event tracking, funnels, cohorts across all tools | Free up to 1M events/mo |
| n8n | Webhook processing, lead routing, nurture orchestration | Free self-hosted; $20/mo cloud |
| Loops | Email nurture sequences personalized by tool results | Free up to 1,000 contacts; $49/mo for 5,000 |
| Attio | CRM storage for tool leads with result data attributes | Free up to 3 seats |
| Anthropic | AI-generated personalized email content | ~$5-15/mo at this volume |

**Play-specific cost:** ~$50-100/mo (Loops + n8n cloud + Anthropic API)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- the interactive tool build workflow (see instructions below) — build each additional interactive tool with tracking and CRM routing
- `posthog-gtm-events` — standardize event taxonomy across all tools for consistent measurement
- `lead-capture-surface-setup` — optimize email gate, CRM routing, and mobile UX per tool
- the interactive tool nurture pipeline workflow (see instructions below) — deploy result-personalized nurture sequences with n8n routing
- `threshold-engine` — evaluate total completions and qualified leads against the pass threshold
