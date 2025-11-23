
"""
IoT Home Automation with Gas Detection
Main Application - MicroPython for ESP8266 NodeMCU
"""
import time
import sys

# Check if running on MicroPython or simulation
try:
    import network
    import urequests as requests
    MICROPYTHON = True
    print("Running on MicroPython (ESP8266)")
except ImportError:
    MICROPYTHON = False
    print("Running in SIMULATION mode (Codespaces)")

# Import configuration
sys.path.append('src')
from config import *

# Import sensor modules
from sensors.gas_sensor import GasSensor
from sensors.ldr_sensor import LDRSensor
from sensors.water_level import WaterLevelSensor

# Import controller modules
from controllers.relay_controller import RelayController
from controllers.buzzer_controller import BuzzerController


class HomeAutomationSystem:
    def __init__(self):
        """Initialize Home Automation System"""
        print("\n" + "=" * 60)
        print("   IoT HOME AUTOMATION WITH GAS DETECTION")
        print("=" * 60)
        print(f"Mode: {'HARDWARE' if MICROPYTHON else 'SIMULATION'}")
        print("=" * 60 + "\n")
        
        # WiFi connection status
        self.connected = False
        
        # Initialize WiFi (only on real hardware)
        if MICROPYTHON:
            self.wlan = network.WLAN(network.STA_IF)
        
        # Initialize sensors
        print("[STEP 1/5] Initializing Sensors...")
        print("  ├─ Gas Sensor (MQ-2)...")
        self.gas_sensor = GasSensor(PIN_MQ2_ANALOG, PIN_MQ2_DIGITAL, GAS_THRESHOLD)
        print("  ├─ Light Sensor (LDR)...")
        self.ldr_sensor = LDRSensor(PIN_LDR)
        print("  └─ Water Level Sensors...")
        self.water_sensor = WaterLevelSensor(PIN_FLOAT_OVERHEAD, PIN_FLOAT_UNDERGROUND)
        print("  ✅ Sensors initialized\n")
        
        # Initialize controllers
        print("[STEP 2/5] Initializing Controllers...")
        print("  ├─ Relay Controller (4-Channel)...")
        self.relay = RelayController(PIN_RELAY_LIGHT, PIN_RELAY_FAN, 
                                     PIN_RELAY_MOTOR, PIN_RELAY_GARDEN)
        print("  └─ Buzzer Controller...")
        self.buzzer = BuzzerController(PIN_BUZZER)
        print("  ✅ Controllers initialized\n")
        
        # System state for manual overrides
        self.manual_override = {
            'light': False,
            'fan': False,
            'motor': False,
            'garden': False
        }
        
        # Warmup gas sensor
        print("[STEP 3/5] Sensor Warmup...")
        self.gas_sensor.warmup(5 if not MICROPYTHON else 10)
        print()
        
        # Connect to WiFi
        if MICROPYTHON:
            print("[STEP 4/5] WiFi Connection...")
            self.connect_wifi()
            print()
        else:
            print("[STEP 4/5] WiFi - Skipped (Simulation Mode)\n")
            self.connected = False
        
        # System ready
        print("[STEP 5/5] System Initialization Complete!")
        self.buzzer.beep_pattern(count=2, beep_time=0.1, pause_time=0.1)
        print("\n" + "=" * 60)
        print("   🚀 SYSTEM READY")
        print("=" * 60 + "\n")
        
    def connect_wifi(self):
        """Connect to WiFi network"""
        if not MICROPYTHON:
            return
            
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print(f"  Connecting to: {WIFI_SSID}")
            self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            
            # Wait for connection (max 30 seconds)
            timeout = 30
            while not self.wlan.isconnected() and timeout > 0:
                print(".", end="")
                time.sleep(1)
                timeout -= 1
            
            print()  # New line
            
            if self.wlan.isconnected():
                self.connected = True
                config = self.wlan.ifconfig()
                print(f"  ✅ WiFi Connected!")
                print(f"     IP Address: {config[0]}")
                print(f"     Subnet: {config[1]}")
                print(f"     Gateway: {config[2]}")
            else:
                print("  ✗ WiFi Connection Failed!")
                print("  → Running in offline mode")
                self.connected = False
        else:
            self.connected = True
            print("  ✅ Already connected")
            print(f"     IP: {self.wlan.ifconfig()[0]}")
    
    def handle_gas_detection(self):
        """Handle gas leakage detection"""
        gas_status = self.gas_sensor.get_status()
        
        if gas_status['detected']:
            # GAS DETECTED - CRITICAL ALERT
            if not self.buzzer.is_alarming:
                print("\n" + "!" * 60)
                print("   ⚠️  ⚠️  ⚠️   GAS LEAKAGE DETECTED   ⚠️  ⚠️  ⚠️")
                print("!" * 60)
                print(f"   Gas Level: {gas_status['analog']} (Threshold: {self.gas_sensor.threshold})")
                print("!" * 60 + "\n")
                
            self.buzzer.alarm_on()
            
            # Send alert to Blynk (if connected)
            if self.connected:
                self.send_to_blynk(V_PIN_GAS_LEVEL, gas_status['analog'])
                self.log_event("gas_alert", f"Level: {gas_status['analog']}")
        else:
            # Gas levels normal
            if self.buzzer.is_alarming:
                print("✅ Gas levels returned to normal\n")
                self.buzzer.alarm_off()
        
        return gas_status
    
    def handle_garden_light(self):
        """Handle automatic garden light control based on LDR"""
        ldr_status = self.ldr_sensor.get_status()
        
        # Automatic control only if no manual override
        if not self.manual_override['garden']:
            if ldr_status['is_dark']:
                self.relay.control_garden_light(True)
            else:
                self.relay.control_garden_light(False)
        
        return ldr_status
    
    def handle_water_tank(self):
        """Handle automatic water motor control based on tank levels"""
        tank_status = self.water_sensor.get_tank_status()
        
        # Automatic control only if no manual override
        if not self.manual_override['motor']:
            if tank_status['can_run_motor']:
                self.relay.control_motor(True)
            else:
                self.relay.control_motor(False)
        
        return tank_status
    
    def send_to_blynk(self, virtual_pin, value):
        """
        Send data to Blynk virtual pin
        :param virtual_pin: Virtual pin number (0-255)
        :param value: Value to send
        """
        if not self.connected or not MICROPYTHON:
            return False
        
        try:
            url = f"http://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&v{virtual_pin}={value}"
            response = requests.get(url)
            response.close()
            return True
        except Exception as e:
            print(f"⚠️  Blynk update error: {e}")
            return False
    
    def log_event(self, event_code, description):
        """
        Log event to Blynk
        :param event_code: Event code name
        :param description: Event description
        """
        if not self.connected or not MICROPYTHON:
            return False
        
        try:
            url = f"http://blynk.cloud/external/api/logEvent?token={BLYNK_AUTH_TOKEN}&code={event_code}"
            response = requests.get(url)
            response.close()
            return True
        except Exception as e:
            print(f"⚠️  Blynk event log error: {e}")
            return False
    
    def print_system_status(self):
        """Print comprehensive system status"""
        print("\n" + "┌" + "─" * 58 + "┐")
        print("│" + " " * 18 + "SYSTEM STATUS" + " " * 27 + "│")
        print("├" + "─" * 58 + "┤")
        
        # Gas sensor status
        gas_status = self.gas_sensor.get_status()
        print("│ 📊 GAS SENSOR" + " " * 44 + "│")
        print(f"│    Reading: {gas_status['analog']:>4} / Threshold: {self.gas_sensor.threshold:>4}" + " " * 21 + "│")
        print(f"│    Status: {gas_status['status_text']}" + " " * (44 - len(gas_status['status_text'])) + "│")
        print("├" + "─" * 58 + "┤")
        
        # LDR sensor status
        ldr_status = self.ldr_sensor.get_status()
        print("│ 💡 LIGHT SENSOR" + " " * 42 + "│")
        print(f"│    {ldr_status['light_status']}" + " " * (54 - len(ldr_status['light_status'])) + "│")
        print("├" + "─" * 58 + "┤")
        
        # Water tank status
        tank_status = self.water_sensor.get_tank_status()
        print("│ 💧 WATER TANKS" + " " * 43 + "│")
        print(f"│    Overhead: {tank_status['overhead_status']}" + " " * (48 - len(tank_status['overhead_status'])) + "│")
        print(f"│    Underground: {tank_status['underground_status']}" + " " * (44 - len(tank_status['underground_status'])) + "│")
        print(f"│    Motor: {tank_status['motor_status']}" + " " * (48 - len(tank_status['motor_status'])) + "│")
        print("├" + "─" * 58 + "┤")
        
        # Relay status
        relay_status = self.relay.get_status()
        print("│ 🔌 APPLIANCES" + " " * 44 + "│")
        print(f"│    Light: {'🟢 ON ' if relay_status['light'] else '🔴 OFF'}" + " " * 42 + "│")
        print(f"│    Fan: {'🟢 ON ' if relay_status['fan'] else '🔴 OFF'}" + " " * 44 + "│")
        print(f"│    Motor: {'🟢 ON ' if relay_status['motor'] else '🔴 OFF'}" + " " * 42 + "│")
        print(f"│    Garden: {'🟢 ON ' if relay_status['garden'] else '🔴 OFF'}" + " " * 41 + "│")
        print("├" + "─" * 58 + "┤")
        
        # Connection status
        conn_status = "🟢 Connected" if self.connected else "🔴 Offline"
        print(f"│ 📡 WiFi: {conn_status}" + " " * (48 - len(conn_status)) + "│")
        print("└" + "─" * 58 + "┘\n")
    
    def run(self):
        """Main control loop - runs continuously"""
        print("🎯 Starting Main Control Loop")
        print("   Monitoring sensors and controlling devices...")
        print("   Press Ctrl+C to stop\n")
        
        loop_count = 0
        
        try:
            while True:
                loop_count += 1
                
                # Priority 1: Handle gas detection (CRITICAL)
                self.handle_gas_detection()
                
                # Priority 2: Handle automatic garden light
                self.handle_garden_light()
                
                # Priority 3: Handle automatic water tank motor
                self.handle_water_tank()
                
                # Print status every 10 loops (~10 seconds)
                if loop_count % 10 == 0:
                    self.print_system_status()
                
                # Send data to Blynk every 5 loops (~5 seconds)
                if self.connected and loop_count % 5 == 0:
                    gas_level = self.gas_sensor.get_gas_level()
                    tank_full = 1 if self.water_sensor.is_overhead_full() else 0
                    light_status = 0 if self.ldr_sensor.is_dark() else 1
                    
                    self.send_to_blynk(V_PIN_GAS_LEVEL, gas_level)
                    self.send_to_blynk(V_PIN_TANK_STATUS, tank_full)
                    self.send_to_blynk(V_PIN_LDR_STATUS, light_status)
                
                # Wait 1 second before next loop
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("   🛑 SYSTEM SHUTDOWN INITIATED")
            print("=" * 60)
            self.cleanup()
    
    def cleanup(self):
        """Cleanup before shutdown"""
        print("\n[1/3] Turning off all devices...")
        self.relay.turn_off_all()
        print("[2/3] Silencing alarm...")
        self.buzzer.alarm_off()
        print("[3/3] Disconnecting WiFi...")
        
        if MICROPYTHON and self.wlan:
            self.wlan.active(False)
        
        print("\n✅ System shutdown complete")
        print("=" * 60 + "\n")


# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + " " * 10 + "IoT HOME AUTOMATION SYSTEM" + " " * 22 + "║")
    print("║" + " " * 10 + "with Gas Detection" + " " * 30 + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        # Create and run the home automation system
        system = HomeAutomationSystem()
        system.run()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import sys
        sys.print_exception(e) if MICROPYTHON else print(f"Error details: {e}")
