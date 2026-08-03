from django.urls import path
from . import views

app_name = 'tiendalibre'

urlpatterns = [
    path('', views.home, name='home'),
    path('home_1/', views.home_1, name='home_1'),
]