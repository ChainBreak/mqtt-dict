import time
import paho.mqtt.client as mqtt
from .exceptions import MissingPayloadError
import collections

class TopicObject:
     def __init__ (self,topic,payload=None,time=None):
         self.topic = topic
         self.payload = payload
         self.time = time



class MqttDict:

    def __init__(self,*args,**kwargs):
        print("init")
        
        self.topic_object_dict = {}
        self.default_qos = 2

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect_callback
        self.mqtt_client.on_message = self.on_message_callback
        self.mqtt_client.connect_async(*args,**kwargs)
        self.mqtt_client.loop_start()
        
 

    def on_connect_callback(self,client,userdata,flags,rc):
        #when we reconnect to the server we must subscribe to everything
   
        if len(self.topic_object_dict) > 0:
            topic_list = list(self.topic_object_dict.keys())
            qos_list = [self.default_qos]*len(topic_list)

            topic_qos_list = list(zip(topic_list,qos_list))

            self.mqtt_client.subscribe(topic_qos_list)
         


    def on_message_callback(self,client, userdata, msg):
        self.topic_object_dict[msg.topic].payload = msg.payload
        self.topic_object_dict[msg.topic].time = time.time()

    def __getitem__(self,topic):
        
        #check if this topic has a payload
        if topic not in self.topic_object_dict:
            
            #create a new topic object for this topic
            self.topic_object_dict[topic] = TopicObject(topic)

            #if the client is connected then subscribe to this topic
            if self.mqtt_client.is_connected:
                self.mqtt_client.subscribe(topic, self.default_qos)

        if self.topic_object_dict[topic].time is not None:
            return self.topic_object_dict[topic].payload
        
        raise MissingPayloadError(f"The topic '{topic}' does not have a payload yet")
        

        


    def __setitem__(self,topic,payload):
        print("publish")
        self.mqtt_client.publish(topic,payload=payload , qos=self.default_qos, retain=True)
        # self.topic_object_dict[topic] = TopicObject(topic,None,None)


