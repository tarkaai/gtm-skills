# GTM Skills Architecture: From Plays to Executable Agent Skills

## The Problem

The 240 plays in the Tarka GTM Playbook are **high-level playbooks**, not **executable agent skills**. When a user runs `npx gtm-skills add marketing/unaware/cold-email-outreach` and tells Claude Code to execute the Smoke level, the agent has to figure out *how* to:

- Build a prospect list in Clay
- Write cold email copy that converts
- Set up Instantly sequences
- Track results in PostHog
- Log deals in Attio

Each of these is a complex workflow the agent can't reliably figure out on its own. The plays say *what* to do, not *how* to do it.

## The Solution: Plays, Drills & Fundamentals

```
                    ┌─────────────────────┐
                    │       PLAYS         │  ← 240 plays (what to run)
                    │   (what to do)      │     e.g., "Cold Email Outreach - Smoke"
                    └────────┬────────────┘
                             │ references
                    ┌────────┴────────────┐
                    │       DRILLS        │  ← ~40 practiced routines
                    │  (how to combine)   │     e.g., "Outbound Sequence Setup"
                    └────────┬────────────┘
                             │ references
                    ┌────────┴────────────┐
                    │   FUNDAMENTALS      │  ← ~25 core tool skills
                    │   (how to use X)    │     e.g., "Clay: Enrich Leads"
                    └─────────────────────┘
                             │ uses
                    ┌────────┴────────────┐
                    │   MCP SERVERS       │  ← External integrations
                    │   (API access)      │     e.g., attio-mcp, n8n-mcp
                    └─────────────────────┘
```

**Plays** (240) reference **Drills** (~40 practiced routines) which reference **Fundamentals** (~25 tool-specific core skills). Users only pull what their config requires.

---

## Research Findings

### What Already Exists (Internalized)

We've internalized battle-tested patterns from the community into our own self-contained skill definitions. No external skill repos are required — everything lives in this repo.

| Layer | Coverage | Skills | Status |
|-------|----------|--------|--------|
| **Clay** | Enrichment, waterfalls, scoring, debugging | 9 sub-skills | Internalized from community best practices |
| **Cold Email** | Exec/IC messaging, personalization, follow-ups | 7 sub-skills | Internalized from community best practices |
| **LinkedIn Ads** | Campaign setup, targeting, optimization | 33 sub-skills | Internalized from community best practices |
| **LinkedIn Content** | Hooks, storytelling, scheduling | 7 sub-skills | Internalized from community best practices |
| **n8n** | Workflow patterns, triggers, error handling | 6 sub-skills | Internalized from community best practices |
| **List Building** | ICP, sourcing, verification | 6 sub-skills | Internalized from community best practices |
| **Signal Detection** | Job changes, funding, hiring signals | 9 sub-skills | Internalized from community best practices |
| **Google/Meta Ads** | Audit checks, campaign structure | 120 checks | Internalized from community best practices |
| **CRO** | Page, signup, onboarding, forms | 6 skills | Internalized from community best practices |
| **SEO** | Audit, AI SEO, programmatic | 6 skills | Internalized from community best practices |
| **PostHog** | Full HogQL, flags, experiments | Full coverage | Use MCP directly |
| **Attio** | Deals, contacts, lists, tasks | Full coverage | Use MCP directly |
| **Apollo** | Search, enrich, sequence | Full coverage | Use connector |

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

### Layer 1: Fundamentals (Tool-Specific Core Skills, ~25 skills)

These teach the agent *how to use a specific tool*. Each is a standalone SKILL.md that can be installed independently.

```
skills/
  fundamentals/
    crm/
      attio/SKILL.md              ← Pipeline, deals, contacts, tasks, lists
      attio-mcp-setup/SKILL.md    ← Install + configure Attio MCP server
    enrichment/
      clay/SKILL.md               ← 9 Clay sub-skills (enrichment, waterfalls, scoring, debugging)
      apollo/SKILL.md             ← Enrichment + sequence via official connector
    email/
      instantly/SKILL.md          ← Campaign setup, warmup, sequences
      smartlead/SKILL.md          ← Via MCP server
      loops/SKILL.md              ← NEW: Lifecycle emails, transactional, broadcasts
    automation/
      n8n/SKILL.md                ← 6 n8n sub-skills (workflow patterns, triggers, error handling)
      n8n-mcp-setup/SKILL.md     ← Install + configure n8n MCP server
    analytics/
      posthog/SKILL.md            ← NEW: GTM event schema, funnels, cohorts
      posthog-mcp-setup/SKILL.md  ← Install + configure PostHog MCP
    messaging/
      intercom/SKILL.md           ← NEW: In-app messages, tours, bots, articles
    social/
      linkedin-organic/SKILL.md   ← LinkedIn content creation (hooks, storytelling, scheduling)
      linkedin-ads/SKILL.md       ← LinkedIn ad campaigns (targeting, optimization)
    ads/
      google-ads/SKILL.md         ← Google Ads audit & campaign management (74 checks)
      meta-ads/SKILL.md           ← Meta Ads audit & campaign management (46 checks)
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

### Layer 2: Drills (Practiced Routines, ~40 skills)

These combine fundamentals into reusable workflows. They reference fundamentals by path.

```
skills/
  drills/
    prospecting/
      build-prospect-list/SKILL.md     ← Clay + Apollo → Attio (uses fundamentals/enrichment/clay, fundamentals/crm/attio)
      enrich-and-score/SKILL.md        ← Clay waterfall + scoring
      signal-detection/SKILL.md        ← Signal sourcing (job changes, funding, hiring)
      icp-definition/SKILL.md          ← ICP definition and validation
    outreach/
      cold-email-sequence/SKILL.md     ← Instantly/Smartlead setup + copy (uses fundamentals/email/instantly)
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

