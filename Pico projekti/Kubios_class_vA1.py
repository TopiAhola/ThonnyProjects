import network, ujson, time
from umqtt.simple import MQTTClient


class Kubios:
    test_message = '''{ "id": 123,"type": "RRI",
        "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800],
        "analysis": { "type": "readiness" } }'''    
    
    def __init__(self)
        self.responses = {}
        
    
    def connect(self):
        #WLAN 
        SSID = "KMD751_Group_3"
        PASSWORD = "topi1234"            
        if wlan.status != 3: #wlan.status() palauttaa verkon tilan           
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.connect(SSID, PASSWORD)       
            
        #Mosquitto client
        if wlan.status == 3:            
            BROKER_IP = "192.168.3.253"
            PORT = 21883
            mqtt_client=MQTTClient("", BROKER_IP, PORT)
            mqtt_client.connect() 
            mqtt_client.set_callback(self.response_callback)
            mqtt_client.subscribe("kubios-response")
        
        else:
            error_message = "WLAN not connected"
        
        return error_message
        
            
        
    def send_request(self, id, type, data)
        # Forms a MQTT message to publish as request
        message = f{ "id": {id}, "type": {type},"data": {data},"analysis": { "type": "readiness" } }     
        mqtt_client.publish("kubios-request", message)
    
    def response_callback(self, topic, message)
        #Saves incoming responses to Kubios.responses dict id used as key
        message_dict = ujson.loads(message)
        self.responses[message_dict["id"]] = message_dict
        
    def has_response(self,id):
        if id in self.responses.keys()
            return True
        else:
            return False
        
    def get_response(self, id):
        return_dict = self.response
        self.response = {}
        return return_dict


