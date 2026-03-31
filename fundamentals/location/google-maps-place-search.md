---
name: google-maps-place-search
description: Search Google Maps Places API for business locations by type and geography
tool: Google Maps
difficulty: Setup
---

# Google Maps Place Search

Search for business locations (coworking spaces, business parks, office buildings, coffee shops) within a geographic area using the Google Maps Places API.

## Authentication

- Google Cloud project with Places API enabled
- API key with Places API access: `GOOGLE_MAPS_API_KEY`
- Billing account linked (Places API is pay-per-use after free tier)

## Nearby Search (recommended for field prospecting)

**Endpoint:** `POST https://places.googleapis.com/v1/places:searchNearby`

**Headers:**
```
Content-Type: application/json
X-Goog-Api-Key: {GOOGLE_MAPS_API_KEY}
X-Goog-FieldMask: places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount,places.googleMapsUri,places.websiteUri,places.types,places.businessStatus
```

**Request body:**
```json
{
  "includedTypes": ["coworking_space"],
  "locationRestriction": {
    "circle": {
      "center": { "latitude": 37.7749, "longitude": -122.4194 },
      "radius": 5000.0
    }
  },
  "maxResultCount": 20,
  "rankPreference": "POPULARITY"
}
```

**Useful `includedTypes` for field prospecting:**
- `coworking_space` — coworking and shared offices
- `office_space` — general office buildings (commercial real estate)
- `business_center` — business centers and serviced offices
- `cafe` — coffee shops (founder hangouts)
- `convention_center` — conference/event venues
- `shopping_mall` — retail if selling to local businesses
- `industrial_area` — warehouses/workshops for trades

Combine multiple searches with different types to build a comprehensive venue list.

## Text Search (for specific queries)

**Endpoint:** `POST https://places.googleapis.com/v1/places:searchText`

**Request body:**
```json
{
  "textQuery": "coworking spaces in Austin TX",
  "locationBias": {
    "circle": {
      "center": { "latitude": 30.2672, "longitude": -97.7431 },
      "radius": 10000.0
    }
  },
  "maxResultCount": 20
}
```

Use text search for more specific queries like "startup incubators near downtown" or "tech hubs in SoMa."

## Place Details (get hours, contact info)

**Endpoint:** `GET https://places.googleapis.com/v1/places/{place_id}`

**Headers:**
```
X-Goog-Api-Key: {GOOGLE_MAPS_API_KEY}
X-Goog-FieldMask: places.displayName,places.formattedAddress,places.regularOpeningHours,places.phoneNumbers,places.websiteUri,places.reviews
```

Pull opening hours so the agent can schedule visits during business hours. Pull reviews to assess foot traffic and business density.

## Alternatives

| Tool | API/Method | Notes |
|------|-----------|-------|
| Google Maps | Places API (New) | Best coverage, pay-per-use |
| Yelp | Fusion API | Good for cafes/restaurants, US-focused |
| Foursquare | Places API | Strong international POI data |
| OpenStreetMap | Overpass API | Free, community-maintained, less business detail |
| Apple Maps | MapKit JS | Good on Apple platforms |

## Pricing

- Google Maps: $0 for first $200/month credit; ~$32 per 1000 Nearby Search requests after
- Yelp Fusion: Free for 5000 calls/day
- Foursquare: Free tier 1000 calls/day; $0.01/call after

## Error Handling

- `ZERO_RESULTS`: Widen the search radius or use a different `includedType`
- `OVER_QUERY_LIMIT`: Rate limited — back off 1 second and retry
- `REQUEST_DENIED`: Check API key and billing status
- `INVALID_REQUEST`: Verify lat/lng coordinates and radius (max 50000m)
