#!/usr/local/bin/python

# kldstat
#Id Refs Address    Size     Name
# 1   10 0xc0400000 522058   kernel
# 2    1 0xc2071000 f000     ipfw.ko
# 3    1 0xc209a000 2000     ng_tcpmss.ko
#14    1 0xc247c000 3e000    cam.ko
#24    1 0xc240b000 2000     uslcom.ko
#25    1 0xc240d000 3000     ucom.ko
#26    2 0xc2410000 25000    usb.ko

import serial
import syslog
import signal
import sys
from datetime import datetime
import time
import tweepy

#get key,secret,token and token_secret from http://dev.twitter.com/apps
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def signal_handler(signal, frame):
        print 'SIGINT caught, byebye'
	syslog.syslog(syslog.LOG_INFO, 'message: SIGINT caught, byebye')
	try:
		x = str(datetime.now())
		api.update_status(x + ' #bojler.py: message: SIGINT caught, byebye')
	except:
		syslog.syslog(syslog.LOG_ERR, 'exception caught in signal_handler!')
	ser.close();
        sys.exit(0)

def checkInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

flag=0
time1=0
time2=0

syslog.syslog(syslog.LOG_INFO, 'message: processing started')
try:
	x = str(datetime.now())
	api.update_status(x + ' #bojler.py: message: processing started')
except:
	syslog.syslog(syslog.LOG_ERR, 'exception caught in main!')
signal.signal(signal.SIGINT, signal_handler)

ser = serial.Serial('/dev/ttyU0', 9600, timeout=1)
while (42):
	line = ser.readline()   # read a '\n' terminated line
				# vhodni podatek je integer med 0 in 1024 z dodanim \n
	line = line.strip()

	#ce vhodni podatek ni integer beri ponovno
	if not checkInt(line):
		continue

	#primerjaj prejsnji in trenutni parameter
	oldflag = flag

	msg = str(datetime.now()) + " line:" + line
	print msg

	#vhodni podatek je integer, zato ga obravnavaj
	line = int(line)

	#trial-and-error kdaj je na fotouporu dovolj svetlobe
	if line < 500:
		flag=0
	if line > 500:
		flag=1

	#line dam v string za ispis v syslogu
	line = str(line)

	#ce ni sprememb beri ponovno sicer obravnavaj in zabelezi spremembe
	if oldflag == flag:
		continue
	elif flag==1:
		msg = str(datetime.now()) + " ON " + line
		print msg
		time1=time.time()
		syslog.syslog(syslog.LOG_NOTICE, 'event: status=on,input=' + line)
		try:
			x = str(datetime.now())
			api.update_status(x + ' #bojler.py: event: status=on,input='+line)
		except:
			syslog.syslog(syslog.LOG_ERR, 'exception caught in while,flag==1')
	elif flag==0:
		time2=time.time()
		delta = str(int(time2-time1))
		msg = str(datetime.now()) + " OFF " + line + ",delta=" + delta
		print msg
		syslog.syslog(syslog.LOG_NOTICE, 'event: status=off,input=' + line + ",delta=" + delta)
		try:
			x = str(datetime.now())
			api.update_status(x + ' #bojler.py: event: status=off,input='+line+',delta='+delta)
		except:
			syslog.syslog(syslog.LOG_ERR, 'exception caught in while,flag==0')

#bonton (zapiraj vrata)
ser.close()
