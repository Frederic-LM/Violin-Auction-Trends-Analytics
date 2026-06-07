# Ana.py
# Copyright (C) 2026 Frédéric Levi Mazloum
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
MIN_SALES_REQUIRED = 10          # Requires N >= 10 sales
MIN_SPAN_REQUIRED = 15           # Requires Span >= 15 years
PROJECTED_TOTAL_MAKERS = 9200    # Reconciled Vannes baseline

# Choose "CPI", "LABOR", or "NONE"
ADJUSTMENT_INDEX = "CPI"

# Regional grouping toggle:
# True: Groups regions into Benelux, North America, Central Europe, UK & Ireland, Iberia
# False: Keeps all countries strictly separated.
GROUP_REGIONS = True

# Group low-volume countries (n < 10) into "Rest of World"
# True (default): Merges small countries so their data is preserved in plots/stats.
# False: Keeps them separate (they will be suppressed individually due to n < 10).
GROUP_LOW_N_COUNTRIES = True

# 21st Century Filter Toggle:
INCLUDE_21ST_CENTURY = False

# --- COMPREHENSIVE 1850-2026 CPI INDEX ---
CPI_INDEX = {
    1850: 7.5,    1851: 7.4,    1852: 7.4,    1853: 8.0,    1854: 8.6,
    1855: 8.9,    1856: 8.7,    1857: 8.9,    1858: 8.3,    1859: 8.4,
    1860: 8.4,    1861: 8.9,    1862: 10.2,   1863: 12.5,   1864: 15.6,
    1865: 15.9,   1866: 15.5,   1867: 14.5,   1868: 13.9,   1869: 13.3,
    1870: 12.8,   1871: 12.1,   1872: 12.1,   1873: 11.9,   1874: 11.4,
    1875: 11.0,   1876: 10.7,   1877: 10.5,   1878: 9.9,    1879: 9.9,
    1880: 10.2,   1881: 10.2,   1882: 10.2,   1883: 10.1,   1884: 9.9,
    1885: 9.7,    1886: 9.4,    1887: 9.5,    1888: 9.5,    1889: 9.3,
    1890: 9.2,    1891: 9.2,    1892: 9.2,    1893: 9.2,    1894: 8.8,
    1895: 8.6,    1896: 8.6,    1897: 8.5,    1898: 8.5,    1899: 8.5,
    1900: 8.6,    1901: 8.7,    1902: 8.8,    1903: 9.0,    1904: 9.1,
    1905: 9.0,    1906: 9.2,    1907: 9.6,    1908: 9.4,    1909: 9.3,
    1910: 9.7,    1911: 9.7,    1912: 9.9,    1913: 9.9,    1914: 10.1,
    1915: 10.1,   1916: 10.9,   1917: 12.8,   1918: 15.1,   1919: 17.3,
    1920: 20.0,   1921: 17.9,   1922: 16.8,   1923: 17.1,   1924: 17.1,
    1925: 17.5,   1926: 17.7,   1927: 17.4,   1928: 17.1,   1929: 17.1,
    1930: 16.7,   1931: 15.2,   1932: 13.7,   1933: 13.0,   1934: 13.4,
    1935: 13.7,   1936: 13.9,   1937: 14.4,   1938: 14.1,   1939: 13.9,
    1940: 14.0,   1941: 14.7,   1942: 16.3,   1943: 17.3,   1944: 17.6,
    1945: 18.0,   1946: 19.5,   1947: 22.3,   1948: 24.1,   1949: 23.8,
    1950: 24.1,   1951: 26.0,   1952: 26.5,   1953: 26.7,   1954: 26.9,
    1955: 26.8,   1956: 27.2,   1957: 28.1,   1958: 28.9,   1959: 29.1,
    1960: 29.6,   1961: 29.9,   1962: 30.2,   1963: 30.6,   1964: 31.0,
    1965: 31.5,   1966: 32.4,   1967: 33.4,   1968: 34.8,   1969: 36.7,
    1970: 38.8,   1971: 40.5,   1972: 41.8,   1973: 44.4,   1974: 49.3,
    1975: 53.8,   1976: 56.9,   1977: 60.6,   1978: 65.2,   1979: 72.6,
    1980: 82.4,   1981: 90.9,   1982: 96.5,   1983: 99.6,   1984: 103.9,
    1985: 107.6,  1986: 109.6,  1987: 113.6,  1988: 118.3,  1989: 124.0,
    1990: 130.7,  1991: 136.2,  1992: 140.3,  1993: 144.5,  1994: 148.2,
    1995: 152.4,  1996: 156.9,  1997: 160.5,  1998: 163.0,  1999: 166.6,
    2000: 172.2,  2001: 177.1,  2002: 179.9,  2003: 184.0,  2004: 188.9,
    2005: 195.3,  2006: 201.6,  2007: 207.342,2008: 215.303,2009: 214.537,
    2010: 218.056,2011: 224.939,2012: 229.594,2013: 232.957,2014: 236.736,
    2015: 237.017,2016: 240.007,2017: 245.120,2018: 251.107,2019: 255.657,
    2020: 258.811,2021: 270.970,2022: 292.655,2023: 304.702,2024: 314.150,
    2025: 322.000,2026: 329.100
}

