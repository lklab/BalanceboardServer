from django.db import models

class OutfitId(models.Model) :
	uuid = models.CharField(max_length=64, primary_key=True)
	id = models.IntegerField()

	def __str__(self) :
		return str(self.id)

class ResultData(models.Model) :
	index = models.BigIntegerField(primary_key=True)
	id = models.IntegerField()
	exercise = models.CharField(max_length=32)
	level = models.IntegerField()
	date = models.DateTimeField()
	fileName = models.CharField(max_length=32)

	def __str__(self) :
		return str(self.fileName)
