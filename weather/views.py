from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from .models import City
from .forms import CityForm




# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=340fb9ddc6c457b9fe7e06ecb544a77a'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            # dabase ma check gareko mathiko ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ name=new_city if xa vane count badaune existion city count ko

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'city does not exist in this planet!!'
            else:
                err_msg = 'city already added to database !! '

        if err_msg:
            message = err_msg
            message_class = "is-danger"
        else:
            message = "city added successfully !!"
            message_class = "is-success"

        print(err_msg)
    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            "city": city.name,
            "temperature": r['main']['temp'],
            "description": r['weather'][0]['description'],
            "icon": r['weather'][0]['icon'],
            "rain": r['weather'][0]['main'],

        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,

    }
    return render(request, 'weather/index.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
