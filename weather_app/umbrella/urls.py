from django.urls import path
from .views import GetForecastView, ForecastHistoryView

urlpatterns = [
    path('forecast/<str:city>/', GetForecastView.as_view(), name='get_forecast'),
    path('forecast/history/', ForecastHistoryView.as_view(), name='forecast_history'),
]