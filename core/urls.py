from django.urls import path
from .views import home

urlpatterns = [
	#Path del Home
    path('', home, name="home"),
]