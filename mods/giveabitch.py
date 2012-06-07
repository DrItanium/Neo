## This is an example file for how all IRC modules should be

import random
## Name of the module, to be returned in desc()
name = "giveabitch.py"

## What the module should return when processing text from IRC
## Gets inp from IRC, processes it, and returns the 
def run(inp,sender,channel):

	words = [line.strip() for line in open('mods/items.dic')]
	gift = random.choice(words).upper()

	if ("what do you give a bitch?" in inp or "what do you give dandylion?" in inp):
		return 'GIVE THAT BITCH A ' + gift + '. BITCHES LOVE ' + gift + 'S.'
	else:
		return ""

## Returns a description of the module including the name at the top
def desc():
	return name + ":Tells you what to give a bitch."
