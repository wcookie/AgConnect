from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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


def login_view(request):
	callbackurl = "http://17495abb.ngrok.io/test/redirecter"
	#callbackurl = request.get_full_path()
	myjson ={'client_id': CLIENT_ID, "mobile": "true", "page":"oidcauthn", "response_type": "code", "redirect_uri":callbackurl, "scope":"openid user"}
	url2 = "https://climate.com/static/app-login/index.html?scope=openid+user"
	newurl2 = "https://climate.com/static/app-login/index.html?scope=openid+user&client_id="+CLIENT_ID+"&mobile=true&page=oidcauthn&response_type=code&redirect_uri="+callbackurl+"&scope=openid user"
	r = requests.get(url2, params=myjson);
	return HttpResponseRedirect(newurl2)
	#return render(request, 'agro/index.html', {"stuff": r.status_code})
def test_view(request):
	myurl = request.get_full_path()
	tester = False
	newstring=""
	for char in myurl:
		if tester==True:
			newstring+=char
		else:
			
			if char =='=':
				tester=True

	return render(request, 'agro/test.html', {"code": newstring})