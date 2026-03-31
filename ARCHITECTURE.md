# GTM Skills Architecture: From Plays to Executable Agent Skills

## The Problem

The 240 plays in the Tarka GTM Playbook are **high-level playbooks**, not **executable agent skills**. When a user runs `npx gtm-skills add marketing/unaware/cold-email-outreach` and tells Claude Code to execute the Smoke level, the agent has to figure out *how* to:

- Build a prospect list in Clay
- Write cold email copy that converts
- Set up Instantly sequences
- Track results in PostHog
- Log deals in Attio

Each of these is a complex workflow the agent can't reliably figure out on its own. The plays say *what* to do, not *how* to do it.

## The Solution: Skill Tree Architecture

```
                    ┌─────────────────────┐
                    │   PLAY SKILLS       │  ← 240 plays (leaves)
                    │   (what to do)      │     e.g., "Cold Email Outreach - Smoke"
                    └────────┬────────────┘
                             │ references
                    ┌────────┴────────────┐
                    │   WORKFLOW SKILLS   │  ← ~40 composites (branches)
                    │   (how to combine)  │     e.g., "Outbound Sequence Setup"
                    └────────┬────────────┘
                             │ references
                    ┌────────┴────────────┐
                    │   TOOL SKILLS       │  ← ~25 atomics (trunk)
                    │   (how to use X)    │     e.g., "Clay: Enrich Leads"
                    └─────────────────────┘
                             │ uses
                    ┌────────┴────────────┐
                    │   MCP SERVERS       │  ← External integrations
                    │   (API access)      │     e.g., attio-mcp, n8n-mcp
                    └─────────────────────┘
```

**Leaf skills** (plays) reference **branch skills** (workflows) which reference **trunk skills** (tool-specific). Users only pull what their config requires.

---

## Research Findings

### What Already Exists (Don't Rebuild)

| Layer | Source | Skills | Quality | Action |
|-------|--------|--------|---------|--------|
| **Clay** | ColdIQ GTM Skills | 9 sub-skills (enrichment, waterfalls, scoring, debugging) | HIGH | Fork + adapt |
| **Cold Email** | ColdIQ GTM Skills | 7 sub-skills (exec/IC messaging, personalization, follow-ups) | HIGH | Fork + adapt |
| **LinkedIn Ads** | ColdIQ GTM Skills + Claude Ads | 8+25 sub-skills | HIGH | Fork + adapt |
| **LinkedIn Content** | ColdIQ GTM Skills | 7 sub-skills (hooks, storytelling, scheduling) | HIGH | Fork + adapt |
| **n8n** | ColdIQ GTM Skills + n8n-skills repo | 6 sub-skills + dedicated repo | HIGH | Fork + adapt |
| **List Building** | ColdIQ GTM Skills | 6 sub-skills (ICP, sourcing, verification) | HIGH | Fork + adapt |
| **Signal Detection** | ColdIQ GTM Skills | 9 sub-skills (job changes, funding, hiring) | HIGH | Fork + adapt |
| **Google/Meta Ads** | Claude Ads (AgriciDaniel) | 74+46 audit checks | HIGH | Reference |
| **CRO** | Corey Haines Marketing Skills | 6 skills (page, signup, onboarding, forms) | HIGH | Reference |
| **SEO** | Corey Haines Marketing Skills | 6 skills (audit, AI SEO, programmatic) | HIGH | Reference |
| **PostHog** | Official MCP + docs | Full HogQL, flags, experiments | HIGH | Use MCP directly |
| **Attio** | Official MCP + community server | Deals, contacts, lists, tasks | HIGH | Use MCP directly |
| **Apollo** | Official Claude Connector | Search, enrich, sequence | HIGH | Use connector |

### What Needs to Be Built

