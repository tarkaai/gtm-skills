---
name: go-module-publish
description: Publish a Go module by tagging a release on GitHub and triggering the Go module proxy
tool: Go CLI
difficulty: Setup
---

# Go Module Publish

Publish a Go module by creating a tagged release. Go modules are distributed via their source repository (typically GitHub) and cached by the Go module proxy (proxy.golang.org).

## Tools

| Tool | Method | Docs |
|------|--------|------|
| git + GitHub CLI | Tag and release | https://go.dev/doc/modules/publishing |
| Go module proxy | Automatic indexing | https://proxy.golang.org/ |
| pkg.go.dev | Auto-generated docs | https://pkg.go.dev/about |

## Authentication

No registry authentication required. Go modules are published by pushing tagged commits to a public repository.

## Instructions

### 1. Configure go.mod for discoverability

```
module github.com/org/go-sdk

go 1.22

// No replace or retract directives on initial publish
```

The module path is the canonical import path. Use `github.com/org/go-sdk` format for GitHub-hosted modules.

### 2. Structure the repository

```
go-sdk/
  go.mod
  go.sum
  README.md           # Include CTA with utm_source=pkg-go-dev
  LICENSE              # MIT
  CHANGELOG.md
  client.go            # Main package code
  client_test.go       # Tests (pkg.go.dev shows test coverage)
  examples/
    basic/main.go      # Runnable example
  doc.go               # Package-level documentation comment
```

The `doc.go` file should contain a package-level comment that will appear on pkg.go.dev:

```go
// Package sdk provides a Go client for the Acme API.
//
// Quick start:
//
//   client := sdk.NewClient("your-api-key")
//   result, err := client.DoThing(ctx, sdk.ThingParams{...})
//
// For full documentation, visit https://yoursite.com/docs/sdk/go?utm_source=pkg-go-dev&utm_medium=registry&utm_campaign=go-sdk
package sdk
```

### 3. Tag and publish

```bash
# Ensure all tests pass
go test ./...

# Tag the release
git tag v1.0.0
git push origin v1.0.0

# Create a GitHub release (triggers visibility in GitHub and Go ecosystem)
gh release create v1.0.0 --title "v1.0.0" --notes "Initial release."
```

### 4. Trigger proxy indexing

```bash
# Request the Go proxy to fetch the module
curl "https://proxy.golang.org/github.com/org/go-sdk/@v/v1.0.0.info"

# Verify on pkg.go.dev (may take a few minutes)
# Visit: https://pkg.go.dev/github.com/org/go-sdk
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `module not found` on proxy | Tag not pushed or repo is private | Ensure the repo is public and the tag is pushed |
| `invalid version: unknown revision` | Tag doesn't match go.mod module path | Ensure `go.mod` module path matches the repo path |
| Docs not showing on pkg.go.dev | Proxy hasn't indexed yet | Request indexing via the curl command above; wait 15 minutes |

## Notes

- **Versioning:** Go enforces semantic versioning. Major version 2+ requires a `/v2` suffix in the module path.
- **Documentation:** pkg.go.dev auto-generates docs from Go doc comments. Write thorough doc comments on exported types and functions.
- **Retraction:** To retract a version, add a `retract` directive to go.mod and publish a new version.
