import re

class Basin():

	BasinNameKey = 'BasinName'
	TemperatureKey = 'Temp'
	SalinityKey = 'Salinity'
	PollDelayKey = 'PollDelay'

	KeySearch = '<[a-zA-Z\s\d.:]*>'
	ValueSearch = '>[a-zA-Z\/\d.:]*<\/'
	
	def __init__(self, Name = 'Default_Name', PollDelay = 300):
		
		self.BasinData = {}
		self.BasinData[self.BasinNameKey] = Name
		self.BasinData[self.TemperatureKey] = 0.0
		self.BasinData[self.SalinityKey] = 0.0
		self.BasinData[self.PollDelayKey] = PollDelay
		
		self.KeyPattern = re.compile(self.KeySearch)
		self.ValuePattern = re.compile(self.ValueSearch)

	def SetField(self, key, value):
		if key in self.BasinData.keys():
			self.BasinData[key] = value
		else:
			print('Key "{0}" not present in dictionary, use "AddField"'.format(key))

	def AddField(self, key, value):
		if key in self.BasinData.keys():
			print('Key "{0}" present in dictionary, use "SetField"'.format(key))
		else:
			self.BasinData[key] = value
	
	def GetField(self, key):
		if not key in self.BasinData.keys():
			print('Key "{0}" not present in dictionary'.format(key))
		else:
			return self.BasinData[key]

	def Serialize(self):
		s = '<Basin>\n'
		for key, val in self.BasinData.items():
			s += '\t<' + str(key) + '>' + str(val) + '</' + str(key) + '>\n'
		s += '</Basin>\n'
		return s

	def Deserialize(self, rawString, diagnosticMode = False):

		self.BasinData.clear()

		rawString = rawString.replace('<Basin>', '').replace('</Basin>', '')

		keys = self.KeyPattern.findall(rawString)
		values = self.ValuePattern.findall(rawString)

		if diagnosticMode:
			print(zip(keys, values))

		if not len(keys) == len(values):
			print('Error Deserializing Basin, number of keys did not match number of values: ({0} != {1})\n{2}'.format(len(keys), len(values), rawString))
			return

		for key, val in zip(keys, values):
			key = key.replace('<', '').replace('>', '')
			val = val.replace('</', '').replace('>', '')
			self.BasinData[key] = val
		
	def __str__(self):
		s = ''
		for key, val in self.BasinData.items():
			s += str(key) + ':' + str(val) + '\n'
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'

	file = open(path)
	data = file.read()
	file.close()

	#cellSearch = '<Cell>[.\\s]*<\/Cell>'
	cellSearch = '<Basin>[a-zA-Z\s<>\/\d.]*<\/Basin>'
	cellPattern = re.compile(cellSearch)

	basinData = cellPattern.findall(data)
	basins = []

	for match in basinData:
		basin = Basin()
		basin.Deserialize(match)

		basins.append(basin)
		print(basin)