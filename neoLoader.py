import imp
import md5
import os.path
import traceback
import sys

class NeoLoader:
	def __init__(self):
		print "Initiated"

## http://code.davidjanes.com/blog/2008/11/27/how-to-dynamically-load-python-code/
	def loadMod(self,path):
		try:
			try:
				## Where are these being used code_dir, code_file?
				code_dir = os.path.dirname(path)
				code_file = os.path.basename(path)

				fin = open(path, 'rb')

				return imp.load_source(md5.new(path).hexdigest(),path,fin)
			finally:
				try: fin.close()
				except: pass

		except ImportError, x:
			traceback.print_exc(file = sys.stderr)
			raise
		except:
			traceback.print_exc(file = sys.stderr)
			raise
