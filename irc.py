import socket, string, random, time, ConfigParser
from threading import Timer
from loader import Loader

class Irc:
	#Parse Configuration File
	config = ConfigParser.RawConfigParser()
	config.read('config.cfg')

	#Obtain Configuration Vaules
	port 		= config.get('Settings', 'port')
	nick 		= config.get('Settings', 'nick')
	username 		= config.get('Settings', 'username')
	password 		= config.get('Settings', 'password')
	realname 		= config.get('Settings', 'realname')
	hostname 		= config.get('Settings', 'hostname')
	servername 	= config.get('Settings', 'servername')
	channel 		= config.get('Settings', 'channel')
	owner 		= config.get('Settings', 'owner')
	silent 		= config.get('Settings', 'silent')
	delay 		= config.get('Settings', 'delay')
	delayTime 	= config.get('Settings', 'delayTime')

	#setup irc socket
	irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	#init the class
	def __init__(self, datloader):
		self.load = datloader
		
		## Load Default Modules, Maybe put this into a list?
		self.load.loadMod('commands')
		self.load.loadMod('remember')

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

	#say into a channel
	def saychan(self,text,channel):
		self.send('PRIVMSG ' + channel + ' :' + str(text) + '\r\n')

	#process the irc messages
	def msgp(self, sender,destination,message):
		print '(', destination, ')', '[',  sender , ']', ':', message
		
		if message.find(self.nick+':') != -1 and len(message.split()) > 1:

			if ( message.split()[1] == 'loader' and sender == owner ):
				if ( message.split()[2] == 'load' ):
					self.saychan(self.load.loadMod(message.split()[3]),channel)
				elif ( message.split()[2] == 'reload' ):
					self.saychan(self.load.reloadMod(message.split()[3]),channel)
				elif ( message.split()[2] == 'run' ):
					self.saychan(self.load.runMethod(message.split()[3],message.split()[4],None),channel)
				elif ( message.split()[2] == 'showmethods' ):
					self.saychan(self.load.showMethods(''),channel)

			elif ( self.load.modules.has_key(message.split()[1]) and sender == owner ):
				if ( message.split()[2] != None ):
					self.saychan(self.load.runMethod(message.split()[1],message.split()[2],message.split()[3:len(message.split())]),channel)
				else:
					self.saychan(self.load.runMethod(message.split()[1],message.split()[2],None),channel)
					## self.saychan("yeah yeah I know some of these words",channel)
				
			else:
				self.saychan(message.split()[1],channel)


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
				self.load.runMethod('remember','memory',message)
				self.msgp(sender,destination,message)
