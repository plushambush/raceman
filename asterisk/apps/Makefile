PROJ = app_extplay
OBJ  = app_extplay.o

CC = gcc
LD = gcc
STRIP = strip
RM = rm -f
CHMOD = chmod
INSTALL = install
DESTDIR =

CFLAGS  += -Wextra -fPIC -DAST_MODULE=\"$(PROJ)\" -D_THREAD_SAFE -I. -I/usr/include -O2 -DICONV_CONST="" -D__DEBUG__ -D__MANAGER__ -D__APP__
LDFLAGS += 
LIBS     = -lavutil -lswresample
SOLINK   = -shared -Xlinker -x

all	: clean $(PROJ).so

install	: all
	$(INSTALL) -d                $(DESTDIR)/usr/lib/asterisk/modules/
	$(INSTALL) -m 755 $(PROJ).so $(DESTDIR)/usr/lib/asterisk/modules/

$(PROJ).so: $(OBJ)
	$(LD) $(LDFLAGS) $(SOLINK) $(OBJ) $(LIBS) -o $@
	$(CHMOD) 755 $@

.c.o	:
	$(CC) $(CFLAGS) -c $<

clean	:
	@$(RM) $(PROJ).so *.o *.core
