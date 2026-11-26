# SIVA service evidence
Reviewed 2026-11-26 from user-supplied official PDFs.

## Sources
- INFORMES-AUDITORIA-INTERNA-BASADA-EN-RIESGOS-2022.pdf, 243 PDF pages; operations audit printed pp. 27–28 (PDF pp. 29–30).
- INFORME-DE-GESTION-EMPALME-GERENCIA-SIVA-SAS-2024.pdf, 256 PDF pages; printed pp. 119–120 (PDF pp. 120–121), tables 2–3.
- Informe-de-Gestion-SIVA-SAS-Vigencia-2025.pdf, 91 pages; pp. 21, 23–32.
Original PDFs not yet archived in GitHub. The relevant 2022/2024 tables were visually inspected against the supplied copies.

## Historical ETLF versus PSO at 2024-10-30
| Route | ETLF interval min | ETLF km | ETLF fleet | PSO weekday peak interval min | PSO km | PSO fleet |
|---|---:|---:|---:|---:|---:|---:|
| R100 | 7 | 32.4 | 15 | 12 | 31.0 | 10 |
| R101 | 7 | 32.2 | 15 | 12 | 31.0 | 10 |
| R214 | 5 | 22.6 | 19 | 8 | 22.3 | 12 |
| R313 | 6 | 20.3 | 12 | 9 | 20.8 | 10 |
| R316 | 7 | 29.1 | 13 | 10 | 12.6 | 5 |
| R412 | 7 | 29.2 | 15 | 8 | 28.1 | 15 |
| R513 | 6 | 27.6 | 15 | 9 | 17.4 | 8 |
| R515 | 7 | 17.3 | 10 | 8 | 22.3 | 13 |
| R561 | 7.5 | 16.5 | 10 | 8 | 18.9 | 11 |
| R562 | 6 | 29.2 | 16 | 8 | 29.1 | 16 |
| R315 | 6 | 29.9 | 17 | | | |
| R416 | 4 | 23.2 | 17 | | | |

2024 report explicitly limits table 3 to weekday peak and says intervals and fleet vary by period. No off-peak/Saturday intervals or exact peak windows established. R315/R416 not among the ten routes in the 2025 operating network. Do not assume 2024 headways remain current, particularly on modified routes.

## Calendar
2022 design (audit printed p28): Mon–Sat 05:00–22:00, Sun/holidays 06:00–20:00, first/last dispatch. Design is not actual operation.
2025 report pp23–24:
- 2022-12-03: Mon–Sat 05:00–21:00; Sun 06:30–19:00.
- 2024-04-01: weekdays 05:00–20:00, Sat 06:00–20:00, Sun 07:00–19:00.
- 2024-08-05: Sat 06:00–19:00; Sunday suspended.
- End 2025: weekdays 05:00–20:00, Sat 06:00–19:00, no Sunday or holiday service for financial reasons.
These are service windows; exact first/last departures by direction remain unknown. Use latest documented regular calendar provisionally; verify 2026 changes. Static transport-network hours agree; show-buses appears to retain old hours.

## Route changes
2025 report pp23–30: R316 restored original alignment 2024-12-14; R513 temporary extension 2025-09-20 via Terminal, Hospitalito San Martin, Carrera 23, hospital zone; IPK chart identifies 513, 513L, 513T. R412 extension 2025-11-22 to north (Populandia, Villamaruamake, La Victoria, Galan, El Limonar), 28.1 to 30.2 km, chart code 412E. API R412 approx 28.91 km; R513 approx 17.22 km. Length discrepancies alone cannot establish alignment. R100 and R101 explicitly circular in PSO table; test full-loop patterns before assigning independent direction departures.

## Additional services
2025 report p31: opening partial runs on 562,100,313,515; closing partial runs on 100,515 to maintain downtown service until approximately 19:00. No exact dispatches or reliable mapping to API suffixes established. Do not add independent full-day variant frequencies.
P32: Christmas route operated Fri–Sun 18:00–22:00 from 2025-12-05 to 2026-01-04; expired seasonal service, no proven connection to R-TUR.

## Operator and fares
2025 report p21: Movivalle SAS established through resolution 004648 dated 2022-10-06; unified operator, SIVA SAS managing authority. Card permits transfers within 45 minutes. P23: fare COP 2900 effective 2025-01-13, not verified for 2026.

## Open work
Find current PSO and off-peak/Saturday headways; verify variant validity, first/last dispatches, circular trip semantics and 2025 alignments; verify 2026 fare and calendar. Preserve geometry exceptions and original API records. No production schedule assumptions applied.
