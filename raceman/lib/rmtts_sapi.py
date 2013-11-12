from circuits import handler,Component,Event
from circuits.core.futures import future
import socket
from raceman.lib.config import *
from raceman.lib.rmsound_base import *
from raceman.lib.rmtts_base import *
import pdb

class RMTTS_SAPI(RMTTS):
	@handler("rmttsconvert_message")
	@future()
	def rmtts_sapi_convert_message(self,message,rmprio=RM_PRIO_NORMAL):
		sock=socket.socket()
		sock.connect((TTS_SAPI_SERVER_HOST,TTS_SAPI_SERVER_PORT))
#		pdb.set_trace()
		sock.send(("%s\r\n" % message).encode('windows-1251'))

		msg=''
		while True:		
			data=sock.recv(TTS_SAPI_BUFFER_SIZE)
			if data<>'':
				msg=msg+data
			else:
				break
		sock.close()
		self.fireEvent(RMSoundPlayBuffer(bytearray(msg),rmprio))