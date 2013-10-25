/*
 * Asterisk -- An open source telephony toolkit.
 *
 * Copyright (C) 1999 - 2005, Digium, Inc.
 *
 * Mark Spencer <markster@digium.com>
 *
 * See http://www.asterisk.org for more information about
 * the Asterisk project. Please do not directly contact
 * any of the maintainers of this project for assistance;
 * the project provides a web site, mailing lists and IRC
 * channels for your use.
 *
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 */

/*! \file
 *
 * \brief Plays sound generated by externall aplication to stdout. Mostly based on app_mp3
 *
 * \author Ivan Konov
 *
 * 
 * \ingroup applications
 */

/*** MODULEINFO
	<support_level>extended</support_level>
 ***/
 
#include "asterisk/asterisk.h"

ASTERISK_FILE_VERSION(__FILE__, "$Revision: 336716 $")

#include <sys/time.h>
#include <signal.h>
#include <math.h>

#include "asterisk/lock.h"
#include "asterisk/file.h"
#include "asterisk/channel.h"
#include "asterisk/frame.h"
#include "asterisk/pbx.h"
#include "asterisk/module.h"
#include "asterisk/translate.h"
#include "asterisk/app.h"

#include <libavutil/audioconvert.h>
#include <libswresample/swresample.h>


/*** DOCUMENTATION
	<application name="extplay" language="en_US">
		<synopsis>
			Plays sound generated by externall aplication to stdout
		</synopsis>
		<syntax>
			<parameter name="Application" required="true">
				<para>Path to the application</para>
			</parameter>
		</syntax>
		<description>
			<para>Plays sound generated by external aplication to stdout</para>
			<para>This application does not automatically answer and should be preceeded by an
			application such as Answer() or Progress().</para>
		</description>
	</application>

 ***/
static char *app = "extplay";

static int exec_extplayer(const char *filename, int fd)
{
	int res;

	res = ast_safe_fork(0);
	if (res < 0) 
		ast_log(LOG_WARNING, "Fork failed\n");
	if (res) {
		return res;
	}
	if (ast_opt_high_priority)
		ast_set_priority(0);

	dup2(fd, STDOUT_FILENO);
	ast_close_fds_above_n(STDERR_FILENO);

    execl(filename, filename, (char *)NULL);

	/* Can't use ast_log since FD's are closed */
	fprintf(stderr, "Execute of extplay failed\n");
	_exit(0);
}

static int timed_read(int fd, void *data, int datalen, int timeout)
{
	int res;
	struct pollfd fds[1];
	fds[0].fd = fd;
	fds[0].events = POLLIN;
	res = ast_poll(fds, 1, timeout);
	if (res < 1) {
		ast_log(LOG_NOTICE, "Poll timed out/errored out with %d\n", res);
		return -1;
	}
	return read(fd, data, datalen);
	
}


#define SAMPLE_BUFFER_SIZE 1600

static int extplay(struct ast_channel *chan, const char *data)
{
	int res=0;
	int fds[2];
	int ms = -1;
	int pid = -1;
	int owriteformat;
	int timeout = 2000;
	struct timeval next;
	struct ast_frame *f;
	struct myframe {
		struct ast_frame f;
		char offset[AST_FRIENDLY_OFFSET];
		uint8_t frdata[SAMPLE_BUFFER_SIZE];
	} myf = {
		.f = { 0, },
	};

	uint8_t res_buffer[SAMPLE_BUFFER_SIZE];
	
	const uint8_t *res_buffer_ptr=res_buffer;
	uint8_t *out_buffer_ptr=myf.frdata;
	
	struct SwrContext * swr;
	

	if (ast_strlen_zero(data)) {
		ast_log(LOG_WARNING, "Extplay requires an argument (filename)\n");
		return -1;
	}

	if (pipe(fds)) {
		ast_log(LOG_WARNING, "Unable to create pipe\n");
		return -1;
	}
	
	ast_stopstream(chan);

	owriteformat = chan->writeformat;
	res = ast_set_write_format(chan, AST_FORMAT_SLINEAR);
	if (res < 0) {
		ast_log(LOG_WARNING, "Unable to set write format to signed linear\n");
		return -1;
	}

	swr=swr_alloc_set_opts(
	NULL,
	AV_CH_LAYOUT_MONO,
	AV_SAMPLE_FMT_S16,
	8000,
	AV_CH_LAYOUT_MONO,
	AV_SAMPLE_FMT_S16,
	22050,
	0,
	NULL);
	// Set up resampler
	if (swr==NULL) {
		ast_log(LOG_WARNING,"Unable to allocate resampler\n");
		return -1;
	}
	res=swr_init(swr);
	if (res!=0) {
		ast_log(LOG_WARNING,"Unable to initialize resampler. Error: %x\n",res);
		swr_free(&swr);
		return -1;
	}

	ast_log(LOG_WARNING,"Initialized resampler\n");
	
	
	res = exec_extplayer(data, fds[1]);
	
	ast_log(LOG_WARNING,"Executed external process %s with pid %d\n",data,res);
	/* Wait 1000 ms first */
	next = ast_tvnow();
	next.tv_sec += 1;
	if (res >= 0) {
		pid = res;
		/* Order is important -- there's almost always going to be mp3...  we want to prioritize the
		   user */
		for (;;) {
			ms = ast_tvdiff_ms(next, ast_tvnow());
			if (ms <= 0) {
				res = timed_read(fds[0], res_buffer, sizeof(res_buffer), timeout);
				if (res > 0) {
					res=swr_convert(swr,&out_buffer_ptr,SAMPLE_BUFFER_SIZE,&res_buffer_ptr,res/2);
					if (res >0) {
						myf.f.frametype = AST_FRAME_VOICE;
						myf.f.subclass.codec = AST_FORMAT_SLINEAR;
						myf.f.datalen = res*2;
						myf.f.samples = res;
						myf.f.mallocd = 0;
						myf.f.offset = AST_FRIENDLY_OFFSET;
						myf.f.src = __PRETTY_FUNCTION__;
						myf.f.delivery.tv_sec = 0;
						myf.f.delivery.tv_usec = 0;
						myf.f.data.ptr = myf.frdata;
						int res1 = ast_write(chan, &myf.f);
						if (res1<0) {
							res = -1;
							break;
						}
					}
				} else {
					ast_debug(1, "No more sound\n");
					res = 0;
					break;
				}
				next = ast_tvadd(next, ast_samp2tv(myf.f.samples, 8000));
			} else {
				ms = ast_waitfor(chan, ms);
				
				if (ms < 0) {
					ast_debug(1, "Hangup detected\n");
					res = -1;
					break;
				}
				if (ms) {
					f = ast_read(chan);
					if (!f) {
						ast_debug(1, "Null frame == hangup() detected\n");
						res = -1;
						break;
					}
					ast_frfree(f);
				} 
			}
		}
	}
	
	ast_log(LOG_WARNING,"Exiting...\n");
	
	close(fds[0]);
	close(fds[1]);
	
	if (pid > -1)
		kill(pid, SIGKILL);
	if (!res && owriteformat)
		ast_set_write_format(chan, owriteformat);
	
	swr_free(&swr);
		
	return res;
}

static int unload_module(void)
{
	return ast_unregister_application(app);
}

static int load_module(void)
{
	return ast_register_application_xml(app, extplay);
}

AST_MODULE_INFO_STANDARD(ASTERISK_GPL_KEY, "External player");
