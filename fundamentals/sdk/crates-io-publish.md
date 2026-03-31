---
name: crates-io-publish
description: Publish or update a Rust crate on crates.io with metadata optimized for discoverability
tool: cargo CLI
difficulty: Setup
---

# crates.io Publish

Publish a Rust crate to crates.io with metadata configured for developer discoverability.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| cargo | `cargo publish` | https://doc.rust-lang.org/cargo/commands/cargo-publish.html |
| crates.io API | REST API | https://crates.io/apidocs |
| GitHub Actions | `cargo publish` in CI | https://doc.rust-lang.org/cargo/reference/publishing.html |

## Authentication

- **cargo:** `cargo login <token>`. Get token at https://crates.io/settings/tokens
- **CI:** Set `CARGO_REGISTRY_TOKEN` env var.

## Instructions

### 1. Configure Cargo.toml for discoverability

```toml
[package]
name = "your-crate-name"
version = "1.0.0"
edition = "2021"
description = "Verb-first description with primary keyword."
license = "MIT"
repository = "https://github.com/org/rust-sdk"
homepage = "https://yoursite.com/docs/sdk/rust?utm_source=crates-io&utm_medium=registry&utm_campaign=rust-sdk"
documentation = "https://docs.rs/your-crate-name"
readme = "README.md"
keywords = ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
categories = ["api-bindings", "web-programming"]
```

Rules:
- `keywords`: Maximum 5 keywords on crates.io. Choose the 5 highest-value search terms.
- `categories`: Must be from the official list at https://crates.io/categories. Pick 1-2 relevant ones.

### 2. Build and publish

```bash
# Dry run to verify
cargo publish --dry-run

# Publish
cargo publish
```

### 3. Verify publication

```bash
cargo search your-crate-name
# Visit: https://crates.io/crates/your-crate-name
# Docs auto-generated at: https://docs.rs/your-crate-name
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `crate version already uploaded` | Version exists | Bump version in Cargo.toml |
| `this crate exists but you don't seem to be an owner` | No publish permission | Request ownership via `cargo owner --add <user>` |

## Notes

- **docs.rs:** crates.io auto-generates documentation at docs.rs. Ensure your doc comments are complete.
- **README:** crates.io renders README.md on the crate page. Include CTA with `utm_source=crates-io`.
- **Yanking:** `cargo yank --version 1.0.0` prevents new projects from depending on it but existing lockfiles still resolve.
