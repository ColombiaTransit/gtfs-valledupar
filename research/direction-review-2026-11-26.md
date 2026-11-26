# Direction and loop review — 2026-11-26

Source: archived SIVAlliu route JSON and geometry audit. Distances are approximate planar meters. Source ID order is supporting evidence, not an explicit sequence field. No raw data modified.

## Ambiguous projection candidates
- R101 IDA 21694: choose 2749 m rather than 7584 m; adjacent IDs 21693 and 21695 project to 3017 and 2168 m.
- R313 IDA 21783: choose 12235 m rather than 11427 m; PIR Patio I lies 5 m from go endpoint, next ID 21784 at 11600 m.
- R316 IDA 21838: choose 12471 m rather than 8810 m; adjacent IDs 21837 and 21839 at 12628 and 12069 m.
- R313L IDA 22201: choose 12810 m rather than 11413 m; Lorenzo is 7 m from go endpoint.
- R513L IDA 22208: choose 0 m rather than 507 m; Lorenzo is 11 m from go start and 10 m from back end.

## Direction exceptions
- R561: swap go/back mapping as candidate (52/54 within 50 m). IDs 22059 and 22060 remain 114 and 87 m from corrected REGRESO shape. On back they occur at 9052 and 8878 m, respectively. Both are near the seam with IDA ending at 8871 m (PIR Patio I). Consider relocating the shape seam at depot rather than flipping passenger direction. Needs review of service termini.
- R513: IDA ends at PIR Patio I (6942 m on go) but go continues to 8830 m. REGRESO starts at PIR Patio R (6952 m on go, only 2 m from line). IDs 22005, 22004, 22003 project at 8062, 8270, 8638 m on go; their following REGRESO stops fit back. Candidate: split go at depot, prepend remaining go segment to back.
- R515: IDA ends at PIR Patio I (9052 m on go); REGRESO starts at PIR Patio R (9061 m on go). IDs 22192, 22191, 22190, 22189 project at 9235, 9564, 9937, 10402 m on go, in sequence before back stops. Candidate: relocate direction seam to depot, prepend go tail to back. go/back original seam gap ~1 m.
- R313: 21835 ICA fits go near terminal (11991 m), but preceding REGRESO terminal 21836 is at back 7 m. 21815 NANDO MARIN fits go at 2032 m but is 940 m from back. Isolated exceptions; do not automatically move to IDA, possible obsolete stop assignments or route changes.
- R515N: IDA 22196 Centro fits back (11 m) rather than go (106 m). Source stop order alone cannot establish whether stop or shape is wrong.
- R-TUR: three REGRESO stops fit go at 3306, 5510, 8665 m; only one remaining REGRESO stop fits back. One stop each at source loop start and near back end. Consider a single loop trip or a different operational split, pending service evidence. Do not generate a one-stop trip.

## Status
All five ambiguity candidates have geometric and/or adjacent-ID evidence. R513/R515 are strong seam relocation candidates, not simple mislabeled stops. R561 direction swap is strong but insufficient alone. R313, R515N, R-TUR need additional review. No production overrides applied. Next: implement non-destructive candidate geometry transformations and validate resulting ordered stop projections, then verify service assumptions.
