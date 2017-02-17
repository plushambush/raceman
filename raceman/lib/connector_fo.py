#!/usr/bin/python  

from circuits import Component,BaseComponent, Debugger,handler,Event,Timer,TimeoutError
from circuits.protocols.websocket import WebSocketCodec
from circuits.web.client import request,Client
from exceptions import ValueError
from raceman.lib.racingtime import RacingTime
from raceman.lib.config import *
from raceman.lib.events_info import *
from raceman.lib.events_connector import *
import circuits  
from raceman.lib.signalr import *
from raceman.lib.rmcomponent import RMComponent
import sys
import pdb
				
###########################################################################################################				
class FORaceDetectorConnect(Event):
	"""Ask RaceDetector to connect to the current race
	"""				

class FORaceDetectorRediscover(Event):
	"""Ask RaceDetector to discover another race
	"""				


class FORaceDetectorSubscribeTimer(Event):
	""" Timer event (subscribe)
	"""

class FORaceDetectorHBTimer(Event):
	""" Timer event (heartbeats)
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

class FORaceDetectorRaceNoData(Event):
	""" Race stopped sending heartbeats	
	Params:
	- race id
	"""

class FORaceDetectorRaceDataBack(Event):
	""" Race restored heartbeats	
	Params:
	- race id
	"""

	
class FORaceDetectorReady(Event):
	""" Ready and waiting for race
	"""

class FORaceDetectorUpdateRaceData(Event):
	"""Received Race start data
	Params:
		data
	"""


class FORaceDetector(RMComponent):

	def __init__(self,*args,**kwargs):
		super(FORaceDetector,self).__init__(*args,**kwargs)
		self.change_state('READY')
		self._webclient=WebClient(channel='rd-webclient')
		self._webclient.register(self)
		self._subscribed_race=None
		self._subscribe_timer=None
		self._hb_timer=None
		self.fire(FORaceDetectorReady())

	def make_web_request(self,url):
		self.fire(WebRequest(\
			method='GET',\
			path='http://club.forzaonline.ru' + url,\
			headers={'User-Agent':USERAGENT,'Host':'club.forzaonline.ru'}),self._webclient)		

	@handler("FORaceDetectorConnect","FORaceDetectorRediscover")
	def state_discovering(self):
		self.change_state('DISCOVERING')
		self.make_web_request(u'/race/GetLastRaceId')
		
	@handler("response",channel='rd-webclient')
	def state_subscribing(self,resp):
		if self._state=='DISCOVERING':
			self.change_state('WAITING')
			data=resp.body.read()
			js=json.loads(data)
			raceid=js[u'id']
			self.fire(FOSubscribeRace(raceid))
			self._subscribed_race=raceid.encode('windows-1251')
			self._subscribe_timer=Timer(FO_RACEDETECTOR_SUBSCRIBE_TIMER,FORaceDetectorSubscribeTimer()).register(self)
		elif self._state=='ACTIVE':
			data=resp.body.read()
			js=json.loads(data)
			self.fire(FORaceDetectorUpdateRaceData(js))
		
	@handler("FOCommandHB")
	def state_waiting(self,time):
		if (self._state=='WAITING'):
			self.change_state('ACTIVE')
			self._subscribe_timer.unregister()
			self.fire(FORaceDetectorRaceStarted(self._subscribed_race))
			self._hb_timer=Timer(FO_RACEDETECTOR_HB_TIMER,FORaceDetectorHBTimer()).register(self)
			self.make_web_request('/race/GetRaceStartData?raceid=%s' % self._subscribed_race)
		elif (self._state=='ACTIVE'):
			self._hb_timer.reset()
		elif (self._state=='NODATA'):
			self.change_state('ACTIVE')
			self._hb_timer=Timer(FO_RACEDETECTOR_HB_TIMER,FORaceDetectorHBTimer()).register(self)
			self.fire(FORaceDetectorRaceDataBack(self._subscribed_race))
			
			
	@handler("FORaceDetectorHBTimer")
	def on_hb_timer(self):
		if self._state=='ACTIVE':
			self.change_state('NODATA')
			self._hb_timer.unregister()
			self.fire(FORaceDetectorRaceNoData(self._subscribed_race))
			
	@handler("FORaceDetectorSubscribeTimer")
	def state_changed(self):
		if (self._state=='WAITING'):
			self.change_state('WRONG')
			self._subscribe_timer.unregister()
			self.fire(FOUnsubscribeRace(self._subscribed_race))
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
	
class RMConnectorFO(RMComponent):
	def __init__(self,*args,**kwargs):
		super(RMConnectorFO,self).__init__(channel='connector')
		self.signalr=Signalr(channel='connector').register(self)
		self.racedetector=FORaceDetector(channel='connector').register(self)
		self._hub='RaceHub'
		self._url='http://club.forzaonline.ru'
		self._bbl=sys.maxint
		self._target=None
		self._rival=None


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
		self.fire(RMConnectorStarted())		
				
	@handler("SignalrStarted",channel='connector')
	def do_started(self,comp):
		self.fire(RMConnectorConnected(),'infoevents')
		self.fire(RMInfoRaceWaiting(),'infoevents')		
		self.fire(FORaceDetectorConnect())

	@handler("FORaceDetectorRaceStarted")
	def on_fo_race_detector_race_started(self,raceid):
		self.fire(RMInfoRaceStarted(raceid),'infoevents')
		
	@handler("FORaceDetectorRaceStopped")	
	def on_fo_race_detector_race_stopped(self,raceid):
		self.fire(RMInfoRaceStopped(),'infoevents')
		
		
	@handler("FORaceDetectorUpdateRaceData")
	def on_update_race_data(self,data):
		self._racedata=data
		self.update_bl(data)

	@handler("RMConnectorConfigure")
	def on_rm_connector_configure(self,config,kartclass,kartid,rival=None):
		self._config=config
		self._kartclass=kartclass
		self._target=int(kartid)
		if rival:
			self._rival=int(rival)



	@handler("SignalrHubMessage",channel='connector')
	def on_signalr_hub_message(self,H,M,A):
		if (H==self._hub):
			if (M==u'newCommand'):
				for c in A:
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



	@handler("FOCommandHB")
	def on_fo_command_hb(self,time):
		self.fire(RMInfoRaceHeartBeat(RacingTime.fromint(time)),'infoevents')

	@handler("FOCommandComp",channel='connector')
	def on_fo_command_comp(self,comp):
		nn=int(comp[u'nn'])
		is_target=( nn==self._target )
		is_rival=( nn==self._rival )
		ll=RacingTime.fromint(int(comp[u'll']))
		pt=RacingTime.fromint(int(comp[u'pt']))
		bl=RacingTime.fromint(int(comp[u'bl']))
		al=RacingTime.fromint(int(comp[u'cs'][u'al']))
		self.fire(RMInfoKartLap(nn,is_target,is_rival,ll,bl,al,self._bbl,pt),'infoevents')
		bbl=int(comp[u'll'])
		if bbl<self._bbl and bbl<>0:
			self._bbl=bbl

	def update_bl(self,data):
		pdb.set_trace()
		for lap in data[u'lastLaps']:
			bl=int(lap[u'lt'])
			if bl < self._bbl:
				self._bbl=bl
			
