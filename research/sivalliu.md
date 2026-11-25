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

No source APK has been uploaded to this repository, no API responses have been validated, and no GTFS feed has been generated. Preliminary findings are not a confirmed API contract.
