#!/usr/bin/python2.6

from irc import Irc
from loader import Loader

datloader = Loader()
irc = Irc(datloader)

irc.startIrc()
