SOUNDS=gong.gsm ding.gsm boo.gsm achv.gsm peew.gsm zzz.gsm
SOUNDS_LIB_DIR=/usr/share/asterisk/sounds/custom
SOUNDS_LIB_FILEMODE=0664
SOUNDS_LIB_USER=root
SOUNDS_LIB_GROUP=root
CONVERTER=sox
CONVERTOPT=speed 1

GONG=gong1
DING=ding1
BOO=boo1
ACHV=achv1
PEEW=peew1
ZZZ=zzz1


gsm: $(SOUNDS)

gong.gsm: $(GONG).wav
	$(CONVERTER)  $< $@ $(CONVERTOPT)

ding.gsm: $(DING).wav
	$(CONVERTER)  $< $@ $(CONVERTOPT)

boo.gsm: $(BOO).wav
	$(CONVERTER)  $< $@ $(CONVERTOPT)

achv.gsm: $(ACHV).wav
	$(CONVERTER)  $< $@ $(CONVERTOPT)

peew.gsm: $(PEEW).wav
	$(CONVERTER)  $< $@ $(CONVERTOPT)

zzz.gsm: $(ZZZ).wav
	$(CONVERTER)  $< $@ $(CONVERTOPT)


install: gsm
	for file in $(SOUNDS); do echo Installing $$file; install -m $(SOUNDS_LIB_FILEMODE) -o $(SOUNDS_LIB_USER) -g $(SOUNDS_LIB_GROUP) -D $$file $(SOUNDS_LIB_DIR)/$$file; done

