import json

class Helper(object):
	
	def getData(data, key = None):

		if type(data) is str:
			data = json.loads(data)

		if key:
			return data[key]
		return data
