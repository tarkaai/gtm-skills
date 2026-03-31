---
name: calcom-inline-embed
description: Embed Cal.com scheduling widget inline on web pages, landing pages, and email CTAs
tool: Cal.com
difficulty: Setup
---

# Embed Cal.com Inline Scheduling Widget

Embed a Cal.com booking calendar directly within a web page so prospects can schedule without leaving the page. This removes the redirect friction of a standalone booking link.

## Prerequisites

- Cal.com account with at least one event type configured (see `calcom-event-types`)
- Access to the HTML/JS of the target page (Webflow, Next.js, plain HTML, etc.)

## Embed Methods

### Method 1: Inline Embed (HTML + JS snippet)

Paste the Cal.com embed loader script in your page `<head>` or before the closing `</body>`:

```html
<script type="text/javascript">
(function (C, A, L) {
  let p = function (a, ar) { a.q.push(ar); };
  let d = C.document;
  C.Cal = C.Cal || function () {
    let cal = C.Cal;
    let ar = arguments;
    if (!cal.loaded) {
      cal.ns = {};
      cal.q = cal.q || [];
      d.head.appendChild(d.createElement("script")).src = A;
      cal.loaded = true;
    }
    if (ar[0] === L) {
      const api = function () { p(api, arguments); };
      const namespace = ar[1];
      api.q = api.q || [];
      if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar);
      return;
    }
    p(cal, ar);
  };
})(window, "https://app.cal.com/embed/embed.js", "init");

Cal("init", { origin: "https://app.cal.com" });
</script>
```

Then place a container element where you want the calendar to appear:

```html
<div id="cal-inline-embed" style="width:100%;height:100%;overflow:scroll"></div>
<script>
Cal("inline", {
  elementOrSelector: "#cal-inline-embed",
  calLink: "YOUR_USERNAME/EVENT_SLUG",
  layout: "month_view"
});
Cal("ui", {
  styles: { branding: { brandColor: "#000000" } },
  hideEventTypeDetails: false,
  layout: "month_view"
});
</script>
```

Replace `YOUR_USERNAME/EVENT_SLUG` with your Cal.com username and event type slug (e.g., `dan/discovery`).

### Method 2: React Embed

Install the Cal.com React embed package:

```bash
npm install @calcom/embed-react
```

Use the `Cal` component:

```tsx
import Cal, { getCalApi } from "@calcom/embed-react";
import { useEffect } from "react";

export default function CalendarEmbed() {
  useEffect(() => {
    (async function () {
      const cal = await getCalApi();
      cal("ui", {
        styles: { branding: { brandColor: "#000000" } },
        hideEventTypeDetails: false,
        layout: "month_view",
      });
    })();
  }, []);

  return (
    <Cal
      calLink="YOUR_USERNAME/EVENT_SLUG"
      style={{ width: "100%", height: "100%", overflow: "scroll" }}
      config={{ layout: "month_view" }}
    />
  );
}
```

### Method 3: Webflow Embed

In Webflow, add an Embed element to your page. Paste the full HTML + JS snippet from Method 1 into the embed code editor. Set the container div to the desired width and height.

## UTM Tracking

Append UTM parameters to the calLink to track which page/CTA drove the booking:

```javascript
Cal("inline", {
  elementOrSelector: "#cal-inline-embed",
  calLink: "YOUR_USERNAME/EVENT_SLUG?utm_source=website&utm_medium=inline-embed&utm_campaign=pricing-page"
});
```

Cal.com passes UTM parameters through to the booking webhook payload, enabling PostHog attribution.

## Embed Events for Analytics

Cal.com embed fires JavaScript events you can capture for PostHog tracking:

```javascript
Cal("on", {
  action: "bookingSuccessful",
  callback: (e) => {
    posthog.capture("meeting_booked", {
      source: "inline-embed",
      page: window.location.pathname,
      event_type: e.detail.data.eventType.slug
    });
  }
});

Cal("on", {
  action: "linkReady",
  callback: () => {
    posthog.capture("calendar_widget_loaded", {
      page: window.location.pathname
    });
  }
});
```

## Error Handling

- If the embed does not render, verify the `calLink` slug matches an active event type.
- If the embed loads but shows no availability, check the event type's availability settings in Cal.com.
- CORS errors indicate the embed script URL is incorrect or blocked. Ensure `https://app.cal.com/embed/embed.js` is not blocked by CSP headers.

## Pricing

Cal.com embed is available on the Free plan ($0/mo) for individual users. Team round-robin embeds require the Teams plan ($15/user/mo). See [cal.com/pricing](https://cal.com/pricing).

## Tool Alternatives

| Tool | Embed Support | API | Pricing |
|------|--------------|-----|---------|
| Cal.com | Inline, popup, floating button | Full REST API + webhooks on free plan | Free - $15/user/mo |
| Calendly | Inline, popup, badge | API on paid plans, webhooks on Pro+ | $10-$16/user/mo |
| SavvyCal | Inline, overlay | API + webhooks | $12-$20/user/mo |
| HubSpot Meetings | Inline embed | HubSpot API | Free with HubSpot CRM |
| Chili Piper | Inline, concierge routing | API + webhooks | $15-$30/user/mo |
