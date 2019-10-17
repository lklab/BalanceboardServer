from django.urls import path
from . import views

urlpatterns = [
	path('fetchCommand', views.fetchCommand, name='fetchCommand'),
	path('updateStatus', views.updateStatus, name='updateStatus'),
]
