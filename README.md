# mqtt-dict
A Python module that wraps a MQTT client into a magical dictionary!

```python
import time
import mqttdict

d = mqttdict.Dict("mqtt.eclipse.org", 1883)

while True:
    try:
        time.sleep(0.1)
        d["fan_on"] = int( float(d["temperature"]) > float(d["setpoint"]) )
    except MissingPayloadError as e:
        print(e)
```
