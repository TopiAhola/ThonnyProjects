# Hardware 1 Networks Final Assignment

The repository contains example code for the Raspberry Pi Pico board for the final assignment of the Networks course in Hardware 1.

The repository contains the following files:
- **connect_to_wlan.py**
You can use the program to connect the Raspberry Pi Pico W to your group's WLAN.
- **install_mqtt.py**
You can use the program to install MQTT client to the Raspberry Pi Pico.
- **mqtt_publish_test.py**
The test connects the Pico W to the group WLAN, opens an MQTT connection and periodically sends MQTT messages.

To use the example programs, you must replace the default values of the following variables at the top of the programs:

```
SSID = "WLAN SSID"
PASSWORD = "WLAN PASSWORD"
BROKER_IP = "192.168.1.254"
```
