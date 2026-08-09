from django.urls import path
from . import views

app_name = 'tiendalibre'

urlpatterns = [
    path('', views.home, name='home'),
    path('home_1/', views.home_1, name='home_1'),
    path('acerca-de-mi/', views.acerca_de_mi, name='acerca-de-mi'),
]