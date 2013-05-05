from circuits import handler,Component,Event, Debugger,future
from circuits.io.file import File,TIMEOUT
from circuits.net.protocols import LP
from collections import deque
import re
import sys


TIMEOUT=0.00001
"""AGI script execute, collect startup variables"""
ST_STARTUP=1 
"""Set command, wait for response"""
ST_BUSY=2 
"""Multiline response string received. Collect until end"""
ST_COLLECT=3 
"""Ready to send commands"""
ST_READY=4 

# from Pyst
AGIARG=re.compile(r'^(\w+): (.*)$')
AGIRESPONSE  = re.compile(r'^(?P<answer>\d{3})([- ])(.*)$')
AGIKV = re.compile(r'result=(?P<result>\S+)(?:\s*\((?P<extra>.*)\))*')

class AGIResult(Event):
    """AGI Result string"""

class AGIReady(Event):
    """Fired when AGI manager is ready to process nect command"""

class AGICommand(Event):
    """Asks AGI to issue a command """


class AGIStartupComplete(Event):
    """Fired to signal startup procedure end"""


class AGIHangup(Event):
    """Fired when AGI requested hangup (200 result=-1)"""


class AGI(Component):
    def __init__(self,*args,**kwargs):
        super(AGI,self).__init__(*args,**kwargs)
        self._state=ST_STARTUP
        self.Input=File(fd=sys.__stdin__,mode="r", channel="agiinput").register(self)
        self.Output=File(fd=sys.__stdout__,mode="w", channel="agioutput", encoding="utf-8").register(self)
        self.LP=LP(channel="agiinput").register(self)
        self._agi_args={}
        self._response=[]
        self._answer=None

    @handler("line",target="agiinput")
    def line(self,line):
        if self._state==ST_STARTUP:
            """Get args and vars from asterisk at startup"""
            match=AGIARG.match(line)
            if match:
                (name,val)=match.groups()
                self._agi_args[name]=val
            elif line=="":
                self._state=ST_READY
                self.fireEvent(AGIStartupComplete(self._agi_args))
            else:
                raise Exception("AGI: Bad line at startup received:%s" % line)
        elif self._state==ST_COLLECT:
            """This is a command result"""
            self._response.append(line)
            if line[:3]==self._answer:
                self.fireEvent(AGIResult(self._answer,None,"\n".join(self._response)))
                self._response=[]
                self._answer=None
                self._state=ST_READY
                self.fireEvent(AGIReady())
                sys.stderr.write("Debug: COLLECT mode end\n")
        elif self._state==ST_BUSY:
            match=AGIRESPONSE.match(line)
            if match:
                (answer,delim,data)=match.groups()
                self._answer=answer
                if delim=='-':
                    self._response=[line]
                    self._answer=answer
                    self._state=ST_COLLECT
                else:
                    match=AGIKV.match(data)
                    if match:
                        self.fireEvent(AGIResult(self._answer,match.group('result'),match.group('extra')))
                    self._response=[]
                    self._answer=None
                    self._state=ST_READY
                    self.fireEvent(AGIReady())
            else:
                raise Exception("AGI: Bad response received:" % line)

        else:
            raise Exception("AGI: Got response when not in BUSY|COLLECT state (line=%s) (state=%d)\n" % (line, self._state))


    @handler("agiresult")
    def _agiresult(self,answer,result,extra):
        if int(answer)==200 and int(result)==-1:
            self.fireEvent(AGIHangup())


    @handler("agicommand")
    def _agicommand(self,data):
        self._state=ST_BUSY
        self.Output.write(bytearray(data+ "\n",'utf-8'))







class AGI2(Component):
    def __init__(self,*args,**kwargs):
        super(AGI2,self).__init__(*args,**kwargs)
        self._state=ST_STARTUP
        self._agi_args={}

    @handler("agiresult")
    def _agiresult(self,answer,result,extra):
        if int(answer)==200 and int(result)==-1:
            self.fireEvent(AGIHangup())

    @handler("started")
    @future()
    def _started(self,*args,**kwargs):
        self._state=ST_STARTUP
        line=None
        while line<>"\n":
            line=sys.stdin.readline()
            match=AGIARG.match(line)
            if match:
                (name,val)=match.groups()
                self._agi_args[name]=val
            elif line=="\n":
                self._state=ST_READY
                self.fireEvent(AGIStartupComplete(self._agi_args))
            else:
                    raise Exception("AGI: Bad line at startup received:%s" % line)

    @handler("agicommand")
    @future()
    def _agicommand(self,data,*args,**kwargs):
        self._state=ST_BUSY
        sys.stdout.write(bytearray(data+ "\n",'utf-8'))
        sys.stdout.flush()

        while 1:
            line=sys.stdin.readline()


            if self._state==ST_COLLECT:
                """This is a command result"""
                self._response.append(line)
                if line[:3]==self._answer:
                    self.fireEvent(AGIResult(self._answer,None,"\n".join(self._response)))
                    self._response=[]
                    self._answer=None
                    self._state=ST_READY
                    self.fireEvent(AGIReady())
                    break
            elif self._state==ST_BUSY:
                match=AGIRESPONSE.match(line)
                if match:
                    (answer,delim,data)=match.groups()
                    self._answer=answer
                    if delim=='-':
                        self._response=[line]
                        self._answer=answer
                        self._state=ST_COLLECT
                    else:
                        match=AGIKV.match(data)
                        if match:
                            self.fireEvent(AGIResult(self._answer,match.group('result'),match.group('extra')))
                        self._response=[]
                        self._answer=None
                        self._state=ST_READY
                        self.fireEvent(AGIReady())
                        break
                else:
                    raise Exception("AGI: Bad response received:" % line)      

            else:
                raise Exception("AGI: Got response when not in BUSY|COLLECT state (line=%s) (state=%d)\n" % (line, self._state))      

