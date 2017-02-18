from circuits.core import Event,handler
from circuits.web.client import Client as WebClient, request as WebRequest, connect as WebConnect  
from circuits.web.websockets import WebSocketClient
from circuits.net.sockets import read,write,connect as WSConnect  
from urlparse import urlparse  
import urllib
import json  

from raceman.lib.rmcomponent import RMComponent




class SignalrReady(Event):
	"""Signalr component has started and ready to connect
		Params:
		- component
	"""
	
class SignalrStart(Event):
	"""Asks Signalr component to connect to the server
		Params:
		URL
		hubs list
	"""

class SignalrStarted(Event):
	"""Sent by Signalr component to inform that it started and ready to serve requests
		Params:
		- component
	"""
	

class SignalrInvoke(Event):
	"""Invokes a method with arguments in hub
		Params:
		- hub
		- method
		- arguments
		
	"""
class SignalrHeartbeat(Event):
	"""Received a heartbeat message
	"""


class SignalrInvokeResult(Event):
	"""Received when server sent a result of the 'send' method
		Params:
		- I,R
	"""

class SignalrInvokeError(Event):
	"""Received when server sent an error message in reply to  the 'send' method
		Params:
		I,E
	"""
	
class SignalrInvokeConfirmation(Event):
	"""Received when server confirmed 'send' method invocation
		Params:
		I
	"""
	
class SignalrGroupAdd(Event):
	"""Received when server sent a group token
		Params:
		G
	"""

class SignalrMessage(Event):
	"""Received when server sent a message
		Params:
		M
	"""
	
class SignalrHubMessage(Event):
	"""Received when server sent a message to the hub
		Params:
		M
	"""
	
class Signalr(RMComponent):  
		channel='signalr'
          
		def __init__(self,useragent,proto='1.5',channel=channel):  
			super(Signalr,self).__init__(channel=channel)
			self._useragent=useragent
			self._proto=proto
			self.change_state('INITIALIZING')
			self._webclient=WebClient(channel='signalr-webclient').register(self)
			self._ws_counter=-1

			
		def get_counter(self):
			self._ws_counter+=1
			return self._ws_counter
			
                  
		@handler("ready",channel='signalr-webclient')  
		def state_initialized(self,arg):  
			self.change_state('READY')
			self.fire(SignalrReady(self))	
			
		@handler("SignalrStart")
		def do_start(self, url, hubs):
			self._hubs=hubs
			self._urlbase=url
			p=urlparse(url)
			self._host=p.hostname
			self._connectionData=urllib.quote(json.dumps([{'Name' : hubname} for hubname in hubs]))  		
			self.change_state('STARTING')		
			_urlpath=url+'/signalr/negotiate?clientProtocol='  + self._proto +\
					'&connectionData=' + self._connectionData
			self.fireEvent(WebRequest(method='GET',path=_urlpath,headers={'User-Agent':self._useragent}),self._webclient)  
          
		@handler("response",channel='signalr-webclient')  
		def control_response(self,resp):  

			if (self._state=='STARTING'):
				data=resp.body.read()
				self._jsondata=json.loads(data)  
				wsurl='ws://'+self._host+self._jsondata['Url'] + \
						'/connect?connectionToken=' + urllib.quote(self._jsondata['ConnectionToken']) + \
						'&connectionData=' + self._connectionData + \
						'&transport=webSockets&clientProtocol=' + self._proto
				self._ws=WebSocketClient(wsurl,channel='ws-internal', wschannel='signalr-websocket',headers={
					'User-Agent': self._useragent,
					'Host': self._host
                }).register(self)  
				
			elif (self._state=='CONTROL_STARTING'):
				self.change_state('STARTED')
				self.fire(SignalrStarted(self))
  
                 
		@handler("ready",channel="ws-internal")  
		def state_starting(self,obj):  
			self.change_state('WEBSOCKET_STARTING')
			self.fireEvent(WSConnect(),self._ws)  
			
		@handler("response",channel="ws-internal")
		def state_ready(self,resp):
			self.change_state('CONTROL_STARTING')
			_urlpath='/signalr/start?'+ \
						'connectionToken=' + urllib.quote(self._jsondata['ConnectionToken']) + \
						'&connectionData=' + self._connectionData + \
						'&transport=webSockets&clientProtocol=' + self._proto
			self.fireEvent(WebRequest(method='GET',path=self._urlbase+_urlpath,headers={'User-Agent':self._useragent,'Host':self._host,'Accept-Encoding': 'identity'}),self._webclient)  
			
			
		@handler("SignalrInvoke")
		def invoke_server(self,hub,method,arguments):
			cntr=self.get_counter()
			jsondata=json.dumps({'I':cntr,'H':hub ,'M':method,'A': arguments})
			self.fire(write(jsondata),'signalr-websocket')
			return cntr
			
		@handler("read",channel="signalr-websocket")
		def ws_read(self,data):

				try:
					js=json.loads(data)
					if (type(js) is dict):
						if (not js):
							self.fire(SignalrHeartbeat())
						else:
							if (js.has_key(u"I")):
								if (js.has_key(u"R")):
									self.fire(SignalrInvokeResult(js[u"I"],js[u"R"]))
								elif (js.has_key(u"E")):
									if (js.has_key(u"H") and js[u"H"]):
										self.fire(SignalrHubError(js[u"I"],js[u"E"],js[u"D"]))
									else:
										self.fire(SignalrInvokeError(js[u"I"],js[u"E"]))
								else:
									self.fire(SignalrInvokeConfirmation(int(js[u"I"])))
							elif (js.has_key(u"C")):
								if (js.has_key(u"G")):
									self.fire(SignalrGroupAdd(js[u"G"]))
								elif (js.has_key(u"M")):
									for m in js[u"M"]:
										self.fire(SignalrMessage(m))
								
				
				except ValueError as e:
					print "Error decoding signalr message",data,e
					return

		@handler("SignalrMessage")
		def on_signalr_message(self,msg):
			self.fire(SignalrHubMessage(msg[u"H"],msg[u"M"],msg[u"A"]))
