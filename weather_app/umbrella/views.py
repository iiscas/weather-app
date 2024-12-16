from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Forecast
from .serializers import ForecastSerializer
import requests

class GetForecastView(APIView):
    def get(self, request, city):
        # Consumindo a API externa
        api_key = "95803606d56249d2abf0f746a907c4d8"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            forecast = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
            }
            # Salvando no banco de dados
            serializer = ForecastSerializer(data=forecast)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

class ForecastHistoryView(APIView):
    def get(self, request):
        forecasts = Forecast.objects.all()
        serializer = ForecastSerializer(forecasts, many=True)
        return Response(serializer.data)
