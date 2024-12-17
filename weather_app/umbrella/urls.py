from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/forecast/<str:city>/', views.city_forecast, name='city_forecast'),  # Nova URL
    path("api/remove-city/<str:city_name>/", views.remove_city, name="remove_city"),

]
