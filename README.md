# OBD2infuxdb
A python script to fetch data from a generic ELM327 Bluetooth OBD2 adaptor and push it into InfluxDB

This script uses the obd and influxdb python modules to pull metrics from the OBD port of a vehicle and send it to Influx DB so that it can be graphed in Grafana etc for later analysis. It has been found to be very slow on a Raspbeery pi zero w and creates so much load that the pi becomes unresponsive. It may be better on devices with more cpu cores. It's thought that the main cuprit of this is the auto connect feature of the OBD module which must try every combination of serial port, baud rate and OBD protocols to figure out the correct setup and maybe specifying them manually will help prevent this issue (to be tested)

To set up the bluetooth connection on a raspberry pi / debian / ubuntu

Use bluetoothctl to scan for, pair and trust the OBD2 adaptor. We do not need to use this to connect
To connect run 
```bash
rfcomm bind 0 00:00:00:00:00:01 
```
0= /dev/rfcomm0
The mac address being the bluetooth mac address of your adaptpr 
Once this is done we should see /dev/rfcomm0 now exists and we should be able to figure out the other settings we need like speed which in my case is 115200.

VW's like my van seem to use the ISO 9141 protocol (protocol id 3?) but this is yet to be tested
