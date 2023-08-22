from auth_class import ElationAPI_access
import requests
import json

api_access = ElationAPI_access()
access_token = api_access.get_access_token()
auth_header = api_access.format_auth()

resp = requests.get("https://sandbox.elationemr.com/api/2.0/practices/", headers={'Authorization': auth_header})

print(resp.status_code)
print(json.dumps(json.loads(resp.content), indent=2))