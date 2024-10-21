from http.server import BaseHTTPRequestHandler
from functools import cached_property
import json
import re


HOST = "192.168.112.15"
PORT = 9999

class SmartGardenHTTPHandler(BaseHTTPRequestHandler):
    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    def do_GET(self):
        self.send_response(200)

        self.send_header("Content-type", "application/json")
        self.end_headers()

        if re.search('/turn-on-values', self.path):
            data = {
                "moisture": self.server.moisture_sensor.turn_on_value,
                "temperature": self.server.aht20_sensor.temp_turn_on_value,
                "humidity": self.server.aht20_sensor.humd_turn_on_value,
                "air_quality": self.server.air_quality_sensor.turn_on_value,
                "light": self.server.light_sensor.turn_on_value
            }
            self.wfile.write(bytes(json.dumps(data), "utf-8"))

        elif re.search('/', self.path):
            if self.server.aht20_sensor.start_measurement_ready():
                (temperature_c,
                temperature_f,
                humidity) = self.server.aht20_sensor.get_sensor_value()
            else:
                temperature_c = 0
                temperature_f = 0
                humidity = 0

            data = {
                "moisture": self.server.moisture_sensor.get_sensor_value(),
                "light": self.server.light_sensor.get_sensor_value(),
                "temperature_C": temperature_c,
                "temperature_F": temperature_f,
                "humidity": humidity,
                "air_quality": self.server.air_quality_sensor.get_sensor_value()
            }

            self.wfile.write(bytes(json.dumps(data), "utf-8"))

    def do_POST(self):
        self.send_response(200)

        self.send_header("Content-type", "text/plain")
        self.end_headers()

        if re.search('/fan/on', self.path):
            self.server.fan.on()
    
            self.wfile.write(bytes("", "utf-8"))

        elif re.search('/fan/off', self.path):
            self.server.fan.off()
    
            self.wfile.write(bytes("", "utf-8"))

        elif re.search('/pump/on', self.path):
            self.server.water_pump.on()
    
            self.wfile.write(bytes("", "utf-8"))

        elif re.search('/pump/off', self.path):
            self.server.water_pump.off()
    
            self.wfile.write(bytes("", "utf-8"))

        elif re.search('/light/on', self.path):
            self.server.led.on()
    
            self.wfile.write(bytes("", "utf-8"))

        elif re.search('/light/off', self.path):
            self.server.led.off()
    
            self.wfile.write(bytes("", "utf-8"))

        elif re.search('/', self.path):
            data = json.loads(self.post_data)
            
            self.server.moisture_sensor.turn_on_value = data["moisture"]
            
            self.server.light_sensor.turn_on_value = data["light"]
            
            self.server.aht20_sensor.temp_turn_on_value = data["temperature"]
            
            self.server.aht20_sensor.humd_turn_on_value = data["humidity"]
           
            self.server.air_quality_sensor.turn_on_value = data["air_quality"]         
        
            self.wfile.write(bytes("", "utf-8"))
