#!/usr/bin/python

#    Quote Of The Day Server Code
#    Copyright (C) 2013  Ian Duncan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from socket import *
from  ConfigParser import *
import sys
from optparse import OptionParser
import random
import errno

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


def parseConfig(filename, createIfNotExist=True):
	
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
	
		if createIfNotExist == False:

			print "[Fatal] Configuration file \'" + filename + "\' does not exist. This program must exit."
			sys.exit()
			
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

def randomLine(filename):
#   #"Retrieve a  random line from a file, reading through the file once"
        fh = open(filename, "r")
        lineNum = 0
        it = ''

        while 1:
                aLine = fh.readline()
                lineNum = lineNum + 1
                if aLine != "":
                        #
                        # How likely is it that this is the last line of the file ? 
                        if random.uniform(0,lineNum)<1:
                                it = aLine
                else:
                        break
        nmsg=it
        return nmsg
        #this is suposed to be a var pull = randomLine(filename)

def doCheckQuotesFile(quotesFilename):
	
	try:
	
		with open(quotesFilename): pass

		print "[Info] Discovered file containing quotes \'" + quotesFilename + "\'"

	except IOError:

		print "[Fatal] Unable to read quotes file \'" + quotesFilename + "\'. This program must exit"
		sys.exit()

def Start(customFilename):

	filename = "qotdconf.ini"

	doInitMessage()

	if customFilename != None:

		filename = customFilename
		print "[Info] A custom configuration file was specified: " + customFilename
		configOptions = parseConfig(filename, False)

	else:

		configOptions = parseConfig(filename)

	

	if configOptions.host == '':
		print "[Info] Will start server at: " + "*"  + ":" + str(configOptions.port)
	else:
		print "[Info] Will start server at: " + configOptions.host + ":" + str(configOptions.port)

	doCheckQuotesFile(configOptions.quoteFile)

	try:
		s = socket(AF_INET, SOCK_STREAM)
		s.bind ( (configOptions.host, configOptions.port) )
		s.listen (5)

		print "[Info] The server is now broadcasting"

		while 1:
    			connection, address = s.accept()
    			print("[Info] Accepted Connection from " +  str(address) + "!")
    			
    			connection.send(randomLine(configOptions.quoteFile) + "\n")

    			connection.close()

	except KeyboardInterrupt as e:
		raise

	except:
		print "[Fatal] There was a problem. This program must exit"
		sys.exit()

	
	
def printLicense(option,opt,value,parser):


	print "Quote Of The Day Server"
	print "-----------------------"
	print ""
	print "This program is free software: you can redistribute it and/or modify"
 	
	print "it under the terms of the GNU General Public License as published by"
	
	print "the Free Software Foundation, either version 2 of the License, or"
	
	print "(at your option) any later version."
	
	print ""

	print "This program is distributed in the hope that it will be useful,"
	
	print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
	
	print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
	
	print "GNU General Public License for more details."

	print ""

	print "You should have received a copy of the GNU General Public License"

	print "along with this program.  If not, see <http://www.gnu.org/licenses/>."

	sys.exit()
	

parser = OptionParser(description="A quote of the day server.", version="Quote Of The Day Server\n\nVersion 1.0 By Ian Duncan", )
parser.add_option("-c", "--config", dest="config", help="specify the path to a custom configuration file",action="store",type="string")
parser.add_option("-l", "--license", action="callback", callback=printLicense, help="Displays licensing information")

(options,args) = parser.parse_args()

Start(options.config)


	

		

	
