MANAGER_LIB=raceman/*.py raceman/*/*.py
MANAGER_LIB_DIR=/usr/local/lib/python2.7/dist-packages/
MANAGER_LIB_FILEMODE=0664
MANAGER_LIB_USER=root
MANAGER_LIB_GROUP=root

MANAGER_EXEC=rman.py
MANAGER_EXEC_DIR=/usr/share/asterisk/agi-bin/
MANAGER_EXEC_FILEMODE=0760
MANAGER_EXEC_USER=asterisk
MANAGER_EXEC_GROUP=adm


default: 

install: $(MANAGER_LIB) $(MANAGER_EXEC)
	find . -name \*.pyc -delete
	for file in $(MANAGER_LIB); do echo Installing $$file; install -m $(MANAGER_LIB_FILEMODE) -o $(MANAGER_LIB_USER) -g $(MANAGER_LIB_GROUP) -D $$file $(MANAGER_LIB_DIR)/$$file; done
	install -D -m $(MANAGER_EXEC_FILEMODE) -o $(MANAGER_EXEC_USER) -g $(MANAGER_EXEC_GROUP) $(MANAGER_EXEC) $(MANAGER_EXEC_DIR)
