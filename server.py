#!/usr/bin/python

from socket import *
from  ConfigParser import *
import sys
import argparse

class serverConf:
	port = 17
	host = ""
	quotefile = ""

def initConfig(filename):

	
	config = ConfigParser()

	config.add_section('Server')
	config.set('Server', 'host', '')
	config.set('Server', 'port', '17')

	config.add_section('Quotes')
	config.set('Quotes', 'file', 'quotes.txt')

	
	

	with open(filename, 'w') as configfile:
		config.write(configfile)


def parseConfig(filename):
	
	configOptions = serverConf()

	
	try:
		config = ConfigParser()
		config.read(filename)

	

		configOptions.port = config.getint('Server', 'port')
		configOptions.host = config.get('Server', 'host')
		configOptions.quoteFile = config.get('Quotes', 'file')

	except KeyboardInterrupt:
		raise

	except:
		print "[Info] Configuration file \'" + filename + "\' does not exist. Creating one with the default values"

		configOptions.port = 17
		configOptions.host = ""
		configOptions.quoteFile = "quotes.txt"

		try:
			initConfig(filename)

		except KeyboardInterrupt:
			raise

		except:

			print "[Fatal] Unable to create configuration file \'" + filename + "\'. This program must exit"
			sys.exit()

		

	

	print "[Info] Read configuration options"

	return configOptions

def doInitMessage():

	print "Quote Of The Day Server"
	print "-----------------------"
	print "Version 1.0 By Ian Duncan"
	print ""

def Start(args):

	filename = "qotdconf.ini"
	configOptions = parseConfig(filename)

	doInitMessage()

	if configOptions.host == '':
		print "[Info] Will start server at: " + "*"  + ":" + str(configOptions.port)
	else:
		print "[Info] Will start server at: " + configOptions.host + ":" + str(configOptions.port)

parser = argparse.ArgumentParser(description='A quote of the day server.')
parser.add_argument('--port', dest='accumulate', action='store_const', const=int, default=max, help='the port the server broadcasts on')
parser.add_argument('--host', dest='accumulate', action='store_const', const=str, default=max, help='the ip address or domain name the server broadcasts on')
parser.add_argument('--quotes', dest='accumulate', action='store_const', const=str, default=max, help='the file that stores the quotes')
parser.add_argument('--config', dest='accumulate', action='store_const', const=str, default=max, help='specify a custom configuration file')

args = parser.parse_args()

Start(args)


	

		

	
