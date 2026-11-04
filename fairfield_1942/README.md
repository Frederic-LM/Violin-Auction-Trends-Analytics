# Fairfield 1942 cohort

American violin makers listed with prices in 1942, followed in the auction record to today.

This folder accompanies Section 7.3 of Levi Mazloum, F. (2026), *The verdict never rendered* (manuscript under review). It tests whether the market sorts contemporary makers over time. The test uses a group of makers fixed in advance by someone else, not makers chosen after their fortunes were known.

## Source and data

Fairfield, J. H. (1983). *Known violin makers* (4th ed.). Virtuoso Publications. (Original work published 1942). American section, pp. 129–188.

The coded entries (names, 1942 prices, status, matched auction names) are published with their full description in the data repository: [Historical Violin Trade Datasets, `Historical price catalogue/1942-JohnH.Fairfield/`](https://github.com/Frederic-LM/Historical-Violin-Trade-Datasets/tree/main/Historical%20price%20catalogue/1942-JohnH.Fairfield). A copy of the entries file is kept here so the scripts run on their own. The source, the transcription, the column list and the hand-checked name matches are described there.

## Files

- `fairfield_1942_american_entries.csv` (copy of the data repository's file): one row for each of the 176 entries. Each row gives:
  - the cohort status and the words in the entry it rests on;
  - the price as printed;
  - the violin price used;
  - the matched auction name, or the reason a name was left unmatched;
  - the book page.
- `fairfield_1942_cohort_outcomes.csv`: auction outcomes for each entry (1942 price, number of sales, first and last sale year, survival after 1990, median 2010–25 price, real growth rate). It contains no individual sale prices.
- `cohort_stats.py`: reproduces every figure below from the outcomes file alone:
  `python cohort_stats.py fairfield_1942_cohort_outcomes.csv`
- `cohort.py`: rebuilds the outcomes file from the entries and an auction transaction file in the schema of `../all_violin_sales_template.csv` (counted violin lots). When the lots carry a `maker_id`, each lot takes its maker's name from `../makers_meta.json`, so a maker's sales count under every spelling the auction houses used:
  `python cohort.py fairfield_1942_american_entries.csv <auction transactions>.csv [../makers_meta.json]`

## Who is in the cohort

Status was set from the text of each entry before any auction data were consulted.

**Main group.** A maker is a professional when the entry states a livelihood in the trade:
- his own shop, atelier or business;
- employment with a dealer, firm or workshop;
- repair or restoration work;
- a guild master's qualification.

**Broad group.** The main group plus the makers whose entries say nothing either way.

**Left out:**
- amateurs and non-commercial makers;
- makers whose main occupation lay elsewhere (physicians, professors, teachers, an electrician);
- entries mixing amateur and trade descriptions;
- firms with no instruments of their own;
- bow makers, since the auction data cover violins only;
- makers who had died before 1942.

**Borderline entries.** A handful were settled by reading the full entry. The reason is recorded in the status column.

**Prices.** The 1942 price is the midpoint of the violin price stated in the entry. Where an entry also prices violas, cellos or bows, only the violin price is used. Where it gives an earlier and a later price, the range runs from the earliest to the latest. An entry giving only a ceiling ("up to", "as high as") or a floor ("and up") uses that figure as both ends. These rows are marked in the file.

## How outcomes were measured

The rules below were fixed before any matching.

**Matching.** A maker is matched to an auction name only when the surname and first name agree and the birth year or city is consistent. Doubtful cases are listed and left unmatched. The auction name is the maker's name in `../makers_meta.json`; every lot with that maker's ID counts, whatever spelling the catalogue used (for example "Mario Frosali" and "Frosali, Mario Antonio").

**Lots.** Only lots counted in the main analysis: violins, firm attribution ("by" the maker), auction house known, no small sizes, no student or damaged lots.

**Survival.** A maker counts as surviving if at least one of his violins sold at auction after 1990.

**Real growth.** Growth runs from the 1942 price to the median auction price of 2010–25, both in 2023 dollars:
- prices are deflated with the US CPI-U annual average (1942 = 16.3; 2023 = 304.702; the 2024 index is used for 2025);
- the rate runs from 1942 to the median year of those sales.

**Two questions.**
1. Did the 1942 price rank the survivors above the others? This is measured by the area under the curve (AUC) from a Mann–Whitney test.
2. Did it predict later growth? This is measured by Spearman's rho.

Auction data: data version 1.17 of this repository (frozen 3 November 2026), counted violin lots.

## Results

Of the 69 professionals working in 1942:
- 21 (30%) still appear at auction after 1990, so about seven in ten have left no trace there;
- 14 have enough recent sales to measure real growth. Of these:
  - three rose by more than 1% a year: Sacconi (+2.6%), Becker (+2.0%) and Sindelar (+1.1%);
  - eight stayed within 1% either way;
  - three fell by more than 1% a year: Stenger (−3.8%), Heinz (−3.0%) and Wilkanowski (−1.1%). The first two rest on a single sale each.

Makers who were dearer in 1942 were more likely to remain at auction (median 1942 price $400 against $275; AUC 0.72, p = 0.012). That is to be expected, since auction houses take only instruments above a certain value.

With fourteen measurable makers, the 1942 price neither predicted nor failed to predict later growth (rho = +0.11, p = 0.71). Of the three dearest makers of 1942, Sacconi rose; Kaye has a single sale since, too few to measure; Litto has none.

| Group | Makers | At auction after 1990 | Measurable | Rose / flat / fell | AUC | rho |
|---|---|---|---|---|---|---|
| Main | 69 | 30% | 14 | 3 / 8 / 3 | 0.72 (p = 0.012) | +0.11 (p = 0.71) |
| Broad | 118 | 25% | 21 | 4 / 10 / 7 | 0.74 (p < 0.001) | −0.33 (p = 0.14) |

**Names checked by hand** (Gemünder, Gould, Heskett, Aerts, Wunderlich): see the data repository's README.

## Reproducing the figures

- **The figures:** `cohort_stats.py` recomputes every count, AUC and rho above from `fairfield_1942_cohort_outcomes.csv`, with no other input.
- **The outcomes themselves:** the auction lots are public, lot by lot, in the Historical Violin Trade Datasets repository (https://github.com/Frederic-LM/Historical-Violin-Trade-Datasets). Each matched maker's auction name is given in the entries file. Format the maker's counted violin lots to the template schema and run `cohort.py`.

## Limitations

- **"Disappeared" means absent from this auction dataset.** Private sales and small regional auctions are not covered.
- **The 1942 figures and the later figures are different kinds of price.** The 1942 figures are makers' asking prices for new instruments; the later ones are auction resales. The gap between the two pulls every growth rate down. The ranking of makers is less affected.
- **Several growth rates rest on one or two sales.** The number of sales is given for each maker.

## Citation

Levi Mazloum, F. (2026). *Violin Auction Trends Analytics* (data version 1.17) [Software and data]. GitHub: https://github.com/Frederic-LM/Violin-Auction-Trends-Analytics. Zenodo: https://doi.org/10.5281/zenodo.20686726 (all versions; each release has its own DOI on that page).

## Licence

Mozilla Public License 2.0, as for the rest of the repository. The source book remains under its own copyright.
