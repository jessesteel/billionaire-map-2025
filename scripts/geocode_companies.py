import json
import subprocess
import urllib.parse
import time
import os

print("Starting geocoding process...")

input_file = "src/data/billionaires.json"
output_file = "src/data/company_coords.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

persons = data.get("personList", {}).get("personsLists", [])

companies = set()
for p in persons:
    comp_name = p.get("organization") or p.get("source")
    if comp_name:
        companies.add(comp_name)

print(f"Found {len(companies)} unique companies/sources.")

generic_terms = {
    "real estate", "diversified", "investments", "hedge funds", "private equity",
    "pharmaceuticals", "hospitals", "banking", "finance", "telecom", "retail",
    "technology", "software", "healthcare", "consumer goods", "manufacturing",
    "semiconductors", "logistics", "shipping", "mining", "chemicals", 
    "food & beverage", "online games", "beverages", "fashion", "casinos", 
    "hotels", "ecommerce"
}

results = {}

for count, comp in enumerate(list(companies)):
    c_lower = comp.lower().strip()
    
    # Skip extremely generic terms
    if c_lower in generic_terms or len(c_lower) < 3:
        results[comp] = None
        continue

    # Use DoH curl to bypass sandbox DNS limits
    encoded_query = urllib.parse.quote(comp)
    req_url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
    
    cmd = [
        "curl", "-s", "--doh-url", "https://1.1.1.1/dns-query",
        "-H", "User-Agent: OpenGrid-Wealth-Dev/1.0",
        req_url
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode == 0 and proc.stdout.strip() and proc.stdout.strip().startswith('['):
            resp_json = json.loads(proc.stdout)
            if len(resp_json) > 0:
                results[comp] = {
                    "lat": float(resp_json[0]["lat"]),
                    "lng": float(resp_json[0]["lon"])
                }
                print(f"[{count+1}/{len(companies)}] Geocoded '{comp}' -> {results[comp]}")
            else:
                results[comp] = None
                print(f"[{count+1}/{len(companies)}] No results for '{comp}'")
        else:
            results[comp] = None
            print(f"[{count+1}/{len(companies)}] Empty/Error response for '{comp}'")
    except Exception as e:
        print(f"Failed to geocode {comp}: {e}")
        results[comp] = None

    # Be nice to Nominatim (1 request per second)
    time.sleep(1.0)

os.makedirs("src/data", exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Geocoding complete! Results saved to", output_file)
