SOUNDS=gong.wav ding.wav boo.wav achv.wav peew.wav zzz.wav taxi.wav
SOUNDS_LIB_DIR=/usr/share/asterisk/sounds/custom
SOUNDS_LIB_FILEMODE=0664
SOUNDS_LIB_USER=root
SOUNDS_LIB_GROUP=root
CONVERTER=sox
CONVERTOPT=-r 16k -e signed-integer

sounds: $(SOUNDS)

gong.wav: gong1.wav
	$(CONVERTER)  $< $(CONVERTOPT) $@

ding.wav: ding1.wav
	$(CONVERTER)  $< $(CONVERTOPT) $@

boo.wav: boo1.wav
	$(CONVERTER)  $< $(CONVERTOPT) $@

achv.wav: achv1.wav
	$(CONVERTER)  $< $(CONVERTOPT) $@

peew.wav: peew1.wav
	$(CONVERTER)  $< $(CONVERTOPT) $@

zzz.wav: zzz1.wav
	$(CONVERTER)  $< $(CONVERTOPT) $@

taxi.wav: taxi.ogg
	$(CONVERTER) $< $(CONVERTOPT) $@

install: sounds
	for file in $(SOUNDS); do echo Installing $$file; install -m $(SOUNDS_LIB_FILEMODE) -o $(SOUNDS_LIB_USER) -g $(SOUNDS_LIB_GROUP) -D $$file $(SOUNDS_LIB_DIR)/$$file; done

