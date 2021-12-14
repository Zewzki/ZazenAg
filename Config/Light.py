import re

class Light():

	LightNameKey = 'LightName'
	PinNumberKey = 'PinNum'

	KeySearch = '<[a-zA-Z\s\d.]*>'
	ValueSearch = '>[a-zA-Z\/\d.]*<\/'
	
	def __init__(self, Name = 'Default_Name', PinNum = None):
		
		self.LightData = {}
		self.LightData[self.LightNameKey] = Name
		self.LightData[self.PinNumberKey] = PinNum
		
		self.KeyPattern = re.compile(self.KeySearch)
		self.ValuePattern = re.compile(self.ValueSearch)

	def SetField(self, key, value):
		if key in self.LightData.keys():
			self.LightData[key] = value
		else:
			print('Key "{0}" not present in dictionary, use "AddField"'.format(key))

	def AddField(self, key, value):
		if key in self.LightData.keys():
			print('Key "{0}" present in dictionary, use "SetField"'.format(key))
		else:
			self.LightData[key] = value
	
	def GetField(self, key):
		if not key in self.LightData.keys():
			print('Key "{0}" not present in dictionary'.format(key))
		else:
			return self.LightData[key]

	def Serialize(self):
		s = '<Light>\n'
		for key in self.LightData.keys():
			s += '\t<' + key + '>' + str(self.LightData[key]) + '</' + key + '>\n'
		s += '</Light>\n'
		return s

	def Deserialize(self, rawString):

		self.LightData.clear()

		rawString = rawString.replace('<Light>', '').replace('</Light>', '')

		keys = self.KeyPattern.findall(rawString)
		values = self.ValuePattern.findall(rawString)

		if not len(keys) == len(values):
			print('Error Deserializing, number of keys did not match number of values: ({0} != {1})\n{2}'.format(len(keys), len(values), rawString))
			return

		for i in range(0, len(keys)):
			key = keys[i]
			val = values[i]

			key = key.replace('<', '').replace('>', '')
			val = val.replace('</', '').replace('>', '')
			self.LightData[key] = val
		
	def __str__(self):
		s = ''
		for key in self.LightData.keys():
			s += key + ':' + str(self.LightData[key]) + '\n'
		return s

if __name__ == '__main__':

	path = '../Zazen-Config.config'

	file = open(path)
	data = file.read()
	file.close()

	cellSearch = '<Light>[a-zA-Z\s<>\/\d.]*<\/Light>'
	cellPattern = re.compile(cellSearch)

	lightData = cellPattern.findall(data)
	lights = []

	for match in lightData:
		light = Light()
		light.Deserialize(match)

		light.append(light)
		print(light)