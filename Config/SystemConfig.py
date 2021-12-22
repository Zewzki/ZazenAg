import re
import os
from os.path import exists
import traceback

from .Garden import Garden
from .Cell import Cell
from .Basin import Basin

class SystemConfig():

	GardenSearch = '<Garden>[a-zA-Z\s<>\/\d.:]*<\/Garden>'
	DiagnosticModeSearch = '<DiagnosticMode>[a-zA-Z]*<\/DiagnosticMode>'
	SystemDelaySearch = '<SystemDelayMs>[\d.:]*<\/SystemDelayMs>'

	DiagnosticModeKey = 'DiagnosticMode'
	SystemDelayKey = 'SystemDelayMs'

	def __init__(self, path):
		
		self.GardenList = {}
		self.GardenPattern = re.compile(self.GardenSearch)
		self.DiagnosticModePattern = re.compile(self.DiagnosticModeSearch)
		self.SystemDelayPattern = re.compile(self.SystemDelaySearch)

		self.DiagnosticMode = False
		self.SystemDelayMs = 1000

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

		s += '<' + self.DiagnosticModeKey + '>' + str(self.DiagnosticMode) + '</' + self.DiagnosticModeKey + '>\n'
		s += '<' + self.SystemDelayKey + '>' + str(self.SystemDelayMs) + '</' + self.SystemDelayKey + '>\n'

		for key, val in self.GardenList.items():
			s += val.Serialize() + '\n'
		
		s += '</SystemConfig>'

		with open(saveDir, 'w') as configFile:
			configFile.write(s)
	
	def Deserialize(self, loadDir):

		try:

			configData = None

			with open(loadDir, 'r') as configFile:
				configData = configFile.read()

			configData = configData.replace('<SystemConfig>', '').replace('</SystemConfig>', '')

			# Search for diagnostic mode
			searchResults = self.DiagnosticModePattern.findall(configData)
			if searchResults is None:
				raise Exception('DiagnosticMode not present in config file')
			searchResults = searchResults[0].replace('<DiagnosticMode>', '').replace('</DiagnosticMode>', '')
			if searchResults == 'True':
				self.DiagnosticMode = True
			else:
				self.DiagnosticMode = False

			# Search for system delay
			searchResults = self.SystemDelayPattern.findall(configData)
			if searchResults is None:
				raise Exception('SystemDelayMs not present in config file')
			searchResults = searchResults[0].replace('<SystemDelayMs>', '').replace('</SystemDelayMs>', '')
			self.SystemDelayMs = float(searchResults)

			gardens = self.GardenPattern.findall(configData)

			if self.DiagnosticMode:
				print(configData)
				print(gardens)

			if len(gardens) == 0:
				raise Exception('Error finding Gardens in config file')

			for match in gardens:
				garden = Garden()
				garden.Deserialize(match, self.DiagnosticMode)
				self.GardenList[garden.GetField('GardenName')] = garden
			
		except Exception:
			print('Unable to Deserialize from "{0}"'.format(loadDir))
			traceback.print_exc()
	
	def __str__(self):
		s = '-System Config-\n'
		for key, val in self.GardenList.items():
			s += str(val) + '\n--------------\n'
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'
	sysConfig = SystemConfig(path)
	print(sysConfig)