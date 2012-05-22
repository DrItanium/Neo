## This is an example file for how all IRC modules should be

## Name of the module, to be returned in desc()
name = "msgproc.py"

## What the module should return when processing text from IRC
## Gets inp from IRC, processes it, and returns the 
def run(inp):
	return "FUCK THIS SHIT " + inp.split()[0]

## Returns a description of the module including the name at the top
def desc():
	return "Module name" + name + "Message processing module used to interpret IRC chat"
