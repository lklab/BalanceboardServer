from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

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
			return HttpResponse("") # TODO report ERROR

	else :
		return HttpResponse("") # TODO report ERROR

@csrf_exempt
def updateStatus(request) :
	if request.method == "POST" :
		print("[Application log] updateStatus(): " + str(request.body))

		try :
			outfitStatus = json.loads(request.body)

			# TODO update outfit status and calculate new command
			# print("received data: " + str(outfitStatus))
			# print("outfit exercise: " + outfitStatus["exercise"])
			# print("outfit level: " + str(outfitStatus["level"]))
			# print("outfit motion: " + str(outfitStatus["motion"]))

			newCommandData = {}
			newCommandData["newCommand"] = "1"
			return HttpResponse(json.dumps(newCommandData))

		except :
			print("updateStatus is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("") # TODO report ERROR

	else :
		return HttpResponse("") # TODO report ERROR

@csrf_exempt
def fetchCommand(request) :
	if request.method == "GET" :
		print("[Application log] fetchCommand(): " + str(request.GET))

		try :
			# TODO calculate command dictionary, this is test code
			response = {}
			response["type"] = Globals.COMMAND_START
			response["exercise"] = Globals.EXERCISE_BI
			response["level"] = 5
			response["signalPeriod"] = 500
			response["changeTime"] = 2
			return HttpResponse(json.dumps(response))

		except :
			print("fetchCommand is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("") # TODO report ERROR

	else :
		return HttpResponse("") # TODO report ERROR

@csrf_exempt
def submitResult(request) :
	if request.method == "POST" :
		print("[Application log] submitResult(): " + str(request.body))

		try :
			resultDictionary = json.loads(request.body)
			BalanceboardManager.saveResultData(resultDictionary)

			# TODO update outfit status and calculate new command
			print("received data: " + str(resultDictionary))
			print("result id: " + resultDictionary["id"])
			print("result exercise: " + resultDictionary["exercise"])
			print("result level: " + str(resultDictionary["level"]))
			print("result result: " + resultDictionary["result"])

			return HttpResponse("")

		except :
			print("submitResult is failed. traceback:")
			traceback.print_exc()
			return HttpResponse("") # TODO report ERROR

	else :
		return HttpResponse("") # TODO report ERROR
