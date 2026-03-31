---
name: onboarding-call-script
description: Design a structured onboarding call agenda with discovery questions, activation walkthrough, feedback capture, and post-call scoring template
category: Product
tools:
  - Fireflies
  - Attio
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - attio-notes
  - attio-custom-attributes
  - posthog-custom-events
---

# Onboarding Call Script

This drill produces a ready-to-execute onboarding call structure: a timed agenda, discovery questions mapped to activation goals, a live walkthrough framework, a feedback capture template, and a post-call scoring rubric. The output is used by the person running the call and by the agent processing the transcript afterward.

## Prerequisites

- Clear definition of the product's activation milestone (the action that predicts 30-day retention)
- Fireflies configured to auto-join and transcribe meetings (see `fireflies-transcription`)
- Attio CRM with a contact record for the user being onboarded
- PostHog tracking the activation milestone event

## Steps

### 1. Define the call structure

Design a 30-minute onboarding call with this timed structure:

| Block | Duration | Purpose |
|-------|----------|---------|
| Welcome + context | 3 min | Greet the user, confirm their role and goals, set expectations for the call |
| Discovery | 7 min | Ask questions to understand their use case, current workflow, and definition of success |
| Guided walkthrough | 12 min | Walk the user through the critical path to the activation milestone, using their real data or scenario |
| Q&A + blockers | 5 min | Address questions, surface blockers, troubleshoot anything that did not work |
| Next steps + close | 3 min | Summarize action items, set the next check-in, ask for feedback on the call |

The walkthrough block is the core. The goal is for the user to complete or nearly complete the activation milestone *during the call*. If the activation action takes longer than 12 minutes, pre-configure parts of their account before the call so they can reach the milestone live.

### 2. Write the discovery questions

Write 5-7 discovery questions that map to qualification and onboarding goals. Each question has a purpose and a scoring rubric:

1. "What problem are you trying to solve with [product]?" -- Purpose: confirm they have a real use case. Score: 1 (vague/exploring) to 3 (specific, urgent problem).
2. "How are you solving this today?" -- Purpose: understand current workflow and switching cost. Score: 1 (no current solution) to 3 (manual process they hate).
3. "What would success look like for you in the first 2 weeks?" -- Purpose: set a concrete activation target. Score: 1 (no clear goal) to 3 (specific measurable outcome).
4. "Who else on your team will use this?" -- Purpose: identify expansion potential. Score: 1 (just me) to 3 (whole team, multiple roles).
5. "Have you tried any features yet? What worked or did not work?" -- Purpose: diagnose pre-call friction. Score: 1 (nothing tried) to 3 (already exploring, hit specific issues).

Store the scores in Attio using `attio-custom-attributes` as numeric fields: `onboarding_call_problem_fit`, `onboarding_call_current_workflow`, `onboarding_call_success_clarity`, `onboarding_call_expansion_potential`, `onboarding_call_pre_engagement`.

### 3. Design the guided walkthrough

Map the walkthrough to the user's activation milestone. The walkthrough must be executable, not presentational. Structure:

1. **Start from their use case.** Use the discovery answers to frame the walkthrough: "You said you want to [goal]. Let me show you the fastest path to that."
2. **Execute the critical path live.** Walk through the exact steps to reach the activation milestone. Have the user perform each action on their own screen while you guide them. Do not do it for them.
3. **Checkpoint after each step.** Confirm the step completed. If it fails, troubleshoot immediately. Log blockers.
4. **Reach the milestone or get as close as possible.** If the user completes the activation milestone during the call, capture the moment: "You just [activation action]. This is the core value of the product."
5. **If the milestone cannot be reached in the call**, document exactly what remains and set a concrete deadline (within 48 hours) for the user to complete it.

### 4. Build the feedback capture template

At the end of each call, capture structured feedback. Use Fireflies transcript + a 3-question verbal ask:

1. "On a scale of 1-5, how clear is the path to your goal after this call?"
2. "What is the one thing that could have made this call more useful?"
3. "Would you recommend this onboarding call to a colleague? Why or why not?"

After the call, use `fireflies-action-items` to extract:
- Action items assigned to the user
- Action items assigned to your team (feature requests, bugs, documentation gaps)
- Key quotes about the product (positive and negative)

Log all feedback in Attio using `attio-notes` as a structured note on the contact record.

### 5. Build the post-call scoring rubric

Score each onboarding call on 4 dimensions using data from the call:

| Dimension | Score 1 (Poor) | Score 2 (OK) | Score 3 (Good) |
|-----------|---------------|--------------|----------------|
| Activation progress | Did not attempt milestone | Attempted, did not complete | Completed milestone during call |
| Engagement level | Passive, camera off, monosyllabic | Engaged but following instructions | Asking questions, exploring independently |
| Feedback quality | No useful feedback | General positive/negative | Specific, actionable feedback |
| Expansion signal | Solo user, no expansion intent | Mentioned teammates vaguely | Named specific colleagues or teams to invite |

Calculate a total score (4-12). Use `posthog-custom-events` to fire:
```
posthog.capture('onboarding_call_completed', {
  user_email: email,
  call_score: totalScore,
  activation_during_call: true/false,
  expansion_signal: true/false,
  nps_score: 1-5,
  blockers_found: ['blocker1', 'blocker2']
})
```

Store the score in Attio using `attio-custom-attributes` as `onboarding_call_score`.

### 6. Create the pre-call prep checklist

Before each call, the agent should prepare:

1. Pull the user's current product usage from PostHog: which features they have tried, how far through onboarding they are, any errors they hit
2. Pull their CRM record from Attio: plan type, signup source, company size, any prior interactions
3. Pre-configure anything that would save time during the walkthrough (sample data, integrations, permissions)
4. Generate a 1-page prep brief: user name, company, plan, usage summary, suggested walkthrough path, potential blockers

This prep brief is the input for the person running the call.

## Output

- A timed 30-minute call structure with discovery, walkthrough, feedback, and scoring
- 5-7 discovery questions with scoring rubrics
- A guided walkthrough framework tied to the activation milestone
- A post-call scoring rubric (4-12 scale)
- PostHog events and Attio attributes for tracking call quality
- A pre-call prep checklist for the agent to run before each call
