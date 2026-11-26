# SIVAlliu geometry audit — 2026-11-26

Source: data/sivalliu snapshot from Actions run 45815832527. All 669 distinct stop IDs in the network response match the union of route detail IDs (no missing or extra IDs). All 15 routes contain go and back geometry. All stop heading values are IDA or REGRESO.

Method: project stops onto each polyline segment in a local planar approximation (109400 m/degree longitude, 110600 m/degree latitude). Use 50 m tolerance. Flag ambiguity when an alternative projection is within 10 m of the best distance, within 50 m overall, and more than 100 m away along the line. This is a heuristic, not verified operational stop order.

| Route | IDA stops | REGRESO stops | go km | back km | >50 m on labelled direction | Ambiguous |
|---|---:|---:|---:|---:|---:|---:|
| R-TUR | 1 | 4 | 11.16 | 4.81 | 3 | 0 |
| R100 | 30 | 55 | 12.70 | 18.37 | 0 | 0 |
| R101 | 57 | 25 | 20.71 | 10.47 | 0 | 1 |
| R214 | 28 | 30 | 11.24 | 11.27 | 0 | 0 |
| R313 | 29 | 25 | 12.24 | 8.68 | 2 | 1 |
| R316 | 29 | 23 | 12.65 | 9.34 | 0 | 1 |
| R412 | 43 | 36 | 15.84 | 13.07 | 0 | 0 |
| R513 | 16 | 23 | 8.83 | 8.39 | 3 | 0 |
| R561 | 25 | 29 | 9.74 | 9.17 | 22 | 0 |
| R562 | 32 | 43 | 13.60 | 15.64 | 0 | 0 |
| R515 | 22 | 36 | 10.57 | 11.79 | 5 | 0 |
| R515N | 4 | 3 | 9.48 | 13.02 | 1 | 0 |
| R313L | 3 | 4 | 12.81 | 8.13 | 0 | 1 |
| R513L | 3 | 4 | 11.81 | 8.62 | 0 | 1 |
| R561DA | 3 | 4 | 9.47 | 9.32 | 0 | 0 |

633/669 match labelled direction within 50 m. All 36 exceptions match the opposite geometry within 50 m. No new geometry is justified on distance evidence alone.

## Exceptions (stop ID: labelled distance / opposite distance, meters)

- R-TUR: 21555 1080.2/9.5; 21554 642.1/0.8; 21556 1389.3/43.9.
- R313: 21835 154.5/28.9; 21815 939.9/1.9.
- R513: 22003 108.3/6.6; 22004 188.1/3.2; 22005 69.7/5.3.
- R561: 22053 173/3.6; 22054 143.9/4.5; 22011 88.6/7.4; 22012 171.6/8.9; 22010 88.9/1.5; 22052 105.7/1.6; 22055 82.9/5.3; 22013 83.3/7.8; 22007 79.9/15.2; 22058 110.6/9.5; 22046 172.6/1.1; 22019 165.8/1; 22045 193.1/0.9; 22020 199.8/5.6; 22044 193.2/0.6; 22021 58.9/3.8; 22032 201.8/2.1; 22029 209.3/8.4; 22030 57.8/1.3; 22031 151.1/2.2; 22035 132.2/8.7; 22034 196.8/12.
- R515: 22192 880.3/1.6; 22193 818.1/9.9; 22191 751.2/2.6; 22190 446.5/0.1; 22189 165/6.9.
- R515N: 22196 105.7/11.3.

R561 reversal hypothesis: 25/25 IDA stops fit back (mean 5.21 m), 27/29 REGRESO stops fit go (mean 10.76 m). Original pairing fits 14/25 IDA and 18/29 REGRESO. Reversed pairing fits 52/54, leaving two exceptions. Verify endpoints and remaining stops before adopting an override.

## Ambiguous projections

R101 IDA 21694 VILLA LIGIA; R313 IDA 21783 PIR Patio I; R316 IDA 21838 TERMINAL DE TRANSPORTE; R313L IDA 22201 Lorenzo; R513L IDA 22208 Lorenzo.

Next: resolve direction conventions and loop ambiguity, then export ordered stop sequences with shape distances. Preserve raw source JSON; do not automatically flip individual headings or regenerate shapes. Audit does not validate schedule or actual service.
