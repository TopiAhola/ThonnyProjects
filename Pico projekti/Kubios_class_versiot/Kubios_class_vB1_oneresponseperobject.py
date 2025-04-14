import network, ujson, time
from umqtt.simple import MQTTClient


class Kubios:
    test_message = '''{ "id": 123,"type": "PPI",
        "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800],
        "analysis": { "type": "readiness" } }'''    
    
    def __init__(self):
        self.response = {}
        self.response_bool = False
        
        SSID = "KMD751_Group_3"
        PASSWORD = "topi1234"                
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(SSID, PASSWORD)      
        
        BROKER_IP = "192.168.3.253"
        PORT = 21883
        
        self.mqtt_client=MQTTClient("", BROKER_IP, PORT)
        self.mqtt_client.connect() 
        self.mqtt_client.set_callback(self.response_callback)
        self.mqtt_client.subscribe("kubios-response")
        
            

    # Tämä on redundantti koska init tekee yhteyden myös...
    def connect(self):
        #WLAN
        SSID = "KMD751_Group_3"
        PASSWORD = "topi1234"                
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(SSID, PASSWORD)       
        return self.wlan
# #         #Mosquitto client
# #         if wlan.status == 3:            
# #             BROKER_IP = "192.168.3.253"
# #             PORT = 21883
# #             self.mqtt_client=MQTTClient("", BROKER_IP, PORT)
# #             mqtt_client.connect() 
# #             mqtt_client.set_callback(self.response_callback)
# #             mqtt_client.subscribe("kubios-response")
# #         
# #         else:
# #             error_message = "WLAN not connected"
# #             print(error_message)
#         
# #         return error_message
        
            
        
    def send_request(self, id, type, data):
        # Forms a MQTT message to publish as request
        message = f'{"id": {id}, "type": {type},"data": {data},"analysis": { "type": "readiness" }}'
        self.mqtt_client.publish("kubios-request", message)
    
    def response_callback(self, topic, message):
        #Saves incoming response
        message_dict = ujson.loads(message)
        self.response = message_dict
        self.response_bool = True
        
    def check_response(self):
        self.mqtt_client.check_msg()
        if self.response_bool:
            return True
        else:
            return False
        
    def get_response(self):        
        return_dict = self.response
        self.response = {}
        self.response_bool = False
        return return_dict

    def test(self):
        error_message = ""
        if not self.wlan.status == 3:           
        
            self.mqtt_client.publish("kubios-request", Kubios.test_message)
        
    
        
if __name__ == "__main__":
    kubios = Kubios()    
    kubios.test()
    print("start")
    while True:
        time.sleep(0.1)
        
        if kubios.check_response():
            break
        else:
            print("Waiting response")
    return_message = kubios.get_response()
    print("end",return_message)
    