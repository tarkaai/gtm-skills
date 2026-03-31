---
name: sdk-library-development-scalable
description: >
  SDK & Library Development — Scalable Automation. Scale SDK coverage to 4+ languages
  via code generation, run A/B tests on README CTAs and docs, and automate
  cross-registry publishing and monitoring.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Product"
level: "Scalable Automation"
time: "80 hours over 3 months"
outcome: ">=5,000 downloads/month across all SDKs and >=40 developer signups/month from registries sustained over 3 months"
kpis: ["Total downloads/month (all registries)", "Downloads per language", "Developer signups/month from SDKs", "Activation rate per language", "CTA A/B test win rate", "SDK coverage (number of languages)"]
slug: "sdk-library-development"
install: "npx gtm-skills add marketing/solution-aware/sdk-library-development"
drills:
  - ab-test-orchestrator
---
# SDK & Library Development — Scalable Automation

> **Stage:** Marketing -> Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Product

## Outcomes
SDKs published across 4+ package registries covering the major developer ecosystems, automated cross-registry publishing from a single API spec, A/B-tested README CTAs and documentation, and a monitoring system that tracks download trends across all languages. The 10x multiplier comes from code generation: each additional SDK adds a new registry's entire developer audience with marginal engineering effort.

## Leading Indicators
- Each new SDK reaches 100+ downloads within its first 2 weeks (organic, no seeding)
- CTA conversion rate improves by >=20% through A/B testing within the first 6 weeks
- At least 2 SDKs independently generate >=5 signups/month (no single-language dependency)
- Cross-registry monitoring detects and alerts on anomalies within 24 hours
- Code generation produces a publishable SDK in <4 hours per new language

## Instructions

### 1. Scale to 4+ languages via code generation
Run the the sdk multi language scaling workflow (see instructions below) drill to:
- Prioritize target languages based on demand signals (docs traffic, support tickets, competitor coverage, registry search volume)
- Generate SDK code from your API specification using OpenAPI Generator or equivalent
- Manually improve each generated SDK: add retry logic, pagination helpers, idiomatic error handling, and usage examples
- Build a shared test suite that validates all SDKs against the same API contract
- Publish each new SDK using the CI pipeline pattern from Baseline

Target coverage:
- **Must-have:** TypeScript (npm), Python (PyPI)
- **High-value:** Go (pkg.go.dev), Rust (crates.io)
- **Broad reach:** Ruby (RubyGems), Java (Maven Central), C# (NuGet)

**Human action required:** Review generated code for each new language. Approve each SDK before first publish.

### 2. A/B test README CTAs and documentation
Run the `ab-test-orchestrator` drill to systematically test SDK conversion variables:

**Test 1 -- README CTA copy:**
- Control: "Try [Product] free"
- Variant: "Get your API key in 30 seconds"
- Metric: CTA click-through rate

**Test 2 -- README format:**
- Control: Comprehensive (install + example + features + architecture + CTA)
- Variant: Minimal (install + 3-line example + CTA)
- Metric: CTA click-through rate

**Test 3 -- Docs landing experience:**
- Control: Unified SDK docs page (all languages on one page)
- Variant: Language-specific landing pages (one page per SDK, UTM-matched)
- Metric: Signup conversion rate from docs visit

Run one test at a time. Apply winners across all SDKs. Each test requires minimum 200 CTA impressions per variant (use the highest-traffic SDKs for testing).

### 3. Automate synchronized releases
Using the release infrastructure from the sdk multi language scaling workflow (see instructions below):
- When your API changes, regenerate SDKs from the updated spec
- Run shared test suites against all SDKs in CI
- Tag and publish all SDKs simultaneously
- Each release body includes a changelog and CTA with version-specific UTM

Build an n8n workflow triggered by a "release all SDKs" webhook that:
1. Creates a GitHub release on each SDK repo
2. Monitors each repo's CI to confirm registry publish succeeded
3. Sends a consolidated "All SDKs released" notification to Slack
4. Updates Attio campaign record with latest version numbers

### 4. Expand distribution channels
Beyond the package registry itself:
- Submit each SDK to Awesome Lists for the language (e.g., awesome-python, awesome-rust)
- Add SDK install badges to your main product README and docs
- List SDKs in the "Integrations" or "API Libraries" page of your marketing site
- Post on language-specific forums/subreddits when a new SDK launches

**Human action required:** Submit to Awesome Lists (requires PRs to external repos). Update marketing site.

### 5. Evaluate against threshold
Measure against: >=5,000 downloads/month across all SDKs and >=40 developer signups/month from registries sustained over 3 months.

If PASS: The SDK distribution engine is working at scale. Proceed to Durable.
If FAIL: Focus resources on the 2-3 highest-converting SDKs. Retire or reduce investment in SDKs that generate downloads but not signups (discoverability without conversion). Investigate whether the problem is SDK quality (developers try it but don't convert) or documentation (developers convert but don't activate).

## Time Estimate
- Language prioritization and demand analysis: 4 hours
- Code generation setup and customization per language: 8 hours x 3 new languages = 24 hours
- Shared test suite development: 8 hours
- CI/CD pipeline for each new SDK: 3 hours x 3 = 9 hours
- A/B test setup and analysis (3 tests): 12 hours
- Synchronized release automation: 6 hours
- Distribution channel expansion: 8 hours
- Monitoring and reporting upgrades: 9 hours

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host all SDK repos, CI/CD | Free for public repos |
| npm / PyPI / crates.io / RubyGems / Maven / NuGet | Package registries | Free to publish |
| OpenAPI Generator | Generate SDK code from API spec | Free, open source |
| PostHog | A/B testing, funnels, dashboards | Free up to 1M events/mo; experiments from $0 (https://posthog.com/pricing) |
| n8n | Cross-registry publishing, monitoring | Free self-hosted or from EUR 20/mo cloud (https://n8n.io/pricing) |
| Attio | Lead tracking across SDKs | Free for small teams (https://attio.com/pricing) |

## Drills Referenced
- the sdk multi language scaling workflow (see instructions below) -- scales SDK coverage to 4+ languages using code generation, shared test suites, and automated cross-registry publishing
- `ab-test-orchestrator` -- designs, runs, and analyzes A/B tests on README CTAs and SDK documentation
