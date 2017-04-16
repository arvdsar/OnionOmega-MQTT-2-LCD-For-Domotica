Based on the library of David Stein to use a 16x2 or 20x4 LCD with an Onion Omega.
http://davidstein.cz/onion-omega-firei2clcd-lib/

I've updated his library with a function to write a string starting at a specific
location on the display. You can find this library with an example here:
https://github.com/arvdsar/OnionOmega-MQTT-2-LCD

You are now at my repository containing a specific version I use to display my
energy consumption and solar energy generation on a 20x4 LCD Display. 

MQTT is at the center of my Domotica setup. All values are available in MQTT Topics.
You'll find the topics I use in the source code. You can replace it with your own topics 
and create something that suits your needs.

Copy the config.ini to myconfig.ini and update with your settings of your MQTT Broker
Edit mqtt2lcd.py and build something nice yourself :-)

start the script using:
python mqtt2lcd.py