| Skill | Why | Priority |
|-------|-----|----------|
| **Intercom: In-App Messaging** | 197 play-level refs, no existing skill | P0 |
| **Loops: Lifecycle Email** | 309 play-level refs, no existing skill | P0 |
| **PostHog: GTM Events Setup** | 849 refs but no GTM-specific event schema | P0 |
| **Attio: Pipeline Management** | 434 refs but no deal-flow skill | P0 |
| **n8n: GTM Workflow Templates** | Specific patterns for our plays, not generic | P1 |
| **Threshold & Guardrail Engine** | Every play uses pass/fail thresholds | P1 |
| **A/B Test Orchestrator** | 284 play-levels need this at Scale/Durable | P1 |
| **Meeting Booking Flow** | Cal.com + CRM sync, 31 refs | P2 |
| **Video Content Pipeline** | Loom/Descript/Riverside, 54 refs | P2 |
| **Ad Campaign Manager** | Google/LinkedIn/Meta setup, 30 refs | P2 |
| **Community Monitoring** | Discord/Slack engagement tracking | P2 |
| **Review/Listing Manager** | G2/Capterra/PH, 18 refs | P3 |

### Gaps Where No Skill or MCP Exists

| Tool | Status | Resolution |
|------|--------|------------|
| Clarify CRM | No MCP, no skill | Build MCP server or drop from recommendations |
| Mixpanel | No MCP, no skill | PostHog covers this; drop Mixpanel |
| Make.com | No MCP | n8n covers this; Make is the config alternative |
| Instantly | No MCP (API only) | Build lightweight skill wrapping API |
| Smartlead | MCP exists (116 tools) | Reference existing MCP |

---

## Detailed Architecture

### Layer 1: Trunk Skills (Tool-Specific, ~25 skills)

These teach the agent *how to use a specific tool*. Each is a standalone SKILL.md that can be installed independently.

```
skills/
  trunk/
    crm/
      attio/SKILL.md              ← Pipeline, deals, contacts, tasks, lists
      attio-mcp-setup/SKILL.md    ← Install + configure Attio MCP server
    enrichment/
      clay/SKILL.md               ← Fork of ColdIQ's 9 Clay sub-skills
      apollo/SKILL.md             ← Enrichment + sequence via official connector
    email/
      instantly/SKILL.md          ← Campaign setup, warmup, sequences
      smartlead/SKILL.md          ← Via MCP server
      loops/SKILL.md              ← NEW: Lifecycle emails, transactional, broadcasts
    automation/
      n8n/SKILL.md                ← Fork of ColdIQ's 6 n8n sub-skills
      n8n-mcp-setup/SKILL.md     ← Install + configure n8n MCP server
    analytics/
      posthog/SKILL.md            ← NEW: GTM event schema, funnels, cohorts
      posthog-mcp-setup/SKILL.md  ← Install + configure PostHog MCP
    messaging/
      intercom/SKILL.md           ← NEW: In-app messages, tours, bots, articles
    social/
      linkedin-organic/SKILL.md   ← Fork of ColdIQ LinkedIn Creator
      linkedin-ads/SKILL.md       ← Fork of ColdIQ + Claude Ads
    ads/
      google-ads/SKILL.md         ← Reference Claude Ads (74 checks)
      meta-ads/SKILL.md           ← Reference Claude Ads (46 checks)
    video/
      loom/SKILL.md               ← Recording, sharing, tracking views
      descript/SKILL.md           ← Editing, transcription, clips
    scheduling/
      calcom/SKILL.md             ← Event types, booking links, CRM sync
    content/
      ghost/SKILL.md              ← Blog publishing, newsletters
      webflow/SKILL.md            ← Landing pages, CMS
    sales/
      gong/SKILL.md               ← Call recording, deal intelligence
      fireflies/SKILL.md          ← Meeting transcription, action items
    ai/
      anthropic/SKILL.md          ← Claude API patterns for GTM agents
      openai/SKILL.md             ← OpenAI API patterns for GTM agents
```

