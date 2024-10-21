from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, turn_on_value):
        self.turn_on_value = turn_on_value

    @abstractmethod
    def get_sensor_value(self):
        pass

    @abstractmethod
    def should_turn_on_actuator(self):
        pass
