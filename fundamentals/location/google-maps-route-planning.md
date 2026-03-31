---
name: google-maps-route-planning
description: Plan optimized multi-stop routes for field visits using Google Maps Routes API
tool: Google
product: Google Maps
difficulty: Setup
---

# Google Maps Route Planning

Plan multi-stop driving/walking routes for field prospecting visits. Optimizes stop order to minimize travel time so the founder covers more ground per session.

## Authentication

- Google Cloud project with Routes API enabled
- API key: `GOOGLE_MAPS_API_KEY`
- Billing account linked

## Compute Routes (point-to-point)

**Endpoint:** `POST https://routes.googleapis.com/directions/v2:computeRoutes`

**Headers:**
```
Content-Type: application/json
X-Goog-Api-Key: {GOOGLE_MAPS_API_KEY}
X-Goog-FieldMask: routes.duration,routes.distanceMeters,routes.legs,routes.optimizedIntermediateWaypointIndex
```

**Request body (multi-stop with optimization):**
```json
{
  "origin": {
    "location": {
      "latLng": { "latitude": 37.7749, "longitude": -122.4194 }
    }
  },
  "destination": {
    "location": {
      "latLng": { "latitude": 37.7849, "longitude": -122.4094 }
    }
  },
  "intermediates": [
    {
      "location": {
        "latLng": { "latitude": 37.7800, "longitude": -122.4150 }
      }
    },
    {
      "location": {
        "latLng": { "latitude": 37.7820, "longitude": -122.4120 }
      }
    }
  ],
  "travelMode": "DRIVE",
  "optimizeWaypointOrder": true,
  "departureTime": "2024-03-15T09:00:00Z"
}
```

**Key parameters:**
- `optimizeWaypointOrder: true` — reorders intermediate stops for shortest total travel time
- `travelMode`: `DRIVE`, `WALK`, `BICYCLE`, `TRANSIT`
- `departureTime` — set to planned visit time for traffic-aware estimates

## Response parsing

The response includes `optimizedIntermediateWaypointIndex` — an array giving the optimal order to visit stops. Use this to reorder the founder's visit schedule.

Each leg contains:
- `duration` — travel time between stops
- `distanceMeters` — distance between stops
- `startLocation` / `endLocation` — coordinates

Sum all leg durations plus estimated time per visit (e.g., 30 minutes per coworking space) to get total session time.

## Building a visit schedule

1. Query `google-maps-place-search` for venues in the target area
2. Filter to venues open during planned visit window
3. Feed venue coordinates as intermediates to this API with `optimizeWaypointOrder: true`
4. Parse the optimized order
5. Generate a schedule: arrival time at each stop = departure from previous + leg duration + visit duration

## Alternatives

| Tool | API/Method | Notes |
|------|-----------|-------|
| Google Maps | Routes API | Best for driving, traffic-aware |
| Mapbox | Optimization API | Good multi-stop optimization |
| HERE | Routing API | Strong commercial vehicle routing |
| OSRM | Open Source | Free, self-hosted, no traffic data |
| Routific | Route Optimization API | Purpose-built for multi-stop optimization |

## Pricing

- Google Maps Routes: $0 for first $200/month credit; ~$5 per 1000 route computations
- Mapbox: 100K free requests/month
- Routific: $0.05/stop for optimization

## Error Handling

- `MAX_WAYPOINTS_EXCEEDED`: Routes API supports up to 25 intermediates. Split into multiple routes if needed.
- `NOT_FOUND`: One or more locations could not be geocoded. Verify coordinates.
- `ZERO_RESULTS`: No route exists between the points (e.g., ocean between them).
