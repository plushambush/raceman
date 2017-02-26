#!/usr/bin/python -u
from raceman.lib.tts_sapi import *
from raceman.lib.sound_pygame import *
from raceman.lib.sound_base import *
from raceman.lib.config import *
from circuits.protocols import Line as LP
from circuits.io.file import File
from circuits import Debugger,Component
from sys import __stdin__
class VoiceManager(Component):
	@handler("line")
	def on_line(self,line):
		self.fire(RMSoundSayMessage(line.decode("utf-8")))
		
	@handler("eof")
	def on_eof(self):
		self.stop()
	


(VoiceManager()+RMSound_Pygame() + 
RMTTS_SAPI() + 
LP() +
File(filename=sys.__stdin__,mode="r", channel="stdin", encoding='utf-8')).run()
