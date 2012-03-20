class Loader():
	modules = {}

	def __init__(self):
		print "Initialized"

	def loadMod(self,name):
		mod = __import__(name, fromlist=[])
		self.modules[name] = mod

	def reloadMod(self,name):
		reload(self.modules[name])

	def runMethod(self,mod,method):
		running = getattr(self.modules[mod],method)
		running()

	def showMethods(self,name):
		if (name == ''):
			for i,j in self.modules.iteritems():

				li = dir(j)
				print "Module:",i
				for i in li:
					if ( i[0:2] != '__' ):
						print i
				print ""
				
		else:
			li = dir(self.modules[name])
			for i in li:
				if ( i[0:2] != '__' ):
					print i

	def showMods(self):
		for i,j in self.modules.iteritems():
			print i , ">>> Module:" , j 
		
