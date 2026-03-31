---
name: intercom-bots
description: Configure Intercom bots for automated user engagement and support
tool: Intercom
difficulty: Intermediate
---

# Set Up Bots in Intercom

## Prerequisites
- Intercom account with Messenger configured
- Help articles created (see `intercom-help-articles`)
- User properties and events flowing into Intercom

## Steps

1. **Understand bot types.** Intercom offers several bot types: Resolution Bot (answers common questions with articles), Custom Bot (interactive conversation flows), and Task Bot (collects information before routing to a human). Start with Resolution Bot for the highest ROI.

2. **Configure Resolution Bot via API.** Use the Intercom API to map question-answer pairs: common questions ("How do I reset my password?") to help article IDs. Intercom uses AI to match similar phrasings. Start with your top 10 support questions and expand as new patterns emerge.

3. **Build a custom qualification bot.** Create a Custom Bot via the API that qualifies inbound leads. Trigger: new conversation from a visitor. Flow: "Are you looking to [use case]?" > Collect company size > Collect role > If enterprise, route to sales. If SMB, suggest self-serve signup. This replaces manual lead qualification.

4. **Build an onboarding bot.** Create a Custom Bot triggered on first login. Flow: "Welcome! What are you trying to accomplish?" > Present 3-4 use case options > Based on selection, link to the relevant product tour (see `intercom-product-tours`) or help article. This personalizes onboarding.

5. **Set up escalation rules.** Configure handoff conditions via the API: if the user says "talk to a human" or "agent" (immediate handoff), if confidence score is below 50% (handoff with context), if the conversation exceeds 3 bot replies without resolution (handoff). Never trap users in a bot loop.

6. **Measure bot effectiveness via API.** Query bot metrics: resolution rate (% resolved without human), deflection rate (questions answered by articles), and satisfaction scores. Target 30%+ resolution rate. If lower, add more question-answer pairs.
