from .models import OutfitId, ResultData

import os
import datetime
from django.utils import timezone

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

print("Balanceboard manager is started.")
