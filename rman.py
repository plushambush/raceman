#!/usr/bin/python

# 50.56.75.58:50006 - arena


from circuits.io import File
from circuits.io.events import Write
from circuits.net.protocols import LP
from circuits.net.sockets import TCPClient,Connect
from circuits import Component,handler,Debugger

import sys

from raceman.lib.rmstream import RMStream
from raceman.lib.rmdecoder import RMDecoder
from raceman.lib.rmanalyzer import RMAnalyzer,RMAnalyzerTarget
from raceman.lib.rmteller import RMTeller
from raceman.lib.rmagimanager import RMAGIManager,RMAGIHandler
from raceman.lib.rmagi import AGI
from signal import SIGHUP
from exceptions import AttributeError

config={'arena': 
        { 'streamip':'50.56.75.58',
          'streamport':50006,
           'park':
                {'1':
                    {'01':'1','02':'2','03':'3','04':'4','05':'5','06':'6',
                     '07':'7','08':'8','09':'9','10':'10','11':'11','12':'12',
                     '13':'13','14':'14','15':'15','16':'16','17':'17','18':'18',
                     '19':'19','20':'20','21':'21','22':'22','23':'23','24':'24'
                    },
                 '2':
                    {'01':'Sodi 1','02':'Sodi 2','03':'Sodi 3','04':'Sodi4','05':'Sodi 5',
                     '06':'Sodi6','07':'Sodi7','08':'Sodi8','09':'Sodi9','10':'Sodi 10',
                     '11':'Sodi 11','12':'Sodi 12'
                    }
                }
        }
       }

# Where is Sodi10, Sodi13,SOdi14,Sodi15

class Manager(Component):
    """MAIN manager"""
    @handler("agihangup")
    def _agihangup(self):
        self.stop()

    @handler("signal")
    def _signal(self,sig,sigtype):
        if sig==SIGHUP:
            self.stop()

    @handler("agistartupcomplete")
    def _agistartupcomplete(self,agiarg):
#        if hasattr(agiargs,'agi_arg_2'):
        self._agiarg=agiarg
        try:
            self.fireEvent(RMAnalyzerTarget(agiarg['agi_arg_1'],config[agiarg['agi_arg_1']]['park'][agiarg['agi_arg_2']][agiarg['agi_arg_3']]))
            self.fireEvent(Connect(config[agiarg['agi_arg_1']]['streamip'],config[agiarg['agi_arg_1']]['streamport'],channels="rminput"))
        except AttributeError:
            pass

    

(Manager()+
Debugger(file="/var/log/asterisk/demo.log")+
TCPClient(channel='rminput',bufsize=8192)+
#File(filename='stream0.txt',channel='rminput')+
LP(channel='rminput')+
RMStream(channel='rminput')+
RMDecoder()+
RMAnalyzer()+
RMTeller()+
AGI()+
RMAGIManager()+
RMAGIHandler()).run()