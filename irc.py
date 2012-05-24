import socket, string, random, time, ConfigParser
from threading import Timer
from neoLoader import NeoLoader
from datetime import datetime
import os,glob
import traceback,sys

class Irc:
	#Parse Configuration File
	config = ConfigParser.RawConfigParser()
	config.read('config.cfg')

	#Obtain Configuration Vaules
	server		= config.get('Settings', 'server')
	port 		= int(config.get('Settings', 'port'))
	nick 		= config.get('Settings', 'nick')
	username 	= config.get('Settings', 'username')
	password 	= config.get('Settings', 'password')
	realname 	= config.get('Settings', 'realname')
	hostname 	= config.get('Settings', 'hostname')
	servername 	= config.get('Settings', 'servername')
	channel 	= config.get('Settings', 'channel')
	owner 		= config.get('Settings', 'owner')
	silent 		= config.getboolean('Settings', 'silent')
	delay 		= config.getboolean('Settings', 'delay')
	delayTime 	= config.getint('Settings', 'delayTime')
	verbose 	= config.getboolean('Settings', 'verbose')

	#setup irc socket
	irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	#init the class
	def __init__(self, datloader):
		## These are crucial modules that you need
		coreDir = "mods/core/"
		defaultModules = []
		self.load = datloader

		## Load Core Modules Automatically
		for infile in glob.glob( os.path.join(coreDir, '*.py') ):
			print "Loaded " + infile
			self.load.load(infile)

		## Load Default Modules
		for i in defaultModules:
			self.load.load(coreDir + i)

		## Get start time for uptime command
		self.startTime = datetime.now()

		## Channel list, if the chan is in the list, girldius is silent. 
		## Is checked AFTER global silence
		self.silentChan = []

	#connect to the server
	def irc_conn(self):
		self.irc.connect((self.server,self.port))
	
	def delaySet(self):
		self.delay = False

	#send raw data through the socket created
	def send(self,cmd):
		self.irc.send(cmd + '\n')

	#send login data
	def login(self,nick):
		self.send("USER %s %s %s %s" % (self.username,self.hostname,self.servername,self.realname))
		self.send("NICK " + nick)

	#join a channel
	def join(self,channel):
		self.send("JOIN %s" % channel)

	#join a channel
	def part(self,channel):
		self.send("PART %s" % channel)

	#say into a channel
	def saychan(self,text,channel):
		self.send('PRIVMSG ' + channel + ' :' + str(text) + '\r\n')

	#process the irc messages
	def msgp(self, sender,channel,message):
		print '(', channel, ')', '[',  sender , ']', ':', message

		## Check for Admin commands, need to be run here.
		if ( message[0] == '!' and sender in self.owner.split(',') ):
			self.admin(channel,message)

		## Run the input through each of the imported modules
		else:
			if(not self.silent and not self.delay and self.silentChan.count(channel) == 0):
				## Set the timer that resets the delay from true to false
				self.delay = True
				t = Timer(self.delayTime,self.delaySet)
				t.start()

				for mod in self.load.listMods():
					try:
						self.saychan(self.load.run(mod,message,sender),channel)
					except:
						self.saychan("Hey something's broken in "+str(mod) ,channel)
						traceback.print_exc(file = sys.stderr)

	## Admin ! commands
	def admin(self,channel,message):
		if (message.split()[0] == "!load"):
			try:
				self.load.load(message.split()[1])
				self.saychan("Loaded " + message.split()[1] + " module." ,channel)
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!unload"):
			try:
				self.load.unload(message.split()[1])
				self.saychan("Unloaded " + message.split()[1] + "module." ,channel)
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!mods"):
			ans = ""
			try:
				if ( message.split()[1] == "running" ):
					self.saychan(str(self.load.listMods()),channel)
				if ( message.split()[1] == "all" ):
					for infile in glob.glob( os.path.join('mods/', '*.py') ):
						ans += str(infile) + " "
					self.saychan(ans,channel)

			except:
				self.reportError(channel)

		elif (message.split()[0] == "!delay"):
			try:
				self.delayTime = int(message.split()[1])
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!desc"):
			try:
				self.saychan(str(self.load.desc(message.split()[1])),channel)
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!silent"):
			try:
				if (message.split()[1] == "+"):
					try:
						self.silentChan.append(message.split()[2])
					except:
						self.reportError(channel)
						
				elif (message.split()[1] == "-"):
					try:
						self.silentChan.remove(message.split()[2])
					except:
						self.reportError(channel)

				elif (message.split()[1] == "clear"):
					try:
						self.silentChan = []
					except:
						self.reportError(channel)
			except:
				if (self.silent == True):
					self.silent = False
				else:
					self.silent = True

		elif (message.split()[0] == "!join"):
			try:
				self.join(message.split()[1])
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!part"):
			try:
				self.part(message.split()[1])
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!verbose"):
			if (self.verbose):
				self.verbose = False
			else:
				self.verbose = True
		
		elif (message.split()[0] == "!uptime"):
			try:
				diff = datetime.now() - self.startTime
				hours, remainder = divmod(diff.seconds, 3600)
				minutes, seconds = divmod(remainder, 60)
				ans =  '%s hours %s minutes %s seconds' % (hours, minutes, seconds)
				print ans
				self.saychan(ans,channel)
			except:
				self.reportError(channel)

		elif (message.split()[0] == "!admin"):
			try:
				if (message.split()[1] == "+"):
					try:
						self.owner += "," + message.split()[2]
					except:
						self.reportError(channel)
						
				elif (message.split()[1] == "-"):
					try:
						self.owner = self.owner.replace(message.split()[2],'')
					except:
						self.reportError(channel)

				elif (message.split()[1] == "default"):
					try:
						self.owner = self.config.get('Settings', 'owner')
					except:
						self.reportError(channel)
			except:
				self.reportError(channel)

	def reportError(self,channel):
		if (self.verbose):
			self.saychan("Error: "+str(sys.exc_info()[1]),channel)
		else:
			self.saychan("I accidently the entire.",channel)

		traceback.print_exc(file = sys.stderr)

	def startIrc(self):
		
		self.irc_conn()
		self.login(self.nick)
		self.join(self.channel)

		while(1):
			data = self.irc.recv(4096)
			if data.find('PING :') != -1 and data.find('PRIVMSG') == -1:
				print 'I sent a ping with data: ' + data
				self.send('PONG :' + data.split()[1] + '\r\n')
				#saychan('I sent a pong with data: ' + data, '#testgradius')

			elif data.find('PRIVMSG') != -1:
				sender = data.split ( '!' ) [ 0 ].replace ( ':', '' )
				message = ':'.join ( data.split ( ':' ) [ 2: ] )
				destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]
				self.msgp(sender,destination,message)
