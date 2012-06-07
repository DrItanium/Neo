## Module loader written specifically for IRC
from neoLoader import NeoLoader

class IrcLoader():
	modList = {}
	nl = NeoLoader()

	def __init__(self):
		print "Initialized"
	
	## Uses neoloader to load the modules
	def load(self, modPath):
		split = modPath.split('/')
		name = split[len(split) - 1]
		self.modList[name] = self.nl.loadMod(modPath)

	def unload(self,name):
		del self.modList[name]

	def listMods(self):
		ans = []
		for i,j in self.modList.iteritems():
			ans.append(i)
		return ans
	
	def run(self,module,inp,sender,channel):
		## Runs the run method for the module
		return self.modList[module].run(inp,sender,channel)

	def desc(self,module):
		## Runs the desc method for the module
		return self.modList[module].desc()
