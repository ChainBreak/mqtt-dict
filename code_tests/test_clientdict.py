import time
import pytest
import subprocess
from mqttdict import MqttDict, MissingPayloadError
from helpers import Broker, wait_true, BackgroundRunner

host = "127.0.0.1"
port = 1235



def test_basic():
    with Broker(port) as broker:
        broker.on()

        c1 = MqttDict(host,port)
        c2 = MqttDict(host,port)

        assert wait_true( lambda: c1.mqtt_client.is_connected() , 10)
        assert wait_true( lambda: c2.mqtt_client.is_connected() , 10)
        
        with pytest.raises(MissingPayloadError):
            c2["test"]

        c1["test"] = 1
        
        assert wait_true(lambda: c2["test"] == b"1" , 10)
   

def test_subscribe_before_connect():
    with Broker(port) as broker:
        
        c1 = MqttDict(host,port)
        c2 = MqttDict(host,port)

        assert not c1.mqtt_client.is_connected()
        assert not c2.mqtt_client.is_connected()

        with pytest.raises(MissingPayloadError):
            c2["test"]

        broker.on()

        assert wait_true( lambda: c1.mqtt_client.is_connected() , 10)
        assert wait_true( lambda: c2.mqtt_client.is_connected() , 10)
        
        c1["test"] = 1
   
        assert wait_true(lambda: c2["test"] == b"1" , 10)


def test_retain():
    with Broker(port) as broker:
        broker.on()

        d1 = MqttDict(host,port)
        d2 = MqttDict(host,port)

        assert wait_true( lambda: d1.mqtt_client.is_connected() , 10)
        assert wait_true( lambda: d2.mqtt_client.is_connected() , 10)

        d1["reatain_test"] = 1

        assert wait_true( lambda: d2["reatain_test"] == b"1" , 10)

        d3 = MqttDict(host,port)
        assert wait_true( lambda: d3.mqtt_client.is_connected() , 10)
        assert wait_true( lambda: d3["reatain_test"] == b"1" , 10)




def test_temperature_example():

    d1 = MqttDict(host,port)
    d2 = MqttDict(host,port)

    def rules():
        try:
            d1["fan_on"] = int(float(d1["temperature"]) > float(d1["setpoint"]))
            time.sleep(0.1)
        except MissingPayloadError:
            pass

    with Broker(port) as broker, BackgroundRunner(rules):
        broker.on()

        assert wait_true( lambda: d1.mqtt_client.is_connected() , 10)
        assert wait_true( lambda: d2.mqtt_client.is_connected() , 10)

        d2["temperature"] = 10
        d2["setpoint"] = 25
        assert wait_true( lambda:  int(d2["fan_on"]) == False)

        d2["temperature"] = 39
        d2["setpoint"] = 24
        assert wait_true( lambda:  int(d2["fan_on"]) == True)


