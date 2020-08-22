import time
import subprocess

class Broker():
    
    def __init__(self,port):
        self.port = port
        self.mosquitto_process = None

    def on(self):
        print("Broker On")
        if self.mosquitto_process == None:
            self.mosquitto_process = subprocess.Popen(["mosquitto","-v","-p",str(self.port)])

    def off(self):
        try:
            
            self.mosquitto_process.terminate() 
            self.mosquitto_process = None
            print("Broker Off")
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.off()
        print("exit")



def wait_true(condition_func, timeout):
    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            if condition_func():
                return True
        except:
            pass 
        time.sleep(0.05)
    
    return condition_func()


# def assert_topic_payload(mqtt_dict, topic, payload, timeout=10):
#     end_time = time.time() + timeout
