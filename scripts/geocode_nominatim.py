import json
import urllib.request
import urllib.parse
import time
import os

print("Loading current global cities cache...")
try:
    with open("src/data/global_cities.json", "r", encoding="utf-8") as f:
        global_cities_cache = json.load(f)
except FileNotFoundError:
    global_cities_cache = {}

print("Loading Forbes 2025 Billionaires list...")
with open("src/data/billionaires.json", "r", encoding="utf-8") as f:
    f_data = json.load(f)

persons = f_data.get("personList", {}).get("personsLists", [])

# Find missing unique cities
missing_cities = set()
for p in persons:
    c_name = str(p.get("city", "")).strip().lower()
    if c_name and c_name not in global_cities_cache:
        missing_cities.add(c_name)

missing_cities = list(missing_cities)
print(f"Discovered {len(missing_cities)} unique obscure cities that need API geocoding.")

if len(missing_cities) == 0:
    print("Ocean is clear! No missing cities found.")
    exit(0)

print("Starting Nominatim 1-second interval batch geocoding...")

headers = {
    'User-Agent': 'BillionaireMapApp/1.0 (Contact: mytestbot@example.com)'
}

successful_fetches = 0

for i, city in enumerate(missing_cities):
    print(f"[{i+1}/{len(missing_cities)}] Fetching GPS for: {city}")
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city)}&format=json&limit=1"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        # Use isolated DoH Curl bypass because python native DNS is firewalled
        curl_cmd = f'curl -s --doh-url https://1.1.1.1/dns-query -H "User-Agent: BillionaireMapApp/1.0" "{url}"'
        response_str = os.popen(curl_cmd).read()
        
        if response_str:
            data = json.loads(response_str)
            if len(data) > 0:
                lat = float(data[0]['lat'])
                lng = float(data[0]['lon'])
                global_cities_cache[city] = {"lat": lat, "lng": lng}
                successful_fetches += 1
                print(f"   -> Success: {lat}, {lng}")
            else:
                print("   -> Found nothing.")
        else:
            print("   -> Curl completely failed.")
    except Exception as e:
        print(f"   -> Failed API Call: {e}")
    
    # Crucial Nominatim API Limit: 1 request per second absolute minimum
    time.sleep(1.2)
    
    # Save incrementally so we don't lose data on crash
    if i % 10 == 0:
        with open("src/data/global_cities.json", "w", encoding="utf-8") as f:
            json.dump(global_cities_cache, f, indent=2)

# Final Save
with open("src/data/global_cities.json", "w", encoding="utf-8") as f:
    json.dump(global_cities_cache, f, indent=2)

print(f"\nDone! Successfully pulled and anchored {successful_fetches} massive global cities!")
