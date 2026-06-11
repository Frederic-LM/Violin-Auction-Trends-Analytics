# record_sales.py
# Copyright (C) 2026 Frédéric Levi Mazloum
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import csv
import json
import datetime
import sys

METADATA_FILE = "makers_meta.json"

# Headers match the final structure expected by analyze.py,
# but the USD, EUR, and GBP columns are left blank for manual Excel calculation.
CSV_HEADERS = [
    "maker_id", 
    "maker_name", 
    "Sale Date Standard", 
    "USD", 
    "EUR",
    "GBP",
    "Type", 
    "Auction House", 
    "Hammer Price",
    "Currency",
    "Comment"
]

def safe_int(val, default=None):
    if val is None:
        return default
    try:
        return int(float(str(val).replace(",", "").strip()))
    except (ValueError, TypeError):
        return default

def load_makers():
    """Loads and normalizes makers metadata from JSON to allow search functionality."""
    if not os.path.exists(METADATA_FILE):
        print(f"[WARNING] '{METADATA_FILE}' not found in current directory.")
        print("Maker lookup will be disabled. You will need to enter IDs manually.")
        return []
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            
        if isinstance(loaded, dict):
            normalized_list = []
            for key, val in loaded.items():
                if isinstance(val, dict):
                    if "maker_id" not in val:
                        val["maker_id"] = safe_int(key, key)
                    normalized_list.append(val)
            return normalized_list
        
        if isinstance(loaded, list):
            return loaded
    except Exception as e:
        print(f"[ERROR] Failed to load metadata: {e}")
    return []

def get_unique_filename(date_str):
    """Generates a non-conflicting filename ending with _violin_sale_RAW.csv"""
    base_name = f"{date_str}_violin_sale_RAW"
    ext = ".csv"
    filename = f"{base_name}{ext}"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}{ext}"
        counter += 1
    return filename

def append_to_csv(filepath, row_data):
    """Safely appends a single row to the CSV. Writes headers if creating a new file."""
    file_exists = os.path.exists(filepath)
    try:
        with open(filepath, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row_data)
        return True
    except Exception as e:
        print(f"[ERROR] Failed writing to file: {e}")
        return False

def select_maker(makers):
    """Handles lookups by ID or partial name searches."""
    while True:
        print("\n" + "-" * 40)
        user_input = input("Enter Maker ID, name search term, or type 'exit' to quit: ").strip()
        
        if user_input.lower() == "exit":
            return "exit", None

        if not user_input:
            print("Input cannot be empty.")
            continue

        # Scenario A: User entered a numeric ID
        m_id = safe_int(user_input)
        if m_id is not None:
            match = next((m for m in makers if safe_int(m.get("maker_id")) == m_id), None)
            if match:
                print(f"-> Selected: {match.get('maker_name')} (ID: {m_id})")
                confirm = input("Confirm selection? (y/n): ").strip().lower()
                if confirm == 'y' or confirm == '':
                    return m_id, match.get("maker_name")
            else:
                print(f"[NOTICE] Maker ID {m_id} is not present in '{METADATA_FILE}'.")
                choice = input("Use as new/unregistered ID? (y/n): ").strip().lower()
                if choice == 'y':
                    custom_name = input("Enter Maker Name: ").strip()
                    return m_id, custom_name if custom_name else "Unknown"
            continue

        # Scenario B: Search query (letters)
        search_term = user_input.lower()
        matches = [m for m in makers if search_term in str(m.get("maker_name", "")).lower()]

        print("\nSearch Results:")
        for idx, m in enumerate(matches, 1):
            print(f" {idx}) {m.get('maker_name')} (ID: {m.get('maker_id')}, Country: {m.get('country', 'Unknown')})")

        print(f" N) Add as a new/unregistered maker")
        print(f" C) Cancel and search again")

        selection = input("\nSelect an option (number, N, or C): ").strip().lower()
        
        if selection == 'c':
            continue
        elif selection == 'n':
            custom_name = input("Enter Maker Name: ").strip()
            custom_id_in = input("Enter unique Maker ID (numeric): ").strip()
            custom_id = safe_int(custom_id_in)
            if custom_id is None:
                print("[ERROR] ID must be numeric. Reverting to search.")
                continue
            return custom_id, custom_name if custom_name else "Unknown"
        else:
            sel_idx = safe_int(selection)
            if sel_idx is not None and 1 <= sel_idx <= len(matches):
                chosen = matches[sel_idx - 1]
                return safe_int(chosen.get("maker_id")), chosen.get("maker_name")
            else:
                print("Invalid selection.")

