from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def fetchCommand(request) :
	if request.method == "GET" :
		return HttpResponse("hello outfit, it works!!!")
	else :
		return HttpResponse("this URL only works by GET")

@csrf_exempt
def updateStatus(request) :
	if request.method == "POST" :
		data = json.loads(request.body)
		print("received data: " + str(data))
		return HttpResponse("")
	else :
		return HttpResponse("")

