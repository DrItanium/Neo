#!/usr/bin/python2.6

from irc import Irc
from ircLoader import IrcLoader

datloader = IrcLoader()
irc = Irc(datloader)

irc.startIrc()