### Layer 3: Plays (240 existing plays — rewritten)

Each play SKILL.md is rewritten to **reference** drills and fundamentals instead of giving vague instructions. Example transformation:

**Before (current Smoke level):**
```markdown
## Instructions
1. Define your ICP. List 3-5 companies that fit.
2. Write 3 cold email variants. Test subject lines.
3. Send 20 emails manually. Track opens and replies.
4. Log results in your CRM. Compare to threshold.
```

**After (referencing drills):**
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

The `.gtm-config.json` determines which fundamentals are pulled:

```json
{
  "crm": "attio",           // → fundamentals/crm/attio
  "automation": "n8n",       // → fundamentals/automation/n8n
  "email_cold": "instantly",  // → fundamentals/email/instantly (alt: smartlead)
  "email_lifecycle": "loops", // → fundamentals/email/loops
  "enrichment": "clay",      // → fundamentals/enrichment/clay (alt: apollo)
  "analytics": "posthog",    // → fundamentals/analytics/posthog
  "messaging": "intercom",   // → fundamentals/messaging/intercom
  "video": "loom",           // → fundamentals/video/loom (alt: descript)
  "social": "linkedin",      // → fundamentals/social/linkedin-organic
  "scheduling": "calcom",    // → fundamentals/scheduling/calcom
  "ads": ["google", "linkedin"] // → fundamentals/ads/google-ads, fundamentals/ads/linkedin-ads
}
```

**Resolution logic in `bin/gtm-skills.js`:**
1. Read `.gtm-config.json`
2. For each play being installed, resolve its drill references
3. For each drill, resolve its fundamental references
4. Only copy fundamentals that match the user's config
5. If a play references `email_cold` and user has `"email_cold": "smartlead"`, pull `fundamentals/email/smartlead` instead of `fundamentals/email/instantly`

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

The research revealed two distinct tool stacks that map cleanly to the three layers:

### Stack A: Outbound/Sales/Marketing (131 plays, 8 motions)
```
Fundamentals:  Attio + Clay + Instantly + PostHog + n8n
Drills:        prospecting/* + outreach/* + content/* + events/* + paid/*
Plays:         Marketing + Sales stage plays
```

### Stack B: Product/Retention (109 plays, LeadCaptureSurface motion)
```
Fundamentals:  Intercom + Loops + OpenAI + PostHog + n8n
Drills:        product/* + measurement/*
Plays:         Product stage plays (Onboard, Retain, Upsell, Referrals, Winback)
```

Both share `PostHog + n8n + measurement/*` as the common data/automation layer.

---

## Level Progression in the Skill Tree

The level system maps perfectly to which layers of the tree are active:

| Level | Fundamentals Used | Drills Used | Agent Autonomy |
|-------|-------------------|-------------|----------------|
| **Smoke** | PostHog (54%), Attio (41%) | threshold-engine, icp-definition | Manual execution, agent assists |
| **Baseline** | +Clay, +email tool, +Loops | +build-prospect-list, +cold-email-sequence | Agent sets up tools, human executes |
| **Scalable** | +n8n (100%), +Intercom | +follow-up-automation, +tool-sync-workflow, +ab-test | Agent builds workflows, runs them |
| **Durable** | +Anthropic, +OpenAI, +Gong | +dashboard-builder, all monitoring drills | Agent runs autonomously with guardrails |

**Key insight:** The skill tree naturally prunes at lower levels. Smoke only needs 2-3 fundamentals. Durable needs the full tree. The `--level` flag on install should control this:

```bash
npx gtm-skills add marketing/unaware/cold-email --level smoke
# Only installs: fundamentals/analytics/posthog, fundamentals/crm/attio, drills/measurement/threshold-engine

npx gtm-skills add marketing/unaware/cold-email --level scalable
# Additionally installs: fundamentals/enrichment/clay, fundamentals/email/instantly, fundamentals/automation/n8n,
# drills/prospecting/*, drills/outreach/*, drills/measurement/ab-test-orchestrator
```

---

## Website Integration

The playbook website should surface the skill tree:

1. **On each play detail page (`/playbook/[slug]`):**
   - Show "Drills & Fundamentals" section listing the drills/fundamentals this play uses
   - Visual tree diagram showing the dependency chain
   - "What you'll need" based on the play's level

2. **New `/playbook/skills` page:**
   - Browse the full skill tree (Fundamentals → Drills → Plays)
   - Filter by tool, by motion, by level
   - Each skill shows: description, dependencies, which plays use it, install command

