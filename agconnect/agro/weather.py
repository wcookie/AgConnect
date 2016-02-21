import requests
WEATHER_SOURCE_KEY = "152730b019699f58c11e"

def try_weather(lat, longi):
	base_url = "https://api.weathersource.com/v1/" + WEATHER_SOURCE_KEY
	