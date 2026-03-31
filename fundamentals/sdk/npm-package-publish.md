---
name: npm-package-publish
description: Publish or update a package on the npm registry with metadata optimized for discoverability
tool: Dev Tools
product: CLI
difficulty: Setup
---

# npm Package Publish

Publish a JavaScript/TypeScript package to the npm registry with metadata configured for maximum discoverability by developers searching for your solution category.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| npm CLI | `npm publish` | https://docs.npmjs.com/cli/v10/commands/npm-publish |
| npm API | `PUT /{package}` | https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md |
| GitHub Actions | `npm publish` in CI | https://docs.github.com/en/actions/publishing-packages/publishing-nodejs-packages |
| Yarn | `yarn npm publish` | https://yarnpkg.com/cli/npm/publish |
| pnpm | `pnpm publish` | https://pnpm.io/cli/publish |

## Authentication

- **npm CLI:** `npm login` or set `NPM_TOKEN` env var. For CI: create an automation token at https://www.npmjs.com/settings/~/tokens with "Automation" type.
- **Token in `.npmrc`:** `//registry.npmjs.org/:_authToken=${NPM_TOKEN}`

## Instructions

### 1. Configure package.json for discoverability

Ensure `package.json` contains search-optimized metadata:

```json
{
  "name": "@org/package-name",
  "version": "1.0.0",
  "description": "Verb-first description with primary search keyword. Example: 'Send transactional emails via the Acme API with retries, rate limiting, and TypeScript types.'",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "homepage": "https://yoursite.com/docs/sdk/node?utm_source=npm&utm_medium=registry&utm_campaign=node-sdk",
  "repository": {
    "type": "git",
    "url": "https://github.com/org/package-name.git"
  },
  "license": "MIT",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist"],
  "engines": { "node": ">=18" }
}
```

Rules for metadata:
- `name`: Use `@org/` scoped packages for brand recognition. The unscoped name should match the search term developers use.
- `description`: Under 255 characters. Start with a verb. Include the primary use case keyword.
- `keywords`: 5-15 keywords. Include: your product name, the problem domain, the API category, common synonyms, and framework names if applicable.
- `homepage`: Link to your SDK docs page with UTM parameters.
- `repository`: Link to the GitHub repo (drives trust signals).

### 2. Build and publish

```bash
# Build the package (TypeScript example)
npm run build

# Dry run to verify contents
npm publish --dry-run

# Publish to npm
npm publish --access public
```

For scoped packages, `--access public` is required on first publish (scoped packages default to private).

### 3. Verify publication

```bash
# Check the package exists on the registry
npm view @org/package-name

# Verify the README renders correctly
# Visit: https://www.npmjs.com/package/@org/package-name
```

## Response Format (API)

```json
{
  "ok": true,
  "id": "@org/package-name@1.0.0",
  "rev": "1-abc123"
}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` | Token lacks publish permission | Create an automation token with publish access |
| `402 Payment Required` | Trying to publish scoped private package on free plan | Add `--access public` flag |
| `403 Package name too similar` | Name conflicts with existing package | Choose a more distinct name or use a scope |
| `E409 version already exists` | Version number already published | Bump version in package.json |

## Notes

- **README on npm:** npm renders the repo's README.md as the package page. Include a CTA section in the README with UTM parameters using `utm_source=npm`.
- **Provenance:** Add `--provenance` flag when publishing from GitHub Actions to get a verified publisher badge.
- **Deprecation:** To deprecate a version: `npm deprecate @org/package-name@"<1.0.0" "Use v1.0.0 or later"`
