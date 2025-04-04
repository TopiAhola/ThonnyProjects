import mip
import network
from time import sleep
from umqtt.simple import MQTTClient

def new_message_callback(topic,message):
    print(topic, message)


SSID = "KMD751_Group_3"
PASSWORD = "topi1234"
BROKER_IP = "192.168.3.253"
#Lähiverkon broker: "192.168.3.253"
#Tämä broker julkaisee porttiin 192.168.3.253:1883 !
#21883 on kubios portti?

#WLAN määritys
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print(wlan.status())

#Mosquitto client
mqtt_client=MQTTClient("", BROKER_IP)
mqtt_client.connect() #clean_session=True poistettu tilapäisesti
mqtt_client.set_callback(new_message_callback)
mqtt_client.subscribe("testi")


#Viesti looppi
if __name__ == "__main__":    
    try:       
        topic = "testi"
        message = input("Your message: ")
        mqtt_client.publish(topic, message)
        print(f"Sending to MQTT: {topic} -> {message}")
        sleep(5)
            
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")
        
        

while True:
    mqtt_client.check_msg()
    sleep(1)


