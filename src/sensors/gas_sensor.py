"""
MQ-2 Gas Sensor Module
Detects gas leakage and smoke
"""
try:
    from machine import Pin, ADC
    import time
    MICROPYTHON = True
except ImportError:
    # Simulation mode for testing in Codespaces
    MICROPYTHON = False
    import time

class GasSensor:
    def __init__(self, analog_pin, digital_pin, threshold=400):
        """
        Initialize MQ-2 Gas Sensor
        :param analog_pin: ADC pin number for analog reading
        :param digital_pin: GPIO pin for digital output
        :param threshold: Gas detection threshold value
        """
        self.threshold = threshold
        self.calibration_value = 0
        self.warmup_complete = False
        
        if MICROPYTHON:
            self.adc = ADC(analog_pin)
            self.digital_pin = Pin(digital_pin, Pin.IN)
        else:
            # Simulation mode
            self.adc = None
            self.digital_pin = None
            self.simulated_value = 250
        
    def warmup(self, duration=10):
        """
        Sensor warmup period (recommended 10-60 seconds)
        In production, use 24-48 hours for first-time calibration
        """
        print(f"🔥 MQ-2 Sensor warming up for {duration} seconds...")
        for i in range(duration):
            print(f"   {i+1}/{duration}...", end="\r")
            time.sleep(1)
        
        self.calibration_value = self.read_analog()
        self.warmup_complete = True
        print(f"\n✅ MQ-2 Sensor ready. Baseline: {self.calibration_value}")
        
    def read_analog(self):
        """
        Read analog value from MQ-2 sensor
        :return: Analog reading (0-1023 for ESP8266)
        """
        if MICROPYTHON:
            # ESP8266 ADC is 10-bit (0-1023)
            return self.adc.read()
        else:
            # Simulation: return random value between 200-600
            import random
            self.simulated_value = random.randint(200, 600)
            return self.simulated_value
    
    def read_digital(self):
        """
        Read digital output from MQ-2 sensor
        :return: 1 if gas detected, 0 otherwise
        """
        if MICROPYTHON:
            return self.digital_pin.value()
        else:
            # Simulation
            return 1 if self.simulated_value > self.threshold else 0
    
    def is_gas_detected(self):
        """
        Check if gas is detected based on threshold
        :return: True if gas detected, False otherwise
        """
        analog_value = self.read_analog()
        return analog_value > self.threshold
    
    def get_gas_level(self):
        """
        Get current gas level reading
        :return: Analog value representing gas concentration
        """
        return self.read_analog()
    
    def get_status(self):
        """
        Get comprehensive sensor status
        """
        analog = self.read_analog()
        digital = self.read_digital()
        detected = self.is_gas_detected()
        
        return {
            'analog': analog,
            'digital': digital,
            'detected': detected,
            'warmup_complete': self.warmup_complete,
            'status_text': '⚠️ GAS DETECTED' if detected else '✅ Normal'
        }

