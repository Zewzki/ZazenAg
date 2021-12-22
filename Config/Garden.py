import re

from .Cell import Cell
from .Basin import Basin
from .Light import Light

class Garden():

	GardenNameKey = 'GardenName'
	CapacityKey = 'Capacity'
	BasinPollDelayKey = 'BasinPollDelay'

	KeySearch = '<[a-zA-Z\s\d.:]*>'
	ValueSearch = '>[a-zA-Z\/\d.:]*<\/'
	CellSearch = '<Cell>[a-zA-Z\s<>\/\d.:]*<\/Cell>'
	BasinSearch = '<Basin>[a-zA-Z\s<>\/\d.:]*<\/Basin>'
	LightSearch = '<Light>[a-zA-Z\s<>\/\d.:]*<\/Light>'

	def __init__(self, Name = 'Default_Name', Capacity = 0, BasinPollDelay = 120.0):

		self.CellList = {}
		self.BasinList = {}
		self.LightList = {}
		self.GardenData = {}
		self.GardenData[self.GardenNameKey] = Name
		self.GardenData[self.CapacityKey] = Capacity
		self.GardenData[self.BasinPollDelayKey] = BasinPollDelay

		self.KeyPattern = re.compile(self.KeySearch)
		self.ValuePattern = re.compile(self.ValueSearch)
		self.CellPattern = re.compile(self.CellSearch)
		self.BasinPattern = re.compile(self.BasinSearch)
		self.LightPattern = re.compile(self.LightSearch)
	
	def SetField(self, key, value):
		if key in self.GardenData.keys():
			self.GardenData[key] = value
		else:
			print('Key "{0}" not present in Data Fields, use "AddField"'.format(key))

	def AddField(self, key, value):
		if key in self.GardenData.keys():
			print('Key "{0}" present in Data Fields, use "SetField"'.format(key))
		else:
			self.GardenData[key] = value
	
	def GetField(self, key):
		if not key in self.GardenData.keys():
			print('Key "{0}" not present in Data Fields'.format(key))
		else:
			return self.GardenData[key]

	def UpdateCell(self, updatedCell):
		cellName = updatedCell.GetField('CellName')
		if not cellName in self.CellList:
			print('Key "{0}" not found in Cell List...'.format(cellName))
		else:
			self.CellList[cellName] = updatedCell
	
	def AddCell(self, newCell):
		cellName = newCell.GetField('CellName')
		if cellName in self.CellList:
			print('Key "{0}" present in Cell List, use UpdateCell...'.format(cellName))
		else:
			self.CellList[cellName] = newCell
	
	def RemoveCell(self, cellName):
		if cellName in self.CellList:
			return self.CellList.pop(cellName)
		else:
			print('Key "{0}" not found in Cell List...'.format(cellName))
			return None
	
	def GetCellList(self):
		return self.CellList
	
	def UpdateBasin(self, updatedBasin):
		basinName = updatedBasin.GetField('BasinName')
		if not basinName in self.BasinList:
			print('Key "{0}" not found in Basin List...'.format(basinName))
		else:
			self.BasinList[basinName] = updatedBasin
	
	def AddBasin(self, newBasin):
		basinName = newBasin.GetField('BasinName')
		if basinName in self.BasinList:
			print('Key "{0}" present in Basin List, use UpdateBasin...'.format(basinName))
		else:
			self.BasinList[basinName] = newBasin
	
	def Removebasin(self, basinName):
		if basinName in self.BasinList:
			return self.BasinList.pop(basinName)
		else:
			print('Key "{0}" not found in Basin List...'.format(basinName))
	
	def GetBasinList(self):
		return self.BasinList

	def UpdateLight(self, updatedLight):
		lightName = updatedLight.GetField('LightName')
		if not lightName in self.LightList:
			print('Key "{0}" not found in Light List...'.format(lightName))
		else:
			self.LightList[lightName] = updatedLight
	
	def AddLight(self, newLight):
		lightName = newLight.GetField('LightName')
		if lightName in self.LightList:
			print('Key "{0}" present in Light List, use Update Light'.format(lightName))
		else:
			self.LightList[lightName] = newLight
	
	def RemoveLight(self, lightName):
		if lightName in self.LightList:
			return self.LightList.pop(lightName)
		else:
			print('Key "{0}" not found in Light List...'.format(lightName))
			return None
	
	def GetLightList(self):
		return self.LightList
	
	def Serialize(self):
		s = '<Garden>\n'
		
		for key, val in self.GardenData.items():
			s += '\t<' + str(key) + '>' + str(val) + '</' + str(key) + '>\n'

		for key, val in self.CellList.items():
			s += val.Serialize()
		
		for key, val in self.BasinList.items():
			s += val.Serialize()

		for key, val in self.LightList.items():
			s += val.Serialize()

		s += '</Garden>\n'

		return s
	
	def Deserialize(self, rawString, diagnosticMode = False):

		self.GardenData.clear()

		rawString = rawString.replace('<Garden>', '').replace('</Garden>', '')

		cells = self.CellPattern.findall(rawString)

		if diagnosticMode:
			print(cells)

		for match in cells:
			rawString = rawString.replace(match, '')
			cell = Cell()
			cell.Deserialize(match, diagnosticMode)
			self.CellList[cell.GetField('CellName')] = cell
		
		basins = self.BasinPattern.findall(rawString)
		if diagnosticMode:
			print(basins)

		for match in basins:
			rawString = rawString.replace(match, '')
			basin = Basin()
			basin.Deserialize(match, diagnosticMode)
			self.BasinList[basin.GetField('BasinName')] = basin
		
		lights = self.LightPattern.findall(rawString)
		if diagnosticMode:
			print(lights)

		for match in lights:
			rawString = rawString.replace(match, '')
			light = Light()
			light.Deserialize(match, diagnosticMode)
			self.LightList[light.GetField('LightName')] = light
		
		keys = self.KeyPattern.findall(rawString)
		vals = self.ValuePattern.findall(rawString)

		if diagnosticMode:
			print(zip(keys, vals))

		if not len(keys) == len(vals):
			print('Error Deserializing Garden, number of keys did not match number of values: ({0} != {1})\n{2}'.format(len(keys), len(vals), rawString))
			print(keys)
			print(vals)
			return
		
		for key, val in zip(keys, vals):
			key = key.replace('<', '').replace('>', '')
			val = val.replace('</', '').replace('>', '')
			self.GardenData[key] = val
	
	def __str__(self):
		s = ''
		for key, val in self.GardenData.items():
			s += str(key) + ':' + str(val) + '\n'

		for cellName in self.CellList:
			s += '----------\n'
			s += str(self.CellList[cellName]) + '\n'
		
		for basinName in self.BasinList:
			s += '----------\n'
			s += str(self.BasinList[basinName]) + '\n'
		
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'
	
	file = open(path)
	data = file.read()
	file.close()

	gardenSearch = '<Garden>[a-zA-Z\s<>\/\d.]*<\/Garden>'
	gardenPattern = re.compile(gardenSearch)

	gardenData = gardenPattern.findall(data)
	gardens = []

	for match in gardenData:
		garden = Garden()
		garden.Deserialize(match.replace('<Garden>', '').replace('</Garden>', ''))

		gardens.append(garden)
		print(garden)
