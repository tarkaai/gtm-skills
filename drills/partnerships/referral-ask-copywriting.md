---
name: referral-ask-copywriting
description: Generate personalized referral ask messages for each connector-target pair with pre-written forwardable blurbs
category: Partnerships
tools:
  - Anthropic
  - Attio
fundamentals:
  - attio-contacts
  - attio-notes
---

# Referral Ask Copywriting

This drill generates personalized referral request messages for each connector-target pair identified by the `referral-network-mapping` drill. Each message includes a short ask to the connector and a pre-written forwardable blurb they can copy-paste to the target, minimizing friction and maximizing the probability the intro actually happens.

## Input

- Referral map from Attio (output of `referral-network-mapping` drill) with connector, target, relationship context, and scores
- Your company's one-liner value proposition
- Recent customer wins or proof points relevant to the target's industry

## Steps

### 1. Pull connector and target context from Attio

Using the `attio-contacts` fundamental, for each connector-target pair on the referral map:

- **Connector context**: Name, relationship type (customer/advisor/investor/peer), how you know them, last interaction date, any previous intros they have made, their communication style preference (email vs LinkedIn DM)
- **Target context**: Name, title, company, company size, industry, known pain points (from enrichment), reason you want to reach them

### 2. Generate the ask message

For each pair, generate a message to the connector with these constraints:

**Structure:**
```
Subject: Quick intro request — {target first name} at {target company}

{Connector first name},

{1 sentence: why you are reaching out to them specifically — reference your relationship}

{1 sentence: who you want to meet and why — specific, not generic}

{1 sentence: what you can offer the target — value, not a pitch}

I wrote a short blurb below you can forward if you are open to it. No pressure at all.

---

{Forwardable blurb — see step 3}

---

Thanks either way,
{Your name}
```

**Rules:**
- Maximum 100 words above the blurb. Connectors are busy; long asks get ignored.
- Reference the specific relationship ("Since you advise {target company}..." or "You mentioned you know {target name} from {context}...")
- State what the target gets, not what you want. "I can share our {industry} benchmark data with them" beats "I want to pitch them."
- Include an explicit opt-out ("No pressure at all" or "Totally fine if not"). Removing social pressure increases response rates.
- Never assume the connector will vouch for your product. Ask for an introduction, not an endorsement.

### 3. Generate the forwardable blurb

The forwardable blurb is what the connector sends to the target. It must be:

**Structure:**
```
Hey {target first name},

I wanted to connect you with {your name} from {your company}. {1 sentence on what your company does, tailored to the target's context}.

{1 sentence on why this is relevant to the target specifically — reference their company, role, or known challenge}.

{Your name} asked if I could make an intro — happy to connect you two if you are open to a quick chat.

{Connector first name}
```

**Rules:**
- Maximum 60 words. The connector is lending their credibility; do not make them send a wall of text.
- Personalize to the target's context. "They help DevTools companies reduce onboarding time" is better than "They have a great product."
- The blurb should sound like it was written by the connector, not by you. Use casual language matching the connector's communication style.
- End with a soft CTA ("open to a quick chat") not a hard one ("book a demo").

### 4. Generate variants for A/B testing

For each ask, generate 2 variants:

- **Variant A (Direct)**: Leads with the intro request immediately. Best for strong relationships (willingness 4-5).
- **Variant B (Warm-up)**: Leads with a relationship touchpoint (congratulations, shared article, question about their work) before the ask. Best for weaker relationships (willingness 2-3).

Store both variants in Attio using the `attio-notes` fundamental so the agent or founder can choose which to send.

### 5. Batch generate for the full referral map

Process all connector-target pairs from the referral map in a single batch. For each pair:
1. Pull context from Attio
2. Generate Variant A and Variant B ask messages
3. Generate the forwardable blurb
4. Store all 3 artifacts as a note on the connector's Attio record, tagged with the target company name
5. Set the pair's status to "Ask Ready"

At Smoke level (15 pairs), this takes approximately 30 minutes of agent time. At Scalable level (100+ pairs), batch processing through n8n is required.

### 6. Quality check

After generation, review each message for:
- Does the relationship reference match reality? (Agent may hallucinate relationship details — verify against Attio data)
- Is the forwardable blurb under 60 words?
- Does the ask message reference specific value to the target, not generic pitch language?
- Is the tone appropriate for the connector's relationship level?

Flag any messages that fail quality checks for manual revision.

## Output

- Personalized ask messages (2 variants each) for every connector-target pair
- Pre-written forwardable blurbs ready for connectors to copy-paste
- All messages stored in Attio, tagged by target company
- Quality-checked and ready to send

## Triggers

Run once after `referral-network-mapping` completes. Re-run when the referral map is updated (monthly at Baseline+).