LABOR_INDEX = {
    1980: 50.0, 1985: 70.0, 1990: 95.0, 1995: 115.0, 2000: 140.0,
    2005: 165.0, 2010: 190.0, 2015: 210.0, 2020: 240.0, 2025: 280.0,
    2026: 288.0
}

def get_index_value(year, index_dict):
    if year in index_dict:
        return index_dict[year]
    years = sorted(index_dict.keys())
    if year <= years[0]:
        return index_dict[years[0]]
    if year >= years[-1]:
        return index_dict[years[-1]]
    lower_year = max([y for y in years if y < year])
    upper_year = min([y for y in years if y > year])
    lower_val = index_dict[lower_year]
    upper_val = index_dict[upper_year]
    proportion = (year - lower_year) / (upper_year - lower_year)
    return lower_val + proportion * (upper_val - lower_val)

def format_century_label(c):
    try:
        val = int(float(c))
        # Determine the correct English ordinal suffix
        suffix = "th"
        j = val % 10
        k = val % 100
        if j == 1 and k != 11:
            suffix = "st"
        elif j == 2 and k != 12:
            suffix = "nd"
        elif j == 3 and k != 13:
            suffix = "rd"
        return f"{val}{suffix} C."
    except (ValueError, TypeError):
        return str(c)

