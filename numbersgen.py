#!/usr/bin/python
# -*- coding=utf-8 -*-
from circuits import Debugger,Component,handler
from raceman.lib.tts_base import RMTTSConvertMessage
from raceman.lib.tts_sapi import RMTTS_SAPI
from raceman.lib.numberspell import *
import pdb
import sys

OUTDIR='./sounds_tts/new/'


def full_name(name,ext):
	return OUTDIR+name+'.'+ext
	
def write_sound(name,data):
	f=open(full_name(name,'raw'),'w')
	f.write(data)
	f.close

class NumberGen(Component):
	def __init__(self,*args,**kwargs):
		super(NumberGen,self).__init__(*args,**kwargs)
		self.tts=RMTTS_SAPI().register(self)
	
	@handler("registered")
	def on_started(self,obj,parent):
		global OUTDIR
		OUTDIR=sys.argv[1]
		start=int(sys.argv[2])
		stop=int(sys.argv[3])
		intonations=['preup','down']
		genders={'m':[0,'LAP'],'f':[1,'SECOND']}
		if obj==self.tts and parent==self:
			for inton in intonations:
				for g in genders.keys():
					for i in range(start,stop+1):
						if inton=='preup':
							s=spell(i, genders[g][1])
							result=self.fire(RMTTSConvertMessage(" ".join(s[:-1])+', '+s[-1]))
						else:
							(r,n)=spell1000(i,genders[g][0])
							result=self.fire(RMTTSConvertMessage(u" ".join(r)))
						yield result
						write_sound("%d-%s-%s"%(i,g,inton),bytearray(result))
		self.stop()
			
			
			
(NumberGen()+Debugger(IgnoreEvents=['RMSoundPlayBuffer'])).run()