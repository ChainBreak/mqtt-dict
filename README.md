# mqtt-dict
A Python module that wraps a MQTT client into a magical dictionary!


```python
import mqtt-dict

d = mqtt-dict.ClientDict("mqtt.eclipse.org", 1883)

while True:
    if d["temperature"] > d["setpoint"]:
        d["fan_request"] = True
```
