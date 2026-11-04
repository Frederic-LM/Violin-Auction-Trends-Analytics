# Methodology

> **DRAFT for the author's review (4 Nov 2026). Not final.**

How the auction data are built and how the results in [RESULTS.md](RESULTS.md) are measured. Every rule is given with
its reason. The detailed checks, with their tables, are in [ROBUSTNESS.md](ROBUSTNESS.md). Figures are those of data
version 1.17 (frozen 3 November 2026).

The lots themselves are public, one file per sale, in
[Historical Violin Trade Datasets](https://github.com/Frederic-LM/Historical-Violin-Trade-Datasets) (`Auctions/`).
Where they come from, house by house and period by period, is in that repository's `Auctions/COVERAGE.md`.

Contents
1. Why the data were rebuilt
2. Sources
3. One line per lot
4. Dates and auction houses
5. Prices
6. Makers
7. Attribution
8. Which lots are counted
9. The growth measure
10. Robustness and precision
11. Other measures on the website
12. Checks
13. Known limits
14. Versions

---

## 1. Why the data were rebuilt

The usual way to study the violin market is through published compilations of auction results. They are very useful,
but for research they have three problems:

- **They do not always say what a price is.** Some figures are the hammer price, others include the buyer's premium,
  and the premium itself changed many times (none in London before 1975, then 10 %, 15 %, 20 %, 25 %, 27 % today).
- **They contain errors** that only the auction houses' own documents reveal: a wrong price convention, a wrong day,
  a lot given to the wrong maker or to the wrong member of a family.
- **They do not publish their method**, and their coverage of a given market changes over time.

Research needs to say, for every price, what it contains and where it comes from. The data were therefore rebuilt
from the auction houses' own documents wherever they exist; compiled records only fill the gaps, checked against each
other.

## 2. Sources

**Primary: the auction house's own document.** Results pages and results documents published by the house, printed
price lists issued after the sale, and the house's catalogues (for the description and the attribution), including the
printed catalogues and price lists of the author's collection, typed lot by lot. Thirteen houses are covered this way
over long periods, among them Vichy Enchères, Bonhams, Skinner, Christie's, Sotheby's, Phillips, Ingles & Hayday, and
the auction houses Tarisio and Amati for their own sales.

**Secondary: any other source.** Where the house's own document is not held (mostly older sales and smaller houses),
a lot is taken from another record of the sale: the author's own notes (hammers written by hand in a catalogue during
the sale); the *Illustrated Yearbook of String Instruments* by Claudio Amighetti (1993–1999, 2005), which reprints the
houses' results and descriptions; for 1857–1911, the auction reports of The Violin Times and The Cremona; and published
compilations of auction results (Tarisio's archive, Amati's records, Maestronet's price history). No secondary record
is taken as it stands: it must name a real sale (house and date), its price is brought to the sale's convention
(section 5), it is compared with every other record of the same sale, and it gives way to the house's own document
wherever one turns up.

**Three levels**, given on every lot of the public files:
- *Primary*: the house's own document;
- *Secondary*: any other source (the author's own notes, published compilations, the press);
- *Cross-checked*: a secondary price that a second, separate record gives alike (the same price, or one differing only
  by the house's premium). Two records count as one where one visibly copies the other.

Version 1.18 holds 128 948 lots (1829–2026). Of the 77 243 lots counted in the analysis, 47 % come from the house's
own documents and 20 % are cross-checked; 3 % rest on the yearbook or the press alone, and 30 % on a single compiled
record of another house's sale (for example a Sotheby's lot known only from Tarisio's archive). The results hold
without these last (section 10).

## 3. One line per lot

The same lot often appears in several sources. It must be counted once, and the best source must give its facts.

**The house's own data first.** When the house's document gives a lot, its maker, attribution, price and date are kept.
Another record may only fill what the house does not give (the exact day, a lot number, a maker identifier), and every
value filled in this way says where it comes from. A record's copy of a lot the house itself gives is not counted.

**Matching the same lot across sources.** Two lines are the same lot when they are the same kind of object (instrument
or bow), at the same house, on the same day (or in the same month, when one source gives only the month), and either
carry the same lot number with prices that agree once the sale's price convention is taken into account, or name the
same maker at the same price. A lot number alone is not enough: some houses restart their numbering at every sale.
Two lines from the same source are never merged (three identical bows sold the same day stay three lots).

**Testing the matching against chance.** The matching is run again with the sale dates of one group of sources moved
by a year, so that every pair still accepted is a coincidence. Chance pairs divided by the pairs the real run accepts
between the same sources estimate the share of accepted matches that are false: 0.5 % over all pairs of sources tested
(0.6 % for the largest pair; at most 1.0 % for any pair with at least 1 000 matches). Every new matching
rule goes through this test (ROBUSTNESS.md, section 7).

**One lot, one price.** House, day and lot number identify a lot. When two records give it at prices no buyer's
premium explains, one is wrong: the case is settled by rule (the yearbook when another record agrees with it; the price
that fits the lot's estimate), or read by hand with the house's own description. A lot the house reports as bought in
or withdrawn is not a sale, whatever another record says.

## 4. Dates and auction houses

- **The day of the sale** comes from the house, or from another record of the same lot.
- **One name per house.** A house recorded under several names is brought under one. A sale room (Hôtel Drouot) is
  not a house.
- **A house inferred from the day.** A lot with an exact day but no house name takes the house that sold on that day,
  when only one is known, and is marked as inferred. Houses whose results we hold in full are never inferred.
- **Lots with no house are not counted** (15 675 lots): a lot that cannot be placed in a real sale cannot be checked.
  Almost all are records that give only the month.
- **Trade sales are not counted** (4 060 lots). Some houses sell trade instruments (for restoration, workshop stock,
  cheap instruments) in separate sales or on a separate day: Tarisio's T2 online sales and its earlier "speculative,
  restorable and trade" sales, Vichy Enchères' first day and its September sales. They are a different market, with
  different fees; one house setting them apart while another mixes them in would bias a comparison.

## 5. Prices

**The house's own figure, in the sale's currency.** Dollars, pounds and euros are computed from it at the official
monthly exchange rate (Bank of England from 1975, European Central Bank from 1999, fixed parities before), never with a
compilation's own conversion.

**One kind of price: the price paid** (hammer plus buyer's premium), what most houses publish and what buyers pay. The
hammer is kept beside it when known. Each house's buyer's premium over time is documented with its source (house's
terms, printed catalogues) in the house's README in the data repository.

**The rounding test.** Auctioneers knock down round figures: a price with the premium, divided by the right factor
(1.10, 1.15, 1.20, 1.25...), gives back a round hammer. This finds each sale's convention and currency, and catches
records that applied the wrong premium (for example a whole sale with the premium added twice).

**Houses whose convention changes lot by lot.** Vichy Enchères' documents give the hammer for some lots and the price
with fees for others. Every Vichy lot is brought to one rule: the hammer plus the house's premium of the period (the
online bidding fee left out: a buyer in the room does not pay it). Records of Vichy sales that we do not hold are
brought back to the hammer with the factor that record used for that sale, then given the same premium.

**Printed price lists and annotated catalogues.** A house's printed list of prices realised replaces a record's price
for the same lot; a record far from the list (more than 35 %) is checked by hand, as it is usually another lot. In a
catalogue with the hammers written in by hand during the sale, the printed text is primary and the written hammers are
the author's notes (secondary, cross-checked when a separate record agrees). A misprint is kept as printed in the
public file, with a note saying how it was read.

**Inflation.** The analysis uses US dollars brought to 2026 dollars with the US consumer price index (CPI-U).

## 6. Makers

**Numeric identifiers.** Each maker has one number, so that spellings, accents and word order do not split a maker's
sales. The numbers follow Tarisio's public index where it has the maker; others get numbers in separate ranges.

**Linking a name to a number.** In order: the same lot already identified in another source; a strict name match
(any word order, accents, generation marks); surname with initials or birth year; known aliases. A doubtful link is
decided by hand, never by a similar surname alone. The same maker under two numbers (spellings, a firm's trade names)
is merged; modern factory brands are not makers.

**When the name does not say which maker.** A family name alone ("Bazin", a "Dodd" stamp) does not say which member
made the instrument: such lots are kept, not counted. For Collin-Mézin, whose three generations used the same name,
the instrument's year decides (to 1901 the father, 1902–1930 the son, from 1931 the grandson); for 1902–1910, when the
son ran the workshop on the father's model, only the house's own words decide. A record's maker never overrides the
house's words.

**The maker file** gives each maker's country, century, birth and death years; countries were checked against the
towns where makers worked.

## 7. Attribution

**Every lot is kept; only lots the house gave to a maker at the time of the sale are counted.**

| Attribution | Example | Counted |
|---|---|---|
| accepted | "a violin by X", a firm ("W. E. Hill & Sons") | yes |
| attributed | "attributed to", "ascribed to", "probably by" | no |
| school, circle, workshop, style | "school of X", "workshop of X" | no |
| labelled | "labelled X", with no attribution | no |
| anonymous | "a violin, Germany, circa 1880" | no |
| composite, several items | "a composite violin", "five bows" | no |

The house's wording decides. Lots not counted keep the maker they refer to, because they can be sleepers: an
instrument sold as "school of" may be attributed later.

## 8. Which lots are counted

A lot is counted when all of the following hold (a lot left out is listed under the first rule it fails):

| Rule | Why | Lots left out (v1.18) |
|---|---|---|
| attribution accepted | the market for a maker's own work | 27 024 |
| auction house known | a lot that cannot be placed in a sale cannot be checked | 15 675 |
| not a trade sale or trade day | another market (section 4) | 4 060 |
| the maker is known for certain (no family name alone; Collin-Mézin by year) | which maker is not known | 1 009 |
| full size (no ½, ¾, 7/8 violins or violin bows) | another market | 969 |
| no description of a student, damaged, repaired or non-pernambuco instrument | not the maker's normal work | 767 |
| not a second record of a lot already counted | one lot, one count | 752 |
| not implausibly cheap: under a tenth of the maker's usual price **and** under half the maker's cheapest sale (same type, within 10 years); or under 0.3 times the maker's cheapest sale in Tarisio's archive | a broken or doubtful instrument, or a reading error | 440 |
| cracks or missing parts, below high value (read one by one) | not the maker's normal work | 107 |
| not bought in, withdrawn, or another lot according to the house's documents | the house's own result wins | 104 |

A further 798 accepted lots have no maker identifier yet. Lots left out stay in the data. **77 243 lots are counted**:
violins 34 378, violin bows 26 204, cello bows 5 729, violas 3 767, cellos 3 385, viola bows 3 267, double basses and
their bows 512.

## 9. The growth measure

`analyze.py` in this repository:
- **deceased makers only**; a sale counts from the maker's 25th year (an earlier one is a misattribution);
- **at least 10 sales over at least 15 years** (a practical minimum: enough sales to fit a line, over enough years for
  a trend);
- **sales from 1975 on** for every maker (setting `SALES_FROM_YEAR`);
- prices in 2026 US dollars (US CPI);
- **real growth** = the slope of a straight line fitted by least squares to the logarithm of the real price against
  the year of sale, as a yearly rate, with its standard error (`Real_CAGR_SE`);
- countries grouped by violin-making tradition (Central Europe, Benelux, UK & Ireland, North America, Iberia); a group
  with fewer than 10 makers goes into "World (Rest of)".

Run on the counted lots, it gives the published lists exactly. Violins and violin bows are measured separately.

**What the measure is, and what it is not.** It is the yearly trend, after inflation, of the prices paid at public
auction for instruments attributed to a maker, among the lots that pass the rules above. It is not the change in value
of one given instrument, nor of an instrument of constant quality: if a maker's best instruments sold early and more
ordinary ones later (or the share of restored instruments, of provenance, of houses changes), the trend carries that
change of mix as well as the market's movement. Without an identifier of each instrument, a repeat-sales measure is not
possible.

**One maker, one vote.** The median and the three groups (lost more than 1 % a year, within 1 %, gained more than 1 %)
give each maker the same weight, whatever the number of sales: they describe the typical maker's fate, not the
market's total value. The groups describe the size of a maker's trend, not its statistical significance (section 10).

**Why 1975 for every maker.** In a straight-line fit, a sale far from the others in time weighs most: measured from
each maker's first sale, a few early sales could decide the result (Montagnana: 6.6 % a year from his first sale in
1955, 0.4 % from 1975). One common window makes makers comparable. 1975 is when the buyer's premium starts and when
coverage improves markedly, although it stays relatively thin until the early 1980s. The ranking of makers hardly
changes with the window; the level does. Earlier sales stay in the data and on the website.

**Deceased makers.** A maker counts as deceased when the death year is known; or when the maker would be over 85 today;
or, with no dates at all, when the maker file places the maker before the 21st century (43 of the 639 violin makers,
mostly firms; for them the 25th-year rule cannot be applied). Living makers are left out: they still sell new
instruments at their own price, and their record is short.

**Long run, by a neutral rule.** Every maker with at least 5 counted sales before 1950 (press reports included) also
gets a growth over all their sales, shown as a second line on the website (40 violin makers, 3 bow makers). No maker is
chosen by name: keeping the early press only for a chosen group would choose the data by the conclusion.

## 10. Robustness and precision

Each test changes one thing; the tables are in [ROBUSTNESS.md](ROBUSTNESS.md).

- **Other data choices** (major houses only, hammer prices, other windows, press reports added): Italy leads and
  France trails in almost every version; the median moves between 0.35 (hammer prices) and 1.36 (seven
  major houses only). The more of the ordinary market is included, the lower the median: recent lots of ordinary
  instruments sell below the same makers' lots at the major houses, and their share of the record grows after 2000.
  Neither version is "the" market: the counted lots aim at the whole public market, the major-house versions at its
  upper part.
- **Without the lots resting on a single compiled record:** the same spread of fates (15 / 43 / 42 %), Italy first and
  France last, makers in nearly the same order (rank correlation 0.83).
- **Other eligibility minimums** (5 sales over 10 years to 20 over 20): median 0.42 to 0.71; Italy first and France
  last at every threshold.
- **The implausibly cheap lots put back:** median 0.60 instead of 0.61.
- **Stricter definitions of deceased** (no-date makers out; death year known only): median 0.69 and 0.80; Italy first
  and France last.
- **Price paid or hammer price.** The results use the price paid (the cost of acquiring the instrument); the hammer is
  closer to what the room bid. Premiums rose over the period, so the two do not grow alike: median 0.61 with the price
  paid, 0.35 with the hammer. Part of the growth of what buyers pay is the growth of the premium.
- **A robust slope** (Theil–Sen, which a few outlying sales cannot pull): median 0.57, rank correlation 0.92 with the
  least-squares rates.
- **Precision of each maker's rate.** Median standard error 0.9 point a year (1.3 for makers with 10 to 19 sales, 0.5
  with 50 or more); allowing for lots of the same sale changes almost nothing. For two thirds of makers the 95 %
  interval includes zero: single makers' rates are often imprecise.
- **Precision of the summary figures:** a bootstrap that resamples whole auction sales (5 000 resamples): median
  0.61 (95 %: 0.45 to 0.80); Italy minus France 1.88 (1.62 to 2.26), Italy above France in every resample; France's
  median near zero (−0.47 to 0.00); the three groups vary by about 1.5 points. The same with the selection of makers
  rerun in each resample.

The bootstrap measures how much the results depend on the particular sales observed. It does not show that the auction
record represents the whole market, nor does it remove changes in the mix of instruments that reach auction.

## 11. Other measures on the website

- **Price index.** Each sale is compared only with sales of the same maker (least squares on the logarithm of the
  price, one level per maker and one per year), in 2026 dollars; years with fewer than 100 sales are left out. Not a
  repeat-sales index.
- **Fees.** The same index on the price paid and on the hammer, to separate what instruments gained from what the
  buyer's premium added. Seller's fees are shown where houses publish them; most negotiate them, so these are list
  rates.
- **Makers who reach auction.** The number of violin makers who ever worked is estimated from a register: of the 14 108
  maker records of Amati's online maker archive, 300 were drawn at random (Python `random.sample`, seed 20260928) and
  196 (65 %) were distinct violin-family makers, giving about 9 200 makers (95 % interval from the sampling error:
  8 457 to 9 977). A full count of Vannès's *Dictionnaire universel des luthiers* (a digital copy based on the 1981
  edition; the author also holds the 1993 printed edition) gives a similar order. The interval covers sampling error
  within the register only: 9 200 estimates the makers such registers document, not a census. Makers then fall in four
  groups: growth measured; seen at auction but too rarely to measure; not seen in the records held; outside the maker
  file. Not seen is not proof of never sold: private sales and small regional auctions are not in the record.

## 12. Checks

After every rebuild of the data, automatic checks look at single lots, not totals: a lot counted twice, a record
counted beside the house's own line, a bow matched to an instrument, an implausible price, and every error once found
by hand (kept as a test so that it cannot come back). A version is frozen only when these pass. Finished sales are
locked: a later change to any of their lots is reported and must be deliberate.

## 13. Known limits

- **Coverage thins before 1980** (30 to 100 counted violin sales a year before 1983).
- **Condition is mostly unrecorded.** Obvious cases are removed (section 8); the rest is not controlled.
- **Attribution is the house's**, the expert's view at the time of the sale; a later opinion is not applied.
- **Two houses are not always two experts:** in France one expert often works for several houses.
- **The buyer's premium of 2000–2001** at the major London houses is assumed (17.5 %): no source was found.
- **Composition:** the share of ordinary instruments in the record grows after 2000 (section 10).
- **No instrument identifier**: the same instrument sold twice counts as two sales, so the sales of one maker are not
  fully independent; no standard error here allows for it.
- **Price index for 2025–2026** is an estimate (annual figures not yet published at the freeze); the index starts in
  1850 (one counted lot is older).
- **One numeraire**: all prices in US dollars deflated by the US index, the purchasing power of a dollar buyer;
  exchange rates move the dollar value of sales in pounds or euros. A test in each sale's own currency, with its own
  country's inflation, has not been run.

## 14. Versions

Each version of the data is frozen, never changed afterwards, and tagged; results always name their version.

| Version | Date | Main change | Violin makers measured | Violin median |
|---|---|---|---|---|
| 1 | 20 Oct 2026 | first freeze | 706 | 0.47 |
| 1.2 | 21 Oct 2026 | lots with no house not counted | 617 | 0.56 |
| 1.3 | 22 Oct 2026 | yearbooks 1993–1999 added; sources closed | 632 | 0.58 |
| 1.9 | 23 Oct 2026 | the same lot counted twice removed | 629 | 0.53 |
| 1.12 | 2 Nov 2026 | sales from 1975 on for every maker | 638 | 0.57 |
| 1.17 | 3 Nov 2026 | house names cleaned | 639 | 0.58 |
| 1.18 | 4 Nov 2026 | lots listed twice by a record, and recorded sales of lots the house did not sell, removed | 639 | 0.61 |
