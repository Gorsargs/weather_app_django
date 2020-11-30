import requests
import json
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
from random import shuffle


context = {'form': CityForm()}

with open('json/cities.json','rb') as json_file:
    data = json.load(json_file)
    city_data = []
    for i in data:
        city_data.append(i['Name'])


def index(request):
    global context
    cities = City.objects.all().order_by('id')
    
    API_key = 'd44e6b76b99c928abf23f8db47ea2a9a'
    url = " http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + API_key
    
    if request.method == 'POST':
        if requests.get(url.format(request.POST['name'])).status_code == 200:
            real_name = requests.get(url.format(request.POST['name'])).json()['name']
            req_dict = request.POST.dict()
            req_dict['name'] = real_name
            form = CityForm(req_dict)
            if form.is_valid():
                form.save()
    

    form = CityForm()

    all_cities = []
    for city in cities[::-1]:
        resp = requests.get(url.format(city.name))
        res = resp.json()

        city_info = {
            'name' : res['name'],
            'temp' : res['main']['temp'],
            'humidity': res['main']['humidity'],
            'icon' : res['weather'][0]['icon'],
            'w_speed' : round(res['wind']['speed'] * 3.6, 2),
            'id'   : city.id,  
        }
        
    
        city.name = res['name']


        all_cities.append(city_info)

    context['form'] = form
    context['cities'] = all_cities
    return render(request, 'weather/index.html',context)


def citiesbyname(request):
    try:
        by_name = [i for i in city_data if i[0] == request.POST['name'][0].upper()]
    except:
        by_name = []
    shuffle(city_data)

    API_key = 'd44e6b76b99c928abf23f8db47ea2a9a'
    url = " http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + API_key

    all_cities_named = []
    for y in range(10):
        try:
            resp = requests.get(url.format(by_name[y]))
            res = resp.json()
        

            city_info = {
                'name' : res['name'],
                'temp' : res['main']['temp'],
                'humidity': res['main']['humidity'],
                'icon' : res['weather'][0]['icon'],
                'w_speed' : round(res['wind']['speed'] * 3.6, 2),
            }

            all_cities_named.append(city_info)
        except:
            pass

        
    
    context['cities_named'] = all_cities_named
    return render(request,'weather/index.html',context)
        





def delete_city(request, city_name):
    try:
        City.objects.get(name=city_name).delete()
    except:
        return redirect('/')
    return redirect('/')


