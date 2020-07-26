import time
import subprocess
from mqttdict.clientdict import ClientDict

host = "127.0.0.1"
port = 1234

class Broker():
    
    def __init__(self):
        self.mosquitto_process = None

    def on(self):
        if self.mosquitto_process == None:
            self.mosquitto_process = subprocess.Popen(["mosquitto","-v","-p",str(port)])

    def off(self):
        try:
            
            self.mosquitto_process.terminate() 
            self.mosquitto_process = None
            print("terminate")
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.off()
        print("exit")

def wait(condition_func, timeout):
    end_time = time.time() + timeout

    while not condition_func() and time.time() < end_time:
        time.sleep(0.05)
    
    return condition_func()

def test_basic():
    with Broker() as broker:
        broker.on()

        c1 = ClientDict(host,port)
        c2 = ClientDict(host,port)

        assert wait( lambda: c1.mqtt_client.is_connected() , 10)
        assert wait( lambda: c2.mqtt_client.is_connected() , 10)

        assert c2["test"] == None

        c1["test"] = 1
        
        assert wait(lambda: c2["test"] == b"1" , 10)
   

def test_subscribe_before_connect():
    with Broker() as broker:
        
        c1 = ClientDict(host,port)
        c2 = ClientDict(host,port)

        assert not c1.mqtt_client.is_connected()
        assert not c2.mqtt_client.is_connected()

        assert c2["test"] == None

        broker.on()

        assert wait( lambda: c1.mqtt_client.is_connected() , 10)
        assert wait( lambda: c2.mqtt_client.is_connected() , 10)
        
        c1["test"] = 1
   
        assert wait(lambda: c2["test"] == b"1" , 10)

