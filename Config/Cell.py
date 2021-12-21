import re

class Cell():

	# Keys known at compile time
	CellNameKey = 'CellName'
	PlantTypeKey = 'PlantType'
	SprayPinKey = 'SprayPin'
	TimeBetweenSpraysKey = 'TimeBetweenSprays'
	SprayDurationKey = 'OnTime'
	LastSprayKey = 'LastSpray'

	KeySearch = '<[a-zA-Z\s\d.]*>'
	ValueSearch = '>[a-zA-Z\/\d.]*<\/'
	
	def __init__(self, Name = 'Default_Name', PlantType = 'Default_Plant', SprayPin = None, TimeBetweenSprays = 120.0, SprayDuration = 10.0, LastSpray = 0.0):
		
		self.CellData = {}
		self.CellData[self.CellNameKey] = Name
		self.CellData[self.PlantTypeKey] = PlantType
		self.CellData[self.SprayPinKey] = SprayPin
		self.CellData[self.TimeBetweenSpraysKey] = TimeBetweenSprays
		self.CellData[self.SprayDurationKey] = SprayDuration
		self.CellData[self.LastSprayKey] = LastSpray
		
		self.KeyPattern = re.compile(self.KeySearch)
		self.ValuePattern = re.compile(self.ValueSearch)

	def SetField(self, key, value):
		if key in self.CellData.keys():
			self.CellData[key] = value
		else:
			print('Key "{0}" not present in dictionary, use "AddField"'.format(key))

	def AddField(self, key, value):
		if key in self.CellData.keys():
			print('Key "{0}" present in dictionary, use "SetField"'.format(key))
		else:
			self.CellData[key] = value
	
	def GetField(self, key):
		if not key in self.CellData.keys():
			print('Key "{0}" not present in dictionary'.format(key))
		else:
			return self.CellData[key]

	def Serialize(self):
		s = '<Cell>\n'
		for key, val in self.CellData.items():
			s += '\t<' + str(key) + '>' + str(val) + '</' + str(key) + '>\n'
		s += '</Cell>\n'

		return s

	def Deserialize(self, rawString, diagnosticMode = False):

		self.CellData.clear()

		rawString = rawString.replace('<Cell>', '').replace('</Cell>', '')

		keys = self.KeyPattern.findall(rawString)
		values = self.ValuePattern.findall(rawString)

		if diagnosticMode:
			print(zip(keys, values))

		if not len(keys) == len(values):
			print('Error Deserializing Cell, number of keys did not match number of values: ({0} != {1})\n{2}'.format(len(keys), len(values), rawString))
			return

		for key, val in zip(keys, values):
			key = key.replace('<', '').replace('>', '')
			val = val.replace('</', '').replace('>', '')
			self.CellData[key] = val
		
	def __str__(self):
		s = ''
		for key, val in self.CellData.items():
			s += str(key) + ':' + str(val) + '\n'
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'

	file = open(path)
	data = file.read()
	file.close()

	#cellSearch = '<Cell>[.\\s]*<\/Cell>'
	cellSearch = '<Cell>[a-zA-Z\s<>\/\d.]*<\/Cell>'
	cellPattern = re.compile(cellSearch)

	cellData = cellPattern.findall(data)
	cells = []

	for match in cellData:
		cell = Cell()
		cell.Deserialize(match)

		cells.append(cell)
		print(cell)


