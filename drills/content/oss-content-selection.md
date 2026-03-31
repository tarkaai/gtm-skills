---
name: oss-content-selection
description: Research, score, and select the highest-impact internal code, tool, dataset, or template to release as open source for GTM leverage
category: Content
tools:
  - Attio
  - Clay
  - GitHub CLI
fundamentals:
  - attio-lists
  - clay-company-search
  - clay-claygent
  - github-traffic-api
  - competitor-changelog-monitoring
  - news-signal-search
---

# OSS Content Selection

Determine which internal asset to release as open source for maximum GTM impact. The goal is NOT to open-source your core product -- it is to extract a self-contained utility, library, dataset, template set, or tool that your ICP needs, that demonstrates your domain expertise, and that creates a natural bridge to your paid offering.

## Input

- ICP definition (from `icp-definition` drill): target titles, company sizes, pain points, tech stacks
- Internal inventory: list of internal tools, scripts, libraries, datasets, config files, templates your team uses
- Competitive landscape: what competitors and adjacent companies have open-sourced

## Steps

### 1. Audit your internal inventory

Catalog every internal asset that could theoretically be extracted and published:

- **Scripts and CLIs:** Build scripts, deployment helpers, data migration tools, testing utilities
- **Libraries:** Abstractions you built over common problems (auth wrappers, API clients, data transformers)
- **Templates:** Config files, infrastructure-as-code modules, design system components, workflow definitions
- **Datasets:** Anonymized benchmark data, industry surveys, taxonomy lists, lookup tables
- **Guides as code:** Runbooks, playbooks, or checklists implemented as executable scripts or structured YAML/JSON

For each asset, record: what it does, what language/framework, how self-contained it is (standalone vs. tightly coupled to your product), and how many hours to extract and clean up.

### 2. Research what the ICP searches for

Using the `clay-claygent` fundamental, research 30 companies matching your ICP. For each, ask: "What open-source tools, libraries, or templates does {Company} use or contribute to in the {your domain} space? What problems do their engineers post about on GitHub Issues, Stack Overflow, or forums?"

Aggregate into a frequency table of unmet needs, pain points, and tooling gaps.

Cross-reference with GitHub search to find demand signals:

```bash
# Find repos in your domain with high stars but low maintenance
gh search repos "{domain keyword}" --sort stars --limit 30 --json fullName,stargazersCount,pushedAt,description

# Find issues across repos that indicate unmet needs
gh search issues "{pain point keyword}" --sort reactions-+1 --limit 30 --json title,repository,reactions
```

### 3. Score competing OSS releases

Using `competitor-changelog-monitoring` fundamental, identify what competitors and adjacent companies have already open-sourced. For each:

- Star count and growth trajectory (use `github-traffic-api` on public repos)
- Last commit date (active vs. abandoned)
- Issues open vs. closed ratio (community health)
- Gap analysis: what do users request in issues that the project does not provide?

Using `news-signal-search`, check recent launches on Hacker News, Product Hunt, and dev.to for open-source releases in your domain. Note which topics and formats get traction.

### 4. Score each candidate asset

For each internal asset from Step 1, score on five dimensions (1-5 each):

| Dimension | 1 (Low) | 5 (High) |
|-----------|---------|----------|
| **ICP demand** | Nobody searches for this | Top unmet need from Step 2 |
| **Uniqueness** | Many alternatives exist | No good OSS alternative |
| **Bridge to product** | No connection to your paid offering | Natural upgrade path |
| **Extraction cost** | Weeks to decouple and document | Already self-contained |
| **Maintenance burden** | Requires constant updates | Stable, rarely needs changes |

Total score = sum of all 5 dimensions. Rank candidates by total score.

### 5. Validate the top candidate

For the highest-scoring candidate:

1. Confirm it contains no proprietary secrets, customer data, or licensed third-party code that cannot be open-sourced
2. Confirm it can run standalone without your product (critical -- the OSS asset must deliver value independently)
3. Confirm you can write a Quick Start that works in under 5 minutes from a fresh clone
4. Estimate: how many hours to extract, document, and publish? If over 40 hours, consider the second-ranked candidate instead.

**Human action required:** Legal/IP review of the candidate asset before proceeding. Confirm MIT license is acceptable.

### 6. Define the CTA bridge

Document exactly how this OSS asset connects to your paid product:

- What does the OSS asset do alone?
- What additional value does the paid product provide on top of it?
- What is the natural moment when a user of the OSS asset would want the paid product?

This bridge informs the README CTA, blog post positioning, and community messaging. The CTA should never feel like a bait-and-switch -- the OSS asset must deliver genuine standalone value.

## Output

- Ranked list of candidate OSS assets with scores
- Selected asset with extraction plan (hours, dependencies, cleanup needed)
- CTA bridge document: what the OSS asset does alone vs. what the paid product adds
- Legal clearance status

## Triggers

Run once at Smoke level. Re-run quarterly at Scalable/Durable levels to identify the next asset to release.
