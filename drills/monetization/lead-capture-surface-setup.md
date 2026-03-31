---
name: lead-capture-surface-setup
description: Build and deploy a single-CTA lead capture surface (form, inline calendar, or chat widget) with full tracking and CRM routing
category: Conversion
tools:
  - Webflow
  - Cal.com
  - Intercom
  - PostHog
  - Attio
  - n8n
  - Loops
fundamentals:
  - webflow-landing-pages
  - webflow-forms
  - calcom-inline-embed
  - calcom-event-types
  - intercom-bots
  - posthog-custom-events
  - n8n-triggers
  - n8n-workflow-basics
  - attio-contacts
  - attio-deals
  - loops-audience
---

# Lead Capture Surface Setup

This drill builds a single-CTA lead capture surface on one web page. A lead capture surface is the conversion element that turns product-aware visitors into leads. It is one of: an inline booking calendar, a short form, or a chat widget. The drill covers choosing the right surface type, deploying it, wiring tracking, and routing leads to CRM and nurture sequences.

## Input

- One high-intent web page where product-aware visitors land (pricing page, product page, comparison page, or dedicated landing page)
- A defined CTA action: book a call, submit a form, or start a chat
- CRM configured with lead stages (Attio or equivalent)
- PostHog tracking installed on the target page

## Steps

### 1. Choose the surface type

The surface type depends on your sales motion and what product-aware visitors need to do next.

| Surface Type | Best When | Conversion Mechanic |
|-------------|-----------|-------------------|
| Inline Calendar | Sales-assisted, prospect needs a conversation | Embedded Cal.com widget, prospect picks a time without leaving the page |
| Short Form | Self-serve or content-gated, prospect gives contact info for a resource or trial | Webflow form (name + email + 1 qualifying question), submits to CRM |
| Chat Widget | Hybrid, prospect has questions before committing | Intercom bot qualifies and either books a meeting or captures lead info |

Choose ONE for the Smoke test. Do not deploy multiple surface types on the same page.

### 2a. Deploy inline calendar (if chosen)

Use `calcom-event-types` to create the event type: name, duration, buffer times, booking window, and 2-3 form questions (company name, what they are evaluating, how they found you).

Use `calcom-inline-embed` to embed the calendar on the target page:
- Place it below the primary value proposition, above the fold if possible
- Use a clear heading: "Pick a time -- 30-minute discovery call" (not "Contact us")
- Configure UTM passthrough: `?utm_source=website&utm_medium=inline-embed&utm_campaign={page-slug}`
- Add the PostHog event listeners from `calcom-inline-embed`: capture `calendar_widget_loaded` and `meeting_booked` events

Use `n8n-triggers` to build a webhook workflow: Cal.com booking webhook fires -> use `attio-contacts` to create Person + Company records -> use `attio-deals` to create Deal at "Meeting Booked" stage -> use `loops-audience` to add the lead to a pre-meeting prep sequence.

### 2b. Deploy short form (if chosen)

Use `webflow-forms` to build a form on the target page:
- Fields: name (required), work email (required), company name (optional), one qualifying question (dropdown: "What are you looking for?" with 3-4 options matching your use cases)
- Submit button: action-specific copy ("Get started" or "Download the guide" -- not "Submit")
- Redirect to a thank-you page that confirms the action and offers a next step (booking link, resource download)

Use `n8n-triggers` to build a webhook workflow: Webflow form submission webhook fires -> use `attio-contacts` to create Person + Company records -> use `attio-deals` to create Deal at "Lead Captured" stage -> use `loops-audience` to enroll in a nurture sequence.

Add tracking with `posthog-custom-events`:
```javascript
// Track form interactions
document.querySelector('form').addEventListener('focus', function(e) {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
    posthog.capture('form_field_focused', {
      field: e.target.name,
      page: window.location.pathname,
      surface_type: 'form'
    });
  }
}, true);

document.querySelector('form').addEventListener('submit', function() {
  posthog.capture('lead_captured', {
    page: window.location.pathname,
    surface_type: 'form',
    utm_source: new URLSearchParams(window.location.search).get('utm_source')
  });
});
```

### 2c. Deploy chat widget (if chosen)

Use `intercom-bots` to build a qualification bot on the target page:
- Trigger: visitor opens Messenger on the target page
- Flow: "Looking for [product category]?" -> collect company size -> collect role -> if ICP match, offer to book a call (link to Cal.com booking page) or capture email for follow-up
- Handoff rule: if visitor says "talk to someone" or "demo," route to a human immediately

Use `posthog-custom-events` to track:
```javascript
Intercom('onShow', function() {
  posthog.capture('chat_widget_opened', {
    page: window.location.pathname,
    surface_type: 'chat'
  });
});
```

Use `n8n-triggers` to build an Intercom webhook workflow: new lead from bot -> use `attio-contacts` to create CRM record -> use `attio-deals` to create Deal.

### 3. Add universal tracking events

Regardless of surface type, use `posthog-custom-events` to capture these events on the target page:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `cta_impression` | CTA element enters viewport | `page`, `surface_type`, `cta_variant` |
| `cta_clicked` | Visitor clicks the CTA or interacts with the surface | `page`, `surface_type`, `cta_variant` |
| `lead_captured` | Form submitted, meeting booked, or email collected via chat | `page`, `surface_type`, `utm_source`, `lead_email` |

Use an Intersection Observer for `cta_impression`:
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      posthog.capture('cta_impression', {
        page: window.location.pathname,
        surface_type: '{form|calendar|chat}',
        cta_variant: 'v1'
      });
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });
observer.observe(document.querySelector('#cta-container'));
```

### 4. Test end-to-end

Before driving any traffic:
1. Load the page, verify the CTA renders correctly
2. Interact with the surface (submit the form, book a test meeting, or complete the chat flow)
3. Verify the PostHog events fire: check PostHog Live Events for `cta_impression`, `cta_clicked`, `lead_captured`
4. Verify the n8n webhook fires and creates the Attio record
5. Verify the Loops sequence enrollment triggers
6. If any step fails, fix before proceeding

## Output

- One live lead capture surface on one high-intent page
- PostHog events flowing: `cta_impression`, `cta_clicked`, `lead_captured`
- n8n webhook routing leads to Attio CRM and Loops nurture sequence
- End-to-end test confirming the full pipeline works

## Triggers

Run once during play setup. Re-run when deploying the surface on additional pages (Scalable level) or when changing the surface type.
