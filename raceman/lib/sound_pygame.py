#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import mixer
from os import environ
from raceman.lib.sound_base import *
from raceman.lib.config  import *
import raceman.lib.config as config
from circuits import Component,Event,handler
from StringIO import StringIO
import pdb


class RMSound_Pygame(RMSound):
	
	@handler("RMSoundDriverInit")
	def _on_rmsound_driver_init(self):
		mixer.init(size=RMS_PYGAME_SAMPLESIZE, channels=RMS_PYGAME_SAMPLECHANNELS,frequency=RMS_PYGAME_FREQUENCY)
		mixer.set_num_channels(RMS_NUM_CHANNELS)
		mixer.set_reserved(RMS_RESERVED_CHANNELS)


	@handler("RMSoundDriverPlayFileAsync")		
	def _on_rmsound_driver_play_file_async(self,filename):
		channel=mixer.find_channel()
		sound=mixer.Sound(filename)
		channel.play(sound)


	@handler("RMSoundDriverPlayFileSync")			
	def _on_rm_sound_driver_play_file_sync(self,filename):
		channel=mixer.find_channel()
		sound=mixer.Sound(filename)
		channel.play(sound)
		while channel.get_busy():
			self.flushEvents()


	@handler("RMSoundDriverPlayArraySync")
	def _on_rm_sound_driver_play_array_sync(self,parts):
		channel=mixer.find_channel()
		for f in parts:
			sound=mixer.Sound(f)
			channel.play(sound)
			while channel.get_busy():
				self.flushEvents()


	@handler("RMSoundDriverPlayStreamAsync")
	def _on_rmsound_driver_play_stream_async(self,stream):
		channel=mixer.find_channel()
		SIO=StringIO(stream)
		sound=mixer.Sound(SIO)
		channel.play(sound)


	@handler("RMSoundDriverPlayStreamSync")
	def _on_rmsound_driver_play_stream_async(self,stream):
		channel=mixer.find_channel()
		SIO=StringIO(stream)
		sound=mixer.Sound(SIO)
		channel.play(sound)
		while channel.get_busy():
			self.flushEvents()


	@handler("RMSoundDriverPlayBufferAsync")
	def _on_rmsound_driver_play_buffer_async(self,buffer):
		channel=mixer.find_channel()
		sound=mixer.Sound(buffer)
		channel.play(sound)


	@handler("RMSoundDriverPlayBufferSync")
	def _on_rmsound_driver_play_buffer_async(self,buffer):
		channel=mixer.find_channel()
		sound=mixer.Sound(buffer)
		channel.play(sound)
		while channel.get_busy():
			self.flushEvents()





	@handler("RMSoundDriverPlayBGM")
	def _on_rmsound_driver_play_bgm(self,filename):
		mixer.music.load(filename)
		mixer.music.set_volume(config.profile['RMS_BGM_VOLUME'])		
		mixer.music.play(-1)


	@handler("RMSoundDriverStopBGM")
	def _on_rmsound_driver_stop_bgm(self):
		mixer.music.fadeout(2000)


	@handler("RMSoundDriverStopAll")
	def _on_rmsound_driver_stop_all(self):
		mixer.fadeout(1000)
		mixer.stop()
		