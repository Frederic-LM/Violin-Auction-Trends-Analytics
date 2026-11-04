"""Fairfield 1942 cohort: survival and real growth of makers priced in 1942.

Usage: python cohort.py fairfield_1942_american_entries.csv <auction transactions>.csv [../makers_meta.json]
The transactions follow ../all_violin_sales_template.csv (counted violin lots). When they carry a maker_id and the
maker file is found, each lot takes the maker file's name, so a maker's lots count under every spelling the houses
used; otherwise the lot's own maker_name is matched. See README.md for the rules.
"""
import csv, json, os, re, sys, statistics as st
from collections import defaultdict
from scipy import stats

CPI = {
    1942: 16.3, 2010: 218.056, 2011: 224.939, 2012: 229.594, 2013: 232.957,
    2014: 236.736, 2015: 237.017, 2016: 240.007, 2017: 245.120, 2018: 251.107,
    2019: 255.657, 2020: 258.811, 2021: 270.970, 2022: 292.655, 2023: 304.702,
    2024: 313.689, 2025: 313.689
}


def to_float(val):
    if val is None:
        return None
    val_str = str(val).replace(',', '').strip()
    try:
        return float(val_str) if val_str != '' else None
    except ValueError:
        return None


def ambiguity_note(val):
    """The column holds a text reason (e.g. 'initials only') or is blank.
    Blank, 'false', '0' or 'no' mean not ambiguous; any other text is kept as the reason."""
    text = (val or '').strip()
    return '' if text.lower() in ('', 'false', '0', 'no') else text


def sale_year(row):
    for k in ('Sale Date Standard', 'Sale Date'):
        m = re.search(r'(19|20)\d\d', row.get(k) or '')
        if m:
            return int(m.group(0))
    return None


def load_names(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return {str(m['maker_id']): m.get('maker_name') for m in json.load(f) if m.get('maker_id') is not None}


def load_sales(path, names=None):
    names = names or {}
    sales = defaultdict(list)
    with open(path, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            mid = (row.get('maker_id') or '').strip()
            maker = (names.get(mid) or row.get('maker_name') or '').strip()
            if not maker:
                continue
            usd = to_float(row.get('USD'))
            sales[maker].append((sale_year(row), usd))
    return sales


def outcome(entry, sales):
    lo = to_float(entry.get('violin_price_min_usd'))
    hi = to_float(entry.get('violin_price_max_usd'))

    if lo is not None and hi is not None:
        mid = (lo + hi) / 2
    elif lo is not None:
        mid = lo
    elif hi is not None:
        mid = hi
    else:
        mid = None

    matched_name = (entry.get('auction_name_matched') or '').strip()
    ss = sales.get(matched_name, []) if matched_name else []
    years = [y for y, _ in ss if y is not None]

    # Real price in 2023 USD for sales between 2010 and 2025
    recent = [
        (y, u * CPI[2023] / CPI[y])
        for y, u in ss
        if y is not None and 2010 <= y <= 2025 and u is not None and u > 0
    ]

    ambiguous = ambiguity_note(entry.get('ambiguous_not_matched'))

    o = dict(
        maker=entry.get('maker', ''),
        cohort=entry.get('cohort', ''),
        auction_name=matched_name,
        ambiguous=ambiguous,
        price1942_mid=mid,
        n_sales=len(ss),
        first_sale=min(years) if years else '',
        last_sale=max(years) if years else '',
        survived_post1990=any(y > 1990 for y in years),
        n_sales_2010_25=len(recent),
        median_2010_25_usd2023='',
        price1942_usd2023='',
        real_cagr_pct=''
    )

    if recent and mid is not None and mid > 0:
        med = st.median(v for _, v in recent)
        yr = st.median(y for y, _ in recent)
        base = mid * CPI[2023] / CPI[1942]
        cagr = ((med / base) ** (1 / (yr - 1942)) - 1) * 100
        o.update(
            median_2010_25_usd2023=round(med),
            price1942_usd2023=round(base),
            real_cagr_pct=round(cagr, 2)
        )
    return o


def summary(rows, label):
    n = len(rows)
    if n == 0:
        print(f"\n{label}: n=0 (no records)")
        return dict(n=0, survived=0, measurable=0)

    surv = [o for o in rows if o['survived_post1990']]
    g = [o['real_cagr_pct'] for o in rows if o['real_cagr_pct'] != '']
    any_sale_count = sum(1 for o in rows if o['n_sales'] > 0)

    print(f"\n{label}: n={n}; any sale={any_sale_count}; "
          f"survived after 1990={len(surv)} ({100 * len(surv) / n:.1f}%)")

    if g:
        print(f"  growth measurable={len(g)}: >+1% {sum(x > 1 for x in g)}, within ±1% "
              f"{sum(-1 <= x <= 1 for x in g)}, <-1% {sum(x < -1 for x in g)}; median {st.median(g):.2f}%/yr")

    s1 = [o['price1942_mid'] for o in rows if o['price1942_mid'] is not None and o['survived_post1990']]
    s0 = [o['price1942_mid'] for o in rows if o['price1942_mid'] is not None and not o['survived_post1990']]

    if s1 and s0:
        u, p = stats.mannwhitneyu(s1, s0, alternative='two-sided')
        auc = u / (len(s1) * len(s0))
        print(f"  1942 price: survivors median ${st.median(s1):.0f} (n={len(s1)}), vanished ${st.median(s0):.0f} "
              f"(n={len(s0)}); AUC={auc:.2f}, p={p:.3f}")

    gp = [(o['price1942_mid'], o['real_cagr_pct']) for o in rows if o['real_cagr_pct'] != '' and o['price1942_mid'] is not None]
    if len(gp) > 3:
        rho, p = stats.spearmanr([a for a, _ in gp], [b for _, b in gp])
        print(f"  1942 price vs real growth: Spearman rho={rho:.2f}, p={p:.3f}, n={len(gp)}")

    return dict(n=n, survived=len(surv), measurable=len(g))


def main(entries_path, auction_path, meta_path=None):
    with open(entries_path, encoding='utf-8-sig') as f:
        entries = list(csv.DictReader(f))

    if not entries:
        print("No entries found in Fairfield dataset.")
        return

    sales = load_sales(auction_path, load_names(meta_path))
    out = [outcome(e, sales) for e in entries]
    fields = list(out[0].keys())

    with open('fairfield_1942_cohort_outcomes.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(out, key=lambda o: ({'main': 0, 'broad': 1}.get(o['cohort'], 2), o['maker'])))

    main_ = [o for o in out if o['cohort'] == 'main']
    broad = [o for o in out if o['cohort'] in ('main', 'broad')]

    summary(main_, 'MAIN (livelihood stated)')
    summary(broad, 'BROAD (main + no evidence)')

    amb = [str(o['maker']) for o in main_ if o['ambiguous']]
    names = ', '.join(amb) if amb else 'none'
    print(f"\nAmbiguous names in main cohort, not matched: {len(amb)} ({names})")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python cohort.py <entries_csv> <auction_csv>")
        sys.exit(1)
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(here, '..', 'makers_meta.json'))