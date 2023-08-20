# mqtt-dahuavto
Play doorbell audio and TTS thru DahuaVTO using MQTT

Configure based on your solution the following settings:

MQTT_BROKER = "192.168.1.10"
MQTT_PORT = 1883
MQTT_TOPIC = "DahuaVTO/ring"  
MQTT_USER = "mqtt"
MQTT_PASSWD = "mqtt"
DAHUA_VTO_IP = "192.168.50.41"
SPEECH_LANGUAGE = "fi"

Whenever you do MQTT Publish with configured topic (default: DahuaVTO/ring) this script reacts to it. 
- If the payload is "ring", generic doorbell sound is played back on Dahua VTO (dootbell_vto.wav).
- If the payload is something else, Google's Text To Speech is called and audio is generated based on the payload in chosen language (default: fi).

  
