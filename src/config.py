# WiFi Configuration
WIFI_SSID = "vivo V23 5G"  # Replace with your WiFi name
WIFI_PASSWORD = "ade ra password"  # Replace with your WiFi password

# Blynk Configuration
BLYNK_TEMPLATE_ID = "TMPL_XXXXXXXX"  # Get from Blynk Console
BLYNK_DEVICE_NAME = "Home_Automation"
BLYNK_AUTH_TOKEN = "YOUR_BLYNK_AUTH_TOKEN"  # Get from Blynk Console

# Pin Configuration (ESP8266 GPIO pins)
# NOTE: These are GPIO numbers, not D0, D1, etc.
PIN_MQ2_ANALOG = 0       # A0 - MQ-2 Gas Sensor (Analog)
PIN_MQ2_DIGITAL = 16     # D0 - MQ-2 Digital Output
PIN_LDR = 14             # D5 - LDR Sensor
PIN_FLOAT_OVERHEAD = 12  # D6 - Overhead Tank Float Switch
PIN_FLOAT_UNDERGROUND = 13  # D7 - Underground Tank Float Switch
PIN_RELAY_LIGHT = 5      # D1 - Light Relay
PIN_RELAY_FAN = 4        # D2 - Fan Relay
PIN_RELAY_MOTOR = 0      # D3 - Water Motor Relay
PIN_RELAY_GARDEN = 2     # D4 - Garden Light Relay
PIN_BUZZER = 15          # D8 - Buzzer

# Sensor Thresholds
GAS_THRESHOLD = 400      # MQ-2 gas detection threshold (adjust after calibration)
LDR_DARK_THRESHOLD = 1   # LDR digital output (LOW = dark)
TANK_FULL = 1            # Float switch HIGH = tank full
TANK_EMPTY = 0           # Float switch LOW = tank empty

# Virtual Pins for Blynk App
V_PIN_LIGHT = 0          # Virtual pin for light control
V_PIN_FAN = 1            # Virtual pin for fan control
V_PIN_MOTOR = 2          # Virtual pin for water motor control
V_PIN_GARDEN = 3         # Virtual pin for garden light control
V_PIN_GAS_LEVEL = 10     # Virtual pin for gas level display
V_PIN_TANK_STATUS = 11   # Virtual pin for tank status
V_PIN_LDR_STATUS = 12    # Virtual pin for light sensor status
V_PIN_SYSTEM_STATUS = 13 # Virtual pin for overall system status

# System Settings
SENSOR_READ_INTERVAL = 1000  # Read sensors every 1000ms (1 second)
BLYNK_UPDATE_INTERVAL = 2000 # Update Blynk every 2000ms (2 seconds)

