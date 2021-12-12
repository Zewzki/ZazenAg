import re

from .Cell import Cell
from .Basin import Basin

class Garden():

	GardenNameKey = 'GardenName'
	CapacityKey = 'Capacity'
	BasinPollDelayKey = 'BasinPollDelay'

	KeySearch = '<[a-zA-Z\s\d.]*>'
	ValueSearch = '>[a-zA-Z\/\d.]*<\/'
	CellSearch = '<Cell>[a-zA-Z\s<>\/\d.]*<\/Cell>'
	BasinSearch = '<Basin>[a-zA-Z\s<>\/\d.]*<\/Basin>'

	def __init__(self, Name = 'Default_Name', Capacity = 0, BasinPollDelay = 120.0):

		self.CellList = {}
		self.BasinList = {}
		self.GardenData = {}
		self.GardenData[self.GardenNameKey] = Name
		self.GardenData[self.CapacityKey] = Capacity
		self.GardenData[self.BasinPollDelayKey] = BasinPollDelay

		self.KeyPattern = re.compile(self.KeySearch)
		self.ValuePattern = re.compile(self.ValueSearch)
		self.CellPattern = re.compile(self.CellSearch)
		self.BasinPattern = re.compile(self.BasinSearch)
	
	def SetField(self, key, value):
		if key in self.GardenData.keys():
			self.GardenData[key] = value
		else:
			print('Key "{0}" not present in dictionary, use "AddField"'.format(key))

	def AddField(self, key, value):
		if key in self.GardenData.keys():
			print('Key "{0}" present in dictionary, use "SetField"'.format(key))
		else:
			self.GardenData[key] = value
	
	def GetField(self, key):
		if not key in self.GardenData.keys():
			print('Key "{0}" not present in dictionary'.format(key))
		else:
			return self.GardenData[key]

	def UpdateCell(self, updatedCell):
		cellName = updatedCell.GetField('CellName')
		if not cellName in self.CellList.keys():
			print('Key "{0}" not found in Cell List...'.format(cellName))
		else:
			self.CellList[cellName] = updatedCell
	
	def AddCell(self, newCell):
		self.CellList[newCell.Name] = newCell
	
	def RemoveCell(self, cellName):
		if cellName in self.CellList.keys():
			return self.CellList.pop(cellName)
		else:
			print('Key "{0}" not found in Cell List...'.format(cellName))
			return None
	
	def GetCellList(self):
		return self.CellList
	
	def Serialize(self):
		s = '<Garden>\n'
		
		for key in self.GardenData.keys():
			s += '\t<' + key + '>' + str(self.GardenData[key]) + '</' + key + '>\n'

		for cellName in self.CellList.keys():
			s += self.CellList[cellName].Serialize()
		
		for basinName in self.BasinList.keys():
			s += self.BasinList[basinName].Serialize()

		s += '</Garden>\n'
		return s
	
	def Deserialize(self, rawString):

		self.GardenData.clear()

		rawString = rawString.replace('<Garden>', '').replace('</Garden>', '')

		cells = self.CellPattern.findall(rawString)

		for match in cells:
			rawString = rawString.replace(match, '')
			cell = Cell()
			cell.Deserialize(match)
			self.CellList[cell.GetField('CellName')] = cell
		
		basins = self.BasinPattern.findall(rawString)

		for match in basins:
			rawString = rawString.replace(match, '')
			basin = Basin()
			basin.Deserialize(match)
			self.BasinList[basin.GetField('BasinName')] = basin
		
		keys = self.KeyPattern.findall(rawString)
		vals = self.ValuePattern.findall(rawString)

		if not len(keys) == len(vals):
			print('Error Deserializing, number of keys did not match number of values: ({0} != {1})\n{2}'.format(len(keys), len(vals), rawString))
			print(keys)
			print(vals)
			return
		
		for i in range(0, len(keys)):
			key = keys[i]
			val = vals[i]

			key = key.replace('<', '').replace('>', '')
			val = val.replace('</', '').replace('>', '')
			self.GardenData[key] = val
	
	def __str__(self):
		s = ''
		for key in self.GardenData.keys():
			s += key + ':' + str(self.GardenData[key]) + '\n'

		for cellName in self.CellList.keys():
			s += '----------\n'
			s += str(self.CellList[cellName]) + '\n'
		
		for basinName in self.BasinList.keys():
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
