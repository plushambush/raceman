ASTERISK_FILES=datacard.conf gtalk.conf jingle.conf jabber.conf modules.conf extensions_custom.conf extensions.conf raceman.conf sip.conf
ASTERISK_USER=asterisk
ASTERISK_GROUP=asterisk
ASTERISK_FILEMODE=0640
ASTERISK_ETC=/etc/asterisk/

default:

install: $(ASTERISK_FILES)
	for file in $(ASTERISK_FILES); do install -m $(ASTERISK_FILEMODE) -o $(ASTERISK_USER) -g $(ASTERISK_GROUP) $$file $(ASTERISK_ETC); done
	
