---
name: rubygems-publish
description: Publish or update a Ruby gem on RubyGems.org with metadata optimized for discoverability
tool: gem CLI
difficulty: Setup
---

# RubyGems Publish

Publish a Ruby gem to RubyGems.org with metadata configured for developer discoverability.

## Tools

| Tool | Method | Docs |
|------|--------|------|
| gem CLI | `gem push` | https://guides.rubygems.org/publishing/ |
| RubyGems API | `POST /api/v1/gems` | https://guides.rubygems.org/rubygems-org-api/ |
| GitHub Actions | `rubygems/release-gem` | https://github.com/rubygems/release-gem |
| Bundler | `bundle exec rake release` | https://bundler.io/guides/creating_gem.html |

## Authentication

- **gem CLI:** `gem signin` or set `GEM_HOST_API_KEY` env var. Get key at https://rubygems.org/profile/api_keys
- **CI:** Create a scoped API key with push permission for the specific gem.

## Instructions

### 1. Configure gemspec for discoverability

```ruby
Gem::Specification.new do |spec|
  spec.name          = "your-gem-name"
  spec.version       = "1.0.0"
  spec.summary       = "Verb-first summary with primary keyword."
  spec.description   = "Longer description with secondary keywords and use cases."
  spec.homepage      = "https://yoursite.com/docs/sdk/ruby?utm_source=rubygems&utm_medium=registry&utm_campaign=ruby-sdk"
  spec.license       = "MIT"
  spec.metadata = {
    "source_code_uri"   => "https://github.com/org/ruby-sdk",
    "changelog_uri"     => "https://github.com/org/ruby-sdk/blob/main/CHANGELOG.md",
    "documentation_uri" => "https://yoursite.com/docs/sdk/ruby",
    "homepage_uri"      => spec.homepage,
    "rubygems_mfa_required" => "true"
  }
  spec.required_ruby_version = ">= 3.1"
  spec.files = Dir["lib/**/*", "README.md", "LICENSE", "CHANGELOG.md"]
end
```

### 2. Build and publish

```bash
gem build your-gem-name.gemspec
gem push your-gem-name-1.0.0.gem
```

### 3. Verify publication

```bash
gem info your-gem-name --remote
# Visit: https://rubygems.org/gems/your-gem-name
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid or expired API key | Re-authenticate with `gem signin` |
| `Repushing of gem versions is not allowed` | Version already exists | Bump version number |
| `This gem name is reserved` | Name conflicts with reserved names | Choose a different name, optionally prefix with org |

## Notes

- **README on RubyGems:** RubyGems renders README.md as the gem landing page. Include CTA with `utm_source=rubygems`.
- **Yank:** To remove a version: `gem yank your-gem-name -v 1.0.0`
