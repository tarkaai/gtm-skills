---
name: sdk-library-development-smoke
description: >
  SDK & Library Development — Smoke Test. Build and publish an SDK for your most-requested
  language to a package registry, instrument conversion tracking, and validate that registry
  presence generates developer signups.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Product"
level: "Smoke Test"
time: "12 hours over 2 weeks"
outcome: ">=100 SDK downloads and >=3 developer signups attributed to the registry README CTA in 4 weeks"
kpis: ["SDK downloads (7d)", "README CTA click-through rate", "Developer signups from SDK", "Time to first API call"]
slug: "sdk-library-development"
install: "npx gtm-skills add marketing/solution-aware/sdk-library-development"
drills:
  - sdk-package-scaffold
  - threshold-engine
---
# SDK & Library Development — Smoke Test

> **Stage:** Marketing -> Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Product

## Outcomes
An SDK published on one package registry (npm, PyPI, or the registry most requested by your ICP) with a conversion-tracked README that generates at least 100 downloads and 3 developer signups in 4 weeks. This proves that registry presence converts to pipeline.

## Leading Indicators
- SDK appears in registry search results for target keywords within 48 hours of publish
- First organic download (not from your team) within 7 days
- At least 1 README CTA click within 14 days
- At least 1 GitHub star from an external developer within 14 days

## Instructions

### 1. Choose the target language and registry
Analyze your existing developer audience to pick the first SDK language:
- Check support tickets and docs traffic for language mentions
- Look at your existing GitHub repos: what languages do your users star/fork?
- If no signal, default to TypeScript/npm (largest registry, broadest audience) or Python/PyPI (fastest-growing, strong in AI/data)

### 2. Scaffold and publish the SDK
Run the `sdk-package-scaffold` drill to:
- Create a GitHub repository with keyword-optimized metadata
- Build a working SDK that wraps your core API operations (minimum: authentication, 3 most-used endpoints, error handling with structured error types, automatic retries)
- Write a README with install command, 5-line quick start, feature list, and CTA block with UTM parameters (`utm_source={registry}&utm_medium=readme&utm_campaign={language}-sdk`)
- Configure CI to run tests and publish on tagged releases
- Publish v1.0.0 to the target registry

**Human action required:** Review the SDK code for correctness. Test the quick start example on a clean machine. Verify the package page renders correctly on the registry website.

### 3. Seed initial visibility
- Post a launch announcement in relevant developer communities (Hacker News Show HN, relevant subreddits, Discord/Slack communities for the language)
- If you have an existing developer mailing list, send a launch email
- Add the SDK to your product docs with an install badge

**Human action required:** Post the community announcements. The agent can draft the posts.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: >=100 SDK downloads and >=3 developer signups attributed to the registry README CTA in 4 weeks.

If PASS: Proceed to Baseline. The registry channel generates real developer leads.
If FAIL: Diagnose -- are downloads low (discoverability problem: improve keywords, description, topics) or are downloads happening but no CTA clicks (README CTA problem: rewrite the CTA section, test different copy)?

## Time Estimate
- Language/registry research: 1 hour
- SDK development and testing: 6 hours
- README, metadata optimization, and publish: 2 hours
- Community seeding: 1 hour
- Tracking setup and threshold configuration: 2 hours

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host SDK repo and CI/CD | Free for public repos |
| npm / PyPI / crates.io | Package registry | Free to publish |
| PostHog | Track CTA clicks and signups | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Log SDK-sourced leads | Free for small teams (https://attio.com/pricing) |

## Drills Referenced
- `sdk-package-scaffold` -- scaffolds the complete SDK package with repo, README, tests, CI, and registry metadata
- `threshold-engine` -- evaluates download and signup counts against the pass threshold
