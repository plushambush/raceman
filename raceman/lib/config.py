#coding=utf-8

RMSYSTEM_LOGFILE='/var/log/raceman.log'

#RMSound configuration 
RMS_SOUND_DIR='/home/ricochet/Projects/Programming/raceman/sounds/'
RMS_SOUND_THEME='.'

RMS_CHANNEL_BGM=0
RMS_CHANNEL_TICKER=1
RMS_CHANNEL_SYSTEM=2
RMS_CHANNEL_TARGET=3
RMS_CHANNEL_OTHER=4
RMS_RESERVED_CHANNELS=RMS_CHANNEL_OTHER+1
RMS_NUM_CHANNELS=RMS_RESERVED_CHANNELS+5

RMS_SDL_AUDIODRIVER='pulse'
RMS_SDL_AUDIOFILE='/dev/stdout'
RMS_FREQUENCY=8000
RMS_BGM_VOLUME=0.2

RMS_PYGAME_SAMPLESIZE=-16
RMS_PYGAME_SAMPLECHANNELS=1
RMS_PYGAME_FREQUENCY=8000

#Sounds
SOUND_STARTSTOP='gong.wav'
SOUND_BGM='taxi.wav'
SOUND_ACHIEVE='achv.wav'
SOUND_LOST='boo.wav'
SOUND_GOOD='peew.wav'
SOUND_BAD='zzz.wav'

TTS_CACHE_DIR='/var/cache/raceman'

#tts_festival configuration
TTS_FESTIVAL_COMMAND=u"(tts_textall \"%s\" \'file)(quit)\n"
TTS_FESTIVAL_SERVER_HOST='127.0.0.1'
TTS_FESTIVAL_SERVER_PORT=1314
TTS_FESTIVAL_BUFFER_SIZE=10*44100*2


TTS_SAPI_SERVER_HOST='192.168.56.102'
TTS_SAPI_SERVER_PORT=40040
TTS_SAPI_BUFFER_SIZE=10*44100*2



config={
			u'arena': { 
				'name':u"Арена",
				'streamip':'50.56.75.58',
				'streamport':50007,
				'park':{
					'1': {
						'01':{'name':u'1','match':'^1$'},
						'02':{'name':u'2','match':'^2$'},
						'03':{'name':u'3','match':'^3$'},
						'04':{'name':u'4','match':'^4$'},
						'05':{'name':u'5','match':'^5$'},
						'06':{'name':u'6','match':'^6$'},
						'07':{'name':u'7','match':'^7$'},
						'08':{'name':u'8','match':'^8$'},
						'09':{'name':u'9','match':'^9$'},
						'10':{'name':u'10','match':'^10$'},
						'11':{'name':u'11','match':'^11$'},
						'12':{'name':u'12','match':'^12$'},
						'13':{'name':u'13','match':'^13$'},
						'14':{'name':u'14','match':'^14$'},
						'15':{'name':u'15','match':'^15$'},
						'16':{'name':u'16','match':'^16$'},
						'17':{'name':u'17','match':'^17$'},
						'18':{'name':u'18','match':'^18$'},
						'19':{'name':u'19','match':'^19$'},
						'20':{'name':u'20','match':'^20$'},
						'21':{'name':u'21','match':'^21$'},
						'22':{'name':u'22','match':'^22$'},
						'23':{'name':u'23','match':'^23$'},
						'24':{'name':u'24','match':'^24$'},
						'25':{'name':u'25','match':'^25$'}
					},
					'2': {
						'01':{'name':u'Соди 1','match':'^Sodi( )?1$'},
						'02':{'name':u'Соди 2','match':'^Sodi( )?2$'},
						'03':{'name':u'Соди 3','match':'^Sodi( )?3$'},
						'04':{'name':u'Соди 4','match':'^Sodi( )?4$'},
						'05':{'name':u'Соди 5','match':'^Sodi( )?5$'},
						'06':{'name':u'Соди 6','match':'^Sodi( )?6$'},
						'07':{'name':u'Соди 7','match':'^Sodi( )?7$'},
						'08':{'name':u'Соди 8','match':'^Sodi( )?8$'},
						'09':{'name':u'Соди 9','match':'^Sodi( )?9$'},
						'10':{'name':u'Соди 10','match':'^Sodi( )?10$'},
						'11':{'name':u'Соди 11','match':'^Sodi( )?11$'},
						'12':{'name':u'Соди 12','match':'^Sodi( )?12$'},
						'13':{'name':u'Соди 13','match':'^Sodi( )?13$'},
						'14':{'name':u'Соди 14','match':'^Sodi( )?14$'},
						'15':{'name':u'Соди 15','match':'^Sodi( )?15$'},
						'16':{'name':u'Соди 16','match':'^Sodi( )?16$'},
						'17':{'name':u'Соди 17','match':'^Sodi( )?17$'},
						'18':{'name':u'Соди 18','match':'^Sodi( )?18$'},
						'19':{'name':u'Соди 19','match':'^Sodi( )?19$'},
						'20':{'name':u'Соди 20','match':'^Sodi( )?20$'},
						'21':{'name':u'Соди 21','match':'^Sodi( )?21$'},
						'22':{'name':u'Соди 22','match':'^Sodi( )?22$'},
						'23':{'name':u'Соди 23','match':'^Sodi( )?23$'},
						'24':{'name':u'Соди 24','match':'^Sodi( )?24$'},
						'25':{'name':u'Соди 25','match':'^Sodi( )?25$'}
					}
				}
			},
			u'forza': { 
				'name':u"Форза",
				'streamip':'50.56.75.58',
				'streamport':50002,
				'park':{
					'1': {
						'01':{'name':u'1','match':'^1$'},
						'02':{'name':u'2','match':'^2$'},
						'03':{'name':u'3','match':'^3$'},
						'04':{'name':u'4','match':'^4$'},
						'05':{'name':u'5','match':'^5$'},
						'06':{'name':u'6','match':'^6$'},
						'07':{'name':u'7','match':'^7$'},
						'08':{'name':u'8','match':'^8$'},
						'09':{'name':u'9','match':'^9$'},
						'10':{'name':u'10','match':'^10$'},
						'11':{'name':u'11','match':'^11$'},
						'12':{'name':u'12','match':'^12$'},
						'13':{'name':u'13','match':'^13$'},
						'14':{'name':u'14','match':'^14$'},
						'15':{'name':u'15','match':'^15$'},
						'16':{'name':u'16','match':'^16$'},
						'17':{'name':u'17','match':'^17$'},
						'18':{'name':u'18','match':'^18$'},
						'19':{'name':u'19','match':'^19$'},
						'20':{'name':u'20','match':'^20$'},
						'21':{'name':u'21','match':'^21$'},
						'22':{'name':u'22','match':'^22$'},
						'23':{'name':u'23','match':'^23$'},
						'24':{'name':u'24','match':'^24$'},
						'25':{'name':u'25','match':'^25$'}
					}
				}
			}
		}