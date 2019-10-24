from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import traceback

import Main.Globals as Globals
import Main.BalanceboardManager as BalanceboardManager

@csrf_exempt
def getOutfitList(request) :
	if request.method == "GET" :
		print("[Application log] getOutfitList(): " + str(request.GET))

		try :
			return HttpResponse(json.dumps(BalanceboardManager.getOutfitStatusList()))

		except :
			print("getOutfitList is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("Parameter error", status=400)

	else :
		return HttpResponse("This URL cannot process method " + request.method, status=400)

@csrf_exempt
def command(request) :
	if request.method == "POST" :
		print("[Application log] command(): " + str(request.body))

		try :
			commandData = json.loads(request.body)
			BalanceboardManager.setCommand(commandData)
			return HttpResponse("")

		except :
			print("command is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("Parameter error", status=400)

	else :
		return HttpResponse("This URL cannot process method " + request.method, status=400)
