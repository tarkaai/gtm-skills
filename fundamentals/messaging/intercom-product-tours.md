---
name: intercom-product-tours
description: Build interactive product tours in Intercom for user onboarding
tool: Intercom
difficulty: Intermediate
---

# Create Product Tours in Intercom

## Prerequisites
- Intercom account with Product Tours add-on
- Clear onboarding flow defined (key steps new users must complete)

## Steps

1. **Map your onboarding steps.** Define the 3-5 critical actions a new user must complete to reach their "aha moment." Example for a project management tool: 1) Create a project, 2) Add a task, 3) Invite a teammate, 4) Set a deadline. Each step becomes a tour stop.

2. **Create a new product tour.** In Intercom, go to Product Tours > New Tour. Name it descriptively (e.g., "New User Onboarding - Core Setup"). Select the starting page where the tour begins (usually the dashboard or home screen after first login).

3. **Build tour steps.** Add steps that highlight specific UI elements. For each step: select the element to spotlight, write a short instruction (under 25 words), and add a CTA ("Next" to continue, or "Try it" for interactive steps). Use Intercom's pointer to target exact buttons or sections.

4. **Add interactive steps.** Make at least 2 tour steps interactive -- the user must actually perform the action (click a button, fill a field) to proceed. Interactive steps have 3x higher completion rates than passive "click next" steps because users learn by doing.

5. **Set trigger conditions.** Configure the tour to start automatically for new users on their first login. Add conditions: show only to users where "onboarding_complete" is false. Set a dismissal option so users can skip if they prefer to explore on their own.

6. **Track completion.** Monitor tour metrics: start rate, step-by-step completion, and overall completion rate. Target 60%+ completion for the full tour. If users drop off at a specific step, simplify that step or break it into two smaller steps. Track whether tour completers activate at higher rates than non-completers.
