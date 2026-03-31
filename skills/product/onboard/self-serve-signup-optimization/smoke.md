---
name: self-serve-signup-optimization-smoke
description: >
  Signup Funnel Optimization — Smoke Test. Instrument the signup funnel with field-level
  tracking, identify the primary conversion bottleneck, and establish baseline metrics.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Signup funnel fully instrumented with baseline CVR measured and primary bottleneck identified"
kpis: ["Signup page CVR", "Form start rate", "Form completion rate", "Form error rate"]
slug: "self-serve-signup-optimization"
install: "npx gtm-skills add product/onboard/self-serve-signup-optimization"
drills:
  - signup-funnel-audit
  - posthog-gtm-events
  - threshold-engine
---

# Signup Funnel Optimization — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

Signup funnel fully instrumented with field-level tracking. Every step from page view through email verification has a PostHog event. Baseline metrics recorded. Primary bottleneck identified with session recording evidence of why users drop off. This is a measurement and diagnosis pass -- no changes to the funnel yet.

## Leading Indicators

- All signup funnel events firing in PostHog Live Events within 2 hours of instrumentation
- Session recording playlists created for drop-off behavior at each funnel step
- Field-level error tracking revealing which form fields cause the most abandonment
- Baseline metric table populated with 7+ days of data

## Instructions

### 1. Instrument the signup funnel

Run the `signup-funnel-audit` drill. This instruments every step of the signup flow with PostHog events: page view, form focus, field completion, field errors, form submission, account creation, email verification, and initial setup completion. Implement field-level tracking so you know exactly which form field causes users to abandon.

**Human action required:** Deploy the tracking code to your signup pages. Verify events appear in PostHog Live Events by completing one test signup yourself.

### 2. Set up the event taxonomy

Run the `posthog-gtm-events` drill to ensure signup events follow the standard naming convention and have consistent properties (source, channel, stage, device_type). Map signup events to the broader product funnel so signup data connects to downstream activation and retention analysis.

### 3. Wait for data collection

Allow 7 days of data collection to establish statistically meaningful baselines. During this period, do not change the signup flow -- you need clean baseline data.

### 4. Analyze the funnel and identify the primary bottleneck

Complete the analysis steps of `signup-funnel-audit`: build the PostHog funnel, identify the step with the largest absolute drop-off, review 15-20 session recordings of users who dropped off at that step, and categorize the friction (form confusion, validation blocking, mobile friction, trust concerns, or distraction).

### 5. Record baseline metrics

Document baseline metrics from `signup-funnel-audit`:
- Signup page CVR (signup_completed / signup_page_viewed)
- Form start rate (signup_form_focused / signup_page_viewed)
- Form completion rate (signup_form_submitted / signup_form_focused)
- Form success rate (signup_completed / signup_form_submitted)
- Email verification rate
- Median time to complete signup
- Mobile CVR vs Desktop CVR

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: is the baseline data clean, are all events firing, and is the primary bottleneck clearly identified? The Smoke test passes when you have reliable baseline metrics and a prioritized list of friction points with evidence. If events are missing or data is noisy, fix instrumentation and re-run the 7-day collection.

## Time Estimate

- 2 hours: Instrument signup funnel events and deploy tracking code
- 1 hour: Configure event taxonomy and verify events
- 7 days: Data collection (passive)
- 2 hours: Funnel analysis, session recording review, baseline documentation
- 1 hour: Threshold evaluation and bottleneck prioritization

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, session recordings | Free tier: 1M events + 5K recordings/mo. Paid: usage-based from $0.00005/event. [posthog.com/pricing](https://posthog.com/pricing) |

## Drills Referenced

- `signup-funnel-audit` — instruments the signup funnel, builds funnels, identifies bottlenecks, establishes baselines
- `posthog-gtm-events` — sets up standard event taxonomy so signup data integrates with the broader analytics system
- `threshold-engine` — evaluates whether the Smoke test produced usable data and clear findings
