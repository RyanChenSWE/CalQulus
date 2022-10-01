from pprint import pprint
import requests
import urllib.parse

from decouple import config

### FUNCTIONS ### 

def matrixConvert(s): 
    s = '[[' + s[s.index('}') + 1:].replace("&", ",").replace('\\\\', '],[').replace(' ', '')
    return s[:s.index('\\')] + ']]'

appid = config('WOLFRAM_ALPHA_APP_ID')

MAX_CHARACTERS = 200

# queries = ["Suzie has 3 apples and I am worthless, how much am I worth?"]
# queries = filter(lambda x: len(x) < MAX_CHARACTERS, queries)
# queries = map(lambda x: urllib.parse.quote(x), queries)

# for query in queries:
#   query_url = f"http://api.wolframalpha.com/v2/query?" \
#       f"appid={appid}" \
#       f"&input={query}" \
#       f"&format=plaintext" \
#       f"&output=json"

#   r = requests.get(query_url).json()

#   print(r['queryresult'])

#   print(r['queryresult']['pods'][0]['subpods'][0]['plaintext'])

# # print(f"Query: '{r}'.")
# equation = "osculating circle y = x^2 at x = 2"
equation = "solve for x^2=1"
query = urllib.parse.quote_plus(f"{equation}")
query_url = f"http://api.wolframalpha.com/v2/query?" \
            f"appid={appid}" \
            f"&input={query}" \
            f"&podstate=Result__Step-by-step+solution" \
            "&format=plaintext" \
            f"&output=json"

r = requests.get(query_url).json()["queryresult"]

# pprint(r)

# filter by succeeded and non errored pods, change to json
pods = list(filter(lambda pod: not pod['error'], r['pods']))

# pprint(pods)

# filter out pods with empty titles in each subpod
pods = list(filter(lambda pod: not all(map(lambda subpod: subpod['title'] == '', pod['subpods'])), pods))

# print second plaintext in subpod
print(pods[0]['subpods'][1]['plaintext'])

# if r["numpods"] == 0:
#   print("No results found.")
# elif r["pods"][0]["subpods"][0]["plaintext"] == '(no solutions exist)' or r["pods"][0]["subpods"][0]["plaintext"] == '(no solution exists)':
#   print("No solutions found.")
# else:
#   pprint(r["pods"][0]["subpods"][0])
#   pprint(r["pods"][0]["subpods"][0]["plaintext"])

# data = r["queryresult"]["pods"][0]["subpods"]
# result = data[0]["plaintext"]
# steps = data[1]["plaintext"]

# print(f"Result of {equation} is '{result}'.\n")
# print(f"Possible steps to solution:\n\n{steps}")
