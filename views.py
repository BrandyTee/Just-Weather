from django.shortcuts import render
from datetime import datetime
import json
from urllib.request import urlopen 
import requests
import urllib.error
from datetime import datetime
import datetime as dt
from django.http import JsonResponse
import pandas as pd
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim


def index(request):
    return render(request,
        'index.html',
        {},
    )


def home(request):
        
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    
    if latitude and longitude:
        #Use Nominatim for reverse geocoding 
        geolocator = Nominatim(user_agent="my_geolocation_app")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
                
        #Extract the town/city name
        address = location.raw.get('address', {})
        city_location = address.get('city') or address.get('town') or address.get('village') or "Unkown"
            
    else:
        city_location = "City"
            
    
    
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}?unitGroup=metric&include=days%2Ccurrent&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json&elements=%2Baqius'
                                        
    headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
    response = requests.get(url, headers=headers)
    weather = response.json()
    
    windspeed = weather["days"][0]["windspeed"]
    snow = weather["days"][0]["snow"]
    winddir = weather["days"][0]["winddir"]
        
    resolvedAddress = weather['resolvedAddress']    
    air_quality = weather["days"][0]["aqius"]    
    rain = weather["days"][0]["precipprob"]
    conditions = weather["days"][0]["conditions"]
    description = weather["days"][0]["description"]
    mintemp = weather["days"][0]["tempmin"]
    maxtemp = weather["days"][0]["tempmax"]
    temp = weather["days"][0]["temp"]
                
    #Get the conditions for the major cities
    cities = ["Los Angeles", "New York City", "Cape Town", "Paris", "Tokyo", "Tel Aviv"]
    
    africa_cities = ["Johannesburg", "Lagos", "Cairo", "Nairobi", "Harare", "Kinshasa"]
    
    asia_cities = ["Seoul", "Mumbai", "Riyadh", "Bangkok", "Chongqing", "Kyoto"]
    
    north_cities = ["Mexico City", "Miami", "Havana", "Las Vegas", "Toronto", "Kingston"]
                
    city_conditions = []
    africa_conditions = []
    asia_conditions = []
    north_conditions = []
                
    #World Cities
    for city in cities:
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days%2Ccurrent&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json&elements=%2Baqius'
                                        
        headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
        response = requests.get(url, headers=headers)
        weather = response.json()
                    
        condition = weather["days"][0]["conditions"]
        city_conditions.append(condition)
                
    
    #Africa Cities
    for city in africa_cities:
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days%2Ccurrent&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json&elements=%2Baqius'
                                        
        headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
        response = requests.get(url, headers=headers)
        weather = response.json()
                    
        condition = weather["days"][0]["conditions"]
        africa_conditions.append(condition)
    
    
    #Asia Cities
    for city in asia_cities:
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days%2Ccurrent&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json&elements=%2Baqius'
                                        
        headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
        response = requests.get(url, headers=headers)
        weather = response.json()
                    
        condition = weather["days"][0]["conditions"]
        asia_conditions.append(condition)
    
    
    
    #North America Cities
    for city in north_cities:
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days%2Ccurrent&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json&elements=%2Baqius'
                                        
        headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
        response = requests.get(url, headers=headers)
        weather = response.json()
                    
        condition = weather["days"][0]["conditions"]
        north_conditions.append(condition)
    
    print(f"Yeah{city_conditions}")
    
    city_images = ['images/la4.jpg', 'images/nyc4.jpg', 'images/cpt3.jpg', 'images/paris3.jpg', 'images/tokyo3.jpg', 'images/telaviv3.jpg']
                
    # Render weather data on the homepage
    return render(request, 
    "home.html",
    {
    
        "conditions": conditions,
        "description": description,
        "mintemp" : mintemp,
        "maxtemp" : maxtemp,
        "rain" : rain,
        "temp" : temp,
        "address" : resolvedAddress,
        "city_location": city_location,
    
        "first_city": cities[0],
        "first_image": city_images[0],
        "first_condition": city_conditions[0],
        'world_cities': zip(cities[1:], city_conditions[1:], city_images[1:]), 
        
        'first_africa_city': africa_cities[0],
        'first_africa_conditions': africa_conditions[0],
        'africa_cities': zip(africa_cities[1:], africa_conditions[1:]),
        
        'first_asia_city': asia_cities[0],
        'first_asia_conditions': asia_conditions[0],
        'asia_cities': zip(asia_cities[1:], asia_conditions[1:]), 
        
        'first_north_city': north_cities[0],
        'first_north_conditions': north_conditions[0],
        'north_cities': zip(north_cities[1:], north_conditions[1:]), 
        
                
    }
    )    



