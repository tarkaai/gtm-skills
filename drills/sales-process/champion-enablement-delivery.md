---
name: champion-enablement-delivery
description: Arm recruited champions with internal selling materials, talking points, and business case assets they can use to advocate internally
category: Deal Management
tools:
  - Attio
  - Loops
  - Loom
  - Anthropic
fundamentals:
  - attio-champion-tracking
  - attio-notes
  - loops-sequences
  - loom-personalized-outreach
  - loom-analytics
  - ai-content-ghostwriting
---

# Champion Enablement Delivery

This drill arms recruited champions with everything they need to sell internally. Champions fail when they believe in your product but lack the tools to convince their colleagues and boss. This drill solves that by providing ready-made internal selling materials.

## Input

- Champions with `champion_status` = "Recruited" in Attio
- Champion briefing from the profiling step (signals, pain points, role)
- Product value proposition and competitive positioning
- Existing case studies and ROI data

## Steps

### 1. Generate Personalized Enablement Kit

For each recruited champion, use `ai-content-ghostwriting` to generate a personalized enablement kit. Send the following to Claude:

```
"Generate an internal champion enablement kit for {champion_name}, {champion_title} at {company_name}. They are championing our product to solve {identified_pain}. Their boss is likely a {economic_buyer_title}.

Generate these 4 assets:

1. INTERNAL EMAIL DRAFT (for the champion to forward to their boss):
   - Subject line
   - 3-paragraph email explaining the problem, the solution, and suggested next step
   - Written in the champion's voice, not ours
   - Include 1-2 specific data points from our case studies

2. ONE-PAGE BUSINESS CASE:
   - Problem statement (2 sentences)
   - Current cost of the problem (use industry benchmarks if we don't have their specific data)
   - Proposed solution (3 bullet points, no jargon)
   - Expected ROI (use conservative estimates)
   - Recommended next step

3. OBJECTION RESPONSES (top 3 objections their boss will raise):
   - For each: the objection, a one-sentence reframe, and supporting evidence

4. TALKING POINTS (for their internal meeting):
   - 5 bullet points they can reference when pitching internally
   - Each point: claim + evidence + so-what

Return as structured markdown with clear section headers."
```

### 2. Create Personalized Walkthrough Video

Using `loom-personalized-outreach`, record a 3-5 minute video for each champion that:
- Addresses them by name
- Walks through the one-page business case
- Shows exactly how they should position the solution to their boss
- Highlights the 2-3 features most relevant to their specific pain
- Ends with: "Forward this to your team if it's helpful — happy to jump on a call with whoever needs to see it"

**Human action required:** Record the Loom video. The agent prepares the script and talking points, but the founder records it for authenticity.

### 3. Set Up Enablement Drip Sequence

Using `loops-sequences`, create a 3-email enablement sequence that delivers the kit over 5 days:

**Email 1 (Day 0) — The Kit:**
Subject: "Your internal pitch kit for {solution_category}"
Body: "As promised, here's everything you need to bring this to your team." Attach: internal email draft + one-page business case. CTA: "Reply if you want me to customize anything."

**Email 2 (Day 2) — The Video:**
Subject: "Quick walkthrough for your team"
Body: Embed the Loom video. Frame it as: "Figured this might be easier than reading a doc. Feel free to forward to anyone who needs context."

**Email 3 (Day 5) — The Check-in:**
Subject: "How did the conversation go?"
Body: Simple check-in. Three response paths: (a) "Great, they want to talk" → book meeting, (b) "Haven't pitched yet" → offer to help prep, (c) "They had concerns" → address objections.

### 4. Track Enablement Engagement

Monitor engagement using `loom-analytics` and `loops-sequences`:
- Did they open the emails?
- Did they watch the Loom video? How much of it?
- Did they forward the video (Loom shows unique viewers)?
- Did they reply to any email?

Log all engagement data to Attio:
- Update `champion_last_engaged` with latest interaction date
- If they forwarded the Loom (multiple viewers), log a note: "Champion forwarded enablement video to {N} colleagues — strong advocacy signal"
- If they watched <25% of the video, log a note: "Low video engagement — may need different format or re-engagement"

### 5. Update Champion Status

Based on engagement within 10 days of kit delivery:
- **Forwarded materials + replied:** Set `champion_status` = "Active", `champion_deal_role` based on their behavior
- **Opened but didn't forward/reply:** Keep as "Recruited", trigger a follow-up call
- **Didn't open:** Flag for re-engagement. Try a different channel (LinkedIn DM, phone call)

## Output

- Personalized enablement kit (4 assets) generated and delivered per champion
- Loom walkthrough video script prepared (founder records)
- Engagement tracked and logged to Attio
- Champion status updated based on enablement response
- Champions who forwarded materials identified as strongest advocates

## Triggers

- Run immediately when a champion's status changes to "Recruited"
- Re-run with refreshed materials if champion status reverts from "Active" to "Recruited" (they need a second push)
