import os.path
import sys
import time
import obd
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "USER"
ifpass = "CHANGEME"
ifdb   = "OBD2"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "obd2"

# Path to serial port our ELM327 adaptor is on. usually /dev/rfcomm0 for bluetooth or /dev/ttyUSB0 for USB
ELM327_port = "/dev/rfcomm0"

if not os.path.exists(ELM327_port):
    print ("Could not connect to OBD2 adaptor, TTY not found")
    exit (2)

connection = obd.OBD(ELM327_port)

if not connection.is_connected():
    print ("Connected to OBD adaptor but vehicle is not running")
    exit (0)

while connection.is_connected(): 

    cmd = obd.commands.SPEED # select an OBD command (sensor)
    response = connection.query(cmd) # send the command, and parse the response
    speed = response.value

    cmd = obd.commands.RPM
    response = connection.query(cmd)
    rpm = response.value

    cmd = obd.commands.AMBIANT_AIR_TEMP 
    response = connection.query(cmd) 
    ambient_temp = response.value

    cmd = obd.commands.CONTROL_MODULE_VOLTAGE
    response = connection.query(cmd)
    voltage = response.value

    cmd = obd.commands.BAROMETRIC_PRESSURE
    response = connection.query(cmd)
    barometric_pressure = response.value

    cmd = obd.commands.MAF
    response = connection.query(cmd)
    maf = response.value

    cmd = obd.commands.INTAKE_TEMP
    response = connection.query(cmd)
    intake_temp = response.value

    cmd = obd.commands.INTAKE_PRESSURE
    response = connection.query(cmd)
    intake_pressure = response.value

    cmd = obd.commands.COOLANT_TEMP
    response = connection.query(cmd)
    coolant_temp = response.value

    cmd = obd.commands.ENGINE_LOAD
    response = connection.query(cmd)
    engine_load = response.value


# form a data record
    body_obd2 = [
        {
            "measurement": measurement_name,
            "fields": {
                "KPH": speed.magnitude,
                "RPM": rpm.magnitude,
                "AMBIENT_TEMP": ambient_temp.magnitude,
                "VOLTAGE": voltage.magnitude,
                "BAROMETRIC_PRESSURE": barometric_pressure.magnitude,
                "MAF": maf.magnitude,
                "INTAKE_TEMP": intake_temp.magnitude,
                "INTAKE_PRESSURE": intake_pressure.magnitude,
                "COOLANT_TEMP": coolant_temp.magnitude,
                "ENGINE_LOAD": engine_load.magnitude,
            }
        }
    ]


# connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
# write the measurement and sleep for a few seconds before we loop again
    ifclient.write_points(body_obd2)
    time.sleep(15)
else:
    print ("Looks like the engine stopped")
    exit (0)