# ==========================================
# 1. DATA LOADING & PROCESSING (STREAMLINED)
# ==========================================
def load_and_process_data():
    print("[SYSTEM] Loading and cleaning data...")
    
    csv_file = 'all_violin_sales_combined_namefixed.csv'
    if os.path.exists('auction_data_enhanced.csv'):
        csv_file = 'auction_data_enhanced.csv'
        print(f"[SYSTEM] Enhanced Excel CSV detected. Loading: {csv_file}")
        
    try:
        auctions = pd.read_csv(csv_file, encoding='utf-8-sig')
        with open('makers_meta.json', 'r', encoding='utf-8') as f:
            makers = pd.DataFrame(json.load(f))
    except Exception as e:
        print(f"Error loading files: {e}")
        sys.exit(1)

    # Prevent suffix collisions (_x, _y) if loading an already-enhanced CSV
    metadata_cols = ['maker_name', 'country', 'century', 'birth', 'death', 'Is_Dead', 'Start_Active', 'End_Active']
    auctions = auctions.drop(columns=[col for col in metadata_cols if col in auctions.columns], errors='ignore')

    # Currency selection (Prefer USD)
    target_currency = 'USD' if 'USD' in auctions.columns else 'EUR' if 'EUR' in auctions.columns else None
    if not target_currency:
        print("Error: Could not find USD or EUR columns in auction data.")
        sys.exit(1)
        
    print(f"[SYSTEM] Primary Currency locked to: {target_currency}")

    auctions['PRICE'] = auctions[target_currency].astype(str).str.replace(',', '', regex=False).str.replace(' ', '', regex=False)
    auctions['PRICE'] = pd.to_numeric(auctions['PRICE'], errors='coerce')
    auctions = auctions.dropna(subset=['PRICE'])
    auctions = auctions[auctions['PRICE'] > 0]
    
    # 1. Look for whichever date column exists (Sale Date, Date, or Sortable Date)
    possible_date_columns = ['Sale Date', 'Date', 'Sortable Date']
    date_col = next((col for col in possible_date_columns if col in auctions.columns), None)
    
    if not date_col:
        print("Error: Could not find a date column. Please name your column 'Sale Date' or 'Date'.")
        sys.exit(1)

    # 2. Try standard Python Date parsing first
    auctions['Sale Year'] = pd.to_datetime(auctions[date_col], errors='coerce').dt.year
    
    # 3. If standard parsing fails, scan the text for a 4-digit year
    if auctions['Sale Year'].isna().any():
        fallback_years = auctions[date_col].astype(str).str.extract(r'(18\d{2}|19\d{2}|20\d{2})')[0]
        auctions['Sale Year'] = auctions['Sale Year'].fillna(pd.to_numeric(fallback_years, errors='coerce'))

    # Clean up empty rows
    auctions = auctions.dropna(subset=['Sale Year'])
    auctions['Sale Year'] = auctions['Sale Year'].astype(int)

    # Lifespan Logic
    def process_lifespan(row):
        birth = pd.to_numeric(row.get('birth', 0), errors='coerce')
        death = pd.to_numeric(row.get('death', 0), errors='coerce')
        if pd.isna(birth) or birth == 0:
            return pd.Series({'Start_Active': 1500, 'End_Active': 2026, 'Is_Dead': True})
        start_active = birth + 25
        if not pd.isna(death) and death > 0:
            end_active = death
            is_dead = True
        else:
            end_active = birth + 85  
            is_dead = (birth + 85) < 2026
        return pd.Series({'Start_Active': start_active, 'End_Active': end_active, 'Is_Dead': is_dead})

    lifespan_df = makers.apply(process_lifespan, axis=1)
    
    if 'Start_Active' in makers.columns:
        makers = makers.drop(columns=['Start_Active', 'End_Active', 'Is_Dead'], errors='ignore')
        
    makers = pd.concat([makers, lifespan_df], axis=1)

    # Calculate Century for EVERYONE first (before filtering dead/alive)
    birth_years = pd.to_numeric(makers['birth'], errors='coerce')
    derived_century = birth_years.apply(lambda b: int((b + 35) // 100 + 1) if not pd.isna(b) and b > 0 else np.nan)
    
    if 'century' not in makers.columns:
        makers['century'] = np.nan
        
    makers['century'] = pd.to_numeric(makers['century'], errors='coerce')
    makers['century'] = makers['century'].fillna(derived_century)
    
    makers['century'] = makers['century'].apply(
        lambda c: str(int(c)) if not pd.isna(c) and c > 0 else "Unknown"
    )

    # --- THE LIVING & 21st  ---
    if INCLUDE_21ST_CENTURY:
        # DISABLE the Alive filter: Keep living makers so contemporary 21st C. makers can enter
        deceased_makers = makers.copy()
    else:
        # STRICT historical mode: Must be deceased AND must not be 21st century
        deceased_makers = makers[(makers['Is_Dead'] == True) & (makers['century'] != "21")].copy()
    # --------------------------------------------

    df_raw_merged = pd.merge(auctions, deceased_makers, on='maker_id', how='inner')
    df_raw_merged = df_raw_merged[df_raw_merged['Sale Year'] >= df_raw_merged['Start_Active']]
    sale_counts_per_maker = df_raw_merged['maker_id'].value_counts()

    # Calculate constant currency "Real Price" for OLS fitting
    dict_to_use = CPI_INDEX if ADJUSTMENT_INDEX == "CPI" else LABOR_INDEX
    def calculate_real_price(row):
        if ADJUSTMENT_INDEX == "NONE":
            return row['PRICE']
        idx_sale = get_index_value(row['Sale Year'], dict_to_use)
        idx_base = get_index_value(2026, dict_to_use)
        if idx_sale == 0:
            return row['PRICE']
        return row['PRICE'] * (idx_base / idx_sale)
        
    df_raw_merged['Real_Price'] = df_raw_merged.apply(calculate_real_price, axis=1)

    # Filter out makers who fail to meet strict N and holding span requirements
    maker_groups = df_raw_merged.groupby('maker_id')
    qualifying_maker_ids = []
    
    for m_id, group in maker_groups:
        n_sales = len(group)
        span = group['Sale Year'].max() - group['Sale Year'].min()
        if n_sales >= MIN_SALES_REQUIRED and span >= MIN_SPAN_REQUIRED:
            qualifying_maker_ids.append(m_id)

    # Fit OLS slope on ln(Real Price) vs Sale Year to find real growth
    maker_growth_records = []
    for m_id in qualifying_maker_ids:
        group = df_raw_merged[df_raw_merged['maker_id'] == m_id]
        x = group['Sale Year'].values
        
        # Real OLS Fit
        y_real = np.log(group['Real_Price'].values)
        slope_real, _ = np.polyfit(x, y_real, 1)
        real_growth_rate = (np.exp(slope_real) - 1) * 100
        
        # Nominal OLS Fit
        y_nom = np.log(group['PRICE'].values)
        slope_nom, _ = np.polyfit(x, y_nom, 1)
        nominal_growth_rate = (np.exp(slope_nom) - 1) * 100
        
        first_row = group.iloc[0]
        maker_growth_records.append({
            'maker_id': m_id,
            'maker_name': first_row['maker_name'],
            'country': first_row['country'],
            'century': first_row['century'],
            'Is_Dead': first_row['Is_Dead'],  # <--- ADD THIS LINE
            'First_Year': int(x.min()),
            'Last_Year': int(x.max()),
            'Years_Between': int(x.max() - x.min()),
            'Nominal_Growth_%': nominal_growth_rate,
            'Annual_Growth_%': real_growth_rate,
            'N_Sales': len(group)
        })

    active_growth = pd.DataFrame(maker_growth_records) if qualifying_maker_ids else pd.DataFrame(columns=[
        'maker_id', 'maker_name', 'country', 'century', 'First_Year', 'Last_Year', 'Years_Between', 'Nominal_Growth_%', 'Annual_Growth_%', 'N_Sales'
    ])

    # Methodological regional groupings
    if GROUP_REGIONS and not active_growth.empty:
        regional_mapping = {
            'Austria': 'Central Europe',
            'Czech Republic': 'Central Europe',
            'Germany': 'Central Europe',
            'Hungary': 'Central Europe',
            'Belgium': 'Benelux',
            'Netherlands': 'Benelux',
            'Great Britain': 'UK & Ireland',
            'Ireland': 'UK & Ireland',
            'UK': 'UK & Ireland',
            'Canada': 'North America',
            'USA': 'North America',
            'Portugal': 'Iberia',
            'Spain': 'Iberia'
        }
        active_growth['country'] = active_growth['country'].replace(regional_mapping)

    # =====================================================================
    # REST OF WORLD (LOW-N) GROUPING LOGIC
    # =====================================================================
    if GROUP_LOW_N_COUNTRIES and not active_growth.empty:
        # Count the active pool size for each country/regional group [1]
        counts = active_growth['country'].value_counts()
        
        # Identify any groups with fewer than 10 total makers [1]
        low_n_countries = counts[counts < 10].index
        
        # Merge those low-volume groups into "Rest of World" [1]
        if len(low_n_countries) > 0:
            active_growth['country'] = active_growth['country'].replace(
                {c: 'World (Rest of)' for c in low_n_countries}
            )
    # =====================================================================
    
    return active_growth, deceased_makers, sale_counts_per_maker, MIN_SALES_REQUIRED, makers, target_currency

# ==========================================
# 2. LEDGER & MARKDOWN EXPORTER
# ==========================================
def display_statistics_ledger(maker_growth, deceased_makers, sale_counts_per_maker, min_sales, currency):
    makers_with_auction_prices = deceased_makers[deceased_makers['maker_id'].isin(sale_counts_per_maker.index)]
    makers_without_auction_prices = deceased_makers[~deceased_makers['maker_id'].isin(sale_counts_per_maker.index)]
    qualifying_maker_ids = maker_growth['maker_id']
    makers_filtered_out_by_N = deceased_makers[
        deceased_makers['maker_id'].isin(sale_counts_per_maker.index) & 
        (~deceased_makers['maker_id'].isin(qualifying_maker_ids))
    ]

    print("\n" + "=" * 50)
    print(f"      MARKET DEMOGRAPHICS SUMMARY (N = {min_sales})")
    print("=" * 50)
    print(f"Index Active: {ADJUSTMENT_INDEX}")
    print(f"Regional Grouping: {'Enabled (Central Europe & Benelux)' if GROUP_REGIONS else 'Disabled (Separate)'}")
    print(f"Total Deceased Violin Makers in DB:    {len(deceased_makers)}")
    print(f"Makers with ANY Auction Activity:      {len(makers_with_auction_prices)}")
    print(f"Makers with ZERO Auction Activity:     {len(makers_without_auction_prices)}")
    print(f"Makers Cut Out by N & Span Rules:      {len(makers_filtered_out_by_N)}")
    print(f"Makers Included in Growth Curve:       {len(qualifying_maker_ids)}")
    print("=" * 50)

    print(f"\n--- FIRST 5 RESULTS (ACTIVE GROWTH POOL - REAL CONSTANT % OLS) ---")
    if not maker_growth.empty:
        print(maker_growth[['maker_name', 'First_Year', 'Last_Year', 'Years_Between', 'Nominal_Growth_%', 'Annual_Growth_%']].head().to_string())

    # Compile medians and counts
    century_grp = maker_growth.groupby('century')['Annual_Growth_%'].agg(['median', 'count']) if not maker_growth.empty else pd.DataFrame()
    country_grp = maker_growth.groupby('country')['Annual_Growth_%'].agg(['median', 'count']) if not maker_growth.empty else pd.DataFrame()
    combined_grp = maker_growth.groupby(['country', 'century'])['Annual_Growth_%'].agg(['median', 'count']).reset_index() if not maker_growth.empty else pd.DataFrame()

    # Print medians with strict n < 10 suppression guards
    print("\n--- ANALYSIS BY CENTURY (MEDIAN REAL GROWTH %) ---")
    for cent, row in century_grp.iterrows():
        med_val = f"{row['median']:.3f}%" if row['count'] >= 10 else "Insuff. Data (n < 10)"
        print(f"{format_century_label(cent):<15} | Median: {med_val:<22} | n: {int(row['count'])}")

    print("\n--- ANALYSIS BY COUNTRY (MEDIAN REAL GROWTH %) ---")
    for country, row in country_grp.iterrows():
        med_val = f"{row['median']:.3f}%" if row['count'] >= 10 else "Insuff. Data (n < 10)"
        print(f"{country:<15} | Median: {med_val:<22} | n: {int(row['count'])}")
    
    # Calculate Performance brackets
    lost_c = len(maker_growth[maker_growth['Annual_Growth_%'] < -1.0]) if not maker_growth.empty else 0
    held_c = len(maker_growth[(maker_growth['Annual_Growth_%'] >= -1.0) & (maker_growth['Annual_Growth_%'] <= 1.0)]) if not maker_growth.empty else 0
    gained_c = len(maker_growth[maker_growth['Annual_Growth_%'] > 1.0]) if not maker_growth.empty else 0
    
    active_total = len(maker_growth)
    db_total = len(deceased_makers)
    hist_total = max(PROJECTED_TOTAL_MAKERS, db_total)
    
    makers_with_auction = len(makers_with_auction_prices)
    makers_zero_auction = len(makers_without_auction_prices)
    makers_cut_by_N = len(makers_filtered_out_by_N)
    
    # Write to Markdown File
    md_filename = "violin_market_statistics.md"
    try:
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write("# Violin Market Valuation & Liquidity Report (OLS Model)\n\n")
            f.write(f"This report compiles complete statistics and performance metrics for deceased violin makers, adjusted for inflation using the **{ADJUSTMENT_INDEX}** index. Growth rates are modeled via OLS log-regression of real price on transaction year.\n\n")
            
            f.write("## 1. Market Demographics & Liquidity\n\n")
            f.write("| Metric | Count / Setting |\n")
            f.write("| :--- | :---: |\n")
            f.write(f"| **Locked Currency** | {currency} |\n")
            f.write(f"| **Active Price Adjustment Index** | {ADJUSTMENT_INDEX} |\n")
            f.write(f"| **Minimum Transaction Threshold (N)** | {min_sales} sales |\n")
            f.write(f"| **Minimum Span Required** | {MIN_SPAN_REQUIRED} years |\n")
            f.write(f"| **Total Deceased Violin Makers in DB** | {db_total} |\n")
            f.write(f"| **Makers with ANY Auction Activity** | {makers_with_auction} |\n")
            f.write(f"| **Makers with ZERO Auction Activity** | {makers_zero_auction} |\n")
            f.write(f"| **Makers Excluded by N & Span Rules** | {makers_cut_by_N} |\n")
            f.write(f"| **Makers Included in Stats (Active Pool)** | {active_total} |\n\n")
            
            f.write("## 2. Market Performance Universes\n\n")
            f.write("These metrics represent how the active traded makers perform, scaled against different structural assumptions of the global market size.\n\n")
            
            # Context A Table
            f.write(f"### Context A: Active Traded Pool (N={active_total})\n")
            f.write("Measuring performance strictly within the liquid auction market.\n\n")
            f.write("| Performance Bracket | Count | Percentage |\n")
            f.write("| :--- | :---: | :---: |\n")
            pct_lost = (lost_c/active_total*100) if active_total > 0 else 0
            pct_held = (held_c/active_total*100) if active_total > 0 else 0
            pct_gained = (gained_c/active_total*100) if active_total > 0 else 0
            f.write(f"| **Lost Real Value** (< -1.0% Real CAGR) | {lost_c} | {pct_lost:.2f}% |\n")
            f.write(f"| **Roughly Held Value** (-1.0% to 1.0% Real CAGR) | {held_c} | {pct_held:.2f}% |\n")
            f.write(f"| **Gained Real Value** (> 1.0% Real CAGR) | {gained_c} | {pct_gained:.2f}% |\n\n")
            
            # Context B Table
            f.write(f"### Context B: Database Total Pool (N={db_total})\n")
            f.write("Measuring performance relative to all deceased makers in your local metadata file.\n\n")
            f.write("| Performance Bracket | Count | Percentage |\n")
            f.write("| :--- | :---: | :---: |\n")
            f.write(f"| **Lost Real Value** | {lost_c} | {lost_c/db_total*100:.2f}% |\n")
            f.write(f"| **Roughly Held Value** | {held_c} | {held_c/db_total*100:.2f}% |\n")
            f.write(f"| **Gained Real Value** | {gained_c} | {gained_c/db_total*100:.2f}% |\n")
            f.write(f"| **Graveyard / Illiquid** (Untraded or filtered) | {db_total-active_total} | {(db_total-active_total)/db_total*100:.2f}% |\n\n")
            
            # Context C Table
            f.write(f"### Context C: Projected Historical Universe (N={hist_total})\n")
            f.write("Measuring performance against the estimated global history of individual violin makers (low-ball dictionary baseline).\n\n")
            f.write("| Performance Bracket | Count | Percentage |\n")
            f.write("| :--- | :---: | :---: |\n")
            f.write(f"| **Lost Real Value** | {lost_c} | {lost_c/hist_total*100:.2f}% |\n")
            f.write(f"| **Roughly Held Value** | {held_c} | {held_c/hist_total*100:.2f}% |\n")
            f.write(f"| **Gained Real Value** | {gained_c} | {gained_c/hist_total*100:.2f}% |\n")
            f.write(f"| **Graveyard / Illiquid** | {hist_total-active_total} | {(hist_total-active_total)/hist_total*100:.2f}% |\n\n")
            
            # Section 3
            f.write("## 3. Real Performance by Historical Century\n\n")
            f.write("| Century | Median Real CAGR (%) | Maker Count |\n")
            f.write("| :--- | :---: | :---: |\n")
            for cent, row in century_grp.iterrows():
                med_val = f"{row['median']:.3f}%" if row['count'] >= 10 else "Insuff. Data (n < 10)"
                f.write(f"| {format_century_label(cent)} | {med_val} | {int(row['count'])} |\n")
            f.write("\n")
            
            # Section 4
            f.write("## 4. Real Performance by Country / Regional Group\n\n")
            f.write("| Country / Region | Median Real CAGR (%) | Maker Count |\n")
            f.write("| :--- | :---: | :---: |\n")
            for country, row in country_grp.iterrows():
                med_val = f"{row['median']:.3f}%" if row['count'] >= 10 else "Insuff. Data (n < 10)"
                f.write(f"| {country} | {med_val} | {int(row['count'])} |\n")
            f.write("\n")
            
            # Section 5
            f.write("## 5. Combined Regional & Century Matrix\n\n")
            f.write("| Country / Region | Century | Median Real CAGR (%) | Maker Count |\n")
            f.write("| :--- | :--- : | :---: | :---: |\n")
            for _, row in combined_grp.iterrows():
                med_val = f"{row['median']:.3f}%" if row['count'] >= 10 else "Insuff. Data (n < 10)"
                f.write(f"| {row['country']} | {format_century_label(row['century'])} | {med_val} | {int(row['count'])} |\n")
                
        print(f"\n[SYSTEM] Successfully generated and updated Markdown stats report:")
        print(f"         {os.path.abspath(md_filename)}")
    except Exception as e:
        print(f"[SYSTEM] Notice: Could not export MD file: {e}")

    input("\nPress Enter to return to menu...")

# ==========================================
# 3. GRAPHS
# ==========================================
def plot_consolidated_histogram(maker_growth, deceased_makers, currency):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8))

    color_lost, color_held, color_gained = '#d95f02', '#7570b3', '#1b9e77'
    bins = np.arange(-5, 6.5, 0.5)
    counts, bin_edges, patches = ax.hist(maker_growth['Annual_Growth_%'], bins=bins, edgecolor='#252525', linewidth=1.2, alpha=0.9)

    for i in range(len(patches)):
        bin_center = (bin_edges[i] + bin_edges[i+1]) / 2
        if bin_center < -1.0:
            patches[i].set_facecolor(color_lost)
        elif bin_center <= 1.0:
            patches[i].set_facecolor(color_held)
        else:
            patches[i].set_facecolor(color_gained)

    lost_c = len(maker_growth[maker_growth['Annual_Growth_%'] < -1.0])
    held_c = len(maker_growth[(maker_growth['Annual_Growth_%'] >= -1.0) & (maker_growth['Annual_Growth_%'] <= 1.0)])
    gained_c = len(maker_growth[maker_growth['Annual_Growth_%'] > 1.0])
    
    active_total = len(maker_growth)
    db_total = len(deceased_makers)
    hist_total = max(PROJECTED_TOTAL_MAKERS, db_total)

    legend_text = (
        f"REAL DISTRIBUTION (Adjusted by: {ADJUSTMENT_INDEX}):\n\n"
        f"1. Active Traded Pool (N={active_total})\n"
        f"   Lost: {lost_c/active_total*100:.1f}% | Held: {held_c/active_total*100:.1f}% | Gained: {gained_c/active_total*100:.1f}%\n\n"
        f"2. Database Total Pool (N={db_total})\n"
        f"   Lost: {lost_c/db_total*100:.1f}% | Held: {held_c/db_total*100:.1f}% | Gained: {gained_c/db_total*100:.1f}% | Graveyard: {(db_total-active_total)/db_total*100:.1f}%\n\n"
        f"3. Projected Historical Universe (N={hist_total})\n"
        f"   Lost: {lost_c/hist_total*100:.1f}% | Held: {held_c/hist_total*100:.1f}% | Gained: {gained_c/hist_total*100:.1f}% | Graveyard: {(hist_total-active_total)/hist_total*100:.1f}%"
    )

    plt.text(0.02, 0.75, legend_text, transform=ax.transAxes, fontsize=10, 
             bbox=dict(facecolor='#1a1a1a', edgecolor='#4d4d4d', boxstyle='round,pad=1'))

    plt.title(f'Constant Currency ({currency}) Price Growth Distribution', fontsize=14, pad=20, fontweight='bold')
    plt.xlabel('Real Annual Growth Rate (%)', fontsize=12, labelpad=10)
    plt.ylabel('Number of Makers (Active)', fontsize=12, labelpad=10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    plt.xlim(-5, 6)
    plt.tight_layout()
    plt.show()

def plot_distribution_by_category(maker_growth, category):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 7))

    df_clean = maker_growth.dropna(subset=[category, 'Annual_Growth_%', 'Is_Dead'])
    counts = df_clean[category].value_counts()
    
    # Strictly raise violin plot category filters to counts >= 10
    valid_groups = counts[counts >= 10].index
    df_clean = df_clean[df_clean[category].isin(valid_groups)]

    if len(df_clean) == 0:
        print(f"Not enough data to plot by {category} (Groups need at least 10 makers).")
        return

    groups = sorted(df_clean[category].unique())
    data_to_plot = [df_clean[df_clean[category] == g]['Annual_Growth_%'].values for g in groups]

    # Plot medians strictly to combat fat-tail CAGR outliers
    parts = ax.violinplot(data_to_plot, showmeans=False, showmedians=True)

    for pc in parts['bodies']:
        pc.set_facecolor('#7570b3')
        pc.set_edgecolor('white')
        pc.set_alpha(0.5)  # Slightly more transparent to see the dots
    
    parts['cmedians'].set_color('#1b9e77')
    parts['cmins'].set_color('#4d4d4d')
    parts['cmaxes'].set_color('#4d4d4d')
    parts['cbars'].set_color('#4d4d4d')

    ax.axhline(0, color='#d95f02', linestyle='--', linewidth=1, alpha=0.8)

    # --- ADD THE SCATTER OVERLAY FOR LIVING VS DEAD ---
    for i, g in enumerate(groups):
        df_g = df_clean[df_clean[category] == g]
        dead_y = df_g[df_g['Is_Dead'] == True]['Annual_Growth_%'].values
        liv_y = df_g[df_g['Is_Dead'] == False]['Annual_Growth_%'].values
        
        x_pos = i + 1
        # Add random horizontal jitter so dots don't stack perfectly on top of each other
        jitter_dead = np.random.normal(0, 0.04, size=len(dead_y))
        jitter_liv = np.random.normal(0, 0.04, size=len(liv_y))
        
        ax.scatter(x_pos + jitter_dead, dead_y, color='white', alpha=0.3, s=15, zorder=3)
        if len(liv_y) > 0:
            ax.scatter(x_pos + jitter_liv, liv_y, color='#e7298a', alpha=0.9, s=35, marker='o', edgecolors='white', linewidth=0.5, zorder=4)
    # --------------------------------------------------

    ax.set_xticks(np.arange(1, len(groups) + 1))
    ax.set_xticklabels(groups, fontsize=12)
    
    plt.title(f'Real Annual Growth Distribution by {category.capitalize()} (Groups >= 10 makers)', fontsize=15, fontweight='bold', pad=20)
    plt.ylabel('Real Annual Growth Rate (%)', fontsize=12, labelpad=10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    
    plt.figtext(0.15, 0.85, '— Median Average', color='#1b9e77', fontweight='bold')
    plt.figtext(0.15, 0.81, '--- Constant Money Break Even (0%)', color='#d95f02', fontweight='bold')
    if not df_clean[df_clean['Is_Dead'] == False].empty:
        plt.figtext(0.15, 0.77, '● Living Maker', color='#e7298a', fontweight='bold')

    plt.tight_layout()
    plt.show()

# ==========================================
# 4. UNIFIED GRID OF ALL COUNTRIES BY CENTURY
# ==========================================
def plot_all_countries_by_century(maker_growth):
    plt.style.use('dark_background')
    
    countries = sorted(maker_growth['country'].dropna().unique())
    
    valid_countries = []
    for country in countries:
        df_c = maker_growth[maker_growth['country'] == country].dropna(subset=['century', 'Annual_Growth_%', 'Is_Dead'])
        counts = df_c['century'].value_counts()
        valid_centuries = sorted(counts[counts >= 10].index)
        if len(valid_centuries) > 0:
            valid_countries.append((country, valid_centuries))
            
    num_countries = len(valid_countries)
    if num_countries == 0:
        print("\nNo countries have enough historic data (at least 10 makers in at least one century) to plot.")
        input("\nPress Enter to return to menu...")
        return
        
    max_cents = max([len(cents) for _, cents in valid_countries])
        
    ncols = 3
    nrows = int(np.ceil(num_countries / ncols))
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4.5 * nrows), sharey=True)
    
    if num_countries == 1: axes = np.array([axes])
    else: axes = axes.flatten()
        
    for idx, (country, valid_centuries) in enumerate(valid_countries):
        ax = axes[idx]
        df_c = maker_growth[maker_growth['country'] == country]
        df_plot = df_c[df_c['century'].isin(valid_centuries)]
        
        data_to_plot = [df_plot[df_plot['century'] == c]['Annual_Growth_%'].values for c in valid_centuries]
        normalized_width = 0.75 * (len(valid_centuries) / max_cents)
        
        parts = ax.violinplot(data_to_plot, showmeans=False, showmedians=True, widths=normalized_width)
        ax.set_xlim(0.5, len(valid_centuries) + 0.5)
        
        for pc in parts['bodies']:
            pc.set_facecolor('#7570b3')
            pc.set_edgecolor('white')
            pc.set_alpha(0.5)
            
        parts['cmedians'].set_color('#1b9e77')
        parts['cmins'].set_color('#4d4d4d')
        parts['cmaxes'].set_color('#4d4d4d')
        parts['cbars'].set_color('#4d4d4d')
        
        ax.axhline(0, color='#d95f02', linestyle='--', linewidth=1, alpha=0.7)
        
        # --- ADD THE SCATTER OVERLAY ---
        for i, cent in enumerate(valid_centuries):
            df_g = df_plot[df_plot['century'] == cent]
            dead_y = df_g[df_g['Is_Dead'] == True]['Annual_Growth_%'].values
            liv_y = df_g[df_g['Is_Dead'] == False]['Annual_Growth_%'].values
            
            x_pos = i + 1
            jitter_dead = np.random.normal(0, 0.03 * (len(valid_centuries)/max_cents), size=len(dead_y))
            jitter_liv = np.random.normal(0, 0.03 * (len(valid_centuries)/max_cents), size=len(liv_y))
            
            ax.scatter(x_pos + jitter_dead, dead_y, color='white', alpha=0.3, s=10, zorder=3)
            if len(liv_y) > 0:
                ax.scatter(x_pos + jitter_liv, liv_y, color='#e7298a', alpha=0.9, s=25, marker='o', edgecolors='white', linewidth=0.5, zorder=4)
        # -------------------------------

        ax.set_xticks(np.arange(1, len(valid_centuries) + 1))
        ax.set_xticklabels([format_century_label(c) for c in valid_centuries], fontsize=10)
        
        ax.set_title(f"{country} (N={len(df_plot)})", fontsize=12, fontweight='bold', pad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', linestyle='--', alpha=0.15)
        
    for idx in range(num_countries, len(axes)):
        axes[idx].axis('off')
        
    fig.text(0.01, 0.5, 'Real Annual Growth Rate (%)', va='center', rotation='vertical', fontsize=12, fontweight='bold')
    fig.suptitle(f"Real Annual Growth by Country & Century (Index: {ADJUSTMENT_INDEX})", fontsize=16, fontweight='bold', y=0.98)
    
    has_living = not maker_growth[maker_growth['Is_Dead'] == False].empty
    if has_living:
        fig.text(0.02, 0.96, '● Living Maker', color='#e7298a', fontweight='bold', fontsize=10)
    
    plt.tight_layout(rect=[0.02, 0.02, 1, 0.95])
    plt.show()

# ==========================================
# MAIN MENU
# ==========================================
def main():
    maker_growth, deceased_makers, sale_counts_per_maker, min_sales, makers, currency = load_and_process_data()
    
    while True:
        print("\n" + "=" * 50)
        print("      CONSTANT CURRENCY MARKET ANALYSIS MENU")
        print("=" * 50)
        print("--- ANALYSIS ---")
        print("1. Display Market Statistics Ledger (Text Form + MD Export)")
        print("2. Display Consolidated Histogram (Real Constant %)")
        print("3. Display Growth Distribution by Country (Violin Plot)")
        print("4. Display Growth Distribution by Century (Violin Plot)")
        print("5. Display Century Distributions for All Countries (Violin Plot Grid)")
        print("6. Exit")
        print("=" * 50)
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            display_statistics_ledger(maker_growth, deceased_makers, sale_counts_per_maker, min_sales, currency)
        elif choice == '2':
            plot_consolidated_histogram(maker_growth, deceased_makers, currency)
        elif choice == '3':
            plot_distribution_by_category(maker_growth, 'country')
        elif choice == '4':
            plot_distribution_by_category(maker_growth, 'century')
        elif choice == '5':
            plot_all_countries_by_century(maker_growth)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()