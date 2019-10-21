from .models import OutfitId, ResultData

import os
import datetime, time
import threading
from django.utils import timezone

import Main.Globals as Globals

outfitStatusList = {}
outfitCommandList = {}
outfitLastReportTime = {}

def getOutfitId(uuid) :
	if len(uuid) > 64 :
		uuid = uuid[0:64]

	try:
		outfitId = OutfitId.objects.get(uuid=uuid)
		return outfitId.id

	except OutfitId.DoesNotExist as e :
		outfitId = OutfitId()
		outfitId.uuid = uuid
		outfitId.id = OutfitId.objects.count()
		outfitId.save()
		return outfitId.id

def updateOutfitStatusList(status) :
	_id = status["id"]

	if not _id in outfitStatusList :
		outfitCommandList[_id] = {}
		outfitCommandList[_id]["exercise"]     = status["exercise"]
		outfitCommandList[_id]["level"]        = status["level"]
		outfitCommandList[_id]["signalPeriod"] = status["signalPeriod"]
		outfitCommandList[_id]["changeTime"]   = status["changeTime"]
		outfitCommandList[_id]["startFlag"]    = False

	outfitStatusList[_id] = status
	outfitLastReportTime[_id] = time.time()

def getCommandCode(_id, clearStartFlag=False) :
	isParameterEquals = False

	# is status equals
	if outfitStatusList[_id]["exercise"] == outfitCommandList[_id]["exercise"] and \
		outfitStatusList[_id]["level"] == outfitCommandList[_id]["level"] :
		isStatusEquals = True
	else :
		isStatusEquals = False

	# is start flag
	isStartFlag = outfitCommandList[_id]["startFlag"]

	# is command's exercise is none
	if outfitCommandList[_id]["exercise"] == Globals.EXERCISE_NONE :
		isExerciseNoneCommand = True
	else :
		isExerciseNoneCommand = False

	# is parameter equals
	if outfitStatusList[_id]["signalPeriod"] == outfitCommandList[_id]["signalPeriod"] and \
		outfitStatusList[_id]["changeTime"] == outfitCommandList[_id]["changeTime"] :
		isParameterEquals = True
	else :
		isParameterEquals = False

	# calculate command code
	if not isExerciseNoneCommand and (not isStatusEquals or isStartFlag) :
		commandCode = Globals.COMMAND_START
	elif not isStatusEquals :
		commandCode = Globals.COMMAND_STOP
	elif not isParameterEquals :
		commandCode = Globals.COMMAND_PARAMETER
	else :
		commandCode = Globals.COMMAND_NONE

	# clear start flag
	if clearStartFlag :
		outfitCommandList[_id]["startFlag"] = False

	return commandCode

def getCommand(_id) :
	command = {}
	command["type"]         = getCommandCode(_id, clearStartFlag=True)
	command["exercise"]     = outfitCommandList[_id]["exercise"]
	command["level"]        = outfitCommandList[_id]["level"]
	command["signalPeriod"] = outfitCommandList[_id]["signalPeriod"]
	command["changeTime"]   = outfitCommandList[_id]["changeTime"]
	return command

def getOutfitStatusList() :
	return outfitStatusList

def setCommand(command) :
	_id = command["id"]

	if command["type"] is Globals.COMMAND_START :
		outfitCommandList[_id]["exercise"]     = command["exercise"]
		outfitCommandList[_id]["level"]        = command["level"]
		outfitCommandList[_id]["signalPeriod"] = command["signalPeriod"]
		outfitCommandList[_id]["changeTime"]   = command["changeTime"]
		outfitCommandList[_id]["startFlag"]    = True
	else : # command["type"] is Globals.COMMAND_STOP
		outfitCommandList[_id]["exercise"]     = Globals.EXERCISE_NONE
		outfitCommandList[_id]["startFlag"]    = False

def saveResultData(resultDictionary) :
	# check result log directory
	if not os.path.exists("ResultLog") :
		os.makedirs("ResultLog")

	# generate result file name
	now = timezone.now()
	kst = datetime.timezone(datetime.timedelta(hours=9))
	fileName = resultDictionary["id"] + "-" + now.astimezone(kst).strftime("%Y%m%d%H%M%S") + "-"
	filePath = os.path.join("ResultLog", fileName)
	number = 0
	while os.path.exists(filePath + str(number) + ".csv") :
		number = number + 1
	fileName = fileName + str(number) + ".csv"
	filePath = os.path.join("ResultLog", fileName)

	# save result data to file
	file = open(filePath, "w")
	file.write(resultDictionary["result"])
	file.close()

	# save data to database
	resultData = ResultData()
	resultData.index = ResultData.objects.count()
	resultData.id = int(resultDictionary["id"])
	resultData.exercise = resultDictionary["exercise"]
	resultData.level = resultDictionary["level"]
	resultData.date = now
	resultData.fileName = fileName
	resultData.save()

def outfitMonitoringTask() :
	# process
	currentTime = time.time()
	disconnectedOutfitList = []

	for _id, reportTime in outfitLastReportTime.items() :
		if reportTime + 5.0 < currentTime :
			disconnectedOutfitList.append(_id)

	for _id in disconnectedOutfitList :
		del outfitStatusList[_id]
		del outfitCommandList[_id]
		del outfitLastReportTime[_id]
		print("[Application log] outfit " + str(_id) + " is disconnected.")

	# register next task
	threading.Timer(5, outfitMonitoringTask).start()

outfitMonitoringTask()
print("Balanceboard manager is started.")
