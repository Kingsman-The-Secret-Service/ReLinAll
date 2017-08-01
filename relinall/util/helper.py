import json
import subprocess, csv

class Helper(object):
	
	def getData(data, key = None):

		if type(data) is str:
			data = json.loads(data)

		if key:
			return data[key]
		return data
	
	def executeCmd(cmd):
		result = subprocess.run(cmd, stdout=subprocess.PIPE)
		return result

	def outputParser(output, delimiter=' ', skipinitialspace=True, fieldnames=[]):
		reader = csv.DictReader(
			output.decode('utf-8').splitlines()
			, delimiter=delimiter
            , skipinitialspace=skipinitialspace
            , fieldnames=fieldnames)
		return reader