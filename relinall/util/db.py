import sqlite3
import os.path

class DB(object):

	def __init__(self):

		dbExists = os.path.exists('ReLinAll.db')
		self.connect()

		if not dbExists:
			self.generateSchema()

	def connect(self):
		self.connection = sqlite3.connect('ReLinAll.db')
		self.connection.row_factory = self.dict_factory
		self.cursor = self.connection.cursor()

	def generateSchema(self):
		
		self.generateServerTable()

	def generateServerTable(self):
		self.cursor.executescript("CREATE TABLE server(groupname,hostname PRIMARY KEY,username,password,port);")
		self.connection.commit()
		# self.cursor.close()

	def dict_factory(self, cursor, row):
	    d = {}
	    for idx,col in enumerate(cursor.description):
	        d[col[0]] = row[idx]
	    return d

class ServerModel(DB):

	def __init__(self):
		super().__init__()
		
	def getServerGrouped(self):
		self.cursor.execute("SELECT groupname, count(groupname) as count FROM server group by groupname")
		groups = self.cursor.fetchall()
		serverGroupedData = {}
		for group in groups:
			serverGroupedData[group['groupname']] = {}
			serverGroupedData[group['groupname']]['list'] = self.getSeverByGroup(group['groupname'])
			serverGroupedData[group['groupname']]['count'] = group['count']
		return serverGroupedData

	def getSeverByGroup(self, groupname):
		self.cursor.execute("SELECT * FROM server where groupname = '" + groupname + "'")
		return self.cursor.fetchall()

	def insertServer(self, values):
		self.connection.execute("REPLACE INTO server (groupname,hostname,username,password,port) VALUES ('" + values['groupname'] +"', '" + values['hostname'] +"', '" + values['username'] +"', '" + values['password'] +"', '" + values['port'] +"')");
		self.connection.commit()

	def deleteServer(self, hostname):
		self.connection.execute("DELETE from server where hostname = '" + hostname + "';");
		self.connection.commit()

	def deleteGroup(self, groupname):
		self.connection.execute("DELETE from server where groupname = '" + groupname + "';");
		self.connection.commit()