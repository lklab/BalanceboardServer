from django.urls import path
from . import views

urlpatterns = [
	path('requestId', views.requestId, name='requestId'),
	path('updateStatus', views.updateStatus, name='updateStatus'),
	path('fetchCommand', views.fetchCommand, name='fetchCommand'),
	path('submitResult', views.submitResult, name='submitResult'),
]
