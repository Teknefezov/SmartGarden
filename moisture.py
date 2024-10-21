from gpiozero import MCP3008
from sensor import Sensor

class Moisture(Sensor):
    def __init__(self, water_value = 38, air_value = 82):
        self.water_value = water_value
        self.air_value = air_value
        self.intervals = (air_value - water_value) / 3
        self.sensor = MCP3008(0)
        super().__init__(air_value - self.intervals)

    def get_sensor_value(self):
        return self.sensor.value * 100
    
    def should_turn_on_actuator(self):
        if self.get_sensor_value() > self.turn_on_value:
            return True
        return False
