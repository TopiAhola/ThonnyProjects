import network
from time import sleep
from umqtt.simple import MQTTClient

# Replace these values with your own
SSID = "KMD751_Group_3"
PASSWORD = "topi1234"
BROKER_IP = "192.168.3.253"

# Function to connect to WLAN
def connect_wlan():
    # Connecting to the group WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Attempt to connect once per second
    while wlan.isconnected() == False:
        print("Connecting... ")
        sleep(1)

    # Print the IP address of the Pico
    print("Connection successful. Pico IP:", wlan.ifconfig()[0])
    
def connect_mqtt():
    mqtt_client=MQTTClient("", BROKER_IP)
    mqtt_client.connect(clean_session=True)
    return mqtt_client

# Main program
if __name__ == "__main__":
    #Connect to WLAN
    connect_wlan()
    
    # Connect to MQTT
    try:
        mqtt_client=connect_mqtt()
        
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")

    # Send MQTT message
    try:
        while True:
            # Sending a message every 5 seconds.
            topic = "test"
            message = "Great job group 3!"
            mqtt_client.publish(topic, message)
            print(f"Sending to MQTT: {topic} -> {message}")
            sleep(5)
            
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")