### Layer 2: Branch Skills (Workflow Composites, ~40 skills)

These combine trunk skills into reusable workflows. They reference trunk skills by path.

```
skills/
  branch/
    prospecting/
      build-prospect-list/SKILL.md     ← Clay + Apollo → Attio (uses trunk/enrichment/clay, trunk/crm/attio)
      enrich-and-score/SKILL.md        ← Clay waterfall + scoring
      signal-detection/SKILL.md        ← Fork of ColdIQ Signal Sourcer
      icp-definition/SKILL.md          ← Fork of ColdIQ List Architect ICP
    outreach/
      cold-email-sequence/SKILL.md     ← Instantly/Smartlead setup + copy (uses trunk/email/instantly)
      linkedin-outreach/SKILL.md       ← Connection + message sequence
      warm-intro-request/SKILL.md      ← Partner mapping + intro ask
      follow-up-automation/SKILL.md    ← n8n workflow for multi-touch
    content/
      social-content-pipeline/SKILL.md ← Create + schedule + track
      blog-seo-pipeline/SKILL.md       ← Write + publish + track
      video-content-pipeline/SKILL.md  ← Record + edit + distribute
      case-study-creation/SKILL.md     ← Interview + write + publish
    product/
      onboarding-flow/SKILL.md         ← Intercom tours + Loops emails + PostHog tracking
      feature-announcement/SKILL.md    ← In-app + email + changelog
      churn-prevention/SKILL.md        ← Usage signals → intervention
      nps-feedback-loop/SKILL.md       ← Survey → analysis → action
      upgrade-prompt/SKILL.md          ← Usage threshold → upsell
      referral-program/SKILL.md        ← Program setup + tracking
      winback-campaign/SKILL.md        ← Churn signal → re-engagement
    events/
      webinar-pipeline/SKILL.md        ← Setup + promote + follow-up
      meetup-pipeline/SKILL.md         ← Organize + track + convert
    paid/
      ad-campaign-setup/SKILL.md       ← Platform setup + tracking
      landing-page-pipeline/SKILL.md   ← Build + test + optimize
      retargeting-setup/SKILL.md       ← Pixel + audience + campaign
    measurement/
      posthog-gtm-events/SKILL.md      ← Standard event schema for all GTM plays
      threshold-engine/SKILL.md        ← Pass/fail thresholds + guardrails
      ab-test-orchestrator/SKILL.md    ← Hypothesis → test → analyze → decide
      dashboard-builder/SKILL.md       ← PostHog dashboard templates per motion
    operations/
      crm-pipeline-setup/SKILL.md      ← Attio pipeline + stages + automation
      meeting-booking-flow/SKILL.md    ← Cal.com + CRM + notifications
      tool-sync-workflow/SKILL.md      ← n8n patterns for connecting tools
```

### Layer 3: Leaf Skills (Plays, 240 existing skills — rewritten)

Each play SKILL.md is rewritten to **reference** branch and trunk skills instead of giving vague instructions. Example transformation:

**Before (current Smoke level):**
```markdown
## Instructions
1. Define your ICP. List 3-5 companies that fit.
2. Write 3 cold email variants. Test subject lines.
3. Send 20 emails manually. Track opens and replies.
4. Log results in your CRM. Compare to threshold.
```

**After (referencing building blocks):**
```markdown
## Instructions

### 1. Build your prospect list
Run `/icp-definition` to define your Ideal Customer Profile, then use
`/build-prospect-list` to source 20 contacts matching your ICP.

### 2. Write outreach
Run `/cold-email-sequence` with `--level smoke --count 3` to generate
3 email variants optimized for founder-led outreach.

### 3. Execute manually
Send the 20 emails manually (Smoke level is always manual execution).
Log each send in `/attio` with status and response.

### 4. Measure results
Run `/threshold-engine check` against your Smoke threshold:
- Pass: ≥ 2 meetings from 20 emails
- If pass → proceed to Baseline level
- If fail → adjust ICP or messaging, re-run Smoke
```

