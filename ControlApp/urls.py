from django.urls import path
from . import views

urlpatterns = [
	path('getOutfitList', views.getOutfitList, name='getOutfitList'),
	path('command', views.command, name='command'),
]
