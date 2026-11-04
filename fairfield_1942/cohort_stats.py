"""Fairfield 1942 cohort: summary figures from the per-maker outcomes file alone.

Usage: python cohort_stats.py fairfield_1942_cohort_outcomes.csv
Needs no auction transaction file. Reproduces the counts, AUC and Spearman rho in README.md.
"""
import csv, sys, statistics as st
from scipy import stats


def num(v):
    try:
        return float(v) if v not in ('', None, 'None') else None
    except ValueError:
        return None


def summary(rows, label):
    n = len(rows)
    surv = [o for o in rows if o['survived_post1990'] == 'True']
    anysale = sum(1 for o in rows if int(o['n_sales'] or 0) > 0)
    print(f"\n{label}: n={n}; any sale={anysale}; survived after 1990={len(surv)} ({100 * len(surv) / n:.1f}%)")
    g = [num(o['real_cagr_pct']) for o in rows if num(o['real_cagr_pct']) is not None]
    if g:
        print(f"  growth measurable={len(g)}: >+1% {sum(x > 1 for x in g)}, within ±1% "
              f"{sum(-1 <= x <= 1 for x in g)}, <-1% {sum(x < -1 for x in g)}; median {st.median(g):.2f}%/yr")
    s1 = [num(o['price1942_mid']) for o in rows if num(o['price1942_mid']) is not None and o['survived_post1990'] == 'True']
    s0 = [num(o['price1942_mid']) for o in rows if num(o['price1942_mid']) is not None and o['survived_post1990'] != 'True']
    if s1 and s0:
        u, p = stats.mannwhitneyu(s1, s0, alternative='two-sided')
        print(f"  1942 price: survivors median ${st.median(s1):.0f} (n={len(s1)}), vanished ${st.median(s0):.0f} "
              f"(n={len(s0)}); AUC={u / (len(s1) * len(s0)):.2f}, p={p:.3f}")
    gp = [(num(o['price1942_mid']), num(o['real_cagr_pct'])) for o in rows
          if num(o['real_cagr_pct']) is not None and num(o['price1942_mid']) is not None]
    if len(gp) > 3:
        rho, p = stats.spearmanr([a for a, _ in gp], [b for _, b in gp])
        print(f"  1942 price vs real growth: Spearman rho={rho:.2f}, p={p:.3f}, n={len(gp)}")


if __name__ == '__main__':
    rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
    summary([o for o in rows if o['cohort'] == 'main'], 'MAIN (livelihood stated)')
    summary([o for o in rows if o['cohort'] in ('main', 'broad')], 'BROAD (main + no evidence)')
