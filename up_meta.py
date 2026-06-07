# update_meta.py
import json
import os

METADATA_FILE = "makers_meta.json"

def safe_int(val, default=None):
    """Safely converts any input (string, float, empty) to an integer without crashing."""
    if val is None:
        return default
    try:
        # Strip commas, whitespace, and convert float strings like '12.0' safely
        cleaned = str(val).replace(",", "").strip()
        return int(float(cleaned))
    except (ValueError, TypeError):
        return default

def load_makers():
    """Loads and normalizes makers metadata from JSON."""
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                
            # If the JSON is structured as a dictionary, convert it to a standard list
            if isinstance(loaded, dict):
                normalized_list = []
                for key, val in loaded.items():
                    if isinstance(val, dict):
                        # Ensure maker_id is preserved inside the dictionary
                        if "maker_id" not in val:
                            val["maker_id"] = safe_int(key, key)
                        normalized_list.append(val)
                return normalized_list
            
            if isinstance(loaded, list):
                return loaded
                
        except Exception as e:
            print(f"[ERROR] Reading JSON failed: {e}")
            return []
    return []

def save_makers(makers):
    """Sorts and saves metadata to JSON safely."""
    try:
        # Sort database by ID using safe integer mapping
        makers = sorted(makers, key=lambda x: safe_int(x.get("maker_id", 0), 0))
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(makers, f, indent=4, ensure_ascii=False)
        print(f"[SUCCESS] Database updated and saved to {METADATA_FILE}")
    except Exception as e:
        print(f"[ERROR] Writing JSON failed: {e}")

def calculate_century(birth, death):
    """
    Applies the generalized century classification rule across all eras:
    If born in the second half of any century (XX50), they belong to century (XX+2)
    UNLESS they passed away before the turn of that century (XX+1 * 100).
    """
    b_val = safe_int(birth)
    d_val = safe_int(death)
    
    if not b_val:
        return "Unknown"
        
    xx = b_val // 100
    mid_century = xx * 100 + 50
    turn_of_century = (xx + 1) * 100
    
    if b_val > mid_century:
        if d_val and d_val < turn_of_century:
            target_century = xx + 1  # Standard birth century
        else:
            target_century = xx + 2  # Subsequent century
    else:
        target_century = xx + 1      # Standard birth century
        
    return str(target_century)

def main():
    print("=" * 55)
    print("      MAKERS METADATA EDITOR & CONTRIBUTION TOOL")
    print("=" * 55)

    makers = load_makers()
    print(f"Loaded {len(makers)} makers from {METADATA_FILE}\n")

    try:
        m_id_input = input("Enter Maker ID (Tarisio numerical ID): ").strip()
        m_id = safe_int(m_id_input)
        
        if m_id is None:
            print("[ERROR] Maker ID must be a numeric integer.")
            return

        # Safely search for existing entries without strict casting crashes
        existing_index = None
        for i, m in enumerate(makers):
            if isinstance(m, dict) and safe_int(m.get("maker_id")) == m_id:
                existing_index = i
                break

        existing_record = makers[existing_index] if existing_index is not None else None

        if existing_record:
            print(f"\n[INFO] Found existing record for ID {m_id}: {existing_record.get('maker_name', 'Unknown')}")
            action = input("Do you want to edit this record? (y/n): ").strip().lower()
            if action != 'y':
                print("Aborted.")
                return

        # Prompt for fields, fallback to old values if editing
        old_name = existing_record.get('maker_name', '') if existing_record else ''
        name = input(f"Maker Name [{old_name}]: ").strip()
        if not name and existing_record: 
            name = old_name

        old_birth = existing_record.get('birth', '') if existing_record else ''
        birth_in = input(f"Birth Year [{old_birth}]: ").strip()
        birth = safe_int(birth_in) if birth_in else (safe_int(old_birth) if existing_record else None)

        old_death = existing_record.get('death', '') if existing_record else ''
        death_in = input(f"Death Year (leave blank if living) [{old_death}]: ").strip()
        death = safe_int(death_in) if death_in else (safe_int(old_death) if existing_record else None)

        old_country = existing_record.get('country', '') if existing_record else ''
        country = input(f"Country of Origin [{old_country}]: ").strip()
        if not country and existing_record: 
            country = old_country

        old_bio = existing_record.get('bio', '') if existing_record else ''
        bio = input(f"Brief Bio (optional) [{old_bio}]: ").strip()
        if not bio and existing_record: 
            bio = old_bio

        # Compute century using the generalized logic
        century = calculate_century(birth, death)

        # Build clean JSON record
        new_record = {
            "maker_id": m_id,
            "maker_name": name if name else "Unknown",
            "birth": birth,
            "death": death,
            "country": country if country else "Unknown",
            "century": century,
            "bio": bio
        }

        # Update or Append safely
        if existing_index is not None:
            makers[existing_index] = new_record
            print(f"\nUpdating entry for ID {m_id}...")
        else:
            makers.append(new_record)
            print(f"\nAdding new entry for ID {m_id}...")

        save_makers(makers)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
