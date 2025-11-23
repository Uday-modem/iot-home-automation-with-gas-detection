"""
Relay Controller Module
Controls 4-channel relay for Light, Fan, Water Motor, Garden Light
"""
try:
    from machine import Pin
    MICROPYTHON = True
except ImportError:
    MICROPYTHON = False

class RelayController:
    def __init__(self, light_pin, fan_pin, motor_pin, garden_pin):
        """
        Initialize 4-Channel Relay Controller
        Note: Relays are ACTIVE LOW (0 = ON, 1 = OFF)
        :param light_pin: GPIO pin for light relay
        :param fan_pin: GPIO pin for fan relay
        :param motor_pin: GPIO pin for water motor relay
        :param garden_pin: GPIO pin for garden light relay
        """
        if MICROPYTHON:
            self.light = Pin(light_pin, Pin.OUT)
            self.fan = Pin(fan_pin, Pin.OUT)
            self.motor = Pin(motor_pin, Pin.OUT)
            self.garden = Pin(garden_pin, Pin.OUT)
        else:
            # Simulation mode
            self.light_state = 1
            self.fan_state = 1
            self.motor_state = 1
            self.garden_state = 1
        
        # Initialize all relays to OFF (HIGH for active-low relays)
        self.turn_off_all()
        
    def turn_off_all(self):
        """Turn off all relays"""
        if MICROPYTHON:
            self.light.value(1)
            self.fan.value(1)
            self.motor.value(1)
            self.garden.value(1)
        else:
            self.light_state = 1
            self.fan_state = 1
            self.motor_state = 1
            self.garden_state = 1
        print("🔌 All relays turned OFF")
        
    def control_light(self, state):
        """
        Control room light
        :param state: True/1 for ON, False/0 for OFF
        """
        # Active LOW: 0 = ON, 1 = OFF
        value = 0 if state else 1
        if MICROPYTHON:
            self.light.value(value)
        else:
            self.light_state = value
        print(f"💡 Light: {'ON' if state else 'OFF'}")
        
    def control_fan(self, state):
        """Control fan"""
        value = 0 if state else 1
        if MICROPYTHON:
            self.fan.value(value)
        else:
            self.fan_state = value
        print(f"🌀 Fan: {'ON' if state else 'OFF'}")
        
    def control_motor(self, state):
        """Control water motor"""
        value = 0 if state else 1
        if MICROPYTHON:
            self.motor.value(value)
        else:
            self.motor_state = value
        print(f"💧 Motor: {'ON' if state else 'OFF'}")
        
    def control_garden_light(self, state):
        """Control garden light"""
        value = 0 if state else 1
        if MICROPYTHON:
            self.garden.value(value)
        else:
            self.garden_state = value
        print(f"🌿 Garden Light: {'ON' if state else 'OFF'}")
        
    def get_status(self):
        """
        Get status of all relays
        """
        if MICROPYTHON:
            return {
                'light': not self.light.value(),  # Invert for active-low
                'fan': not self.fan.value(),
                'motor': not self.motor.value(),
                'garden': not self.garden.value()
            }
        else:
            return {
                'light': not self.light_state,
                'fan': not self.fan_state,
                'motor': not self.motor_state,
                'garden': not self.garden_state
            }