### Config-Driven Skill Resolution

The `.gtm-config.json` determines which trunk skills are pulled:

```json
{
  "crm": "attio",           // → trunk/crm/attio
  "automation": "n8n",       // → trunk/automation/n8n
  "email_cold": "instantly",  // → trunk/email/instantly (alt: smartlead)
  "email_lifecycle": "loops", // → trunk/email/loops
  "enrichment": "clay",      // → trunk/enrichment/clay (alt: apollo)
  "analytics": "posthog",    // → trunk/analytics/posthog
  "messaging": "intercom",   // → trunk/messaging/intercom
  "video": "loom",           // → trunk/video/loom (alt: descript)
  "social": "linkedin",      // → trunk/social/linkedin-organic
  "scheduling": "calcom",    // → trunk/scheduling/calcom
  "ads": ["google", "linkedin"] // → trunk/ads/google-ads, trunk/ads/linkedin-ads
}
```

**Resolution logic in `bin/gtm-skills.js`:**
1. Read `.gtm-config.json`
2. For each play being installed, resolve its branch skill references
3. For each branch skill, resolve its trunk skill references
4. Only copy trunk skills that match the user's config
5. If a play references `email_cold` and user has `"email_cold": "smartlead"`, pull `trunk/email/smartlead` instead of `trunk/email/instantly`

**The `init` command walks the user through this:**
```
$ npx gtm-skills init

What CRM do you use?
  ● Attio (recommended)  ○ HubSpot  ○ Salesforce  ○ Pipedrive

What's your automation platform?
  ● n8n (recommended)  ○ Make  ○ Claude Code only

Cold email tool?
  ● Instantly  ○ Smartlead  ○ None (manual only)

...
```

---

## The Two Stacks

The research revealed two distinct tool stacks that map cleanly to the tree:

### Stack A: Outbound/Sales/Marketing (131 plays, 8 motions)
```
Trunk:  Attio + Clay + Instantly + PostHog + n8n
Branch: prospecting/* + outreach/* + content/* + events/* + paid/*
Leaf:   Marketing + Sales stage plays
```

### Stack B: Product/Retention (109 plays, LeadCaptureSurface motion)
```
Trunk:  Intercom + Loops + OpenAI + PostHog + n8n
Branch: product/* + measurement/*
Leaf:   Product stage plays (Onboard, Retain, Upsell, Referrals, Winback)
```

Both share `PostHog + n8n + measurement/*` as the common data/automation layer.

---

## Level Progression in the Skill Tree

The level system maps perfectly to which layers of the tree are active:

| Level | Trunk Skills Used | Branch Skills Used | Agent Autonomy |
|-------|-------------------|--------------------|----------------|
| **Smoke** | PostHog (54%), Attio (41%) | threshold-engine, icp-definition | Manual execution, agent assists |
| **Baseline** | +Clay, +email tool, +Loops | +build-prospect-list, +cold-email-sequence | Agent sets up tools, human executes |
| **Scalable** | +n8n (100%), +Intercom | +follow-up-automation, +tool-sync-workflow, +ab-test | Agent builds workflows, runs them |
| **Durable** | +Anthropic, +OpenAI, +Gong | +dashboard-builder, all monitoring branches | Agent runs autonomously with guardrails |

**Key insight:** The skill tree naturally prunes at lower levels. Smoke only needs 2-3 trunk skills. Durable needs the full tree. The `--level` flag on install should control this:

```bash
npx gtm-skills add marketing/unaware/cold-email --level smoke
# Only installs: trunk/analytics/posthog, trunk/crm/attio, branch/measurement/threshold-engine

npx gtm-skills add marketing/unaware/cold-email --level scalable
# Additionally installs: trunk/enrichment/clay, trunk/email/instantly, trunk/automation/n8n,
# branch/prospecting/*, branch/outreach/*, branch/measurement/ab-test-orchestrator
```

