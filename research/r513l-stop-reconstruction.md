# R513L stop reconstruction
Review of archived SIVAlliu network and route detail data, 2026-11-26.

The 2025 SIVA management report pp. 27–28 describes the extension via Terminal de Transportes, Hospitalito San Martín, Parque San Martín, Carrera 23 and the hospital zone. R513L matches these references better than R513. User-supplied OSM export dated 2026-11-26 corroborates the alignment. Current service status is not independently confirmed.

## Candidate projection
All 669 network source stop records projected onto each raw R513L polyline using local planar scaling (109400 m/degree longitude, 110600 m/degree latitude). Nearest segment distance and cumulative along-line distance. Deduplication here uses exact source coordinate strings and trimmed uppercase names.
| Metric | go | back |
|---|---:|---:|
| Within 25 m | 89 | 64 |
| Within 50 m | 101 | 72 |
| Unique coordinate/name groups within 50 m | 61 | 45 |
| Original R513 records within 50 m | 30 | 18 |
| R513L records within 50 m | 7 | 7 |

All seven explicitly assigned variant records are close to both shapes. Direction labels of other routes are not transferable. Do not include all nearby stops or assume all depot records permit boarding.

## New corridor candidates
Raw go geometry starts at Lorenzo and ends near Gobernación; raw back returns to Lorenzo. Distances below are approximate; source IDs refer to archived network.json.
| Candidate | Source IDs | go distance m | go chainage m | back distance m | back chainage m |
|---|---|---:|---:|---:|---:|
| Hospital Calle 44 | 21636 | 2 | 4658 | 13 | 5135 |
| Parqueadero Municipal | 21637,21844 | 0 | 5038 | | |
| Terminal de Transporte | 21838,22062 | 18 | 5139 | | |
| Parqueadero Municipal | 21652 | 9 | 5572 | | |
| Hospital Calle 44 | 21653 | 11 | 5847 | | |
| Hospital Rosario Pumarejo | 21875,21917,22173 | | | 28 | 894 |
| Catedral Ecce Homo | 21791,21857,21940,22143 | | | 3 | 982 |
| María Mulata | 21792 | | | 2 | 1285 |
| Clínica Santa María del Caribe | 21793 | | | 10 | 1523 |

Blank cells indicate no candidate within 50 m in that direction. These are geometric candidates only, not confirmed service stops.

## Open checks
- Compare same-location direction pairs and road side; retain explicitly assigned variant records in their source direction only.
- Inspect 2025 alignment near Hospitalito and Parque San Martín; no matching named stop appears in the 50 m candidate lists. A nearby facility does not establish a boarding point.
- Check multiple depot and Mercado records near go chainage 9.5–9.8 km; avoid false terminal split.
- Confirm operational direction and service status before replacing the original R513 pattern.
- Keep public route number R513 and PSO peak headway 540 seconds; no additional independent R513L frequency.
- R412E remains unresolved because the OSM export lacks reliable neighborhood objects.
No production shapes or stop_times changed.
