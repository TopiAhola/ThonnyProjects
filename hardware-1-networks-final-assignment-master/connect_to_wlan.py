import network
from time import sleep

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

# Main program
connect_wlan()