---

## External Skill References

Some trunk skills should reference (not fork) existing high-quality skills:

| Our Skill | References | How |
|-----------|-----------|-----|
| `trunk/enrichment/clay` | ColdIQ Clay Expert (9 sub-skills) | Fork into our repo, adapt for our config system |
| `trunk/social/linkedin-organic` | ColdIQ LinkedIn Creator (7 sub-skills) | Fork + adapt |
| `trunk/automation/n8n` | ColdIQ n8n Architect (6 sub-skills) + czlonkowski/n8n-skills | Fork + adapt |
| `trunk/ads/google-ads` | Claude Ads (74 checks) | Reference via `npx skills add AgriciDaniel/claude-ads` |
| `trunk/ads/meta-ads` | Claude Ads (46 checks) | Same reference |
| `branch/content/blog-seo-pipeline` | Corey Haines SEO skills (6) | Reference via skills.sh |
| `branch/product/onboarding-flow` | Corey Haines CRO skills (6) | Reference via skills.sh |

**Reference format in SKILL.md:**
```markdown
## Dependencies

This skill requires the following. Install if not present:
- `npx skills add sachacoldiq/ColdIQ-s-GTM-Skills` (Clay enrichment sub-skills)
- Attio MCP server: `npx attio-mcp-server init`
- PostHog MCP server: configured in `.claude/settings.json`
```

---

## Website Integration

The playbook website should surface the skill tree:

1. **On each play detail page (`/playbook/[slug]`):**
   - Show "Building Block Skills" section listing the branch/trunk skills this play uses
   - Visual tree diagram showing the dependency chain
   - "What you'll need" based on the play's level

2. **New `/playbook/skills` page:**
   - Browse the full skill tree (trunk → branch → leaf)
   - Filter by tool, by motion, by level
   - Each skill shows: description, dependencies, which plays use it, install command

3. **On the intro section:**
   - Explain the tree concept: "Each play is built on tested building-block skills"
   - Link to the skills tree page

---

## Implementation Plan

### Phase 1: Foundation (Week 1-2)
**Goal:** Ship the P0 trunk skills and the config resolution system.

1. **Build the 6 P0 trunk skills:**
   - `trunk/analytics/posthog` — GTM event schema (track, identify, group events for all play types)
   - `trunk/crm/attio` — Pipeline setup, deal flow, contact management patterns
   - `trunk/email/loops` — Lifecycle email setup, transactional templates, broadcasts
   - `trunk/messaging/intercom` — In-app messages, product tours, help articles
   - `trunk/email/instantly` — Warmup, campaign creation, sequence management
   - `trunk/enrichment/clay` — Fork ColdIQ's 9 Clay sub-skills, adapt to our config format

2. **Build config resolution in `bin/gtm-skills.js`:**
   - `init` command with interactive CRM/tool selection
   - `install` resolves skill dependencies based on config
   - `add` with `--level` flag to control tree depth
   - Dependency graph walker that only pulls needed trunk/branch skills

3. **Build the 4 P0 branch skills:**
   - `branch/measurement/threshold-engine` — Universal pass/fail + guardrail system
   - `branch/measurement/posthog-gtm-events` — Standard event taxonomy
   - `branch/prospecting/build-prospect-list` — Clay + Apollo → Attio flow
   - `branch/outreach/cold-email-sequence` — Copy generation + Instantly/Smartlead setup

4. **Test with Claude Code sessions:**
   - Run 3 Smoke-level plays end-to-end with Claude Code
   - Verify the agent can follow the skill references
   - Document failures and adjust skill instructions

### Phase 2: Outbound Stack (Week 3-4)
**Goal:** Complete Stack A (131 plays usable with full skill tree).

