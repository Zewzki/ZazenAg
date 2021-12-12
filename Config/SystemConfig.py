import re
import os
from os.path import exists

from .Garden import Garden
from .Cell import Cell
from .Basin import Basin

class SystemConfig():

	GardenSearch = '<Garden>[a-zA-Z\s<>\/\d.]*<\/Garden>'

	def __init__(self, path):
		
		self.GardenList = {}
		self.GardenPattern = re.compile(self.GardenSearch)

		self.Deserialize(path)

	def GetGarden(self, name):
		if not name in self.GardenList.keys():
			print('Key "{0}" not present in GardenList'.format(name))
			return
		return self.GardenList[name]
	
	def AddGarden(self, newGardenName):
		if newGardenName in self.GardenList.keys():
			print('Key "{0}" is already present in GardenList. Please select a different name'.format(newGardenName))
			return
		self.GardenList[newGardenName] = Garden()
	
	def UpdateGarden(self, updatedGarden):
		gardenName = updatedGarden.GetField('GardenName')

		if not gardenName in self.GardenList.keys():
			print('Key "{0}" is not present in GardenList. Ensure provided garden structure is accurately named'.format(gardenName))
			return
		self.GardenList[gardenName] = updatedGarden
	
	def Serialize(self, saveDir):
		s = '<SystemConfig>\n'
		
		for gardenName in self.GardenList.keys():
			s += self.GardenList[gardenName].Serialize() + '\n'
		
		s += '</SystemConfig>'

		configFile = open(saveDir, 'w')
		configFile.write(s)
		configFile.close()
	
	def Deserialize(self, loadDir):

		try:

			configFile = open(loadDir, 'r')
			configData = configFile.read()
			configFile.close()

			configData = configData.replace('<SystemConfig>', '').replace('</SystemConfig>', '')

			gardens = self.GardenPattern.findall(configData)

			for match in gardens:
				garden = Garden()
				garden.Deserialize(match)

				self.GardenList[garden.GetField('GardenName')] = garden
		except:
			print('Unable to Deserialize from "{0}"'.format(loadDir))
	
	def __str__(self):
		s = '-System Config-\n'
		for gardenName in self.GardenList.keys():
			s += str(self.GardenList[gardenName]) + '\n--------------\n'
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'
	sysConfig = SystemConfig(path)
	print(sysConfig)