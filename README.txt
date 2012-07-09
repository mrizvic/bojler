bojler
======

household boiler attached to arduino via HM-TR433-TTL RF modules to alix2d3 pc board

Somewhere in june 2012 I started to wonder how much time does our 80L water heater (called 'bojler' in Slovenia) spend being ON or OFF regarding our needs.
We are three member family and just waiting for the forth member btw :)

On tuesday, 19th of June 2012 at 9pm I started to work with circuit and code. By midnight I got it finished and went to bed.
Later I added twitter logging and some unhandled exceptions were fixed.

How its made? 

Somewhere on boiler's control panel there is has small light which is on when boiler is heating water and thus consuming power.
I ducktaped photoresistor on that light so microcontroller's analogue input circut on arduino would sense when light is on or off.

Items used in this project:
-          arduino with atmega328p ( www.arduino.cc )
-		   prototype shield from DX ( http://www.dealextreme.com/p/arduino-prototype-shield-with-mini-breadboard-65273?item=8 )
-          couple of HopeRF modules (HM-TR433-TTL) with antenna ( http://www.hoperf.com/rf_fsk/fsk/HM-TR.htm )
-          PoUSB12 modul for PC connection, works like virtual serial port ( http://www.poscope.com/pousb12 - CP2102 chipset, i tested on windows and freebsd )
-          photoresistor and some pullup/pulldown resistors
 
I stacked prototype shield to arduino and glued protoboard on top. Photoresistor is wired between +5V and pin 0. 10k pulldown resistor is also used as shown in picture below.
This is called voltage divider and its purpose is to measure voltage with analog input 0 pin on arduino.

           PhotoR     10K
 +5    o---/\/\/--.--/\/\/---o GND
                  |
 Pin 0 o-----------
 

You might want to check this page for details:
- http://en.wikipedia.org/wiki/Voltage_divider
- http://www.arduino.cc/playground/Learning/PhotoResistor

I also connected HM-TR433-TTL to arduino's TX/RX pins.
Arduino repeatedly measures value on analog input pin0 and sends it via UART (TX/RX pins) to HM-TR433-TTL transciever. After that is 'sleeps' 1 second.

On the other side another HM-TR433-TTL transciever is connected to PoUSB12 module which is connected to USB port on ALIX2D3 PC board which I use as router (FreeBSD on 4Gb CF card).
Python script is used to read values from incoming 'virtual com' port. Values are interpreted and simple state machine is used to implement logic which detects boiler's sttate (on or off).

Na routerju python skripta berem vrednosti na 'COM' portu in glede na input v syslog belezi stanje on/off.

A lot of things could be improved:
- code is ugly because functionalities were implemented during brainstorms
- arduino code could detect and report boiler state changes via RF link instead of repatedly sending sensor value to ether

I hope you find something useful here. Or at least smile at funny freaky project :)

You can follow boiler state on twitter via #bojler.py tag (user syslog)
https://twitter.com/#!/search/realtime/%23bojler.py

Events are logged with syslog:
# grep bojler.py /var/log/all.log
Jul  9 07:42:09 monolith bojler.py: event: status=on,input=602
Jul  9 08:01:32 monolith bojler.py: event: status=off,input=108,delta=1162
Jul  9 14:12:02 monolith bojler.py: message: SIGINT caught, byebye
Jul  9 14:13:32 monolith bojler.py: message: processing started
Jul  9 14:26:11 monolith bojler.py: message: SIGINT caught, byebye
Jul  9 14:26:15 monolith bojler.py: message: processing started
Jul  9 14:37:13 monolith bojler.py: message: SIGINT caught, byebye
Jul  9 14:37:20 monolith bojler.py: message: processing started
Jul  9 14:46:35 monolith bojler.py: message: SIGINT caught, byebye
Jul  9 14:46:50 monolith bojler.py: message: processing started

Console ouput while bojler.py is running (stdout):
2012-07-09 15:13:18.268276 line:0
2012-07-09 15:13:19.268292 line:0
2012-07-09 15:13:20.268262 line:0
2012-07-09 15:13:21.268260 line:0
2012-07-09 15:13:22.268258 line:0
2012-07-09 15:13:23.269321 line:0
2012-07-09 15:13:24.269338 line:0
2012-07-09 15:13:25.269347 line:0
2012-07-09 15:13:26.269346 line:0
2012-07-09 15:13:27.269314 line:2
2012-07-09 15:13:28.270236 line:0
2012-07-09 15:13:29.270221 line:2
2012-07-09 15:13:30.270221 line:0
2012-07-09 15:13:31.270238 line:0
2012-07-09 15:13:32.270214 line:0

CTRL+C on console or SIGINT signal can be used to gracefully shutdown running process (write syslog/twitter message, close serial port).

I also wrote cronjob script to generate daily reports:
5 0 * * * /home/user/bojler-logparse.sh

# cat /home/user/bojler-logparse.sh
#!/bin/sh
/usr/bin/bzgrep "bojler.py: event" /var/log/all.log.0.bz2
echo -n "SUM(delta) = "
/usr/bin/bzgrep "bojler.py: event" /var/log/all.log.0.bz2 | grep delta | cut -d '=' -f4 | awk '{ sum += $1; c++ } END { print sum/60 " min"} '

Sample report sent from cronjob:
Jul  5 09:05:58 monolith bojler.py: event: status=on,input=632
Jul  5 09:23:04 monolith bojler.py: event: status=off,input=119,delta=1025
Jul  5 11:53:18 monolith bojler.py: event: status=on,input=547
Jul  5 12:07:51 monolith bojler.py: event: status=off,input=98,delta=873
Jul  5 18:10:59 monolith bojler.py: event: status=on,input=704
Jul  5 18:29:51 monolith bojler.py: event: status=off,input=138,delta=1132
SUM(delta) = 50.5 min


Kind regards,
Marko


