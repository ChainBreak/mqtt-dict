import paho.mqtt.client as mqtt
from .exceptions import MissingPayloadError

class MqttDict():

    def __init__(self,*args,**kwargs):
        print("init")
        
        self.topic_payload_dict = {}
        self.default_qos = 2

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect_callback
        self.mqtt_client.on_message = self.on_message_callback
        self.mqtt_client.connect_async(*args,**kwargs)
        self.mqtt_client.loop_start()
        
 

    def on_connect_callback(self,client,userdata,flags,rc):
        #when we reconnect to the server we must subscribe to everything
        print("connect")
        topic_list = list(self.topic_payload_dict.keys())
        qos_list = [self.default_qos]*len(topic_list)

        topic_qos_list = list(zip(topic_list,qos_list))

        self.mqtt_client.subscribe(topic_qos_list)


    def on_message_callback(self,client, userdata, msg):
        self.topic_payload_dict[msg.topic] = msg.payload

    def __getitem__(self,topic):
        #check if this topic has a payload
        if topic not in self.topic_payload_dict:
            
            self.topic_payload_dict[topic] = None

            #if the client is connected then subscribe to this topic
            if self.mqtt_client.is_connected:
                self.mqtt_client.subscribe(topic, self.default_qos)
            
            raise MissingPayloadError(f"The topic '{topic}' does not have a payload yet")

        if self.topic_payload_dict[topic] == None:
            raise MissingPayloadError(f"The topic '{topic}' does not have a payload yet")

        return self.topic_payload_dict[topic]


    def __setitem__(self,topic,payload):
        print("publish")
        self.mqtt_client.publish(topic,payload=payload , qos=self.default_qos, retain=True)
        self.topic_payload_dict[topic] = payload