5. **Fork and adapt ColdIQ skills:**
   - Signal detection (9 sub-skills)
   - LinkedIn Creator (7 sub-skills)
   - n8n Architect (6 sub-skills)
   - List Architect (6 sub-skills)
   - Cold Email Strategist (7 sub-skills)

6. **Build remaining outbound branch skills:**
   - `branch/outreach/linkedin-outreach`
   - `branch/outreach/follow-up-automation`
   - `branch/outreach/warm-intro-request`
   - `branch/content/social-content-pipeline`
   - `branch/events/webinar-pipeline`
   - `branch/paid/ad-campaign-setup`
   - `branch/measurement/ab-test-orchestrator`

7. **Rewrite 20 representative play skills** (leaves) to reference branch skills
   - Pick 2-3 plays per motion, cover all 4 levels
   - Test each with Claude Code

### Phase 3: Product Stack (Week 5-6)
**Goal:** Complete Stack B (109 plays usable with full skill tree).

8. **Build product branch skills:**
   - `branch/product/onboarding-flow`
   - `branch/product/feature-announcement`
   - `branch/product/churn-prevention`
   - `branch/product/nps-feedback-loop`
   - `branch/product/upgrade-prompt`
   - `branch/product/referral-program`
   - `branch/product/winback-campaign`

9. **Build remaining trunk skills:**
   - `trunk/video/loom`, `trunk/video/descript`
   - `trunk/scheduling/calcom`
   - `trunk/sales/gong`, `trunk/sales/fireflies`
   - `trunk/content/ghost`, `trunk/content/webflow`

10. **Rewrite remaining 220 play skills** to reference building blocks

### Phase 4: Polish & Ship (Week 7-8)
**Goal:** Full system tested and documented.

11. **Website integration:**
    - Build `/playbook/skills` tree browser page
    - Add "Building Block Skills" section to `/playbook/[slug]`
    - Update intro to explain the skill tree concept

12. **Automated testing:**
    - Script that validates all skill references resolve correctly
    - CI check that every play references existing branch/trunk skills
    - Integration tests: `npx gtm-skills add <play> --level <X>` produces correct file set

13. **Documentation:**
    - Update AGENTS.md with skill tree architecture
    - Update CLAUDE.md with how to navigate the tree
    - Write "Contributing a Skill" guide for community

14. **Release v0.2.0** with the full skill tree

---

## Testing Strategy

### Unit Tests (automated, run in CI)
- Every SKILL.md has valid frontmatter (name, description)
- Every play skill's branch/trunk references resolve to existing files
- Config resolution produces correct skill sets for all config combinations
- `--level` flag correctly prunes the dependency tree

### Integration Tests (Claude Code sessions)
- Run 1 play per motion at Smoke level → verify agent can execute
- Run 1 play per motion at Scalable level → verify automation workflows work
- Run 1 play at Durable level → verify agent monitoring loop works
- Test with different configs (Attio vs HubSpot, Instantly vs Smartlead)

### Acceptance Criteria
- Agent can execute a Smoke play with < 2 clarifying questions
- Agent can set up a Scalable workflow without human intervention
- Durable-level agent correctly detects metric drops and takes action
- Switching config (e.g., Instantly → Smartlead) produces working skills with zero manual changes

---

## Open Questions

1. **License for forked skills:** ColdIQ's repo is public but has no explicit license. Need to verify we can fork and adapt. If not, build from scratch using their architecture as inspiration.

2. **MCP server management:** Should `npx gtm-skills init` also install MCP servers (attio-mcp, posthog-mcp, n8n-mcp)? Or leave that to the user?

3. **Skill versioning:** When we update a trunk skill (e.g., improve the Clay enrichment workflow), how do installed copies get updated? VERSIONS.md tracks this but the update mechanism needs design.

4. **Community contributions:** Should the skill tree be open for community-contributed trunk/branch skills? If so, what's the review process?

5. **Pricing:** Are all skills free (MIT)? Or do some advanced Durable-level skills require a Tarka subscription?
