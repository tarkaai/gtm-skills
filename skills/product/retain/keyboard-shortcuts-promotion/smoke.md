---
name: keyboard-shortcuts-promotion-smoke
description: >
  Power User Features — Smoke Test. Instrument shortcut tracking, build contextual
  hints for top 3 shortcuts, launch to 10-20 users, and measure whether any shortcut
  adoption signal emerges within 7 days.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=20% of test users try at least 1 promoted shortcut within 7 days"
kpis: ["Shortcut hint-to-trial conversion rate", "Shortcut ratio (shortcut actions / total actions)", "Number of unique shortcuts tried per user"]
slug: "keyboard-shortcuts-promotion"
install: "npx gtm-skills add product/retain/keyboard-shortcuts-promotion"
drills:
  - threshold-engine
---

# Power User Features — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

At least 20% of the 10-20 test users try a promoted keyboard shortcut within 7 days of seeing their first contextual hint. This proves that contextual in-product shortcut hints produce measurable adoption signal before investing in always-on automation.

## Leading Indicators

- Users are seeing shortcut hints (hint impression events firing in PostHog)
- At least some users click or perform the suggested shortcut within the same session
- Shortcut reference page gets organic traffic from hint CTAs
- No complaints or support tickets about intrusive hints

## Instructions

### 1. Map your top 3 shortcuts

Run the first step of the the shortcut discovery promotion workflow (see instructions below) drill: build the shortcut action map. For the Smoke test, identify only the **top 3 highest-impact shortcuts** — the ones that correspond to the most frequently performed mouse actions. Rank by `frequency_of_mouse_action * estimated_seconds_saved`.

Example output:
| Shortcut | Keys | Mouse equivalent | Est. daily uses per active user |
|----------|------|------------------|---------------------------------|
| Quick search | Cmd+K | Click search bar | 8-12 |
| Submit form | Cmd+Enter | Click submit button | 5-8 |
| Navigate back | Cmd+[ | Click back arrow | 4-6 |

**Human action required:** Confirm the shortcut map is accurate. Verify each shortcut works on both Mac and Windows (Cmd vs Ctrl). Test each shortcut manually.

### 2. Instrument shortcut tracking

Run step 2 of the the shortcut discovery promotion workflow (see instructions below) drill: add PostHog events for the 3 selected shortcuts. Implement these events in your product code:

- `action_via_mouse` with properties: `action_id`, `shortcut_equivalent`, `page`
- `action_via_shortcut` with properties: `action_id`, `shortcut_key`, `page`
- `shortcut_hint_shown` with properties: `shortcut_id`, `trigger_type`, `page`
- `shortcut_hint_converted` with properties: `shortcut_id`, `time_since_hint_seconds`

**Human action required:** Deploy the tracking code to your staging environment. Trigger each event manually and verify it appears in PostHog Live Events. Fix any property mismatches before proceeding.

### 3. Build contextual hints for 3 shortcuts

Run step 4 of the the shortcut discovery promotion workflow (see instructions below) drill to create Intercom tooltip messages for each of the 3 shortcuts. For Smoke, use simple rules:

- **Trigger:** User performs `action_via_mouse` for a shortcut-eligible action
- **Message:** "Pro tip: Press `{keys}` to do this instantly."
- **Display:** Tooltip near the element they clicked. Auto-dismiss after 5 seconds.
- **Frequency cap:** Maximum 1 hint per session. Same hint never shown twice if dismissed.

Gate the entire hint system behind a PostHog feature flag (`shortcut-hints-v1`) set to target only the test group.

### 4. Launch to test group

Using PostHog feature flags, enable `shortcut-hints-v1` for 10-20 users. Select users who:
- Have been active for 14+ days (know the product)
- Use the product at least 3 times per week (enough sessions to encounter hints)
- Have not used any keyboard shortcuts yet (room to improve)

Do NOT select power users who already use shortcuts — they will inflate your signal.

### 5. Measure against threshold

Run the `threshold-engine` drill after 7 days. Query PostHog for:

```
shortcut_trial_rate = count(distinct users with at least 1 shortcut_hint_converted event)
                      / count(distinct users in test group with at least 1 shortcut_hint_shown event)
```

**Pass threshold: >= 20% shortcut trial rate.**

Also capture:
- Which of the 3 shortcuts got the most trials
- Average time from hint shown to shortcut used
- Whether any users tried shortcuts they were NOT prompted about (organic discovery)
- Hint dismissal rate (if > 70%, the hints feel intrusive)

### 6. Decide next step

If PASS (>= 20% trial rate): Document which shortcuts converted best, what hint copy worked, and proceed to Baseline to automate and expand.

If FAIL (< 20% trial rate): Diagnose. Check:
- Were hints actually shown? (impression count > 0 for each user)
- Were hints shown at the right moment? (immediately after the mouse action, not delayed)
- Was the hint copy clear? (test "Press Cmd+K to search instantly" vs "Try the keyboard shortcut")
- Were the selected shortcuts valuable enough? (try different shortcuts)

Iterate and re-run Smoke. Do not proceed to Baseline until signal is proven.

## Time Estimate

- 2 hours: shortcut mapping, event instrumentation, deployment
- 1 hour: Intercom hint setup and PostHog feature flag configuration
- 1 hour: launch to test group, verify events are firing
- 2 hours: 7-day analysis, threshold evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, cohort targeting | Free tier: 1M events/mo, 1M flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Tooltip-style in-app hint messages | Essential: $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |

**Estimated play-specific cost at this level:** Free (within PostHog free tier + existing Intercom seat)

## Drills Referenced

- the shortcut discovery promotion workflow (see instructions below) — builds the shortcut map, tracking events, contextual hints, and progressive education system
- `threshold-engine` — evaluates the 20% trial rate pass/fail threshold and recommends next action
