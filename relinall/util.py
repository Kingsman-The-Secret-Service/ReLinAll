import json

class Util(object):
	
	def getData(data, key = None):
		if key:
			return json.loads(data)[key]
		return json.loads(data)
