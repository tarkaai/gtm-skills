---
name: best-practices-personalization
description: Segment users by role, usage pattern, and product maturity to deliver persona-specific best practices at scale
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - Anthropic
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-feature-flags
  - intercom-user-properties
  - intercom-in-app-messages
  - loops-sequences
  - ai-content-ghostwriting
  - n8n-workflow-basics
---

# Best Practices Personalization

This drill transforms the one-size-fits-all best-practices library into a per-persona content system. Instead of showing the same tips to every user, it segments users by role, feature usage pattern, and product maturity, then delivers tips that match each user's specific context. This is the 10x multiplier: the same content engine serves 5+ distinct audiences without proportional content creation effort.

## Input

- Best-practices content cards from the `best-practices-content-pipeline` drill (at least 8 cards)
- PostHog usage data with at least 60 days of history
- User role data (from signup flow, Intercom properties, or enrichment)
- Delivery automation running from the `best-practices-delivery-automation` drill

## Steps

### 1. Define user personas from behavior data

Using `posthog-cohorts`, create behavioral personas based on actual product usage patterns. Do not use assumed personas — let the data define them:

**Query PostHog for usage clusters:**
- **Builders:** Users who primarily use creation/editing features (create 5+ items per week, spend 70%+ of time in the editor)
- **Reviewers:** Users who primarily use viewing/commenting features (view 10+ items per week, rarely create)
- **Admins:** Users who access team settings, billing, permissions, and integrations (visit settings 2+ times per week)
- **Power users:** Users who use 8+ distinct features per week and use the product 5+ days per week
- **Casual users:** Users who log in 1-2 times per week and use 2-3 features

Create a PostHog cohort for each persona. Using `intercom-user-properties`, sync each user's persona to their Intercom profile as a custom property: `best_practices_persona`.

### 2. Map content cards to personas

For each content card from the library, assign a primary persona and up to 2 secondary personas:

| Card Category | Primary Persona | Secondary Personas |
|--------------|----------------|-------------------|
| Workflow optimization | Builders | Power users |
| Shortcuts and speed | Power users | Builders |
| Configuration and settings | Admins | Power users |
| Collaboration features | Reviewers | Admins |
| Integration setup | Admins | Builders |
| Advanced features | Power users | Builders, Admins |

A card is only delivered to a user if their persona matches the card's primary or secondary persona assignment.

### 3. Generate persona-specific copy variants

Using the `ai-content-ghostwriting` fundamental, generate copy variants of each card's hook and body for each relevant persona. The factual content stays the same; the framing changes:

```
System prompt: "Rewrite this product best-practice tip for a specific user persona. Keep the instructions identical. Change only the hook line and the first sentence of the body to resonate with this persona's priorities.

Persona: {PERSONA_NAME} — {PERSONA_DESCRIPTION}. They care about {PERSONA_PRIORITIES}.

Original tip:
Title: {TITLE}
Hook: {HOOK}
Body: {BODY}"

User prompt: "Generate the persona-specific variant."
```

Example:
- **Original hook:** "Save 2 minutes per task with keyboard shortcuts"
- **Builder variant:** "Edit faster — keyboard shortcuts that keep you in flow"
- **Admin variant:** "Boost team productivity with shortcuts your team does not know about"
- **Reviewer variant:** "Navigate and comment without touching the mouse"

Store variants as properties on the card: `hook_{persona}`, `body_{persona}`.

### 4. Configure persona-aware delivery

Update the n8n orchestration workflow from the `best-practices-delivery-automation` drill:

1. When selecting which card to show a user, filter by persona match (card's persona list must include the user's persona)
2. When delivering the card, use the persona-specific copy variant instead of the default
3. Using `posthog-feature-flags`, set up a feature flag per persona that controls which card variant is displayed in-app

For Intercom in-app messages, use `intercom-in-app-messages` to create persona-specific message versions. Target each version to users with the matching `best_practices_persona` property.

For Loops emails, use `loops-sequences` to create persona-specific email templates. Include the persona-appropriate hook in the subject line and the persona-specific body in the email content.

### 5. Create product maturity tiers

Beyond persona, segment users by product maturity — how long they have been using the product and how deep their usage goes:

- **Week 1-2 (Novice):** Show only foundational tips — basic workflow, essential configuration, core features
- **Week 3-8 (Intermediate):** Show efficiency tips — shortcuts, integrations, collaboration features
- **Week 9+ (Advanced):** Show power tips — advanced features, automation, custom configurations

Using `posthog-custom-events`, track the user's `days_since_signup` and `features_used_count`. Combine with persona to create the final delivery matrix: a Week-1 Builder sees different tips than a Week-9 Admin.

### 6. Build the personalization matrix dashboard

Using PostHog, create a dashboard showing:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Persona distribution | Pie chart | What percentage of active users fall into each persona |
| Tip engagement by persona | Bar chart | Which persona engages most with tips (completion rate) |
| Tip engagement by maturity tier | Bar chart | How engagement changes as users mature |
| Top-performing cards per persona | Table | Which specific cards have the highest completion rate for each persona |
| Persona migration | Sankey diagram | Users moving between personas over time (Casual -> Builder) |
| Retention by tip engagement | Line chart | 30-day retention for users who complete 0, 1-3, 4+ tips, split by persona |

### 7. Test persona assignment accuracy

Every 30 days, audit the persona cohorts:
- Are persona sizes stable? If one persona grows to >50% of users, the segments may be too broad.
- Do users stay in their persona? If >30% migrate within 30 days, the cohort definitions need tightening.
- Does persona-specific copy outperform generic copy? If the variant completion rate is not at least 5pp higher than the original, the personalization is not adding value.

If persona assignment is inaccurate, refine the PostHog cohort definitions with tighter behavioral criteria.

## Output

- 5 behavioral personas defined from PostHog usage data and synced to Intercom
- Persona-specific copy variants for each content card
- Product maturity tiers layered on top of personas
- Updated delivery automation that matches persona + maturity to content
- Personalization matrix dashboard tracking engagement by persona and maturity

## Triggers

Set up at Scalable level. Review persona definitions monthly. Generate new persona-specific copy variants when new cards are added to the library. Re-run the persona clustering analysis quarterly as the user base evolves.
