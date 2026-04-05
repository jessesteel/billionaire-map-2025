import json
import subprocess
import urllib.parse
import os

print("Fetching Walmart locations from Overpass API...")

query = """
[out:json];
(
  node["name"~"Walmart",i]["shop"~"supermarket|department_store|wholesale|doityourself|convenience|yes"];
  way["name"~"Walmart",i]["shop"~"supermarket|department_store|wholesale|doityourself|convenience|yes"];
);
out center;
"""

encoded_query = urllib.parse.quote(query.strip())
req_url = f"https://overpass-api.de/api/interpreter?data={encoded_query}"

cmd = [
    "curl", "-s", "--doh-url", "https://1.1.1.1/dns-query",
    "-H", "User-Agent: OpenGrid-Wealth-Dev/1.0",
    req_url
]

try:
    print("Executing cURL request (this may take up to 30-60 seconds)...")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if proc.returncode == 0:
        data = json.loads(proc.stdout)
        
        locations = []
        for element in data.get("elements", []):
            if "tags" in element:
                if element["type"] == "node":
                    locations.append([element["lat"], element["lon"]])
                elif element["type"] == "way" and "center" in element:
                    locations.append([element["center"]["lat"], element["center"]["lon"]])
        
        output_file = "src/data/walmart_locations.json"
        os.makedirs("src/data", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(locations, f)
            
        print(f"Successfully cached {len(locations)} Walmart properties to {output_file}!")
    else:
        print("cURL command failed with error:", proc.stderr)
except Exception as e:
    print(f"Failed to fetch locations: {e}")
