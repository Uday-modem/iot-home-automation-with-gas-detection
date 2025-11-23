"""
LDR (Light Dependent Resistor) Sensor Module
Detects ambient light for automatic garden light control
"""
try:
    from machine import Pin
    MICROPYTHON = True
except ImportError:
    MICROPYTHON = False

class LDRSensor:
    def __init__(self, digital_pin):
        """
        Initialize LDR Sensor
        :param digital_pin: GPIO pin for digital output
        """
        if MICROPYTHON:
            self.digital_pin = Pin(digital_pin, Pin.IN)
        else:
            # Simulation mode
            self.digital_pin = None
            self.simulated_value = 1  # Start with light condition
        
    def is_dark(self):
        """
        Check if it's dark (for automatic light control)
        :return: True if dark, False if light
        """
        # LDR module outputs LOW (0) when dark, HIGH (1) when light
        if MICROPYTHON:
            return self.digital_pin.value() == 0
        else:
            # Simulation
            import random
            self.simulated_value = random.choice([0, 1])
            return self.simulated_value == 0
    
    def read(self):
        """
        Read digital value from LDR sensor
        :return: 0 (dark) or 1 (light)
        """
        if MICROPYTHON:
            return self.digital_pin.value()
        else:
            return self.simulated_value
    
    def get_status(self):
        """
        Get comprehensive sensor status
        """
        is_dark = self.is_dark()
        digital_val = self.read()
        
        return {
            'digital': digital_val,
            'is_dark': is_dark,
            'light_status': '🌙 Dark' if is_dark else '☀️ Light',
            'action': 'Garden light ON' if is_dark else 'Garden light OFF'
        }

