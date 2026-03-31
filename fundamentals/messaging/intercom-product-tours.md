---
name: intercom-product-tours
description: Build interactive product tours in Intercom for user onboarding
tool: Intercom
product: Intercom
difficulty: Intermediate
---

# Create Product Tours in Intercom

## Prerequisites
- Intercom account with Product Tours add-on
- Clear onboarding flow defined (key steps new users must complete)

## Steps

1. **Map your onboarding steps.** Define the 3-5 critical actions a new user must complete to reach their "aha moment." Example for a project management tool: 1) Create a project, 2) Add a task, 3) Invite a teammate, 4) Set a deadline. Each step becomes a tour stop.

2. **Create a new product tour via API.** Use the Intercom API to define the tour. Name it descriptively (e.g., "New User Onboarding - Core Setup"). Configure the starting URL where the tour begins (usually the dashboard or home screen after first login).

3. **Build tour steps.** Define steps that highlight specific UI elements. For each step: specify the CSS selector of the element to spotlight, write a short instruction (under 25 words), and add a CTA ("Next" to continue, or "Try it" for interactive steps). Interactive steps have 3x higher completion rates.

4. **Add interactive steps.** Make at least 2 tour steps interactive -- the user must actually perform the action (use a button, fill a field) to proceed. Users learn by doing, which drives higher activation rates.

5. **Set trigger conditions via API.** Configure the tour to start automatically for new users on first login. Add conditions: show only to users where `onboarding_complete` is false. Set a dismissal option so users can skip if they prefer to explore independently.

6. **Track completion via API.** Monitor tour metrics: `GET /product_tours/<id>/stats`. Track start rate, step-by-step completion, and overall completion rate. Target 60%+ completion. If users drop off at a specific step, simplify it. Correlate tour completion with activation rates to prove ROI.
