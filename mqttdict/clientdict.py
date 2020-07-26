import paho.mqtt.client as mqtt

class ClientDict():

    def __init__(self,address,port=1883):
        print("init")

    def __getitem__(self,index):
        print(index)

    def __setitem__(self,index,value):
        print(index,value)

