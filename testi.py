def send_request(self, id="123", type="PPI", data=[]):
    # Forms a MQTT message to publish as request
    message = f"{'id': {id}, 'type": {type},"data": {data},"analysis": { "type": "readiness" }}"


    mqtt_client.publish("kubios-request", message)


