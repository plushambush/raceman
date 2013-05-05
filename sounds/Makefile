CONVERTER=sox
CONVERTOPT=speed 1
GONG=gong1
DING=ding1
BOO=boo1
ACHV=achv1
PEEW=peew1
ZZZ=zzz1

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


GSM: gong.gsm ding.gsm boo.gsm achv.gsm peew.gsm zzz.gsm
