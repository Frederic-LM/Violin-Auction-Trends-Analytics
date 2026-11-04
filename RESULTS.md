# Results, data version 1.18

Frozen 2026-11-04. Every figure below is computed from that version (`tools/figures.py`); the per-maker lists are
`maker_cagr_master_list.csv` (violins) and `maker_cagr_master_list_bows.csv` (violin bows). Violins and bows are
measured separately and never mixed.

Real growth = the yearly growth of a maker's prices after inflation (2026 US dollars, US CPI, buyer's premium
included), the slope of a straight line fitted to the logarithm of the price against the year of sale. It is
measured on the sales from 1975 on for every maker, so that makers can be compared. Only deceased makers with
at least 10 counted sales over at least 15 years are measured. Method: [METHODOLOGY.md](METHODOLOGY.md).

## Violins

639 makers measured, out of 3,893 with at least one counted sale. Median real growth: **0.61 % a year**.

| Fate | Makers | Share |
|---|---|---|
| Lost real value (below -1 % a year) | 100 | 15.6 % |
| Roughly held (-1 % to +1 %) | 270 | 42.3 % |
| Gained real value (above +1 %) | 269 | 42.1 % |

227 makers (35.5 %) are below zero; 143 above +2 %, 34 below -2 %.

| Region | Median growth (% a year) | Makers |
|---|---|---|
| Italy | 1.70 | 197 |
| Benelux | 0.88 | 13 |
| North America | 0.78 | 23 |
| UK & Ireland | 0.60 | 104 |
| World (Rest of) | 0.49 | 5 |
| Central Europe | 0.34 | 106 |
| France | -0.18 | 191 |

| Century of the maker | Median growth (% a year) | Makers |
|---|---|---|
| 17th c. | 1.95 | 24 |
| 18th c. | 1.09 | 128 |
| 19th c. | 0.48 | 252 |
| 20th c. | 0.32 | 235 |

Region and century (cells with at least 10 makers):

| Region | Century | Median growth (% a year) | Makers |
|---|---|---|---|
| Central Europe | 18th c. | 0.45 | 32 |
| Central Europe | 19th c. | 0.64 | 42 |
| Central Europe | 20th c. | -0.36 | 31 |
| France | 18th c. | 0.41 | 24 |
| France | 19th c. | -0.11 | 102 |
| France | 20th c. | -0.91 | 65 |
| Italy | 17th c. | 1.86 | 20 |
| Italy | 18th c. | 1.86 | 42 |
| Italy | 19th c. | 2.04 | 50 |
| Italy | 20th c. | 1.44 | 85 |
| North America | 19th c. | 1.63 | 11 |
| North America | 20th c. | -0.13 | 12 |
| UK & Ireland | 18th c. | 1.52 | 27 |
| UK & Ireland | 19th c. | 0.35 | 44 |
| UK & Ireland | 20th c. | 0.22 | 32 |

Long run: 40 makers have at least 5 sales before 1950; their growth over all their sales is shown on the website as a second line (not used in the figures above).

## Violin bows

198 makers measured, out of 778 with at least one counted sale. Median real growth: **0.89 % a year**.

| Fate | Makers | Share |
|---|---|---|
| Lost real value (below -1 % a year) | 24 | 12.1 % |
| Roughly held (-1 % to +1 %) | 82 | 41.4 % |
| Gained real value (above +1 %) | 92 | 46.5 % |

56 makers (28.3 %) are below zero; 56 above +2 %, 9 below -2 %.

| Region | Median growth (% a year) | Makers |
|---|---|---|
| France | 1.38 | 98 |
| Central Europe | 0.80 | 60 |
| UK & Ireland | 0.57 | 27 |
| World (Rest of) | -0.10 | 13 |

| Century of the maker | Median growth (% a year) | Makers |
|---|---|---|
| 18th c. | 2.10 | 10 |
| 19th c. | 1.53 | 80 |
| 20th c. | 0.50 | 108 |

Region and century (cells with at least 10 makers):

| Region | Century | Median growth (% a year) | Makers |
|---|---|---|---|
| Central Europe | 19th c. | 1.81 | 17 |
| Central Europe | 20th c. | 0.63 | 42 |
| France | 19th c. | 1.50 | 51 |
| France | 20th c. | 0.53 | 39 |
| UK & Ireland | 20th c. | -0.13 | 17 |
| World (Rest of) | 20th c. | -0.36 | 10 |

Long run: 3 makers have at least 5 sales before 1950; their growth over all their sales is shown on the website as a second line (not used in the figures above).

## Robustness and precision

How these figures change under other data choices, and how precise they are: [ROBUSTNESS.md](ROBUSTNESS.md).
