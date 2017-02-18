from circuits import handler,Component,Event
import socket
from raceman.lib.config_global import *
from raceman.lib.rmsound_base import *
from raceman.lib.rmtts_base import *

class RMTTS_Festival(RMTTS):
	@handler("rmttsconvert_message")
	def rmtts_festival_convert_message(self,message,rmprio=RM_PRIO_NORMAL):
		sock=socket.socket()
		sock.connect((TTS_FESTIVAL_SERVER_HOST,TTS_FESTIVAL_SERVER_PORT))
		sock.send((TTS_FESTIVAL_COMMAND % message).encode('utf-8'))

		msg=''
		while True:		
			data=sock.recv(TTS_FESTIVAL_BUFFER_SIZE)
			if data<>'':
				msg=msg+data
			else:
				break
		sock.close()
		self.fireEvent(RMSoundPlayStream(bytearray(msg[3:-61]),rmprio))  # ABSOLUTELY DIRTY HACKY (SHAME!)