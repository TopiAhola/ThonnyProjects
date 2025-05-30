import network, ujson, time
from umqtt.simple import MQTTClient


class Kubios:
    test_message = '''{ "id": 999,"type": "PPI",
        "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800],
        "analysis": { "type": "readiness" } }'''    
    
    def __init__(self):
        self.response = {}
        self.response_bool = False     
        self.mqtt_client = object
        self.wlan = object
            

    def connect(self):
        #WLAN        
        SSID = "KMD751_Group_3"
        PASSWORD = "topi1234"        
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(SSID, PASSWORD)
        print("WLAN status:", self.wlan.status())
        
        attempt = 0
        while attempt < 5:
            if self.wlan.status() == 3:
                BROKER_IP = "192.168.3.253"
                PORT = 21883        
                self.mqtt_client=MQTTClient("", BROKER_IP, PORT)
                self.mqtt_client.connect(clean_session=True) 
                self.mqtt_client.set_callback(self.response_callback)
                self.mqtt_client.subscribe("kubios-response")
                print("Wlan is connected.")
                break
                
            else:
                print("Wlan is not connected!")
                time.sleep(1)
                attempt = attempt +1
            
        
    def send_request(self, measurement):
        # Forms a MQTT message to publish as request
        message = ujson.dumps(measurement)        
        self.mqtt_client.publish("kubios-request", message)
        
        
        
    def send_request_VANHA_VERSIO2(self, id, type, data):
        # Forms a MQTT message to publish as request
        message = ujson.dumps({"id": id, "type": type,"data": data,"analysis": { "type": "readiness" }})        
        self.mqtt_client.publish("kubios-request", message)
        
        
    def send_request_VANHA_VERSIO1(self, message):
        # Sends a MQTT message. 
        message_str = str(message)
        print("Sending:", message_str)
        self.mqtt_client.publish("kubios-request", message_str)      
        
        
    
    def response_callback(self, topic, message):
        #Saves incoming response
        message_dict = ujson.loads(message)
        self.response = message_dict
        self.response_bool = True
        
    def check_response(self):
        #Checks for MQTT message, saves it at self.response, returns True if message has been saved
        self.mqtt_client.check_msg()
        if self.response_bool:
            return True
        else:
            return False
        
    def get_response(self):
        #Returns and clears self.response
        return_dict = self.response
        self.response = {}
        self.response_bool = False
        return return_dict

    def test(self):
        #Runs a test. Prints error message. Returns True or False if test is succesful 
        print("Kubios test...")
        error_message = "0"
        test_bool = False
        try:
            if self.wlan.status() == 3:        
                self.mqtt_client.publish("kubios-request", Kubios.test_message)
                print("Sending message:", Kubios.test_message)
            else:
                error_message = "Wlan is not connected!"
                print(error_message)
                
            if error_message == "0":
                attempt = 0
                print("attempt:",attempt)
                while attempt < 4:
                    time.sleep(0.5)
                    if self.check_response():
                        response = self.get_response()
                        print(response)
                        break
                    else:
                        attempt = attempt +1
                        
                if response["id"] == 999:
                    error_message = "Kubios connection is working."
                    print(error_message)
                    test_bool = True
                else:
                    error_message = "Kubios response was bad."
                print(response)
            else:
                print("Error message not 0")
        except:
            error_message = "Kubios.test error"
        print(error_message)
        return test_bool
            
        
if __name__ == "__main__":
    
    kubios = Kubios()
    kubios.connect()
    error = kubios.test()
    print("Kubios working:",error)
    
    
    from measurement_example import test_measurement
    kubios.send_request(test_measurement)
    time.sleep(1)
    kubios.check_response()
    time.sleep(1)
    return_message = kubios.get_response()
    print("end",return_message)
    
    
#     print("start")
#     while True:
#         time.sleep(0.1)
#         
#         if kubios.check_response():
#             break
#         else:
#             print("Waiting response")


# 		VANHA2 testaukseen
#     id2 = 222
#     type2 = "PPI"
#     data2 = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]
#     kubios.send_request(id2, type2, data2)
#     time.sleep(1)
#     kubios.check_response()
#     time.sleep(1)
#     return_message = kubios.get_response()
#     print("end",return_message)

    
#     print("Yritys2")
#     kubios.send_request(id2, type2, data2)
#     time.sleep(1)
#     kubios.check_response()
#     return_message = kubios.get_response()
#     print("end",return_message)
    
