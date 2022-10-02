from pprint import pprint
import requests
import urllib.parse

from decouple import config

### FUNCTIONS ###


def matrixConvert(s):
    s = '[[' + s[s.index('}') + 1:].replace("&",
                                            ",").replace('\\\\', '],[').replace(' ', '')
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

# print(f"Query: '{r}'.")
query = urllib.parse.quote_plus(input())
query_url = "http://api.wolframalpha.com/v2/query?" \
            f"appid={appid}" \
            f"&input={query}" \
            "&podstate=Result__Step-by-step+solution" \
            "&format=plaintext" \
            "&output=json"

r = requests.get(query_url).json()["queryresult"]

# pprint(r)

#check if a pod contains id "Result"
if any(pod["id"] == "Result" for pod in r["pods"]):

    #get the pod with id "Result"
    result_pod = next(pod for pod in r["pods"] if pod["id"] == "Result")

    # print all plaintexts in the pod
    for subpod in result_pod["subpods"]:
        print(subpod["plaintext"])

    # print(next(pod["subpods"][0]["plaintext"] for pod in r["pods"] if pod["id"] == "Result"))
else:
    # get results pod
    results_pod = list(filter(lambda x: x['numsubpods'] > 0 and x['subpods']
                      [0]['plaintext'] != '', r['pods']))[0]['subpods'][0]['plaintext']

    if (len(results_pod) == 0):
        print("No steps shown.")
    else:
        print(results_pod)


# print second plaintext in subpod
# print(pods[0]['subpods'][1]['plaintext'])

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
