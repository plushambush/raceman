from pygame import mixer
from os import environ
from circuits.core import Component,handler

RMS_CHANNEL_BGM=0
RMS_CHANNEL_TICKER=1
RMS_CHANNEL_SYSTEM=2
RMS_CHANNEL_TARGET=3
RMS_CHANNEL_OTHER=4
RMS_CHANNELS=RMS_CHANNEL_OTHER

class RMSound(Component):
	@handler("agistartupcomplete")
	def _agistartupcomplete(self,_agi_args,*args,**kwargs):
		environ['SDL_AUDIODRIVER']='alsa'
		environ['AUDIODEV']='raceman_jack'
		environ['RACEMAN_JACK_PORT']=_agi_args['agi_channel']+':input'
	
		mixer.init(frequency=8000,size=-16,channels=1)
		mixer.set_num_channels(RMS_CHANNELS)

