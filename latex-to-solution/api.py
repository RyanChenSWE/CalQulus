from pprint import pprint
import requests
import os
import urllib.parse

os.environ['WOLFRAM_ALPHA_APP_ID'] = '8QG9EK-E6HUAUGP6H'
appid = os.environ.get('WOLFRAM_ALPHA_APP_ID')

query = urllib.parse.quote_plus("4+5")
query_url = f"http://api.wolframalpha.com/v2/query?" \
    f"appid={appid}" \
    f"&input={query}" \
    f"&format=plaintext" \
    f"&output=json"

r = requests.get(query_url).json()

print(f"Query: '{r}'.")
