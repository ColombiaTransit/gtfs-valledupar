# SIVAlliu 3.2.10 — preliminary APK research

Source: user-supplied SIVAlliu_3.2.10_APKPure.xapk. Previous preliminary inspection reported Flutter/Dart ARM64, package com.sivalliu.dashfleet, version code 35, SHA-256 ae6c8e188903f55ae35aea69b9efeebee3538ae0d486def7c8ebf3005f5339e2. Reverify against the original archive before automated analysis.

## Candidate endpoints

- https://android.valliu.co/api/transport-network
- https://android.valliu.co/api/find-route
- https://android.valliu.co/api/show-buses

HTTP methods, parameters, access requirements and response schemas remain unverified.

## Reported transport symbols

AllRoutes.fromJson, AllStop.fromJson, AllPolylineRoutes.fromJson, TransportModelRouteAndStop, TransportModelFilteredRoute, VehicleToRoute.fromJson, VehicleToStopModel.fromJson, getTransportAllStops, getTransportPolylineRoute, refreshDataRoutesAndStops, refreshDataVehiclesToStop.

Candidate fields: route_id, route_short_name, stop_name, start_stop, end_stop, time_user_stop.

## Next steps

1. Verify archive hash and inventory APK contents.
2. Inspect compiled Dart AOT code (libapp.so) with a compatible Blutter version.
3. Establish exact public transport request methods, parameters and response schemas. Do not publish credentials or payment data.
4. Validate route, stop and shape coverage; investigate schedules and headways.
5. Keep measured headways distinct from official service frequencies.

The source XAPK is available in the [source-sivalliu-3.2.10 release](https://github.com/ColombiaTransit/gtfs-valledupar/releases/tag/source-sivalliu-3.2.10). GitHub reports 43,644,788 bytes and the SHA-256 listed above. No successful transport response has been validated and no GTFS feed has been generated. Preliminary findings are not a confirmed API contract.

## Browser tests (2026-11-25)

The user reports that GET requests to all three candidate URLs return `{"error":"The method specified in the request is not valid","code":405}`. The actual HTTP status and Allow header were not captured. POST is a hypothesis, not a confirmed method. Establish the read-only transport request contract from static code before testing.

## Research scope decision (2026-11-25)

Prioritize `transport-network` for static route, stop and shape data and `show-buses` for public realtime vehicle information and potential observed headways. `find-route` is out of scope: journey planning will be handled by OpenTripPlanner using our GTFS feed and OpenStreetMap. Do not investigate or call the journey-planning endpoint further. Payment functionality remains excluded.

The initial Blutter analysis (run 45646676734) succeeded. The follow-up run 45647292820 is still in progress at the time of this update; its detailed request evidence has not yet been reviewed.

## Request reconstruction — run 45649520378

All seven POST call sites were extracted successfully. Object-pool annotations confirm the following request keys (values are not all resolved):

| Response parser | Request keys | Explicit auth in caller |
|---|---|---|
| TransportModelRouteAndStop | city, with_stops, with_polyline, with_route, stops_and_route, lat, long | Bearer, runtime access token |
| TransportModel | city, stops_and_route, lat, long | No explicit auth header |
| TransportModelFilteredRoute | city, route_short_name, with_stops, with_polyline, with_route, lat, long | No explicit auth header |
| PulylineRoute | city, route_short_name, with_polyline, lat, long | No explicit auth header |
| VehicleToAllStop | latitud, longitud, stop_name, routes, heading | No explicit header argument |
| VehicleModel | latitud, longitud, stop_name, routes | No explicit header argument |
| VehicleToStopModel | latitud, longitud, stop_name, routes, heading | No explicit header argument |

TransportModel caller hardcodes city=valledupar, interpolates GPS coordinates as strings and sets Accept: application/json. VehicleModel uses empty strings for latitud, longitud and stop_name, and constructs a single-element route list from a function argument. Global client interceptors and server-side authorization requirements are unverified.

Candidate manual network probe (not yet executed): POST JSON {"city":"valledupar","stops_and_route":true,"lat":"10.4750","long":"-73.2500"}. Boolean true is a hypothesis pending inspection of the immediate instruction at assembly lines 398–400; coordinates are illustrative city-center values, not a user's location. No live response has been captured. Do not bypass authentication if required. Journey planning and payment remain excluded.