#Create Today Page 
def today(request, city):
    
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days%2Ccurrent&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json&elements=%2Baqius'
                                        
    headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
    response = requests.get(url, headers=headers)
    weather = response.json()
    
    windspeed = weather["days"][0]["windspeed"]
    snow = weather["days"][0]["snow"]
    winddir = weather["days"][0]["winddir"]
        
    resolvedAddress = weather['resolvedAddress']    
    air_quality = weather["days"][0]["aqius"]    
    rain = weather["days"][0]["precipprob"]
    condition = weather["days"][0]["conditions"]
    description = weather["days"][0]["description"]
    mintemp = weather["days"][0]["tempmin"]
    maxtemp = weather["days"][0]["tempmax"]
    temp = weather["days"][0]["temp"]
    
    good = ''
    moderate = ''
    sensitive = ''
    unhealthy = ''
    very = ''
    
    if air_quality > 0 and air_quality < 51:
        good = air_quality
    elif air_quality > 50 and air_quality < 101:
        moderate = air_quality
    elif air_quality > 100 and air_quality < 151:
        sensitive = air_quality
    elif air_quality > 150 and air_quality < 201:
        unhealthy = air_quality
    elif air_quality > 200 and air_quality < 301:
        very = air_quality
        
    
    #Get the date
    today = datetime.today()    
    now = today.date()
    #dates = now + dt.timedelta(days=1)
    formatted = now.strftime('%a %d %b %Y')
    
    
    days_rains = []
    days_conditions = []
    days_min = []
    days_max = []
    days_date = []
    for x in range(15):
        rain = weather["days"][x]["precipprob"]
        condition = weather["days"][x]["conditions"]
        mintemp = weather["days"][x]["tempmin"]
        maxtemp = weather["days"][x]["tempmax"]

        #Get the date
        today = datetime.today()    
        now = today.date()
        dates = now + dt.timedelta(days=x)
        todays_date = dates.strftime('%a %d %b %Y')
        
        days_rains.append(rain)
        days_conditions.append(condition)
        days_min.append(mintemp)
        days_max.append(maxtemp)
        days_date.append(todays_date)
            
    
    good = ''
    moderate = ''
    sensitive = ''
    unhealthy = ''
    very = ''
    
    if air_quality > 0 and air_quality < 51:
        good = air_quality
    elif air_quality > 50 and air_quality < 101:
        moderate = air_quality
    elif air_quality > 100 and air_quality < 151:
        sensitive = air_quality
    elif air_quality > 150 and air_quality < 201:
        unhealthy = air_quality
    elif air_quality > 200 and air_quality < 301:
        very = air_quality
        
    
    #Get the date
    today = datetime.today()    
    now = today.date()
    #dates = now + dt.timedelta(days=1)
    formatted = now.strftime('%a %d %b %Y')
    
    
    #Hourly Weather
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key=W9KHP5YVT5FZQDSKY2Y9DNCW6&contentType=json'
                                        
    headers = {'X-Auth-Token' : 'W9KHP5YVT5FZQDSKY2Y9DNCW6', 'Accept-Encoding': '' }
                        
    response = requests.get(url, headers=headers)
    weather = response.json()
    
    hours_rains = []
    hours_conditions = []
    hours_temp = []
    hours_date = []
    for x in range(len(weather["days"][0]["hours"])):
        time = weather["days"][0]["hours"][x]["datetime"]        
        rain = weather["days"][0]["hours"][x]["precipprob"]
        condition = weather["days"][0]["hours"][x]["conditions"]
        temp = weather["days"][0]["hours"][x]["temp"]

        
        
        hours_rains.append(rain)
        hours_conditions.append(condition)
        hours_temp.append(temp)
        hours_date.append(time)
    
    return render(request,
        "today.html", 
        {
            
            "mintemp" : mintemp,
            "maxtemp" : maxtemp,
            "description" : description,
            "temp" : temp,
            "condition" : condition,
            "rain" : rain,
            "windspeed" : windspeed,
            "winddir" : winddir,
            "snow" : snow,
            "resolvedAddress" : resolvedAddress, 
            "air_quality" : air_quality,
            "good" : good,
            "very" : very,
            "unhealthy" : unhealthy,
            "moderate" : moderate,
            "sensitive" : sensitive,
            "city": city,
            "formatted" : formatted,
            
            'first_day_min': days_min[0],
            'first_day_max': days_max[0],
            'first_day_rains': days_rains[0],
            'first_day_date': days_date[0],
            'first_day_conditions': days_conditions[0],
            
            'days_weather': zip(days_min[1:], days_max[1:], days_conditions[1:], days_rains[1:], days_date[1:]),
            
            'first_hour_temp': hours_temp[0],
            'first_hour_rains': hours_rains[0],
            'first_hour_date': hours_date[0],
            'first_hour_conditions': hours_conditions[0],
            
            'hours_weather': zip(hours_temp[1:], hours_conditions[1:], hours_rains[1:], hours_date[1:]), 
        }
    )   
    

#Search Page Function
def search_page(request, searched_city):
    cities = pd.read_csv('/storage/emulated/0/weather/justweather/static/csv/worldcities/worldcities.csv')
    #print(cities.info())
    cities_df = cities[cities['city_ascii'].apply(lambda x: not isinstance(x, float))]
    city = cities_df['city_ascii'].values
    print(city)
    
    my_cities = []
    
    for c in city:
        if searched_city in c:                
            my_cities.append(c)
    
    #print(my_cities)
    
    return render(request,
        "search_page.html",
        {"my_cities" : my_cities},
    )



