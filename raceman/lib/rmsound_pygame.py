#!/usr/bin/python
# -*- coding: utf-8 -*-
from pygame import mixer
from os import environ
from raceman.lib.rmsound_base import *
from raceman.lib.config import *
from circuits import Component,Event,handler
from StringIO import StringIO



class RMSound_Pygame(RMSound):
	
	@handler("rmsound_driver_init")
	def _on_rmsound_driver_init(self):
		mixer.init(size=RMS_PYGAME_SAMPLESIZE, channels=RMS_PYGAME_SAMPLECHANNELS,frequency=RMS_PYGAME_FREQUENCY)
		mixer.set_num_channels(RMS_NUM_CHANNELS)
		mixer.set_reserved(RMS_RESERVED_CHANNELS)


	@handler("rmsound_driver_play_file_async")		
	def _on_rmsound_driver_play_file_async(self,filename):
		channel=mixer.find_channel()
		sound=mixer.Sound(filename)
		channel.play(sound)


	@handler("rmsound_driver_play_file_sync")			
	def _on_rm_sound_driver_play_file_sync(self,filename):
		channel=mixer.find_channel()
		sound=mixer.Sound(filename)
		channel.play(sound)
		while channel.get_busy():
			self.flushEvents()


	@handler("rmsound_driver_play_stream_async")
	def _on_rmsound_driver_play_stream_async(self,stream):
		channel=mixer.find_channel()
		SIO=StringIO(stream)
		sound=mixer.Sound(SIO)
		channel.play(sound)


	@handler("rmsound_driver_play_stream_sync")
	def _on_rmsound_driver_play_stream_async(self,stream):
		channel=mixer.find_channel()
		SIO=StringIO(stream)
		sound=mixer.Sound(SIO)
		channel.play(sound)
		while channel.get_busy():
			self.flushEvents()


	@handler("rmsound_driver_play_buffer_async")
	def _on_rmsound_driver_play_buffer_async(self,buffer):
		channel=mixer.find_channel()
		sound=mixer.Sound(buffer)
		channel.play(sound)


	@handler("rmsound_driver_play_buffer_sync")
	def _on_rmsound_driver_play_buffer_async(self,buffer):
		channel=mixer.find_channel()
		sound=mixer.Sound(buffer)
		channel.play(sound)
		while channel.get_busy():
			self.flushEvents()





	@handler("rmsound_driver_play_bgm")
	def _on_rmsound_driver_play_bgm(self,filename):
		mixer.music.load(filename)
		mixer.music.set_volume(RMS_BGM_VOLUME)		
		mixer.music.play(-1)


	@handler("rmsound_driver_stop_bgm")
	def _on_rmsound_driver_stop_bgm(self):
		mixer.music.fadeout(2000)


	@handler("rmsound_driver_stop_all")
	def _on_rmsound_driver_stop_all(self):
		mixer.fadeout(1000)
		mixer.stop()
		