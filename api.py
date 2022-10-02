from pprint import pprint
import requests
import urllib.parse

from decouple import config

### FUNCTIONS ###

def matrixConvert(s):
    s = '[[' + s[s.index('}') + 1:].replace("&", ",").replace('\\\\', '],[').replace(' ', '')
    return s[:s.index('\\')] + ']]'

# CONSTANTS ### 

appid = config('WOLFRAM_ALPHA_APP_ID')
MAX_CHARACTERS = 200

def latexSolver(query): 
  query = urllib.parse.quote_plus(query)
  query_url = "http://api.wolframalpha.com/v2/query?" \
              f"appid={appid}" \
              f"&input={query}" \
              "&podstate=Result__Step-by-step+solution" \
              "&format=plaintext" \
              "&output=json"

  query_url_image = "http://api.wolframalpha.com/v2/query?" \
              f"appid={appid}" \
              f"&input={query}" \
              "&output=json"

  r = requests.get(query_url).json()["queryresult"]
  r2 = requests.get(query_url_image).json()["queryresult"]

  pprint(r2)

  # check if a pod contains id "Result"
  if any(pod["id"] == "Result" for pod in r["pods"]):

      # get the pod with id "Result"
      result_pod = next(pod for pod in r["pods"] if pod["id"] == "Result")

      # print all plaintexts in the pod
      for subpod in result_pod["subpods"]:
          print(subpod["plaintext"])
  else:
      # get results pod
      results_pod = list(filter(lambda x: x['numsubpods'] > 0 and x['subpods']
                                [0]['plaintext'] != '', r['pods']))[0]['subpods'][0]['plaintext']

      if (len(results_pod) == 0):
          print("No steps shown.")
      else:
          print(results_pod)