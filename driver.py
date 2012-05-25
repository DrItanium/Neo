#!/usr/bin/python2.6

from irc import Irc
from ircLoader import IrcLoader
from optparse import OptionParser

## Command line parser to enable raw output
parser = OptionParser()
parser.add_option("-r","--raw",action="store_true",dest="raw",default=False,help="Print the raw IRC data instead of formatting it.")
(options,args) = parser.parse_args()

datloader = IrcLoader()
irc = Irc(datloader,options)

irc.startIrc()
