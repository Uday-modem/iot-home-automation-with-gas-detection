"""
Water Level Float Switch Sensors
Monitors water levels in overhead and underground tanks
"""
try:
    from machine import Pin
    MICROPYTHON = True
except ImportError:
    MICROPYTHON = False

class WaterLevelSensor:
    def __init__(self, overhead_pin, underground_pin):
        """
        Initialize Water Level Sensors
        :param overhead_pin: GPIO pin for overhead tank float switch
        :param underground_pin: GPIO pin for underground tank float switch
        """
        if MICROPYTHON:
            self.overhead = Pin(overhead_pin, Pin.IN, Pin.PULL_UP)
            self.underground = Pin(underground_pin, Pin.IN, Pin.PULL_UP)
        else:
            # Simulation mode
            self.overhead = None
            self.underground = None
            self.overhead_state = 0
            self.underground_state = 1
        
    def is_overhead_full(self):
        """
        Check if overhead tank is full
        :return: True if full, False otherwise
        """
        if MICROPYTHON:
            return self.overhead.value() == 1
        else:
            import random
            self.overhead_state = random.choice([0, 1])
            return self.overhead_state == 1
    
    def is_underground_empty(self):
        """
        Check if underground tank is empty
        :return: True if empty, False otherwise
        """
        if MICROPYTHON:
            return self.underground.value() == 0
        else:
            import random
            self.underground_state = random.choice([0, 1])
            return self.underground_state == 0
    
    def can_run_motor(self):
        """
        Determine if water motor can run safely
        Motor should NOT run if:
        - Overhead tank is full (prevent overflow)
        - Underground tank is empty (prevent dry running)
        :return: True if motor can run, False otherwise
        """
        overhead_full = self.is_overhead_full()
        underground_empty = self.is_underground_empty()
        
        return not overhead_full and not underground_empty
    
    def get_tank_status(self):
        """
        Get comprehensive tank status
        """
        overhead_full = self.is_overhead_full()
        underground_empty = self.is_underground_empty()
        motor_allowed = self.can_run_motor()
        
        # Determine status messages
        overhead_msg = '🟢 Full' if overhead_full else '🔵 Not Full'
        underground_msg = '🔴 Empty' if underground_empty else '🟢 Has Water'
        motor_msg = '✅ Can Run' if motor_allowed else '🛑 Cannot Run'
        
        return {
            'overhead_full': overhead_full,
            'underground_empty': underground_empty,
            'can_run_motor': motor_allowed,
            'overhead_status': overhead_msg,
            'underground_status': underground_msg,
            'motor_status': motor_msg
        }

