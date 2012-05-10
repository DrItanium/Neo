class Loader():
	modules = {}

	def __init__(self):
		print "Loader Initialized"

	def loadMod(self,name):
		mod = __import__(name, fromlist=[])
		self.modules[name] = mod
		return "Loaded " + name + " Module"

	def reloadMod(self,name):
		reload(self.modules[name])
		return "Module Reloaded"

	def runMethod(self,mod,method,arg):
		running = getattr(self.modules[mod],method)
		if ( arg != None ):
			return running(arg)
		return running()

	def showMethods(self,name):
		answer = ""
		if (name == ''):
			for i,j in self.modules.iteritems():

				li = dir(j)
				print "Module:",i
				answer += "Module:" + i + " "
				for i in li:
					if ( i[0:2] != '__' ):
						print i
						answer += "," + i
				print ""
				answer += " | "
				
		else:
			li = dir(self.modules[name])
			for i in li:
				if ( i[0:2] != '__' ):
					print i
		return answer

	def showMods(self):
		for i,j in self.modules.iteritems():
			print i , ">>> Module:" , j 
		return self.modules
		
