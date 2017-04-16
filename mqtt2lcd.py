#The MIT License (MIT)
#
#Copyright (c) [2016] [David "Fires" Stein] [http://davidstein.cz]
#
#Based on RPI I2C backpack from Michael Horne at http://www.recantha.co.uk/blog/?p=4849
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#Updated section 2017 by Alexander van der Sar [http://www.vdsar.net]
#Based on the Onion Omega Fire i2c LCD library of David Stein
#at [http://davidstein.cz/onion-omega-firei2clcd-lib/]
#Thanks for the great library David!
# Added lcd.lcd_display_string_position("test1",1,3); where 1 is row, 3 is position
# MQTT messages to i2c lcd
# build completely for my Domotica solution where all energy consumption and generation
# is supplied via MQTT.

import paho.mqtt.client as mqtt  #import the client1
import time
import lcddriver   
import configparser
from time import gmtime, strftime

config = configparser.ConfigParser()
config.read('myconfig.ini')


#from time import * 
lcd = lcddriver.lcd(0x3F)  
lcd.backlightOn() 
#initialize values at start
content = {
    'energy/solar/actual': '0',
    'energy/solar/today': '0',
    'energy/solar/peak': '0',
    'energy/solar/total': '0',
    'energy/solar/totalactual': '0',
    'energy/solar/nactual': '0',
    'energy/solar/nactualreturn': '0',
    'energy/gas/today': '0',
    'energy/solar/nettoday': '0',
    'energy/solar/totaltoday': '0',
    'energy/year/solar': '0',
    'energy/year/import': '0',
    'energy/year/export': '0',
    'energy/year/gas': '0',
    'energy/year/consumption': '0',
    'energy/gas/hour': '0',
    'home/outdoor/temperature': '0'
}


def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id  "+str(client)
    print(m)

