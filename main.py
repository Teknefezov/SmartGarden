from moisture import Moisture
from DFRobot_AHT20 import *
from air_quality import Air_quality
import time
from server import PORT, HOST, SmartGardenHTTPHandler
from http.server import HTTPServer
import threading
from gpiozero import LED, DigitalOutputDevice
from BH1750 import BH1750

def water_plant():
    water_pump.on()
    time.sleep(2)
    water_pump.off()

moisture_sensor = Moisture(41,79)
light_sensor = BH1750()
aht20_sensor = DFRobot_AHT20()
air_quality_sensor = Air_quality()

led = LED(17)
fan = DigitalOutputDevice(27, active_high=False)
water_pump = DigitalOutputDevice(22, active_high=False)

server = HTTPServer((HOST,PORT),SmartGardenHTTPHandler)
server.moisture_sensor = moisture_sensor
server.light_sensor = light_sensor
server.aht20_sensor = aht20_sensor
server.air_quality_sensor = air_quality_sensor
server.fan = fan
server.led = led
server.water_pump = water_pump
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

while (True):
    if moisture_sensor.should_turn_on_actuator() and water_pump.value == 0:
        pump_thread = threading.Thread(target=water_plant)
        pump_thread.start()

    if light_sensor.should_turn_on_actuator() and not led.is_lit:
        led.on()
    elif led.is_lit and not light_sensor.should_turn_on_actuator():
        led.off()

    if (aht20_sensor.should_turn_on_actuator() 
        or air_quality_sensor.should_turn_on_actuator()) and fan.value == 0:
        fan.on()
    
    if(not aht20_sensor.should_turn_on_actuator()
       and not air_quality_sensor.should_turn_on_actuator()
       and fan.value == 1):
        fan.off()

# Uncomment if you want to see values without using the mobile app
    # print(moisture_sensor.get_sensor_value())
    # print(light_sensor.get_sensor_value())
    # if aht20_sensor.start_measurement_ready():
    #     print(aht20_sensor.get_sensor_value())
    # print(air_quality_sensor.get_sensor_value())

    time.sleep(3)
