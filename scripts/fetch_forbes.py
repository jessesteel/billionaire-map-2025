import urllib.request
import json
import gzip

url = "https://www.forbes.com/forbesapi/person/billionaires/2023/position/true.json?limit=3000"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.forbes.com/billionaires/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
})

print("Fetching URL:", url)
try:
    with urllib.request.urlopen(req, timeout=15) as response:
        if response.info().get('Content-Encoding') == 'gzip':
            data = gzip.decompress(response.read())
        else:
            data = response.read()
            
        with open('forbes_test.json', 'wb') as f:
            f.write(data)
        print("Success! Downloaded", len(data), "bytes.")
except Exception as e:
    print("Failed:", e)
