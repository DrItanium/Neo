import socket, string, random, time
from threading import Timer

server = 'irc.freenode.net'
port = 6667
nick = 'girldius'
username = 'girldius'
password = None
realname = 'gradiusbot'
hostname = 'gibson'
servername = 'gibson'
channel = '#testgradius'
owner = 'gradius'
silent = False
delay = False
delayTime = 5
irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect to the server
def irc_conn():
	irc.connect((server,port))

#send raw data through the socket created
def send(cmd):
	irc.send(cmd + '\n')

#send login data
def login(nick):
	send("USER %s %s %s %s" % (username,hostname,servername,realname))
	send("NICK " + nick)

#join a channel
def join(channel):
	send("JOIN %s" % channel)

#say into a channel
def saychan(text,channel):
	send('PRIVMSG ' + channel + ' :' + str(text) + '\r\n')

#process the irc messages
def msgp(sender,destination,message):
	print '(', destination, ')', '[',  sender , ']', ':', message
	
	if message.find(nick+':') != -1 and len(message.split()) > 1:
		saychan('Your dumb ass told me to ' + message.split(':')[1], '#testgradius')
		#self.saychan(self.comm.get(message.split(':')[1], sender, destination),destination)

def startIrc():
	
	irc_conn()
	login(nick)
	join(channel)

	while(1):
		data = irc.recv(4096)
		if data.find('PING :') != -1 and data.find('PRIVMSG') == -1:
			print 'I sent a ping with data: ' + data
			send('PONG :' + data.split()[1] + '\r\n')
			#saychan('I sent a pong with data: ' + data, '#testgradius')

		elif data.find('PRIVMSG') != -1:
			sender = data.split ( '!' ) [ 0 ].replace ( ':', '' )
			message = ':'.join ( data.split ( ':' ) [ 2: ] )
			destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]
			msgp(sender,destination,message)
