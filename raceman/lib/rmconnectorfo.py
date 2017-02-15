#!/usr/bin/python  

from circuits import Component,BaseComponent, Debugger,handler,Event,Timer,TimeoutError
from circuits.protocols.websocket import WebSocketCodec
from circuits.web.client import request,Client
from exceptions import ValueError
from raceman.lib.racingtime import RacingTime
from raceman.lib.config import *
from raceman.lib.rminfoevents import *
from raceman.lib.rmconnectorevents import *
import circuits  
from raceman.lib.signalr import *
				
###########################################################################################################				
class FORaceDetectorConnect(Event):
	"""Ask RaceDetector to connect to the current race
	"""				

class FORaceDetectorRediscover(Event):
	"""Ask RaceDetector to discover another race
	"""				


class FORaceDetectorSubscribeTimer(Event):
	""" Timer event
	"""
	
class FORaceDetectorRaceStarted(Event):
	""" Race started signal from Race Detector
	Params:
	- race id
	"""
class FORaceDetectorRaceStopped(Event):
	""" Race stopped signal from Race Detector	
	Params:
	- race id
	"""

class FORaceDetector(FOComponent):

	def __init__(self,*args,**kwargs):
		super(FORaceDetector,self).__init__(*args,**kwargs)
		self.change_state('READY')
		self._webclient=Client(channel='rd-webclient')
		self._webclient.register(self)
		

	@handler("FORaceDetectorConnect","FORaceDetectorRediscover")
	def state_discovering(self):
		self.change_state('DISCOVERING')
		resp = yield self.call(request(\
			method='GET',\
			path='http://club.forzaonline.ru/race/GetLastRaceId',\
			headers={'User-Agent':USERAGENT,'Host':'club.forzaonline.ru'}),self._webclient)
			
		self.change_state('WAITING')
		data=resp.value.body.read()
		js=json.loads(data)
		raceid=js[u'id']
		self.fire(FOSubscribeRace(raceid))
		self._subscribed_race=raceid
		try:
			hb = yield self.wait("FOCommandHB",timeout=50)
			self.change_state('ACTIVE')
			self.fire(FORaceDetectorRaceStarted(self._subscribed_race))
		except TimeoutError:
			self.change_state("TIMEOUT")
			self.fire(FOUnsubscribeRace(raceid))
			self.fire(FORaceDetectorRediscover())
			
	@handler("FOCommandOnlineStatus")
	def state_stopped(self,online,regn,raceid):
		if (online and raceid==self._subscribed_race and self._state=='ACTIVE'):
			self.change_state('STOPPED')
			self.fire(FORaceDetectorRaceStopped(self._subscribed_race))
	
class FOCommand(Event):
	""" FO Command
	Params
	Method
	Time
	isWideSpread
	Command(Method arguments)
	"""
	pass	
	
class FOCommandOnlineStatus(Event):
	""" FO Command "OnlineStatus"
	Params:
		Online
		RegNumber
		RaceId
		
	"""
	pass
	
class FOCommandHB(Event):
	""" FO Command 'hb' (Heartbeat)
	Params:
		Time
	"""	


class FOCommandComp(Event):
	""" FO Command 'Comp'
	Params
	- Comp (comp data)
	"""	
	
class FOCommandSession(Event):
	""" FO Command 'Session'
	Params
	- Session (session data)
	"""	
	
	
class FOSubscribeRace(Event):	
	""" Asks connector to subscribe race
	Params
	- RaceId
	"""
	
class FOUnsubscribeRace(Event):	
	""" Asks connector to unsibscribe race
	Params
	- RaceId
	"""
	
	
class FORaceIsOver(Event):
	""" Signals that race is over
	Params:
	- RaceId
	"""
	
class RMConnectorFO(FOComponent):
	def __init__(self,*args,**kwargs):
		super(RMConnectorFO,self).__init__(channel='connector')
		self.signalr=Signalr(channel='connector').register(self)
		self.racedetector=FORaceDetector(channel='connector').register(self)
		self._hub='RaceHub'
		self._url='http://club.forzaonline.ru'


	@handler("FOSubscribeRace",channel='connector')
	def on_subscribe_race(self,raceid):
		return self.fire(SignalrInvoke(self._hub,'SubscribeRace',[raceid]))
		
	@handler("FOUnsubscribeRace",channel='connector')
	def on_unsubscribe_race(self,raceid):
		return self.fire(SignalrInvoke(self._hub,'UnsubscribeRace',[raceid]))
		

	@handler("SignalrReady",channel='connector')
	def do_ready(self,comp):
		self.fire(RMConnectorReady())
		
	@handler("RMConnectorStart")
	def on_rm_connector_start(self):
		self.fire(SignalrStart(self._url,[self._hub]),self.signalr)
				
	@handler("SignalrStarted",channel='connector')
	def do_started(self,comp):
		self.fire(RMConnectorStarted())
		self.fire(RMInfoConnected(),'infoevents')
		self.fire(FORaceDetectorConnect())

	@handler("FORaceDetectorRaceStarted")
	def on_fo_race_detector_race_started(self,raceid):
		self.fire(RMInfoRaceGoing(),'infoevents')
		
	@handler("FORaceDetectorRaceStopped")	
	def on_fo_race_detector_race_stopped(self):
		self.fire(RMInfoRaceFinish(),'infoevents')

	@handler("RMConnectorConfigure")
	def on_rm_connector_configure(self,config,kartclass,kartid):
		self._config=config
		self._kartclass=kartclass
		self._target=kartid



	@handler("FOCommandComp")
	def on_fo_command_comp(self,comp):
		if int(comp[u'nn'])==self._target:
			ll=RacingTime.fromint(int(comp[u'll']))
			pt=RacingTime.fromint(int(comp[u'pt']))
			bl=RacingTime.fromint(int(comp[u'bl']))
			self.fire(RMInfoKartLap(self._target,ll,pt),'infoevents')
			if ll>bl:
				self.fire(RMInfoKartLapBetter(),'infoevents')
			elif ll<bl:
				self.fire(RMInfoKartLapWorse(),'infoevents')



	@handler("SignalrHubMessage",channel='connector')
	def on_signalr_hub_message(self,H,M,A):
		if (H==self._hub):
			if (M==u'newCommand'):
				for c in A:
					#sWideSpread': True, u'Command': {u'isOnline': False, u'RegNumber': None, u'RaceId': u'551263f0-4431-4211-af92-8fc93ec8f796'}, u'Method': u'OnlineStatus', u'Time': 631000} )>

					self.fire(FOCommand(c[u'Method'],c[u'Time'],c[u'IsWideSpread'],c[u'Command']))
			else:
				raise ValueError("Unknown command %s" % [M])
		else:
			raise ValueError("Unknown hub name %s" % [H])
			
			
	@handler("FOCommand",channel='connector')
	def on_fo_command(self,method,time,iswidespread,command):
		if (method==u'OnlineStatus'):
			self.fire(FOCommandOnlineStatus(command[u'isOnline'],command[u'RegNumber'],command[u'RaceId']))
		elif (method==u'hb'):
			self.fire(FOCommandHB(time))
		elif (method==u'Comp'):
			self.fire(FOCommandComp(command))
		elif (method==u'Session'):
			self.fire(FOCommandSession(command))
		else:
			raise ValueError("Unknown FO Command %s",[method])
