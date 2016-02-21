from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import requests
import json
import base64
from requests_oauthlib import OAuth1
from geopy.geocoders import Nominatim

CLIENT_ID="dpv6qe32snp744"
CLIENT_SECRET="bvbbhspmkm6442lnfh0eujqcsl"
INTERNAL_ID="02ff6b24-701e-4527-a96a-99dcd0a42d68"
url="https://climate.com/api/oauth/token/"
GOOGLE_MAPS_API_KEY = "AIzaSyBATtuDcFMBidVP5S2yXSusDckEuTBw2nI"
GOOGLE_MAPS_URL="https://maps.googleapis.com/maps/api/geocode/json"

def login_view(request):
	callbackurl = "http://17495abb.ngrok.io/test/redirecter"
	#callbackurl = request.get_full_path()
	myjson ={'client_id': CLIENT_ID, "mobile": "true", "page":"oidcauthn", "response_type": "code", "redirect_uri":callbackurl, "scope":"openid user"}
	url2 = "https://climate.com/static/app-login/index.html?scope=openid+user"
	newurl2 = "https://climate.com/static/app-login/index.html?scope=openid+user&client_id="+CLIENT_ID+"&mobile=true&page=oidcauthn&response_type=code&redirect_uri="+callbackurl+"&scope=openid user"
	return HttpResponseRedirect(newurl2)
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
	posturl =  "https://climate.com/api/oauth/token"
	postjson = {"grant_type": "authorization_code", "scope": "openid user", "redirect_uri": "http://17495abb.ngrok.io/test/redirecter", "code":newstring}
	encoded =base64.b64encode(CLIENT_ID+':'+CLIENT_SECRET)
	headers = {"Authorization": "Basic "+encoded}
	r=requests.post(posturl, data=postjson, headers=headers)
	d = json.loads(r.text)
	access_token = d['access_token']
	farmsurl= "https://hackillinois.climate.com/api/fields/"
	headers2= {"Authorization": "Bearer " +access_token}
	r2=requests.get(farmsurl, headers=headers2)
	return render(request, 'agro/test.html', {"code": r2.text})
def homepage(request):
	geturl = "http://quickstats.nass.usda.gov/api/api_GET"
	API_KEY = "9C641011-EF91-327C-85AE-BAF02D9A5BAD"
	params = {"key": API_KEY, "commodity_desc": "CORN", "year":"2012","begin_code_alpha":"1", "end_code_alpha":"2", "county_code_alpha": "001", "state_alpha": "CT", "format": "JSON"}
	r = requests.get(geturl, params)
	d = json.loads(r.text)
	myjson =[]
	tons =0
	tonscount=0
	tonsperacre=0
	tonsperacrecount=0
	dollars=0
	dollarscount=0
	for j in d['data']:
		val=j['Value']
		oldval=val
		val=val.replace(',', '')
		#print val
		try:
			intval=int(val)
		#try: 
			if j['unit_desc']=="$":
				
				dollars+=intval
				dollarscount+=1
			elif j['unit_desc']=="TONS":
				tons+=intval
				tonscount+=1
			elif j['unit_desc']=="TONS / ACRE":
				tonsperacrecount+=1
				tonsperacre += intval
			myjson.append([j['unit_desc'], j['Value']])
		except:
			print j['unit_desc']
			print "oldval: " +oldval + "new val: " +val
		#except:
		#	myjson.append({"NO VALUE"})
		
	lat = 41.78648088915638
	longi = -89.04467321197389
	print str(lat) + ", AND " + str(longi)
	newjson = [ {"$": [dollars, dollarscount, dollars/dollarscount], "TONS": [tons, tonscount, tons/tonscount], "TONS / ACRE": [tonsperacre, tonsperacrecount, tonsperacre/tonsperacrecount]}]
	geolocator = Nominatim()
	location = geolocator.reverse(str(lat) + "," + str(longi))
#	print location.address

	return render(request, "agro/index.html", {"stuff": location.address})