def main():
    print("=" * 55)
    print("        VIOLIN SALES DATA COLLECTION COMPANION")
    print("=" * 55)

    makers = load_makers()

    # 1. Establish session date
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    session_date = input(f"Enter transaction session date (YYYY-MM-DD) [{today_str}]: ").strip()
    if not session_date:
        session_date = today_str

    # Validate date structure basically
    try:
        datetime.datetime.strptime(session_date, "%Y-%m-%d")
    except ValueError:
        print("[WARNING] Date format does not strictly match YYYY-MM-DD. Using literal input.")

    # 2. Select Auction House
    auction_houses = [
        "Tarisio", 
        "Brompton's", 
        "Skinner", 
        "Sotheby's", 
        "Christie's", 
        "Vichy Enchères"
    ]
    print("\nSelect Auction House for this session:")
    for idx, house in enumerate(auction_houses, 1):
        print(f" {idx}) {house}")
    print(" 7) Other (Type custom name)")
    
    house_choice = input("Choice: ").strip()
    if house_choice == '7':
        auction_house = input("Enter Custom Auction House Name: ").strip()
    else:
        choice_idx = safe_int(house_choice)
        if choice_idx is not None and 1 <= choice_idx <= len(auction_houses):
            auction_house = auction_houses[choice_idx - 1]
        else:
            auction_house = input("Invalid choice. Enter custom Auction House Name: ").strip()
            if not auction_house:
                auction_house = "Unknown House"

    # 3. Select Session Currency
    print("\nSelect currency unit for this session's Hammer Prices:")
    print(" 1) USD ($)")
    print(" 2) EUR (€)")
    print(" 3) GBP (£)")
    currency_choice = input("Choice [1]: ").strip()
    if currency_choice == "2":
        session_currency = "EUR"
        currency_symbol = "€"
    elif currency_choice == "3":
        session_currency = "GBP"
        currency_symbol = "£"
    else:
        session_currency = "USD"
        currency_symbol = "$"

    # 4. Create unique RAW file
    filename = get_unique_filename(session_date)
    print(f"\n[SYSTEM] Ready to write raw records to: {os.path.abspath(filename)}")
    print(f"         Prices will be stored in 'Hammer Price' with Currency code: {session_currency}")
    print("         USD, EUR, and GBP conversion columns will be written as blank.")
    print("All progress is saved dynamically. Type 'exit' to conclude the session.")

    last_used_type = "Violin"
    type_options = {
        "1": "Violin",
        "2": "Viola",
        "3": "Cello",
        "4": "Violin Bow",
        "5": "Viola Bow",
        "6": "Cello Bow"
    }

    # 5. Entry Loop
    while True:
        # Step A: Maker selection
        maker_id, maker_name = select_maker(makers)
        if maker_id == "exit":
            print(f"\n[FINISHED] Session terminated.")
            print(f"           Data securely saved to raw file: {filename}")
            print("\nNext Steps:")
            print(f" 1. Open '{filename}' in Excel.")
            print(" 2. Add buyer's premiums and convert values to USD manually.")
            print(" 3. Save the resulting processed file as 'all_violin_sales.csv' to run analytics.")
            break

        # Step B: Instrument Type Selection
        print("\nSelect Instrument Type:")
        print(" 1) Violin       2) Viola       3) Cello")
        print(" 4) Violin Bow   5) Viola Bow   6) Cello Bow")
        type_input = input(f"Enter option number or custom type [Last used: {last_used_type}]: ").strip()
        
        if not type_input:
            chosen_type = last_used_type
        elif type_input in type_options:
            chosen_type = type_options[type_input]
        else:
            chosen_type = type_input # Allows custom user strings

        last_used_type = chosen_type

        # Step C: Hammer Price
        while True:
            price_input = input(f"\nEnter Hammer Price ({currency_symbol} {session_currency}): ").strip()
            price_val = safe_int(price_input)
            if price_val is not None and price_val >= 0:
                break
            print("[ERROR] Invalid price. Enter a non-negative numerical integer.")

        # Step D: Comments / Notes
        comment = input("Enter optional comments/notes: ").strip()

        # Step E: Construct and Save Row (preserving blank USD/EUR/GBP placeholders)
        row_dict = {
            "maker_id": maker_id,
            "maker_name": maker_name,
            "Sale Date Standard": session_date,
            "USD": "", # Left blank for manual Excel calculation
            "EUR": "", # Left blank for manual Excel calculation
            "GBP": "", # Left blank for manual Excel calculation
            "Type": chosen_type,
            "Auction House": auction_house,
            "Hammer Price": price_val,
            "Currency": session_currency,
            "Comment": comment if comment else "N/A"
        }

        success = append_to_csv(filename, row_dict)
        if success:
            print(f"\n[SAVED] {maker_name} entry written to {filename}.")
        else:
            print("\n[CRITICAL ERROR] Failed to record transaction.")

if __name__ == "__main__":
    main()