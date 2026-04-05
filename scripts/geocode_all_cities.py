import json
import re

print("Loading raw bulk cities dataset...")
try:
    with open("cities_raw.json", "r", encoding="utf-8") as f:
        cities_db = json.load(f)
except FileNotFoundError:
    print("Error: cities_raw.json not found.")
    exit(1)

# Build quick lookup
print("Building fast Hash lookup for global cities...")
city_map = {}
for c in cities_db:
    name = str(c.get("name", "")).strip().lower()
    # Normalize unicode to basic ascii if needed, but lower() is fine for exact match
    if name not in city_map:
        city_map[name] = {"lat": float(c["lat"]), "lng": float(c["lng"])}

print(f"Indexed {len(city_map)} unique world locations.")

print("Loading Forbes 2025 Billionaires list...")
with open("src/data/billionaires.json", "r", encoding="utf-8") as f:
    f_data = json.load(f)

persons = f_data.get("personList", {}).get("personsLists", [])

# Hardcoded patch for major missing cities due to naming discrepancies
MANUAL_OVERRIDES = {
    "new york": {"lat": 40.7128, "lng": -74.0060},
    "la coruna": {"lat": 43.3623, "lng": -8.4115},
    "zurich": {"lat": 47.3769, "lng": 8.5417},
    "frankfurt": {"lat": 50.1109, "lng": 8.6821},
    "bad homburg": {"lat": 50.2269, "lng": 8.6186},
    "monte carlo": {"lat": 43.7401, "lng": 7.4266},
    "haverford": {"lat": 40.0151, "lng": -75.3121},
    "kuenzelsau": {"lat": 49.2789, "lng": 9.6896},
    "ras al khaimah": {"lat": 25.7895, "lng": 55.9432},
    "newport coast": {"lat": 33.6062, "lng": -117.8251},
    "mulheim an der ruhr": {"lat": 51.4278, "lng": 6.8828},
    "muelheim": {"lat": 51.4278, "lng": 6.8828},
    "gladwyne": {"lat": 40.0354, "lng": -75.2818},
    "medina": {"lat": 47.61, "lng": -122.23},
    "seattle": {"lat": 47.60, "lng": -122.33},
    "palo alto": {"lat": 37.44, "lng": -122.14},
    "los altos": {"lat": 37.38, "lng": -122.11},
    "hunts point": {"lat": 47.63, "lng": -122.23}
}

global_cities_cache = {}
matched = 0
unmatched = []

print(f"Processing {len(persons)} billionaire home cities...")
for p in persons:
    c_name = str(p.get("city", "")).strip().lower()
    if not c_name:
        continue
    
    if c_name not in global_cities_cache:
        # Check formal DB or overrides
        if c_name in MANUAL_OVERRIDES:
            global_cities_cache[c_name] = MANUAL_OVERRIDES[c_name]
            matched += 1
        elif c_name in city_map:
            global_cities_cache[c_name] = city_map[c_name]
            matched += 1
        else:
            # Maybe check stripped versions?
            clean_name = re.sub(r'[^a-z ]', '', c_name)
            if clean_name in city_map:
                global_cities_cache[c_name] = city_map[clean_name]
                matched += 1
            else:
                unmatched.append(c_name)

print(f"Successfully matched {matched} unique cities.")
print(f"Failed to cleanly match {len(set(unmatched))} obscure cities.")

with open("src/data/global_cities.json", "w", encoding="utf-8") as f:
    json.dump(global_cities_cache, f, indent=2)
    
print("Successfully generated src/data/global_cities.json!")
