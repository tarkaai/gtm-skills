---
name: sdk-multi-language-scaling
description: Scale SDK coverage to 4+ languages using code generation, shared test suites, and automated cross-registry publishing
category: SDK
tools:
  - GitHub CLI
  - n8n
  - PostHog
  - Anthropic
fundamentals:
  - github-repo-create
  - github-release-publish
  - npm-package-publish
  - pypi-package-publish
  - crates-io-publish
  - rubygems-publish
  - nuget-package-publish
  - go-module-publish
  - maven-central-publish
  - registry-download-tracking
  - n8n-workflow-basics
  - posthog-experiments
  - hypothesis-generation
---

# SDK Multi-Language Scaling

This drill scales SDK coverage from 1-2 languages to 4+ by using code generation from an API spec, shared test suites, and automated cross-registry publishing. The goal is 10x language coverage without 10x maintenance burden.

## Input

- At least 1 SDK at Baseline level with proven download-to-signup conversion
- An API specification (OpenAPI 3.x, GraphQL schema, or Protocol Buffers)
- Download and conversion data from `sdk-registry-distribution` drill (at least 4 weeks)
- List of target languages prioritized by ICP demand

## Steps

### 1. Prioritize target languages by demand signals

Query your existing data to rank language demand:

1. **Docs traffic:** Check PostHog for SDK docs page visits broken down by language preference (detected from `Accept-Language` header or explicit language selector clicks)
2. **Support tickets:** Search for "SDK", "client library", "wrapper" mentions and tag by requested language
3. **Competitor coverage:** Catalog which languages competitor SDKs support
4. **Registry search volume:** Use `registry-download-tracking` to check download volumes for competitors in each registry
5. **GitHub issues:** Search for "language request" issues in your repos

Rank languages by composite score: (docs demand * 3) + (support requests * 2) + (competitor coverage * 1).

Output: Ordered list of languages to build next, with justification.

### 2. Generate SDKs from API specification

If you have an OpenAPI spec, use code generation to accelerate SDK creation:

```bash
# Install the OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate SDKs for each target language
openapi-generator-cli generate -i openapi.yaml -g typescript-node -o ./sdks/node --additional-properties=npmName=@org/sdk-node
openapi-generator-cli generate -i openapi.yaml -g python -o ./sdks/python --additional-properties=packageName=your_sdk
openapi-generator-cli generate -i openapi.yaml -g ruby -o ./sdks/ruby --additional-properties=gemName=your-sdk
openapi-generator-cli generate -i openapi.yaml -g rust -o ./sdks/rust
openapi-generator-cli generate -i openapi.yaml -g go -o ./sdks/go
openapi-generator-cli generate -i openapi.yaml -g java -o ./sdks/java
openapi-generator-cli generate -i openapi.yaml -g csharp -o ./sdks/dotnet
```

After generation, manually improve each SDK:
- Add retry logic with exponential backoff (generators rarely include this)
- Add pagination helpers for list endpoints
- Improve error types to be idiomatic for the language
- Add usage examples beyond auto-generated boilerplate
- Write a README following `github-readme-optimization` patterns

### 3. Build a shared test suite

Create a language-agnostic test specification that each SDK must pass:

```yaml
# sdk-test-spec.yaml
tests:
  - name: "auth_with_valid_key"
    method: "client.authenticate(api_key)"
    expect: "no error, client is authenticated"
  - name: "auth_with_invalid_key"
    method: "client.authenticate('invalid')"
    expect: "AuthenticationError with status 401"
  - name: "list_resources_pagination"
    method: "client.resources.list(limit=2)"
    expect: "returns 2 items and has_more=true"
  - name: "retry_on_transient_error"
    method: "client.resources.get('id') with server returning 503 then 200"
    expect: "succeeds on retry, no error raised"
```

Each SDK implements these tests in its native test framework. CI for each SDK runs the full shared test suite. A top-level GitHub Actions workflow can run all SDK test suites in parallel.

### 4. Publish all SDKs with synchronized versioning

For coordinated releases across registries:

1. Use a monorepo or a central release script that tags all SDK repos simultaneously
2. Run `github-release-publish` for each repo
3. Each CI pipeline auto-publishes to its respective registry on tag
4. The n8n workflow from `sdk-registry-distribution` already tracks all registries -- verify new packages appear in the weekly report

### 5. A/B test SDK documentation and CTAs

Using `posthog-experiments` and `hypothesis-generation`:

Run experiments on SDK-specific variables:
- **README format:** Minimal (install + 5-line example) vs comprehensive (install + example + features + architecture)
- **CTA placement:** After quick start vs at the bottom
- **CTA copy:** "Try free" vs "Get API key" vs "See full docs"
- **Docs landing page:** Language-specific landing page vs unified SDK docs page

Test one variable at a time across all SDKs. Implement winners and apply the pattern to new SDKs.

### 6. Automate cross-registry monitoring

Extend the n8n download tracking workflow to:
1. Collect downloads from all registries for all languages
2. Calculate per-language download growth rate
3. Flag any SDK where downloads decline >20% week-over-week
4. Flag any SDK that hasn't had a release in >60 days (staleness risk)
5. Generate a matrix report: language x metric (downloads, CTAs, signups)

## Output

- 4+ SDKs published across major package registries
- Code generation pipeline from API spec to SDK code
- Shared test suite ensuring parity across all languages
- Synchronized release process
- A/B test results on SDK docs and CTAs
- Cross-registry monitoring covering all languages

## Triggers

- Run once to expand from 1-2 to 4+ languages
- Shared test suite runs on every PR to any SDK repo
- Cross-registry monitoring runs weekly
- Re-evaluate language priority quarterly based on demand data
