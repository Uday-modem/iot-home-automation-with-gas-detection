"""
Buzzer Controller Module
Controls active buzzer for gas detection alarm
"""
try:
    from machine import Pin
    import time
    MICROPYTHON = True
except ImportError:
    MICROPYTHON = False
    import time

class BuzzerController:
    def __init__(self, buzzer_pin):
        """
        Initialize Buzzer Controller
        :param buzzer_pin: GPIO pin for buzzer
        """
        if MICROPYTHON:
            self.buzzer = Pin(buzzer_pin, Pin.OUT)
            self.buzzer.value(0)  # Start with buzzer OFF
        else:
            self.buzzer_state = 0
        
        self.is_alarming = False
        
    def alarm_on(self):
        """Turn on alarm"""
        if MICROPYTHON:
            self.buzzer.value(1)
        else:
            self.buzzer_state = 1
        self.is_alarming = True
        print("🚨 ALARM ON!")
        
    def alarm_off(self):
        """Turn off alarm"""
        if MICROPYTHON:
            self.buzzer.value(0)
        else:
            self.buzzer_state = 0
        self.is_alarming = False
        print("🔇 Alarm OFF")
        
    def beep(self, duration=0.5):
        """
        Single beep
        :param duration: Beep duration in seconds
        """
        self.alarm_on()
        time.sleep(duration)
        self.alarm_off()
        
    def beep_pattern(self, count=3, beep_time=0.2, pause_time=0.2):
        """
        Beep pattern (multiple beeps)
        :param count: Number of beeps
        :param beep_time: Duration of each beep
        :param pause_time: Pause between beeps
        """
        print(f"🔔 Beeping {count} times...")
        for i in range(count):
            self.alarm_on()
            time.sleep(beep_time)
            self.alarm_off()
            if i < count - 1:  # Don't pause after last beep
                time.sleep(pause_time)

