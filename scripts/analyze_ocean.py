import json
import re

print("Loading cached global cities...")
with open("src/data/global_cities.json", "r", encoding="utf-8") as f:
    global_cities = json.load(f)

print("Loading Forbes 2025 Billionaires list...")
with open("src/data/billionaires.json", "r", encoding="utf-8") as f:
    f_data = json.load(f)

persons = f_data.get("personList", {}).get("personsLists", [])

in_ocean = []
for p in persons:
    c_name = str(p.get("city", "")).strip().lower()
    country = str(p.get("country", "")).strip().lower()
    
    # If they have a city but it's not in our map
    if c_name and c_name not in global_cities:
        in_ocean.append({
            "name": p.get("personName", ""),
            "city": p.get("city", ""),
            "country": p.get("country", ""),
            "worth": p.get("finalWorth", 0)
        })
    elif not c_name and country:
        # If no city at all, they fall back to countryCoords or hash
        pass 

# Sort by net worth descending to prioritize the richest people in the ocean
in_ocean.sort(key=lambda x: x["worth"], reverse=True)

print(f"Total billionaires currently in the ocean: {len(in_ocean)}")
print("Top 20 most prominent individuals in the ocean:")
for p in in_ocean[:20]:
    print(f"- {p['name']} | City: '{p['city']}' | Country: '{p['country']}' | ${p['worth']/1000:.1f}B")

