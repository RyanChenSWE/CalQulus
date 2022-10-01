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
equation = "derivative of 3x^2-2"
query = urllib.parse.quote_plus(f"solve {equation}")
query_url = f"http://api.wolframalpha.com/v2/query?" \
            f"appid={appid}" \
            f"&input={query}" \
            f"&scanner=Solve" \
            f"&podstate=Result__Step-by-step+solution" \
            "&format=plaintext" \
            f"&output=json"

r = requests.get(query_url).json()["queryresult"]
if r["numpods"] == 0:
  print("No results found.")
elif r["pods"][0]["subpods"][0]["plaintext"] == '(no solutions exist)' or r["pods"][0]["subpods"][0]["plaintext"] == '(no solution exists)':
  print("No solutions found.")
else:
  print(r["pods"][0]["subpods"][0]["plaintext"])

# data = r["queryresult"]["pods"][0]["subpods"]
# result = data[0]["plaintext"]
# steps = data[1]["plaintext"]

# print(f"Result of {equation} is '{result}'.\n")
# print(f"Possible steps to solution:\n\n{steps}")
