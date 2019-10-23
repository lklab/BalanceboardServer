from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import traceback

import Main.Globals as Globals
import Main.BalanceboardManager as BalanceboardManager

@csrf_exempt
# TODO: This code is vulnerable to an infinite request attack.
def requestId(request) :
	if request.method == "GET" :
		print("[Application log] requestId(): " + str(request.GET))

		try :
			response = {}
			response["id"] = BalanceboardManager.getOutfitId(request.GET["uuid"])
			return HttpResponse(json.dumps(response))

		except :
			print("requestId is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("Parameter error", status=400)

	else :
		return HttpResponse("This URL cannot process method " + request.method, status=400)

@csrf_exempt
def updateStatus(request) :
	if request.method == "POST" :
		print("[Application log] updateStatus(): " + str(request.body))

		try :
			outfitStatus = json.loads(request.body)
			BalanceboardManager.updateOutfitStatusList(outfitStatus)

			newCommandData = {}
			if BalanceboardManager.getCommandCode(outfitStatus["id"]) == Globals.COMMAND_NONE :
				newCommandData["newCommand"] = 0
			else :
				newCommandData["newCommand"] = 1
			return HttpResponse(json.dumps(newCommandData))

		except :
			print("updateStatus is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("Parameter error", status=400)

	else :
		return HttpResponse("This URL cannot process method " + request.method, status=400)

@csrf_exempt
def fetchCommand(request) :
	if request.method == "GET" :
		print("[Application log] fetchCommand(): " + str(request.GET))

		try :
			response = BalanceboardManager.getCommand(int(request.GET["id"]))
			return HttpResponse(json.dumps(response))

		except :
			print("fetchCommand is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("Parameter error", status=400)

	else :
		return HttpResponse("This URL cannot process method " + request.method, status=400)

@csrf_exempt
def submitResult(request) :
	if request.method == "POST" :
		print("[Application log] submitResult(): " + str(request.body))

		try :
			resultDictionary = json.loads(request.body)
			BalanceboardManager.saveResultData(resultDictionary)
			return HttpResponse("")

		except :
			print("submitResult is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("Parameter error", status=400)

	else :
		return HttpResponse("This URL cannot process method " + request.method, status=400)
