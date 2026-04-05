import json

print("Scanning top billionaires for sparse networks...")

with open("src/data/billionaires.json", "r", encoding="utf-8") as f:
    data = json.load(f)

persons = data.get("personList", {}).get("personsLists", [])

# Sort billionaires by worth
persons.sort(key=lambda p: p.get("finalWorth", 0), reverse=True)

try:
    with open("src/data/holding_companies.json", "r", encoding="utf-8") as f:
        holdings = json.load(f)
except:
    holdings = {}

print(f"\n{'Name':<25} | {'Net Worth':<10} | {'Corporate Key (compName)'}")
print("-" * 70)

for i in range(40):
    p = persons[i]
    name = p.get("personName", "")
    worth = p.get("finalWorth", 0)
    
    compName = p.get("organization") or p.get("source")
    
    if compName and compName not in holdings:
        print(f"{name:<25} | ${worth/1000:<7.1f}B | '{compName}'")
