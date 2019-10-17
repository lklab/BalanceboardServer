from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def getOutfitList(request) :
	if request.method == "GET" :
		outfitList = {}
		outfitList["outfitDataList"] = []
		outfitList["outfitDataList"].append({"id" : "1", "status" : "idle", "signalPeriod" : "1000", "changeTime" : "5000"})
		outfitList["outfitDataList"].append({"id" : "2", "status" : "bi/4/3", "signalPeriod" : "1000", "changeTime" : "5000"})
		outfitList["outfitDataList"].append({"id" : "3", "status" : "bi/1/2", "signalPeriod" : "1000", "changeTime" : "5000"})
		outfitList["outfitDataList"].append({"id" : "4", "status" : "bi/5/323", "signalPeriod" : "1000", "changeTime" : "5000"})

		return HttpResponse(json.dumps(outfitList))
	else :
		return HttpResponse("this URL only works by GET")

@csrf_exempt
def command(request) :
	if request.method == "POST" :
		data = json.loads(request.body)
		print("received data: " + str(data))
		return HttpResponse("")
	else :
		return HttpResponse("")
