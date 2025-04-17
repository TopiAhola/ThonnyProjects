# Kubios luokka
### Käytetään Kubios analyysin hakemiseen pilvestä

Pääohjelmassa käytetään näin:


    my_kubios = Kubios() #Objektin määrittely
    my_kubios.connect() #Yhdistää WLANiin, kestää 0-4s tulostaa konsoliin mutta ei palauta virheilmoitusta
    error_message = my_kubios.test() #Testaa Kubios-yhteyden testiviestillä. Palauttaa virheilmoituksen.

Kun halutaan saada analyysi:

    my_kubios.send_request(id, type, data): #id = mittauksen numero, type = "PPI", data = lista [] PPI arvoista.
    my_kubios.check_response(): #Päivittää self.response_bool arvon jos response on saapunut.
    my_response = my_kubios.get_response() #Palauttaa responsen ja tyhjentää self.responsen
    print(my_response) # Tulosta response

### Luokan Metodit:

    class Kubios:
        def __init__(self):
            self.response = {} #Kubios response tallennetaan tähän
            self.response_bool = False #Kertoo onko vastausta saatavilla.
            self.mqtt_client = object #Viittaus MQTT luokkaan
            self.wlan = object #Viittaus WLAN luokkaan
    
        def connect(self):
            Yhdistää Picon WLANiin määrittelemällä Kubios.wlan attribuutin.
            Tulostaa konsoliin: "Wlan is connected." tai "Wlan is not connected!"
            Ei palauta mitään.
    
        def send_request(self, id, type, data):
            #id = mittauksen numero, type = "PPI", data = lista [] PPI arvoista.
            #Ei palauta mitään.
    
        def check_response(self):
            #Hakee viestejä MQTT:n kautta.
            #Tallentaa viestin self.response
            #Palauttaa True tai False jos response on saatavilla.
    
        def get_response(self):
            #Palauttaa responsen,
            # tyhjentää self.response ja asettaa self.response_bool = False
    
        def test(self):
            #Ajaa testin, palauttaa virheilmoituksen.
    
        def response_callback(self, topic, message):
            # Tätä ei tarvitse käyttää itse.
            # Saves incoming response to self.response. Sets response_bool = True
            # Ei palauta mitään.
