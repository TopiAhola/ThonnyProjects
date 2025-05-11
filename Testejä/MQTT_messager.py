import mip   #Mitä Mip tekee?
import network, ujson
from time import sleep
from umqtt.simple import MQTTClient

messages_list = []

def new_message_callback(topic, message):
    print(topic, message)    
    message_only = ujson.loads(message)
    print(message_only["id"])
    print(message_only)
    global messages_list
    messages_list.append((topic,message))
    


SSID = "KMD751_Group_3"
PASSWORD = "topi1234"
BROKER_IP = "192.168.3.253"
PORT = 21883
#Lähiverkon broker: "192.168.3.253"
#Tämä broker julkaisee porttiin 192.168.3.253:1883 !
#21883 on kubios portti?

#WLAN määritys
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print(wlan.status())

## MQTT class::
## classumqtt.simple.MQTTClient(client_id, server, port=0, user=None,
## password=None, keepalive=0, ssl=False, ssl_params={}

#Mosquitto client
mqtt_client=MQTTClient("", BROKER_IP, PORT)
mqtt_client.connect() #clean_session=True poistettu tilapäisesti
mqtt_client.set_callback(new_message_callback)
mqtt_client.subscribe("kubios-response")


#Viesti looppi
if __name__ == "__main__":    


    message = '''{  "id": 123,
        "type": "RRI",
        "data": [
          828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812,
          812, 756, 820, 812, 800
        ],
        "analysis": { "type": "readiness" }
      }'''
    
    #message_json = ujson.dumps(message) #Does nothing?
    
    try:       
        topic = "kubios-request"
        #message = input("Your message: ") #Kirjoita viesti itse
        mqtt_client.publish(topic, message)
        print(f"Sending to MQTT: {topic} -> {message}")
        sleep(5)
            
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")
 
 


# print(message)
# print(message_obj)
        
timer = 0
while timer < 2:
    mqtt_client.check_msg()  
    
    print(messages_list)     
    
    sleep(1)
    timer += 1
    
# print("List:", messages_list)
# print("List item:", messages_list[0])
# print("Message with b", messages_list[0][1])
# print("Message", ujson.loads(messages_list[0][1]))


