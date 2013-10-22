GCC=gcc
AST_MODULE=ast_extplay

app_extplay.so: app_extplay.c
	$(GCC) -DAST_MODULE=\"$(AST_MODULE)\" -shared -o app_extplay.so app_extplay.c
	
install: app_extplay.so
	cp app_extplay.so /usr/lib/asterisk/modules/