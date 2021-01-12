########### Python Form Recognizer Labeled Async Train #############
import json
import time
from requests import get, post

# Endpoint URL
endpoint = r"<endpoint>"
post_url = endpoint + r"/formrecognizer/v2.0/custom/models"
source = r"<SAS URL>"
prefix = "<Blob folder name>"
includeSubFolders = False
useLabelFile = False

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '<subsription key>',
}

body =     {
    "source": source,
    "sourceFilter": {
        "prefix": prefix,
        "includeSubFolders": includeSubFolders
    },
    "modelName":"<your model name>",
    "useLabelFile": useLabelFile
}

try:
    resp = post(url = post_url, json = body, headers = headers)
    if resp.status_code != 201:
        print("POST model failed (%s):\n%s" % (resp.status_code, json.dumps(resp.json())))
        quit()
    print("POST model succeeded:\n%s" % resp.headers)
    get_url = resp.headers["location"]
except Exception as e:
    print("POST model failed:\n%s" % str(e))
    quit() 


## Get Training Results
# n_tries = 15
# n_try = 0
# wait_sec = 5
# max_wait_sec = 60
# while n_try < n_tries:
#     try:
#         resp = get(url = get_url, headers = headers)
#         resp_json = resp.json()
#         if resp.status_code != 200:
#             print("GET model failed (%s):\n%s" % (resp.status_code, json.dumps(resp_json)))
#             quit()
#         model_status = resp_json["modelInfo"]["status"]
#         if model_status == "ready":
#             print("Training succeeded:\n%s" % json.dumps(resp_json))
#             quit()
#         if model_status == "invalid":
#             print("Training failed. Model is invalid:\n%s" % json.dumps(resp_json))
#             quit()
#         # Training still running. Wait and retry.
#         time.sleep(wait_sec)
#         n_try += 1
#         wait_sec = min(2*wait_sec, max_wait_sec)     
#     except Exception as e:
#         msg = "GET model failed:\n%s" % str(e)
#         print(msg)
#         quit()
# print("Train operation did not complete within the allocated time.")
