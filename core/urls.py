from django.urls import path
from . import views

urlpatterns = [
	#Path del Home
    path('', views.home, name="home"),
]
