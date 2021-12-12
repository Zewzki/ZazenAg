import re
import os
from os.path import exists

from Garden import Garden
from Cell import Cell
from Basin import Basin

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
	
	def Serialize(self, saveDir):
		s = '<SystemConfig>'
		
		for gardenName in self.GardenList.keys():
			s += str(self.GardenList[gardenName]) + '\n'
		
		s = '</SystemConfig>'

		configFile = open(saveDir, 'w')
		configFile.write(s)
		configFile.close()
	
	def Deserialize(self, loadDir):
		configFile = open(loadDir, 'r')
		configData = configFile.read()
		configFile.close()

		configData = configData.replace('<SystemConfig>', '').replace('</SystemConfig>', '')

		gardens = self.GardenPattern.findall(configData)

		for match in gardens:
			garden = Garden()
			garden.Deserialize(match)

			self.GardenList[garden.GetField('GardenName')] = garden
	
	def __str__(self):
		s = '-System Config-\n'
		for gardenName in self.GardenList.keys():
			s += str(self.GardenList[gardenName]) + '\n--------------\n'
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'
	sysConfig = SystemConfig(path)
	print(sysConfig)