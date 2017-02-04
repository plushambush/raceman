#coding=utf-8
import win32com.client
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

SPF_IS_XML=8
SAFT16kHz16BitMono=18
SAFT22kHz16BitMono=22
SAFT8kHz16BitMono = 6
ServerHost='0.0.0.0'
ServerPort=40040

class RMSAPIServer(LineReceiver):
	def __init__(self):
		print "Connection received"
		self.SAPI=win32com.client.Dispatch("SAPI.SpVoice")
		self.Stream=win32com.client.Dispatch("SAPI.SpMemoryStream")
		format=win32com.client.Dispatch("SAPI.SpAudioFormat")
		format.Type=SAFT8kHz16BitMono
		self.Stream.Format=format
		self.SAPI.AudioOutputStream=self.Stream
			
	def lineReceived(self, line):
		try:
			encline=line.decode('cp1251').encode('cp866')
		except UnicodeEncodeError:
			encline=line
		print "Speak request:%s" % encline
		self.SAPI.Speak(line, SPF_IS_XML)
		data=str(self.Stream.GetData())
		self.transport.write(data)
		self.transport.loseConnection()

class RMSAPIFactory(Factory):
	def buildProtocol(self, addr):
		return RMSAPIServer()

print "Started SAPI server"
reactor.listenTCP(ServerPort, RMSAPIFactory())
reactor.run()
