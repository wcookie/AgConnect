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
import webscraper
import time
import csvparser
CLIENT_ID="dpv6qe32snp744"
CLIENT_SECRET="bvbbhspmkm6442lnfh0eujqcsl"
INTERNAL_ID="02ff6b24-701e-4527-a96a-99dcd0a42d68"
url="https://climate.com/api/oauth/token/"
GOOGLE_MAPS_API_KEY = "AIzaSyBATtuDcFMBidVP5S2yXSusDckEuTBw2nI"
GOOGLE_MAPS_URL="https://maps.googleapis.com/maps/api/geocode/json"

def login_view(request):
	callbackurl = "https://7e2ca291.ngrok.io/test/redirecter"
	#callbackurl = request.get_full_path()
	myjson ={'client_id': CLIENT_ID, "mobile": "true", "page":"oidcauthn", "response_type": "code", "redirect_uri":callbackurl, "scope":"openid user"}
	url2 = "https://climate.com/static/app-login/index.html?scope=openid+user"
	newurl2 = "https://climate.com/static/app-login/index.html?scope=openid+user&client_id="+CLIENT_ID+"&mobile=true&page=oidcauthn&response_type=code&redirect_uri="+callbackurl+"&scope=openid user"
	return HttpResponseRedirect(newurl2)
	#This stuff is all of my login oatuh stuff

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
	postjson = {"grant_type": "authorization_code", "scope": "openid user", "redirect_uri": "https://7e2ca291.ngrok.io/test/redirecter", "code":newstring}
	encoded =base64.b64encode(CLIENT_ID+':'+CLIENT_SECRET)
	headers = {"Authorization": "Basic "+encoded}
	r=requests.post(posturl, data=postjson, headers=headers)
	d = json.loads(r.text)
	access_token = d['access_token']
	print access_token
	#farmsurl= "https://hackillinois.climate.com/api/fields/"
	#headers2= {"Authorization": "Bearer " +access_token}
	#r2=requests.get(farmsurl, headers=headers2)
	request.session['access_token'] = access_token
	return HttpResponseRedirect(reverse('dash'))
	#this gets all of the users fields that they have
	#return render(request, 'agro/test.html', {"code": r2.text})

def homepage(request):
	access_token=""
	while (True):
		try:
			access_token = request.session['access_token']
			print access_token
			break
		except:
			pass
			

	#print access_token
	farmsurl= "https://hackillinois.climate.com/api/fields/"
	headers2= {"Authorization": "Bearer " +access_token}
	
	r2=requests.get(farmsurl, headers=headers2)
	geturl = "http://quickstats.nass.usda.gov/api/api_GET"
	API_KEY = "9C641011-EF91-327C-85AE-BAF02D9A5BAD"
	d=[]
	while (True):
		try:
			d=json.loads(r2.text)
			break
		except:
			pass
	longi = []
	lat =[]
	longi.append( d['fields'][0]['centroid']['coordinates'][0])
	lat.append( d['fields'][0]['centroid']['coordinates'][1])
	longi.append( d['fields'][1]['centroid']['coordinates'][0])
	print longi
	lat.append( d['fields'][1]['centroid']['coordinates'][1])
	print lat
	codes = []
	codes=geo_helper(lat[1],longi[1])
	print codes
	codes2=[]
	codes2=geo_helper(lat[0],longi[0])
	#params = {"key": API_KEY, "commodity_desc": "CORN", "year":"2012","begin_code_alpha":"1", "end_code_alpha":"2", "county_code_alpha": "001", "state_alpha": "CT", "format": "JSON"}
	state_val=""
	state_val2=""
	if codes[0]=="17":
		state_val="IL"
	elif codes[0]=="09":
		state_val="CT"
	elif codes[0]=="19":
		state_val="IA"
	elif codes[0]=="34":
		state_val="NJ"	
	# 001 CT
	# 061 IA
	# 027 NJ
	if codes2[0]=="17":
		state_val2="IL"
	elif codes2[0]=="09":
		state_val2="CT"
	elif codes2[0]=="19":
		state_val2="IA"
	elif codes2[0]=="34":
		state_val2="NJ"
	print state_val2
	params = {"key": API_KEY, "commodity_desc": "CORN", 
	"year":"2012","begin_code_alpha":"1", "end_code_alpha":"12", "county_code_alpha":codes[1], 
	"state_alpha": state_val, "format": "JSON"}
	params2 = {"key": API_KEY, "commodity_desc": "CORN", 
	"year":"2012","begin_code_alpha":"1", "end_code_alpha":"12", "county_code_alpha":codes2[1], 
	"state_alpha": state_val2, "format": "JSON"}
	r2=requests.get(geturl, params2)
	r = requests.get(geturl, params)
	d = json.loads(r.text)
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
		except:
			pass
			#print j['unit_desc']
			#print "oldval: " +oldval + "new val: " +val
	#so far this is arbitrary.  time to make it take an input of a JSON object of all the fields lat and long and names
	# then pass it into geo_view which i will change from a view
	#into a function that takes two parameters, lat and longi.  Then display the stuff I was doing before. 
	newjson=[{}, {}]
	if dollarscount>0:
		newjson[0]['$']=[dollars,dollarscount,dollars/dollarscount]
	if tonscount>0:
		newjson[0]['TONS']=[tons, tonscount, tons/tonscount]
	if tonsperacrecount>0:
		newjson[0]["TONS / ACRE"] = [tonsperacre, tonsperacrecount, tonsperacre/tonsperacrecount]
	d=json.loads(r2.text)
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
		except:
			pass
	if dollarscount>0:
		newjson[1]['$']=[dollars,dollarscount,dollars/dollarscount]
	if tonscount>0:
		newjson[1]['TONS']=[tons, tonscount, tons/tonscount]
	if tonsperacrecount>0:
		newjson[1]["TONS / ACRE"] = [tonsperacre, tonsperacrecount, tonsperacre/tonsperacrecount]

#	newjson =  {"$": [dollars, dollarscount, dollars/dollarscount], "TONS": [tons, tonscount, tons/tonscount], "TONS / ACRE": [tonsperacre, tonsperacrecount, tonsperacre/tonsperacrecount]}
	return render(request, "agro/index.html", {"stuff": newjson})	



def geo_view(request):

	lat = 41.78648088915638
	longi = -89.04467321197389
	geolocator = Nominatim()
	location = geolocator.reverse(str(lat) + "," + str(longi))
	arr = location.address.split(',')
	print arr[2]
	mystring=""
	for char in arr[2][1::]:
		if char==' ':
			break
		else:
			mystring+=char
#	print location.address
	jsons = csvparser.weather_stuff("Dubuque")
	codes = webscraper.parse_file("Illinois", mystring)
	return render(request, "agro/index.html", {"stuff": jsons})


def geo_helper(lat, longi):
	geolocator = Nominatim()
	location = geolocator.reverse(str(lat) + "," + str(longi))
	arr = location.address.split(',')
	print arr[2]
	print arr[3]
	mystate=""
	mycounty=""
	for char in arr[3][1::]:
		if char==' ':
			break
		else:
			mystate+=char
	for char in arr[2][1::]:
		if char==' ':
			break
		else:
			mycounty+=char
	print mycounty
	codes = webscraper.parse_file(mystate, mycounty)
	return codes