---
name: field-visit-planning
description: Research local venues, build target lists of locations, and plan optimized visit routes for in-person prospecting
category: Field
tools:
  - Google Maps
  - Clay
  - Attio
  - Cal.com
fundamentals:
  - google-maps-place-search
  - google-maps-route-planning
  - clay-table-setup
  - clay-enrichment-waterfall
  - attio-lists
  - calcom-event-types
---

# Field Visit Planning

This drill prepares the founder for door-to-door or in-person prospecting by researching venues, identifying which locations have the highest density of ICP-matching businesses, and building an optimized visit schedule.

## Input

- ICP definition (from `icp-definition` drill)
- Target geography: city, neighborhood, or zip code radius
- Available time window: which days/hours the founder can be in the field
- Visit duration estimate: typically 20-40 minutes per venue

## Steps

### 1. Discover venues in the target area

Use the `google-maps-place-search` fundamental to search for venues by type within the target radius. Run multiple searches for different venue types relevant to your ICP:

- **If selling to startups/tech:** search `coworking_space` and `business_center` within 5-10km of a startup-dense neighborhood
- **If selling to SMBs:** search `office_space` and `shopping_mall` in commercial districts
- **If selling to trades/local services:** search `industrial_area` and relevant business types

Collect: venue name, address, coordinates, rating, review count, website, opening hours.

### 2. Enrich venues with business density data

Create a Clay table using `clay-table-setup` with the venue list. For each coworking space or business center, use `clay-enrichment-waterfall` to find:

- Number of member companies (check the venue's website, Crunchbase, LinkedIn company page)
- Types of businesses housed there (tech, creative, professional services)
- Community events hosted (meetups, lunch-and-learns, demo days)
- Foot traffic indicators (Google Maps "busy times" data, review volume)

Score each venue on ICP density: How many businesses matching your ICP are likely at this location?

### 3. Filter and prioritize venues

Remove venues that:
- Are closed during the founder's available hours
- Have very low review counts (likely low foot traffic)
- House primarily non-ICP businesses (e.g., a coworking space focused on artists when you sell DevTools)

Rank remaining venues by: ICP density score (50%), accessibility/parking (20%), event programming (15%), Google rating (15%).

### 4. Build the visit route

Take the top venues for a session (typically 4-6 per half-day) and use `google-maps-route-planning` fundamental to optimize the visit order. Set `optimizeWaypointOrder: true` and the planned departure time. The API returns the optimal stop sequence and travel time between each.

Build the schedule:
```
09:00 — Depart [home/office]
09:20 — Arrive WeWork SoMa (30 min visit)
10:00 — Drive 8 min
10:08 — Arrive Galvanize (30 min visit)
10:45 — Walk 5 min
10:50 — Arrive The Vault (30 min visit)
11:30 — Drive 12 min
11:42 — Arrive Hacker Dojo (30 min visit)
12:15 — Lunch / debrief
```

### 5. Prepare venue-specific intel

For each venue on the route, prepare a one-page brief the founder can review in the car between stops:

- Venue name and address
- What businesses are there (names, what they do, key people if available)
- Community manager name if findable (checking LinkedIn, venue website)
- Any upcoming events at the venue
- Suggested conversation opener relevant to the venue's community
- Any existing connections (check Attio for contacts already at this venue)

### 6. Set up booking infrastructure

Use the `calcom-event-types` fundamental to create a "Quick Coffee Chat — 15 min" event type the founder can offer on the spot. Generate a short link or QR code the founder can share verbally or on a business card. This converts an in-person conversation into a calendared follow-up.

### 7. Push the plan to CRM

Use `attio-lists` to create a list called "Field Visit — [Date] — [Area]" in Attio. Add each venue as a Company record (if not already present). Tag with `field-visit-target` and the planned visit date.

## Output

- Prioritized venue list with ICP density scores
- Optimized visit route with time estimates
- Per-venue intel briefs
- Cal.com booking link ready for in-field use
- Attio list tracking planned visits

## Triggers

Run this drill 1-2 days before each planned field session so the founder has time to review the briefs. Rerun for each new geography or when the venue list gets stale (every 4-6 weeks).
