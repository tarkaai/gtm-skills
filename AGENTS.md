# AGENTS.md

Guidelines for AI agents working in this repository.

## Repository Overview

This repository contains **GTM play skills** for AI agents — 240 battle-tested B2B startup plays packaged for use with Claude Code, Cursor, Windsurf, n8n, and any MCP-compatible agent.

- **Name**: GTM Skills
- **GitHub**: [tarkaai/gtm-skills](https://github.com/tarkaai/gtm-skills)
- **Maintained by**: [Tarka](https://tarka.ai)
- **Playbook**: [tarka.ai/playbook](https://tarka.ai/playbook)
- **License**: MIT

## Repository Structure

The repo is organized into three skill layers: **Plays** (240 game plans), **Drills** (~40 practiced routines), and **Fundamentals** (~25 tool-specific core skills). Plays reference drills, drills reference fundamentals.

```
gtm-skills/
├── .claude-plugin/
│   └── marketplace.json   # Claude Code plugin marketplace manifest
├── bin/
│   └── gtm-skills.js      # npx CLI for install and config
├── scripts/
│   └── export.js          # Export plays from canonical data source
├── skills/                # GTM skills (3 layers)
│   ├── marketing/         # Plays — Marketing stage
│   │   ├── unaware/
│   │   ├── problem-aware/
│   │   ├── solution-aware/
│   │   └── product-aware/
│   ├── sales/             # Plays — Sales stage
│   │   ├── qualified/
│   │   ├── connected/
│   │   ├── aligned/
│   │   ├── proposed/
│   │   └── won/
│   ├── product/           # Plays — Product stage
│   │   ├── onboard/
│   │   ├── retain/
│   │   ├── upsell/
│   │   ├── referrals/
│   │   └── winback/
│   ├── drills/            # Drills — composite workflows
│   └── fundamentals/      # Fundamentals — tool-specific core skills
├── tools/
│   ├── crm/               # CRM-specific meta-skills
│   └── automation/        # Automation platform meta-skills
├── CLAUDE.md
├── VERSIONS.md
└── README.md
```

## Skill Structure

Each play lives at `skills/{stage}/{sub-stage}/{play-slug}/` and contains four level files:

```
skills/marketing/solution-aware/outbound-founder-email/
├── smoke.md      # Validate in ~1 week, free
├── baseline.md   # Prove repeatable results in ~2 weeks
├── scalable.md   # Scale 5–10× with automation over ~2 months
└── durable.md    # Agent-driven continuous improvement, 6+ months
```

### Frontmatter Fields

```yaml
---
name: play-name-level
description: >
  Short description of the play and what level this is.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, LinkedIn"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=3 replies from ICP prospects in 1 week"
---
```

## Stack Config

Before running any skill, check for `.gtm-config.json` in the project root or `~/.gtm-config.json` globally. This file specifies the user's tools (CRM, automation, email, enrichment, LinkedIn, scheduling). Substitute tool names throughout play instructions when this config exists.

If no config exists, prompt: "Run `npx gtm-skills init` to configure your stack, or tell me your CRM and automation platform."

## Level Progression Rule

Never skip levels. If a user asks to run Scalable without Baseline results, remind them to prove the play at Baseline first. A Smoke that misses its outcome is signal to iterate ICP, offer, or channel — not a failure.

## Checking for Updates

When using any skill from this repository:

1. **Once per session**, on first skill use, check for updates:
   - Fetch `VERSIONS.md` from GitHub: https://raw.githubusercontent.com/tarkaai/gtm-skills/main/VERSIONS.md
   - Compare versions against local skill files

2. **Only prompt if meaningful**:
   - 2 or more plays have updates, OR
   - Any play has a major version bump (e.g., 1.x to 2.x)

3. **Non-blocking notification** at end of response:
   ```
   ---
   Skills update available: X GTM plays have updates.
   Say "update skills" to update automatically, or run `git pull` in your gtm-skills folder.
   ```

4. **If user says "update skills"**:
   - Run `git pull` in the gtm-skills directory
   - Confirm what was updated

## Build / Lint / Test

Skills are content-only — no build step. Verify manually:
- YAML frontmatter is valid
- `name` field is present
- `level` matches one of: Smoke Test, Baseline, Scalable, Durable
- File is under 500 lines (move detail to references/ if needed)

## Git Workflow

### Branch Naming

- New plays: `feature/play-name`
- Improvements: `fix/play-name-description`
- Documentation: `docs/description`

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add play-name play`
- `fix: improve clarity in outbound-founder-email`
- `docs: update README`

### Pull Request Checklist

- [ ] Frontmatter is valid YAML
- [ ] All four level files present (smoke, baseline, scalable, durable)
- [ ] Play slug matches directory name
- [ ] No sensitive data or credentials

## Claude Code Plugin

This repo serves as a plugin marketplace. The manifest at `.claude-plugin/marketplace.json` lists all plays for installation via:

```bash
/plugin marketplace add tarkaai/gtm-skills
/plugin install gtm-skills
```

## Skill Categories

See `README.md` for the full list of plays organized by stage and sub-stage.