def on_message(client1, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")))
    print("Topic: ",str(message.topic))
    content[message.topic] = message.payload
    #lcd.lcd_clear()
    #time.sleep(0.1)
    #lcd.lcd_display_string_position("test1",1,3);
    #lcd.lcd_display_string_position("test2",2,5);
    #lcd.lcd_display_string_position("test3",3,2);
    #lcd.lcd_display_string_position("test4",4,10);
    #lcd.lcd_display_string("Nettoday: " + content['energy/solar/nettoday'], 1)
    #lcd.lcd_display_string("SolarActual: " + content['energy/solar/totalactual'], 2)
    #lcd.lcd_display_string("BuitenTemp: " + content['home/outdoor/temperature'], 3)
    #lcd.lcd_display_string("nActual: " + content['energy/solar/nactual'], 4)
    #print "totalactual: ", content['energy/solar/totalactual']
    #print "outdoor: ", content['home/outdoor/temperature']




def screen_1():
    print("updating display 1")
    actual = int(content['energy/solar/actual'])
    print(actual)
    if actual  == 0:
        print("actual is 0")
        lcd.lcd_display_string("Geen zon",1);
    elif actual >= 2500:
        print("actual is >=2500")
    	lcd.lcd_display_string("***",1);
    	lcd.lcd_display_string_position(content['energy/solar/actual']+"W",1,8-len(content['energy/solar/actual']));
    elif actual >= 1500:
        print("actual is >=1500")
        lcd.lcd_display_string("**",1);
        lcd.lcd_display_string_position(content['energy/solar/actual']+"W",1,8-len(content['energy/solar/actual']));
    elif actual >= 100:
        print("actual is >= 100")
        lcd.lcd_display_string("*",1);
        lcd.lcd_display_string_position(content['energy/solar/actual']+"W",1,8-len(content['energy/solar/actual']));
    elif actual > 0:
        print("actual is > 0")
        lcd.lcd_display_string("",1);
        lcd.lcd_display_string_position(content['energy/solar/actual']+"W",1,8-len(content['energy/solar/actual']));  
    
    TotalActualCosts = float(content['energy/solar/totalactual']);
    TotalActualCosts = (TotalActualCosts/1000) * 0.21;
    TotalActualCostsStr = "%1.2f" % TotalActualCosts
    lcd.lcd_display_string_position("$" + TotalActualCostsStr,1,10);
    lcd.lcd_display_string_position(content['energy/solar/totalactual']+"W",1,20-len(content['energy/solar/totalactual']));   

    lcd.lcd_display_string(strftime("%H:%M", gmtime()),3);
    lcd.lcd_display_string(strftime("%a %d %b", gmtime()),4);



#Screen definition 2
def screen_2():
    print("updating display 2")
    #first line
    lcd.lcd_display_string("A: ",1);
    lcd.lcd_display_string_position(content['energy/solar/actual'],1,9-len(content['energy/solar/actual']));
    lcd.lcd_display_string_position("W   C:",1,9);
    lcd.lcd_display_string_position(content['energy/solar/totalactual'],1,20-len(content['energy/solar/totalactual']));
    lcd.lcd_display_string_position("W",1,20);
    #second line
    lcd.lcd_display_string("P: ",2);
    lcd.lcd_display_string_position(content['energy/solar/peak'],2,9-len(content['energy/solar/peak']));
    lcd.lcd_display_string_position("W   I:",2,9);
    lcd.lcd_display_string_position(content['energy/solar/nactual'],2,20-len(content['energy/solar/nactual']));
    lcd.lcd_display_string_position("W",2,20);
    #third line
    lcd.lcd_display_string("T: ",3);
    lcd.lcd_display_string_position(content['energy/solar/today'],3,9-len(content['energy/solar/today']));
    lcd.lcd_display_string_position("Wh  E:",3,9);
    lcd.lcd_display_string_position(content['energy/solar/nactualreturn'],3,20-len(content['energy/solar/nactualreturn']));
    lcd.lcd_display_string_position("W",3,20);    
    #fourth line
    lcd.lcd_display_string("L: ",4);
    lcd.lcd_display_string_position(content['energy/solar/total'],4,9-len(content['energy/solar/total']));
    lcd.lcd_display_string_position("kWh G:",4,9);
    lcd.lcd_display_string_position(content['energy/gas/today'],4,20-len(content['energy/gas/today']));
    lcd.lcd_display_string_position("Q",4,20);    
 
def screen_3():
	#first line
    lcd.lcd_display_string(strftime("%Y Year Stats kWh", gmtime()),1);
	#2nd Line
    lcd.lcd_display_string("S: ",2);
    lcd.lcd_display_string_position(str(int(content['energy/year/solar'])/1000),2,8-len(str(int(content['energy/year/solar'])/1000)));
    lcd.lcd_display_string_position("kW  I:",2,8);
    lcd.lcd_display_string_position(str(int(content['energy/year/import'])/1000),2,19-len(str(int(content['energy/year/import'])/1000)));
    lcd.lcd_display_string_position("kW",2,19);
	#third line
    lcd.lcd_display_string("C: ",3);
    lcd.lcd_display_string_position(str(int(content['energy/year/consumption'])/1000),3,8-len(str(int(content['energy/year/consumption'])/1000)));
    lcd.lcd_display_string_position("kW  E:",3,8);
    lcd.lcd_display_string_position(str(int(content['energy/year/export'])/1000),3,19-len(str(int(content['energy/year/export'])/1000)));
    lcd.lcd_display_string_position("kW",3,19);
	#fourth line
    lcd.lcd_display_string("T: ",4);
    lcd.lcd_display_string_position(content['energy/solar/totaltoday'],4,8-len(content['energy/solar/totaltoday']));
    lcd.lcd_display_string_position("W   G:",4,8);
    lcd.lcd_display_string_position(str(int(content['energy/year/gas'])/1000),4,19-len(str(int(content['energy/year/gas'])/1000)));
    lcd.lcd_display_string_position("Q",4,20);
  


broker_address=config['DEFAULT']['Broker']
client1 = mqtt.Client("P1")    #create new instance
client1.on_connect= on_connect        #attach function to callback
client1.on_message=on_message        #attach function to callback
client1.username_pw_set(username=config['DEFAULT']['User'],password=config['DEFAULT']['Password'])

time.sleep(1)

client1.connect(broker_address)      #connect to broker
client1.loop_start()    #start the loop
client1.subscribe("energy/#")
client1.subscribe("home/outdoor/#")

#client1.publish("python","KOEKOEK")
while 1:
    time.sleep(5)
    lcd.lcd_clear()
    screen_1()
    time.sleep(5)
    lcd.lcd_clear()
    screen_2()
    time.sleep(5)
    lcd.lcd_clear()
    screen_3()

client1.disconnect()
client1.loop_stop()
                 
