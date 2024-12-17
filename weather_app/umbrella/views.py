from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# URL para pegar os dados do OpenWeatherMap
API_KEY = '0c8ca0134cd7534aaf34fdca3a003878'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + API_KEY
WEATHER_API = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely&appid=' + API_KEY + '&units=metric'

# Função para a página inicial (exibe as cidades e suas temperaturas)
def index(request):
    cities = City.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0c8ca0134cd7534aaf34fdca3a003878'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name'].strip()
            # Verificar se a cidade já existe no banco de dados
            if City.objects.filter(name__iexact=city_name).exists():
                messages.warning(request, f'The city "{city_name}" is already in the list.')
            else:
                # Adicionar a cidade à base de dados
                form.save()
                messages.success(request, f'The city "{city_name}" was successfully added.')

    form = CityForm()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city.name)).json()
        weather = {
            'city': city.name,
            'temperature': int(city_weather['main']['temp']),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'umbrella/index.html', context)

# Função para formatar o timestamp para hora
def dt_to_hour(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%H:%M")

# Função para formatar o timestamp para dia
def dt_to_day(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%A, %d %b")

# Função para obter previsão do tempo
def city_forecast(request, city):
    # URL para obter dados de previsão de 5 dias / 3 horas
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse({"error": "City not found or API error"}, status=404)

    forecast_data = response.json()

    # Hora atual
    current_time = datetime.now()

    # Filtrando as previsões para hoje e as 5 previsões seguintes
    hourly_forecast_today = []
    for item in forecast_data["list"]:
        forecast_time = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")

        # Se a previsão é para hoje ou para as 5 previsões seguintes
        if forecast_time >= current_time:
            hourly_forecast_today.append({
                "hour": dt_to_hour(forecast_time.timestamp()),
                "temperature": int(item["main"]["temp"]),  # Arredondar para número inteiro
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"]
            })

        # Limitar para as 5 previsões seguintes
        if len(hourly_forecast_today) == 5:
            break

    # Extraindo previsão diária (mínima e máxima para cada dia)
    daily_forecast = {}
    for item in forecast_data["list"]:
        forecast_date = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
        if forecast_date not in daily_forecast:
            daily_forecast[forecast_date] = {
                "day": dt_to_day(datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").timestamp()),
                "min_temp": int(item["main"]["temp"]),  # Arredondar para número inteiro
                "max_temp": int(item["main"]["temp"]),  # Arredondar para número inteiro
                "icon": item["weather"][0]["icon"]
            }
        else:
            daily_forecast[forecast_date]["min_temp"] = min(daily_forecast[forecast_date]["min_temp"], int(item["main"]["temp"]))
            daily_forecast[forecast_date]["max_temp"] = max(daily_forecast[forecast_date]["max_temp"], int(item["main"]["temp"]))

    daily_forecast_summary = [
        {
            "day": details["day"],
            "min_temp": details["min_temp"],
            "max_temp": details["max_temp"],
            "icon": details["icon"]  # Icone do primeiro período para cada dia
        }
        for date, details in daily_forecast.items()
    ]

    return JsonResponse({
        "hourly_forecast_today": hourly_forecast_today,  # Previsão detalhada do dia de hoje
        "daily_forecast": daily_forecast_summary  # Previsão diária
    })

@csrf_exempt
def remove_city(request, city_name):
    if request.method == "DELETE":
        try:
            city = City.objects.get(name=city_name)
            city.delete()
            return JsonResponse({"message": "City removed successfully."}, status=200)
        except City.DoesNotExist:
            return JsonResponse({"error": "City not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=405)
