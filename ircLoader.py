## Module loader written specifically for IRC
from neoLoader import NeoLoader

class IrcLoader():
	modList = {}
	nl = NeoLoader()

	def __init__(self):
		print "Initialized"

	def load(self, modPath):
		name = modPath.split('/')[len(modPath.split('/'))-1]
		self.modList[name] = self.nl.loadMod(modPath)

	def listMods(self):
		ans = []
		for i,j in self.modList.iteritems():
			ans.append(i)
		return ans
	
	def run(self,module,inp):
		## Runs the run method for the module
		return self.modList[module].run(inp)

	def desc(self,module):
		## Runs the desc method for the module
		return self.modList[module].desc()
