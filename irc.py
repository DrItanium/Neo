import socket, string, random, time, ConfigParser
from threading import Timer
from neoLoader import NeoLoader
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
	delayTime 	= config.get('Settings', 'delayTime')
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

	#connect to the server
	def irc_conn(self):
		self.irc.connect((self.server,self.port))

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
		if ( message[0] == '!' and sender == self.owner ):
			self.admin(channel,message)

		## Run the input through each of the imported modules
		else:
			if(not self.silent):
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
				if (self.verbose):
					self.saychan("Error: "+str(sys.exc_info()[1]),channel)
				else:
					self.saychan("I accidently the entire.",channel)

				traceback.print_exc(file = sys.stderr)

		elif (message.split()[0] == "!unload"):
			try:
				self.load.unload(message.split()[1])
				self.saychan("Unloaded " + message.split()[1] + "module." ,channel)
			except:
				self.saychan("I accidently the entire." ,channel)
				traceback.print_exc(file = sys.stderr)

		elif (message.split()[0] == "!mods"):
			self.saychan(str(self.load.listMods()),channel)

		elif (message.split()[0] == "!desc"):
			try:
				self.saychan(str(self.load.desc(message.split()[1])),channel)
			except:
				self.saychan("I accidently the entire." ,channel)
				traceback.print_exc(file = sys.stderr)

		elif (message.split()[0] == "!silent"):
			self.silent = True

		elif (message.split()[0] == "!unsilent"):
			self.silent = False

		elif (message.split()[0] == "!join"):
			self.join(message.split()[1])

		elif (message.split()[0] == "!part"):
			self.part(message.split()[1])

		elif (message.split()[0] == "!verbose"):
			print "Verbose:",self.delay
			if (self.verbose):
				self.verbose = False
			else:
				self.verbose = True
			print "Verbose:",self.verbose


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
