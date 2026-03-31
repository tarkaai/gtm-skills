---
name: sdk-package-scaffold
description: Scaffold a complete SDK package for one language with docs, tests, CI, and registry-optimized metadata
category: SDK
tools:
  - GitHub CLI
  - npm / PyPI / crates.io / RubyGems / NuGet / Maven
  - PostHog
fundamentals:
  - github-repo-create
  - github-readme-optimization
  - github-topics-seo
  - github-social-preview
  - npm-package-publish
  - pypi-package-publish
  - crates-io-publish
  - rubygems-publish
  - nuget-package-publish
  - go-module-publish
  - maven-central-publish
  - posthog-custom-events
---

# SDK Package Scaffold

End-to-end workflow to create, structure, and publish an SDK or client library for a single language. This drill produces a live package on the target registry with a GitHub repo, docs, tests, CI pipeline, and conversion-tracked README.

## Input

- **API or product:** What the SDK wraps (REST API, GraphQL, webhook system, etc.)
- **Target language:** Which language/ecosystem to publish for (Node.js, Python, Ruby, Rust, Go, Java/.NET)
- **ICP description:** Which developers should find this SDK (what frameworks they use, what problems they solve)
- **Product CTA URL:** Where to send developers who want the full product

## Steps

### 1. Research the registry landscape

Before building, research what already exists in the target registry:

**For npm:**
```bash
npm search "<your-problem-domain>" --long 2>/dev/null | head -20
gh search repos "<your-problem-domain> sdk" --language=TypeScript --limit 10 --json fullName,stargazersCount,description --sort stars
```

**For PyPI:**
```bash
pip search is disabled; use web search instead:
# Search https://pypi.org/search/?q=<keyword>
gh search repos "<your-problem-domain> sdk" --language=Python --limit 10 --json fullName,stargazersCount,description --sort stars
```

Record:
- Top 5 competing packages: names, download counts, last updated dates
- Common naming patterns (e.g., `product-python`, `python-product`, `py-product`)
- Feature gaps: what do competitor SDKs lack? (async support, type hints, retries, pagination helpers)
- Keyword opportunities: terms with search volume but weak existing packages

### 2. Create the GitHub repository

Run the `github-repo-create` fundamental:
- Name: `{product}-{language}` or `{product}-sdk-{language}` (match the registry naming convention)
- Description: `Official {Language} SDK for the {Product} API. {Primary feature}.`
- Topics: `{product}`, `sdk`, `{language}`, `api-client`, `{problem-domain}`, plus 5+ more from keyword research
- License: MIT

### 3. Scaffold the package structure

Structure depends on language. Universal requirements:
- Working code that wraps the core API operations
- Type definitions (TypeScript types, Python type hints, Go interfaces, etc.)
- Automatic retries with exponential backoff for transient errors
- Structured error types that surface API error details
- At least 3 usage examples covering the most common operations
- Unit tests with >80% code coverage
- CI pipeline (GitHub Actions) that runs tests and publishes on tag

**Node.js/TypeScript example:**
```
your-sdk-node/
  src/
    index.ts           # Main client class
    types.ts           # TypeScript interfaces for all API objects
    errors.ts          # Custom error classes
    resources/         # One file per API resource
  examples/
    basic.ts
    advanced.ts
    error-handling.ts
  tests/
    client.test.ts
    resources.test.ts
  README.md
  LICENSE
  CHANGELOG.md
  package.json
  tsconfig.json
  .github/
    workflows/
      ci.yml           # Test on PR
      release.yml      # Publish on tag
    social-preview.png
```

### 4. Write the README with CTA

Run the `github-readme-optimization` fundamental, adapted for SDK context:

1. **Title + badges:** Package name, npm/PyPI badge, CI status badge, license badge
2. **Install command:** The one-liner developers need (`npm install @org/sdk`, `pip install your-sdk`)
3. **Quick start:** 5-10 lines of code showing the most common operation, copy-pasteable
4. **API reference link:** Point to full docs with UTM
5. **Features list:** What makes this SDK better (types, retries, pagination, async)
6. **CTA block:** `utm_source={registry}&utm_medium=readme&utm_campaign={language}-sdk`
7. **Contributing + License**

### 5. Configure CI/CD for automated publishing

Create a GitHub Actions workflow that publishes to the registry on tagged releases:

```yaml
# .github/workflows/release.yml
name: Publish
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # For npm provenance or PyPI trusted publishers
    steps:
      - uses: actions/checkout@v4
      - # Language-specific setup and build steps
      - # Publish to registry using the relevant fundamental
```

### 6. Publish the first version

Run the publish fundamental for the target registry (`npm-package-publish`, `pypi-package-publish`, etc.):
- Publish v1.0.0
- Verify the package page renders correctly
- Verify the install command works from a clean environment
- Verify all links (homepage, repo, docs) resolve correctly

### 7. Instrument conversion tracking

Using `posthog-custom-events`, set up tracking on your docs/landing page for SDK-sourced traffic:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `sdk_readme_cta_clicked` | Visit with `utm_source={registry}` | `registry`, `language`, `utm_campaign` |
| `sdk_signup_started` | Signup initiated from SDK-sourced session | `registry`, `language` |
| `sdk_api_key_created` | New API key created by SDK-sourced user | `registry`, `language` |

### 8. Set the social preview

Run the `github-social-preview` fundamental:
- Show: the install command, supported language logo, your brand mark

**Human action required:** Upload the social preview image via GitHub repo settings.

## Output

- Live package on the target registry with optimized metadata
- GitHub repo with README, tests, CI/CD, and social preview
- Conversion tracking from registry to product signup
- CI pipeline that auto-publishes on tagged releases

## Triggers

Run once per language/registry. Re-run when creating the next language SDK.
