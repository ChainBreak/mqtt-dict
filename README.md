# mqtt-dict
A Python module that wraps a MQTT client into a magical dictionary!


```python
import mqttdict

d = mqttdict.Dict("mqtt.eclipse.org", 1883)


while True:
    try:
        if d["temperature"] > d["setpoint"]:
            d["fan_request"] = True
    except MissingTopicError as e:
        print(e)

```