3. **On the intro section:**
   - Explain the three layers: "Each play is built on practiced drills and mastered fundamentals"
   - Link to the skills tree page

---

## Implementation Plan

### Phase 1: Foundation (Week 1-2)
**Goal:** Ship the P0 fundamentals and the config resolution system.

1. **Build the 6 P0 fundamentals:**
   - `fundamentals/analytics/posthog` — GTM event schema (track, identify, group events for all play types)
   - `fundamentals/crm/attio` — Pipeline setup, deal flow, contact management patterns
   - `fundamentals/email/loops` — Lifecycle email setup, transactional templates, broadcasts
   - `fundamentals/messaging/intercom` — In-app messages, product tours, help articles
   - `fundamentals/email/instantly` — Warmup, campaign creation, sequence management
   - `fundamentals/enrichment/clay` — 9 Clay sub-skills, adapted to our config format

2. **Build config resolution in `bin/gtm-skills.js`:**
   - `init` command with interactive CRM/tool selection
   - `install` resolves skill dependencies based on config
   - `add` with `--level` flag to control tree depth
   - Dependency graph walker that only pulls needed fundamentals/drills

3. **Build the 4 P0 drills:**
   - `drills/measurement/threshold-engine` — Universal pass/fail + guardrail system
   - `drills/measurement/posthog-gtm-events` — Standard event taxonomy
   - `drills/prospecting/build-prospect-list` — Clay + Apollo → Attio flow
   - `drills/outreach/cold-email-sequence` — Copy generation + Instantly/Smartlead setup

4. **Test with Claude Code sessions:**
   - Run 3 Smoke-level plays end-to-end with Claude Code
   - Verify the agent can follow the skill references
   - Document failures and adjust skill instructions

### Phase 2: Outbound Stack (Week 3-4)
**Goal:** Complete Stack A (131 plays usable with full skill tree).

5. **Build internalized outbound skills:**
   - Signal detection (9 sub-skills)
   - LinkedIn content creation (7 sub-skills)
   - n8n workflow patterns (6 sub-skills)
   - List building (6 sub-skills)
   - Cold email strategy (7 sub-skills)

6. **Build remaining outbound drills:**
   - `drills/outreach/linkedin-outreach`
   - `drills/outreach/follow-up-automation`
   - `drills/outreach/warm-intro-request`
   - `drills/content/social-content-pipeline`
   - `drills/events/webinar-pipeline`
   - `drills/paid/ad-campaign-setup`
   - `drills/measurement/ab-test-orchestrator`

7. **Rewrite 20 representative plays** to reference drills
   - Pick 2-3 plays per motion, cover all 4 levels
   - Test each with Claude Code

### Phase 3: Product Stack (Week 5-6)
**Goal:** Complete Stack B (109 plays usable with full skill tree).

8. **Build product drills:**
   - `drills/product/onboarding-flow`
   - `drills/product/feature-announcement`
   - `drills/product/churn-prevention`
   - `drills/product/nps-feedback-loop`
   - `drills/product/upgrade-prompt`
   - `drills/product/referral-program`
   - `drills/product/winback-campaign`

9. **Build remaining fundamentals:**
   - `fundamentals/video/loom`, `fundamentals/video/descript`
   - `fundamentals/scheduling/calcom`
   - `fundamentals/sales/gong`, `fundamentals/sales/fireflies`
   - `fundamentals/content/ghost`, `fundamentals/content/webflow`

10. **Rewrite remaining 220 plays** to reference drills

### Phase 4: Polish & Ship (Week 7-8)
**Goal:** Full system tested and documented.

11. **Website integration:**
    - Build `/playbook/skills` tree browser page
    - Add "Drills & Fundamentals" section to `/playbook/[slug]`
    - Update intro to explain the Plays / Drills / Fundamentals concept

12. **Automated testing:**
    - Script that validates all skill references resolve correctly
    - CI check that every play references existing drills/fundamentals
    - Integration tests: `npx gtm-skills add <play> --level <X>` produces correct file set

13. **Documentation:**
    - Update AGENTS.md with Plays / Drills / Fundamentals architecture
    - Update CLAUDE.md with how to navigate the three layers
    - Write "Contributing a Skill" guide for community

14. **Release v0.2.0** with the full skill tree

---

## Testing Strategy

### Unit Tests (automated, run in CI)
- Every SKILL.md has valid frontmatter (name, description)
- Every play's drill/fundamental references resolve to existing files
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

1. **MCP server management:** Should `npx gtm-skills init` also install MCP servers (attio-mcp, posthog-mcp, n8n-mcp)? Or leave that to the user?

2. **Skill versioning:** When we update a fundamental (e.g., improve the Clay enrichment workflow), how do installed copies get updated? VERSIONS.md tracks this but the update mechanism needs design.

3. **Community contributions:** Should the skill tree be open for community-contributed drills/fundamentals? If so, what's the review process?

4. **Pricing:** Are all skills free (MIT)? Or do some advanced Durable-level skills require a Tarka subscription?
