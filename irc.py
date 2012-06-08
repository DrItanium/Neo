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
	def __init__(self, datloader,options):
		## These are crucial modules that you need
		coreDir = "mods/core/"
		defaultModules = []
		self.load = datloader
		self.ircRaw = options.raw

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

	#process the PMs
	def pmproc(self,sender,message):
		self.msgp(sender,sender,message,True)

	#process the irc messages
	def msgp(self, sender,channel,message,isPM):
		if (not self.ircRaw):
			print '[', channel, ']', sender ,':', message

		## Check for Admin commands, need to be run here.
		if ( message[0] == '!' and sender in self.owner.split(',') ):
			self.admin(channel,message)

		## Run the input through each of the imported modules
		else:
			if(not self.silent and not self.delay and self.silentChan.count(channel) == 0):

				for mod in self.load.listMods():
					try:
						ans = self.load.run(mod,message,sender,channel)
						if (ans != ""):
							self.saychan(ans,channel)

							## Set the timer that resets the delay from true to false
							## Don't delay in PMs
							if (not isPM):
								self.delay = True
								t = Timer(self.delayTime,self.delaySet)
								t.start()
								print "Delayed:",self.delayTime

					except:
						self.saychan("Hey something's broken in "+str(mod) ,channel)
						traceback.print_exc(file = sys.stderr)

	## Admin ! commands
	def admin(self,channel,message):
		split = message.split()
		cmd = split[0]
		arg = ""
		if ( len(split) > 1 ):
			arg = split[1]
		if (cmd == "!load"):
			try:
				self.load.load(arg)
				self.saychan("Loaded " + arg + " module." ,channel)
			except:
				self.reportError(channel)

		elif (cmd == "!unload"):
			try:
				self.load.unload(arg)
				self.saychan("Unloaded " + arg + "module." ,channel)
			except:
				self.reportError(channel)

		elif (cmd == "!mods"):
			ans = ""
			try:
				if ( arg == "running" ):
					self.saychan(str(self.load.listMods()),channel)
				elif ( arg == "all" ):
					for infile in glob.glob( os.path.join('mods/', '*.py') ):
						ans += str(infile) + " "
					self.saychan(ans,channel)
				else:
					self.saychan("Silly Bear! I have no idea what you're trying to do to my modules.")
			except:
				self.reportError(channel)

		elif (cmd == "!delay"):
			try:
				self.delayTime = int(arg)
			except:
				self.reportError(channel)

		elif (cmd  == "!desc"):
			try:
				self.saychan(str(self.load.desc(arg),channel)
			except:
				self.reportError(channel)

		elif (cmd == "!silent"):
			try:
				if (arg == "+"):
					try:
						self.silentChan.append(split[2])
					except:
						self.reportError(channel)
						
				elif (arg == "-"):
					try:
						self.silentChan.remove(split[2])
					except:
						self.reportError(channel)

				elif (arg == "clear"):
					try:
						self.silentChan = []
					except:
						self.reportError(channel)
			except:
				if (self.silent == True):
					self.silent = False
					print "Silent:False"
				else:
					self.silent = True
					print "Silent:True"

		elif (cmd == "!join"):
			try:
				self.join(arg)
			except:
				self.reportError(channel)

		elif (cmd == "!part"):
			try:
				self.part(arg)
			except:
				self.reportError(channel)

		elif (cmd == "!verbose"):
			self.verbose = not self.verbose
		elif (cmd == "!uptime"):
			try:
				diff = datetime.now() - self.startTime
				days = diff.days
				hours, remainder = divmod(diff.seconds, 3600)
				minutes, seconds = divmod(remainder, 60)
				ans =  '%s days %s hours %s minutes %s seconds' % (days,hours, minutes, seconds)
				print ans
				self.saychan(ans,channel)
			except:
				self.reportError(channel)

		elif (cmd == "!admin"):
			try:
				if (arg == "+"):
					try:
						self.owner += "," + split[2]
						print "Owner",split[2],"added."
					except:
						self.reportError(channel)
						
				elif (arg == "-"):
					try:
						arg2 = split[2]
						self.owner = self.owner.replace(arg2,'')
						print "Owner",arg2,"removed."
					except:
						self.reportError(channel)

				elif (arg == "default"):
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
				if self.ircRaw:
					print data

				sender = data.split ( '!' ) [ 0 ].replace ( ':', '' )
				message = ':'.join ( data.split ( ':' ) [ 2: ] )
				destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]

				if ( destination == self.nick ):
					self.pmproc(sender,message)

				if (not destination == self.nick):
					self.msgp(sender,destination,message,False)
