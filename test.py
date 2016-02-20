import requests
import json
from requests_oauthlib import OAuth1
CLIENT_ID="dpv6qe32snp744"
CLIENT_SECRET="bvbbhspmkm6442lnfh0eujqcsl"
INTERNAL_ID="02ff6b24-701e-4527-a96a-99dcd0a42d68"
url="https://climate.com/api/oauth/token/"
"""
auth=OAuth1(INTERNAL_ID, CLIENT_ID, CLIENT_SECRET)
print requests.get(url, auth=auth)
"""
myjson ={'client_id': CLIENT_ID}
url2 = "https://climate.com/static/app-login/index.html?scope=openid+user"
r = requests.get(url2, params=myjson);
print r.json